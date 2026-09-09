import sys
from pathlib import Path

from loguru import logger

from backend.app.core.config import get_settings

__all__ = ["setup_logging", "get_logger"]

LOG_CATEGORIES: dict[str, str] = {
    "app": "app",
    "training": "training",
    "prediction": "predictions",
    "api": "api",
    "security": "security",
    "error": "errors",
}

_configured = False


def setup_logging() -> None:
    global _configured
    if _configured:
        return

    settings = get_settings()
    log_path = Path(settings.log_dir)
    level = settings.log_level.upper()

    logger.remove()

    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    for category, subdir in LOG_CATEGORIES.items():
        category_dir = log_path / subdir
        category_dir.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(category_dir / "{time:YYYY-MM-DD}.log"),
            level=level if category != "error" else "ERROR",
            rotation="100 MB",
            retention="30 days",
            compression="gz",
            filter=lambda record, cat=category: record["extra"].get("category") == cat,
            serialize=settings.is_production,
        )

    _configured = True


def get_logger(name: str = "app") -> logger.__class__:
    if not _configured:
        setup_logging()
    return logger.bind(category=name)
