"""
Face verification service — orchestrates registration and verification.

Wraps existing face_service logic and ai_models.face_verification.liveness
while routing all camera access through CameraManager.
"""

from __future__ import annotations

import os
import pickle
import shutil
from typing import Any, Dict, Optional

import cv2
import face_recognition
from fastapi import UploadFile

from ai_models.face_verification.liveness import verify_liveness
from backend.config import get_settings
from backend.core.camera_manager import get_camera_manager
from backend.services.face_service import (
    register_driver_service,
    verify_driver_service,
)


class FaceVerificationService:
    """Orchestrates driver KYC registration and face verification."""

    MATCH_THRESHOLD = 0.60

    def __init__(self) -> None:
        settings = get_settings()
        settings.ensure_directories()
        self._settings = settings
        self._camera = get_camera_manager()

    def run_kyc_scan(self, driver_id: str) -> Optional[str]:
        """
        Interactive multi-frame KYC capture using singleton camera manager.
        """
        save_path = str(
            self._settings.face_live_dir / f"{driver_id}_live.jpg"
        )
        frame_count = 0
        best_frame = None
        max_frames = self._settings.camera_max_kyc_frames

        with self._camera.session() as cap:
            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                display = frame.copy()
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)

                for top, right, bottom, left in face_locations:
                    cv2.rectangle(
                        display,
                        (left, top),
                        (right, bottom),
                        (0, 255, 0),
                        2,
                    )

                if frame_count < 30:
                    text = "LOOK STRAIGHT"
                elif frame_count < 60:
                    text = "TURN SLIGHTLY LEFT"
                elif frame_count < 90:
                    text = "TURN SLIGHTLY RIGHT"
                else:
                    text = "CAPTURING SNAPSHOT..."

                cv2.putText(
                    display,
                    text,
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2,
                )
                cv2.imshow("Bamboo Force KYC Capture", display)

                if face_locations:
                    best_frame = frame

                frame_count += 1
                if cv2.waitKey(1) == 27:
                    break

        if best_frame is None:
            return None

        cv2.imwrite(save_path, best_frame)
        return save_path

    async def register_driver(
        self,
        driver_id: str,
        driver_name: str,
        id_image: UploadFile,
        live_image: UploadFile,
    ) -> Dict[str, Any]:
        """Full registration pipeline: ID save → live face save → embedding.
        
        Uses browser-uploaded media as primary source.
        Server webcam (CameraManager) is kept only as fallback for local development.
        """
        # Save ID proof image
        id_path = str(
            self._settings.face_id_dir / f"{driver_id}_id.jpg"
        )
        with open(id_path, "wb") as buffer:
            shutil.copyfileobj(id_image.file, buffer)

        # Save live face image from browser camera
        live_face_path = str(
            self._settings.face_live_dir / f"{driver_id}_live.jpg"
        )
        with open(live_face_path, "wb") as buffer:
            shutil.copyfileobj(live_image.file, buffer)

        # Generate embedding using browser-uploaded face
        result = register_driver_service(
            face_path=live_face_path,
            id_path=id_path,
            driver_id=driver_id,
        )

        if not result.get("success"):
            return {
                "success": False,
                "status_code": 403,
                "detail": result,
            }

        return {
            "success": True,
            "status": "success",
            "message": "Driver registered securely",
            "driver_id": driver_id,
            "driver_name": driver_name,
            "biometric_distance": result.get("distance"),
        }

    def verify_driver(
        self,
        verification_image_path: str,
        driver_id: str = "DRV_001",
    ) -> Dict[str, Any]:
        """Verify a driver face against stored embedding."""
        return verify_driver_service(
            path=verification_image_path,
            driver_id=driver_id,
        )

    async def verify_driver_upload(
        self,
        driver_id: str,
        live_image: UploadFile,
    ) -> Dict[str, Any]:
        """Verify driver from uploaded live image."""
        temp_path = str(
            self._settings.temp_dir / f"verify_{driver_id}_{live_image.filename}"
        )
        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(live_image.file, buffer)
            return self.verify_driver(temp_path, driver_id=driver_id)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


face_verification_service = FaceVerificationService()
