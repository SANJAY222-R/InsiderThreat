"""
PredictionService
=================

Business logic for threat prediction orchestration.
Wraps the Predictor engine with persistence and audit logging.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ai.inference.predictor import Predictor
from backend.app.models.prediction import Prediction

__all__ = ["PredictionService"]


class PredictionService:
    """
    Service layer for threat prediction orchestration.
    """

    def __init__(self, model_version: str = "1.0.0") -> None:
        self._predictor = Predictor(model_version=model_version)

    def run_prediction(
        self,
        employee_id: str,
        db: Session,
        context: Optional[Dict[str, Any]] = None,
        events: Optional[List[Dict[str, Any]]] = None,
    ) -> Prediction:
        result = self._predictor.predict(
            employee_id=employee_id,
            events=events or [],
            context=context,
        )
        record = Prediction(
            employee_id=result["employee_id"],
            risk_score=result["risk_score"],
            threat_level=result["threat_level"],
            confidence=result["confidence"],
            model_version=result["model_version"],
            explanation=result.get("explanation", {}),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def batch_predict(
        self,
        employee_ids: List[str],
        db: Session,
    ) -> List[Prediction]:
        return [self.run_prediction(eid, db) for eid in employee_ids]

    def get_by_id(self, prediction_id: int, db: Session) -> Optional[Prediction]:
        return db.query(Prediction).filter(Prediction.id == prediction_id).first()

    def list_predictions(
        self,
        db: Session,
        employee_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Prediction]:
        query = db.query(Prediction)
        if employee_id:
            query = query.filter(Prediction.employee_id == employee_id)
        return query.order_by(Prediction.created_at.desc()).offset(skip).limit(limit).all()

    def get_risk_summary(self, db: Session) -> Dict[str, Any]:
        all_predictions = db.query(Prediction).all()
        if not all_predictions:
            return {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "avg_risk": 0.0}

        counts: Dict[str, int] = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        total_risk = 0.0
        for p in all_predictions:
            counts[p.threat_level] = counts.get(p.threat_level, 0) + 1
            total_risk += p.risk_score

        return {
            "total": len(all_predictions),
            "critical": counts["CRITICAL"],
            "high": counts["HIGH"],
            "medium": counts["MEDIUM"],
            "low": counts["LOW"],
            "avg_risk": round(total_risk / len(all_predictions), 2),
            "evaluated_at": datetime.now().isoformat(),
        }
