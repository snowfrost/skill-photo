"""Small shared helpers used across command-line adapters."""

from __future__ import annotations

from typing import Any


def as_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return "" if value is None else str(value)


def clean_placeholder_key(value: Any) -> str | None:
    text = "" if value is None else str(value).strip()
    if not text or text.startswith("填入"):
        return None
    return text
