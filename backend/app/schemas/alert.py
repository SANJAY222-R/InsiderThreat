from datetime import datetime

from pydantic import BaseModel, ConfigDict

__all__ = ["AlertCreate", "AlertUpdate", "AlertResponse"]


class AlertCreate(BaseModel):
    employee_id: str
    prediction_id: int | None = None
    severity: str = "medium"
    title: str
    description: str | None = None
    notes: str | None = None


class AlertUpdate(BaseModel):
    status: str | None = None
    assigned_to: str | None = None
    notes: str | None = None
    severity: str | None = None


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prediction_id: int | None = None
    employee_id: str
    severity: str
    status: str
    assigned_to: str | None = None
    title: str
    description: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    resolved_at: datetime | None = None
