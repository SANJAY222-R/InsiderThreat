from pydantic import BaseModel
from typing import List, Optional

class PredictionRequest(BaseModel):
    user_id: str
    session_ids: Optional[List[str]] = None

class PredictionResponse(BaseModel):
    user_id: str
    risk_score: float
    threat_level: str
    confidence: float
    prediction_time: str
