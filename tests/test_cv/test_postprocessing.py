import json

import cv2
import pytest
import numpy as np
import torch

from app.cv.pipeline import analyze_image_bytes
from app.cv.postprocessing import annotate_image, build_detections


def test_build_detections_uses_readable_labels_and_percentages() -> None:
    pred = {
        "boxes": torch.tensor([[1.0, 2.0, 11.0, 22.0]]),
        "scores": torch.tensor([0.9876]),
        "labels": torch.tensor([1]),
    }

    detections = build_detections(pred)

    assert detections == [
        {
            "label_id": 1,
            "label": "person",
            "confidence": pytest.approx(0.9876),
            "confidence_percent": 98.76,
            "bbox": {"x": 1, "y": 2, "w": 10, "h": 20},
        }
    ]


def test_annotate_image_accepts_named_detection() -> None:
    image = np.zeros((80, 80, 3), dtype=np.uint8)
    detections = [
        {
            "label_id": 3,
            "label": "car",
            "confidence": 0.9,
            "confidence_percent": 90.0,
            "bbox": {"x": 10, "y": 20, "w": 30, "h": 25},
        }
    ]

    annotated = annotate_image(image, detections)
    decoded = cv2.imdecode(
        np.frombuffer(annotated, np.uint8), cv2.IMREAD_COLOR
    )

    assert decoded is not None
    assert decoded.shape == image.shape
    assert decoded.sum() > 0


def test_pipeline_summary_includes_evaluation_metrics(monkeypatch) -> None:
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    ok, encoded = cv2.imencode(".png", image)
    assert ok

    def fake_inference(_tensor: torch.Tensor) -> dict:
        return {
            "boxes": torch.tensor([[1.0, 2.0, 11.0, 22.0]]),
            "scores": torch.tensor([0.75]),
            "labels": torch.tensor([3]),
        }

    monkeypatch.setattr("app.cv.pipeline.run_inference", fake_inference)

    result_json, _ = analyze_image_bytes(encoded.tobytes())
    result = json.loads(result_json)
    summary = result["results"]["summary"]

    assert summary["detection_accuracy_percent"] == 75.0
    assert summary["detected_category_count"] == 1
    assert summary["detected_categories"] == ["car"]
    assert summary["detection_confidence_threshold"] == 0.7
    assert summary["detection_confidence_threshold_percent"] == 70.0
    assert summary["model_category_count"] == 80
    assert summary["processing_time_ms"] >= 0
    assert "throughput_images_per_min" in summary


def test_pipeline_filters_detections_below_configured_threshold(
    monkeypatch,
) -> None:
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    ok, encoded = cv2.imencode(".png", image)
    assert ok

    def fake_inference(_tensor: torch.Tensor) -> dict:
        return {
            "boxes": torch.tensor([[1.0, 2.0, 11.0, 22.0]]),
            "scores": torch.tensor([0.69]),
            "labels": torch.tensor([3]),
        }

    monkeypatch.setattr("app.cv.pipeline.run_inference", fake_inference)

    result_json, _ = analyze_image_bytes(encoded.tobytes())
    result = json.loads(result_json)
    summary = result["results"]["summary"]

    assert result["results"]["detections"] == []
    assert summary["total_detections"] == 0
