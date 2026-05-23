"""Model metadata endpoint."""

from fastapi import APIRouter

router = APIRouter(prefix="/models")


@router.get("")
async def list_models() -> list[dict[str, str]]:
    """Return available inference model metadata."""
    return [
        {
            "name": "fasterrcnn_resnet50_fpn",
            "task": "object_detection",
            "framework": "torchvision",
        }
    ]
