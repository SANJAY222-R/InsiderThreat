"""
Graph Pydantic Schemas
======================
Request/response models for graph query endpoints.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel

__all__ = ["GraphQueryRequest", "GraphQueryResponse", "SubgraphRequest", "AddEventRequest", "SampleEntity"]


class GraphQueryRequest(BaseModel):
    """Schema for graph neighborhood query."""
    node_id: str
    node_type: str = "user"  # user, device, email, file, url, usb
    depth: int = 2
    max_nodes: int = 80


class GraphQueryResponse(BaseModel):
    """Schema for graph query results."""
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    metadata: Dict[str, Any] = {}


class SubgraphRequest(BaseModel):
    """Schema for temporal subgraph extraction."""
    center_node: str
    time_start: Optional[str] = None
    time_end: Optional[str] = None
    hop_count: int = 2


class AddEventRequest(BaseModel):
    """Schema for dynamic event injection."""
    user_id: str
    event_type: str
    target_entity: str
    target_type: str = "device"
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SampleEntity(BaseModel):
    """Schema for sample entity lookup."""
    id: str
    label: str
    type: str
    role: Optional[str] = None
    department: Optional[str] = None
