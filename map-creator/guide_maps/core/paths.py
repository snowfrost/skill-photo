"""Shared paths for map-creator."""

from __future__ import annotations

import os
from pathlib import Path


CORE_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = CORE_DIR.parent
PROJECT_ROOT = PACKAGE_DIR.parent


def _env_path(name: str, legacy_name: str, default: Path) -> Path:
    return Path(os.environ.get(name) or os.environ.get(legacy_name) or default)


THEMES_DIR = _env_path("MAP_CREATOR_THEMES_DIR", "OPEN_GUIDE_MAPS_THEMES_DIR", PACKAGE_DIR / "themes")
FONTS_DIR = _env_path("MAP_CREATOR_FONTS_DIR", "OPEN_GUIDE_MAPS_FONTS_DIR", PACKAGE_DIR / "fonts")
CACHE_DIR = _env_path("MAP_CREATOR_CACHE_DIR", "OPEN_GUIDE_MAPS_CACHE_DIR", PROJECT_ROOT / "cache")
OUTPUTS_DIR = _env_path("MAP_CREATOR_OUTPUTS_DIR", "OPEN_GUIDE_MAPS_OUTPUTS_DIR", PROJECT_ROOT / "outputs")
POSTERS_DIR = _env_path("MAP_CREATOR_POSTERS_DIR", "OPEN_GUIDE_MAPS_POSTERS_DIR", OUTPUTS_DIR / "posters")
STYLIZED_DIR = _env_path("MAP_CREATOR_STYLIZED_DIR", "OPEN_GUIDE_MAPS_STYLIZED_DIR", OUTPUTS_DIR / "stylized")
POI_SETS_DIR = _env_path("MAP_CREATOR_POI_SETS_DIR", "OPEN_GUIDE_MAPS_POI_SETS_DIR", OUTPUTS_DIR / "poi_sets")


def ensure_runtime_dirs() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    POI_SETS_DIR.mkdir(parents=True, exist_ok=True)
    POSTERS_DIR.mkdir(parents=True, exist_ok=True)
    STYLIZED_DIR.mkdir(parents=True, exist_ok=True)

