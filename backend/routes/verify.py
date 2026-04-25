from fastapi import APIRouter, UploadFile, File
import shutil
import os
from backend.services.face_service import register_driver, verify_driver

router = APIRouter()


@router.post("/register")
async def register(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = register_driver(path)

    os.remove(path)  # clean temp file
    return result


@router.post("/verify")
async def verify(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = verify_driver(path)

    os.remove(path)
    return result