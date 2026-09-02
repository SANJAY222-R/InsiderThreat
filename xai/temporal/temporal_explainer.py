from typing import Dict, Any, List

class TemporalExplainer:
    """
    Explains temporal behavior and risk evolution across a timeline.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def explain_evolution(self, timeline_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes a sequence of events to explain how risk evolved over time.
        """
        evolution = {
            'timeline_explanation': "Risk remained low until a sudden spike during after-hours.",
            'critical_timestamps': [],
            'behavior_changes': [],
            'sliding_window_contribution': []
        }
        
        prev_risk = 0.0
        for event in timeline_events:
            current_risk = event.get('risk_score', 0.0)
            if current_risk - prev_risk > 20.0:
                evolution['critical_timestamps'].append(event.get('timestamp'))
                evolution['behavior_changes'].append(
                    f"Sharp risk increase (+{current_risk - prev_risk}) at {event.get('timestamp')} due to {event.get('type')}"
                )
            prev_risk = current_risk
            
        return evolution
