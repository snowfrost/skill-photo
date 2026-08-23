#!/usr/bin/env python3
"""Run a map-creator draft script, then optionally style the result."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from guide_maps.core.paths import POSTERS_DIR, ensure_runtime_dirs
from guide_maps.styling.gpt_image import GPTImageError, style_poster


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a map-creator pipeline.")
    parser.add_argument("--map-script", required=True, type=Path)
    parser.add_argument("--vars", type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--skip-style", action="store_true")
    parser.add_argument("--dry-run-style", action="store_true")
    return parser.parse_args()


def main() -> int:
    configure_console()
    args = parse_args()
    ensure_runtime_dirs()
    completed = subprocess.run([sys.executable, str(args.map_script)], check=False)
    if completed.returncode != 0:
        return completed.returncode
    poster = args.input.resolve() if args.input else _latest_poster()
    if poster is None:
        print("[ERROR] No poster image found in outputs/posters.")
        return 1
    print(f"[OK] Poster draft: {poster}")
    if args.skip_style:
        return 0
    try:
        result = style_poster(poster, variables_path=args.vars, template_path=args.template, config_path=args.config, output_dir=args.output_dir, dry_run=args.dry_run_style)
    except (GPTImageError, OSError, ValueError) as exc:
        print(f"[ERROR] {exc}")
        return 1
    print(f"[OK] {result.message}")
    return 0


def _latest_poster() -> Path | None:
    files = [path for path in POSTERS_DIR.glob("*.png") if path.is_file()]
    return max(files, key=lambda path: path.stat().st_mtime).resolve() if files else None


def configure_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    raise SystemExit(main())
