"""Analyze endpoint."""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.store import job_store
from app.schemas.jobs import AnalyzeAcceptedResponse
from app.tasks.analyze_task import run_pipeline_sync

router = APIRouter(prefix="/analyze")

ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("", response_model=AnalyzeAcceptedResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze_image(file: UploadFile = File(...)) -> AnalyzeAcceptedResponse:
    """Validate upload and queue analysis job."""
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    data = await file.read()
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # NOTE: simple placeholder dimensions for scaffold phase.
    job = job_store.create_job(filename=file.filename or "uploaded", width=640, height=640, size_bytes=len(data))
    run_pipeline_sync(job.job_id, data)
    return AnalyzeAcceptedResponse(job_id=job.job_id)
