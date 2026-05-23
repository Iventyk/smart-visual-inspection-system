"""Celery task placeholder for CV pipeline execution."""

from datetime import UTC, datetime
from uuid import UUID

from app.core.store import job_store


def run_pipeline_sync(job_id: UUID, payload: bytes) -> None:
    """Prototype synchronous pipeline runner.

    A production implementation should enqueue Celery task and run OpenCV + PyTorch pipeline.
    """
    job = job_store.get_job(job_id)
    if not job:
        return

    job.status = "processing"
    # Placeholder output resembling detection payload.
    job.result = {
        "detections": [
            {
                "label": "person",
                "confidence": 0.9,
                "bbox": {"x": 110, "y": 80, "w": 200, "h": 320},
            }
        ],
        "summary": {
            "total_detections": 1,
            "max_confidence": 0.9,
            "processing_time_ms": 25,
            "payload_size": len(payload),
        },
    }
    job.status = "done"
    job.processed_at = datetime.now(tz=UTC)
