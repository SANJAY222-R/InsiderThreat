import logging
from typing import Dict, Any, List
import yaml

from threat_detection.risk_engine.scoring_engine import ScoringEngine
from threat_detection.classification.classifier import ThreatClassifier
from threat_detection.behavior_analysis.behavior_analyzer import BehaviorAnalyzer
from threat_detection.alerts.alert_generator import AlertGenerator, Alert
from threat_detection.alerts.prioritizer import AlertPrioritizer
from threat_detection.incidents.correlation_engine import CorrelationEngine, Incident
from threat_detection.history.history_manager import HistoryManager
from threat_detection.reports.reporting_engine import ReportingEngine

logger = logging.getLogger(__name__)

class DetectionEngine:
    """
    Main pipeline coordinating the flow from THGNN scores and behavioral features 
    to final alerts, incidents, and reports.
    """
    def __init__(self, config_path: str = "configs/detection_config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.scoring_engine = ScoringEngine(self.config)
        self.classifier = ThreatClassifier(self.config)
        self.behavior_analyzer = BehaviorAnalyzer(self.config)
        self.alert_generator = AlertGenerator(self.config)
        self.prioritizer = AlertPrioritizer(self.config)
        self.correlation_engine = CorrelationEngine(self.config)
        self.history_manager = HistoryManager(self.config)
        self.reporting_engine = ReportingEngine(self.config)
        
        self.active_incidents: List[Incident] = []
        
    def process_user_activity(self, user_id: str, thgnn_base_prob: float, session_data: List[Dict[str, Any]]):
        """
        Process a user's recent activity batch.
        """
        user_alerts = []
        session_probs = []
        anomalies_list = []
        
        # 1. Analyze sessions
        for session in session_data:
            session_prob = session.get('thgnn_session_prob', thgnn_base_prob)
            session_probs.append(session_prob)
            
            # Behavior Analysis
            anomalies = self.behavior_analyzer.analyze_session(session)
            if anomalies:
                anomalies_list.extend(anomalies)
                
        # 2. Risk Scoring
        penalty = self.behavior_analyzer.calculate_anomaly_penalty(anomalies_list)
        risk_score = self.scoring_engine.calculate_user_risk(thgnn_base_prob, session_probs, behavior_penalty=penalty)
        
        # 3. Classification
        severity = self.classifier.classify(risk_score)
        
        # 4. History
        self.history_manager.save_user_risk(user_id, risk_score, severity)
        
        # 5. Alert Generation
        alert = self.alert_generator.generate_alert(
            user_id=user_id,
            risk_score=risk_score,
            severity=severity,
            anomalies=anomalies_list,
            assets=[s.get('host_id') for s in session_data if s.get('host_id')]
        )
        
        if alert:
            user_alerts.append(alert)
            
        return user_alerts
        
    def run_pipeline(self, batch_data: List[Dict[str, Any]]):
        """
        Executes the full pipeline for a batch of users.
        batch_data format: [{'user_id': 'u1', 'thgnn_prob': 0.8, 'sessions': [...]}, ...]
        """
        new_alerts = []
        
        # Process all users in batch
        for data in batch_data:
            alerts = self.process_user_activity(
                user_id=data['user_id'],
                thgnn_base_prob=data['thgnn_prob'],
                session_data=data.get('sessions', [])
            )
            new_alerts.extend(alerts)
            
        # Prioritize alerts
        # For MVP, assume uniform asset criticality
        prioritized_alerts = self.prioritizer.prioritize(new_alerts, asset_criticality={})
        
        # Correlate into Incidents
        self.active_incidents = self.correlation_engine.group_alerts(prioritized_alerts, self.active_incidents)
        
        # Save incident history and generate reports for critical ones
        for incident in self.active_incidents:
            self.history_manager.save_incident(incident)
            if incident.severity in ['HIGH', 'CRITICAL']:
                self.reporting_engine.generate_incident_report(incident, format='markdown')
                
        # Generate SOC Summary
        if self.active_incidents:
            self.reporting_engine.generate_soc_summary(self.active_incidents, format='csv')
            
        logger.info(f"Pipeline complete. Generated {len(prioritized_alerts)} alerts and correlated into {len(self.active_incidents)} incidents.")
        return self.active_incidents
