import torch
import torch.nn as nn
from torch_geometric.nn import global_mean_pool, global_max_pool, GlobalAttention

class GraphPooling(nn.Module):
    """
    Graph pooling module supporting Global Mean, Global Max, and Attention Pooling.
    Generates graph-level or session-level embeddings.
    """
    def __init__(self, hidden_dim: int, pooling_type: str = 'attention'):
        super().__init__()
        self.pooling_type = pooling_type
        
        if pooling_type == 'attention':
            gate_nn = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim),
                nn.Tanh(),
                nn.Linear(hidden_dim, 1)
            )
            self.pool = GlobalAttention(gate_nn=gate_nn)
            
    def forward(self, x_dict: dict, batch_dict: dict | None = None) -> torch.Tensor:
        """
        Pools across all nodes in the heterogeneous graph to create a graph embedding.
        """
        # Concatenate all node features
        x_all = []
        batch_all = []
        
        for ntype, x in x_dict.items():
            x_all.append(x)
            if batch_dict is not None and ntype in batch_dict:
                batch_all.append(batch_dict[ntype])
            else:
                # If no batch info, assume all nodes belong to graph 0
                batch_all.append(torch.zeros(x.size(0), dtype=torch.long, device=x.device))
                
        if not x_all:
            return torch.empty(0)
            
        x_cat = torch.cat(x_all, dim=0)
        batch_cat = torch.cat(batch_all, dim=0)
        
        if self.pooling_type == 'mean':
            return global_mean_pool(x_cat, batch_cat)
        elif self.pooling_type == 'max':
            return global_max_pool(x_cat, batch_cat)
        elif self.pooling_type == 'attention':
            return self.pool(x_cat, batch_cat)
        else:
            raise ValueError(f"Unsupported pooling type: {self.pooling_type}")
