#!/usr/bin/env python3
"""Style a map-creator draft with GPT Image."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from guide_maps.styling.gpt_image import GPTImageError, style_poster


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Style a map-creator draft with GPT Image.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--vars", type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    configure_console()
    args = parse_args()
    try:
        result = style_poster(args.input, variables_path=args.vars, template_path=args.template, config_path=args.config, output_dir=args.output_dir, dry_run=args.dry_run)
    except (GPTImageError, OSError, ValueError) as exc:
        print(f"[ERROR] {exc}")
        return 1
    print(f"[{result.status}] {result.message}")
    return 0


def configure_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    raise SystemExit(main())
