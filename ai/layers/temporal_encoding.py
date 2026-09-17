import torch
import torch.nn as nn
import math

class TimeEncoder(nn.Module):
    """
    Temporal encoding module.
    Supports Sinusoidal Time Encoding and Learnable Time Embeddings.
    """
    def __init__(self, out_dim: int, method: str = 'sinusoidal') -> None:
        super().__init__()
        self.out_dim = out_dim
        self.method = method
        
        if self.method == 'learnable':
            self.linear = nn.Linear(1, out_dim)

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        """
        t: shape (N,) or (N, 1), continuous or relative time
        """
        if t.dim() == 1:
            t = t.unsqueeze(1)
            
        if self.method == 'sinusoidal':
            # Sinusoidal positional encoding
            pe = torch.zeros(t.size(0), self.out_dim, device=t.device)
            position = t
            div_term = torch.exp(torch.arange(0, self.out_dim, 2, dtype=torch.float, device=t.device) * (-math.log(10000.0) / self.out_dim))
            pe[:, 0::2] = torch.sin(position * div_term)
            if self.out_dim % 2 != 0:
                pe[:, 1::2] = torch.cos(position * div_term[:-1])
            else:
                pe[:, 1::2] = torch.cos(position * div_term)
            return pe
        elif self.method == 'learnable':
            return self.linear(t)
        else:
            raise ValueError(f"Unknown time encoding method: {self.method}")
