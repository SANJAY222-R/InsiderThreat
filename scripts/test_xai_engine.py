from xai.xai_engine import XAIEngine
import os

def test_xai():
    print("Initializing XAI Engine...")
    engine = XAIEngine(config_path="configs/xai_config.yaml")
    
    # Dummy Prediction Data (from Phase 7)
    prediction_data = {
        'user_id': 'U1234',
        'risk_score': 85.0,
        'severity': 'HIGH',
        'confidence': 0.92,
        'affected_assets': ['Server_Omega']
    }
    
    # Dummy Behavior Data (from Phase 7)
    behavior_data = {
        'anomalies': [
            {'type': 'Abnormal Login Time', 'evidence': 'Login at 3 AM'},
            {'type': 'USB Misuse', 'evidence': 'Unauthorized device insertion'}
        ]
    }
    
    print(f"Generating XAI for User {prediction_data['user_id']}...")
    reasoning, nl_exp = engine.generate_explanation(prediction_data, behavior_data)
    
    print("\n--- NATURAL LANGUAGE EXPLANATION ---")
    print(nl_exp['detailed_explanation'])
    
    print("\n--- COUNTERFACTUAL ANALYSIS ---")
    # Load and print counterfactuals from JSON to verify export
    import json
    with open('xai/visualizations/outputs/counterfactuals_U1234.json', 'r') as f:
        cfs = json.load(f)
        for cf in cfs:
            print(f"- {cf['scenario']}: Risk would drop by {abs(cf['risk_delta'])}")
            
    print("\nCheck 'xai/visualizations/outputs' and 'xai/reports/outputs' for exported artifacts.")

if __name__ == "__main__":
    test_xai()
