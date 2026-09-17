from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

__all__ = ["PredictionRequest", "PredictionResponse", "BatchPredictionRequest"]


class PredictionRequest(BaseModel):
    employee_id: str
    context: dict[str, Any] | None = None
    time_window_start: datetime | None = None
    time_window_end: datetime | None = None


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: str
    risk_score: float
    threat_level: str
    confidence: float | None = None
    explanation: dict[str, Any] = {}
    model_version: str
    created_at: datetime


class BatchPredictionRequest(BaseModel):
    employee_ids: list[str]
