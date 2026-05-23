"""Analyze endpoint."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.deps import get_current_user
from app.core.config import settings
from app.schemas.jobs import AnalyzeCreateResponse
from app.tasks.analyze_task import analyze_task

router = APIRouter(prefix="/api/v1", tags=["analyze"])
JOBS: dict[str, dict] = {}


@router.post("/analyze", response_model=AnalyzeCreateResponse)
async def analyze_image(
    file: UploadFile = File(...),
    user: str = Depends(get_current_user),
) -> AnalyzeCreateResponse:
    """Validate upload and enqueue CV analysis task."""
    data = await file.read()
    if file.content_type not in settings.allowed_mime_types:
        raise HTTPException(status_code=400, detail="Unsupported MIME type")
    if len(data) > settings.max_file_size_bytes:
        raise HTTPException(status_code=400, detail="File too large")
    job_id = str(uuid.uuid4())
    async_result = analyze_task.delay(data)
    JOBS[job_id] = {
        "id": job_id,
        "user": user,
        "task_id": async_result.id,
        "status": "pending",
        "filename": file.filename,
        "created_at": datetime.now(timezone.utc),
        "processed_at": None,
        "result_json": None,
        "annotated": None,
    }
    return AnalyzeCreateResponse(job_id=job_id, status="pending")
