import os
from typing import Dict, Any, List
import json

class XAIReporter:
    """
    Generates detailed PDF and Markdown Explainability Reports.
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_report(self, reasoning: Dict[str, Any], nl_exp: Dict[str, str], identifier: str, format: str = 'markdown') -> str:
        """
        Generates a comprehensive explainability report.
        """
        filepath = os.path.join(self.output_dir, f"XAI_Report_{identifier}.{format}")
        
        if format == 'markdown':
            content = f"# Explainability Report: {identifier}\n\n"
            content += f"**User:** {reasoning.get('user_id')}\n"
            content += f"**Risk Score:** {reasoning.get('risk_score')}\n"
            content += f"**Severity:** {reasoning.get('prediction_severity')}\n"
            content += f"**AI Confidence:** {reasoning.get('confidence'):.2%}\n\n"
            
            content += "## Natural Language Summary\n"
            content += f"{nl_exp.get('detailed_explanation')}\n\n"
            
            content += "## Supporting Behaviors\n"
            for b in reasoning.get('supporting_behaviors', []):
                content += f"- {b}\n"
                
            content += "\n## Counterfactual Analysis\n"
            # In a full flow, counterfactuals would be passed in
            content += "_See attached JSON data for what-if scenarios._\n"
            
            with open(filepath, 'w') as f:
                f.write(content)
                
        elif format == 'json':
            with open(filepath, 'w') as f:
                json.dump({
                    'reasoning': reasoning,
                    'nl_explanation': nl_exp
                }, f, indent=4)
                
        return filepath
