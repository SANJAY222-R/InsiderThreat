from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ai.explainability.attention_explainer import AttentionExplainer
from ai.explainability.feature_importance import FeatureImportance
from ai.explainability.gnn_explainer import GNNExplainerWrapper
from backend.app.auth.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.prediction import Prediction
from backend.app.models.user import User

router = APIRouter()
feat_importance = FeatureImportance()
gnn_explainer = GNNExplainerWrapper()
attention_explainer = AttentionExplainer()


@router.get("/{prediction_id}")
def get_explanation(prediction_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> Dict[str, Any]:
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    explanation = prediction.explanation
    if not explanation or not explanation.get("feature_importance"):
        feat_result = feat_importance.explain(
            prediction.employee_id,
            context={"risk_score": prediction.risk_score},
        )
        explanation = {
            "feature_importance": feat_result["feature_attributions"],
            "top_features": [
                {"name": k, "value": v, "direction": "above_normal"}
                for k, v in list(feat_result["feature_attributions"].items())[:3]
            ],
            "counterfactuals": feat_result.get("counterfactuals", []),
            "model_version": prediction.model_version,
            "method": "Temporal Graph Attention (THGNN)",
        }

    return {
        "prediction_id": prediction.id,
        "employee_id": prediction.employee_id,
        "risk_score": prediction.risk_score,
        "threat_level": prediction.threat_level,
        "explanation": explanation,
    }


@router.get("/{prediction_id}/subgraph")
def get_subgraph_explanation(prediction_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> Dict[str, Any]:
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    return gnn_explainer.explain(
        prediction.employee_id,
        context={"risk_score": prediction.risk_score},
    )


@router.get("/{prediction_id}/attention")
def get_attention_explanation(prediction_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> Dict[str, Any]:
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    return attention_explainer.explain(
        prediction.employee_id,
        context={"risk_score": prediction.risk_score},
    )
