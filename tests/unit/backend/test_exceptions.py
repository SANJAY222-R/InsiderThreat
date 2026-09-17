"""
Test: Custom Exception Hierarchy
"""

import pytest
from backend.app.core.exceptions import (
    InsiderThreatBaseException,
    ValidationError,
    DatabaseError,
    GraphError,
    AIError,
    AuthenticationError,
)


class TestExceptionHierarchy:
    """Tests for the custom exception hierarchy."""

    def test_base_exception_has_error_code(self) -> None:
        exc = InsiderThreatBaseException(message="test", error_code="TEST")
        assert exc.error_code == "TEST"
        assert exc.message == "test"

    def test_base_exception_to_dict(self) -> None:
        exc = InsiderThreatBaseException(message="fail", error_code="E001")
        result = exc.to_dict()
        assert result["error_code"] == "E001"
        assert result["message"] == "fail"

    def test_validation_error_inherits_base(self) -> None:
        exc = ValidationError("invalid input")
        assert isinstance(exc, InsiderThreatBaseException)
        assert exc.error_code == "VALIDATION_ERROR"

    def test_database_error_inherits_base(self) -> None:
        assert issubclass(DatabaseError, InsiderThreatBaseException)

    def test_graph_error_inherits_base(self) -> None:
        assert issubclass(GraphError, InsiderThreatBaseException)

    def test_ai_error_inherits_base(self) -> None:
        assert issubclass(AIError, InsiderThreatBaseException)

    def test_auth_error_inherits_base(self) -> None:
        assert issubclass(AuthenticationError, InsiderThreatBaseException)
