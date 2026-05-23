"""API v1 router."""

from fastapi import APIRouter

from app.api.v1 import analyze, auth, jobs, models

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(analyze.router, tags=["analyze"])
api_router.include_router(jobs.router, tags=["jobs"])
api_router.include_router(models.router, tags=["models"])
