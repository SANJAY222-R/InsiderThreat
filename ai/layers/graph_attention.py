import torch
import torch.nn as nn
from torch_geometric.nn import HeteroConv, GATv2Conv

class TemporalHeteroGAT(nn.Module):
    """
    Multi-head graph attention module for heterogeneous temporal graphs.
    Supports Node/Edge/Relation attention with residual connections and dropout.
    """
    def __init__(self, hidden_dim: int, num_heads: int, edge_types: list, dropout: float = 0.2):
        super().__init__()
        self.hidden_dim = hidden_dim
        
        convs = {}
        for e_type in edge_types:
            convs[e_type] = GATv2Conv(
                in_channels=hidden_dim,
                out_channels=hidden_dim // num_heads,
                heads=num_heads,
                dropout=dropout,
                edge_dim=hidden_dim, # We assume edge attributes are encoded to hidden_dim
                add_self_loops=False
            )
            
        self.hetero_conv = HeteroConv(convs, aggr='sum')
        self.layer_norm = nn.LayerNorm(hidden_dim)
        self.activation = nn.ELU()
        
    def forward(self, x_dict, edge_index_dict, edge_attr_dict=None):
        out_dict = self.hetero_conv(x_dict, edge_index_dict, edge_attr_dict=edge_attr_dict)
        
        # Residual connections and LayerNorm
        res_dict = {}
        for ntype, out in out_dict.items():
            if ntype in x_dict:
                # pad or truncate if node degrees were 0
                if out.size(0) == x_dict[ntype].size(0):
                    out = out + x_dict[ntype]
                res_dict[ntype] = self.activation(self.layer_norm(out))
            else:
                res_dict[ntype] = self.activation(self.layer_norm(out))
                
        # Persist un-updated nodes
        for ntype, x in x_dict.items():
            if ntype not in res_dict:
                res_dict[ntype] = x
                
        return res_dict
