from threat_detection.detection_engine import DetectionEngine
import os

def test_engine() -> None:
    print("Initializing Detection Engine...")
    engine = DetectionEngine(config_path="configs/detection_config.yaml")
    
    # Dummy THGNN predictions + Raw behavior features
    batch_data = [
        {
            'user_id': 'U1234',
            'thgnn_prob': 0.85, # High model probability
            'sessions': [
                {
                    'session_id': 'S_1',
                    'host_id': 'PC-4001',
                    'thgnn_session_prob': 0.90,
                    'login_hour': 3, # Abnormal (3 AM)
                    'file_access_count': 120, # Excessive (> 50)
                    'usb_devices': ['USB_UNAUTHORIZED_01'],
                    'session_duration_hours': 14 # Long session (> 12)
                }
            ]
        },
        {
            'user_id': 'U9999',
            'thgnn_prob': 0.10, # Low model probability
            'sessions': [
                {
                    'session_id': 'S_2',
                    'host_id': 'PC-1002',
                    'thgnn_session_prob': 0.05,
                    'login_hour': 9, # Normal
                    'file_access_count': 10
                }
            ]
        }
    ]
    
    print("Running Pipeline...")
    incidents = engine.run_pipeline(batch_data)
    
    print(f"\nTotal Active Incidents: {len(incidents)}")
    for inc in incidents:
        print(f"Incident {inc.incident_id} | User {inc.user_id} | Severity {inc.severity} | Risk {inc.max_risk_score}")
        for alert in inc.alerts:
            print(f"  -> Alert: {alert.threat_category} | Evidence: {len(alert.supporting_evidence)}")
            
    print("\nCheck the 'reports' and 'threat_detection/history/data' directories for outputs!")

if __name__ == "__main__":
    test_engine()
