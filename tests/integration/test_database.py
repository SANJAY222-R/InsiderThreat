"""
Test: Database Integration
==========================

Integration tests for database connectivity, pooling, Alembic migrations,
and model persistence with JSON/JSONB support.
"""

import os
import tempfile
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.database.database import (
    Base,
    check_database_liveness,
    create_db_engine,
    get_normalized_database_url,
)
from backend.app.models.alert import Alert
from backend.app.models.audit_log import AuditLog
from backend.app.models.prediction import Prediction
from backend.app.models.user import User


class TestDatabaseIntegration:
    """Integration tests for database connectivity and ORM models."""

    @pytest.mark.integration
    def test_database_connection(self, db_session: Session) -> None:
        """Should connect to the database and verify liveness."""
        result = db_session.execute(text("SELECT 1")).scalar()
        assert result == 1
        assert check_database_liveness() is True

    @pytest.mark.integration
    def test_migrations_apply(self) -> None:
        """Alembic migrations should apply cleanly and rollback cleanly."""
        temp_db_file = os.path.join(tempfile.gettempdir(), "test_migration_suite.db")
        temp_db_url = f"sqlite:///{Path(temp_db_file).as_posix()}"

        alembic_ini_path = Path(__file__).resolve().parent.parent.parent / "alembic.ini"
        alembic_cfg = Config(str(alembic_ini_path))
        alembic_cfg.set_main_option("sqlalchemy.url", temp_db_url)

        try:
            # Upgrade to head
            command.upgrade(alembic_cfg, "head")

            # Verify tables created
            temp_engine = create_db_engine(temp_db_url)
            with temp_engine.connect() as conn:
                tables_result = conn.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table'")
                ).fetchall()
                table_names = {row[0] for row in tables_result}
                assert "users" in table_names
                assert "predictions" in table_names
                assert "alerts" in table_names
                assert "audit_logs" in table_names
                assert "alembic_version" in table_names
            temp_engine.dispose()

            # Downgrade back to base
            command.downgrade(alembic_cfg, "base")

            # Re-upgrade to head to verify re-runnability
            command.upgrade(alembic_cfg, "head")
        finally:
            if os.path.exists(temp_db_file):
                try:
                    os.remove(temp_db_file)
                except Exception:
                    pass

    @pytest.mark.integration
    def test_normalized_database_url(self) -> None:
        """Should normalize legacy postgres URLs to use psycopg driver."""
        assert (
            get_normalized_database_url("postgres://user:pass@host:5432/db")
            == "postgresql+psycopg://user:pass@host:5432/db"
        )
        assert (
            get_normalized_database_url("postgresql://user:pass@host:5432/db")
            == "postgresql+psycopg://user:pass@host:5432/db"
        )
        assert (
            get_normalized_database_url("postgresql+psycopg://user:pass@host:5432/db")
            == "postgresql+psycopg://user:pass@host:5432/db"
        )
        assert (
            get_normalized_database_url("sqlite:///./data.db")
            == "sqlite:///./data.db"
        )

    @pytest.mark.integration
    def test_prediction_and_audit_json_persistence(self, db_session: Session) -> None:
        """Should correctly persist and query JSON/JSONB explanation and details fields."""
        # 1. Prediction with rich explanation payload
        explanation_data = {
            "feature_importance": {"usb_insertion": 0.45, "external_email": 0.35},
            "top_features": [
                {"name": "usb_insertion", "value": 3.0, "direction": "above_normal"}
            ],
            "method": "Temporal Graph Attention (THGNN)",
        }
        pred = Prediction(
            employee_id="EMP_TEST_999",
            risk_score=88.5,
            threat_level="HIGH",
            confidence=0.92,
            model_version="1.0.0",
            explanation=explanation_data,
        )
        db_session.add(pred)
        db_session.commit()
        db_session.refresh(pred)

        assert pred.id is not None
        assert pred.explanation["method"] == "Temporal Graph Attention (THGNN)"
        assert pred.explanation["feature_importance"]["usb_insertion"] == 0.45

        # 2. Audit log with metadata payload
        audit = AuditLog(
            user_id="test_admin",
            action="UPDATE_ALERT_STATUS",
            resource_type="Alert",
            resource_id="1",
            details={"previous_status": "open", "new_status": "investigating"},
            ip_address="192.168.1.50",
        )
        db_session.add(audit)
        db_session.commit()
        db_session.refresh(audit)

        assert audit.id is not None
        assert audit.details["new_status"] == "investigating"

        # Cleanup
        db_session.delete(pred)
        db_session.delete(audit)
        db_session.commit()

    @pytest.mark.integration
    def test_user_alert_relationships(self, db_session: Session) -> None:
        """Should maintain relationships between users, predictions, and alerts."""
        user = db_session.query(User).filter(User.username == "admin").first()
        assert user is not None

        alerts = db_session.query(Alert).filter(Alert.assigned_to == user.id).all()
        assert isinstance(alerts, list)
        for a in alerts:
            assert a.assignee is not None
            assert a.assignee.username == "admin"
