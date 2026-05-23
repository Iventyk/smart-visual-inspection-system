"""FastAPI app entrypoint."""

from fastapi import FastAPI

from app.api.v1.analyze import router as analyze_router
from app.api.v1.auth import router as auth_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.models import router as models_router

app = FastAPI(title="Smart Visual Inspection System")
app.include_router(auth_router)
app.include_router(analyze_router)
app.include_router(jobs_router)
app.include_router(models_router)


@app.get("/health")
async def health() -> dict:
    """Service health endpoint."""
    return {"status": "ok", "models": "ready", "queue": "configured"}
