import pickle
from pathlib import Path
from typing import Any

from app.core.config import MODEL_METADATA, MODELS_ARTIFACTS_DIR


class ModelsRepository:
    def __init__(self, models_dir: Path = MODELS_ARTIFACTS_DIR) -> None:
        self.models_dir = models_dir
        self.models: dict[str, Any] = {}

    def load(self) -> None:
        self.models = {}
        if not self.models_dir.exists():
            return
        for model_key in MODEL_METADATA:
            path = self.models_dir / f"{model_key}_model.pkl"
            if path.exists():
                with path.open("rb") as file:
                    self.models[model_key] = pickle.load(file)

    def get_models(self) -> dict[str, Any]:
        if not self.models:
            raise RuntimeError("ML models are not loaded.")
        return self.models

    @property
    def is_loaded(self) -> bool:
        return set(MODEL_METADATA).issubset(self.models.keys())

