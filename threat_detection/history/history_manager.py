import os
import json
from typing import Dict, Any, List
from datetime import datetime, timezone

class HistoryManager:
    """
    Manages the persistence of Risk, Alert, Incident, and User histories.
    """
    def __init__(self, config: Dict[str, Any]):
        self.storage_type = config.get('engine', {}).get('storage_type', 'json')
        self.history_dir = config.get('engine', {}).get('history_dir', 'threat_detection/history/data')
        os.makedirs(self.history_dir, exist_ok=True)
        
    def save_incident(self, incident: Any):
        """
        Saves incident details.
        """
        if self.storage_type == 'json':
            path = os.path.join(self.history_dir, f"incident_{incident.incident_id}.json")
            with open(path, 'w') as f:
                json.dump(incident.model_dump(), f, indent=4)
                
    def save_user_risk(self, user_id: str, risk_score: float, severity: str):
        """
        Appends user risk to history.
        """
        if self.storage_type == 'json':
            path = os.path.join(self.history_dir, f"user_{user_id}_risk_history.jsonl")
            record = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'risk_score': risk_score,
                'severity': severity
            }
            with open(path, 'a') as f:
                f.write(json.dumps(record) + "\n")
                
    def get_user_risk_history(self, user_id: str) -> List[Dict[str, Any]]:
        path = os.path.join(self.history_dir, f"user_{user_id}_risk_history.jsonl")
        history = []
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    history.append(json.loads(line))
        return history
