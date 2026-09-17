import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.app.core.config import get_settings
from backend.app.database.database import Base, create_db_engine, get_normalized_database_url
# Explicitly import all models to populate Base.metadata
from backend.app.models.alert import Alert  # noqa: F401
from backend.app.models.audit_log import AuditLog  # noqa: F401
from backend.app.models.prediction import Prediction  # noqa: F401
from backend.app.models.user import User  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    # 1. Main option explicitly provided in Alembic Config (e.g. programmatic override or CLI)
    main_url = config.get_main_option("sqlalchemy.url")
    if (
        main_url
        and main_url != "sqlite:///./insider_threat.db"
        and main_url != "driver://user:pass@localhost/dbname"
    ):
        return get_normalized_database_url(main_url)

    # 2. Environment variable DATABASE_URL
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return get_normalized_database_url(env_url)

    # 3. Application Settings
    try:
        settings = get_settings()
        if settings.database_url:
            return get_normalized_database_url(settings.database_url)
    except Exception:
        pass

    return get_normalized_database_url(
        main_url or "sqlite:///./insider_threat.db"
    )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Creates an Engine and associates a connection with the context.
    """
    url = get_url()
    connectable = create_db_engine(db_url=url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
