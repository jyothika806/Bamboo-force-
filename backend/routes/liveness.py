"""
Liveness detection API routes — thin layer over LivenessService.
"""

import os
import shutil

from fastapi import APIRouter, File, UploadFile

from backend.config import get_settings
from backend.services.liveness_service import liveness_service

router = APIRouter()
settings = get_settings()


@router.post("/check")
async def check(file: UploadFile = File(...)):
    settings.ensure_directories()
    path = str(settings.temp_dir / f"liveness_{file.filename}")

    try:
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = liveness_service.check_liveness(path)
        return {"success": True, "data": result}

    except Exception as exc:
        return {"success": False, "error": str(exc)}

    finally:
        if os.path.exists(path):
            os.remove(path)
