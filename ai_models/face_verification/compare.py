import numpy as np
import logging

logger = logging.getLogger(__name__)


def compare_faces(known_encoding, test_encoding, threshold=0.5):
    """
    Compare two face embeddings and return verification result with confidence.

    Args:
        known_encoding (np.ndarray): Stored face embedding of the registered user.
        test_encoding (np.ndarray): New face embedding to verify.
        threshold (float): Distance threshold for deciding match (lower = stricter).

    Returns:
        dict:
            {
                "verified": bool,
                "distance": float or None,
                "confidence": float
            }
    """

    try:
        # 🔹 Validate inputs (must not be None)
        if known_encoding is None or test_encoding is None:
            logger.warning("One or both encodings are None")
            return {
                "verified": False,
                "distance": None,
                "confidence": 0.0,
            }

        # 🔹 Ensure inputs are numpy arrays (important for math operations)
        known_encoding = np.asarray(known_encoding, dtype=np.float32)
        test_encoding = np.asarray(test_encoding, dtype=np.float32)

        # 🔹 Check if both encodings have same shape (should be 128-d)
        if known_encoding.shape != test_encoding.shape:
            logger.warning(
                "Encoding shape mismatch: %s vs %s",
                known_encoding.shape,
                test_encoding.shape,
            )
            return {
                "verified": False,
                "distance": None,
                "confidence": 0.0,
            }

        # 🔹 Compute Euclidean distance between embeddings
        # Smaller distance → more similar faces
        distance = np.linalg.norm(known_encoding - test_encoding)

        # 🔹 Handle invalid numerical results (NaN or Inf)
        if np.isnan(distance) or np.isinf(distance):
            logger.warning("Invalid distance computed")
            return {
                "verified": False,
                "distance": None,
                "confidence": 0.0,
            }

        # 🔹 Convert distance into confidence score
        # Using exponential mapping for smoother scaling (0 to 1 range)
        confidence = float(np.exp(-distance))

        # 🔹 Final decision: compare distance with threshold
        verified = distance < threshold

        # 🔹 Log result (useful for debugging and monitoring)
        logger.info(
            "Face comparison | Distance: %.4f | Confidence: %.4f | Verified: %s",
            distance,
            confidence,
            verified,
        )

        # 🔹 Return structured result
        return {
            "verified": bool(verified),
            "distance": float(distance),
            "confidence": confidence,
        }

    except Exception as e:
        # 🔹 Catch unexpected errors and log full traceback
        logger.exception("Error during face comparison: %s", e)

        return {
            "verified": False,
            "distance": None,
            "confidence": 0.0,
        }