from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException

from backend.app.auth.dependencies import get_current_admin
from backend.app.core.config import get_settings
from backend.app.models.user import User

router = APIRouter()


@router.get("/")
def get_settings_view() -> Dict[str, Any]:
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "app_env": settings.app_env,
        "app_version": settings.app_version,
        "log_level": settings.log_level,
        "cors_origins": settings.cors_origins,
    }


@router.put("/")
def update_settings(_: User = Depends(get_current_admin)) -> Any:
    raise HTTPException(status_code=501, detail="Settings modification requires application restart")
