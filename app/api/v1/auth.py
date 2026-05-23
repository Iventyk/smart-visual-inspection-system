"""Authentication endpoints."""

from fastapi import APIRouter, Form, HTTPException

from app.core.security import create_access_token, get_password_hash, verify_password
from app.schemas.auth import RegisterRequest, TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
_USERS: dict[str, str] = {}


@router.post("/register", status_code=201)
async def register(payload: RegisterRequest) -> dict:
    """Register user and store hashed password."""
    if payload.email in _USERS:
        raise HTTPException(status_code=409, detail="User already exists")
    _USERS[payload.email] = get_password_hash(payload.password)
    return {"email": payload.email}


@router.post("/token", response_model=TokenResponse)
async def token(username: str = Form(...), password: str = Form(...)) -> TokenResponse:
    """OAuth2 password token endpoint."""
    hashed = _USERS.get(username)
    if not hashed or not verify_password(password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(username))
