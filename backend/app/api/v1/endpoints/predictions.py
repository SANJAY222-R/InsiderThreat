from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ai.inference.predictor import Predictor
from backend.app.auth.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.prediction import Prediction
from backend.app.models.user import User
from backend.app.schemas.prediction import PredictionRequest, PredictionResponse

router = APIRouter()
predictor = Predictor(model_version="1.0.0")


@router.post("/predict", response_model=PredictionResponse, status_code=201)
@router.post("/", response_model=PredictionResponse, status_code=201)
def create_prediction(req: PredictionRequest, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    result = predictor.predict(employee_id=req.employee_id, context=req.context)

    prediction = Prediction(
        employee_id=result["employee_id"],
        risk_score=result["risk_score"],
        threat_level=result["threat_level"],
        confidence=result["confidence"],
        model_version=result["model_version"],
        explanation=result.get("explanation", {}),
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("/", response_model=list[PredictionResponse])
def list_predictions(
    skip: int = 0,
    limit: int = 50,
    employee_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Prediction)
    if employee_id:
        query = query.filter(Prediction.employee_id == employee_id)
    return query.order_by(Prediction.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction
