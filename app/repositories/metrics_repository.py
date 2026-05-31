import json
from pathlib import Path
from typing import Any

from app.core.config import METRICS_ARTIFACTS_DIR


class MetricsRepository:
    def __init__(self, artifacts_dir: Path = METRICS_ARTIFACTS_DIR) -> None:
        self.artifacts_dir = artifacts_dir
        self.artifacts: dict[str, Any] = {}

    def load(self) -> None:
        self.artifacts = {}
        if not self.artifacts_dir.exists():
            return
        for path in self.artifacts_dir.glob("*.json"):
            with path.open("r", encoding="utf-8") as file:
                self.artifacts[path.stem] = json.load(file)

    def get_artifact(self, name: str) -> Any:
        try:
            return self.artifacts[name]
        except KeyError as exc:
            raise RuntimeError(f"Metrics artifact '{name}' is not loaded.") from exc

    @property
    def is_loaded(self) -> bool:
        return bool(self.artifacts)

