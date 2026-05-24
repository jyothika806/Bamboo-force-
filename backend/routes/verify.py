"""
Face verification API routes — thin layer over FaceVerificationService.
"""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from backend.services.face_verification_service import (
    face_verification_service,
)

router = APIRouter()


def _raise_from_service(result: dict) -> None:
    if result.get("success"):
        return
    status_code = result.get("status_code", 400)
    detail = result.get("detail", result)
    raise HTTPException(status_code=status_code, detail=detail)


@router.post("/register_driver")
async def register_driver(
    driver_id: str = Form(...),
    driver_name: str = Form(...),
    id_image: UploadFile = File(...),
    live_image: UploadFile = File(...),
):
    result = await face_verification_service.register_driver(
        driver_id=driver_id,
        driver_name=driver_name,
        id_image=id_image,
        live_image=live_image,
    )
    _raise_from_service(result)
    return result


@router.post("/register")
async def register_driver_alias(
    driver_id: str = Form(...),
    driver_name: str = Form(...),
    id_image: UploadFile = File(...),
    live_image: UploadFile = File(...),
):
    """Alias for frontend compatibility."""
    return await register_driver(driver_id, driver_name, id_image, live_image)


@router.post("/verify")
async def verify_driver(
    driver_id: str = Form(...),
    live_image: UploadFile = File(...),
):
    result = await face_verification_service.verify_driver_upload(
        driver_id=driver_id,
        live_image=live_image,
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=result,
        )
    return {"success": True, "data": result}
