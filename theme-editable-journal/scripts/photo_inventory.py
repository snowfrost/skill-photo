#!/usr/bin/env python3
"""Create a photo inventory CSV and contact sheet for journal layout planning."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from PIL import Image, ImageOps, ImageDraw, ImageFont


EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"}


def image_files(folder: Path) -> list[Path]:
    return sorted(p for p in folder.rglob("*") if p.suffix.lower() in EXTS and p.is_file())


def orientation(w: int, h: int) -> str:
    if w == h:
        return "square"
    return "vertical" if h > w else "horizontal"


def make_thumb(path: Path, size: tuple[int, int]) -> Image.Image:
    img = Image.open(path)
    img = ImageOps.exif_transpose(img).convert("RGB")
    thumb = ImageOps.contain(img, size, method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, "#f7f4ec")
    x = (size[0] - thumb.width) // 2
    y = (size[1] - thumb.height) // 2
    canvas.paste(thumb, (x, y))
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("photo_folder", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--cols", type=int, default=5)
    args = parser.parse_args()

    folder = args.photo_folder.expanduser().resolve()
    out_dir = (args.out or folder / "_journal_inventory").expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    photos = image_files(folder)
    rows = []
    for idx, path in enumerate(photos, 1):
        try:
            with Image.open(path) as img:
                img = ImageOps.exif_transpose(img)
                w, h = img.size
            rows.append({
                "index": idx,
                "file": str(path),
                "width": w,
                "height": h,
                "orientation": orientation(w, h),
                "megapixels": round((w * h) / 1_000_000, 2),
            })
        except Exception as exc:  # keep inventory useful even with one bad file
            rows.append({
                "index": idx,
                "file": str(path),
                "width": "",
                "height": "",
                "orientation": "unreadable",
                "megapixels": "",
                "error": str(exc),
            })

    csv_path = out_dir / "photo_inventory.csv"
    fieldnames = ["index", "file", "width", "height", "orientation", "megapixels", "error"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    if photos:
        cols = max(1, args.cols)
        cell = (220, 190)
        label_h = 38
        contact_rows = (len(photos) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell[0], contact_rows * (cell[1] + label_h)), "#efe9dc")
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.load_default()
        for i, path in enumerate(photos):
            x = (i % cols) * cell[0]
            y = (i // cols) * (cell[1] + label_h)
            try:
                sheet.paste(make_thumb(path, cell), (x, y))
            except Exception:
                draw.rectangle([x, y, x + cell[0], y + cell[1]], fill="#ddd5c8")
                draw.text((x + 8, y + 8), "unreadable", fill="#5b5148", font=font)
            label = f"{i + 1:02d} {path.name[:24]}"
            draw.text((x + 8, y + cell[1] + 10), label, fill="#3c3a35", font=font)
        sheet.save(out_dir / "contact_sheet.jpg", quality=92)

    print(f"photos: {len(photos)}")
    print(f"csv: {csv_path}")
    if photos:
        print(f"contact_sheet: {out_dir / 'contact_sheet.jpg'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
