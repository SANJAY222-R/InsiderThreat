"""
Abstract Base Model
===================

Base class for all neural network models in the system.
Defines the standard interface for training, inference, and serialization.

Phase 0: Interface definition only.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

__all__ = ["BaseModel"]


class BaseModel(ABC):
    """
    Abstract base class for all AI models.

    Subclasses must implement forward(), save(), and load().

    TODO (Phase 4): Implement with torch.nn.Module inheritance.
    """

    @abstractmethod
    def forward(self, *args: Any, **kwargs: Any) -> Any:
        """Forward pass through the model."""
        ...

    @abstractmethod
    def save(self, path: Path) -> None:
        """Save model weights and config to disk."""
        ...

    @abstractmethod
    def load(self, path: Path) -> None:
        """Load model weights and config from disk."""
        ...

    @abstractmethod
    def get_config(self) -> dict[str, Any]:
        """Return model configuration as a dictionary."""
        ...
