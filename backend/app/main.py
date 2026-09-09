import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from backend.app.core.config import get_settings
from backend.app.core.logging import setup_logging
from backend.app.database.database import engine, Base
from backend.app.middleware.cors import setup_cors
from backend.app.middleware.error_handler import setup_error_handler
from backend.app.middleware.logging import RequestLoggingMiddleware
from backend.app.middleware.rate_limiter import RateLimitMiddleware
from backend.app.middleware.auth import AuthMiddleware
from backend.app.api.v1.router import api_v1_router
from backend.app.websocket.manager import manager

import backend.app.models  # noqa: F401 — ensure all models are registered

settings = get_settings()
setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Insider Threat Detection API",
    description="FastAPI backend for temporal heterogeneous graph learning insider threat detection",
    version=settings.app_version,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)

setup_cors(app)
setup_error_handler(app)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=120)
app.add_middleware(AuthMiddleware)

app.include_router(api_v1_router, prefix="/api/v1")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.is_development,
        workers=1 if settings.is_development else settings.backend_workers,
    )
