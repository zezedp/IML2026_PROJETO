from typing import Any

from pydantic import BaseModel, ConfigDict


class FlexibleResponse(BaseModel):
    model_config = ConfigDict(extra="allow")


class OverviewResponse(FlexibleResponse):
    total_transactions: int
    legitimate_transactions: int
    fraud_transactions: int
    fraud_rate: float


class StatisticsResponse(BaseModel):
    statistics: list[dict[str, Any]]


class ClassDistributionResponse(FlexibleResponse):
    pass


class SampleResponse(BaseModel):
    sample: list[dict[str, Any]]

