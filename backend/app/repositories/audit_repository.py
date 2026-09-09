from sqlalchemy.orm import Session

from backend.app.models.audit_log import AuditLog


class AuditRepository:
    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        user_id: str | None = None,
        action: str | None = None,
    ):
        q = db.query(AuditLog)
        if user_id:
            q = q.filter(AuditLog.user_id == user_id)
        if action:
            q = q.filter(AuditLog.action == action)
        return q.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()

    def log(
        self,
        db: Session,
        action: str,
        user_id: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        details: dict | None = None,
        ip_address: str | None = None,
    ):
        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
        )
        db.add(entry)
        db.commit()
        return entry
