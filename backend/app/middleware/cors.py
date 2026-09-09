from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.app.core.config import get_settings

__all__ = ["setup_cors"]


def setup_cors(app: FastAPI) -> None:
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
