"""
Report Pydantic Schemas
=======================

Request/response models for report generation endpoints.
Phase 0: Schema stubs.
"""

from datetime import datetime
from pydantic import BaseModel

__all__ = ["ReportRequest", "ReportResponse"]


class ReportRequest(BaseModel):
    """Schema for report generation request."""
    report_type: str  # daily_summary, threat_analysis, user_behavior
    date_from: datetime
    date_to: datetime
    format: str = "pdf"  # pdf, csv, json


class ReportResponse(BaseModel):
    """Schema for report API response."""
    report_id: int
    report_type: str
    status: str  # pending, generating, complete, failed
    download_url: str | None = None
    generated_at: datetime | None = None
