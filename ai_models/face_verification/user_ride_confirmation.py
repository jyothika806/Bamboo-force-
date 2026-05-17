import os
import cv2
import pickle
import face_recognition

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

EMBEDDING_DIR = os.path.join(
    BASE_DIR,
    "embeddings"
)

# =========================================================
# LOAD DRIVER EMBEDDING
# =========================================================

def load_driver_embedding(driver_id):

    embedding_path = os.path.join(
        EMBEDDING_DIR,
        f"{driver_id}.pkl"
    )

    if not os.path.exists(embedding_path):

        print("Driver embedding not found")
        return None

    with open(embedding_path, "rb") as f:

        embedding = pickle.load(f)

    return embedding

# =========================================================
# SCAN ARRIVING DRIVER
# =========================================================

def scan_driver():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print("Camera not opened")
        return None

    print("\nRide Confirmation Started")
    print("Scan arriving driver")
    print("Press SPACE to capture")
    print("Press ESC to cancel\n")

    frame_capture = None

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow(
            "User Ride Confirmation",
            frame
        )

        key = cv2.waitKey(1)

        # SPACE
        if key == 32:

            frame_capture = frame
            break

        # ESC
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return frame_capture

# =========================================================
# VERIFY DRIVER
# =========================================================

def verify_driver_for_ride(driver_id):

    # ============================================
    # LOAD ASSIGNED DRIVER
    # ============================================

    registered_embedding = load_driver_embedding(
        driver_id
    )

    if registered_embedding is None:
        return

    # ============================================
    # LIVE SCAN
    # ============================================

    frame = scan_driver()

    if frame is None:

        print("Verification cancelled")
        return

    # ============================================
    # BGR → RGB
    # ============================================

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # ============================================
    # FACE ENCODING
    # ============================================

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

    print(f"\nFace Distance: {distance}")

    THRESHOLD = 0.55
    

    # ============================================
    # RESULT
    # ============================================

    if distance < THRESHOLD:

        print("\nRIDE VERIFIED ✅")
        print("Authorized driver confirmed")

    else:

        print("\nRIDE BLOCKED ❌")
        print("Unauthorized driver detected")

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    assigned_driver_id = input(
        "Enter Assigned Driver ID: "
    )

    verify_driver_for_ride(
        assigned_driver_id
    )