from typing import List, Dict, Any
from threat_detection.incidents.correlation_engine import Incident

class RecommendationEngine:
    """
    Generates analyst recommendations based on threat categories and behaviors.
    """
    def __init__(self):
        # Basic mapping of anomaly type to recommendations
        self.rule_map = {
            'Abnormal Login Time': 'Review authentication logs for impossible travel or credential stuffing.',
            'Excessive File Access': 'Review accessed files for sensitive data exposure. Consider revoking access temporarily.',
            'USB Misuse': 'Disable USB mass storage on affected hosts. Isolate hosts from the network.',
            'Long Session': 'Force re-authentication for the user.',
            'MODEL_PREDICTION': 'Investigate user baseline behavior and recent organizational changes.'
        }
        
    def generate_recommendations(self, incident: Incident) -> List[str]:
        recommendations = set()
        
        # General recommendations based on severity
        if incident.severity in ['CRITICAL', 'HIGH']:
            recommendations.add("Escalate to Tier 2 SOC Analyst immediately.")
            recommendations.add("Consider temporary account suspension pending investigation.")
            
        # Specific recommendations based on alerts
        for alert in incident.alerts:
            if alert.threat_category == 'MODEL_PREDICTION':
                recommendations.add(self.rule_map['MODEL_PREDICTION'])
                
            for evidence in alert.supporting_evidence:
                anomaly_type = evidence.get('type')
                if anomaly_type in self.rule_map:
                    recommendations.add(self.rule_map[anomaly_type])
                    
        return list(recommendations)
