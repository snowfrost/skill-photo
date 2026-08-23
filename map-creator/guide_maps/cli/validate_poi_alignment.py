#!/usr/bin/env python3
"""Validate POI coordinate alignment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from guide_maps.geocoding.poi_alignment import compute_frame_bounds, validate_alignment
from guide_maps.core.paths import PROJECT_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate POI coordinate alignment.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    configure_console()
    args = parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    pois = payload.get("pois", [])
    frame = compute_frame_bounds(pois)
    results, _ = validate_alignment(pois, city=str(payload.get("city") or ""), frame=frame, fetch_roads=False)
    output = args.output or PROJECT_ROOT / "outputs" / "debug" / f"{args.input.stem}_alignment.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "input": str(args.input),
                "results": [
                    {
                        "input_name": result.input_name,
                        "status": result.status,
                        "in_frame": result.in_frame,
                        "city_bounds_ok": result.city_bounds_ok,
                        "issues": [issue.__dict__ for issue in result.issues],
                    }
                    for result in results
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[OK] Wrote {output}")
    return 0


def configure_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    raise SystemExit(main())
