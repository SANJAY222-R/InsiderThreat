from sqlalchemy.orm import Session

from backend.app.models.prediction import Prediction


class PredictionRepository:
    def get(self, db: Session, prediction_id: int):
        return db.query(Prediction).filter(Prediction.id == prediction_id).first()

    def get_by_employee(self, db: Session, employee_id: str, skip: int = 0, limit: int = 100):
        return (
            db.query(Prediction)
            .filter(Prediction.employee_id == employee_id)
            .order_by(Prediction.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(Prediction)
            .order_by(Prediction.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self, db: Session):
        return db.query(Prediction).count()

    def create(
        self,
        db: Session,
        employee_id: str,
        risk_score: float,
        threat_level: str,
        confidence: float | None = None,
        model_version: str = "1.0.0",
        explanation: dict | None = None,
    ):
        pred = Prediction(
            employee_id=employee_id,
            risk_score=risk_score,
            threat_level=threat_level,
            confidence=confidence,
            model_version=model_version,
            explanation=explanation or {},
        )
        db.add(pred)
        db.commit()
        db.refresh(pred)
        return pred
