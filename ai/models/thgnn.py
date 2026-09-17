import torch
import torch.nn as nn
from typing import Dict, List, Tuple, Any, Optional, cast
from torch_geometric.data import HeteroData

from ai.encoders.node_encoder import HeteroNodeEncoder
from ai.encoders.edge_encoder import EdgeFeatureEncoder
from ai.layers.temporal_encoding import TimeEncoder
from ai.layers.graph_attention import TemporalHeteroGAT
from ai.layers.transformer_encoder import HeteroTransformerEncoder
from ai.layers.graph_pooling import GraphPooling


class PredictionHead(nn.Module):
    def __init__(self, hidden_dim: int) -> None:
        super().__init__()
        self.node_predictor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ELU(),
            nn.Linear(hidden_dim // 2, 1)
        )
        self.graph_predictor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ELU(),
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, x_dict: Dict[str, torch.Tensor], graph_emb: torch.Tensor) -> Dict[str, Any]:
        node_scores = {ntype: self.node_predictor(x) for ntype, x in x_dict.items()}
        graph_score = self.graph_predictor(graph_emb) if graph_emb.numel() > 0 else None
        
        # Calculate probabilities
        node_probs = {ntype: torch.sigmoid(score) for ntype, score in node_scores.items()}
        graph_prob = torch.sigmoid(graph_score) if graph_score is not None else None
        
        return {
            'node_scores': node_scores,
            'node_probs': node_probs,
            'graph_score': graph_score,
            'graph_prob': graph_prob
        }


class THGNN(nn.Module):
    """
    Temporal Heterogeneous Graph Neural Network (THGNN).
    Assembles encoders, layers, pooling, and prediction head.
    """
    def __init__(
        self,
        node_types: List[str],
        edge_types: List[Tuple[str, str, str]],
        hidden_dim: int = 128,
        num_layers: int = 3,
        num_heads: int = 8,
        dropout: float = 0.2,
        pooling_type: str = 'attention',
        time_encoding: str = 'sinusoidal'
    ) -> None:
        super().__init__()
        
        self.node_encoder = HeteroNodeEncoder(hidden_dim, node_types)
        self.edge_encoder = EdgeFeatureEncoder(hidden_dim, edge_types)
        
        self.time_encoder = TimeEncoder(hidden_dim, method=time_encoding)
        
        self.gat_layers = nn.ModuleList([
            TemporalHeteroGAT(hidden_dim, num_heads, edge_types, dropout)
            for _ in range(num_layers)
        ])
        
        self.transformer = HeteroTransformerEncoder(hidden_dim, num_heads, num_layers=1, dropout=dropout)
        
        self.pool = GraphPooling(hidden_dim, pooling_type=pooling_type)
        self.head = PredictionHead(hidden_dim)

    def forward(self, data: HeteroData) -> Dict[str, Any]:
        # 1. Encode Nodes
        x_dict = self.node_encoder(data.x_dict)
        
        # 2. Encode Edges
        edge_attr_dict = {}
        for e_type in data.edge_types:
            if hasattr(data[e_type], 'edge_attr') and data[e_type].edge_attr is not None:
                edge_attr_dict[e_type] = data[e_type].edge_attr
            else:
                num_edges = data[e_type].edge_index.size(1)
                edge_attr_dict[e_type] = torch.zeros((num_edges, 4), device=data[e_type].edge_index.device)
                
        edge_attr_dict = self.edge_encoder(edge_attr_dict)
        
        # 3. Add Temporal Embeddings to edges if time attribute exists
        for e_type in data.edge_types:
            if hasattr(data[e_type], 'time') and data[e_type].time is not None:
                t_emb = self.time_encoder(data[e_type].time)
                if e_type in edge_attr_dict:
                    edge_attr_dict[e_type] = edge_attr_dict[e_type] + t_emb
                else:
                    edge_attr_dict[e_type] = t_emb

        # 4. Message Passing / Attention
        for gat_layer in self.gat_layers:
            x_dict = gat_layer(x_dict, data.edge_index_dict, edge_attr_dict)
            
        # 5. Contextual refinement
        x_dict = self.transformer(x_dict)
        
        # 6. Graph Pooling
        batch_dict = {}
        for n_type in data.node_types:
            if hasattr(data[n_type], 'batch') and data[n_type].batch is not None:
                batch_dict[n_type] = data[n_type].batch
        graph_emb = self.pool(x_dict, batch_dict if batch_dict else None)
        
        # 7. Prediction
        predictions: Dict[str, Any] = cast(Dict[str, Any], self.head(x_dict, graph_emb))
        
        # Attach embeddings to predictions for export
        predictions['node_embeddings'] = x_dict
        predictions['graph_embedding'] = graph_emb
        
        return predictions
