"""
Singleton webcam manager for Bamboo Force AI.

Prevents multiple concurrent VideoCapture(0) instances that cause
device locks and resource leaks during driver registration / KYC.
"""

from __future__ import annotations

import logging
import threading
from contextlib import contextmanager
from typing import Generator, Optional, Tuple

import cv2

from backend.config import get_settings

logger = logging.getLogger(__name__)


class CameraManager:
    """Thread-safe singleton for webcam access."""

    _instance: Optional["CameraManager"] = None
    _init_lock = threading.Lock()

    def __new__(cls) -> "CameraManager":
        if cls._instance is None:
            with cls._init_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._capture = None
                    cls._instance._access_lock = threading.RLock()
                    cls._instance._camera_index = get_settings().camera_index
        return cls._instance

    def configure(self, camera_index: Optional[int] = None) -> None:
        with self._access_lock:
            if camera_index is not None:
                self._camera_index = camera_index

    def _open_capture(self) -> cv2.VideoCapture:
        cap = cv2.VideoCapture(self._camera_index)
        if not cap.isOpened():
            raise RuntimeError(
                f"Cannot open camera at index {self._camera_index}"
            )
        return cap

    @contextmanager
    def session(self) -> Generator[cv2.VideoCapture, None, None]:
        """
        Context manager: opens camera, yields capture, always releases.
        Only one session runs at a time (serialized by lock).
        """
        with self._access_lock:
            cap = self._open_capture()
            try:
                yield cap
            finally:
                cap.release()
                cv2.destroyAllWindows()
                logger.debug("Camera session released")

    def read_frame(self) -> Tuple[bool, Optional[object]]:
        """Capture a single frame (opens and closes camera)."""
        with self.session() as cap:
            return cap.read()

    def capture_to_file(self, output_path: str) -> Optional[str]:
        """Capture one frame and save to disk."""
        ret, frame = self.read_frame()
        if not ret or frame is None:
            logger.error("Failed to capture frame from camera")
            return None
        cv2.imwrite(output_path, frame)
        logger.info("Captured image saved to %s", output_path)
        return output_path

    def is_available(self) -> bool:
        try:
            with self.session() as cap:
                ret, _ = cap.read()
                return ret
        except Exception as exc:
            logger.warning("Camera availability check failed: %s", exc)
            return False


def get_camera_manager() -> CameraManager:
    return CameraManager()
