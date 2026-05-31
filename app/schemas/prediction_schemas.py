from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    distance_from_home: float = Field(..., ge=0)
    distance_from_last_transaction: float = Field(..., ge=0)
    ratio_to_median_purchase_price: float = Field(..., ge=0)
    repeat_retailer: int = Field(..., ge=0, le=1)
    used_chip: int = Field(..., ge=0, le=1)
    used_pin_number: int = Field(..., ge=0, le=1)
    online_order: int = Field(..., ge=0, le=1)


class ModelPrediction(BaseModel):
    name: str
    full_name: str
    classification: str
    is_fraud: bool
    fraud_probability: float


class AggregatePrediction(BaseModel):
    average_probability: float
    fraud_votes: int
    total_models: int
    consensus: str
    consensus_message: str
    risk_level: str


class PredictionResponse(BaseModel):
    models: dict[str, ModelPrediction]
    aggregate: AggregatePrediction
    input_features: PredictionRequest


class Scenario(BaseModel):
    id: str
    label: str
    style: str
    features: PredictionRequest


class ScenariosResponse(BaseModel):
    scenarios: list[Scenario]

