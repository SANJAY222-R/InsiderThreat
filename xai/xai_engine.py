import yaml
import logging
from typing import Dict, Any, List

from xai.local.local_explainer import LocalExplainer
from xai.global_exp.global_explainer import GlobalExplainer
from xai.graph.graph_explainer import GraphExplainer
from xai.temporal.temporal_explainer import TemporalExplainer
from xai.feature_importance.feature_attribution import FeatureAttributionModule
from xai.attention.attention_visualizer import AttentionVisualizer
from xai.evidence.evidence_generator import EvidenceGenerator
from xai.reasoning.nl_explainer import NLExplainer
from xai.reasoning.risk_reasoning import RiskReasoningEngine
from xai.counterfactual.counterfactual_analyzer import CounterfactualAnalyzer
from xai.reports.xai_reporter import XAIReporter
from xai.visualizations.exporter import XAIExporter

logger = logging.getLogger(__name__)

class XAIEngine:
    """
    Main Orchestrator for the Explainable AI (XAI) Engine.
    Coordinates all explanation modules for a given prediction or incident.
    """
    def __init__(self, config_path: str = "configs/xai_config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        outputs_dir = self.config.get('engine', {}).get('output_dir', 'xai/visualizations/outputs')
        reports_dir = self.config.get('engine', {}).get('reports_dir', 'xai/reports/outputs')
        
        self.local_explainer = LocalExplainer(self.config)
        self.global_explainer = GlobalExplainer(self.config)
        self.graph_explainer = GraphExplainer(self.config)
        self.temporal_explainer = TemporalExplainer(self.config)
        self.feature_attribution = FeatureAttributionModule(self.config)
        self.attention_visualizer = AttentionVisualizer(outputs_dir)
        self.evidence_generator = EvidenceGenerator()
        self.nl_explainer = NLExplainer(self.config)
        self.risk_reasoning = RiskReasoningEngine(self.config)
        self.counterfactual_analyzer = CounterfactualAnalyzer(self.config)
        self.reporter = XAIReporter(reports_dir)
        self.exporter = XAIExporter(outputs_dir)
        
    def generate_explanation(self, prediction_data: Dict[str, Any], behavior_data: Dict[str, Any], model: Any = None, graph_data: Any = None):
        """
        Generates end-to-end explanation for a prediction.
        """
        user_id = prediction_data.get('user_id')
        logger.info(f"Generating explanations for user {user_id}")
        
        # 1. Local Explanation
        local_exp = self.local_explainer.explain_prediction(prediction_data, behavior_data)
        
        # 2. Graph Explanation (Stub)
        graph_exp = self.graph_explainer.extract_explanation_subgraph(graph_data, "User", user_id) if graph_data else {}
        
        # 3. Feature Attribution (Stub)
        attributions = self.feature_attribution.attribute(model, None)
        
        # 4. Evidence Generation
        evidence = self.evidence_generator.generate_evidence(prediction_data, behavior_data)
        
        # 5. Counterfactual Analysis
        counterfactuals = self.counterfactual_analyzer.run_what_if_scenarios(prediction_data, behavior_data)
        
        # 6. Structured Risk Reasoning
        reasoning = self.risk_reasoning.generate_reasoning(prediction_data, local_exp, graph_exp)
        
        # 7. Natural Language Explanation
        nl_exp = self.nl_explainer.generate_explanation(reasoning)
        
        # 8. Attention Visualization (Stub)
        attention_maps = self.attention_visualizer.extract_attention(model, graph_data)
        self.attention_visualizer.export_attention(attention_maps, identifier=user_id)
        
        # 9. Reporting and Export
        self.reporter.generate_report(reasoning, nl_exp, identifier=user_id, format='markdown')
        self.exporter.export_data(reasoning, f"reasoning_{user_id}", format='json')
        self.exporter.export_data(counterfactuals, f"counterfactuals_{user_id}", format='json')
        
        logger.info(f"Successfully generated all XAI artifacts for user {user_id}")
        return reasoning, nl_exp
