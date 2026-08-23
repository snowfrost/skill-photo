"""Data structures for POI resolution."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class AMapPOICandidate:
    poi_id: str
    name: str
    address: str
    province: str
    city: str
    district: str
    type: str
    typecode: str
    lng_gcj02: float
    lat_gcj02: float
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResolvedPOI:
    input_name: str
    resolved_name: str | None
    source: str
    poi_id: str | None
    address: str | None
    province: str | None
    city: str | None
    district: str | None
    type: str | None
    typecode: str | None
    lng_gcj02: float | None
    lat_gcj02: float | None
    lng_wgs84: float | None
    lat_wgs84: float | None
    confidence: float
    status: str
    needs_review: bool
    candidates: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class POISet:
    city: str
    theme: str
    source: str
    coordinate_policy: str
    pois: list[ResolvedPOI]

    def to_dict(self) -> dict[str, Any]:
        return {
            "city": self.city,
            "theme": self.theme,
            "source": self.source,
            "coordinate_policy": self.coordinate_policy,
            "pois": [poi.to_dict() for poi in self.pois],
        }

