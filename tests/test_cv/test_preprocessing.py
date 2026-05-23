import cv2
import numpy as np
import pytest

from app.cv.preprocessing import preprocess_image


def test_preprocess_image_success() -> None:
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    ok, encoded = cv2.imencode('.png', image)
    assert ok
    out, original = preprocess_image(encoded.tobytes())
    assert out.shape == (640, 640, 3)
    assert original == (300, 300)


def test_preprocess_image_invalid() -> None:
    with pytest.raises(ValueError):
        preprocess_image(b'not-an-image')
