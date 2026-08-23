"""Small pickle cache for OSMnx fetches."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from guide_maps.core.paths import CACHE_DIR


class DiskCache:
    def __init__(self, directory: Path = CACHE_DIR):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def path_for(self, key: str) -> Path:
        safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in key)
        return self.directory / f"{safe}.pkl"

    def get(self, key: str) -> Any | None:
        path = self.path_for(key)
        if not path.exists():
            return None
        try:
            with path.open("rb") as handle:
                return pickle.load(handle)
        except Exception:
            return None

    def set(self, key: str, value: Any) -> None:
        path = self.path_for(key)
        with path.open("wb") as handle:
            pickle.dump(value, handle)


def get_cache() -> DiskCache:
    return DiskCache()
