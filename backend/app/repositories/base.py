"""
Abstract Base Repository
========================

Defines the repository interface for all data access patterns.
Follows the Repository Pattern for clean separation of concerns.

Phase 0: Abstract interface only.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

__all__ = ["BaseRepository"]

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository defining standard CRUD operations.

    Type Parameters:
        T: The entity type managed by this repository.

    TODO (Phase 1): Add SQLAlchemy session dependency.
    """

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T | None:
        """Retrieve an entity by its primary key."""
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        """Retrieve a paginated list of entities."""
        ...

    @abstractmethod
    async def create(self, entity: Any) -> T:
        """Create a new entity."""
        ...

    @abstractmethod
    async def update(self, entity_id: int, data: Any) -> T | None:
        """Update an existing entity."""
        ...

    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        """Delete an entity by ID. Returns True if deleted."""
        ...
