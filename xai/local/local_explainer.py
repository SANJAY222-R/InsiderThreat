from typing import Dict, Any, List

class LocalExplainer:
    """
    Generates local explanations for a specific prediction.
    Explains suspicious behaviors, critical timestamps, and feature logic.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def explain_prediction(self, prediction_data: Dict[str, Any], behavior_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes a local explanation based on model outputs and behavioral data.
        """
        user_id = prediction_data.get('user_id')
        risk_score = prediction_data.get('risk_score', 0.0)
        
        explanation = {
            'user_id': user_id,
            'risk_score': risk_score,
            'confidence': prediction_data.get('confidence', 0.0),
            'suspicious_behaviors': [],
            'critical_timestamps': [],
            'top_features': prediction_data.get('top_features', []),
            'important_interactions': []
        }
        
        # Extract behaviors
        if 'anomalies' in behavior_data:
            for anomaly in behavior_data['anomalies']:
                explanation['suspicious_behaviors'].append(anomaly['type'])
                
        # Extract timestamps (stub logic for MVP)
        if 'events' in behavior_data:
            for event in behavior_data['events']:
                if event.get('is_anomalous'):
                    explanation['critical_timestamps'].append(event.get('timestamp'))
                    explanation['important_interactions'].append(f"{event.get('type')} on {event.get('asset')}")
                    
        return explanation
