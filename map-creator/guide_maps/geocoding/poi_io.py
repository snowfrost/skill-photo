"""POI JSON persistence helpers."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from guide_maps.core.paths import POI_SETS_DIR
from guide_maps.geocoding.schemas import POISet, ResolvedPOI


def load_poi_set(path: Path) -> POISet:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return POISet(
        city=str(payload.get("city") or "city"),
        theme=str(payload.get("theme") or path.stem),
        source=str(payload.get("source") or "json"),
        coordinate_policy=str(payload.get("coordinate_policy") or "WGS84 coordinates used for rendering"),
        pois=[ResolvedPOI(**item) for item in payload.get("pois", [])],
    )


def save_poi_set(poi_set: POISet, output: Path | None = None) -> Path:
    destination = output or POI_SETS_DIR / f"{slug(poi_set.city)}_{slug(poi_set.theme)}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps({**poi_set.to_dict(), "generated_at": datetime.now().isoformat(timespec="seconds")}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return destination


def slug(value: str) -> str:
    text = re.sub(r"\s+", "_", value.strip().lower())
    text = re.sub(r"[^\w\u4e00-\u9fff-]+", "", text, flags=re.UNICODE)
    return text.strip("_") or "map"
