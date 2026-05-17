import os
import cv2
import pickle
import face_recognition
from flask import Blueprint, request, jsonify

register_bp = Blueprint("register_driver", __name__)

# =========================================================
# PATHS
# =========================================================

BASE_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DATA_DIR, "data", "test_faces")
ID_DIR = os.path.join(DATA_DIR, "ids")
LIVE_DIR = os.path.join(DATA_DIR, "live_faces")

EMBEDDING_DIR = os.path.join(BASE_DATA_DIR, "embeddings")

os.makedirs(ID_DIR, exist_ok=True)
os.makedirs(LIVE_DIR, exist_ok=True)
os.makedirs(EMBEDDING_DIR, exist_ok=True)

# =========================================================
# KYC LIVE FACE SCAN
# =========================================================

def run_kyc_scan(driver_id):

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return None

    print("KYC Scan Started")
    print("Look Straight at Camera")

    frame_count = 0
    best_frame = None

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        display = frame.copy()

        # Face detection
        face_locations = face_recognition.face_locations(frame)

        # Draw rectangles
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(
                display,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

        # Instructions
        if frame_count < 30:
            text = "LOOK STRAIGHT"
        elif frame_count < 60:
            text = "TURN LEFT"
        elif frame_count < 90:
            text = "TURN RIGHT"
        else:
            text = "CAPTURING..."

        cv2.putText(
            display,
            text,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow("KYC Verification", display)

        # Save best frame
        if len(face_locations) > 0:
            best_frame = frame

        frame_count += 1

        # Auto capture
        if frame_count > 100:
            break

        # ESC to cancel
        key = cv2.waitKey(1)

        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    if best_frame is None:
        return None

    save_path = os.path.join(
        LIVE_DIR,
        f"{driver_id}_live.jpg"
    )

    cv2.imwrite(save_path, best_frame)

    return save_path

# =========================================================
# REGISTER DRIVER API
# =========================================================

@register_bp.route("/register_driver", methods=["POST"])
def register_driver():

    try:

        # =================================================
        # FORM DATA
        # =================================================

        driver_id = request.form.get("driver_id")
        driver_name = request.form.get("driver_name")

        id_image = request.files.get("id_image")

        # =================================================
        # VALIDATION
        # =================================================

        if not driver_id or not driver_name:
            return jsonify({
                "success": False,
                "message": "Missing driver details"
            }), 400

        if not id_image:
            return jsonify({
                "success": False,
                "message": "ID image required"
            }), 400

        # =================================================
        # SAVE ID IMAGE
        # =================================================

        id_path = os.path.join(
            ID_DIR,
            f"{driver_id}_id.jpg"
        )

        id_image.save(id_path)

        # =================================================
        # RUN LIVE KYC SCAN
        # =================================================

        live_face_path = run_kyc_scan(driver_id)

        if live_face_path is None:
            return jsonify({
                "success": False,
                "message": "KYC scan failed"
            })

        # =================================================
        # LOAD IMAGES
        # =================================================

        id_img = face_recognition.load_image_file(id_path)
        live_img = face_recognition.load_image_file(live_face_path)

        # =================================================
        # FACE ENCODINGS
        # =================================================

        id_encodings = face_recognition.face_encodings(id_img)
        live_encodings = face_recognition.face_encodings(live_img)
        
        print("ID Faces Found:", len(id_encodings))
        print("Live Faces Found:", len(live_encodings))
        if len(id_encodings) == 0:
            return jsonify({
                "success": False,
                "message": "No face found in ID image"
            })

        if len(live_encodings) == 0:
            return jsonify({
                "success": False,
                "message": "No face found during KYC scan"
            })

        id_embedding = id_encodings[0]
        live_embedding = live_encodings[0]

        # =================================================
        # FACE COMPARISON
        # =================================================

        distance = face_recognition.face_distance(
            [id_embedding],
            live_embedding
        )[0]

        THRESHOLD = 0.75
        print("Face Distance:", distance)
        # =================================================
        # VERIFIED
        # =================================================

        if distance < THRESHOLD:

            embedding_path = os.path.join(
                EMBEDDING_DIR,
                f"{driver_id}.pkl"
            )
            print("Saving embedding...")
            print(embedding_path)
            with open(embedding_path, "wb") as f:
                pickle.dump(live_embedding, f)

            return jsonify({
                "success": True,
                "message": "Driver verified successfully",
                "driver_id": driver_id,
                "driver_name": driver_name,
                "distance": float(distance)
            })

        # =================================================
        # FAILED
        # =================================================

        else:

            return jsonify({
                "success": False,
                "message": "Face mismatch",
                "distance": float(distance)
            })
        
        


    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500