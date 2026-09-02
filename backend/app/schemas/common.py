"""
Common Pydantic Schemas
=======================

Shared response envelopes and pagination models.
"""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel

__all__ = ["ResponseEnvelope", "PaginatedResponse", "ErrorResponse", "HealthResponse"]

T = TypeVar("T")


class ResponseEnvelope(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool = True
    data: T | None = None
    message: str = ""


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response."""
    items: list[T] = []
    total: int = 0
    page: int = 1
    page_size: int = 20
    total_pages: int = 0


class ErrorResponse(BaseModel):
    """Error response body."""
    success: bool = False
    error_code: str
    message: str
    details: dict[str, Any] = {}


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "0.1.0"
    environment: str = "development"
