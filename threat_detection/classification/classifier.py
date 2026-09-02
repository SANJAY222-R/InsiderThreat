import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ThreatClassifier:
    """
    Maps normalized risk scores to threat levels 
    (Normal, Low, Medium, High, Critical) based on YAML thresholds.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('risk_scoring', {})
        self.severity_mapping = self.config.get('severity_mapping', {
            'normal': [0, 20],
            'low': [21, 50],
            'medium': [51, 75],
            'high': [76, 90],
            'critical': [91, 100]
        })
        
    def classify(self, score: float) -> str:
        """
        Classifies a 0-100 score into a discrete threat level.
        """
        for level, (min_val, max_val) in self.severity_mapping.items():
            if min_val <= score <= max_val:
                return level.upper()
                
        # Fallback for out-of-bounds (e.g. floats slightly above max due to rounding)
        if score > 100:
            return 'CRITICAL'
        return 'NORMAL'
