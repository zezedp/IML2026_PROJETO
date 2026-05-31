from typing import Any

from app.core.config import CONTINUOUS_FEATURES
from app.repositories.dataset_repository import DatasetRepository


class ExplorationService:
    def __init__(self, repository: DatasetRepository) -> None:
        self.repository = repository

    def histogram(self, feature: str) -> dict[str, Any]:
        self._validate_continuous_feature(feature)
        return self.repository.get_artifact("histograms")[feature]

    def boxplot(self, feature: str) -> dict[str, Any]:
        self._validate_continuous_feature(feature)
        return self.repository.get_artifact("boxplots")[feature]

    def binary_features(self) -> dict[str, Any]:
        return self.repository.get_artifact("binary_features")

    def correlation(self) -> dict[str, Any]:
        return self.repository.get_artifact("correlation")

    @staticmethod
    def _validate_continuous_feature(feature: str) -> None:
        if feature not in CONTINUOUS_FEATURES:
            allowed = ", ".join(CONTINUOUS_FEATURES)
            raise ValueError(f"Unsupported feature '{feature}'. Expected one of: {allowed}.")

