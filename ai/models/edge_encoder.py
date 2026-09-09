"""
Edge Feature Encoder
====================

Encodes relationship types and edge interaction attributes (timestamps,
action volume, security severity, bytes transferred) into edge embeddings.
"""

import math
from typing import Any, Dict, List, Optional, Union

__all__ = ["EdgeEncoder"]


class EdgeEncoder:
    """
    Encodes heterogeneous edge attributes and relational types into embeddings.

    Supported edge relation types:
    - LOGIN_TO: user -> host (timestamp, session duration, is_after_hours, auth_status)
    - ACCESS_FILE: user -> file (bytes_read, is_sensitive, access_mode)
    - SEND_EMAIL: user -> email (is_external, attachment_count, recipient_count)
    - CONNECT_USB: user -> usb (bytes_written, vendor_known)
    - AUTHENTICATE: user -> session (method, MFA_passed)
    """

    def __init__(
        self,
        hidden_dim: int = 128,
        edge_types: Optional[List[str]] = None,
    ):
        self.hidden_dim = hidden_dim
        self.edge_types = edge_types or [
            "LOGIN_TO",
            "ACCESS_FILE",
            "SEND_EMAIL",
            "CONNECT_USB",
            "AUTHENTICATE",
            "CONNECT_NETWORK",
        ]

    def _normalize(self, vector: List[float]) -> List[float]:
        """L2 normalization of a feature vector."""
        norm = math.sqrt(sum(x * x for x in vector))
        if norm < 1e-7:
            return vector
        return [x / norm for x in vector]

    def encode_edge(self, edge_type: str, edge_attr: Optional[Union[Dict[str, Any], List[float]]] = None) -> List[float]:
        """
        Encodes edge interaction attributes into an edge embedding vector.
        """
        if edge_attr is None:
            raw_vec = [1.0, 0.0, 0.0, 1.0]
        elif isinstance(edge_attr, dict):
            raw_vec = [float(v) for v in edge_attr.values() if isinstance(v, (int, float))]
            if not raw_vec:
                raw_vec = [1.0, 0.0, 0.0, 1.0]
        else:
            raw_vec = [float(x) for x in edge_attr] if edge_attr else [1.0]

        # Project to hidden_dim
        in_dim = len(raw_vec)
        out: List[float] = [0.0] * self.hidden_dim
        type_hash = sum(ord(c) for c in edge_type) % 100

        for i in range(self.hidden_dim):
            val = 0.0
            for j in range(in_dim):
                weight = math.cos((i + 1) * (j + 1) * 0.15 + type_hash)
                val += raw_vec[j] * weight
            out[i] = val if val > 0 else (math.exp(min(max(val, -10.0), 0.0)) - 1.0)

        return self._normalize(out)

    def encode_dict(self, edge_dict: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[List[float]]]:
        """
        Encodes collections of edges grouped by relation type.
        """
        encoded: Dict[str, List[List[float]]] = {}
        for e_type, edges in edge_dict.items():
            encoded[e_type] = [self.encode_edge(e_type, edge) for edge in edges]
        return encoded
