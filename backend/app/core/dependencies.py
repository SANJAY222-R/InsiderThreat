"""
Dependency Injection Container
==============================

FastAPI dependency injection stubs for database sessions,
authentication, and service instances.

Phase 0: Interface stubs only.
"""

from typing import Any, AsyncGenerator

__all__ = ["get_db", "get_current_user", "get_settings"]


async def get_db() -> AsyncGenerator[Any, None]:
    """
    Yield a database session for request-scoped usage.

    Yields:
        SQLAlchemy AsyncSession.

    TODO (Phase 1): Implement with SQLAlchemy async session.
    """
    raise NotImplementedError("Phase 1: Database session dependency")
    yield  # noqa: unreachable — keeps generator signature


async def get_current_user() -> Any:
    """
    Extract and validate the current user from JWT token.

    Returns:
        User model instance.

    Raises:
        AuthenticationError: If token is missing or invalid.

    TODO (Phase 2): Implement JWT extraction from request headers.
    """
    raise NotImplementedError("Phase 2: Authentication dependency")
