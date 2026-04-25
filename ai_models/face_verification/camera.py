import cv2
import logging

logger = logging.getLogger(__name__)


def capture_image(output_path="captured.jpg"):
    """
    Capture a single image from webcam and save it.

    Args:
        output_path (str): File path to save captured image.

    Returns:
        str or None:
            Path of saved image if successful, else None.
    """

    try:
        # Open default camera (0)
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            logger.error("Cannot access camera")
            return None

        # Capture frame
        ret, frame = cam.read()
        cam.release()

        if not ret:
            logger.error("Failed to capture image")
            return None

        # Save image
        cv2.imwrite(output_path, frame)

        logger.info("Image captured: %s", output_path)
        return output_path

    except Exception as e:
        logger.exception("Camera error: %s", e)
        return None
