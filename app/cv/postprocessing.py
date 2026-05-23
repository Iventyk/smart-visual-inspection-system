"""Postprocessing helpers: filtering, annotation, summary."""

import cv2
import numpy as np


def build_detections(pred: dict, threshold: float = 0.5) -> list[dict]:
    """Convert raw predictions to API detection objects."""
    boxes = pred["boxes"].cpu().numpy() if len(pred.get("boxes", [])) else np.empty((0, 4))
    scores = pred["scores"].cpu().numpy() if len(pred.get("scores", [])) else np.empty((0,))
    labels = pred["labels"].cpu().numpy() if len(pred.get("labels", [])) else np.empty((0,))
    out: list[dict] = []
    for box, score, label in zip(boxes, scores, labels):
        if score < threshold:
            continue
        x1, y1, x2, y2 = box.tolist()
        out.append({"label": str(int(label)), "confidence": float(score), "bbox": {"x": int(x1), "y": int(y1), "w": int(x2-x1), "h": int(y2-y1)}})
    return out


def annotate_image(image: np.ndarray, detections: list[dict]) -> bytes:
    """Draw boxes and labels and return PNG bytes."""
    annotated = image.copy()
    for det in detections:
        x = det["bbox"]["x"]
        y = det["bbox"]["y"]
        w = det["bbox"]["w"]
        h = det["bbox"]["h"]
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(annotated, f"{det['label']}:{det['confidence']:.2f}", (x, max(10, y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    ok, encoded = cv2.imencode('.png', annotated)
    if not ok:
        raise ValueError("Failed to encode annotated image")
    return encoded.tobytes()
