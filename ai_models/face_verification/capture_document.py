import os
import cv2

# =========================================================
# SAVE PATH
# =========================================================

SAVE_DIR = os.path.join(
    "data",
    "test_faces",
    "ids"
)

os.makedirs(SAVE_DIR, exist_ok=True)

# =========================================================
# CAPTURE DOCUMENT
# =========================================================

def capture_document(driver_id):

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print("Camera not opened")
        return None

    print("\nDocument Capture Started")
    print("Hold ID card clearly")
    print("Press SPACE to capture")
    print("Press ESC to cancel\n")

    save_path = os.path.join(
        SAVE_DIR,
        f"{driver_id}_id.jpg"
    )

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow(
            "Live Document Capture",
            frame
        )

        key = cv2.waitKey(1)

        # SPACE
        if key == 32:

            cv2.imwrite(
                save_path,
                frame
            )

            print("\nDocument captured successfully ✅")
            print(save_path)

            break

        # ESC
        if key == 27:

            save_path = None
            break

    cap.release()
    cv2.destroyAllWindows()

    return save_path

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    driver_id = input(
        "Enter Driver ID: "
    )

    capture_document(driver_id)