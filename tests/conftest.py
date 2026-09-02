"""
Shared Test Fixtures
====================

PyTest fixtures available to all test modules.

Phase 0: Basic fixture stubs.
"""

import pytest

__all__ = ["app_settings", "sample_user_data"]


@pytest.fixture
def app_settings():
    """Provide test application settings."""
    # TODO (Phase 1): Return Settings instance with test overrides
    return {
        "app_env": "testing",
        "database_url": "sqlite:///./data/test.db",
        "log_level": "WARNING",
    }


@pytest.fixture
def sample_user_data():
    """Provide sample user data for testing."""
    return {
        "username": "test_analyst",
        "email": "analyst@test.com",
        "password": "SecureP@ssw0rd!",
        "role": "analyst",
    }
