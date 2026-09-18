import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from sqlalchemy.orm import Session, sessionmaker

# Ensure project root is in python path when run directly
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.app.auth.auth_handler import get_password_hash
from backend.app.database.database import Base, SessionLocal, engine
from backend.app.models.alert import Alert
from backend.app.models.prediction import Prediction
from backend.app.models.report import Report
from backend.app.models.user import User
from backend.app.services.report_builder import build_report_data, export_report_file

__all__ = ["seed_db", "seed_db_with_engine"]


def seed_db_with_engine(target_engine: Any) -> None:
    """Seed database using a specific SQLAlchemy engine."""
    Session = sessionmaker(autocommit=False, autoflush=False, bind=target_engine)
    session = Session()
    try:
        seed_db(session)
    finally:
        session.close()


def seed_db(db: Session | None = None) -> None:
    """Idempotently seed essential default users, baseline predictions, and alerts."""
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        # 1. Seed Users
        default_users = [
            {
                "username": "analyst",
                "email": "analyst@socnexus.internal",
                "password": "password123",
                "full_name": "Primary SOC Analyst",
                "role": "analyst",
                "department": "Cyber Defense Operations",
            },
            {
                "username": "admin",
                "email": "admin@socnexus.internal",
                "password": "admin123",
                "full_name": "Lead Security Architect",
                "role": "admin",
                "department": "Security Engineering",
            },
            {
                "username": "auditor",
                "email": "auditor@socnexus.internal",
                "password": "auditor123",
                "full_name": "Compliance Auditor",
                "role": "auditor",
                "department": "Governance & Compliance",
            },
        ]

        admin_user_id = None
        for u in default_users:
            existing = db.query(User).filter(User.username == u["username"]).first()
            if not existing:
                new_user = User(
                    id=str(uuid.uuid4()),
                    username=u["username"],
                    email=u["email"],
                    hashed_password=get_password_hash(u["password"]),
                    full_name=u["full_name"],
                    role=u["role"],
                    department=u["department"],
                    is_active=True,
                )
                db.add(new_user)
                db.flush()
                if u["username"] == "admin":
                    admin_user_id = new_user.id
            elif u["username"] == "admin":
                admin_user_id = existing.id

        db.commit()

        # 2. Seed Baseline Predictions
        sample_predictions = [
            {
                "employee_id": "MOH0273",
                "risk_score": 94.2,
                "threat_level": "CRITICAL",
                "confidence": 0.96,
                "model_version": "1.0.0",
                "explanation": {
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
                "offset_minutes": 45,
            },
            {
                "employee_id": "LAP0338",
                "risk_score": 78.5,
                "threat_level": "HIGH",
                "confidence": 0.91,
                "model_version": "1.0.0",
                "explanation": {
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
                "offset_minutes": 120,
            },
            {
                "employee_id": "CEL0561",
                "risk_score": 62.0,
                "threat_level": "HIGH",
                "confidence": 0.88,
                "model_version": "1.0.0",
                "explanation": {
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
                "offset_minutes": 300,
            },
            {
                "employee_id": "HPH0075",
                "risk_score": 45.0,
                "threat_level": "MEDIUM",
                "confidence": 0.85,
                "model_version": "1.0.0",
                "explanation": {
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
                "offset_minutes": 480,
            },
            {
                "employee_id": "ASD0577",
                "risk_score": 15.0,
                "threat_level": "LOW",
                "confidence": 0.98,
                "model_version": "1.0.0",
                "explanation": {
                    "feature_importance": {
                        "is_after_hours": 0.05,
                        "login_frequency": 0.1,
                    },
                    "top_features": [],
                    "model_version": "1.0.0",
                    "method": "Temporal Graph Attention (THGNN)",
                },
                "offset_minutes": 720,
            },
        ]

        for p in sample_predictions:
            existing_pred = db.query(Prediction).filter(Prediction.employee_id == p["employee_id"]).first()
            if not existing_pred:
                pred = Prediction(
                    employee_id=p["employee_id"],
                    risk_score=p["risk_score"],
                    threat_level=p["threat_level"],
                    confidence=p["confidence"],
                    model_version=p["model_version"],
                    explanation=p["explanation"],
                    created_at=datetime.now(timezone.utc) - timedelta(minutes=p["offset_minutes"]),
                )
                db.add(pred)

        db.commit()

        # 3. Seed Alerts
        pred_moh = db.query(Prediction).filter(Prediction.employee_id == "MOH0273").first()
        pred_lap = db.query(Prediction).filter(Prediction.employee_id == "LAP0338").first()
        pred_cel = db.query(Prediction).filter(Prediction.employee_id == "CEL0561").first()

        sample_alerts = [
            {
                "employee_id": "MOH0273",
                "prediction_id": pred_moh.id if pred_moh else None,
                "severity": "critical",
                "status": "open",
                "title": "Critical Data Exfiltration via Removable Media",
                "description": "Multiple USB connects detected followed by large DOC/PDF file reads outside normal working hours on PC-6699.",
                "notes": "Flagged by THGNN graph temporal anomaly detector.",
                "assigned_to": admin_user_id,
                "offset_minutes": 30,
            },
            {
                "employee_id": "LAP0338",
                "prediction_id": pred_lap.id if pred_lap else None,
                "severity": "high",
                "status": "investigating",
                "title": "Abnormal External Email Volume and Sensitive Attachments",
                "description": "High ratio of outbound emails directed to non-corporate domains (earthlink.net, netzero.com).",
                "notes": "Assigned for automated graph correlation.",
                "assigned_to": admin_user_id,
                "offset_minutes": 105,
            },
            {
                "employee_id": "CEL0561",
                "prediction_id": pred_cel.id if pred_cel else None,
                "severity": "medium",
                "status": "open",
                "title": "Repeated Authentication Anomalies and Host Switching",
                "description": "Spike in failed authentication attempts across multiple workstations within short time window.",
                "notes": "Under initial triage.",
                "assigned_to": None,
                "offset_minutes": 240,
            },
        ]

        for a in sample_alerts:
            existing_alert = (
                db.query(Alert)
                .filter(Alert.employee_id == a["employee_id"], Alert.title == a["title"])
                .first()
            )
            if not existing_alert:
                alert = Alert(
                    employee_id=a["employee_id"],
                    prediction_id=a["prediction_id"],
                    severity=a["severity"],
                    status=a["status"],
                    title=a["title"],
                    description=a["description"],
                    notes=a["notes"],
                    assigned_to=a["assigned_to"],
                    created_at=datetime.now(timezone.utc) - timedelta(minutes=a["offset_minutes"]),
                )
                db.add(alert)

        db.commit()

        # 4. Seed Baseline Reports
        if db.query(Report).count() == 0:
            now = datetime.now(timezone.utc)
            sample_report_configs = [
                {
                    "title": "Comprehensive Threat Analysis & Forensic Summary",
                    "report_type": "threat_analysis",
                    "format": "pdf",
                    "date_from": now - timedelta(days=7),
                    "date_to": now,
                    "created_by": "SOC Analyst",
                },
                {
                    "title": "Executive Daily Threat Intelligence Digest",
                    "report_type": "daily_summary",
                    "format": "csv",
                    "date_from": now - timedelta(days=1),
                    "date_to": now,
                    "created_by": "SOC Analyst",
                },
                {
                    "title": "Entity Behavioral Deviation & Risk Profile",
                    "report_type": "user_behavior",
                    "format": "json",
                    "date_from": now - timedelta(days=30),
                    "date_to": now,
                    "created_by": "Compliance Auditor",
                },
            ]

            for rc in sample_report_configs:
                rep_title, summary_metrics, detailed_data = build_report_data(
                    db=db,
                    report_type=rc["report_type"],
                    date_from=rc["date_from"],
                    date_to=rc["date_to"],
                    title=rc["title"],
                    created_by=rc["created_by"],
                )
                report = Report(
                    title=rep_title,
                    report_type=rc["report_type"],
                    format=rc["format"],
                    status="complete",
                    date_from=rc["date_from"],
                    date_to=rc["date_to"],
                    summary_metrics=summary_metrics,
                    data=detailed_data,
                    created_by=rc["created_by"],
                )
                db.add(report)
                db.flush()
                report.download_url = f"/api/v1/reports/{report.id}/download"
                try:
                    content_bytes, _, _ = export_report_file(report)
                    report.file_size = len(content_bytes)
                except Exception:
                    report.file_size = 1024

            db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_db()
    print("Database seeding completed successfully.")
