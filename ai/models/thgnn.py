"""
Temporal Heterogeneous Graph Neural Network (THGNN)
===================================================

Core model architecture for insider threat detection.
Combines heterogeneous graph attention with temporal encoding
to learn user behavior patterns over time.

Phase 0: Architecture stub only.

Architecture Overview:
    1. Node Encoder: Encodes heterogeneous node features
    2. Edge Encoder: Encodes relationship features
    3. Temporal Encoder: Captures temporal dynamics
    4. HGAT Layers: Heterogeneous graph attention
    5. Readout: User-level threat score prediction

TODO (Phase 4): Implement with PyTorch Geometric HeteroData.
"""

__all__ = ["THGNN"]


class THGNN:
    """
    Temporal Heterogeneous Graph Neural Network.

    This model operates on heterogeneous temporal graphs where:
    - Nodes: Users, Devices, Emails, Files, URLs
    - Edges: logon, device_use, email_send, file_copy, http_visit
    - Temporal: Time-stamped edges with temporal attention

    Args:
        node_types: List of node type names.
        edge_types: List of (src, relation, dst) edge type tuples.
        hidden_dim: Hidden layer dimensionality.
        num_heads: Number of attention heads.
        num_layers: Number of HGAT layers.
        temporal_dim: Temporal encoding dimensionality.
        dropout: Dropout rate.

    TODO (Phase 4): Full implementation.
    """
    pass
