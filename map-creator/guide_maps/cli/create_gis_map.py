#!/usr/bin/env python3
"""Create a Jufu-Chang-style GIS map from a city and place names."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from guide_maps.geocoding.amap_cli_client import AMapCLIClientError
from guide_maps.geocoding.amap_client import AMapClientError
from guide_maps.geocoding.poi_io import load_poi_set, save_poi_set, slug
from guide_maps.geocoding.schemas import ResolvedPOI
from guide_maps.geocoding.workflow import read_place_names, resolve_to_poi_set
from guide_maps.rendering.osm_context_map_template import ContextMapSpec, ContextSpot, render_context_map


CATEGORY_SEQUENCE = ("coffee", "bar", "vintage", "food")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve city/place names and render an OSM/GIS guide-map draft.")
    parser.add_argument("--city", required=True)
    parser.add_argument("--places", nargs="*")
    parser.add_argument("--places-file", type=Path)
    parser.add_argument("--title")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--output")
    parser.add_argument("--theme", default="guide")
    parser.add_argument("--poi-json", type=Path)
    parser.add_argument("--save-poi-json", type=Path)
    parser.add_argument("--source", choices=("auto", "cli", "api"), default="auto")
    parser.add_argument("--candidate-limit", type=int, default=5)
    parser.add_argument("--road-labels", nargs="*", default=[])
    parser.add_argument("--no-road-labels", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    configure_console()
    args = parse_args()
    places = read_places(args)
    if args.poi_json:
        poi_set = load_poi_set(args.poi_json)
    else:
        if not places:
            raise SystemExit("Provide --places, --places-file, or --poi-json.")
        poi_set = resolve_places(args, places)
        output = save_poi_set(poi_set, args.save_poi_json)
        print(f"[OK] Wrote POI JSON: {output}")

    valid = [poi for poi in poi_set.pois if poi.lng_wgs84 is not None and poi.lat_wgs84 is not None]
    if not valid:
        raise SystemExit("No POIs with valid WGS84 coordinates were found.")
    review = [poi for poi in valid if poi.needs_review]
    if review and args.strict:
        raise SystemExit("POIs need review: " + ", ".join(poi.input_name for poi in review))

    spec = ContextMapSpec(
        title=args.title or f"{poi_set.city}\u901b\u901b\u5730\u56fe",
        subtitle=args.subtitle or "",
        output_name=args.output or f"{slug(poi_set.city)}_{slug(poi_set.theme)}_gis_map.png",
        spots=to_context_spots(valid),
        road_labels=args.road_labels,
        area_labels=[],
        show_road_labels=not args.no_road_labels,
    )
    output = render_context_map(spec)
    print(f"[OK] GIS map ready: {output}")
    if review:
        print("[!] Some POIs were rendered but should be reviewed:")
        for poi in review:
            print(f"    - {poi.input_name}: {poi.status}, confidence={poi.confidence}, best={poi.resolved_name}")
    return 0


def read_places(args: argparse.Namespace) -> list[str]:
    return read_place_names(args.places, args.places_file)


def resolve_places(args: argparse.Namespace, places: list[str]):
    try:
        return resolve_to_poi_set(
            city=args.city,
            names=places,
            theme=args.theme,
            source=args.source,
            candidate_limit=args.candidate_limit,
        )
    except (AMapCLIClientError, AMapClientError) as exc:
        raise SystemExit(str(exc)) from exc


def to_context_spots(pois: list[ResolvedPOI]) -> list[ContextSpot]:
    spots: list[ContextSpot] = []
    for index, poi in enumerate(pois):
        if poi.lat_wgs84 is None or poi.lng_wgs84 is None:
            continue
        spots.append(ContextSpot(poi.input_name, poi.input_name, float(poi.lat_wgs84), float(poi.lng_wgs84), CATEGORY_SEQUENCE[index % len(CATEGORY_SEQUENCE)], display_address(poi)))
    return spots


def display_address(poi: ResolvedPOI) -> str:
    for candidate in poi.candidates:
        address = candidate.get("formatted_address") or candidate.get("address")
        if address:
            return compact_address(str(address))
    return compact_address(poi.address or poi.district or poi.resolved_name or "")


def compact_address(address: str) -> str:
    text = address.strip()
    for prefix in ("\u6c5f\u82cf\u7701\u5357\u4eac\u5e02", "\u5357\u4eac\u5e02"):
        if text.startswith(prefix):
            return text[len(prefix) :]
    return text

def configure_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    raise SystemExit(main())
