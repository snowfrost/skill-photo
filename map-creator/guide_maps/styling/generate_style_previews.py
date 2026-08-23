#!/usr/bin/env python3
"""Generate deterministic style preview images from a GIS map draft."""

from __future__ import annotations

import argparse
import math
import re
import sys
from collections.abc import Callable
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps

from guide_maps.core.paths import PROJECT_ROOT, STYLIZED_DIR


ImageTransform = Callable[[Image.Image], Image.Image]
RoofStyle = dict[str, object]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate deterministic preview images for map style templates.")
    parser.add_argument("--input", required=True, type=Path, help="Source GIS map draft image.")
    parser.add_argument(
        "--template-dir",
        default=PROJECT_ROOT / "prompts" / "map_style_templates",
        type=Path,
        help="Directory containing numbered style prompt templates.",
    )
    parser.add_argument(
        "--output-dir",
        default=STYLIZED_DIR / "style_previews",
        type=Path,
        help="Directory to write preview PNG files.",
    )
    parser.add_argument("--start", default=2, type=int)
    parser.add_argument("--end", default=11, type=int)
    return parser.parse_args()


def generate_previews(input_path: Path, template_dir: Path, output_dir: Path, start: int = 2, end: int = 11) -> list[Path]:
    base = Image.open(input_path).convert("RGB")
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []
    for template in _iter_templates(template_dir, start, end):
        style_number = _style_number(template)
        transform = STYLE_TRANSFORMS.get(style_number, _minimal_info)
        preview = transform(base)
        if preview.size != base.size:
            preview = preview.resize(base.size, Image.Resampling.LANCZOS)
        out_path = output_dir / f"{template.stem}.png"
        preview.save(out_path)
        outputs.append(out_path)
    return outputs


def _iter_templates(template_dir: Path, start: int, end: int) -> list[Path]:
    templates = []
    for path in sorted(template_dir.glob("*.md")):
        number = _style_number(path)
        if number is not None and start <= number <= end:
            templates.append(path)
    return templates


def _style_number(path: Path) -> int | None:
    match = re.match(r"^(\d{2})_", path.name)
    return int(match.group(1)) if match else None


def _as_rgba(image: Image.Image) -> Image.Image:
    return image.convert("RGBA")


def _tint(image: Image.Image, color: tuple[int, int, int], opacity: float) -> Image.Image:
    overlay = Image.new("RGB", image.size, color)
    return Image.blend(image, overlay, opacity)


def _contrast(image: Image.Image, factor: float) -> Image.Image:
    return ImageEnhance.Contrast(image).enhance(factor)


def _saturation(image: Image.Image, factor: float) -> Image.Image:
    return ImageEnhance.Color(image).enhance(factor)


def _brightness(image: Image.Image, factor: float) -> Image.Image:
    return ImageEnhance.Brightness(image).enhance(factor)


def _edge_layer(image: Image.Image, color: tuple[int, int, int], opacity: float, blur: float = 0.0) -> Image.Image:
    edges = ImageOps.grayscale(image).filter(ImageFilter.FIND_EDGES)
    edges = ImageOps.autocontrast(edges)
    if blur:
        edges = edges.filter(ImageFilter.GaussianBlur(blur))
    alpha = edges.point(lambda value: min(255, int(value * opacity)))
    layer = Image.new("RGBA", image.size, color + (0,))
    layer.putalpha(alpha)
    return layer


def _composite(base: Image.Image, *layers: Image.Image) -> Image.Image:
    current = _as_rgba(base)
    for layer in layers:
        current = Image.alpha_composite(current, layer)
    return current.convert("RGB")


def _screen(base: Image.Image, overlay: Image.Image, opacity: float) -> Image.Image:
    screened = ImageChops.screen(base.convert("RGB"), overlay.convert("RGB"))
    return Image.blend(base, screened, opacity)


def _draw_scanlines(image: Image.Image, color: tuple[int, int, int], opacity: int = 22, step: int = 6) -> Image.Image:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for y in range(0, image.height, step):
        draw.line((0, y, image.width, y), fill=color + (opacity,), width=1)
    return _composite(image, layer)


