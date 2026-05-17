import cv2
import torch
import numpy as np

from ai_models.video_model import model
from ai_models.video_model.model import (
    VideoModel
)

# =====================================================
# DEVICE
# =====================================================

device = torch.device("cpu")

# =====================================================
# LOAD MODEL
# =====================================================

model = VideoModel().to(device)

model.load_state_dict(
    torch.load(


        "video_liveness_model.pth",


        map_location=device
    )
)

model.eval()

# =====================================================
# PREPROCESS FRAMES
# =====================================================

def preprocess_frames(frames):

    frames = np.array(frames) / 255.0

    frames = torch.tensor(frames).float()

    # (T,H,W,C) -> (T,C,H,W)

    frames = frames.permute(

        0,

        3,

        1,

        2
    )

    return frames

# =====================================================
# CHECK LIVENESS
# =====================================================

def check_liveness(video_path):

    try:

        cap = cv2.VideoCapture(video_path)

        frames = []

        MAX_FRAMES = 10

        # =============================================
        # EXTRACT FRAMES
        # =============================================

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_small = cv2.resize(

                frame,

                (112, 112)
            )

            frames.append(frame_small)

            if len(frames) >= MAX_FRAMES:
                break

        cap.release()

        # =============================================
        # VALIDATION
        # =============================================

        if len(frames) < MAX_FRAMES:

            return {

                "is_live": False,

                "error":
                    "Not enough frames captured"
            }

        # =============================================
        # PREPROCESS
        # =============================================

        input_tensor = preprocess_frames(
            frames
        )

        input_tensor = input_tensor.unsqueeze(0)

        input_tensor = input_tensor.to(device)

        # =============================================
        # MODEL INFERENCE
        # =============================================

        with torch.no_grad():

            output = model(input_tensor)

            prediction = torch.argmax(

                output,

                dim=1
            ).item()

        # =============================================
        # REAL
        # =============================================

        if prediction == 1:

            return {

                "is_live": True,

                "prediction":
                    "REAL"
            }

        # =============================================
        # SPOOF
        # =============================================

        else:

            return {

                "is_live": False,

                "prediction":
                    "SPOOF"
            }

    except Exception as e:

        return {

            "is_live": False,

            "error": str(e)
        }