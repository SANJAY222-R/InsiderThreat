"""
Graph Node Type Definitions
============================

Defines all node types in the heterogeneous enterprise graph.

Node Types:
    - USER: Enterprise employee (from LDAP)
    - DEVICE: Workstation or removable media
    - EMAIL: Email message
    - FILE: File copied to removable media
    - URL: Website visited
    - PC: Computer/workstation

Phase 0: Enum and schema definitions.
"""

from enum import Enum

__all__ = ["NodeType", "NODE_FEATURE_DIMS"]


class NodeType(str, Enum):
    """Enumeration of all node types in the heterogeneous graph."""

    USER = "user"
    DEVICE = "device"
    EMAIL = "email"
    FILE = "file"
    URL = "url"
    PC = "pc"


# Expected feature dimensionality for each node type
# TODO (Phase 3): Update with actual feature dimensions after feature engineering
NODE_FEATURE_DIMS: dict[NodeType, int] = {
    NodeType.USER: 64,
    NodeType.DEVICE: 16,
    NodeType.EMAIL: 128,
    NodeType.FILE: 64,
    NodeType.URL: 128,
    NodeType.PC: 16,
}
