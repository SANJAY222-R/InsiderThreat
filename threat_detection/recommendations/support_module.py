from typing import List, Dict, Any
from threat_detection.incidents.correlation_engine import Incident

class InvestigationSupport:
    """
    Generates investigation artifacts like Behavior Summaries and Top Suspicious Activities.
    """
    def generate_summary(self, incident: Incident) -> Dict[str, Any]:
        """
        Creates a high-level summary of an incident for SOC Analysts.
        """
        anomaly_types = set()
        for alert in incident.alerts:
            for evidence in alert.supporting_evidence:
                # Evidence is expected to be dict with 'type' and 'evidence'
                if isinstance(evidence, dict) and 'type' in evidence:
                    anomaly_types.add(evidence['type'])
                    
        return {
            'incident_id': incident.incident_id,
            'user': incident.user_id,
            'max_risk_score': incident.max_risk_score,
            'severity': incident.severity,
            'alert_count': len(incident.alerts),
            'affected_resources': incident.assets_involved,
            'identified_anomalies': list(anomaly_types),
            'summary_text': f"User {incident.user_id} generated {len(incident.alerts)} alerts "
                            f"reaching {incident.severity} severity, involving {len(incident.assets_involved)} assets."
        }
