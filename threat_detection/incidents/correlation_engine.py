from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime, timedelta, timezone
from dateutil import parser
from threat_detection.alerts.alert_generator import Alert

class Incident(BaseModel):
    incident_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    user_id: str
    alerts: List[Alert]
    max_risk_score: float = 0.0
    severity: str = "LOW"
    status: str = "OPEN"
    assets_involved: List[str] = Field(default_factory=list)

class CorrelationEngine:
    """
    Groups related alerts into Incidents based on time windows and user similarity.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('incidents', {})
        self.time_window_hours = self.config.get('correlation_window_hours', 24)
        
    def group_alerts(self, new_alerts: List[Alert], active_incidents: List[Incident]) -> List[Incident]:
        """
        Correlates new alerts into existing incidents, or creates new ones.
        For MVP, we group strictly by user_id within a time window.
        """
        for alert in new_alerts:
            alert_time = parser.parse(alert.timestamp)
            matched = False
            
            # Try to match with an active incident for the same user
            for incident in active_incidents:
                if incident.status != "OPEN":
                    continue
                if incident.user_id != alert.user_id:
                    continue
                    
                # Check time window from the incident creation
                incident_time = parser.parse(incident.created_at)
                if alert_time - incident_time <= timedelta(hours=self.time_window_hours):
                    # Match found
                    self._add_alert_to_incident(incident, alert)
                    matched = True
                    break
                    
            if not matched:
                # Create a new incident
                new_incident = Incident(
                    user_id=alert.user_id,
                    alerts=[alert],
                    max_risk_score=alert.risk_score,
                    severity=alert.severity,
                    assets_involved=alert.affected_assets.copy()
                )
                active_incidents.append(new_incident)
                
        return active_incidents

    def _add_alert_to_incident(self, incident: Incident, alert: Alert):
        incident.alerts.append(alert)
        if alert.risk_score > incident.max_risk_score:
            incident.max_risk_score = alert.risk_score
            incident.severity = alert.severity # Upgrade severity if needed
            
        for asset in alert.affected_assets:
            if asset not in incident.assets_involved:
                incident.assets_involved.append(asset)
