"""
Shared Test Fixtures
====================

PyTest fixtures providing TestClient, in-memory DB, auth headers, and sample data.
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database.database import Base, get_db
from backend.app.models import User, Prediction, Alert, AuditLog
from backend.app.database.seed import seed_db_with_engine

TEST_DB_PATH = "/tmp/test.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

# Remove existing test db in /tmp if present
if os.path.exists(TEST_DB_PATH):
    try:
        os.remove(TEST_DB_PATH)
    except Exception:
        pass

_test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)

__all__ = [
    "client",
    "db_session",
    "auth_headers",
    "analyst_auth_headers",
    "app_settings",
    "sample_user_data",
    "sample_prediction_payload",
]


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=_test_engine)
    seed_db_with_engine(_test_engine)
    yield
    Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture(scope="session")
def client(setup_test_database):
    from backend.app.main import app
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def db_session(setup_test_database):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def auth_headers(client):
    """Admin auth token obtained via login endpoint."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    if response.status_code == 200:
        token = response.json().get("access_token", "")
        return {"Authorization": f"Bearer {token}"}
    return {}


@pytest.fixture(scope="session")
def analyst_auth_headers(client):
    """Analyst auth token obtained via login endpoint."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "analyst", "password": "password123"},
    )
    if response.status_code == 200:
        token = response.json().get("access_token", "")
        return {"Authorization": f"Bearer {token}"}
    return {}


@pytest.fixture
def app_settings():
    return {
        "app_env": "testing",
        "database_url": TEST_DB_URL,
        "log_level": "WARNING",
    }


@pytest.fixture
def sample_user_data():
    return {
        "username": "test_analyst",
        "email": "analyst@test.com",
        "password": "SecureP@ssw0rd!",
        "role": "analyst",
    }


@pytest.fixture
def sample_prediction_payload():
    return {
        "employee_id": "MOH0273",
        "context": {
            "is_after_hours": 1.0,
            "failed_login_ratio": 0.5,
            "usb_insertion_count": 3.0,
            "file_download_bytes_mb": 500.0,
            "sensitive_resource_access": 4.0,
            "email_external_ratio": 0.7,
            "device_switching_count": 2.0,
        },
    }
