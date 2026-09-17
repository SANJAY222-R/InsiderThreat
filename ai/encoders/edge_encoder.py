import torch
import torch.nn as nn
from typing import Dict, List, Tuple

class EdgeFeatureEncoder(nn.Module):
    """
    Encodes edge features such as timestamp, weight, duration, and interaction count.
    Generates learnable edge embeddings.
    """
    def __init__(self, hidden_dim: int, edge_types: List[Tuple[str, str, str]]) -> None:
        super().__init__()
        self.hidden_dim = hidden_dim
        self.edge_types = edge_types
        
        self.encoders = nn.ModuleDict()
        
        for e_type in edge_types:
            # e_type is typically a tuple (src, rel, dst)
            rel_name = "_".join(e_type)
            
            # We assume a fixed set of edge features: [timestamp, weight, duration, count]
            in_dim = 4
            
            self.encoders[rel_name] = nn.Sequential(
                nn.Linear(in_dim, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.ELU(),
                nn.Dropout(0.1)
            )

    def forward(self, edge_attr_dict: Dict[Tuple[str, str, str], torch.Tensor]) -> Dict[Tuple[str, str, str], torch.Tensor]:
        out_dict = {}
        for e_type, attr in edge_attr_dict.items():
            rel_name = "_".join(e_type)
            if rel_name in self.encoders:
                # Handle missing attributes by zero-filling
                attr_clean = torch.nan_to_num(attr, nan=0.0)
                # Pad to 4 features if necessary
                if attr_clean.size(-1) < 4:
                    pad = torch.zeros(*attr_clean.shape[:-1], 4 - attr_clean.size(-1), device=attr.device)
                    attr_clean = torch.cat([attr_clean, pad], dim=-1)
                
                out_dict[e_type] = self.encoders[rel_name](attr_clean)
        return out_dict
