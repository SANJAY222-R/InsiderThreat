import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ScoringEngine:
    """
    Calculates and normalizes User, Session, Department, Host, and Organization 
    Risk Scores on a 0-100 scale using configurable weighting.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('risk_scoring', {})
        self.weights = self.config.get('weights', {
            'user_base_risk': 0.4,
            'session_max_risk': 0.3,
            'behavior_anomaly': 0.3
        })
        
    def normalize_score(self, raw_score: float) -> float:
        """
        Normalizes a raw prob/score (0.0 - 1.0) to a 0-100 scale.
        """
        score = max(0.0, min(1.0, raw_score)) * 100
        return round(score, 2)
        
    def calculate_user_risk(self, base_prob: float, session_probs: list, behavior_penalty: float = 0.0) -> float:
        """
        Aggregates THGNN base probability, max session probability, and behavioral penalties.
        """
        session_max = max(session_probs) if session_probs else base_prob
        
        # Calculate weighted risk (0.0 to 1.0 ideally)
        risk = (
            base_prob * self.weights.get('user_base_risk', 0.4) +
            session_max * self.weights.get('session_max_risk', 0.3) +
            behavior_penalty * self.weights.get('behavior_anomaly', 0.3)
        )
        
        return self.normalize_score(risk)
        
    def calculate_asset_risk(self, incident_scores: list) -> float:
        """
        General calculation for Hosts or Departments based on related incident severities.
        """
        if not incident_scores:
            return 0.0
        # Example logic: max score + log(len) penalty
        max_score = max(incident_scores)
        freq_penalty = min(20.0, len(incident_scores) * 2.0)
        
        return min(100.0, max_score + freq_penalty)
