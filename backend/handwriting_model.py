# ============================================================
# GESTUREX - HANDWRITING CHARACTER RECOGNITION
# A-Z + 0-9
# ============================================================

import cv2
import numpy as np


# ============================================================
# PREPROCESS HANDWRITING
# ============================================================

def preprocess_character(image):

    if image is None:
        return None

    # --------------------------------------------------------
    # Convert to grayscale
    # --------------------------------------------------------

    if len(image.shape) == 3:

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

    else:

        gray = image.copy()

    # --------------------------------------------------------
    # Find non-empty pixels
    # --------------------------------------------------------

    _, threshold = cv2.threshold(
        gray,
        40,
        255,
        cv2.THRESH_BINARY
    )

    coords = cv2.findNonZero(
        threshold
    )

    if coords is None:

        return None

    # --------------------------------------------------------
    # Crop handwriting
    # --------------------------------------------------------

    x, y, w, h = cv2.boundingRect(
        coords
    )

    padding = 20

    x1 = max(
        0,
        x - padding
    )

    y1 = max(
        0,
        y - padding
    )

    x2 = min(
        gray.shape[1],
        x + w + padding
    )

    y2 = min(
        gray.shape[0],
        y + h + padding
    )

    cropped = gray[
        y1:y2,
        x1:x2
    ]

    if cropped.size == 0:

        return None

    # --------------------------------------------------------
    # Make square
    # --------------------------------------------------------

    height, width = cropped.shape

    size = max(
        height,
        width
    )

    square = np.zeros(
        (size, size),
        dtype=np.uint8
    )

    offset_x = (
        size - width
    ) // 2

    offset_y = (
        size - height
    ) // 2

    square[
        offset_y:
        offset_y + height,

        offset_x:
        offset_x + width
    ] = cropped

    # --------------------------------------------------------
    # Resize
    # --------------------------------------------------------

    square = cv2.resize(
        square,
        (28, 28),
        interpolation=cv2.INTER_AREA
    )

    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    square = square.astype(
        np.float32
    ) / 255.0

    return square

def recognize_character(image):
    # your recognition code here
    return {
        "success": False,
        "character": "",
        "confidence": 0,
        "message": "Character recognition model is not trained yet"
    }
# ============================================================
# CREATE FEATURE VECTOR
# ============================================================

def create_features(image):

    processed = preprocess_character(
        image
    )

    if processed is None:

        return None

    return processed.reshape(
        1,
        -1
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "GestureX Handwriting Recognition Module"
    )

    print(
        "Supports A-Z and 0-9 model integration."
    )