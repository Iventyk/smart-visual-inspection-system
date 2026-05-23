"""Jobs CRUD endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import JSONResponse

from app.core.store import job_store
from app.schemas.jobs import JobResultResponse

router = APIRouter(prefix="/jobs")


@router.get("/{job_id}", response_model=JobResultResponse)
async def get_job(job_id: UUID) -> JobResultResponse:
    """Get single job status and result."""
    job = job_store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResultResponse(
        job_id=job.job_id,
        status=job.status,
        created_at=job.created_at,
        processed_at=job.processed_at,
        model=job.model,
        input=job.input_data,
        results=job.result,
        annotated_image_url=f"/api/v1/jobs/{job.job_id}/image" if job.status == "done" else None,
    )


@router.get("", response_model=list[JobResultResponse])
async def list_jobs(offset: int = Query(default=0, ge=0), limit: int = Query(default=20, ge=1, le=100)) -> list[JobResultResponse]:
    """List user jobs with pagination."""
    items = []
    for job in job_store.list_jobs(offset=offset, limit=limit):
        items.append(
            JobResultResponse(
                job_id=job.job_id,
                status=job.status,
                created_at=job.created_at,
                processed_at=job.processed_at,
                model=job.model,
                input=job.input_data,
                results=job.result,
                annotated_image_url=f"/api/v1/jobs/{job.job_id}/image" if job.status == "done" else None,
            )
        )
    return items


@router.get("/{job_id}/image")
async def get_annotated_image(job_id: UUID) -> Response:
    """Return placeholder annotated image metadata."""
    job = job_store.get_job(job_id)
    if not job or job.status != "done":
        raise HTTPException(status_code=404, detail="Annotated image not available")
    return JSONResponse({"message": "annotated image stored in object storage", "job_id": str(job_id)})


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: UUID) -> Response:
    """Delete job and linked files."""
    if not job_store.delete_job(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    return Response(status_code=204)
