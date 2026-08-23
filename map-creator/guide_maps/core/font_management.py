"""Font loading helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.font_manager as fm

from guide_maps.core.paths import FONTS_DIR


def load_fonts(family: str = "Noto Sans SC") -> dict[str, str]:
    """Return regular/bold/light font paths when available.

    The function prefers bundled/cache fonts and falls back to Matplotlib's
    default DejaVu Sans so rendering still works in a fresh checkout.
    """
    cache = FONTS_DIR / "cache"
    candidates = {
        "regular": [
            cache / "noto_sans_sc_regular.ttf",
            cache / "noto_serif_sc_regular.ttf",
            FONTS_DIR / "Roboto-Regular.ttf",
        ],
        "bold": [
            cache / "noto_sans_sc_bold.ttf",
            cache / "noto_serif_sc_bold.ttf",
            FONTS_DIR / "Roboto-Bold.ttf",
        ],
        "light": [
            cache / "noto_sans_sc_light.ttf",
            cache / "noto_serif_sc_light.ttf",
            FONTS_DIR / "Roboto-Light.ttf",
        ],
    }
    windows_fonts = Path("C:/Windows/Fonts")
    system_regular = [
        windows_fonts / "msyh.ttc",
        windows_fonts / "simhei.ttf",
        windows_fonts / "simsun.ttc",
    ]
    system_bold = [
        windows_fonts / "msyhbd.ttc",
        windows_fonts / "simhei.ttf",
        windows_fonts / "simsun.ttc",
    ]
    candidates["regular"][0:0] = system_regular
    candidates["bold"][0:0] = system_bold
    candidates["light"][0:0] = system_regular
    default = Path(fm.findfont(fm.FontProperties(family="DejaVu Sans")))
    result: dict[str, str] = {}
    for key, paths in candidates.items():
        result[key] = str(next((path for path in paths if path.exists()), default))
    return result
