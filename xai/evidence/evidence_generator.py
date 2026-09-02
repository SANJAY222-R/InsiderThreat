from typing import Dict, Any, List

class EvidenceGenerator:
    """
    Generates investigation evidence: Suspicious Events, High-risk Sessions, Associated Resources.
    """
    def generate_evidence(self, alert_data: Dict[str, Any], behavior_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compiles the evidence object.
        """
        evidence = {
            'suspicious_events': [],
            'important_relationships': [],
            'high_risk_sessions': [],
            'associated_resources': alert_data.get('affected_assets', []),
            'risk_timeline': [] # Timeline objects
        }
        
        # Populate from behavior data anomalies
        if 'anomalies' in behavior_data:
            for anomaly in behavior_data['anomalies']:
                evidence['suspicious_events'].append({
                    'event_type': anomaly.get('type'),
                    'description': anomaly.get('evidence')
                })
                
        return evidence
