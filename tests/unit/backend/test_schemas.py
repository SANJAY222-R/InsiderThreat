"""
Test: Pydantic Schemas
"""

import pytest
from backend.app.schemas.common import ResponseEnvelope, ErrorResponse, HealthResponse


class TestCommonSchemas:
    """Tests for shared Pydantic schemas."""

    def test_response_envelope_default(self) -> None:
        resp = ResponseEnvelope(data={"key": "value"})
        assert resp.success is True

    def test_error_response_structure(self) -> None:
        err = ErrorResponse(error_code="E001", message="something failed")
        assert err.success is False

    def test_health_response_default(self) -> None:
        health = HealthResponse()
        assert health.status == "healthy"

    # TODO (Phase 2): Add tests for all schema models.
