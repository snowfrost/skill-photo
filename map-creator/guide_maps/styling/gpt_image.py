"""GPT Image styling helpers."""

from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from guide_maps.core.config import load_gpt_image_config
from guide_maps.core.paths import PROJECT_ROOT, STYLIZED_DIR
from guide_maps.core.utils import clean_placeholder_key


class GPTImageError(RuntimeError):
    pass


@dataclass
class StyleResult:
    status: str
    message: str
    input_path: Path
    output_path: Path | None = None
    prompt_path: Path | None = None
    sidecar_path: Path | None = None


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    if config_path:
        raw = json.loads(config_path.read_text(encoding="utf-8-sig"))
        if "gpt_image" in raw:
            return dict(raw["gpt_image"])
        return raw
    return load_gpt_image_config()


def find_api_key(config: dict[str, Any] | None = None) -> str | None:
    config = config or {}
    return clean_placeholder_key(os.environ.get("OPENAI_API_KEY")) or clean_placeholder_key(os.environ.get("GPT_IMAGE_API_KEY")) or clean_placeholder_key(config.get("api_key"))


def render_prompt(template_path: Path, variables: dict[str, Any]) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, value in variables.items():
        if isinstance(value, list):
            rendered = "\n".join(str(item) for item in value)
        elif isinstance(value, dict):
            rendered = json.dumps(value, ensure_ascii=False, indent=2)
        else:
            rendered = str(value)
        text = text.replace("{" + key + "}", rendered)
    return text


def default_output_path(input_path: Path, template_path: Path, output_dir: Path, output_format: str) -> Path:
    return output_dir / f"{input_path.stem}__{template_path.stem}.{output_format}"


def style_poster(
    input_path: Path,
    variables_path: Path | None = None,
    template_path: Path | None = None,
    config_path: Path | None = None,
    output_dir: Path | None = None,
    variables: dict[str, Any] | None = None,
    dry_run: bool = False,
) -> StyleResult:
    input_path = input_path.resolve()
    config = load_config(config_path)
    template = template_path or Path(config.get("template") or PROJECT_ROOT / "prompts" / "map_style_templates" / "01_手绘风城市导览地图.md")
    out_dir = output_dir or Path(config.get("output_dir") or STYLIZED_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_format = str(config.get("output_format") or "png")
    api_key = find_api_key(config)

    vars_payload: dict[str, Any] = {}
    if variables_path:
        vars_payload.update(json.loads(variables_path.read_text(encoding="utf-8-sig")))
    if variables:
        vars_payload.update(variables)
    prompt = render_prompt(template, vars_payload) if template.exists() else ""
    prompt_path = out_dir / f"{input_path.stem}__{template.stem}.prompt.md"

    if not api_key:
        return StyleResult("missing_key", "No GPT Image API key configured.", input_path)
    prompt_path.write_text(prompt, encoding="utf-8")
    if dry_run:
        return StyleResult("dry_run", f"Prompt written: {prompt_path}", input_path, prompt_path=prompt_path)

    output_path = default_output_path(input_path, template, out_dir, output_format)
    image_bytes = request_image_edit(input_path, prompt, config, api_key)
    output_path.write_bytes(image_bytes)
    sidecar_path = output_path.with_suffix(output_path.suffix + ".json")
    sidecar_path.write_text(
        json.dumps(
            {
                "input_path": str(input_path),
                "output_path": str(output_path),
                "prompt_path": str(prompt_path),
                "model": config.get("model") or "gpt-image-2",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return StyleResult("styled", f"Styled image written: {output_path}", input_path, output_path, prompt_path, sidecar_path)


def request_image_edit(input_path: Path, prompt: str, config: dict[str, Any], api_key: str) -> bytes:
    model = config.get("model") or "gpt-image-2"
    endpoint = config.get("endpoint") or "https://api.openai.com/v1/images/edits"
    with input_path.open("rb") as image:
        response = requests.post(
            endpoint,
            headers={"Authorization": f"Bearer {api_key}"},
            data={"model": model, "prompt": prompt, "size": config.get("size") or "1536x1024"},
            files={"image": (input_path.name, image, "image/png")},
            timeout=int(config.get("timeout", 120)),
        )
    if response.status_code >= 400:
        raise GPTImageError(response.text)
    payload = response.json()
    data = payload.get("data") or []
    if data and data[0].get("b64_json"):
        return base64.b64decode(data[0]["b64_json"])
    raise GPTImageError("GPT Image response did not contain b64_json image data.")

