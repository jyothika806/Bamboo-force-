import os
import pickle
import face_recognition

# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(

    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(BASE_DIR)
)

EMBEDDING_DIR = os.path.join(

    PROJECT_ROOT,

    "ai_models",

    "face_verification",

    "embeddings"
)

os.makedirs(

    EMBEDDING_DIR,

    exist_ok=True
)

# =====================================================
# REGISTER DRIVER SERVICE
# =====================================================

def register_driver_service(

    face_path,

    id_path,

    driver_id="DRV_001"
):

    try:

        # =============================================
        # VALIDATE FILES
        # =============================================

        if not os.path.exists(face_path):

            return {

                "success": False,

                "error":
                    "Live face image not found"
            }

        if not os.path.exists(id_path):

            return {

                "success": False,

                "error":
                    "ID proof image not found"
            }

        # =============================================
        # LOAD IMAGES
        # =============================================

        live_img = face_recognition.load_image_file(
            face_path
        )

        id_img = face_recognition.load_image_file(
            id_path
        )

        # =============================================
        # FACE ENCODINGS
        # =============================================

        live_encodings = face_recognition.face_encodings(
            live_img
        )

        id_encodings = face_recognition.face_encodings(
            id_img
        )

        # =============================================
        # VALIDATION
        # =============================================

        if len(live_encodings) == 0:

            return {

                "success": False,

                "error":
                    "No face found in live image"
            }

        if len(id_encodings) == 0:

            return {

                "success": False,

                "error":
                    "No face found in ID proof"
            }

        # =============================================
        # EMBEDDINGS
        # =============================================

        live_embedding = live_encodings[0]

        id_embedding = id_encodings[0]

        # =============================================
        # FACE DISTANCE
        # =============================================

        distance = face_recognition.face_distance(

            [id_embedding],

            live_embedding
        )[0]

        THRESHOLD = 0.75

        # =============================================
        # VERIFIED
        # =============================================

        if distance < THRESHOLD:

            embedding_path = os.path.join(

                EMBEDDING_DIR,

                f"{driver_id}.pkl"
            )

            # =========================================
            # SAVE EMBEDDING
            # =========================================

            with open(

                embedding_path,

                "wb"
            ) as f:

                pickle.dump(

                    live_embedding,

                    f
                )

            return {

                "success": True,

                "registered": True,

                "driver_id": driver_id,

                "embedding_saved": True,

                "distance": float(distance)
            }

        # =============================================
        # FACE MISMATCH
        # =============================================

        else:

            return {

                "success": False,

                "registered": False,

                "error":
                    "Face mismatch",

                "distance":
                    float(distance)
            }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# =====================================================
# VERIFY DRIVER SERVICE
# =====================================================

def verify_driver_service(

    path,

    driver_id="DRV_001"
):

    try:

        # =============================================
        # VALIDATE FILE
        # =============================================

        if not os.path.exists(path):

            return {

                "success": False,

                "error":
                    "Verification image not found"
            }

        # =============================================
        # EMBEDDING FILE
        # =============================================

        embedding_path = os.path.join(

            EMBEDDING_DIR,

            f"{driver_id}.pkl"
        )

        if not os.path.exists(embedding_path):

            return {

                "success": False,

                "error":
                    "Registered embedding not found"
            }

        # =============================================
        # LOAD REGISTERED EMBEDDING
        # =============================================

        with open(

            embedding_path,

            "rb"
        ) as f:

            registered_embedding = pickle.load(f)

        # =============================================
        # LOAD LIVE IMAGE
        # =============================================

        live_img = face_recognition.load_image_file(
            path
        )

        live_encodings = face_recognition.face_encodings(
            live_img
        )

        if len(live_encodings) == 0:

            return {

                "success": False,

                "error":
                    "No face detected"
            }

        live_embedding = live_encodings[0]

        # =============================================
        # FACE DISTANCE
        # =============================================

        distance = face_recognition.face_distance(

            [registered_embedding],

            live_embedding
        )[0]

        THRESHOLD = 0.55

        # =============================================
        # VERIFIED
        # =============================================

        if distance < THRESHOLD:

            return {

                "success": True,

                "verified": True,

                "driver_id": driver_id,

                "distance": float(distance)
            }

        # =============================================
        # FAILED
        # =============================================

        else:

            return {

                "success": False,

                "verified": False,

                "error":
                    "Driver mismatch",

                "distance":
                    float(distance)
            }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }