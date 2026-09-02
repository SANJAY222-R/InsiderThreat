from fastapi import APIRouter, Depends
from backend.app.auth.dependencies import get_current_user

router = APIRouter(prefix="/reports", tags=["Report APIs"])

@router.get("/generate/{report_type}")
def generate_report(report_type: str, format: str = "pdf", current_user=Depends(get_current_user)):
    """
    Mock endpoint for report generation (Threat, Incident, Executive).
    """
    return {
        "report_type": report_type,
        "format": format,
        "download_url": f"/static/reports/mock_report.{format}",
        "status": "GENERATED"
    }
