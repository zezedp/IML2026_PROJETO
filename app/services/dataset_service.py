from typing import Any

from app.repositories.dataset_repository import DatasetRepository


class DatasetService:
    def __init__(self, repository: DatasetRepository) -> None:
        self.repository = repository

    def overview(self) -> dict[str, Any]:
        return self.repository.get_artifact("overview")

    def statistics(self) -> dict[str, Any]:
        return self.repository.get_artifact("statistics")

    def class_distribution(self) -> dict[str, Any]:
        return self.repository.get_artifact("class_distribution")

    def sample(self) -> dict[str, Any]:
        return self.repository.get_artifact("sample")

