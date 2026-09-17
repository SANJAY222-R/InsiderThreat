"""
ExplainabilityService
=====================

Business logic for XAI explanations for model predictions.
Orchestrates FeatureImportance, GNNExplainerWrapper, and AttentionExplainer.
"""

from typing import Any, Dict, Optional

from ai.explainability.attention_explainer import AttentionExplainer
from ai.explainability.feature_importance import FeatureImportance
from ai.explainability.gnn_explainer import GNNExplainerWrapper

__all__ = ["ExplainabilityService"]


class ExplainabilityService:
    """
    Service layer for XAI explanations for model predictions.
    """

    def __init__(self) -> None:
        self._feat_importance = FeatureImportance()
        self._gnn_explainer = GNNExplainerWrapper()
        self._attention_explainer = AttentionExplainer()

    def get_feature_explanation(
        self,
        employee_id: str,
        risk_score: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        ctx = {"risk_score": risk_score, **(context or {})}
        result = self._feat_importance.explain(employee_id, context=ctx)
        return {
            "employee_id": employee_id,
            "risk_score": risk_score,
            "feature_importance": result.get("feature_attributions", {}),
            "counterfactuals": result.get("counterfactuals", []),
            "method": "SHAP-style Feature Attribution",
            "explainer": result.get("explainer", "FeatureImportance"),
        }

    def get_subgraph_explanation(
        self,
        employee_id: str,
        risk_score: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        ctx = {"risk_score": risk_score, **(context or {})}
        return self._gnn_explainer.explain(employee_id, context=ctx)

    def get_attention_explanation(
        self,
        employee_id: str,
        risk_score: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        ctx = {"risk_score": risk_score, **(context or {})}
        return self._attention_explainer.explain(employee_id, context=ctx)

    def get_full_explanation(
        self,
        employee_id: str,
        risk_score: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        feat = self.get_feature_explanation(employee_id, risk_score, context)
        subgraph = self.get_subgraph_explanation(employee_id, risk_score, context)
        attention = self.get_attention_explanation(employee_id, risk_score, context)
        return {
            "employee_id": employee_id,
            "risk_score": risk_score,
            "feature_importance": feat["feature_importance"],
            "counterfactuals": feat["counterfactuals"],
            "subgraph": {
                "nodes": subgraph.get("nodes", []),
                "edges": subgraph.get("edges", []),
            },
            "attention_heads": attention.get("attention_heads", []),
        }
