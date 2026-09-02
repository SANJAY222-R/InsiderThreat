import torch
import torch.nn as nn

class TransformerEncoderLayerCustom(nn.Module):
    """
    Transformer Encoder layer for contextual node embeddings.
    Implements Multi-head Self Attention, FFN, LayerNorm, Residuals, Dropout.
    """
    def __init__(self, hidden_dim: int, num_heads: int, dropout: float = 0.2):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.norm1 = nn.LayerNorm(hidden_dim)
        
        self.ffn = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim * 4, hidden_dim)
        )
        self.norm2 = nn.LayerNorm(hidden_dim)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Self attention
        attn_out, _ = self.self_attn(x, x, x)
        x = self.norm1(x + self.dropout(attn_out))
        
        # FFN
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        
        return x

class HeteroTransformerEncoder(nn.Module):
    """
    Applies Transformer Encoder independently to each node type's embeddings 
    to capture cross-node context if framed sequentially (e.g. within a session).
    """
    def __init__(self, hidden_dim: int, num_heads: int, num_layers: int, dropout: float = 0.2):
        super().__init__()
        self.layers = nn.ModuleList([
            TransformerEncoderLayerCustom(hidden_dim, num_heads, dropout)
            for _ in range(num_layers)
        ])
        
    def forward(self, x_dict: dict) -> dict:
        out_dict = {}
        for ntype, x in x_dict.items():
            # Treat node set as sequence length dimension. Shape: (batch_size=1, seq_len=N, hidden_dim)
            x_seq = x.unsqueeze(0)
            for layer in self.layers:
                x_seq = layer(x_seq)
            out_dict[ntype] = x_seq.squeeze(0)
        return out_dict
