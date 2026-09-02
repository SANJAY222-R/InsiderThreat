from typing import Dict, Any, List

class RiskReasoningEngine:
    """
    Generates structured reasoning for every prediction, aggregating evidence.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def generate_reasoning(self, prediction: Dict[str, Any], local_exp: Dict[str, Any], graph_exp: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produces the final structured reasoning payload.
        """
        return {
            'user_id': prediction.get('user_id'),
            'prediction_severity': prediction.get('severity'),
            'risk_score': prediction.get('risk_score'),
            'confidence': prediction.get('confidence', 0.85),
            'supporting_behaviors': local_exp.get('suspicious_behaviors', []),
            'supporting_nodes': graph_exp.get('important_nodes', []),
            'supporting_edges': graph_exp.get('important_edges', []),
            'temporal_evidence': local_exp.get('critical_timestamps', []),
            'alternative_hypotheses': [
                "User is performing sanctioned off-hours maintenance.",
                "Compromised credential being used by external actor."
            ]
        }
