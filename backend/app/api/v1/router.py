"""
API v1 Aggregated Router
========================

Combines all v1 endpoint routers into a single router.

Phase 0: Router registration stubs.
"""

from fastapi import APIRouter

__all__ = ["api_v1_router"]

api_v1_router = APIRouter()

# TODO (Phase 2): Include endpoint routers
# api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# api_v1_router.include_router(users_router, prefix="/users", tags=["Users"])
# api_v1_router.include_router(predictions_router, prefix="/predictions", tags=["Predictions"])
# api_v1_router.include_router(graphs_router, prefix="/graphs", tags=["Graphs"])
# api_v1_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
# api_v1_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
# api_v1_router.include_router(explainability_router, prefix="/explain", tags=["Explainability"])
# api_v1_router.include_router(settings_router, prefix="/settings", tags=["Settings"])
