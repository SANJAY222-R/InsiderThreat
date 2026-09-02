from fastapi import APIRouter, Depends
from backend.app.schemas.prediction_schema import PredictionRequest, PredictionResponse
from backend.app.auth.dependencies import get_current_user
from datetime import datetime, timezone
import random

router = APIRouter(prefix="/predictions", tags=["Threat Prediction"])

@router.post("/predict", response_model=PredictionResponse)
def predict_user_risk(request: PredictionRequest, current_user=Depends(get_current_user)):
    """
    Endpoint to trigger the THGNN + Threat Detection Engine.
    For this API MVP phase, we mock the inference output.
    """
    # Mocking inference from Phase 6 & 7
    mock_score = random.uniform(10.0, 95.0)
    level = "LOW"
    if mock_score > 75: level = "HIGH"
    elif mock_score > 50: level = "MEDIUM"
    elif mock_score > 90: level = "CRITICAL"
    
    return PredictionResponse(
        user_id=request.user_id,
        risk_score=round(mock_score, 2),
        threat_level=level,
        confidence=round(random.uniform(0.7, 0.99), 2),
        prediction_time=datetime.now(timezone.utc).isoformat()
    )
