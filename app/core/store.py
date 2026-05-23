"""In-memory store used for local development."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass
class Job:
    """Internal job record."""

    job_id: UUID
    created_at: datetime
    status: str = "pending"
    model: str = "fasterrcnn_resnet50_fpn"
    input_data: dict[str, int | str] = field(default_factory=dict)
    result: dict[str, object] = field(default_factory=dict)
    processed_at: datetime | None = None


class JobStore:
    """Thread-unsafe in-memory store for prototype."""

    def __init__(self) -> None:
        self._jobs: dict[UUID, Job] = {}

    def create_job(self, *, filename: str, width: int, height: int, size_bytes: int) -> Job:
        job = Job(
            job_id=uuid4(),
            created_at=datetime.now(tz=UTC),
            input_data={
                "filename": filename,
                "width": width,
                "height": height,
                "size_bytes": size_bytes,
            },
        )
        self._jobs[job.job_id] = job
        return job

    def get_job(self, job_id: UUID) -> Job | None:
        return self._jobs.get(job_id)

    def list_jobs(self, *, offset: int, limit: int) -> list[Job]:
        jobs = list(self._jobs.values())
        return jobs[offset : offset + limit]

    def delete_job(self, job_id: UUID) -> bool:
        return self._jobs.pop(job_id, None) is not None


job_store = JobStore()
