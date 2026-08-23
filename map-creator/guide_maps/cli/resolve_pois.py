#!/usr/bin/env python3
"""Resolve place names with AMap and export reviewable POI JSON."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from guide_maps.geocoding.workflow import read_place_names, resolve_to_poi_set
from guide_maps.geocoding.poi_io import save_poi_set


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve POI names and export JSON.")
    parser.add_argument("--city", required=True)
    parser.add_argument("--theme", default="guide")
    parser.add_argument("--names", nargs="*")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--candidate-limit", type=int, default=5)
    parser.add_argument("--source", choices=("auto", "cli", "api"), default="auto")
    return parser.parse_args()


def main() -> int:
    configure_console()
    args = parse_args()
    names = read_place_names(args.names, args.input)
    if not names:
        raise SystemExit("No POI names provided.")
    poi_set = resolve_to_poi_set(
        city=args.city,
        names=names,
        theme=args.theme,
        source=args.source,
        candidate_limit=args.candidate_limit,
    )
    output = save_poi_set(poi_set, args.output)
    print(f"[OK] Wrote {output}")
    return 0


def configure_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    raise SystemExit(main())
