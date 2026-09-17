import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from backend.app.auth.auth_handler import get_password_hash
from backend.app.database.database import SessionLocal, engine, Base
from backend.app.models.user import User
from backend.app.models.alert import Alert
from backend.app.models.prediction import Prediction


def seed_db_with_engine(target_engine) -> None:
    """Seed database using a specific SQLAlchemy engine."""
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(autocommit=False, autoflush=False, bind=target_engine)
    session = Session()
    try:
        seed_db(session)
    finally:
        session.close()


def seed_db(db: Session | None = None) -> None:
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        # 1. Seed Users if missing
        if db.query(User).count() == 0:
            users_to_seed = [
                User(
                    id=str(uuid.uuid4()),
                    username="analyst",
                    email="analyst@socnexus.internal",
                    hashed_password=get_password_hash("password123"),
                    full_name="Primary SOC Analyst",
                    role="analyst",
                    department="Cyber Defense Operations",
                    is_active=True,
                ),
                User(
                    id=str(uuid.uuid4()),
                    username="admin",
                    email="admin@socnexus.internal",
                    hashed_password=get_password_hash("admin123"),
                    full_name="Lead Security Architect",
                    role="admin",
                    department="Security Engineering",
                    is_active=True,
                ),
                User(
                    id=str(uuid.uuid4()),
                    username="auditor",
                    email="auditor@socnexus.internal",
                    hashed_password=get_password_hash("auditor123"),
                    full_name="Compliance Auditor",
                    role="auditor",
                    department="Governance & Compliance",
                    is_active=True,
                ),
            ]
            db.add_all(users_to_seed)
            db.commit()

        # 2. Seed Predictions if missing
        if db.query(Prediction).count() == 0:
            sample_predictions = [
                Prediction(
                    employee_id="MOH0273",
                    risk_score=94.2,
                    threat_level="CRITICAL",
                    confidence=0.96,
                    model_version="1.0.0",
                    explanation={
                        "feature_importance": {
                            "usb_insertion_count": 0.38,
                            "file_download_bytes_mb": 0.31,
                            "is_after_hours": 0.22,
                            "email_external_ratio": 0.09,
                        },
                        "top_features": [
                            {"name": "usb_insertion_count", "value": 4.0, "importance": 0.38, "direction": "above_normal"},
                            {"name": "file_download_bytes_mb", "value": 850.0, "importance": 0.31, "direction": "above_normal"},
                            {"name": "is_after_hours", "value": 1.0, "importance": 0.22, "direction": "above_normal"},
                        ],
                        "model_version": "1.0.0",
                        "method": "Temporal Graph Attention (THGNN)",
                    },
                    created_at=datetime.now(timezone.utc) - timedelta(minutes=45),
                ),
                Prediction(
                    employee_id="LAP0338",
                    risk_score=78.5,
                    threat_level="HIGH",
                    confidence=0.91,
                    model_version="1.0.0",
                    explanation={
                        "feature_importance": {
                            "email_external_ratio": 0.42,
                            "is_after_hours": 0.28,
                            "sensitive_resource_access": 0.18,
                        },
                        "top_features": [
                            {"name": "email_external_ratio", "value": 0.75, "importance": 0.42, "direction": "above_normal"},
                            {"name": "is_after_hours", "value": 1.0, "importance": 0.28, "direction": "above_normal"},
                        ],
                        "model_version": "1.0.0",
                        "method": "Temporal Graph Attention (THGNN)",
                    },
                    created_at=datetime.now(timezone.utc) - timedelta(hours=2),
                ),
                Prediction(
                    employee_id="CEL0561",
                    risk_score=62.0,
                    threat_level="HIGH",
                    confidence=0.88,
                    model_version="1.0.0",
                    explanation={
                        "feature_importance": {
                            "failed_login_ratio": 0.45,
                            "device_switching_count": 0.30,
                        },
                        "top_features": [
                            {"name": "failed_login_ratio", "value": 0.6, "importance": 0.45, "direction": "above_normal"},
                        ],
                        "model_version": "1.0.0",
                        "method": "Temporal Graph Attention (THGNN)",
                    },
                    created_at=datetime.now(timezone.utc) - timedelta(hours=5),
                ),
                Prediction(
                    employee_id="HPH0075",
                    risk_score=45.0,
                    threat_level="MEDIUM",
                    confidence=0.85,
                    model_version="1.0.0",
                    explanation={
                        "feature_importance": {
                            "usb_insertion_count": 0.35,
                            "file_download_bytes_mb": 0.25,
                        },
                        "top_features": [
                            {"name": "usb_insertion_count", "value": 1.0, "importance": 0.35, "direction": "above_normal"},
                        ],
                        "model_version": "1.0.0",
                        "method": "Temporal Graph Attention (THGNN)",
                    },
                    created_at=datetime.now(timezone.utc) - timedelta(hours=8),
                ),
                Prediction(
                    employee_id="ASD0577",
                    risk_score=15.0,
                    threat_level="LOW",
                    confidence=0.98,
                    model_version="1.0.0",
                    explanation={
                        "feature_importance": {
                            "is_after_hours": 0.05,
                            "login_frequency": 0.1,
                        },
                        "top_features": [],
                        "model_version": "1.0.0",
                        "method": "Temporal Graph Attention (THGNN)",
                    },
                    created_at=datetime.now(timezone.utc) - timedelta(hours=12),
                ),
            ]
            db.add_all(sample_predictions)
            db.commit()

        # 3. Seed Alerts if missing
        if db.query(Alert).count() == 0:
            pred_moh = db.query(Prediction).filter(Prediction.employee_id == "MOH0273").first()
            pred_lap = db.query(Prediction).filter(Prediction.employee_id == "LAP0338").first()
            pred_cel = db.query(Prediction).filter(Prediction.employee_id == "CEL0561").first()

            sample_alerts = [
                Alert(
                    employee_id="MOH0273",
                    prediction_id=pred_moh.id if pred_moh else None,
                    severity="critical",
                    status="open",
                    title="Critical Data Exfiltration via Removable Media",
                    description="Multiple USB connects detected followed by large DOC/PDF file reads outside normal working hours on PC-6699.",
                    notes="Flagged by THGNN graph temporal anomaly detector.",
                    created_at=datetime.now(timezone.utc) - timedelta(minutes=30),
                ),
                Alert(
                    employee_id="LAP0338",
                    prediction_id=pred_lap.id if pred_lap else None,
                    severity="high",
                    status="investigating",
                    title="Abnormal External Email Volume and Sensitive Attachments",
                    description="High ratio of outbound emails directed to non-corporate domains (earthlink.net, netzero.com).",
                    notes="Assigned for automated graph correlation.",
                    created_at=datetime.now(timezone.utc) - timedelta(hours=1, minutes=45),
                ),
                Alert(
                    employee_id="CEL0561",
                    prediction_id=pred_cel.id if pred_cel else None,
                    severity="medium",
                    status="open",
                    title="Repeated Authentication Anomalies and Host Switching",
                    description="Spike in failed authentication attempts across multiple workstations within short time window.",
                    notes="Under initial triage.",
                    created_at=datetime.now(timezone.utc) - timedelta(hours=4),
                ),
            ]
            db.add_all(sample_alerts)
            db.commit()

    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_db()
    print("Database seeding completed successfully.")
