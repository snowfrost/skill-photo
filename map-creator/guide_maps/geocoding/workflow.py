"""Shared POI resolution workflow helpers."""

from __future__ import annotations

from pathlib import Path

from guide_maps.geocoding.amap_cli_client import AMapCLIClient
from guide_maps.geocoding.amap_client import AMapClient
from guide_maps.geocoding.poi_resolver import POIResolver
from guide_maps.geocoding.schemas import POISet


COORDINATE_POLICY = "AMap GCJ-02 is converted to WGS84 for OSMnx rendering"


def read_place_names(names: list[str] | None = None, names_file: Path | None = None) -> list[str]:
    raw_names: list[str] = []
    if names_file:
        raw_names.extend(
            line.strip()
            for line in names_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    if names:
        raw_names.extend(name.strip() for name in names if name.strip())

    deduped: list[str] = []
    seen: set[str] = set()
    for name in raw_names:
        key = name.casefold()
        if key not in seen:
            deduped.append(name)
            seen.add(key)
    return deduped


def build_resolver(source: str, probe_name: str, city: str) -> tuple[POIResolver, str]:
    if source == "cli":
        return POIResolver(AMapCLIClient(), source="amap-cli"), "amap-cli"
    if source == "api":
        return POIResolver(AMapClient(), source="amap-api"), "amap-api"

    cli_resolver = POIResolver(AMapCLIClient(), source="amap-cli")
    try:
        cli_resolver.resolve_one(probe_name, city=city, limit=1)
        return cli_resolver, "amap-cli"
    except Exception as exc:
        print(f"[!] AMap CLI unavailable: {exc}")
        print("[!] Falling back to AMap Web API.")
    return POIResolver(AMapClient(), source="amap-api"), "amap-api"


def resolve_to_poi_set(
    *,
    city: str,
    names: list[str],
    theme: str = "guide",
    source: str = "auto",
    candidate_limit: int = 5,
) -> POISet:
    resolver, source_name = build_resolver(source, names[0], city)
    print(f"Resolving {len(names)} POIs in {city} via {source_name}...")
    pois = resolver.resolve_many(names, city=city, limit=candidate_limit)
    return POISet(city, theme, source_name, COORDINATE_POLICY, pois)
