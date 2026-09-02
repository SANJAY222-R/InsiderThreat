from fastapi import APIRouter, Depends
from backend.app.auth.dependencies import get_current_user

router = APIRouter(prefix="/xai", tags=["Explainability APIs"])

@router.get("/local/{user_id}")
def get_local_explanation(user_id: str, current_user=Depends(get_current_user)):
    """
    Mock endpoint to fetch local explanation for a prediction.
    """
    return {
        "user_id": user_id,
        "nl_summary": f"User {user_id} was classified as HIGH risk due to abnormal login times.",
        "top_features": [
            {"feature": "session_duration", "weight": 0.45},
            {"feature": "after_hours_login", "weight": 0.35}
        ]
    }

@router.post("/counterfactual/{user_id}")
def run_counterfactual(user_id: str, current_user=Depends(get_current_user)):
    """
    Mock endpoint for counterfactual analysis.
    """
    return {
        "user_id": user_id,
        "scenarios": [
            {"scenario": "remove_usb_events", "risk_drop": 25.0}
        ]
    }
