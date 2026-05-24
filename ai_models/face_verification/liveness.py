import cv2
import torch
import numpy as np

from ai_models.video_model.model import VideoModel


# =====================================================
# DEVICE
# =====================================================

device = torch.device("cpu")


# =====================================================
# LOAD MODEL
# =====================================================
# =====================================================
# LOAD LIVENESS MODEL
# =====================================================

def load_liveness_model():

    model = VideoModel().to(device)

    model.load_state_dict(
        torch.load(
            "video_liveness_model.pth",
            map_location=device
        )
    )

    model.eval()
    return model


# =====================================================
# PREPROCESS
# =====================================================

def preprocess_frames(frames):

    frames = np.array(frames) / 255.0

    frames = torch.tensor(frames).float()

    frames = frames.permute(0, 3, 1, 2)

    return frames


# =====================================================
# VERIFY LIVENESS
# =====================================================

def verify_liveness():
    model = load_liveness_model()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        return {
            "verified": False,
            "message": "Camera not accessible"
        }

    buffer = []

    MAX_FRAMES = 10

    print("\nLiveness Detection Started")
    print("Look at camera...\n")

    try:

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_small = cv2.resize(
                frame,
                (112, 112)
            )

            buffer.append(frame_small)

            if len(buffer) > MAX_FRAMES:
                buffer.pop(0)

            cv2.imshow(
                "Liveness Detection",
                frame
            )

            if len(buffer) == MAX_FRAMES:

                input_tensor = preprocess_frames(
                    buffer
                )

                input_tensor = input_tensor.unsqueeze(0)

                input_tensor = input_tensor.to(device)

                with torch.no_grad():

                    output = model(input_tensor)

                    
                    
                    probabilities = torch.softmax(
                        output,
                        dim=1
                    )

                    confidence, prediction = torch.max(
                        probabilities,
                        dim=1
                    )

                    prediction = prediction.item()

                    confidence = confidence.item()
                # =====================================
                # REAL
                # =====================================

                if prediction == 1:

                    return {
                        "verified": True,
                        "label": "REAL",
                        "confidence": round(confidence, 2)
                    }

                # =====================================
                # SPOOF
                # =====================================

                else:

                    return {
                        "verified": False,
                        "label": "SPOOF",
                        "confidence": round(confidence, 2),
                        "message": "Spoof detected"
                    }

            key = cv2.waitKey(1)

            if key == ord("q"):
                break

    finally:

        cap.release()

        cv2.destroyAllWindows()

    return {
        "verified": False,
        "message": "Liveness failed"
    }