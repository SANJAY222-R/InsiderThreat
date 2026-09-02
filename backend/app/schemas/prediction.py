"""
Prediction Pydantic Schemas
===========================

Request/response models for prediction endpoints.
Phase 0: Schema stubs.
"""

from datetime import datetime
from typing import Any
from pydantic import BaseModel

__all__ = ["PredictionRequest", "PredictionResponse", "BatchPredictionRequest"]


class PredictionRequest(BaseModel):
    """Schema for requesting a threat prediction."""
    employee_id: str
    time_window_start: datetime | None = None
    time_window_end: datetime | None = None


class PredictionResponse(BaseModel):
    """Schema for prediction results."""
    prediction_id: int
    employee_id: str
    risk_score: float
    threat_level: str
    explanation: dict[str, Any] = {}
    model_version: str
    timestamp: datetime


class BatchPredictionRequest(BaseModel):
    """Schema for batch prediction requests."""
    employee_ids: list[str]
    time_window_start: datetime | None = None
    time_window_end: datetime | None = None
