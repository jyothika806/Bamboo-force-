import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from .. import __init__  # (optional, ensures package awareness)
from ai_models.face_verification.encode import encode_face
from ai_models.face_verification.compare import compare_faces

stored_encoding = None  # temporary storage


def register_driver(image_path):
    global stored_encoding

    encoding = encode_face(image_path)

    if encoding is None:
        return {"success": False, "message": "Face not detected properly"}

    stored_encoding = encoding
    return {"success": True, "message": "Driver registered"}


def verify_driver(image_path):
    global stored_encoding

    if stored_encoding is None:
        return {"success": False, "message": "No driver registered"}

    test_encoding = encode_face(image_path)

    if test_encoding is None:
        return {"success": False, "message": "Face not detected"}

    result = compare_faces(stored_encoding, test_encoding)

    return {
        "success": True,
        "verified": result["verified"],
        "confidence": result["confidence"],
        "distance": result["distance"],
    }