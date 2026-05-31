from typing import Any

from app.repositories.metrics_repository import MetricsRepository


class ModelsService:
    def __init__(self, repository: MetricsRepository) -> None:
        self.repository = repository

    def metrics(self) -> dict[str, Any]:
        return self.repository.get_artifact("metrics")

    def roc_curves(self) -> dict[str, Any]:
        return self.repository.get_artifact("roc_curves")

    def cross_validation(self) -> dict[str, Any]:
        return self.repository.get_artifact("cross_validation")

    def confusion_matrices(self) -> dict[str, Any]:
        return self.repository.get_artifact("confusion_matrices")

    def feature_importance(self) -> dict[str, Any]:
        return self.repository.get_artifact("feature_importance")

