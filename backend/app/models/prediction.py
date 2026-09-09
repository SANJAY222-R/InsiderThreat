from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func

from backend.app.database.database import Base

__all__ = ["Prediction"]


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(100), index=True, nullable=False)
    risk_score = Column(Float, nullable=False)
    threat_level = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=True)
    model_version = Column(String(50), default="1.0.0")
    explanation = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
