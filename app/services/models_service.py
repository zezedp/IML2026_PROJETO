from typing import Any

from app.repositories.metrics_repository import MetricsRepository


class ModelsService:
    def __init__(self, repository: MetricsRepository) -> None:
        self.repository = repository

    def metrics(self) -> dict[str, Any]:
        return self.repository.get_artifact("metrics")

    def roc_curves(self) -> dict[str, Any]:
        return self._sample_curve_artifact("roc_curves")

    def pr_curves(self) -> dict[str, Any]:
        return self._sample_curve_artifact("pr_curves")

    def cross_validation(self) -> dict[str, Any]:
        return self.repository.get_artifact("cross_validation")

    def confusion_matrices(self) -> dict[str, Any]:
        return self.repository.get_artifact("confusion_matrices")

    def feature_importance(self) -> dict[str, Any]:
        return self.repository.get_artifact("feature_importance")

    def _sample_curve_artifact(self, name: str, max_points: int = 900) -> dict[str, Any]:
        artifact = self.repository.get_artifact(name)
        sampled_artifact = {**artifact, "models": {}}

        for model_id, model in artifact.get("models", {}).items():
            points = model.get("points", [])
            sampled_artifact["models"][model_id] = {
                **model,
                "points": self._sample_points(points, max_points),
            }

        return sampled_artifact

    @staticmethod
    def _sample_points(points: list[dict[str, float]], max_points: int) -> list[dict[str, float]]:
        if len(points) <= max_points:
            return points

        last_index = len(points) - 1
        indexes = sorted({round(index * last_index / (max_points - 1)) for index in range(max_points)})
        return [points[index] for index in indexes]

