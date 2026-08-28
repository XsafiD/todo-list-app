"""Authentication & token helpers for single-user setup."""
import base64
import hashlib
import hmac
import time
from functools import lru_cache

import bcrypt

from app.config import settings

TOKEN_TTL_SECONDS = 60 * 60 * 24 * 30  # 30 days


def hash_password(plain: str) -> str:
    """Hash a plain text password using bcrypt."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


@lru_cache(maxsize=1)
def _stored_password_hash() -> bytes:
    """Return cached password hash (support APP_PASSWORD_HASH env var)."""
    if settings.APP_PASSWORD_HASH:
        return settings.APP_PASSWORD_HASH.encode("utf-8")
    return hash_password(settings.APP_PASSWORD).encode("utf-8")


def verify_credentials(username: str, password: str) -> bool:
    """Verify username/password against stored credentials."""
    if username != settings.APP_USERNAME:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), _stored_password_hash())
    except ValueError:
        return False


def _b64_encode(data: bytes) -> str:
    """URL-safe base64 encode without padding."""
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64_decode(data: str) -> bytes:
    """URL-safe base64 decode with padding restoration."""
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def create_access_token() -> str:
    """Create a signed JWT-like access token (HMAC-SHA256)."""
    expires_at = int(time.time()) + TOKEN_TTL_SECONDS
    payload = f"{settings.APP_USERNAME}:{expires_at}"
    signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return f"{_b64_encode(payload.encode('utf-8'))}.{_b64_encode(signature)}"


def verify_access_token(token: str) -> bool:
    """Verify an access token's signature and expiry."""
    try:
        payload_b64, signature_b64 = token.split(".", 1)
        payload = _b64_decode(payload_b64).decode("utf-8")
        expected = hmac.new(
            settings.SECRET_KEY.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256
        ).digest()
        provided = _b64_decode(signature_b64)
        if not hmac.compare_digest(expected, provided):
            return False
        username, expires_at = payload.split(":", 1)
        return username == settings.APP_USERNAME and int(expires_at) > time.time()
    except (ValueError, UnicodeDecodeError):
        return False
