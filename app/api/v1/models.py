"""Model metadata endpoint."""

from fastapi import APIRouter

from app.cv.postprocessing import MODEL_CATEGORY_COUNT

router = APIRouter(prefix="/api/v1/models", tags=["models"])


@router.get("")
async def list_models() -> list[dict]:
    """List available models with metadata."""
    return [
        {
            "name": "fasterrcnn_resnet50_fpn",
            "type": "detection",
            "batch_size": 1,
            "category_count": MODEL_CATEGORY_COUNT,
        }
    ]
