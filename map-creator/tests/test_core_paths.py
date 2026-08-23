from pathlib import Path

from guide_maps.core.paths import FONTS_DIR, PACKAGE_DIR, PROJECT_ROOT, _env_path


def test_project_root_points_to_repository_root():
    assert (PROJECT_ROOT / "config.example.json").is_file()
    assert PACKAGE_DIR == PROJECT_ROOT / "guide_maps"
    assert FONTS_DIR == PACKAGE_DIR / "fonts"


def test_env_path_prefers_new_name(monkeypatch):
    monkeypatch.setenv("MAP_CREATOR_CACHE_DIR", "new-cache")
    monkeypatch.setenv("OPEN_GUIDE_MAPS_CACHE_DIR", "old-cache")

    assert _env_path("MAP_CREATOR_CACHE_DIR", "OPEN_GUIDE_MAPS_CACHE_DIR", Path("default")) == Path("new-cache")


def test_env_path_keeps_legacy_fallback(monkeypatch):
    monkeypatch.delenv("MAP_CREATOR_CACHE_DIR", raising=False)
    monkeypatch.setenv("OPEN_GUIDE_MAPS_CACHE_DIR", "old-cache")

    assert _env_path("MAP_CREATOR_CACHE_DIR", "OPEN_GUIDE_MAPS_CACHE_DIR", Path("default")) == Path("old-cache")
