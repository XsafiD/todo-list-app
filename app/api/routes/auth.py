"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status

from app import security, schemas
from app.api.dependencies import require_auth

router = APIRouter()


@router.post("/login", response_model=schemas.LoginResponse)
async def login(payload: schemas.LoginRequest):
    """Exchange username/password for a bearer token."""
    if not security.verify_credentials(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return schemas.LoginResponse(
        access_token=security.create_access_token(),
        token_type="bearer",
        expires_in=security.TOKEN_TTL_SECONDS,
        username=payload.username,
    )


@router.get("/me")
async def me(username: str = Depends(require_auth)):
    """Return the currently authenticated user."""
    return {"username": username}
