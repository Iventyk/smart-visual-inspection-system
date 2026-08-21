"""Postprocessing helpers: filtering, annotation, summary."""

import cv2
import numpy as np

# COCO class id groups used by torchvision Faster R-CNN.
PERSON_LABELS = {1}
TRANSPORT_LABELS = {2, 3, 4, 5, 6, 7, 8, 9}
ANIMAL_LABELS = {16, 17, 18, 19, 20, 21, 22, 23, 24, 25}

COCO_LABELS = {
    1: "person",
    2: "bicycle",
    3: "car",
    4: "motorcycle",
    5: "airplane",
    6: "bus",
    7: "train",
    8: "truck",
    9: "boat",
    10: "traffic light",
    11: "fire hydrant",
    13: "stop sign",
    14: "parking meter",
    15: "bench",
    16: "bird",
    17: "cat",
    18: "dog",
    19: "horse",
    20: "sheep",
    21: "cow",
    22: "elephant",
    23: "bear",
    24: "zebra",
    25: "giraffe",
    27: "backpack",
    28: "umbrella",
    31: "handbag",
    32: "tie",
    33: "suitcase",
    34: "frisbee",
    35: "skis",
    36: "snowboard",
    37: "sports ball",
    38: "kite",
    39: "baseball bat",
    40: "baseball glove",
    41: "skateboard",
    42: "surfboard",
    43: "tennis racket",
    44: "bottle",
    46: "wine glass",
    47: "cup",
    48: "fork",
    49: "knife",
    50: "spoon",
    51: "bowl",
    52: "banana",
    53: "apple",
    54: "sandwich",
    55: "orange",
    56: "broccoli",
    57: "carrot",
    58: "hot dog",
    59: "pizza",
    60: "donut",
    61: "cake",
    62: "chair",
    63: "couch",
    64: "potted plant",
    65: "bed",
    67: "dining table",
    70: "toilet",
    72: "tv",
    73: "laptop",
    74: "mouse",
    75: "remote",
    76: "keyboard",
    77: "cell phone",
    78: "microwave",
    79: "oven",
    80: "toaster",
    81: "sink",
    82: "refrigerator",
    84: "book",
    85: "clock",
    86: "vase",
    87: "scissors",
    88: "teddy bear",
    89: "hair drier",
    90: "toothbrush",
}
MODEL_CATEGORY_COUNT = len(COCO_LABELS)

# OpenCV uses BGR color order.
COLOR_PERSON = (0, 0, 255)  # red
COLOR_TRANSPORT = (0, 255, 0)  # green
COLOR_ANIMAL = (255, 0, 0)  # blue
COLOR_DEFAULT = (0, 255, 255)  # yellow for other classes


def label_name(label_id: int) -> str:
    """Return a human-readable COCO label name."""
    return COCO_LABELS.get(label_id, f"class {label_id}")


def _pick_color(label_id: int) -> tuple[int, int, int]:
    """Return color by coarse object category."""

    if label_id in PERSON_LABELS:
        return COLOR_PERSON
    if label_id in TRANSPORT_LABELS:
        return COLOR_TRANSPORT
    if label_id in ANIMAL_LABELS:
        return COLOR_ANIMAL
    return COLOR_DEFAULT


def build_detections(pred: dict, threshold: float = 0.5) -> list[dict]:
    """Convert raw predictions to API detection objects."""
    boxes = (
        pred["boxes"].cpu().numpy()
        if len(pred.get("boxes", []))
        else np.empty((0, 4))
    )
    scores = (
        pred["scores"].cpu().numpy()
        if len(pred.get("scores", []))
        else np.empty((0,))
    )
    labels = (
        pred["labels"].cpu().numpy()
        if len(pred.get("labels", []))
        else np.empty((0,))
    )
    out: list[dict] = []
    for box, score, label in zip(boxes, scores, labels):
        if score < threshold:
            continue
        label_id = int(label)
        x1, y1, x2, y2 = box.tolist()
        out.append(
            {
                "label_id": label_id,
                "label": label_name(label_id),
                "confidence": float(score),
                "confidence_percent": round(float(score) * 100, 2),
                "bbox": {
                    "x": int(x1),
                    "y": int(y1),
                    "w": int(x2 - x1),
                    "h": int(y2 - y1),
                },
            }
        )
    return out


def annotate_image(image: np.ndarray, detections: list[dict]) -> bytes:
    """Draw boxes and readable labels and return PNG bytes."""
    annotated = image.copy()
    for det in detections:
        x = det["bbox"]["x"]
        y = det["bbox"]["y"]
        w = det["bbox"]["w"]
        h = det["bbox"]["h"]
        color = _pick_color(det["label_id"])
        caption = f"{det['label']} {det['confidence_percent']:.1f}%"
        cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
        cv2.putText(
            annotated,
            caption,
            (x, max(16, y - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1,
        )
    ok, encoded = cv2.imencode(".png", annotated)
    if not ok:
        raise ValueError("Failed to encode annotated image")
    return encoded.tobytes()
