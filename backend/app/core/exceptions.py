"""
Custom Exception Hierarchy
==========================

Centralized exception classes for the Insider Threat Detection System.
All custom exceptions inherit from InsiderThreatBaseException to enable
unified error handling across the application.

Exception Tree:
    InsiderThreatBaseException
    ├── ValidationError
    ├── DatabaseError
    │   ├── ConnectionError
    │   └── QueryError
    ├── GraphError
    │   ├── GraphBuildError
    │   └── GraphQueryError
    ├── AIError
    │   ├── ModelLoadError
    │   ├── TrainingError
    │   └── InferenceError
    ├── AuthenticationError
    │   ├── InvalidCredentialsError
    │   └── TokenExpiredError
    └── SystemError
"""

from typing import Any, Dict, Optional

__all__ = [
    "InsiderThreatBaseException",
    "ValidationError",
    "DatabaseError",
    "DatabaseConnectionError",
    "DatabaseQueryError",
    "GraphError",
    "GraphBuildError",
    "GraphQueryError",
    "AIError",
    "ModelLoadError",
    "TrainingError",
    "InferenceError",
    "AuthenticationError",
    "InvalidCredentialsError",
    "TokenExpiredError",
    "SystemError",
]


class InsiderThreatBaseException(Exception):
    """
    Base exception for all Insider Threat Detection System errors.

    Attributes:
        message: Human-readable error message.
        error_code: Machine-readable error code for API responses.
        details: Additional context about the error.
    """

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize exception to dictionary for API responses."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
        }


# ---------------------------------------------------------------------------
# Validation Errors
# ---------------------------------------------------------------------------
class ValidationError(InsiderThreatBaseException):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, error_code="VALIDATION_ERROR", details=details)


# ---------------------------------------------------------------------------
# Database Errors
# ---------------------------------------------------------------------------
class DatabaseError(InsiderThreatBaseException):
    """Base exception for database-related errors."""

    def __init__(self, message: str = "Database error", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, error_code="DATABASE_ERROR", details=details)


class DatabaseConnectionError(DatabaseError):
    """Raised when a database connection cannot be established."""

    def __init__(
        self, message: str = "Database connection failed", details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, details=details)
        self.error_code = "DATABASE_CONNECTION_ERROR"


class DatabaseQueryError(DatabaseError):
    """Raised when a database query fails."""

    def __init__(
        self, message: str = "Database query failed", details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, details=details)
        self.error_code = "DATABASE_QUERY_ERROR"


# ---------------------------------------------------------------------------
# Graph Errors
# ---------------------------------------------------------------------------
class GraphError(InsiderThreatBaseException):
    """Base exception for graph-related errors."""

    def __init__(self, message: str = "Graph error", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, error_code="GRAPH_ERROR", details=details)


class GraphBuildError(GraphError):
    """Raised when graph construction fails."""

    def __init__(
        self, message: str = "Graph build failed", details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, details=details)
        self.error_code = "GRAPH_BUILD_ERROR"


class GraphQueryError(GraphError):
    """Raised when a graph query fails."""

    def __init__(
        self, message: str = "Graph query failed", details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, details=details)
        self.error_code = "GRAPH_QUERY_ERROR"


# ---------------------------------------------------------------------------
# AI / ML Errors
# ---------------------------------------------------------------------------
class AIError(InsiderThreatBaseException):
    """Base exception for AI/ML-related errors."""

    def __init__(self, message: str = "AI error", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, error_code="AI_ERROR", details=details)


class ModelLoadError(AIError):
    """Raised when a model fails to load."""

    def __init__(self, message: str = "Model load failed", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, details=details)
        self.error_code = "MODEL_LOAD_ERROR"


class TrainingError(AIError):
    """Raised when model training encounters an error."""

    def __init__(self, message: str = "Training failed", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, details=details)
        self.error_code = "TRAINING_ERROR"


class InferenceError(AIError):
    """Raised when model inference fails."""

    def __init__(self, message: str = "Inference failed", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, details=details)
        self.error_code = "INFERENCE_ERROR"


# ---------------------------------------------------------------------------
# Authentication Errors
# ---------------------------------------------------------------------------
class AuthenticationError(InsiderThreatBaseException):
    """Base exception for authentication errors."""

    def __init__(
        self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, error_code="AUTH_ERROR", details=details)


class InvalidCredentialsError(AuthenticationError):
    """Raised when credentials are invalid."""

    def __init__(
        self, message: str = "Invalid credentials", details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, details=details)
        self.error_code = "INVALID_CREDENTIALS"


class TokenExpiredError(AuthenticationError):
    """Raised when a JWT token has expired."""

    def __init__(self, message: str = "Token expired", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, details=details)
        self.error_code = "TOKEN_EXPIRED"


# ---------------------------------------------------------------------------
# System Errors
# ---------------------------------------------------------------------------
class SystemError(InsiderThreatBaseException):
    """Raised for critical system-level errors."""

    def __init__(
        self, message: str = "System error", details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, error_code="SYSTEM_ERROR", details=details)
