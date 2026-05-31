from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_prediction_service
from app.schemas.prediction_schemas import (
    PredictionRequest,
    PredictionResponse,
    ScenariosResponse,
)
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/prediction", tags=["prediction"])


@router.get("/scenarios", response_model=ScenariosResponse)
def get_scenarios(service: PredictionService = Depends(get_prediction_service)) -> dict:
    return service.scenarios()


@router.post("/predict", response_model=PredictionResponse)
def predict(
    payload: PredictionRequest,
    service: PredictionService = Depends(get_prediction_service),
) -> dict:
    try:
        return service.predict(payload.model_dump())
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

