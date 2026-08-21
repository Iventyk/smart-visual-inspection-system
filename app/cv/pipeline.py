"""Main CV pipeline orchestration."""

import json
import time

import numpy as np
import torch

from app.core.config import settings
from app.cv.inference import run_inference
from app.cv.postprocessing import (
    MODEL_CATEGORY_COUNT,
    annotate_image,
    build_detections,
)
from app.cv.preprocessing import preprocess_image


def analyze_image_bytes(image_bytes: bytes) -> tuple[str, bytes]:
    """Run full CV pipeline and return JSON result plus annotated PNG bytes."""
    started = time.perf_counter()
    image, (orig_w, orig_h) = preprocess_image(image_bytes)
    image_rgb = image[:, :, ::-1].astype(np.float32) / 255.0
    tensor = torch.from_numpy(image_rgb).permute(2, 0, 1)
    pred = run_inference(tensor)
    detections = build_detections(
        pred, threshold=settings.detection_confidence_threshold
    )
    annotated = annotate_image(image, detections)
    elapsed = int((time.perf_counter() - started) * 1000)
    elapsed_seconds = elapsed / 1000 if elapsed else 0
    throughput = 60 / elapsed_seconds if elapsed_seconds else 0
    categories = sorted({d["label"] for d in detections})
    mean_confidence = (
        sum(d["confidence"] for d in detections) / len(detections)
        if detections
        else 0.0
    )
    result = {
        "input": {
            "width": orig_w,
            "height": orig_h,
            "size_bytes": len(image_bytes),
        },
        "results": {
            "detections": detections,
            "summary": {
                "total_detections": len(detections),
                "max_confidence": max(
                    (d["confidence"] for d in detections), default=0.0
                ),
                "processing_time_ms": elapsed,
                "processing_time_sec": round(elapsed_seconds, 3),
                "throughput_images_per_min": round(throughput, 2),
                "detection_accuracy_percent": round(mean_confidence * 100, 2),
                "detected_category_count": len(categories),
                "detected_categories": categories,
                "detection_confidence_threshold": (
                    settings.detection_confidence_threshold
                ),
                "detection_confidence_threshold_percent": round(
                    settings.detection_confidence_threshold * 100, 2
                ),
                "model_category_count": MODEL_CATEGORY_COUNT,
            },
        },
    }
    return json.dumps(result), annotated
