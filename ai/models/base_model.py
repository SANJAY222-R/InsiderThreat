"""
Abstract Base Model
===================

Defines the standard interface for neural network models and classical baselines.
Provides serialization, deserialization, configuration management, and inference methods.
"""

from abc import ABC, abstractmethod
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

__all__ = ["BaseModel"]


class BaseModel(ABC):
    """
    Abstract base class for all Insider Threat AI models.

    Defines forward computation, persistence, configuration serialization,
    and inference execution contracts.
    """

    def __init__(self, name: str = "BaseModel", version: str = "1.0.0", config: Optional[Dict[str, Any]] = None) -> None:
        self.name = name
        self.version = version
        self.config = config or {}
        self.is_trained = False

    @abstractmethod
    def forward(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute forward pass through the model architecture.
        """
        ...

    def predict(self, inputs: Any) -> Any:
        """
        Generate predictions on given input data.
        """
        return self.forward(inputs)

    def save(self, path: Union[str, Path]) -> None:
        """
        Save model configuration, metadata, and weights to disk.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        meta = {
            "name": self.name,
            "version": self.version,
            "config": self.config,
            "is_trained": self.is_trained,
        }

        with open(path.with_suffix(".json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

    def load(self, path: Union[str, Path]) -> None:
        """
        Load model configuration, metadata, and weights from disk.
        """
        path = Path(path)
        meta_file = path.with_suffix(".json")
        if meta_file.exists():
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
            self.name = meta.get("name", self.name)
            self.version = meta.get("version", self.version)
            self.config = meta.get("config", self.config)
            self.is_trained = meta.get("is_trained", self.is_trained)

    def get_config(self) -> Dict[str, Any]:
        """
        Return model hyperparameters and configuration.
        """
        return {
            "name": self.name,
            "version": self.version,
            "config": self.config,
            "is_trained": self.is_trained,
        }

    def summary(self) -> str:
        """
        Return human-readable summary of model architecture and parameters.
        """
        return f"{self.name} (version: {self.version}) - Config: {self.config}"
