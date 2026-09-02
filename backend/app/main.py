"""
Insider Threat Detection System — FastAPI Application Factory
=============================================================

This module creates and configures the FastAPI application instance.
All routers, middleware, and event handlers are registered here.

Phase 0: Scaffold only. No endpoints implemented.
"""

from fastapi import FastAPI

__all__ = ["create_app"]


def create_app() -> FastAPI:
    """
    Application factory for the Insider Threat Detection API.

    Returns:
        FastAPI: Configured application instance.

    TODO (Phase 1):
        - Register API v1 router
        - Configure CORS middleware
        - Configure authentication middleware
        - Register startup/shutdown events
        - Configure exception handlers
        - Set up database connections
    """
    app = FastAPI(
        title="Insider Threat Detection System",
        description="Temporal Heterogeneous Graph Learning for Explainable Insider Threat Detection",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # TODO: Register routers
    # app.include_router(api_v1_router, prefix="/api/v1")

    # TODO: Register middleware
    # app.add_middleware(...)

    # TODO: Register event handlers
    # @app.on_event("startup")
    # @app.on_event("shutdown")

    return app
