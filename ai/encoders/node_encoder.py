import torch
import torch.nn as nn
from typing import Dict, List, Optional

class HeteroNodeEncoder(nn.Module):
    """
    Encodes features for heterogeneous nodes independently.
    Projects diverse feature spaces to a fixed-dimensional embedding.
    Supports missing attributes and normalization.
    """
    def __init__(self, hidden_dim: int, node_types: List[str], feature_dims: Optional[Dict[str, int]] = None):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_types = node_types
        
        # If feature dims aren't provided, default to a fallback embedding
        self.feature_dims = feature_dims or {}
        
        self.encoders = nn.ModuleDict()
        
        for n_type in node_types:
            in_dim = self.feature_dims.get(n_type, -1)
            if in_dim > 0:
                # If we know the feature dimension, use a linear projection
                self.encoders[n_type] = nn.Sequential(
                    nn.Linear(in_dim, hidden_dim),
                    nn.LayerNorm(hidden_dim),
                    nn.ELU(),
                    nn.Dropout(0.1)
                )
            else:
                # Fallback: simple learnable embedding if no features or unknown dim
                # Using a linear layer that expects to project from a dummy dimension or we just handle it in forward
                # Let's assume we create an embedding layer for a max number of nodes if no features
                # But for PyG, typically node features are provided. We'll use a lazy linear layer.
                self.encoders[n_type] = nn.Sequential(
                    nn.LazyLinear(hidden_dim),
                    nn.LayerNorm(hidden_dim),
                    nn.ELU(),
                    nn.Dropout(0.1)
                )
                
    def forward(self, x_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        out_dict = {}
        for n_type, x in x_dict.items():
            if n_type in self.encoders:
                # Handle missing attributes by zero-filling NaNs
                x_clean = torch.nan_to_num(x, nan=0.0)
                out_dict[n_type] = self.encoders[n_type](x_clean)
        return out_dict
