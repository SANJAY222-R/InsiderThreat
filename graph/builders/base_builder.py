"""
Abstract Graph Builder
======================

Defines the interface for constructing heterogeneous temporal graphs
from enterprise log data.

Phase 0: Interface only.
"""

from abc import ABC, abstractmethod
from typing import Any

__all__ = ["BaseGraphBuilder"]


class BaseGraphBuilder(ABC):
    """
    Abstract base class for graph builders.

    Subclasses implement specific node/edge construction logic.

    TODO (Phase 3): Implement with NetworkX / PyG backends.
    """

    @abstractmethod
    def build(self, data: Any) -> Any:
        """Build graph from input data."""
        ...

    @abstractmethod
    def validate(self) -> bool:
        """Validate the constructed graph."""
        ...

    @abstractmethod
    def get_statistics(self) -> dict[str, Any]:
        """Return graph statistics (nodes, edges, density, etc.)."""
        ...
