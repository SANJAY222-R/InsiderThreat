"""
Test: Model Loading and Inference
"""

import pytest


class TestModelLoading:
    """Tests for model checkpoint loading."""

    @pytest.mark.slow
    def test_model_loads_from_checkpoint(self) -> None:
        """Should load model weights from checkpoint file."""
        from ai.inference.predictor import Predictor
        predictor = Predictor()
        assert predictor is not None
        assert predictor.model_version == "1.0.0"

    def test_predictor_returns_valid_risk_score(self) -> None:
        from ai.inference.predictor import Predictor
        predictor = Predictor()
        result = predictor.predict("MOH0273")
        assert "risk_score" in result
        assert 0.0 <= result["risk_score"] <= 100.0
        assert result["threat_level"] in ("CRITICAL", "HIGH", "MEDIUM", "LOW")

    def test_predictor_feature_importance_present(self) -> None:
        from ai.inference.predictor import Predictor
        predictor = Predictor()
        result = predictor.predict(
            "TEST001",
            context={
                "is_after_hours": 1.0,
                "failed_login_ratio": 0.6,
                "usb_insertion_count": 2.0,
                "file_download_bytes_mb": 300.0,
                "sensitive_resource_access": 3.0,
                "email_external_ratio": 0.5,
                "device_switching_count": 1.0,
            },
        )
        explanation = result.get("explanation", {})
        assert "feature_importance" in explanation
        assert len(explanation["feature_importance"]) > 0

    def test_predictor_high_risk_context_yields_high_score(self) -> None:
        from ai.inference.predictor import Predictor
        predictor = Predictor()
        result = predictor.predict(
            "HIGHRISK001",
            context={
                "is_after_hours": 1.0,
                "failed_login_ratio": 1.0,
                "usb_insertion_count": 10.0,
                "file_download_bytes_mb": 1000.0,
                "sensitive_resource_access": 10.0,
                "email_external_ratio": 1.0,
                "device_switching_count": 5.0,
            },
        )
        assert result["risk_score"] >= 30.0  # At minimum MEDIUM


class TestXAIExplainers:
    """Tests for the three XAI explainer modules."""

    def test_feature_importance_explain(self) -> None:
        from ai.explainability.feature_importance import FeatureImportance
        explainer = FeatureImportance()
        result = explainer.explain("MOH0273", context={"risk_score": 94.2})
        assert "target_id" in result
        assert "feature_attributions" in result
        attributions = result["feature_attributions"]
        assert len(attributions) > 0
        for val in attributions.values():
            assert isinstance(val, float)

    def test_feature_importance_counterfactuals(self) -> None:
        from ai.explainability.feature_importance import FeatureImportance
        explainer = FeatureImportance()
        result = explainer.explain("MOH0273", context={"risk_score": 94.2})
        assert "counterfactuals" in result
        cfs = result["counterfactuals"]
        assert isinstance(cfs, list)
        assert len(cfs) > 0

    def test_gnn_explainer_returns_subgraph(self) -> None:
        from ai.explainability.gnn_explainer import GNNExplainerWrapper
        explainer = GNNExplainerWrapper()
        result = explainer.explain("MOH0273", context={"risk_score": 94.2})
        assert "nodes" in result
        assert "edges" in result
        assert isinstance(result["nodes"], list)
        assert isinstance(result["edges"], list)

    def test_gnn_nodes_have_required_fields(self) -> None:
        from ai.explainability.gnn_explainer import GNNExplainerWrapper
        explainer = GNNExplainerWrapper()
        result = explainer.explain("MOH0273", context={"risk_score": 94.2})
        for node in result["nodes"]:
            assert "id" in node or "node_id" in node

    def test_attention_explainer_returns_heads(self) -> None:
        from ai.explainability.attention_explainer import AttentionExplainer
        explainer = AttentionExplainer()
        result = explainer.explain("MOH0273", context={"risk_score": 94.2})
        assert "attention_heads" in result
        assert isinstance(result["attention_heads"], list)
        assert len(result["attention_heads"]) > 0

    def test_attention_heads_sum_to_one(self) -> None:
        from ai.explainability.attention_explainer import AttentionExplainer
        explainer = AttentionExplainer()
        result = explainer.explain("MOH0273", context={"risk_score": 94.2})
        weights = [h.get("weight", 0) for h in result["attention_heads"]]
        total = sum(weights)
        assert abs(total - 1.0) < 0.01, f"Attention weights sum to {total}, expected ~1.0"
