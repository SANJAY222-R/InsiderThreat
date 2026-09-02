"""
Application Configuration
=========================

Centralized configuration using Pydantic Settings.
Loads values from environment variables and .env files.
"""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        app_name: Application display name.
        app_env: Current environment (development/staging/production).
        app_debug: Enable debug mode.
        app_version: Semantic version string.
        backend_host: API server host.
        backend_port: API server port.
        database_url: SQLAlchemy database connection string.
        neo4j_uri: Neo4j Bolt URI.
        neo4j_user: Neo4j username.
        neo4j_password: Neo4j password.
        jwt_secret_key: Secret key for JWT token signing.
        jwt_algorithm: JWT signing algorithm.
        jwt_access_token_expire_minutes: Access token TTL in minutes.
        dataset_raw_path: Path to raw CERT r4.2 dataset.
        log_level: Logging level.
        log_dir: Directory for log files.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "InsiderThreatDetection"
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = True
    app_version: str = "0.1.0"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_workers: int = 4

    # Database
    database_url: str = "sqlite:///./data/insider_threat.db"

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "changeme"
    neo4j_database: str = "insiderthreat"

    # JWT
    jwt_secret_key: str = "CHANGE_ME_TO_RANDOM_SECRET"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Dataset
    dataset_raw_path: Path = Path("./r4.2")
    dataset_processed_path: Path = Path("./dataset/processed")

    # Logging
    log_level: str = "DEBUG"
    log_dir: Path = Path("./logs")

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"


def get_settings() -> Settings:
    """
    Get cached application settings instance.

    Returns:
        Settings: Application settings.

    TODO (Phase 1): Add lru_cache for singleton pattern.
    """
    return Settings()
