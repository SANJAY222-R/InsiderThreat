import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from backend.app.core.logging import get_logger

__all__ = ["RequestLoggingMiddleware"]

logger = get_logger("api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info(
            f"{request.method} {request.url.path} → {response.status_code} ({elapsed_ms:.1f}ms)",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(elapsed_ms, 1),
            client=request.client.host if request.client else None,
        )
        return response
