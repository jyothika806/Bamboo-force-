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
    exit()

# =========================================================
# LOAD IMAGE
# =========================================================

image = face_recognition.load_image_file(
    image_path
)

# =========================================================
# DETECT FACE
# =========================================================

face_locations = face_recognition.face_locations(
    image
)

print("Faces Found:", len(face_locations))

if len(face_locations) == 0:

    print("No face found")
    exit()

# =========================================================
# EXTRACT FACE
# =========================================================

top, right, bottom, left = face_locations[0]

face_image = image[
    top:bottom,
    left:right
]

# =========================================================
# RGB → BGR
# =========================================================

face_image = cv2.cvtColor(
    face_image,
    cv2.COLOR_RGB2BGR
)

# =========================================================
# SAVE FACE
# =========================================================

output_path = os.path.join(
    "data",
    "test_faces",
    "cropped_face.jpg"
)

cv2.imwrite(
    output_path,
    face_image
)

print("\nFace extracted successfully ✅")
print(f"Saved at: {output_path}")