from typing import Dict, Any, List

class NLExplainer:
    """
    Automatically generates analyst-friendly natural language explanations 
    using deterministic templates.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('nl_generation', {})
        self.style = self.config.get('template_style', 'soc_analyst')
        
    def generate_explanation(self, reasoning_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Takes structured reasoning and produces Short, Detailed, and Summary texts.
        """
        user_id = reasoning_data.get('user_id', 'Unknown')
        severity = reasoning_data.get('severity', 'UNKNOWN')
        behaviors = reasoning_data.get('supporting_behaviors', [])
        confidence = reasoning_data.get('confidence', 0.0)
        
        behaviors_str = ", ".join(behaviors) if behaviors else "unidentified anomalous activities"
        
        short_exp = f"User {user_id} classified as {severity} Risk due to {behaviors_str}."
        
        detailed_exp = (
            f"User {user_id} was classified as {severity} Risk with a confidence score of {confidence:.2f}. "
            f"The model's attention was primarily drawn to the following behaviors: {behaviors_str}. "
            f"Additionally, the temporal analysis identified critical timestamps corresponding to these actions."
        )
        
        soc_summary = (
            f"**SOC ALERT SUMMARY**\n"
            f"- **Entity:** {user_id}\n"
            f"- **Threat Level:** {severity}\n"
            f"- **Key Drivers:** {behaviors_str}\n"
            f"- **AI Confidence:** {confidence:.2%}\n"
        )
        
        return {
            'short_explanation': short_exp,
            'detailed_explanation': detailed_exp,
            'soc_summary': soc_summary
        }
