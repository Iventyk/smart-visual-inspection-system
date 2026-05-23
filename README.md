# Smart Visual Inspection System

Domain: **Object detection and tracking in camera streams (transport, people, animals)**.

## Stack
- Python 3.11+
- FastAPI + Celery + Redis
- OpenCV + PyTorch / torchvision
- Docker Compose

## Architecture
Client -> FastAPI -> Redis/Celery -> CV Pipeline -> Result API

## Run
```bash
docker compose up --build
```

## API
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/token`
- `POST /api/v1/analyze`
- `GET /api/v1/jobs/{job_id}`
- `GET /api/v1/jobs/{job_id}/image`
- `GET /api/v1/jobs`
- `DELETE /api/v1/jobs/{job_id}`
- `GET /api/v1/models`
- `GET /health`

Docs available at `/docs`.

## Quality
Run locally:
```bash
pytest --cov=app
ruff check .
black --check .
```
