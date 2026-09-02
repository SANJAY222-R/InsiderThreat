"""
Test: Application Configuration
"""

import pytest


class TestSettings:
    """Tests for Settings configuration loading."""

    def test_default_settings_load(self, app_settings):
        """Settings should load with default values."""
        assert app_settings["app_env"] == "testing"

    def test_database_url_configured(self, app_settings):
        """Database URL should be set for test environment."""
        assert "test.db" in app_settings["database_url"]

    # TODO (Phase 1): Add tests for env var overrides, validation, etc.
