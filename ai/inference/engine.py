import os
import json
import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.data import HeteroData
from typing import Dict, Union, List

class InferenceEngine:
    """
    Inference Engine for THGNN.
    Supports Single User, Batch, and Graph Predictions.
    Exports predictions to JSON or CSV.
    """
    def __init__(self, model: nn.Module, device: torch.device):
        self.model = model.to(device)
        self.model.eval()
        self.device = device
        
    @torch.no_grad()
    def predict_batch(self, data: HeteroData) -> dict:
        data = data.to(self.device)
        # Assuming autocast wasn't explicitly requested for inference but it's good practice
        with torch.cuda.amp.autocast(enabled=True):
            predictions = self.model(data)
        
        # Convert tensors to CPU numpy arrays for easier handling downstream
        res = {
            'node_probs': {k: v.cpu().numpy() for k, v in predictions['node_probs'].items()},
            'node_embeddings': {k: v.cpu().numpy() for k, v in predictions['node_embeddings'].items()}
        }
        
        if predictions['graph_prob'] is not None:
            res['graph_prob'] = predictions['graph_prob'].cpu().numpy()
            res['graph_embedding'] = predictions['graph_embedding'].cpu().numpy()
            
        return res
        
    def predict_single_user(self, user_id: int, user_data: HeteroData) -> float:
        # A specific wrapper that isolates a single user prediction
        # Assumes user_data represents the ego-graph for that user
        res = self.predict_batch(user_data)
        # Depending on how nodes are ordered, retrieve the target user
        # For an ego graph, user_id might map to index 0
        probs = res['node_probs'].get('user')
        if probs is not None and len(probs) > 0:
            return float(probs[0])
        return 0.0

    def export_predictions(self, predictions: dict, output_path: str, format: str = 'json'):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # We need to flatten or restructure predictions for export
        export_data = {}
        for ntype, probs in predictions['node_probs'].items():
            export_data[ntype] = probs.flatten().tolist()
            
        if 'graph_prob' in predictions:
            export_data['graph'] = predictions['graph_prob'].flatten().tolist()
            
        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=4)
        elif format == 'csv':
            # Flatten into a dataframe
            records = []
            for ntype, probs in predictions['node_probs'].items():
                for idx, p in enumerate(probs.flatten().tolist()):
                    records.append({'entity_type': ntype, 'id': idx, 'risk_score': p})
            df = pd.DataFrame(records)
            df.to_csv(output_path, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")
