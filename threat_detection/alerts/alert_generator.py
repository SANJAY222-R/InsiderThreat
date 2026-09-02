from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime, timezone

class Alert(BaseModel):
    alert_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    user_id: str
    session_id: Optional[str] = None
    threat_category: str
    risk_score: float
    severity: str
    status: str = "NEW"
    affected_assets: List[str] = Field(default_factory=list)
    supporting_evidence: List[Dict[str, str]] = Field(default_factory=list)

class AlertGenerator:
    """
    Generates Pydantic-validated Alert objects.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('alerts', {})
        self.min_score = self.config.get('min_score_for_alert', 30)

    def generate_alert(self, 
                       user_id: str, 
                       risk_score: float, 
                       severity: str, 
                       anomalies: List[Dict[str, str]], 
                       session_id: Optional[str] = None,
                       assets: Optional[List[str]] = None) -> Optional[Alert]:
        """
        Creates an Alert if the risk score exceeds the minimum threshold.
        """
        if risk_score < self.min_score:
            return None
            
        threat_category = "BEHAVIORAL_ANOMALY" if anomalies else "MODEL_PREDICTION"
        
        alert = Alert(
            user_id=user_id,
            session_id=session_id,
            threat_category=threat_category,
            risk_score=risk_score,
            severity=severity,
            affected_assets=assets or [],
            supporting_evidence=anomalies
        )
        return alert
