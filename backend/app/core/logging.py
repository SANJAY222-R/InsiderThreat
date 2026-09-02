"""
Centralized Logging Configuration
==================================

Loguru-based logging with structured output and multiple sinks.

Supports:
    - Application logs  → logs/app/
    - Training logs     → logs/training/
    - Prediction logs   → logs/predictions/
    - API logs          → logs/api/
    - Security logs     → logs/security/
    - Error logs        → logs/errors/

Phase 0: Configuration stubs. Logger setup for future phases.
"""

from pathlib import Path
from typing import Any

__all__ = ["setup_logging", "get_logger"]

# Log categories and their subdirectories
LOG_CATEGORIES: dict[str, str] = {
    "app": "app",
    "training": "training",
    "prediction": "predictions",
    "api": "api",
    "security": "security",
    "error": "errors",
}


def setup_logging(
    log_dir: str | Path = "./logs",
    log_level: str = "DEBUG",
    json_output: bool = False,
) -> None:
    """
    Configure centralized logging with Loguru.

    Creates log directories and configures file + console sinks
    for each log category.

    Args:
        log_dir: Root directory for log files.
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        json_output: If True, output structured JSON logs.

    TODO (Phase 1):
        - Configure Loguru sinks for each category
        - Add log rotation (daily, 100MB max)
        - Add log retention (30 days)
        - Add structured JSON serialization
        - Add correlation ID injection
        - Intercept stdlib logging
    """
    log_path = Path(log_dir)
    for category, subdir in LOG_CATEGORIES.items():
        (log_path / subdir).mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "app") -> Any:
    """
    Get a logger instance for the specified category.

    Args:
        name: Logger category name (app, training, prediction, api, security, error).

    Returns:
        Configured Loguru logger.

    TODO (Phase 1): Return bound Loguru logger with category context.
    """
    raise NotImplementedError("Phase 1: Loguru logger setup")
