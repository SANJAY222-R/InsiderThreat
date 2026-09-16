from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from backend.app.core.config import get_settings
from backend.app.core.security import verify_password, hash_password as get_password_hash


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
