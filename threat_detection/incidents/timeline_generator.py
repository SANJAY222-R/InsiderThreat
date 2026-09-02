from typing import List, Dict, Any
from dateutil import parser
from pydantic import BaseModel

class TimelineEvent(BaseModel):
    timestamp: str
    event_type: str
    description: str
    risk_delta: float = 0.0

class TimelineGenerator:
    """
    Constructs a chronological timeline of events for an incident or user.
    """
    def __init__(self):
        pass
        
    def generate_timeline(self, raw_events: List[Dict[str, Any]], alerts: List[Any]) -> List[TimelineEvent]:
        """
        Merges raw logs (logins, files, emails) and alerts into a sorted timeline.
        """
        timeline = []
        
        # 1. Parse raw events
        for event in raw_events:
            dt = event.get('timestamp', event.get('date'))
            if not dt: continue
            
            timeline.append(TimelineEvent(
                timestamp=dt,
                event_type=event.get('activity', event.get('type', 'Unknown Event')),
                description=str(event),
                risk_delta=0.0
            ))
            
        # 2. Parse alerts
        for alert in alerts:
            # Assume alert is an Alert object or dict
            is_dict = isinstance(alert, dict)
            dt = alert.get('timestamp') if is_dict else alert.timestamp
            desc = f"ALERT GENERATED: {alert.get('threat_category') if is_dict else alert.threat_category}"
            risk = alert.get('risk_score') if is_dict else alert.risk_score
            
            timeline.append(TimelineEvent(
                timestamp=dt,
                event_type="ALERT",
                description=desc,
                risk_delta=risk
            ))
            
        # Sort chronologically
        timeline.sort(key=lambda x: parser.parse(x.timestamp))
        return timeline
