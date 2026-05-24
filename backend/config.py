"""
Central configuration for Bamboo Force AI backend.
Loads settings from environment variables and .env file.
"""

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Bamboo Force AI"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"

    host: str = "0.0.0.0"
    port: int = 8000

    cors_origins: List[str] = Field(default_factory=lambda: ["*"])

    device: str = "cpu"

    video_liveness_model_path: Path = Field(
        default=PROJECT_ROOT / "video_liveness_model.pth"
    )
    risk_autoencoder_path: Path = Field(
        default=PROJECT_ROOT
        / "ai_models"
        / "ride_risk_prediction"
        / "checkpoints"
        / "autoencoder.pth"
    )
    risk_scaler_path: Path = Field(
        default=PROJECT_ROOT
        / "ai_models"
        / "ride_risk_prediction"
        / "checkpoints"
        / "scaler.save"
    )
    risk_anomaly_threshold: float = 0.000537

    camera_index: int = 0
    camera_max_kyc_frames: int = 110

    # Liveness detection settings
    liveness_threshold: float = 0.3
    allow_low_confidence_liveness: bool = False

    face_data_dir: Path = Field(
        default=PROJECT_ROOT / "backend" / "data" / "test_faces"
    )
    face_embedding_dir: Path = Field(
        default=PROJECT_ROOT
        / "ai_models"
        / "face_verification"
        / "embeddings"
    )

    temp_dir: Path = Field(default=PROJECT_ROOT / "backend" / "temp")

    ride_expiry_seconds: int = 3600
    ride_state_path: Path = Field(
        default=PROJECT_ROOT / "backend" / "data" / "ride_state.json"
    )

    @property
    def face_id_dir(self) -> Path:
        return self.face_data_dir / "ids"

    @property
    def face_live_dir(self) -> Path:
        return self.face_data_dir / "live_faces"

    def ensure_directories(self) -> None:
        for path in (
            self.temp_dir,
            self.face_data_dir,
            self.face_id_dir,
            self.face_live_dir,
            self.face_embedding_dir,
            self.ride_state_path.parent,
        ):
            path.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
