#!/usr/bin/env python3
"""Reusable Jufu-Chang-style OSM context renderer for any city or area."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import osmnx as ox
from matplotlib.font_manager import FontProperties
from shapely.geometry import Point

from guide_maps.geocoding.coordinate_transform import amap_to_wgs84
from guide_maps.core.font_management import load_fonts
from guide_maps.core.paths import POSTERS_DIR, ensure_runtime_dirs
from guide_maps.rendering import osm_context_style as style


FIGURE_SIZE = (16, 9)
LEGEND_WIDTH = 0.25
MAP_WIDTH = 1.0 - LEGEND_WIDTH
MAP_ASPECT = FIGURE_SIZE[0] * MAP_WIDTH / FIGURE_SIZE[1]
LEGEND_INDEX_START_Y = 0.735


@dataclass(frozen=True)
class ContextSpot:
    name: str
    display: str
    lat: float
    lon: float
    category: str
    note: str


@dataclass(frozen=True)
class AreaLabel:
    text: str
    lat: float
    lon: float
    size: int = 16


@dataclass(frozen=True)
class ContextMapSpec:
    title: str
    subtitle: str
    output_name: str
    spots: list[ContextSpot]
    road_labels: list[str]
    area_labels: list[AreaLabel]
    footer: str = ""
    show_road_labels: bool = True


def amap_spot(lat_gcj02: float, lon_gcj02: float) -> tuple[float, float]:
    lon_wgs84, lat_wgs84 = amap_to_wgs84(lon_gcj02, lat_gcj02)
    return lat_wgs84, lon_wgs84


def render_context_map(spec: ContextMapSpec) -> Path:
    ensure_runtime_dirs()
    output = POSTERS_DIR / spec.output_name
    fonts = load_fonts("Noto Sans SC")

    style_spots = _to_style_spots(spec.spots)
    frame, center, dist = style.compute_frame(style_spots, target_aspect=MAP_ASPECT)
    large_map = dist > 3200
    network_type = "drive" if large_map else "walk"
    print(f"Fetching OSM map data for {spec.title}...")
    graph = style.fetch_graph(center, dist, network_type=network_type)
    map_features = style.fetch_map_features(center, dist, include_lifestyle=not large_map)
    buildings = style.select_buildings(map_features)
    parks = style.select_parks(map_features)
    water = style.select_water(map_features)
    lifestyle = None if large_map else style.select_lifestyle(map_features)

    graph_proj = ox.project_graph(graph)
    crs = graph_proj.graph["crs"]
    frame_proj = gpd.GeoSeries([frame], crs="EPSG:4326").to_crs(crs).iloc[0]
    minx, miny, maxx, maxy = frame_proj.bounds

    fig = plt.figure(figsize=FIGURE_SIZE, facecolor=style.THEME["bg"])
    legend_ax, ax = _create_context_axes(fig)
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_autoscale_on(False)

    style.draw_polygons(ax, water, crs, style.THEME["water"], 0.8, 0.2)
    style.draw_polygons(ax, parks, crs, style.THEME["park"], 0.65, 0.3)
    style.draw_buildings(ax, buildings, crs)
    style.draw_roads(ax, graph_proj)
    if not large_map:
        style.draw_walkways(ax, graph_proj)
    style.draw_context_pois(ax, lifestyle, crs)
    _lock_view(ax, minx, miny, maxx, maxy)
    draw_area_labels(ax, spec.area_labels, crs, fonts)
    add_title(legend_ax, spec, fonts)
    style.add_index(legend_ax, style_spots, fonts, start_y=LEGEND_INDEX_START_Y)
    label_placer = style.LabelPlacer(ax)
    style.draw_spots(ax, style_spots, crs, fonts, label_placer)
    style.draw_park_labels(ax, parks, crs, fonts, label_placer, limit=10 if not large_map else 6)
    if spec.show_road_labels:
        style.draw_road_labels(
            ax,
            graph_proj,
            fonts,
            label_placer,
            preferred_labels=spec.road_labels,
            limit=5 if large_map else 7,
            large_map=large_map,
        )
    _lock_view(ax, minx, miny, maxx, maxy)
    ax.axis("off")
    legend_ax.axis("off")

    output = style.save_figure(fig, output)
    plt.close(fig)
    print(f"[OK] Wrote {output}")
    return output


def _create_context_axes(fig):
    legend_ax = fig.add_axes((0.0, 0.0, LEGEND_WIDTH, 1.0))
    map_ax = fig.add_axes((LEGEND_WIDTH, 0.0, MAP_WIDTH, 1.0))
    for axis in (legend_ax, map_ax):
        axis.set_facecolor(style.THEME["bg"])
        axis.set_autoscale_on(False)
    legend_ax.set_xlim(0, 1)
    legend_ax.set_ylim(0, 1)
    legend_ax.axvline(1.0, color="#CDBB9F", linewidth=1.2, alpha=0.75, zorder=1)
    return legend_ax, map_ax


def _lock_view(ax, minx: float, miny: float, maxx: float, maxy: float) -> None:
    ax.set_aspect("auto")
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_autoscale_on(False)


def draw_area_labels(ax, labels: list[AreaLabel], crs, fonts) -> None:
    if not labels:
        return
    data = gpd.GeoDataFrame(
        [{"text": label.text, "size": label.size, "geometry": Point(label.lon, label.lat)} for label in labels],
        crs="EPSG:4326",
    ).to_crs(crs)
    for _, row in data.iterrows():
        font = FontProperties(fname=fonts["bold"], size=int(row["size"])) if fonts and fonts.get("bold") else None
        ax.text(
            row.geometry.x,
            row.geometry.y,
            row["text"],
            color="#6F6252",
            fontsize=int(row["size"]),
            fontproperties=font,
            ha="center",
            va="center",
            zorder=6.4,
            alpha=0.92,
            clip_on=True,
            path_effects=[path_effects.withStroke(linewidth=4.8, foreground=style.THEME["bg"])],
        )


def add_title(ax, spec: ContextMapSpec, fonts) -> None:
    title = _format_panel_title(spec.title)
    title_font = FontProperties(fname=fonts["bold"], size=34) if fonts and fonts.get("bold") else None
    ax.text(
        0.08,
        0.94,
        title,
        transform=ax.transAxes,
        color=style.THEME["text"],
        fontproperties=title_font,
        fontsize=34,
        ha="left",
        va="top",
        linespacing=1.08,
        zorder=30,
        path_effects=[path_effects.withStroke(linewidth=3.8, foreground=style.THEME["bg"])],
    )
    ax.plot([0.08, 0.90], [0.765, 0.765], transform=ax.transAxes, color="#BDAA8B", linewidth=1.1, alpha=0.7, zorder=2)


def _format_panel_title(title: str) -> str:
    clean = str(title or "").strip()
    if "\n" in clean or len(clean) <= 8:
        return clean
    for suffix in ("\u6253\u5361\u5730\u56fe", "\u901b\u901b\u5730\u56fe", "\u6f2b\u6e38\u5730\u56fe", "\u5730\u56fe"):
        if clean.endswith(suffix) and len(clean) > len(suffix) + 2:
            return f"{clean[:-len(suffix)]}\n{suffix}"
    midpoint = max(4, len(clean) // 2)
    return f"{clean[:midpoint]}\n{clean[midpoint:]}"


def add_footer(ax, spec: ContextMapSpec, fonts) -> None:
    footer_font = FontProperties(fname=fonts["regular"], size=8) if fonts and fonts.get("regular") else None
    ax.text(0.94, 0.045, spec.footer, transform=ax.transAxes, color=style.THEME["muted"], fontproperties=footer_font, fontsize=8, ha="right", va="bottom", zorder=30)


def _to_style_spots(spots: list[ContextSpot]) -> list[style.Spot]:
    return [style.Spot(spot.name, spot.display, spot.lat, spot.lon, spot.category, spot.note) for spot in spots]
