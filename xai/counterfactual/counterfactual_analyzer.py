from typing import Dict, Any, List

class CounterfactualAnalyzer:
    """
    Generates counterfactual explanations by simulating perturbation of input features.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('counterfactuals', {})
        self.perturbation_types = self.config.get('perturbation_types', [])
        
    def run_what_if_scenarios(self, prediction_data: Dict[str, Any], behavior_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Runs "What-If" scenarios to estimate risk changes.
        """
        original_risk = prediction_data.get('risk_score', 0.0)
        scenarios = []
        
        # Stub logic for MVP: We simulate the score change based on the behaviors present
        anomalies = [a['type'] for a in behavior_data.get('anomalies', [])]
        
        for pert in self.perturbation_types:
            scenario = {
                'scenario': pert,
                'original_risk': original_risk,
                'estimated_new_risk': original_risk,
                'risk_delta': 0.0,
                'description': ''
            }
            
            if pert == "remove_usb_events" and 'USB Misuse' in anomalies:
                scenario['estimated_new_risk'] = max(0.0, original_risk - 25.0)
                scenario['description'] = "What if USB activity did not occur?"
                
            elif pert == "normalize_login_time" and 'Abnormal Login Time' in anomalies:
                scenario['estimated_new_risk'] = max(0.0, original_risk - 15.0)
                scenario['description'] = "What if login time was normal?"
                
            elif pert == "reduce_file_access" and 'Excessive File Access' in anomalies:
                scenario['estimated_new_risk'] = max(0.0, original_risk - 30.0)
                scenario['description'] = "What if file access volume was reduced below threshold?"
                
            else:
                continue # Skip if scenario isn't relevant to this user's anomalies
                
            scenario['risk_delta'] = scenario['estimated_new_risk'] - original_risk
            scenarios.append(scenario)
            
        return scenarios
