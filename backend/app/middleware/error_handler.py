from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.core.exceptions import InsiderThreatBaseException, AuthenticationError, ValidationError
from backend.app.core.logging import get_logger

__all__ = ["setup_error_handler"]

logger = get_logger("error")

_STATUS_MAP: dict[str, int] = {
    "AUTH_ERROR": 401,
    "INVALID_CREDENTIALS": 401,
    "TOKEN_EXPIRED": 401,
    "VALIDATION_ERROR": 422,
    "DATABASE_CONNECTION_ERROR": 503,
    "DATABASE_ERROR": 500,
    "DATABASE_QUERY_ERROR": 500,
    "GRAPH_ERROR": 500,
    "GRAPH_BUILD_ERROR": 500,
    "GRAPH_QUERY_ERROR": 500,
    "AI_ERROR": 500,
    "MODEL_LOAD_ERROR": 500,
    "TRAINING_ERROR": 500,
    "INFERENCE_ERROR": 500,
    "SYSTEM_ERROR": 500,
    "INTERNAL_ERROR": 500,
}


def setup_error_handler(app: FastAPI) -> None:
    @app.exception_handler(InsiderThreatBaseException)
    async def custom_exception_handler(request: Request, exc: InsiderThreatBaseException):
        status_code = _STATUS_MAP.get(exc.error_code, 500)
        logger.error(f"{exc.error_code}: {exc.message}", extra={"details": exc.details, "path": str(request.url)})
        return JSONResponse(
            status_code=status_code,
            content=exc.to_dict(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception on {request.method} {request.url}")
        return JSONResponse(
            status_code=500,
            content={
                "error_code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {},
            },
        )
