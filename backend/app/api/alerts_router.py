from fastapi import APIRouter, Depends
from backend.app.auth.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/alerts", tags=["Alert APIs"])

@router.get("/")
def list_alerts(status: str = "OPEN", current_user=Depends(get_current_user)):
    return [
        {
            "alert_id": str(uuid.uuid4()),
            "user_id": "U1234",
            "severity": "HIGH",
            "status": status
        }
    ]

@router.put("/{alert_id}/resolve")
def resolve_alert(alert_id: str, current_user=Depends(get_current_user)):
    return {"alert_id": alert_id, "status": "RESOLVED", "resolved_by": current_user.username}
