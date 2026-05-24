"""Job management endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.deps import get_current_user
from app.api.v1.analyze import JOBS
from app.schemas.jobs import JobResponse
from app.tasks.analyze_task import celery_app

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


def _refresh(job: dict) -> None:
    ar = celery_app.AsyncResult(job["task_id"])
    if ar.successful() and job["status"] != "done":
        val = ar.result
        job["status"] = "done"
        job["processed_at"] = datetime.now(timezone.utc)
        job["result_json"] = val["result_json"]
        job["annotated"] = bytes.fromhex(val["annotated"])
    elif ar.failed():
        job["status"] = "failed"


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    user: str = Depends(get_current_user), skip: int = 0, limit: int = 20
) -> list[JobResponse]:
    items = [j for j in JOBS.values() if j["user"] == user][
        skip : skip + limit
    ]
    return [
        JobResponse(
            job_id=i["id"],
            status=i["status"],
            created_at=i["created_at"],
            processed_at=i["processed_at"],
            result_json=i["result_json"],
            annotated_image_url=f"/api/v1/jobs/{i['id']}/image",
        )
        for i in items
    ]


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str, user: str = Depends(get_current_user)
) -> JobResponse:
    job = JOBS.get(job_id)
    if not job or job["user"] != user:
        raise HTTPException(status_code=404, detail="Job not found")
    _refresh(job)
    return JobResponse(
        job_id=job_id,
        status=job["status"],
        created_at=job["created_at"],
        processed_at=job["processed_at"],
        result_json=job["result_json"],
        annotated_image_url=f"/api/v1/jobs/{job_id}/image",
    )


@router.get("/{job_id}/image")
async def get_job_image(
    job_id: str, user: str = Depends(get_current_user)
) -> Response:
    job = JOBS.get(job_id)
    if not job or job["user"] != user:
        raise HTTPException(status_code=404, detail="Job not found")
    _refresh(job)
    if not job.get("annotated"):
        raise HTTPException(status_code=409, detail="Image not available")
    return Response(content=job["annotated"], media_type="image/png")


@router.delete("/{job_id}", status_code=204)
async def delete_job(
    job_id: str, user: str = Depends(get_current_user)
) -> None:
    job = JOBS.get(job_id)
    if not job or job["user"] != user:
        raise HTTPException(status_code=404, detail="Job not found")
    del JOBS[job_id]
