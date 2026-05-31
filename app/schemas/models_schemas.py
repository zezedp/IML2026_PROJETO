from typing import Any

from pydantic import BaseModel, ConfigDict


class FlexibleResponse(BaseModel):
    model_config = ConfigDict(extra="allow")


class MetricsResponse(FlexibleResponse):
    models: list[dict[str, Any]]
    best_model: str


class RocCurvesResponse(FlexibleResponse):
    models: dict[str, Any]


class CrossValidationResponse(FlexibleResponse):
    folds: list[int]
    models: dict[str, Any]


class ConfusionMatricesResponse(FlexibleResponse):
    models: dict[str, Any]
    test_size: int


class FeatureImportanceResponse(FlexibleResponse):
    model: str
    features: list[dict[str, Any]]

