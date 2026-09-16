import os
import json
import logging
import urllib.request
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class NLExplainer:
    """
    Generates analyst-friendly natural language explanations using
    Google Gemini LLM when GEMINI_API_KEY is available, with graceful
    fallback to deterministic templates.
    """
    def __init__(self, config: Dict[str, Any] = None):
        self.config = (config or {}).get('nl_generation', {})
        self.style = self.config.get('template_style', 'soc_analyst')
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    def _call_gemini(self, prompt: str) -> str:
        """Calls Google Gemini API using native urllib."""
        if not self.api_key:
            return ""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 800
                }
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
        except Exception as e:
            logger.warning(f"Gemini generation error, falling back to templates: {e}")
        return ""

    def generate_explanation(self, reasoning_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Takes structured reasoning and produces Short, Detailed, and Summary texts.
        Uses Gemini LLM if configured; otherwise uses deterministic templates.
        """
        user_id = reasoning_data.get('user_id', 'Unknown')
        severity = reasoning_data.get('prediction_severity', reasoning_data.get('severity', 'UNKNOWN'))
        behaviors = reasoning_data.get('supporting_behaviors', [])
        confidence = reasoning_data.get('confidence', 0.0)
        risk_score = reasoning_data.get('risk_score', 0.0)
        
        behaviors_str = ", ".join(behaviors) if behaviors else "unidentified anomalous activities"
        
        # Deterministic fallback explanations
        short_exp = f"User {user_id} classified as {severity} Risk ({risk_score}/100) due to {behaviors_str}."
        
        detailed_exp = (
            f"User {user_id} was classified as {severity} Risk with a confidence score of {confidence:.2f}. "
            f"The model's attention was primarily drawn to the following behaviors: {behaviors_str}. "
            f"Additionally, the temporal graph analysis identified critical timestamps and anomalous multi-hop interactions."
        )
        
        soc_summary = (
            f"**SOC ALERT SUMMARY**\n"
            f"- **Entity:** {user_id}\n"
            f"- **Threat Level:** {severity} (Risk Score: {risk_score}/100)\n"
            f"- **Key Drivers:** {behaviors_str}\n"
            f"- **AI Confidence:** {confidence:.2%}\n"
        )
        
        # If Gemini API Key is available, synthesize dynamic executive intelligence
        if self.api_key:
            prompt = (
                f"You are a Senior Cyber Threat Intelligence SOC Analyst. "
                f"Analyze this insider threat detection result and provide a structured security briefing:\n"
                f"- Entity (Employee ID): {user_id}\n"
                f"- Risk Score: {risk_score}/100\n"
                f"- Severity Level: {severity}\n"
                f"- Model Confidence: {confidence:.2%}\n"
                f"- Key Driver Behaviors: {behaviors_str}\n"
                f"- Supporting Graph Nodes/Edges: {reasoning_data.get('supporting_edges', [])}\n"
                f"Provide:\n"
                f"1. Executive Threat Summary (2-3 sentences)\n"
                f"2. Risk Analysis (Why this pattern indicates malicious insider intent)\n"
                f"3. Recommended SOC Mitigation Actions (3 bullet points)"
            )
            llm_text = self._call_gemini(prompt)
            if llm_text:
                soc_summary = llm_text
                detailed_exp = llm_text

        return {
            'short_explanation': short_exp,
            'detailed_explanation': detailed_exp,
            'soc_summary': soc_summary
        }
