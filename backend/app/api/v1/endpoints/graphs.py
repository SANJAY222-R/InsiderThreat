from fastapi import APIRouter, Depends

from backend.app.auth.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.schemas.graph import GraphQueryRequest, GraphQueryResponse, SubgraphRequest

router = APIRouter()


@router.post("/query", response_model=GraphQueryResponse)
def query_graph(req: GraphQueryRequest, _: User = Depends(get_current_user)):
    nodes = [
        {"id": req.node_id, "type": req.node_type, "label": req.node_id},
        {"id": f"{req.node_id}_peer_1", "type": "user", "label": "Peer 1"},
        {"id": f"{req.node_id}_device_1", "type": "device", "label": "Workstation-A"},
        {"id": f"{req.node_id}_file_1", "type": "file", "label": "report.pdf"},
    ]
    edges = [
        {"source": req.node_id, "target": f"{req.node_id}_peer_1", "type": "communicates_with"},
        {"source": req.node_id, "target": f"{req.node_id}_device_1", "type": "uses"},
        {"source": req.node_id, "target": f"{req.node_id}_file_1", "type": "accessed"},
    ]
    return GraphQueryResponse(nodes=nodes, edges=edges, metadata={"depth": req.depth, "total_nodes": len(nodes)})


@router.post("/subgraph", response_model=GraphQueryResponse)
def extract_subgraph(req: SubgraphRequest, _: User = Depends(get_current_user)):
    nodes = [
        {"id": req.center_node, "type": "user", "label": req.center_node},
        {"id": f"{req.center_node}_email_1", "type": "email", "label": "email-thread-1"},
    ]
    edges = [
        {"source": req.center_node, "target": f"{req.center_node}_email_1", "type": "sent"},
    ]
    return GraphQueryResponse(
        nodes=nodes,
        edges=edges,
        metadata={"center": req.center_node, "time_start": req.time_start, "time_end": req.time_end},
    )
