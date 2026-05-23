"""OpenCV preprocessing utilities."""

import cv2
import numpy as np


MIN_SIZE = 224
MAX_SIZE = 4096


def preprocess_image(data: bytes, target_size: int = 640) -> tuple[np.ndarray, tuple[int, int]]:
    """Validate and preprocess image bytes."""
    arr = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image format")
    h, w = image.shape[:2]
    if h < MIN_SIZE or w < MIN_SIZE or h > MAX_SIZE or w > MAX_SIZE:
        raise ValueError("Image dimensions out of allowed range")
    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    scale = min(target_size / w, target_size / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (nw, nh))
    canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    top = (target_size - nh) // 2
    left = (target_size - nw) // 2
    canvas[top : top + nh, left : left + nw] = resized
    return canvas, (w, h)
