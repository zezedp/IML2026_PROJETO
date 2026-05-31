from __future__ import annotations

import math
from typing import Any

import pandas as pd

from app.core.config import FEATURES, MODEL_METADATA
from app.repositories.models_repository import ModelsRepository


class ModelManager:
    def __init__(self, models_repository: ModelsRepository) -> None:
        self.models_repository = models_repository
        self.models: dict[str, Any] = {}

    def load_models(self) -> None:
        self.models_repository.load()
        self.models = self.models_repository.models

    def predict_all(self, features: dict[str, float | int]) -> dict[str, dict[str, Any]]:
        if not self.models:
            raise RuntimeError("ML models are not loaded.")

        row = pd.DataFrame([[features[name] for name in FEATURES]], columns=FEATURES, dtype=float)
        results: dict[str, dict[str, Any]] = {}

        for key, model in self.models.items():
            probability = self._fraud_probability(model, row)
            short_name, full_name = MODEL_METADATA[key]
            is_fraud = probability >= 0.5
            results[key] = {
                "name": short_name,
                "full_name": full_name,
                "classification": "FRAUDE" if is_fraud else "LEGITIMA",
                "is_fraud": is_fraud,
                "fraud_probability": round(probability, 6),
            }

        return results

    @staticmethod
    def _fraud_probability(model: Any, row: pd.DataFrame) -> float:
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(row)[0]
            classes = list(getattr(model, "classes_", [0, 1]))
            class_index = classes.index(1) if 1 in classes else len(probabilities) - 1
            return float(probabilities[class_index])

        if hasattr(model, "decision_function"):
            score = float(model.decision_function(row)[0])
            return 1.0 / (1.0 + math.exp(-score))

        return float(model.predict(row)[0])

    @property
    def is_loaded(self) -> bool:
        return set(MODEL_METADATA).issubset(self.models.keys())
