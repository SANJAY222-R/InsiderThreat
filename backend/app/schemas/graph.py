"""
Graph Pydantic Schemas
======================

Request/response models for graph query endpoints.
Phase 0: Schema stubs.
"""

from typing import Any
from pydantic import BaseModel

__all__ = ["GraphQueryRequest", "GraphQueryResponse", "SubgraphRequest"]


class GraphQueryRequest(BaseModel):
    """Schema for graph neighborhood query."""
    node_id: str
    node_type: str  # user, device, email, file, url
    depth: int = 2
    max_nodes: int = 100


class GraphQueryResponse(BaseModel):
    """Schema for graph query results."""
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    metadata: dict[str, Any] = {}


class SubgraphRequest(BaseModel):
    """Schema for temporal subgraph extraction."""
    center_node: str
    time_start: str
    time_end: str
    hop_count: int = 2
