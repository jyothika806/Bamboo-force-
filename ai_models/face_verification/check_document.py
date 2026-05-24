import os
import cv2
import face_recognition

# =========================================================
# IMAGE PATH
# =========================================================

image_path = os.path.join(
    "data",
    "test_faces",
    "ids",
    "DR001_id.jpg"
)

# =========================================================
# CHECK FILE EXISTS
# =========================================================

if not os.path.exists(image_path):

    print("Document image not found")
    raise SystemExit

# =========================================================
# LOAD IMAGE
# =========================================================

image = cv2.imread(image_path)

if image is None:

    print("Invalid image")
    raise SystemExit

# =========================================================
# IMAGE SIZE CHECK
# =========================================================

h, w, _ = image.shape

print(f"Width: {w}")
print(f"Height: {h}")

if w < 300 or h < 300:

    print("Low quality document")
    exit()

# =========================================================
# BLUR CHECK
# =========================================================

gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

blur_score = cv2.Laplacian(
    gray,
    cv2.CV_64F
).var()

print(f"Blur Score: {blur_score:.2f}")

if blur_score < 50:

    print("Blurry document")
    exit()

# =========================================================
# FACE DETECTION
# =========================================================

rgb = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2RGB
)

faces = face_recognition.face_locations(rgb)

print("Faces Found:", len(faces))

if len(faces) == 0:

    print("No face found in document")
    exit()

# =========================================================
# DOCUMENT VALID
# =========================================================

print("\nValid document image ✅")