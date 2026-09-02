import os
from typing import Dict, Any, List

class AttentionVisualizer:
    """
    Visualizes Node, Edge, Relation, Temporal, and Transformer Attention.
    Exports to JSON/CSV (heatmaps require UI integration).
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def extract_attention(self, model: Any, data: Any) -> Dict[str, Any]:
        """
        Extracts attention weights from the THGNN model layers.
        """
        # In PyG, attention weights can be returned by passing return_attention_weights=True
        # Simulated extraction for MVP
        attention_maps = {
            'node_attention': {"User_1": 0.9, "Host_4001": 0.8},
            'edge_attention': {"LOGIN_TO": 0.7, "INSERT_USB": 0.95},
            'temporal_attention': {"03:00_AM": 0.88, "09:00_AM": 0.1}
        }
        return attention_maps
        
    def export_attention(self, attention_maps: Dict[str, Any], identifier: str, format: str = 'json'):
        """
        Exports the attention maps to the desired format.
        """
        import json
        if format == 'json':
            path = os.path.join(self.output_dir, f"attention_{identifier}.json")
            with open(path, 'w') as f:
                json.dump(attention_maps, f, indent=4)
