"""
Neural network model architectures and encoders for Insider Threat Detection.
"""

from ai.models.base_model import BaseModel
from ai.models.node_encoder import NodeEncoder
from ai.models.edge_encoder import EdgeEncoder
from ai.models.temporal_encoder import TemporalEncoder

__all__ = [
    "BaseModel",
    "NodeEncoder",
    "EdgeEncoder",
    "TemporalEncoder",
]

try:
    from ai.models.thgnn import THGNN
    __all__.append("THGNN")
except ImportError:
    pass
