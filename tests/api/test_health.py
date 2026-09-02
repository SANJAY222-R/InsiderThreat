"""
Test: Health Check Endpoint
"""

import pytest


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    @pytest.mark.api
    def test_health_returns_200(self):
        """Health check should return 200 OK."""
        # TODO (Phase 2): Implement with httpx TestClient
        pass
