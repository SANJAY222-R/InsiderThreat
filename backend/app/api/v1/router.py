from fastapi import APIRouter

from backend.app.api.v1.endpoints import (
    alerts,
    auth,
    explainability,
    graphs,
    predictions,
    reports,
    settings,
    users,
)

__all__ = ["api_v1_router"]

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(users.router, prefix="/users", tags=["Users"])
api_v1_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
api_v1_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
api_v1_router.include_router(graphs.router, prefix="/graphs", tags=["Graphs"])
api_v1_router.include_router(explainability.router, prefix="/explain", tags=["Explainability"])
api_v1_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_v1_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
