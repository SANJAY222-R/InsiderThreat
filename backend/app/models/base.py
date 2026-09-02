
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

__all__ = ["Base"]


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Provides common columns: id, created_at, updated_at.

    TODO (Phase 1): Add soft-delete mixin, audit mixin.
    """
    pass
