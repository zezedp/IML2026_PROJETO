from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_dataset_service
from app.schemas.dataset_schemas import (
    ClassDistributionResponse,
    OverviewResponse,
    SampleResponse,
    StatisticsResponse,
)
from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/dataset", tags=["dataset"])

# TODO: Verificar se vamos exibir o dataset somado com os dados sintéticos ou não

def _service_unavailable(exc: RuntimeError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))


@router.get("/overview", response_model=OverviewResponse)
def get_overview(service: DatasetService = Depends(get_dataset_service)) -> dict:
    try:
        return service.overview()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics(service: DatasetService = Depends(get_dataset_service)) -> dict:
    try:
        return service.statistics()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


@router.get("/class-distribution", response_model=ClassDistributionResponse)
def get_class_distribution(service: DatasetService = Depends(get_dataset_service)) -> dict:
    try:
        return service.class_distribution()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc


@router.get("/sample", response_model=SampleResponse)
def get_sample(service: DatasetService = Depends(get_dataset_service)) -> dict:
    try:
        return service.sample()
    except RuntimeError as exc:
        raise _service_unavailable(exc) from exc

