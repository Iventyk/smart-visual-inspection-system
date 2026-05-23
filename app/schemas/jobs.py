"""Pydantic schemas for jobs."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AnalyzeCreateResponse(BaseModel):
    """Response returned when a job is created."""

    job_id: UUID
    status: str


class JobResponse(BaseModel):
    """Detailed job response."""

    job_id: UUID
    status: str
    created_at: datetime | None
    processed_at: datetime | None
    result_json: str | None
    annotated_image_url: str | None
