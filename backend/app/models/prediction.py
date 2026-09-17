from sqlalchemy import Column, DateTime, Float, Index, Integer, JSON, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from backend.app.database.database import Base

__all__ = ["Prediction"]


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(100), index=True, nullable=False)
    risk_score = Column(Float, nullable=False, index=True)
    threat_level = Column(String(20), nullable=False, index=True)
    confidence = Column(Float, nullable=True)
    model_version = Column(String(50), default="1.0.0")
    explanation = Column(JSONB().with_variant(JSON, "sqlite"), default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    __table_args__ = (
        Index("ix_predictions_explanation_gin", "explanation", postgresql_using="gin"),
        Index("ix_predictions_employee_created", "employee_id", "created_at"),
    )
