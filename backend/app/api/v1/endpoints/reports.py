from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.auth.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.alert import Alert
from backend.app.models.prediction import Prediction
from backend.app.models.user import User
from backend.app.schemas.prediction import PredictionResponse
from backend.app.schemas.report import ReportRequest, ReportResponse

router = APIRouter()


@router.get("/summary")
def get_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> Dict[str, Any]:
    total_predictions = db.query(func.count(Prediction.id)).scalar() or 0
    total_alerts = db.query(func.count(Alert.id)).scalar() or 0

    alerts_by_status = dict(
        db.query(Alert.status, func.count(Alert.id)).group_by(Alert.status).all()
    )
    alerts_by_severity = dict(
        db.query(Alert.severity, func.count(Alert.id)).group_by(Alert.severity).all()
    )

    recent_predictions = (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "total_predictions": total_predictions,
        "total_alerts": total_alerts,
        "alerts_by_status": alerts_by_status,
        "alerts_by_severity": alerts_by_severity,
        "recent_predictions": [PredictionResponse.model_validate(p) for p in recent_predictions],
    }


@router.post("/generate", response_model=ReportResponse, status_code=202)
def generate_report(req: ReportRequest, _: User = Depends(get_current_user)) -> ReportResponse:
    return ReportResponse(
        report_id=1,
        report_type=req.report_type,
        status="pending",
    )
