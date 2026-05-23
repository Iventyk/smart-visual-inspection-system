"""Pydantic schemas for jobs."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class AnalyzeAcceptedResponse(BaseModel):
    """Analyze API response when job was queued."""

    job_id: UUID
    status: Literal["pending"] = "pending"


class JobResultResponse(BaseModel):
    """Serialized analysis result."""

    job_id: UUID
    status: Literal["pending", "processing", "done", "failed"]
    created_at: datetime
    processed_at: datetime | None = None
    model: str
    input: dict[str, int | str]
    results: dict[str, object] = Field(default_factory=dict)
    annotated_image_url: str | None = None
