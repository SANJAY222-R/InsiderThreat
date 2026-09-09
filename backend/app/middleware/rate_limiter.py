import time
from collections import defaultdict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

__all__ = ["RateLimitMiddleware"]


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute
        self._window: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - 60

        hits = self._window[client_ip]
        self._window[client_ip] = [t for t in hits if t > window_start]
        hits = self._window[client_ip]

        if len(hits) >= self.rpm:
            return JSONResponse(
                status_code=429,
                content={"error_code": "RATE_LIMITED", "message": "Too many requests", "details": {}},
            )

        hits.append(now)
        return await call_next(request)
