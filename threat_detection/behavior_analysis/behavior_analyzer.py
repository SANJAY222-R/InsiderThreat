import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class BehaviorAnalyzer:
    """
    Analyzes raw behavior and temporal features to identify explicit patterns:
    Abnormal Login Time, Excessive File Access, USB Misuse, etc.
    """
    def __init__(self, config: Dict[str, Any]):
        self.rules = config.get('behavioral_rules', {})
        
    def analyze_session(self, session_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyzes a single session for behavioral anomalies based on config thresholds.
        Returns a list of identified anomalies with supporting evidence.
        """
        anomalies = []
        
        # 1. Abnormal Login Hours
        login_hour = session_data.get('login_hour')
        if login_hour is not None:
            start_h = self.rules.get('abnormal_login_hours', {}).get('start_hour', 20)
            end_h = self.rules.get('abnormal_login_hours', {}).get('end_hour', 6)
            # if start > end, it crosses midnight
            is_abnormal = False
            if start_h > end_h:
                is_abnormal = (login_hour >= start_h) or (login_hour <= end_h)
            else:
                is_abnormal = (start_h <= login_hour <= end_h)
                
            if is_abnormal:
                anomalies.append({
                    'type': 'Abnormal Login Time',
                    'evidence': f"Login at hour {login_hour}, expected between {end_h} and {start_h}"
                })

        # 2. Excessive File Access
        file_count = session_data.get('file_access_count', 0)
        file_threshold = self.rules.get('excessive_file_access', {}).get('threshold', 50)
        if file_count > file_threshold:
            anomalies.append({
                'type': 'Excessive File Access',
                'evidence': f"Accessed {file_count} files in one session (threshold: {file_threshold})"
            })
            
        # 3. USB Misuse
        usb_events = session_data.get('usb_devices', [])
        allow_list = self.rules.get('usb_misuse', {}).get('allow_list', [])
        for usb in usb_events:
            if allow_list and usb not in allow_list:
                anomalies.append({
                    'type': 'USB Misuse',
                    'evidence': f"Unauthorized USB device connected: {usb}"
                })
        # If allow_list is empty, any USB might be an anomaly depending on strictness. 
        # For this MVP, if allow_list is empty, we don't flag unless strictly configured.
        
        # 4. Long Sessions
        duration = session_data.get('session_duration_hours', 0)
        duration_threshold = self.rules.get('long_session_hours', {}).get('threshold', 12)
        if duration > duration_threshold:
            anomalies.append({
                'type': 'Long Session',
                'evidence': f"Session lasted {duration} hours (threshold: {duration_threshold})"
            })

        return anomalies
        
    def calculate_anomaly_penalty(self, anomalies: List[Dict[str, Any]]) -> float:
        """
        Calculates a penalty score (0.0 to 1.0) based on the number and type of anomalies.
        """
        if not anomalies:
            return 0.0
        # Simple penalty mapping
        penalty = min(1.0, len(anomalies) * 0.2)
        return penalty
