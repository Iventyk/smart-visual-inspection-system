"""Celery task for asynchronous analysis."""

from celery import Celery

from app.core.config import settings
from app.cv.pipeline import analyze_image_bytes

celery_app = Celery("svis", broker=settings.redis_url, backend=settings.redis_url)


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def analyze_task(self, payload: bytes) -> dict:
    """Execute pipeline in background worker."""
    result_json, annotated = analyze_image_bytes(payload)
    return {"result_json": result_json, "annotated": annotated.hex()}
