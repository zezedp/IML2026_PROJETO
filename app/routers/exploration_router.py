from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import get_exploration_service
from app.schemas.exploration_schemas import (
    BinaryFeaturesResponse,
    BoxplotResponse,
    CorrelationResponse,
    HistogramResponse,
)
from app.services.exploration_service import ExplorationService

ContinuousFeature = Literal[
    "distance_from_home",
    "distance_from_last_transaction",
    "ratio_to_median_purchase_price",
]

router = APIRouter(prefix="/exploration", tags=["exploration"])


def _service_unavailable(exc: RuntimeError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))


@router.get("/histogram", response_model=HistogramResponse)
def get_histogram(
    feature: ContinuousFeature = Query(...),
    service: ExplorationService = Depends(get_exploration_service),
) -> dict:
    try:
        return service.histogram(feature)
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


@router.get("/boxplot", response_model=BoxplotResponse)
def get_boxplot(
    feature: ContinuousFeature = Query(...),
    service: ExplorationService = Depends(get_exploration_service),
) -> dict:
    try:
        return service.boxplot(feature)
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


// TODO: Verificar se faz sentido esse gráfico
@router.get("/binary-features", response_model=BinaryFeaturesResponse)
def get_binary_features(
    service: ExplorationService = Depends(get_exploration_service),
) -> dict:
    try:
        return service.binary_features()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


@router.get("/correlation", response_model=CorrelationResponse)
def get_correlation(service: ExplorationService = Depends(get_exploration_service)) -> dict:
    try:
        return service.correlation()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc

