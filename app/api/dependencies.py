"""Shared FastAPI dependencies."""
import base64
from functools import lru_cache

from fastapi import Header, HTTPException, status

from app import security
from app.config import settings
from app.database import SessionLocal


@lru_cache(maxsize=1)
def _get_db():
    """Cached database session factory."""
    return SessionLocal()


def get_db():
    """Dependency injection for database session."""
    db = _get_db()
    try:
        yield db
    finally:
        db.close()


AUTH_SCHEMES = {"bearer", "basic"}


def require_auth(
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None),
) -> str:
    """Authenticate via Basic Auth, Bearer token, or X-API-Key header."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if x_api_key and security.verify_access_token(x_api_key):
        return settings.APP_USERNAME

    if authorization:
        scheme, sep, credential = authorization.partition(" ")
        if not sep:
            raise credentials_error
        scheme = scheme.lower()
        if scheme == "bearer" and security.verify_access_token(credential):
            return settings.APP_USERNAME
        if scheme == "basic":
            try:
                decoded = base64.b64decode(credential).decode("utf-8")
                username, _, password = decoded.partition(":")
                if security.verify_credentials(username, password):
                    return username
            except (ValueError, UnicodeDecodeError):
                pass

    raise credentials_error
