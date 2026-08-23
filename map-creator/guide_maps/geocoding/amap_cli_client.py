"""Adapter for optional AMap CLI JSON output."""

from __future__ import annotations

import json
import subprocess
from typing import Any

from guide_maps.core.utils import as_text

from .schemas import AMapPOICandidate


class AMapCLIClientError(RuntimeError):
    pass


class AMapCLIClient:
    def __init__(self, command: str = "amap-gui"):
        self.command = command

    def search_text(self, keyword: str, city: str) -> list[AMapPOICandidate]:
        try:
            completed = subprocess.run(
                [self.command, "search", keyword, "--city", city, "--json"],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise AMapCLIClientError(str(exc)) from exc
        if completed.returncode != 0:
            raise AMapCLIClientError(completed.stderr.strip() or "AMap CLI failed")
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise AMapCLIClientError("AMap CLI did not return JSON") from exc
        return [candidate for item in _extract_items(payload) if (candidate := _candidate_from_item(item)) is not None]


def _extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("pois", "data", "results", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _candidate_from_item(item: dict[str, Any]) -> AMapPOICandidate | None:
    location = item.get("location") or item.get("lnglat")
    try:
        if isinstance(location, dict):
            lng = float(location.get("lng") or location.get("lon") or location.get("longitude"))
            lat = float(location.get("lat") or location.get("latitude"))
        elif isinstance(location, str):
            lng_text, lat_text = location.split(",", 1)
            lng, lat = float(lng_text), float(lat_text)
        else:
            lng = float(item.get("lng") or item.get("lon") or item.get("longitude"))
            lat = float(item.get("lat") or item.get("latitude"))
    except (TypeError, ValueError, AttributeError):
        return None
    return AMapPOICandidate(
        poi_id=str(item.get("id") or item.get("poi_id") or ""),
        name=str(item.get("name") or ""),
        address=as_text(item.get("address")),
        province=as_text(item.get("province") or item.get("pname")),
        city=as_text(item.get("city") or item.get("cityname")),
        district=as_text(item.get("district") or item.get("adname")),
        type=as_text(item.get("type")),
        typecode=as_text(item.get("typecode")),
        lng_gcj02=lng,
        lat_gcj02=lat,
        raw=item,
    )

