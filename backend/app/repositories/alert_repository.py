from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.app.models.alert import Alert


class AlertRepository:
    def get(self, db: Session, alert_id: int):
        return db.query(Alert).filter(Alert.id == alert_id).first()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: str | None = None,
        severity: str | None = None,
    ):
        q = db.query(Alert)
        if status:
            q = q.filter(Alert.status == status)
        if severity:
            q = q.filter(Alert.severity == severity)
        return q.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()

    def count(self, db: Session, status: str | None = None):
        q = db.query(Alert)
        if status:
            q = q.filter(Alert.status == status)
        return q.count()

    def create(
        self,
        db: Session,
        employee_id: str,
        title: str,
        severity: str = "medium",
        prediction_id: int | None = None,
        description: str | None = None,
        notes: str | None = None,
    ):
        alert = Alert(
            employee_id=employee_id,
            title=title,
            severity=severity,
            prediction_id=prediction_id,
            description=description,
            notes=notes,
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    def update(self, db: Session, alert_id: int, **kwargs):
        alert = self.get(db, alert_id)
        if not alert:
            return None
        for k, v in kwargs.items():
            if v is not None and hasattr(alert, k):
                setattr(alert, k, v)
        if kwargs.get("status") == "resolved":
            alert.resolved_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(alert)
        return alert
