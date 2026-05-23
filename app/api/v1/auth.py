"""Authentication endpoints."""

from pydantic import BaseModel, EmailStr
from fastapi import APIRouter

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register")
async def register(data: RegisterRequest) -> dict[str, str]:
    """Mock registration endpoint."""
    return {"message": f"User {data.email} registered"}


@router.post("/token", response_model=TokenResponse)
async def token() -> TokenResponse:
    """Mock JWT token endpoint."""
    return TokenResponse(access_token="dev-token")