def _draw_grid(image: Image.Image, color: tuple[int, int, int], opacity: int = 24, spacing: int = 96) -> Image.Image:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for x in range(0, image.width, spacing):
        draw.line((x, 0, x, image.height), fill=color + (opacity,), width=1)
    for y in range(0, image.height, spacing):
        draw.line((0, y, image.width, y), fill=color + (opacity,), width=1)
    return _composite(image, layer)


def _paper_noise(image: Image.Image, opacity: float = 0.08, sigma: float = 32.0) -> Image.Image:
    noise = Image.effect_noise(image.size, sigma).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(image, noise_rgb, opacity)


def _draw_border(image: Image.Image, color: tuple[int, int, int], opacity: int = 80, width: int = 3) -> Image.Image:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    inset = width * 3
    for i in range(width):
        draw.rectangle((inset + i, inset + i, image.width - inset - i, image.height - inset - i), outline=color + (opacity,))
    return _composite(image, layer)


def _draw_roofs(base: Image.Image, roof_style: RoofStyle, spacing: int = 34) -> Image.Image:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    start_x = int(base.width * 0.25) + spacing
    end_x = base.width - spacing
    start_y = spacing
    end_y = base.height - spacing

    for y in range(start_y, end_y, spacing):
        for x in range(start_x, end_x, spacing):
            sample_x = x + ((x * 17 + y * 11) % 13) - 6
            sample_y = y + ((x * 7 + y * 19) % 13) - 6
            if not _looks_like_building(base, sample_x, sample_y):
                continue
            size = int(roof_style.get("size", 11))
            angle = -1 if (x // spacing + y // spacing) % 2 else 1
            _draw_roof(draw, sample_x, sample_y, size, angle, roof_style)

    return layer


def _looks_like_building(image: Image.Image, x: int, y: int) -> bool:
    if x < int(image.width * 0.25) or x >= image.width or y < 0 or y >= image.height:
        return False
    window = 2
    pixels = []
    for yy in range(max(0, y - window), min(image.height, y + window + 1)):
        for xx in range(max(0, x - window), min(image.width, x + window + 1)):
            pixels.append(image.getpixel((xx, yy)))
    if not pixels:
        return False
    r = sum(pixel[0] for pixel in pixels) / len(pixels)
    g = sum(pixel[1] for pixel in pixels) / len(pixels)
    b = sum(pixel[2] for pixel in pixels) / len(pixels)
    brightness = (r + g + b) / 3
    spread = max(r, g, b) - min(r, g, b)
    green_bias = g - max(r, b)
    blue_bias = b - max(r, g)
    return 174 <= brightness <= 232 and spread <= 34 and green_bias < 10 and blue_bias < 12


def _draw_roof(draw: ImageDraw.ImageDraw, x: int, y: int, size: int, angle: int, style: RoofStyle) -> None:
    roof = tuple(style.get("roof", (170, 120, 82, 90)))
    side = tuple(style.get("side", (120, 90, 70, 46)))
    line = tuple(style.get("line", (80, 60, 42, 88)))
    width = int(style.get("line_width", 1))
    mode = str(style.get("mode", "filled"))

    if mode == "pixel":
        draw.rectangle((x - size, y - size // 2, x + size, y + size // 2), fill=roof)
        draw.line((x - size, y, x + size, y), fill=line, width=width)
        return

    ridge_y = y - size // 2
    left = (x - size, y)
    right = (x + size, y)
    ridge = (x + angle * size // 3, ridge_y)
    lower_left = (x - size + angle * 3, y + size // 2)
    lower_right = (x + size + angle * 3, y + size // 2)

    if mode == "outline":
        draw.line((left, ridge, right), fill=line, width=width)
        draw.line((left, lower_left, lower_right, right), fill=line, width=width)
        draw.line((ridge, (x + angle * size // 3, y + size // 2)), fill=line, width=width)
        return

    draw.polygon((left, ridge, right, (x + angle * size // 3, y + size // 2)), fill=roof)
    draw.polygon((left, lower_left, lower_right, right), fill=side)
    draw.line((left, ridge, right), fill=line, width=width)
    draw.line((ridge, (x + angle * size // 3, y + size // 2)), fill=line, width=width)


def _map_area_mask(size: tuple[int, int]) -> Image.Image:
    width, height = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((int(width * 0.25), 0, width, height), fill=255)
    return mask


def _right_side_layer(base: Image.Image, layer: Image.Image) -> Image.Image:
    masked = Image.new("RGBA", base.size, (0, 0, 0, 0))
    masked.paste(layer.convert("RGBA"), (0, 0), _map_area_mask(base.size))
    return _composite(base, masked)


def _cyberpunk(base: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(base)
    image = ImageOps.colorize(gray, black="#050817", white="#1dd7ff").convert("RGB")
    image = _contrast(image, 1.35)
    image = _screen(image, _edge_layer(base, (255, 30, 200), 0.9).convert("RGB"), 0.5)
    image = _composite(image, _edge_layer(base, (0, 255, 230), 0.45, blur=1.2))
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[2], spacing=32))
    image = _draw_grid(image, (0, 220, 255), opacity=20, spacing=80)
    image = _draw_scanlines(image, (255, 0, 180), opacity=18, step=5)
    return _draw_border(image, (0, 220, 255), opacity=110, width=2)


def _game_quest(base: Image.Image) -> Image.Image:
    image = _saturation(base, 1.55)
    image = _contrast(image, 1.2)
    image = ImageOps.posterize(image, 5)
    image = _tint(image, (12, 34, 70), 0.18)
    image = _composite(image, _edge_layer(base, (40, 190, 255), 0.42))
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[3], spacing=34))
    image = _draw_grid(image, (45, 180, 255), opacity=18, spacing=72)
    return _draw_border(image, (40, 180, 255), opacity=95, width=2)


def _vintage(base: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(base)
    image = ImageOps.colorize(gray, black="#4c321f", white="#f3dfbd").convert("RGB")
    image = _saturation(image, 0.82)
    image = _contrast(image, 1.08)
    image = _paper_noise(image, opacity=0.1, sigma=38)
    image = _composite(image, _edge_layer(base, (96, 57, 31), 0.18))
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[4], spacing=34))
    return _draw_border(image, (106, 73, 42), opacity=90, width=2)


def _blueprint(base: Image.Image) -> Image.Image:
    bg = Image.new("RGB", base.size, (6, 23, 55))
    edges = _edge_layer(base, (230, 248, 255), 1.0)
    glow = _edge_layer(base, (64, 210, 255), 0.55, blur=1.5)
    image = _composite(bg, glow, edges)
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[5], spacing=32))
    image = _draw_grid(image, (145, 220, 255), opacity=36, spacing=64)
    image = _draw_scanlines(image, (160, 220, 255), opacity=12, step=8)
    return _draw_border(image, (160, 220, 255), opacity=90, width=2)


def _japanese_walk(base: Image.Image) -> Image.Image:
    image = _brightness(base, 1.08)
    image = _saturation(image, 0.64)
    image = _contrast(image, 0.94)
    image = _tint(image, (247, 230, 218), 0.18)
    image = _paper_noise(image, opacity=0.035, sigma=18)
    image = _composite(image, _edge_layer(base, (74, 72, 68), 0.12))
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[6], spacing=36))
    return _draw_border(image, (180, 130, 115), opacity=48, width=1)


def _pixel_game(base: Image.Image) -> Image.Image:
    width, height = base.size
    small = base.resize((max(1, width // 4), max(1, height // 4)), Image.Resampling.NEAREST)
    image = small.resize(base.size, Image.Resampling.NEAREST)
    image = ImageOps.posterize(_saturation(image, 1.35), 4)
    image = _contrast(image, 1.18)
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[7], spacing=36))
    return _draw_grid(image, (0, 0, 0), opacity=16, spacing=32)


def _night_lights(base: Image.Image) -> Image.Image:
    image = _brightness(base, 0.38)
    image = _saturation(image, 1.25)
    image = _tint(image, (8, 17, 38), 0.35)
    cyan = _edge_layer(base, (18, 220, 255), 0.45, blur=0.8)
    amber = _edge_layer(base, (255, 176, 56), 0.28, blur=2.2)
    image = _composite(image, amber, cyan)
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[8], spacing=34))
    image = _draw_scanlines(image, (80, 150, 255), opacity=10, step=7)
    return _draw_border(image, (255, 190, 80), opacity=55, width=1)


def _outdoor_contour(base: Image.Image) -> Image.Image:
    image = _saturation(base, 0.78)
    image = _contrast(image, 1.02)
    image = _tint(image, (224, 211, 168), 0.2)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    start_x = int(image.width * 0.25)
    for y in range(-120, image.height + 120, 58):
        points = []
        for x in range(start_x, image.width + 24, 24):
            wave = int(18 * math.sin((x + y) / 105))
            points.append((x, y + wave))
        draw.line(points, fill=(112, 96, 46, 40), width=2)
    image = _right_side_layer(image, layer)
    image = _composite(image, _edge_layer(base, (80, 105, 45), 0.16))
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[9], spacing=36))
    return _draw_border(image, (116, 98, 46), opacity=54, width=1)


def _curation(base: Image.Image) -> Image.Image:
    image = _brightness(base, 1.16)
    image = _saturation(image, 0.42)
    image = _contrast(image, 1.05)
    image = _tint(image, (250, 250, 246), 0.16)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    start_x = int(image.width * 0.25)
    swatches = [
        (start_x + 60, 92, start_x + 210, 190, (231, 70, 85, 34)),
        (image.width - 360, 210, image.width - 160, 330, (47, 130, 210, 30)),
        (start_x + 460, image.height - 260, start_x + 700, image.height - 140, (245, 181, 52, 28)),
    ]
    for x0, y0, x1, y1, color in swatches:
        draw.rectangle((x0, y0, x1, y1), fill=color)
    image = _right_side_layer(image, layer)
    image = _composite(image, _edge_layer(base, (32, 32, 32), 0.12))
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[10], spacing=40))
    return _draw_border(image, (32, 32, 32), opacity=58, width=1)


def _minimal_info(base: Image.Image) -> Image.Image:
    image = _brightness(base, 1.12)
    image = _saturation(image, 0.34)
    image = _contrast(image, 1.18)
    image = ImageOps.posterize(image, 5)
    image = _tint(image, (248, 248, 244), 0.08)
    image = _composite(image, _edge_layer(base, (45, 45, 45), 0.14))
    image = _composite(image, _draw_roofs(base, ROOF_STYLES[11], spacing=42))
    return _draw_border(image, (80, 80, 80), opacity=42, width=1)


STYLE_TRANSFORMS: dict[int, ImageTransform] = {
    2: _cyberpunk,
    3: _game_quest,
    4: _vintage,
    5: _blueprint,
    6: _japanese_walk,
    7: _pixel_game,
    8: _night_lights,
    9: _outdoor_contour,
    10: _curation,
    11: _minimal_info,
}

ROOF_STYLES: dict[int, RoofStyle] = {
    2: {"mode": "outline", "line": (0, 255, 235, 150), "line_width": 2, "size": 10},
    3: {"roof": (120, 216, 255, 92), "side": (40, 90, 150, 58), "line": (230, 255, 255, 130), "size": 11},
    4: {"roof": (128, 82, 46, 84), "side": (96, 64, 42, 42), "line": (74, 45, 25, 100), "size": 10},
    5: {"mode": "outline", "line": (225, 252, 255, 130), "line_width": 1, "size": 10},
    6: {"roof": (208, 145, 136, 58), "side": (178, 154, 132, 32), "line": (116, 90, 80, 58), "size": 9},
    7: {"mode": "pixel", "roof": (226, 136, 82, 96), "line": (92, 60, 40, 84), "size": 8},
    8: {"roof": (255, 185, 82, 60), "side": (78, 62, 84, 48), "line": (255, 214, 130, 110), "size": 9},
    9: {"roof": (138, 103, 64, 58), "side": (104, 122, 72, 34), "line": (82, 72, 42, 78), "size": 9},
    10: {"roof": (230, 72, 92, 46), "side": (64, 104, 170, 30), "line": (42, 42, 42, 70), "size": 10},
    11: {"mode": "outline", "line": (56, 56, 56, 72), "line_width": 1, "size": 9},
}


def main() -> int:
    args = parse_args()
    outputs = generate_previews(args.input, args.template_dir, args.output_dir, args.start, args.end)
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
