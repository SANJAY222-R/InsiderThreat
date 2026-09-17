from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query

from backend.app.auth.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.schemas.graph import (
    GraphQueryRequest,
    GraphQueryResponse,
    SubgraphRequest,
    AddEventRequest,
    SampleEntity,
)
from backend.app.services.graph_service import get_graph_service

router = APIRouter()


@router.get("/samples", response_model=List[SampleEntity])
def get_sample_entities(_: User = Depends(get_current_user)) -> List[Dict[str, Any]]:
    """Return a curated list of active entity IDs for easy graph navigation."""
    service = get_graph_service()
    return service.get_sample_entities()


@router.post("/query", response_model=GraphQueryResponse)
def query_graph(req: GraphQueryRequest, _: User = Depends(get_current_user)) -> GraphQueryResponse:
    """Extract neighborhood graph around a specific node up to N hops."""
    service = get_graph_service()
    res = service.query_neighborhood(
        node_id=req.node_id,
        node_type=req.node_type,
        depth=req.depth,
        max_nodes=req.max_nodes,
    )
    return GraphQueryResponse(**res)


@router.post("/subgraph", response_model=GraphQueryResponse)
def extract_subgraph(req: SubgraphRequest, _: User = Depends(get_current_user)) -> GraphQueryResponse:
    """Extract temporal interaction subgraph."""
    service = get_graph_service()
    res = service.extract_subgraph(
        center_node=req.center_node,
        time_start=req.time_start,
        time_end=req.time_end,
        hop_count=req.hop_count,
    )
    return GraphQueryResponse(**res)


@router.post("/event")
def add_graph_event(req: AddEventRequest, _: User = Depends(get_current_user)) -> Dict[str, str]:
    """Dynamically inject an event into the live heterogeneous graph."""
    service = get_graph_service()
    service.add_custom_event(
        user_id=req.user_id,
        event_type=req.event_type,
        target_entity=req.target_entity,
        target_type=req.target_type,
        timestamp=req.timestamp,
        metadata=req.metadata,
    )
    return {"status": "success", "message": f"Event {req.event_type} added successfully."}
