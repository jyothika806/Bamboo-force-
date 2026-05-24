"""
Video liveness detection service.

Uses centralized ModelRegistry — does not reload model from disk per request.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

import cv2
import numpy as np
import torch

from backend.config import get_settings
from backend.core.model_registry import get_model_registry

logger = logging.getLogger(__name__)


class LivenessService:
    """Wraps video_model inference via ModelRegistry."""

    MAX_FRAMES = 10
    FRAME_SIZE = (112, 112)

    def __init__(self) -> None:
        self._settings = get_settings()
        self._threshold = self._settings.liveness_threshold
        self._allow_low_confidence = self._settings.allow_low_confidence_liveness

    @staticmethod
    def calculate_brightness(frame: np.ndarray) -> float:
        """Calculate average brightness of a frame (0-255)."""
        if len(frame.shape) == 3:
            return float(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)))
        return float(np.mean(frame))

    @staticmethod
    def normalize_brightness(frame: np.ndarray, target_brightness: float = 128.0) -> np.ndarray:
        """Normalize frame brightness to target value."""
        current_brightness = LivenessService.calculate_brightness(frame)
        if current_brightness < 1.0:
            return frame
        factor = target_brightness / current_brightness
        adjusted = cv2.convertScaleAbs(frame, alpha=factor, beta=0)
        return np.clip(adjusted, 0, 255).astype(np.uint8)

    @staticmethod
    def preprocess_frames(frames: List[np.ndarray]) -> torch.Tensor:
        """Preprocess frames with brightness normalization and consistent resizing."""
        processed = []
        for frame in frames:
            # Normalize brightness
            normalized = LivenessService.normalize_brightness(frame)
            # Ensure consistent resize
            resized = cv2.resize(normalized, LivenessService.FRAME_SIZE)
            processed.append(resized)
        
        frames_arr = np.array(processed) / 255.0
        tensor = torch.tensor(frames_arr).float()
        return tensor.permute(0, 3, 1, 2)

    def check_liveness(self, video_path: str) -> Dict[str, Any]:
        """Check liveness with enhanced logging and configurable threshold."""
        try:
            registry = get_model_registry()
            model = registry.get_video_model()
            
            # Fallback when model is unavailable
            if model is None:
                logger.warning("Video liveness model not available - using fallback mode")
                # In fallback mode, accept the liveness check but log it
                return {
                    "is_live": True,
                    "prediction": "REAL",
                    "confidence": 0.0,
                    "threshold": self._threshold,
                    "fallback_mode": True,
                    "warning": "Model unavailable - fallback mode active",
                }
            
            device = registry.device

            cap = cv2.VideoCapture(video_path)
            frames: List[np.ndarray] = []
            brightness_values = []

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_small = cv2.resize(frame, self.FRAME_SIZE)
                frames.append(frame_small)
                brightness_values.append(self.calculate_brightness(frame_small))
                if len(frames) >= self.MAX_FRAMES:
                    break

            cap.release()

            if len(frames) < self.MAX_FRAMES:
                logger.warning(f"Not enough frames captured: {len(frames)}/{self.MAX_FRAMES}")
                return {
                    "is_live": False,
                    "error": "Not enough frames captured",
                }

            # Log brightness statistics
            avg_brightness = np.mean(brightness_values)
            logger.info(f"Frame count: {len(frames)}, Average brightness: {avg_brightness:.2f}")

            input_tensor = self.preprocess_frames(frames)
            input_tensor = input_tensor.unsqueeze(0).to(device)

            with torch.no_grad():
                output = model(input_tensor)
                probabilities = torch.softmax(output, dim=1)
                confidence, prediction = torch.max(probabilities, dim=1)
                confidence = confidence.item()
                prediction = prediction.item()

            # Log prediction details
            logger.info(f"Raw prediction: {prediction}, Confidence: {confidence:.4f}, Threshold: {self._threshold}")

            # Development override mode
            if self._allow_low_confidence:
                logger.warning("Development override: ALLOW_LOW_CONFIDENCE_LIVENESS is True - accepting all liveness checks")
                return {
                    "is_live": True,
                    "prediction": "REAL",
                    "confidence": confidence,
                    "threshold": self._threshold,
                    "override_mode": True,
                }

            # Normal decision logic with threshold
            if prediction == 1 and confidence >= self._threshold:
                logger.info(f"Liveness check PASSED: {confidence:.4f} >= {self._threshold}")
                return {
                    "is_live": True,
                    "prediction": "REAL",
                    "confidence": confidence,
                    "threshold": self._threshold,
                }

            logger.warning(f"Liveness check FAILED: prediction={prediction}, confidence={confidence:.4f} < {self._threshold}")
            return {
                "is_live": False,
                "prediction": "SPOOF",
                "confidence": confidence,
                "threshold": self._threshold,
            }

        except RuntimeError as exc:
            logger.error(f"Runtime error in liveness check: {exc}")
            return {"is_live": False, "error": str(exc)}
        except Exception as exc:
            logger.error(f"Unexpected error in liveness check: {exc}")
            return {"is_live": False, "error": str(exc)}


liveness_service = LivenessService()


def check_liveness(video_path: str) -> Dict[str, Any]:
    """Backward-compatible function used by routes."""
    return liveness_service.check_liveness(video_path)
