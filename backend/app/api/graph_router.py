from fastapi import APIRouter, Depends
from backend.app.auth.dependencies import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/graph", tags=["Graph APIs"])

@router.get("/neighborhood/{node_id}")
def get_neighborhood(node_id: str, hops: int = 1, current_user=Depends(get_current_user)):
    """
    Mock endpoint to fetch graph neighborhood for a node.
    """
    return {
        "node_id": node_id,
        "neighborhood": [
            {"src": node_id, "rel": "LOGIN_TO", "dst": "Host_123"},
            {"src": node_id, "rel": "ACCESS", "dst": "File_456"}
        ]
    }

@router.get("/timeline/{user_id}")
def get_timeline(user_id: str, current_user=Depends(get_current_user)):
    """
    Mock endpoint to fetch user timeline.
    """
    return {
        "user_id": user_id,
        "timeline": [
            {"timestamp": "2026-09-02T10:00:00Z", "event": "Login", "risk": 10.0}
        ]
    }
