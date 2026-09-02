import os
import json
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime, timezone

from threat_detection.incidents.correlation_engine import Incident
from threat_detection.recommendations.support_module import InvestigationSupport
from threat_detection.recommendations.recommendation_engine import RecommendationEngine

class ReportingEngine:
    """
    Generates formatted Threat, User Risk, Incident, and SOC reports.
    """
    def __init__(self, config: Dict[str, Any]):
        self.reports_dir = config.get('engine', {}).get('reports_dir', 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        self.support = InvestigationSupport()
        self.recommendations = RecommendationEngine()
        
    def generate_incident_report(self, incident: Incident, format: str = 'markdown') -> str:
        """
        Generates a detailed incident report.
        """
        summary = self.support.generate_summary(incident)
        recs = self.recommendations.generate_recommendations(incident)
        
        filename = f"Incident_Report_{incident.incident_id}.{format}"
        filepath = os.path.join(self.reports_dir, filename)
        
        if format == 'markdown':
            content = f"# Incident Report: {incident.incident_id}\n\n"
            content += f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f"**User:** {incident.user_id}\n"
            content += f"**Severity:** {incident.severity}\n"
            content += f"**Max Risk Score:** {incident.max_risk_score}\n\n"
            
            content += "## Summary\n"
            content += f"{summary['summary_text']}\n\n"
            
            content += "## Recommendations\n"
            for r in recs:
                content += f"- {r}\n"
                
            content += "\n## Affected Assets\n"
            for a in incident.assets_involved:
                content += f"- {a}\n"
                
            with open(filepath, 'w') as f:
                f.write(content)
                
        elif format == 'json':
            with open(filepath, 'w') as f:
                json.dump({
                    'incident': incident.model_dump(),
                    'summary': summary,
                    'recommendations': recs
                }, f, indent=4)
                
        return filepath
        
    def generate_soc_summary(self, incidents: List[Incident], format: str = 'csv') -> str:
        """
        Generates a daily or weekly SOC summary.
        """
        filepath = os.path.join(self.reports_dir, f"SOC_Summary_{datetime.now(timezone.utc).strftime('%Y%m%d')}.{format}")
        
        records = []
        for inc in incidents:
            records.append({
                'IncidentID': inc.incident_id,
                'Date': inc.created_at,
                'User': inc.user_id,
                'Severity': inc.severity,
                'MaxRisk': inc.max_risk_score,
                'AlertCount': len(inc.alerts)
            })
            
        df = pd.DataFrame(records)
        
        if format == 'csv':
            df.to_csv(filepath, index=False)
        elif format == 'html':
            df.to_html(filepath, index=False)
            
        return filepath
