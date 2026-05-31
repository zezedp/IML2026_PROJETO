import json
from pathlib import Path
from typing import Any

import pandas as pd

from app.core.config import DATASET_ARTIFACTS_DIR, DATASET_PATH


class DatasetRepository:
    def __init__(
        self,
        dataset_path: Path = DATASET_PATH,
        artifacts_dir: Path = DATASET_ARTIFACTS_DIR,
    ) -> None:
        self.dataset_path = dataset_path
        self.artifacts_dir = artifacts_dir
        self.df: pd.DataFrame | None = None
        self.artifacts: dict[str, Any] = {}

    def load(self) -> None:
        if self.dataset_path.exists():
            self.df = pd.read_csv(self.dataset_path)
        self.load_artifacts()

    def load_artifacts(self) -> None:
        self.artifacts = {}
        if not self.artifacts_dir.exists():
            return
        for path in self.artifacts_dir.glob("*.json"):
            with path.open("r", encoding="utf-8") as file:
                self.artifacts[path.stem] = json.load(file)

    def get_dataframe(self) -> pd.DataFrame:
        if self.df is None:
            raise RuntimeError("Dataset is not loaded.")
        return self.df

    def get_artifact(self, name: str) -> Any:
        try:
            return self.artifacts[name]
        except KeyError as exc:
            raise RuntimeError(f"Dataset artifact '{name}' is not loaded.") from exc

    @property
    def is_loaded(self) -> bool:
        return self.df is not None

    @property
    def artifacts_loaded(self) -> bool:
        return bool(self.artifacts)

