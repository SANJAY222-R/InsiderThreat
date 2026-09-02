"""
Alert Pydantic Schemas
======================

Request/response models for alert endpoints.
Phase 0: Schema stubs.
"""

from datetime import datetime
from pydantic import BaseModel

__all__ = ["AlertCreate", "AlertUpdate", "AlertResponse"]


class AlertCreate(BaseModel):
    """Schema for creating an alert."""
    prediction_id: int
    severity: str = "warning"
    notes: str = ""


class AlertUpdate(BaseModel):
    """Schema for updating alert status."""
    status: str | None = None
    assigned_to: int | None = None
    notes: str | None = None


class AlertResponse(BaseModel):
    """Schema for alert API responses."""
    id: int
    prediction_id: int
    severity: str
    status: str
    assigned_to: int | None
    notes: str
    created_at: datetime
    resolved_at: datetime | None
