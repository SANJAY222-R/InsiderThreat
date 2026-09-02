from typing import List, Dict, Any
from .alert_generator import Alert

class AlertPrioritizer:
    """
    Ranks generated alerts based on Risk Score, Asset Criticality, 
    and Historical Context.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def prioritize(self, alerts: List[Alert], asset_criticality: Dict[str, float] = None) -> List[Alert]:
        """
        Sorts alerts by a composite priority score.
        Priority = Risk Score + (Max Asset Criticality Bonus)
        """
        if not asset_criticality:
            asset_criticality = {}
            
        def get_priority_score(alert: Alert) -> float:
            base_score = alert.risk_score
            # Add bonus for critical assets
            asset_bonus = 0.0
            for asset in alert.affected_assets:
                bonus = asset_criticality.get(asset, 0.0)
                if bonus > asset_bonus:
                    asset_bonus = bonus
            return base_score + asset_bonus
            
        # Sort descending by priority score
        return sorted(alerts, key=get_priority_score, reverse=True)
