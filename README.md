# Smart Visual Inspection System (SVIS)

A backend service for **object detection and tracking on images/video**
(vehicles, people, animals) using FastAPI and a CV pipeline.

## Project status

This repository currently contains a production-oriented scaffold:
- API v1 endpoints (`/analyze`, `/jobs`, `/models`, `/auth`, `/health`)
- Pydantic response schemas for job lifecycle payloads
- A prototype analysis pipeline runner (placeholder for Celery/OpenCV/PyTorch)
- Basic API smoke tests

## Domain choice

This implementation targets the domain:
**Object detection and tracking for transportation, people, and animals**.

## Development run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Swagger UI: `http://127.0.0.1:8000/docs`

## Next implementation steps

1. Replace in-memory store with PostgreSQL models and repository layer.
2. Replace synchronous `run_pipeline_sync` with Celery task execution.
3. Integrate object storage (MinIO/S3) for original and annotated files.
4. Add JWT auth with persistent users and access control.
5. Expand tests to cover analyze/jobs/auth happy and error paths.
