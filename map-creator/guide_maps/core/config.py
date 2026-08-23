"""Local configuration loading for API keys and runtime options."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from guide_maps.core.paths import PROJECT_ROOT, STYLIZED_DIR


DEFAULT_CONFIG = {
    "amap": {
        "api_key": "",
        "timeout": 12,
    },
    "gpt_image": {
        "api_key": "",
        "model": "gpt-image-2",
        "endpoint": "https://api.openai.com/v1/images/edits",
        "template": "prompts/map_style_templates/01_手绘风城市导览地图.md",
        "output_dir": "outputs/stylized",
        "output_format": "png",
        "size": "1536x1024",
        "timeout": 120,
    },
}


def load_app_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load root config and merge it with defaults.

    `config.local.json` is intended for real local keys and is ignored by git.
    `config.example.json` documents the shape for open source users.
    """
    path = config_path or PROJECT_ROOT / "config.local.json"
    config = _deep_copy(DEFAULT_CONFIG)
    if path.exists():
        config = _merge(config, json.loads(path.read_text(encoding="utf-8-sig")))
    return config


def load_amap_config(config_path: Path | None = None) -> dict[str, Any]:
    config = load_app_config(config_path)
    return dict(config.get("amap") or {})


def load_gpt_image_config(config_path: Path | None = None) -> dict[str, Any]:
    config = load_app_config(config_path)
    gpt = dict(config.get("gpt_image") or {})
    gpt["template"] = str(_resolve_project_path(gpt.get("template") or DEFAULT_CONFIG["gpt_image"]["template"]))
    gpt["output_dir"] = str(_resolve_project_path(gpt.get("output_dir") or STYLIZED_DIR))
    return gpt


def _resolve_project_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _merge(dict(base[key]), value)
        else:
            base[key] = value
    return base


def _deep_copy(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value))
