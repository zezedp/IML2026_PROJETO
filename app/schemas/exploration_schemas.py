from typing import Any

from pydantic import BaseModel, ConfigDict


class FlexibleResponse(BaseModel):
    model_config = ConfigDict(extra="allow")


class HistogramResponse(FlexibleResponse):
    feature: str
    labels: list[str]
    legitimate: list[float]
    fraud: list[float]


class BoxplotResponse(FlexibleResponse):
    feature: str
    legitimate: dict[str, float]
    fraud: dict[str, float]


class BinaryFeaturesResponse(FlexibleResponse):
    features: list[str]
    display_names: list[str]
    legitimate: list[float]
    fraud: list[float]


class CorrelationResponse(BaseModel):
    labels: list[str]
    matrix: list[list[float]]

