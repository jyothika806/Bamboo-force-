import os
import cv2
import pickle
import face_recognition
from ai_models.face_verification.liveness import verify_liveness
# =========================================================
# EMBEDDING PATH
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EMBEDDING_DIR = os.path.join(
    BASE_DIR,
    "embeddings"
)

# =========================================================
# LOAD ASSIGNED DRIVER EMBEDDING
# =========================================================

def load_driver_embedding(driver_id):

    path = os.path.join(
        EMBEDDING_DIR,
        f"{driver_id}.pkl"
    )

    if not os.path.exists(path):

        print("Assigned driver embedding not found")
        return None

    with open(path, "rb") as f:
        embedding = pickle.load(f)

    return embedding

# =========================================================
# LIVE DRIVER SCAN
# =========================================================

def scan_driver_face():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print("Camera could not open")
        return None

    print("\nPassenger Verification Started")
    print("Press SPACE to scan driver")
    print("Press ESC to cancel\n")

    captured_frame = None

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow(
            "Verify Assigned Driver",
            frame
        )

        key = cv2.waitKey(1)

        # SPACE KEY
        if key == 32:

            captured_frame = frame
            break

        # ESC KEY
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return captured_frame

# =========================================================
# VERIFY ASSIGNED DRIVER
# =========================================================

def verify_assigned_driver(driver_id):

    # ============================================
    # LOAD REGISTERED EMBEDDING
    # ============================================

    registered_embedding = load_driver_embedding(
        driver_id
    )

    if registered_embedding is None:
        return

    # ============================================
    # LIVE SCAN
    # ============================================

    frame = scan_driver_face()

    if frame is None:

        print("Live scan failed")
        return

    # ============================================
    # CONVERT BGR → RGB
    # ============================================

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # ============================================
    # FACE ENCODING
    # ============================================
    # ============================================
    # LIVENESS CHECK
    # ============================================

    liveness_result = verify_liveness()

    if not liveness_result["verified"]:

        print("Spoof attack detected")
        return

    encodings = face_recognition.face_encodings(
        rgb_frame
    )

    if len(encodings) == 0:

        print("No face detected")
        return

    live_embedding = encodings[0]

    # ============================================
    # FACE DISTANCE
    # ============================================

    distance = face_recognition.face_distance(
        [registered_embedding],
        live_embedding
    )[0]

    THRESHOLD = 0.55

    print(f"\nFace Distance: {distance:.4f}")

    # ============================================
    # RESULT
    # ============================================

    if distance < THRESHOLD:

        print("\nAUTHORIZED DRIVER ✅")
        print("Ride verified successfully")

    else:

        print("\nUNAUTHORIZED DRIVER ❌")
        print("Ride blocked")

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    assigned_driver_id = input(
        "Enter Assigned Driver ID: "
    )

    verify_assigned_driver(
        assigned_driver_id
    )