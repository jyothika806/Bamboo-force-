"""
Centralized AI model loading for Bamboo Force AI.

Models are loaded once at application startup and reused across requests.
Existing ai_models packages are not modified — this module wraps them.
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import joblib
import torch
import torch.nn as nn

from ai_models.ride_risk_prediction.autoencoder_model import RideRiskAutoEncoder
from ai_models.video_model.model import VideoModel
from backend.config import Settings, get_settings

logger = logging.getLogger(__name__)

RISK_FEATURE_COLUMNS: List[str] = [
    "aggression_score",
    "driving_stability",
    "emergency_risk",
    "telemetry_reliability",
    "suspicious_route_score",
    "overall_risk_score",
]


@dataclass
class RiskModelBundle:
    model: RideRiskAutoEncoder
    scaler: Any
    feature_columns: List[str]
    device: torch.device
    threshold: float
    criterion: nn.Module


class ModelRegistry:
    """Thread-safe singleton registry for loaded AI models."""

    _instance: Optional["ModelRegistry"] = None
    _init_lock = threading.Lock()

    def __new__(cls) -> "ModelRegistry":
        if cls._instance is None:
            with cls._init_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._registry_lock = threading.RLock()
                    cls._instance._video_model = None
                    cls._instance._risk_bundle = None
                    cls._instance._device = None
                    cls._instance._loaded = False
        return cls._instance

    @property
    def device(self) -> torch.device:
        if self._device is None:
            settings = get_settings()
            if settings.device == "cuda" and torch.cuda.is_available():
                self._device = torch.device("cuda")
            else:
                self._device = torch.device("cpu")
        return self._device

    def load_all(self, settings: Optional[Settings] = None) -> Dict[str, bool]:
        """Load all models. Returns status per model."""
        settings = settings or get_settings()
        status: Dict[str, bool] = {}

        with self._registry_lock:
            status["video_liveness"] = self._load_video_model(settings)
            status["risk_autoencoder"] = self._load_risk_model(settings)
            self._loaded = any(status.values())
        return status

    def _load_video_model(self, settings: Settings) -> bool:
        if self._video_model is not None:
            return True

        path = settings.video_liveness_model_path
        if not path.exists():
            logger.warning(
                "Video liveness model not found at %s — liveness routes may fail",
                path,
            )
            return False

        try:
            model = VideoModel().to(self.device)
            model.load_state_dict(
                torch.load(str(path), map_location=self.device)
            )
            model.eval()
            self._video_model = model
            logger.info("Loaded video liveness model from %s", path)
            return True
        except Exception as exc:
            logger.error("Failed to load video liveness model: %s", exc)
            return False

    def _load_risk_model(self, settings: Settings) -> bool:
        if self._risk_bundle is not None:
            return True

        model_path = settings.risk_autoencoder_path
        scaler_path = settings.risk_scaler_path

        if not model_path.exists() or not scaler_path.exists():
            logger.warning(
                "Risk model artifacts missing (model=%s, scaler=%s)",
                model_path,
                scaler_path,
            )
            return False

        try:
            input_dim = len(RISK_FEATURE_COLUMNS)
            model = RideRiskAutoEncoder(input_dim=input_dim).to(self.device)
            model.load_state_dict(
                torch.load(str(model_path), map_location=self.device)
            )
            model.eval()

            scaler = joblib.load(str(scaler_path))
            self._risk_bundle = RiskModelBundle(
                model=model,
                scaler=scaler,
                feature_columns=RISK_FEATURE_COLUMNS,
                device=self.device,
                threshold=settings.risk_anomaly_threshold,
                criterion=nn.MSELoss(),
            )
            logger.info("Loaded risk autoencoder from %s", model_path)
            return True
        except Exception as exc:
            logger.error("Failed to load risk model: %s", exc)
            return False

    def get_video_model(self) -> Optional[VideoModel]:
        with self._registry_lock:
            if self._video_model is None:
                self._load_video_model(get_settings())
            return self._video_model

    def get_risk_bundle(self) -> Optional[RiskModelBundle]:
        with self._registry_lock:
            if self._risk_bundle is None:
                self._load_risk_model(get_settings())
            return self._risk_bundle

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def health(self) -> Dict[str, Any]:
        return {
            "video_liveness_loaded": self._video_model is not None,
            "risk_model_loaded": self._risk_bundle is not None,
            "device": str(self.device),
        }


def get_model_registry() -> ModelRegistry:
    return ModelRegistry()
