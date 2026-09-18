"""
Report Pydantic Schemas
=======================

Request/response models for report generation and management endpoints.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "ReportRequest",
    "ReportResponse",
    "ReportDetailResponse",
    "ReportSummaryStats",
]


class ReportRequest(BaseModel):
    """Schema for report generation request."""
    report_type: str = "threat_analysis"  # threat_analysis, daily_summary, user_behavior, audit_trail
    date_from: datetime
    date_to: datetime
    format: str = "pdf"  # pdf, csv, json
    title: Optional[str] = None


class ReportResponse(BaseModel):
    """Schema for report metadata response."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    report_id: Optional[int] = None
    title: str
    report_type: str
    format: str = "pdf"
    status: str = "complete"
    date_from: datetime
    date_to: datetime
    summary_metrics: Optional[Dict[str, Any]] = Field(default_factory=dict)
    download_url: Optional[str] = None
    file_size: Optional[int] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None

    def model_post_init(self, __context: Any) -> None:
        if self.report_id is None:
            self.report_id = self.id


class ReportDetailResponse(ReportResponse):
    """Schema for full report response including detailed data payload."""
    data: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ReportSummaryStats(BaseModel):
    """Schema for overall reports tab statistics."""
    total_reports: int
    reports_by_type: Dict[str, int]
    reports_by_format: Dict[str, int]
    last_generated_at: Optional[datetime] = None
