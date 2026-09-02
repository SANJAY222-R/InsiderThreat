import torch
import torch.nn as nn
from torch_geometric.nn import MessagePassing
from typing import Dict, Tuple

class HeteroMessagePassing(MessagePassing):
    """
    Message passing layer customized for relation types using attention mechanisms.
    """
    def __init__(self, hidden_dim: int, edge_types: list):
        super().__init__(aggr='add', node_dim=0)
        self.hidden_dim = hidden_dim
        self.edge_types = edge_types
        
        # Linear transformations for messages per edge type
        self.msg_linears = nn.ModuleDict({
            "_".join(e_type): nn.Linear(hidden_dim, hidden_dim) 
            for e_type in edge_types
        })

    def forward(self, x_dict: Dict[str, torch.Tensor], edge_index_dict: Dict[Tuple[str, str, str], torch.Tensor], edge_attr_dict: Dict[Tuple[str, str, str], torch.Tensor] = None) -> Dict[str, torch.Tensor]:
        out_dict = {ntype: torch.zeros_like(x) for ntype, x in x_dict.items()}
        
        for e_type, edge_index in edge_index_dict.items():
            src_type, rel, dst_type = e_type
            rel_name = "_".join(e_type)
            
            if rel_name not in self.msg_linears:
                continue
                
            x_src = x_dict[src_type]
            x_dst = x_dict[dst_type]
            edge_attr = edge_attr_dict.get(e_type) if edge_attr_dict else None
            
            # Message passing for this specific relation
            out = self.propagate(edge_index, x=(x_src, x_dst), edge_attr=edge_attr, rel_name=rel_name)
            out_dict[dst_type] = out_dict[dst_type] + out
            
        return out_dict
        
    def message(self, x_j: torch.Tensor, edge_attr: torch.Tensor, rel_name: str) -> torch.Tensor:
        # Incorporate edge features if available
        if edge_attr is not None:
            msg = x_j + edge_attr
        else:
            msg = x_j
            
        return self.msg_linears[rel_name](msg)
