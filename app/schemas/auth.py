"""Pydantic auth schemas."""

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """Registration payload."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """OAuth token response."""

    access_token: str
    token_type: str = "bearer"
