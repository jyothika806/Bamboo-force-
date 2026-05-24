"""
Video liveness detection service.

Uses centralized ModelRegistry — does not reload model from disk per request.
"""

from __future__ import annotations

from typing import Any, Dict, List

import cv2
import numpy as np
import torch

from backend.config import get_settings
from backend.core.model_registry import get_model_registry


class LivenessService:
    """Wraps video_model inference via ModelRegistry."""

    MAX_FRAMES = 10
    FRAME_SIZE = (112, 112)

    def __init__(self) -> None:
        self._settings = get_settings()

    @staticmethod
    def preprocess_frames(frames: List[np.ndarray]) -> torch.Tensor:
        frames_arr = np.array(frames) / 255.0
        tensor = torch.tensor(frames_arr).float()
        return tensor.permute(0, 3, 1, 2)

    def check_liveness(self, video_path: str) -> Dict[str, Any]:
        try:
            registry = get_model_registry()
            model = registry.get_video_model()
            device = registry.device

            cap = cv2.VideoCapture(video_path)
            frames: List[np.ndarray] = []

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_small = cv2.resize(frame, self.FRAME_SIZE)
                frames.append(frame_small)
                if len(frames) >= self.MAX_FRAMES:
                    break

            cap.release()

            if len(frames) < self.MAX_FRAMES:
                return {
                    "is_live": False,
                    "error": "Not enough frames captured",
                }

            input_tensor = self.preprocess_frames(frames)
            input_tensor = input_tensor.unsqueeze(0).to(device)

            with torch.no_grad():
                output = model(input_tensor)
                prediction = torch.argmax(output, dim=1).item()

            if prediction == 1:
                return {"is_live": True, "prediction": "REAL"}

            return {"is_live": False, "prediction": "SPOOF"}

        except RuntimeError as exc:
            return {"is_live": False, "error": str(exc)}
        except Exception as exc:
            return {"is_live": False, "error": str(exc)}


liveness_service = LivenessService()


def check_liveness(video_path: str) -> Dict[str, Any]:
    """Backward-compatible function used by routes."""
    return liveness_service.check_liveness(video_path)
