from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.auth.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.alert import Alert
from backend.app.models.prediction import Prediction
from backend.app.models.report import Report
from backend.app.models.user import User
from backend.app.schemas.prediction import PredictionResponse
from backend.app.schemas.report import (
    ReportDetailResponse,
    ReportRequest,
    ReportResponse,
    ReportSummaryStats,
)
from backend.app.services.report_builder import (
    build_report_data,
    export_report_file,
)

router = APIRouter()


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Provides general platform dashboard & report statistics."""
    total_predictions = db.query(func.count(Prediction.id)).scalar() or 0
    total_alerts = db.query(func.count(Alert.id)).scalar() or 0
    total_reports = db.query(func.count(Report.id)).scalar() or 0

    alerts_by_status = dict(
        db.query(Alert.status, func.count(Alert.id)).group_by(Alert.status).all()
    )
    alerts_by_severity = dict(
        db.query(Alert.severity, func.count(Alert.id)).group_by(Alert.severity).all()
    )
    reports_by_type = dict(
        db.query(Report.report_type, func.count(Report.id)).group_by(Report.report_type).all()
    )
    reports_by_format = dict(
        db.query(Report.format, func.count(Report.id)).group_by(Report.format).all()
    )

    recent_predictions = (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .limit(5)
        .all()
    )

    last_report = db.query(Report).order_by(Report.created_at.desc()).first()

    return {
        "total_predictions": total_predictions,
        "total_alerts": total_alerts,
        "total_reports": total_reports,
        "alerts_by_status": alerts_by_status,
        "alerts_by_severity": alerts_by_severity,
        "reports_by_type": reports_by_type,
        "reports_by_format": reports_by_format,
        "last_generated_at": last_report.created_at.isoformat() if last_report and last_report.created_at else None,
        "recent_predictions": [PredictionResponse.model_validate(p) for p in recent_predictions],
    }


@router.get("/", response_model=List[ReportResponse])
def list_reports(
    skip: int = 0,
    limit: int = 50,
    report_type: Optional[str] = Query(default=None),
    format: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> List[Report]:
    """Lists all previously compiled and saved reports."""
    query = db.query(Report)
    if report_type:
        query = query.filter(Report.report_type == report_type)
    if format:
        query = query.filter(Report.format == format)
    return query.order_by(Report.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_report(
    req: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Report:
    """Generates a comprehensive insider threat report from live database intelligence."""
    title, summary_metrics, detailed_data = build_report_data(
        db=db,
        report_type=req.report_type,
        date_from=req.date_from,
        date_to=req.date_to,
        title=req.title,
        created_by=current_user.username or current_user.email,
    )

    report = Report(
        title=title,
        report_type=req.report_type,
        format=req.format or "pdf",
        status="complete",
        date_from=req.date_from,
        date_to=req.date_to,
        summary_metrics=summary_metrics,
        data=detailed_data,
        created_by=current_user.username or current_user.email or "SOC Analyst",
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    # Set calculated download URL and estimated file size
    report.download_url = f"/api/v1/reports/{report.id}/download"
    try:
        content_bytes, _, _ = export_report_file(report)
        report.file_size = len(content_bytes)
    except Exception:
        report.file_size = 1024

    db.commit()
    db.refresh(report)
    return report


@router.get("/{report_id}", response_model=ReportDetailResponse)
def get_report_details(
    report_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Report:
    """Retrieves full report details and data payload for on-screen inspection/preview."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report #{report_id} not found",
        )
    return report


@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    format: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Response:
    """Streams the generated PDF, CSV, or JSON file to the client."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report #{report_id} not found",
        )

    content, media_type, filename = export_report_file(report, format_override=format)

    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.post("/instant-download")
def instant_download(
    req: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    """Instantly generates and streams a report on-the-fly without saving to database."""
    title, summary_metrics, detailed_data = build_report_data(
        db=db,
        report_type=req.report_type,
        date_from=req.date_from,
        date_to=req.date_to,
        title=req.title,
        created_by=current_user.username or current_user.email,
    )

    temp_report = Report(
        id=999,
        title=title,
        report_type=req.report_type,
        format=req.format or "pdf",
        status="complete",
        date_from=req.date_from,
        date_to=req.date_to,
        summary_metrics=summary_metrics,
        data=detailed_data,
        created_by=current_user.username or "SOC Analyst",
        created_at=datetime.now(timezone.utc),
    )

    content, media_type, filename = export_report_file(temp_report)

    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Deletes a report from the historical record."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report #{report_id} not found",
        )
    db.delete(report)
    db.commit()
    return {"success": True, "message": f"Report #{report_id} deleted successfully"}
