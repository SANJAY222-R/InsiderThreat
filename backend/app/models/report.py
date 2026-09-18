from sqlalchemy import Column, DateTime, Index, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from backend.app.database.database import Base

__all__ = ["Report"]


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    report_type = Column(String(50), nullable=False, index=True)
    format = Column(String(20), nullable=False, default="pdf")
    status = Column(String(30), nullable=False, default="complete", index=True)
    date_from = Column(DateTime(timezone=True), nullable=False)
    date_to = Column(DateTime(timezone=True), nullable=False)
    summary_metrics = Column(JSONB().with_variant(JSON, "sqlite"), default=dict)
    data = Column(JSONB().with_variant(JSON, "sqlite"), default=dict)
    created_by = Column(String(100), nullable=True)
    download_url = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    __table_args__ = (
        Index("ix_reports_type_created", "report_type", "created_at"),
    )
