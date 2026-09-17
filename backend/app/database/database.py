from collections.abc import Generator
from typing import Any
from sqlalchemy import Engine, create_engine, pool, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.core.config import get_settings

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "get_normalized_database_url",
    "create_db_engine",
    "check_db_connection",
    "check_database_liveness",
]


def get_normalized_database_url(url: str) -> str:
    """Normalize database connection URLs for SQLAlchemy 2.0 with modern psycopg driver."""
    if not url:
        return "sqlite:///./insider_threat.db"

    # Convert legacy postgres:// to postgresql+psycopg://
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)

    # Convert postgresql:// to postgresql+psycopg:// (psycopg 3)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)

    return url


def create_db_engine(db_url: str | None = None, **kwargs: Any) -> Engine:
    """Factory function to build a production-ready SQLAlchemy Engine with optimal pooling."""
    settings = get_settings()
    target_url = get_normalized_database_url(db_url or settings.database_url)

    connect_args: dict[str, Any] = kwargs.pop("connect_args", {})

    if target_url.startswith("sqlite"):
        connect_args.setdefault("check_same_thread", False)
        return create_engine(
            target_url,
            connect_args=connect_args,
            echo=kwargs.pop("echo", settings.db_echo),
            **kwargs,
        )

    # PostgreSQL / Neon configuration with robust connection pooling & pre-ping
    poolclass = kwargs.get("poolclass")
    engine_kwargs: dict[str, Any] = {
        "echo": kwargs.pop("echo", settings.db_echo),
        "connect_args": connect_args,
    }

    if poolclass is pool.NullPool or (isinstance(poolclass, type) and issubclass(poolclass, pool.NullPool)):
        pass
    else:
        engine_kwargs.update(
            {
                "pool_size": kwargs.pop("pool_size", settings.db_pool_size),
                "max_overflow": kwargs.pop("max_overflow", settings.db_max_overflow),
                "pool_recycle": kwargs.pop("pool_recycle", settings.db_pool_recycle),
                "pool_timeout": kwargs.pop("pool_timeout", settings.db_pool_timeout),
                "pool_pre_ping": kwargs.pop("pool_pre_ping", settings.db_pool_pre_ping),
            }
        )

    engine_kwargs.update(kwargs)
    return create_engine(target_url, **engine_kwargs)


settings = get_settings()
engine: Engine = create_db_engine()
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection(target_engine: Engine | None = None) -> tuple[bool, str]:
    """Verify database connectivity and return status along with database version."""
    eng = target_engine or engine
    try:
        with eng.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            if result == 1:
                return True, "Database connection healthy"
            return False, "Unexpected health query response"
    except Exception as exc:
        return False, f"Database connection failed: {exc}"


def check_database_liveness(target_engine: Engine | None = None) -> bool:
    """Check database liveness for health probes."""
    is_healthy, _ = check_db_connection(target_engine)
    return is_healthy

