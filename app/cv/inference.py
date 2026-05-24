"""PyTorch model loading and inference."""

import torch
import torchvision

_model = None


def get_model() -> torch.nn.Module:
    """Load model singleton once for worker lifespan."""
    global _model
    if _model is None:
        _model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
            weights="DEFAULT"
        )
        _model.eval()
    return _model


def run_inference(image_tensor: torch.Tensor) -> dict:
    """Run detection inference in no_grad mode."""
    model = get_model()
    with torch.no_grad():
        output = model([image_tensor])[0]
    return output
