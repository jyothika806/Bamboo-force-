# backend/routes/face_verification.py
import os
import cv2
import pickle
import shutil
import face_recognition
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse

# Import your liveness logic from your video model system
from ai_models.face_verification.liveness import verify_liveness

router = APIRouter()

# Setup paths relative to this route file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "test_faces")
ID_DIR = os.path.join(DATA_DIR, "ids")
LIVE_DIR = os.path.join(DATA_DIR, "live_faces")
EMBEDDING_DIR = os.path.join(BASE_DIR, "embeddings")

os.makedirs(ID_DIR, exist_ok=True)
os.makedirs(LIVE_DIR, exist_ok=True)
os.makedirs(EMBEDDING_DIR, exist_ok=True)

# =========================================================
# KYC LIVE FACE CAPTURE (Webcam Helper)
# =========================================================
def run_kyc_scan(driver_id: str):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None

    print(f"[INFO] Starting KYC Face Scan for {driver_id}...")
    frame_count = 0
    best_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        # Draw guideline bounding boxes around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(display, (left, top), (right, bottom), (0, 255, 0), 2)

        # Provide directional prompts to the driver to prevent static image loops
        if frame_count < 30:
            text = "LOOK STRAIGHT"
        elif frame_count < 60:
            text = "TURN SLIGHTLY LEFT"
        elif frame_count < 90:
            text = "TURN SLIGHTLY RIGHT"
        else:
            text = "CAPTURING SNAPSHOT..."

        cv2.putText(display, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow("Bamboo Force KYC Capture", display)

        if len(face_locations) > 0:
            best_frame = frame

        frame_count += 1
        if frame_count > 110:
            break

        if cv2.waitKey(1) == 27:  # Stop early if ESC key is pressed
            break

    cap.release()
    cv2.destroyAllWindows()

    if best_frame is None:
        return None

    save_path = os.path.join(LIVE_DIR, f"{driver_id}_live.jpg")
    cv2.imwrite(save_path, best_frame)
    return save_path

# =========================================================
# FASTAPI DRIVER REGISTRATION ROUTE
# =========================================================
@router.post("/register_driver")
async def register_driver(
    driver_id: str = Form(...),
    driver_name: str = Form(...),
    id_image: UploadFile = File(...)
):
    # 1. Trigger the Anti-Spoofing Liveness Evaluation Check
    print(f"[INFO] Triggering Video Model Liveness Validation for: {driver_id}")
    liveness_result = verify_liveness()
    
    if not liveness_result.get("verified"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Anti-Spoofing Security Block",
                "reason": liveness_result.get("message", "Spoofing attempt detected"),
                "confidence": liveness_result.get("confidence", 0.0)
            }
        )

    # 2. Save down the uploaded identification document file securely
    id_path = os.path.join(ID_DIR, f"{driver_id}_id.jpg")
    with open(id_path, "wb") as buffer:
        shutil.copyfileobj(id_image.file, buffer)

    # 3. Fire up the interactive multi-frame KYC scanning utility 
    live_face_path = run_kyc_scan(driver_id)
    if not live_face_path:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="KYC scanning camera sequence failed to isolate a profile frame."
        )

    # 4. Process deep feature face encodings
    id_img = face_recognition.load_image_file(id_path)
    live_img = face_recognition.load_image_file(live_face_path)

    id_encodings = face_recognition.face_encodings(id_img)
    live_encodings = face_recognition.face_encodings(live_img)

    if not id_encodings:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No valid face detected within the uploaded ID image document."
        )
        
    if not live_encodings:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No face detected during the live webcam verification sequence."
        )

    # 5. Execute 128D Spatial Vector Distance Comparison
    biometric_distance = face_recognition.face_distance([id_encodings[0]], live_encodings[0])[0]
    MATCH_THRESHOLD = 0.60  # Standard strict threshold for identity matching

    if biometric_distance <= MATCH_THRESHOLD:
        # Pickle and store reference facial biometric features for secure future lookups
        embedding_path = os.path.join(EMBEDDING_DIR, f"{driver_id}.pkl")
        with open(embedding_path, "wb") as f:
            pickle.dump(live_encodings[0], f)

        return {
            "status": "success",
            "message": "Driver registered securely",
            "driver_id": driver_id,
            "driver_name": driver_name,
            "biometric_distance": round(float(biometric_distance), 4),
            "liveness_confidence": liveness_result.get("confidence")
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Identity Verification Failed",
                "message": "Facial characteristics from ID do not match the live user profile.",
                "biometric_distance": round(float(biometric_distance), 4)
            }
        )