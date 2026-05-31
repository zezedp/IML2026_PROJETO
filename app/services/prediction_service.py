from typing import Any

from app.ml.model_manager import ModelManager


SCENARIOS = [
    {
        "id": "legitimate",
        "label": "Transacao Claramente Legitima",
        "style": "green",
        "features": {
            "distance_from_home": 8,
            "distance_from_last_transaction": 2,
            "ratio_to_median_purchase_price": 0.9,
            "repeat_retailer": 1,
            "used_chip": 1,
            "used_pin_number": 1,
            "online_order": 0,
        },
    },
    {
        "id": "fraud",
        "label": "Fraude Obvia",
        "style": "red",
        "features": {
            "distance_from_home": 120,
            "distance_from_last_transaction": 60,
            "ratio_to_median_purchase_price": 7.5,
            "repeat_retailer": 0,
            "used_chip": 0,
            "used_pin_number": 0,
            "online_order": 1,
        },
    },
    {
        "id": "ambiguous",
        "label": "Caso Ambiguo",
        "style": "yellow",
        "features": {
            "distance_from_home": 35,
            "distance_from_last_transaction": 8,
            "ratio_to_median_purchase_price": 2.7,
            "repeat_retailer": 1,
            "used_chip": 0,
            "used_pin_number": 0,
            "online_order": 1,
        },
    },
]


class PredictionService:
    def __init__(self, model_manager: ModelManager) -> None:
        self.model_manager = model_manager

    def scenarios(self) -> dict[str, Any]:
        return {"scenarios": SCENARIOS}

    def predict(self, features: dict[str, float | int]) -> dict[str, Any]:
        models = self.model_manager.predict_all(features)
        probabilities = [item["fraud_probability"] for item in models.values()]
        fraud_votes = sum(1 for item in models.values() if item["is_fraud"])
        average_probability = sum(probabilities) / len(probabilities)

        aggregate = {
            "average_probability": round(average_probability, 6),
            "fraud_votes": fraud_votes,
            "total_models": len(models),
            "consensus": self._consensus_label(fraud_votes, len(models)),
            "consensus_message": self._consensus_message(fraud_votes, len(models)),
            "risk_level": self._risk_level(fraud_votes, len(models)),
        }

        return {
            "models": models,
            "aggregate": aggregate,
            "input_features": features,
        }

    @staticmethod
    def _risk_level(fraud_votes: int, total_models: int) -> str:
        if fraud_votes == 0:
            return "low"
        if fraud_votes == total_models:
            return "high"
        return "medium"

    @staticmethod
    def _consensus_label(fraud_votes: int, total_models: int) -> str:
        if fraud_votes == 0:
            return "Legitima"
        if fraud_votes == total_models:
            return "Fraude"
        return "Divergente"

    @staticmethod
    def _consensus_message(fraud_votes: int, total_models: int) -> str:
        if fraud_votes == 0:
            return "Todos os modelos classificam esta transacao como legitima. Risco baixo."
        if fraud_votes == total_models:
            return "Todos os modelos classificam esta transacao como fraude. Risco alto."
        return (
            f"{fraud_votes} de {total_models} modelos classificam como fraude. "
            "A decisao merece revisao."
        )

