from fastapi import APIRouter, UploadFile, File

import shutil
import os

from backend.services.face_service import (
    register_driver_service,
    verify_driver_service
)

router = APIRouter()

# =====================================================
# DRIVER REGISTRATION
# =====================================================

@router.post("/register")

async def register(

    file: UploadFile = File(...),

    id_proof: UploadFile = File(...)
):

    face_path = (
        f"temp_face_{file.filename}"
    )

    id_path = (
        f"temp_id_{id_proof.filename}"
    )

    try:

        # =============================================
        # SAVE LIVE FACE FRAME
        # =============================================

        with open(

            face_path,

            "wb"
        ) as buffer:

            shutil.copyfileobj(

                file.file,

                buffer
            )

        # =============================================
        # SAVE ID PROOF
        # =============================================

        with open(

            id_path,

            "wb"
        ) as buffer:

            shutil.copyfileobj(

                id_proof.file,

                buffer
            )

        # =============================================
        # AI PROCESSING
        # =============================================

        result = register_driver_service(

            face_path,

            id_path
        )

        return {

            "success": True,

            "data": result
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

    finally:

        # =============================================
        # CLEAN TEMP FILES
        # =============================================

        if os.path.exists(face_path):

            os.remove(face_path)

        if os.path.exists(id_path):

            os.remove(id_path)
# =====================================================
# VERIFY DRIVER
# =====================================================

@router.post("/verify")

async def verify(

    file: UploadFile = File(...)
):

    path = f"temp_{file.filename}"

    try:

        # =============================================
        # SAVE LIVE IMAGE
        # =============================================

        with open(

            path,

            "wb"
        ) as buffer:

            shutil.copyfileobj(

                file.file,

                buffer
            )

        # =============================================
        # AI VERIFICATION
        # =============================================

        result = verify_driver_service(
            path
        )

        return result

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

    finally:

        # =============================================
        # CLEAN TEMP FILE
        # =============================================

        if os.path.exists(path):

            os.remove(path)