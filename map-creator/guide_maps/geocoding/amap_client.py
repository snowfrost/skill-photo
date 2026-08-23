"""AMap place-search client."""

from __future__ import annotations

import os
from typing import Any

import requests

from guide_maps.core.config import load_amap_config
from guide_maps.core.utils import as_text, clean_placeholder_key

from .coordinate_transform import parse_lnglat
from .schemas import AMapPOICandidate


class AMapClientError(RuntimeError):
    pass


class AMapClient:
    endpoint = "https://restapi.amap.com/v3/place/text"

    def __init__(self, api_key: str | None = None, timeout: int = 12):
        config = load_amap_config()
        self.api_key = api_key or os.environ.get("AMAP_KEY") or clean_placeholder_key(config.get("api_key"))
        self.timeout = int(timeout or config.get("timeout") or 12)
        if not self.api_key:
            raise AMapClientError("AMap API key is not set. Fill config.local.json or set AMAP_KEY.")

    def search_text(self, keyword: str, city: str, offset: int = 20) -> list[AMapPOICandidate]:
        params = {
            "key": self.api_key,
            "keywords": keyword,
            "city": city,
            "citylimit": "true",
            "offset": offset,
            "page": 1,
            "extensions": "base",
            "output": "json",
        }
        response = requests.get(self.endpoint, params=params, timeout=self.timeout)
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        if payload.get("status") != "1":
            raise AMapClientError(f"AMap search failed for {keyword!r}: {payload.get('info') or 'unknown AMap error'}")

        candidates: list[AMapPOICandidate] = []
        for item in payload.get("pois", []):
            location = item.get("location")
            if not location:
                continue
            try:
                lng, lat = parse_lnglat(location)
            except (TypeError, ValueError):
                continue
            candidates.append(
                AMapPOICandidate(
                    poi_id=str(item.get("id") or ""),
                    name=str(item.get("name") or ""),
                    address=as_text(item.get("address")),
                    province=as_text(item.get("pname")),
                    city=as_text(item.get("cityname")),
                    district=as_text(item.get("adname")),
                    type=as_text(item.get("type")),
                    typecode=as_text(item.get("typecode")),
                    lng_gcj02=lng,
                    lat_gcj02=lat,
                    raw=item,
                )
            )
        return candidates


