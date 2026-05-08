import logging
import os
import face_recognition
import cv2
import numpy as np

logger = logging.getLogger(__name__)

def encode_face(
    image_path,
    model="small",
    num_jitters=1,
    resize_to=800,
):
    """
    Encodes a face image into a normalized 128-dimensional embedding vector.

    Args:
        image_path (str): Path to the input face image.
        model (str): Encoding model to use. Options are "small" (faster) or "large" (more accurate). Default is "small".
        num_jitters (int): Number of times to re-sample the face when calculating encoding.
                           Higher values improve accuracy but increase processing time. Default is 1.
        resize_to (int): Maximum size (in pixels) for the longer side of the image.
                         Image is resized proportionally if larger than this value. Default is 800.

    Returns:
        np.ndarray or None:
            A normalized 128-dimensional embedding vector if exactly one face is detected.
            Returns None if:
                - image does not exist
                - image cannot be loaded
                - no face is detected
                - multiple faces are detected
                - any processing error occurs
    """

    # Check if image file exists
    if not os.path.exists(image_path):
        logger.warning("Image does not exist: %s", image_path)
        return None

    try:
        # Load image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            logger.warning("Failed to decode image: %s", image_path)
            return None

        # Resize image if it is too large (for performance optimization)
        h, w = image.shape[:2]
        if resize_to and max(h, w) > resize_to:
            scale = resize_to / max(h, w)
            image = cv2.resize(image, (int(w * scale), int(h * scale)))

        # Convert BGR (OpenCV format) to RGB (required by face_recognition)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        del image  # free memory

        # Detect face locations using HOG model (CPU-friendly)
        face_locations = face_recognition.face_locations(rgb, model="hog")

        # Ensure exactly one face is detected (important for verification systems)
        if len(face_locations) != 1:
            logger.warning(
                "Expected 1 face, found %d in %s",
                len(face_locations),
                image_path,
            )
            return None

        # Generate face encoding (128-d vector)
        encodings = face_recognition.face_encodings(
            rgb,
            face_locations,
            model=model,
            num_jitters=num_jitters,
        )
        del rgb  # free memory

        # Check if encoding was generated
        if len(encodings) == 0:
            logger.info("No encoding generated for: %s", image_path)
            return None

        # Convert encoding to numpy array (float32 for efficiency)
        encoding = np.array(encodings[0], dtype=np.float32, copy=True)
        del encodings

        # Normalize encoding (important for stable comparison)
        norm = np.linalg.norm(encoding)
        if norm == 0:
            logger.warning("Zero norm encoding: %s", image_path)
            return None

        encoding = encoding / norm

        return encoding

    except Exception as e:
        # Log full exception for debugging
        logger.exception("Error encoding face from %s: %s", image_path, e)
        return None