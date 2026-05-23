"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.api.v1.routes import api_router


def create_app() -> FastAPI:
    """Build and configure FastAPI application."""
    app = FastAPI(title="Smart Visual Inspection System", version="0.1.0")
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
