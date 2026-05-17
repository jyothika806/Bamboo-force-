from fastapi import APIRouter, UploadFile, File

import shutil
import os

from backend.services.liveness_service import (
    check_liveness
)

router = APIRouter()

# =====================================================
# LIVENESS CHECK
# =====================================================

@router.post("/check")

async def check(

    file: UploadFile = File(...)
):

    path = (
        f"temp_liveness_{file.filename}"
    )

    try:

        # =============================================
        # SAVE FRAME
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
        # AI LIVENESS CHECK
        # =============================================

        result = check_liveness(path)

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
        # CLEAN TEMP FILE
        # =============================================

        if os.path.exists(path):

            os.remove(path)