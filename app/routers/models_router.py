from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_models_service
from app.schemas.models_schemas import (
    ConfusionMatricesResponse,
    CrossValidationResponse,
    FeatureImportanceResponse,
    MetricsResponse,
    RocCurvesResponse,
)
from app.services.models_service import ModelsService

router = APIRouter(prefix="/models", tags=["models"])


def _service_unavailable(exc: RuntimeError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics(service: ModelsService = Depends(get_models_service)) -> dict:
    try:
        return service.metrics()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


@router.get("/roc-curves", response_model=RocCurvesResponse)
def get_roc_curves(service: ModelsService = Depends(get_models_service)) -> dict:
    try:
        return service.roc_curves()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


@router.get("/cross-validation", response_model=CrossValidationResponse)
def get_cross_validation(service: ModelsService = Depends(get_models_service)) -> dict:
    try:
        return service.cross_validation()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


@router.get("/confusion-matrices", response_model=ConfusionMatricesResponse)
def get_confusion_matrices(service: ModelsService = Depends(get_models_service)) -> dict:
    try:
        return service.confusion_matrices()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


@router.get("/feature-importance", response_model=FeatureImportanceResponse)
def get_feature_importance(service: ModelsService = Depends(get_models_service)) -> dict:
    try:
        return service.feature_importance()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc

