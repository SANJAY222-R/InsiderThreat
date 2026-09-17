"""
BaseExplainer
=============

Abstract base class for all Explainable AI (XAI) modules in the system.
Defines interfaces for natural language explanations, feature attributions,
and counterfactual impact simulations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

__all__ = ["BaseExplainer"]


class BaseExplainer(ABC):
    """
    Abstract base class for threat explainability methods.
    """

    def __init__(self, name: str = "BaseExplainer") -> None:
        self.name = name

    @abstractmethod
    def explain(self, target_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate explainability output for a given entity or prediction.
        """
        ...
