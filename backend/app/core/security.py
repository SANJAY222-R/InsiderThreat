"""
Security Utilities
==================

JWT token creation/validation and password hashing.

Phase 0: Interface definitions only. No implementation.
"""

from datetime import datetime
from typing import Any

__all__ = [
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "hash_password",
    "verify_password",
]


def create_access_token(subject: str, expires_delta: int | None = None) -> str:
    """
    Create a JWT access token.

    Args:
        subject: Token subject (usually user ID).
        expires_delta: Custom expiry in minutes.

    Returns:
        Encoded JWT string.

    TODO (Phase 2): Implement with python-jose.
    """
    raise NotImplementedError("Phase 2: JWT implementation")


def create_refresh_token(subject: str) -> str:
    """
    Create a JWT refresh token with extended expiry.

    Args:
        subject: Token subject (usually user ID).

    Returns:
        Encoded JWT refresh token string.

    TODO (Phase 2): Implement with python-jose.
    """
    raise NotImplementedError("Phase 2: JWT implementation")


def verify_token(token: str) -> dict[str, Any]:
    """
    Verify and decode a JWT token.

    Args:
        token: Encoded JWT string.

    Returns:
        Decoded token payload.

    Raises:
        AuthenticationError: If token is invalid or expired.

    TODO (Phase 2): Implement with python-jose.
    """
    raise NotImplementedError("Phase 2: JWT implementation")


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Args:
        password: Plaintext password.

    Returns:
        Bcrypt hash string.

    TODO (Phase 2): Implement with passlib.
    """
    raise NotImplementedError("Phase 2: Password hashing")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plaintext password to verify.
        hashed_password: Stored bcrypt hash.

    Returns:
        True if password matches.

    TODO (Phase 2): Implement with passlib.
    """
    raise NotImplementedError("Phase 2: Password verification")
