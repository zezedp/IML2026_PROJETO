from functools import lru_cache

from app.ml.model_manager import ModelManager
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.metrics_repository import MetricsRepository
from app.repositories.models_repository import ModelsRepository
from app.services.dataset_service import DatasetService
from app.services.exploration_service import ExplorationService
from app.services.models_service import ModelsService
from app.services.prediction_service import PredictionService


class AppContainer:
    def __init__(self) -> None:
        self.dataset_repository = DatasetRepository()
        self.models_repository = ModelsRepository()
        self.metrics_repository = MetricsRepository()

        self.model_manager = ModelManager(self.models_repository)

        self.dataset_service = DatasetService(self.dataset_repository)
        self.exploration_service = ExplorationService(self.dataset_repository)
        self.prediction_service = PredictionService(self.model_manager)
        self.models_service = ModelsService(self.metrics_repository)

    def load(self) -> None:
        self.dataset_repository.load()
        self.metrics_repository.load()
        self.model_manager.load_models()

    def health(self) -> dict[str, bool | str]:
        healthy = (
            self.dataset_repository.is_loaded
            and self.dataset_repository.artifacts_loaded
            and self.metrics_repository.is_loaded
            and self.model_manager.is_loaded
        )
        return {
            "status": "healthy" if healthy else "degraded",
            "models_loaded": self.model_manager.is_loaded,
            "dataset_loaded": self.dataset_repository.is_loaded,
            "artifacts_loaded": self.dataset_repository.artifacts_loaded
            and self.metrics_repository.is_loaded,
        }


@lru_cache
def get_container() -> AppContainer:
    return AppContainer()


def get_dataset_service() -> DatasetService:
    return get_container().dataset_service


def get_exploration_service() -> ExplorationService:
    return get_container().exploration_service


def get_prediction_service() -> PredictionService:
    return get_container().prediction_service


def get_models_service() -> ModelsService:
    return get_container().models_service

