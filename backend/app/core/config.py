import secrets
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "InsiderThreatDetection"
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = False
    app_version: str = "1.0.0"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_workers: int = 4

    database_url: str = "sqlite:///./insider_threat.db"

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "changeme"
    neo4j_database: str = "insiderthreat"

    jwt_secret_key: str = "soc-nexus-super-secure-jwt-secret-key-32-chars-minimum-prod"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    dataset_raw_path: Path = Path("./r4.2")
    dataset_processed_path: Path = Path("./dataset/processed")

    log_level: str = "INFO"
    log_dir: Path = Path("./logs")

    cors_origins: str = "http://localhost:5173"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
