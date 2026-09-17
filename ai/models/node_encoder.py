"""
Node Feature Encoder
====================

Encodes heterogeneous node features (user, host, file, email, usb, department)
into a unified, shared embedding dimension.
Supports feature projection, missing attribute imputation, and normalization.
"""

import math
from typing import Any, Dict, List, Optional, Union

__all__ = ["NodeEncoder"]


class NodeEncoder:
    """
    Encodes heterogeneous entity features into dense vector embeddings.

    Supports multiple node types:
    - user: behavioral, psychometric, clearance features
    - host/device: operating system, security level, hardware type
    - file: sensitivity, classification, extension, size
    - email: domain, external flag, recipient count
    - usb: vendor ID, storage capacity, encryption status
    """

    def __init__(
        self,
        hidden_dim: int = 128,
        node_types: Optional[List[str]] = None,
        feature_dims: Optional[Dict[str, int]] = None,
    ) -> None:
        self.hidden_dim = hidden_dim
        self.node_types = node_types or ["user", "host", "device", "file", "email", "usb", "session", "department"]
        self.feature_dims = feature_dims or {
            "user": 16,
            "host": 8,
            "device": 8,
            "file": 10,
            "email": 8,
            "usb": 6,
            "session": 8,
            "department": 4,
        }

    def _normalize(self, vector: List[float]) -> List[float]:
        """L2 normalization of a feature vector."""
        norm = math.sqrt(sum(x * x for x in vector))
        if norm < 1e-7:
            return vector
        return [x / norm for x in vector]

    def _project_vector(self, vector: List[float], target_dim: int, seed_type: str = "") -> List[float]:
        """
        Projects a vector of arbitrary dimension to target_dim using deterministic linear weights.
        """
        in_dim = len(vector)
        out: List[float] = [0.0] * target_dim

        # Deterministic linear projection based on sinusoidal basis
        type_hash = sum(ord(c) for c in seed_type) % 100
        for i in range(target_dim):
            val = 0.0
            for j in range(in_dim):
                weight = math.sin((i + 1) * (j + 1) * 0.1 + type_hash)
                val += vector[j] * weight
            # ELU non-linearity: f(x) = x if x > 0 else exp(x) - 1
            activated = val if val > 0 else (math.exp(min(max(val, -10.0), 0.0)) - 1.0)
            out[i] = activated

        return self._normalize(out)

    def encode_node(self, node_type: str, features: Union[Dict[str, Any], List[float]]) -> List[float]:
        """
        Encodes a single node's features into the shared hidden dimension.
        """
        if isinstance(features, dict):
            # Extract numerical values
            raw_vec = [float(v) for v in features.values() if isinstance(v, (int, float))]
            if not raw_vec:
                raw_vec = [1.0]
        else:
            raw_vec = [float(x) for x in features] if features else [1.0]

        # Handle missing or zero-length input
        expected_dim = self.feature_dims.get(node_type, 8)
        if len(raw_vec) < expected_dim:
            raw_vec = raw_vec + [0.0] * (expected_dim - len(raw_vec))

        return self._project_vector(raw_vec, self.hidden_dim, seed_type=node_type)

    def encode_dict(self, node_dict: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[List[float]]]:
        """
        Encodes collections of heterogeneous nodes grouped by type.
        """
        encoded_output: Dict[str, List[List[float]]] = {}
        for n_type, nodes in node_dict.items():
            encoded_output[n_type] = [self.encode_node(n_type, node) for node in nodes]
        return encoded_output
