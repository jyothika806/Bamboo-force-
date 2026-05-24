"""Core infrastructure: model registry, camera manager."""

from backend.core.camera_manager import CameraManager, get_camera_manager
from backend.core.model_registry import ModelRegistry, get_model_registry

__all__ = [
    "CameraManager",
    "get_camera_manager",
    "ModelRegistry",
    "get_model_registry",
]
