"""
XAI Engine Test
===============

Tests all three XAI explainability modules against real employee scenarios.
Run from the project root: python scripts/test_xai_engine.py
"""

import sys
import os

# Add project root to path so ai.* imports resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.explainability.feature_importance import FeatureImportance
from ai.explainability.gnn_explainer import GNNExplainerWrapper
from ai.explainability.attention_explainer import AttentionExplainer
from ai.inference.predictor import Predictor


def test_feature_importance(employee_id: str, risk_score: float):
    print(f"\n{'='*60}")
    print(f"FEATURE IMPORTANCE EXPLAINER — {employee_id}")
    print(f"{'='*60}")
    explainer = FeatureImportance()
    result = explainer.explain(employee_id, context={"risk_score": risk_score})

    print(f"\nEmployee : {result['target_id']}")
    print(f"Explainer: {result.get('explainer', 'FeatureImportance')}")
    print("\nFeature Attributions:")
    for feat, score in result["feature_attributions"].items():
        bar = "█" * int(score * 30)
        print(f"  {feat:<35} {score:.3f}  {bar}")

    if result.get("counterfactuals"):
        print("\nCounterfactual Interventions (what would reduce risk):")
        for cf in result["counterfactuals"]:
            scenario = cf.get("scenario", cf.get("feature", ""))
            delta = cf.get("risk_delta", cf.get("impact", 0))
            print(f"  - {scenario}: risk would drop by {abs(delta):.1f} pts")


def test_gnn_explainer(employee_id: str, risk_score: float):
    print(f"\n{'='*60}")
    print(f"GNN SUBGRAPH EXPLAINER — {employee_id}")
    print(f"{'='*60}")
    explainer = GNNExplainerWrapper()
    result = explainer.explain(employee_id, context={"risk_score": risk_score})

    nodes = result.get("nodes", [])
    edges = result.get("edges", [])
    print(f"\nSubgraph: {len(nodes)} nodes, {len(edges)} edges")

    print("\nTop Nodes (by importance):")
    top_nodes = sorted(nodes, key=lambda n: n.get("importance", 0), reverse=True)[:5]
    for n in top_nodes:
        nid = n.get("id") or n.get("node_id", "?")
        ntype = n.get("type", "unknown")
        imp = n.get("importance", 0)
        print(f"  Node [{nid}] type={ntype}  importance={imp:.3f}")

    print("\nKey Edges:")
    for e in edges[:5]:
        src = e.get("source", "?")
        tgt = e.get("target", "?")
        w = e.get("weight", e.get("importance", 0))
        print(f"  {src} -> {tgt}  weight={w:.3f}")


def test_attention_explainer(employee_id: str, risk_score: float):
    print(f"\n{'='*60}")
    print(f"ATTENTION EXPLAINER — {employee_id}")
    print(f"{'='*60}")
    explainer = AttentionExplainer()
    result = explainer.explain(employee_id, context={"risk_score": risk_score})

    heads = result.get("attention_heads", [])
    print(f"\nAttention Heads: {len(heads)}")
    total_weight = sum(h.get("weight", 0) for h in heads)
    print(f"Sum of weights : {total_weight:.4f} (should be ~1.0)")

    print("\nPer-Head Analysis:")
    for head in sorted(heads, key=lambda h: h.get("weight", 0), reverse=True):
        name = head.get("name", head.get("head", "?"))
        weight = head.get("weight", 0)
        focus = head.get("focus", head.get("description", ""))
        bar = "█" * int(weight * 40)
        print(f"  {name:<35} {weight:.3f}  {bar}")
        if focus:
            print(f"    └─ {focus}")


def run_full_pipeline(employee_id: str, risk_score: float):
    print(f"\n{'#'*60}")
    print(f"FULL XAI PIPELINE — {employee_id}  (Risk Score: {risk_score})")
    print(f"{'#'*60}")

    predictor = Predictor()
    prediction = predictor.predict(employee_id)
    print(f"\nPredictor Output:")
    print(f"  Risk Score  : {prediction['risk_score']}")
    print(f"  Threat Level: {prediction['threat_level']}")
    print(f"  Confidence  : {prediction['confidence']}")

    test_feature_importance(employee_id, prediction["risk_score"])
    test_gnn_explainer(employee_id, prediction["risk_score"])
    test_attention_explainer(employee_id, prediction["risk_score"])


if __name__ == "__main__":
    employees = [
        ("MOH0273", 94.2),   # CRITICAL
        ("LAP0338", 78.5),   # HIGH
        ("ASD0577", 15.0),   # LOW
    ]

    print("XAI Engine Test Suite")
    print("Using modules: ai.explainability.feature_importance, gnn_explainer, attention_explainer")

    for emp_id, score in employees:
        run_full_pipeline(emp_id, score)

    print(f"\n{'='*60}")
    print("All XAI tests completed successfully.")
    print("="*60)
