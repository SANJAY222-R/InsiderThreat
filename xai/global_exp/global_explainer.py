from typing import Dict, Any, List
import pandas as pd

class GlobalExplainer:
    """
    Generates overall model explanations across all predictions.
    Ranks feature importance and node/edge type importance globally.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.feature_importances = {} # Aggregated state
        
    def aggregate_importance(self, local_attributions: Dict[str, float]):
        """
        Aggregates local feature attributions into a global state.
        """
        for feature, weight in local_attributions.items():
            if feature not in self.feature_importances:
                self.feature_importances[feature] = 0.0
            self.feature_importances[feature] += abs(weight)
            
    def get_global_explanation(self) -> Dict[str, Any]:
        """
        Returns the top globally important features and relationships.
        """
        # Sort features by aggregated importance
        sorted_features = sorted(self.feature_importances.items(), key=lambda x: x[1], reverse=True)
        
        # Stub global rankings for MVP
        explanation = {
            'top_node_types': ['User', 'Host', 'File'],
            'top_edge_types': ['LOGIN_TO', 'ACCESS_FILE', 'INSERT_USB'],
            'top_behavioral_patterns': ['Abnormal Login Hours', 'Excessive File Access'],
            'feature_importance_ranking': sorted_features[:20],
            'model_sensitivity': 'High sensitivity to USB events and after-hours logins.'
        }
        
        return explanation
