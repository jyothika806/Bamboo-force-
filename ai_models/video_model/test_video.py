import cv2
import torch
import numpy as np

from ai_models.video_model.model import VideoModel
def main():
    # =========================================================
    # DEVICE
    # =========================================================

    device = torch.device("cpu")

    # =========================================================
    # LOAD MODEL
    # =========================================================

    model = VideoModel().to(device)

    model.load_state_dict(
        torch.load(
            "video_liveness_model.pth",
            map_location=device
        )
    )

    model.eval()

    # =========================================================
    # PREPROCESS
    # =========================================================

    def preprocess_frames(frames):

        frames = np.array(frames) / 255.0

        frames = torch.tensor(frames).float()

        # (T,H,W,C) -> (T,C,H,W)
        frames = frames.permute(0, 3, 1, 2)

        return frames

    # =========================================================
    # CAMERA
    # =========================================================

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not accessible")
        return

    print("Press Q to quit")

    # =========================================================
    # FRAME BUFFER
    # =========================================================

    buffer = []

    MAX_FRAMES = 10

    # =========================================================
    # MAIN LOOP
    # =========================================================
    try:
        while True:

            ret, frame = cap.read()

            if not ret:
                break

            # Resize
            frame_small = cv2.resize(frame, (112, 112))

            buffer.append(frame_small)

            # Keep fixed buffer
            if len(buffer) > MAX_FRAMES:
                buffer.pop(0)

            # Predict only when buffer full
            if len(buffer) == MAX_FRAMES:

                input_tensor = preprocess_frames(buffer)

                input_tensor = input_tensor.unsqueeze(0)

                input_tensor = input_tensor.to(device)

                with torch.no_grad():

                    output = model(input_tensor)

                    prediction = torch.argmax(output, dim=1).item()

                # =================================================
                # LABELS
                # =================================================

                if prediction == 1:
                    text = "REAL"
                    color = (0, 255, 0)

                else:
                    text = "SPOOF"
                    color = (0, 0, 255)

                cv2.putText(
                    frame,
                    text,
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    color,
                    2
                )

            # =====================================================
            # SHOW
            # =====================================================

            cv2.imshow("Video Liveness Detection", frame)

            key = cv2.waitKey(1)

            if key == ord("q"):
                break
    finally:

        cap.release()

        cv2.destroyAllWindows()
        # =========================================================
    # CLEANUP
    # =========================================================

    
if __name__ == "__main__":
    
    main()