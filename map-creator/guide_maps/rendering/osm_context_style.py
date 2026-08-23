#!/usr/bin/env python3
"""Reusable OSM/GIS drawing helpers for guide maps."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import geopandas as gpd
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import osmnx as ox
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import Bbox
from shapely.geometry import LineString, Point, box
from shapely.ops import linemerge

from guide_maps.core.cache import get_cache
from guide_maps.core.font_management import load_fonts
from guide_maps.core.paths import POSTERS_DIR, PROJECT_ROOT, ensure_runtime_dirs


@dataclass(frozen=True)
class Spot:
    name: str
    display: str
    lat: float
    lon: float
    category: str
    note: str


@dataclass(frozen=True)
class RoadLabelCandidate:
    name: str
    line: object
    score: float


@dataclass(frozen=True)
class IndexEntryLayout:
    marker_x: float
    text_x: float
    marker_y: float
    name_y: float
    note_y: float


THEME = {
    "bg": "#F7F1E7",
    "panel": "#FFF9ED",
    "building": "#D8CDBA",
    "park": "#B9C9A6",
    "road_major": "#A98F6D",
    "road_minor": "#D0B993",
    "road_tiny": "#E2D1B0",
    "text": "#29241E",
    "muted": "#766B5D",
    "water": "#9BC9D2",
}

CATEGORY_COLORS = {
    "coffee": "#2B7C8E",
    "bar": "#7D5A9E",
    "vintage": "#A65F45",
    "food": "#B48A3C",
}

INDEX_MARKER_X = 0.06
INDEX_TEXT_X = 0.099
INDEX_START_Y = 0.820
INDEX_MIN_ITEM_GAP = 0.086
INDEX_MAX_ITEM_GAP = 0.102
INDEX_NOTE_OFFSET = 0.030

BASE_FEATURE_TAGS = {
    "building": True,
    "leisure": "park",
    "landuse": ["grass", "forest"],
    "natural": "water",
    "waterway": True,
}

LIFESTYLE_FEATURE_TAGS = {
    "amenity": ["cafe", "bar", "pub", "restaurant", "fast_food"],
    "shop": ["boutique", "clothes", "florist", "books", "antiques", "art"],
    "tourism": ["gallery", "artwork", "attraction"],
    "historic": True,
}

TRANSIT_FEATURE_TAGS = {
    "railway": ["subway_entrance", "station"],
    "public_transport": ["station", "platform"],
    "highway": "bus_stop",
}

ROAD_LABELS = ["富民路", "长乐路", "巨鹿路", "常熟路", "陕西南路", "淮海中路", "延安中路", "华山路"]


def main() -> None:
    ensure_runtime_dirs()
    poi_path = PROJECT_ROOT / "data" / "poi_sets" / "shanghai_jufuchang_guide.json"
    output = POSTERS_DIR / "shanghai_jufuchang_guide_map_osm_context.png"
    spots = load_spots(poi_path)
    fonts = load_fonts("Noto Sans SC")

    frame, center, dist = compute_frame(spots)
    print("Fetching OSM map data...")
    graph = fetch_graph(center, dist)
    map_features = fetch_map_features(center, dist, include_lifestyle=True, include_transit=True)
    buildings = select_buildings(map_features)
    parks = select_parks(map_features)
    water = select_water(map_features)
    lifestyle = select_lifestyle(map_features)
    transit = select_transit(map_features)

    graph_proj = ox.project_graph(graph)
    crs = graph_proj.graph["crs"]
    frame_proj = gpd.GeoSeries([frame], crs="EPSG:4326").to_crs(crs).iloc[0]
    minx, miny, maxx, maxy = frame_proj.bounds

    fig, ax = plt.subplots(figsize=(16, 10), facecolor=THEME["bg"])
    ax.set_facecolor(THEME["bg"])
    ax.set_position((0.0, 0.0, 1.0, 1.0))
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_autoscale_on(False)

    draw_polygons(ax, water, crs, THEME["water"], 0.8, 0.2)
    draw_polygons(ax, parks, crs, THEME["park"], 0.65, 0.3)
    draw_buildings(ax, buildings, crs)
    draw_roads(ax, graph_proj)
    draw_walkways(ax, graph_proj)
    draw_context_pois(ax, lifestyle, crs)
    draw_transit(ax, transit, crs, fonts)
    draw_road_labels(ax, graph_proj, fonts)
    draw_spots(ax, spots, crs, fonts)
    add_title(ax, fonts)
    add_index(ax, spots, fonts)
    add_footer(ax, fonts)
    ax.axis("off")

    output = save_figure(fig, output)
    plt.close(fig)
    print(f"[OK] Wrote {output}")


def load_spots(path: Path) -> list[Spot]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    meta = {
        "SLAB TOWN": ("SLAB TOWN", "coffee", "富民路咖啡主理"),
        "村口大树": ("村口大树", "coffee", "意境特调咖啡"),
        "ALWAYS Coffee&Bar": ("ALWAYS Coffee&Bar", "bar", "夜晚威士忌酒吧"),
        "times remake": ("times remake", "vintage", "古着与复古选品"),
        "Cosmos Retro Flower & Vintage": ("Cosmos Retro Flower", "vintage", "鲜花与复古选品"),
        "台湾黑金卤肉饭": ("台湾黑金卤肉饭", "food", "富民路台式简餐"),
    }
    spots = []
    for poi in payload.get("pois", []):
        name = str(poi.get("input_name") or "")
        if poi.get("lng_wgs84") is None or poi.get("lat_wgs84") is None:
            continue
        display, category, note = meta.get(name, (name, "coffee", ""))
        spots.append(Spot(name, display, float(poi["lat_wgs84"]), float(poi["lng_wgs84"]), category, note))
    return spots


def compute_frame(spots: list[Spot], target_aspect: float = 16 / 10):
    gdf = gpd.GeoDataFrame([{"geometry": Point(spot.lon, spot.lat)} for spot in spots], crs="EPSG:4326")
    projected = gdf.to_crs(gdf.estimate_utm_crs())
    minx, miny, maxx, maxy = projected.total_bounds
    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2
    width = max(maxx - minx + 560, 1500)
    height = max(maxy - miny + 680, 1600)
    if width / height < target_aspect:
        width = height * target_aspect
    else:
        height = width / target_aspect
    frame_proj = box(cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2)
    frame_wgs84 = gpd.GeoSeries([frame_proj], crs=projected.crs).to_crs("EPSG:4326").iloc[0]
    center_wgs84 = gpd.GeoSeries([Point(cx, cy)], crs=projected.crs).to_crs("EPSG:4326").iloc[0]
    dist = int(max(width, height) / 2 + 520)
    return frame_wgs84, (center_wgs84.y, center_wgs84.x), dist


def cache_get_or_set(key: str, factory: Callable):
    cache = get_cache()
    cached = cache.get(key)
    if cached is not None:
        return cached
    value = factory()
    cache.set(key, value)
    return value


def save_figure(fig, output: Path) -> Path:
    try:
        fig.savefig(output, dpi=230, facecolor=THEME["bg"], pad_inches=0)
        return output
    except PermissionError:
        fallback_dir = PROJECT_ROOT / "outputs" / "fallback"
        fallback_dir.mkdir(exist_ok=True)
        fallback = fallback_dir / f"{output.stem}_fixed{output.suffix}"
        fig.savefig(fallback, dpi=230, facecolor=THEME["bg"], pad_inches=0)
        print(f"[!] Output was locked, wrote fallback: {fallback}")
        return fallback


def fetch_graph(point: tuple[float, float], dist: float, network_type: str = "walk"):
    return cache_get_or_set(
        f"osm_{network_type}_graph_{point[0]}_{point[1]}_{dist}",
        lambda: ox.graph_from_point(point, dist=dist, network_type=network_type, simplify=True),
    )


def fetch_features(point: tuple[float, float], dist: float, tags: dict, key: str):
    def factory():
        try:
            return ox.features_from_point(point, tags=tags, dist=dist)
        except Exception as exc:
            print(f"[!] Could not fetch {key}: {exc}")
            return None

    return cache_get_or_set(f"osm_{key}_{point[0]}_{point[1]}_{dist}", factory)


def fetch_map_features(point: tuple[float, float], dist: float, *, include_lifestyle: bool = True, include_transit: bool = False):
    tags = dict(BASE_FEATURE_TAGS)
    key_parts = ["map_features"]
    if include_lifestyle:
        tags.update(LIFESTYLE_FEATURE_TAGS)
        key_parts.append("lifestyle")
    if include_transit:
        tags.update(TRANSIT_FEATURE_TAGS)
        key_parts.append("transit")
    return fetch_features(point, dist, tags, "_".join(key_parts))


def select_buildings(features):
    return _filter_features(features, lambda row: _row_has_any(row, "building"))


def select_parks(features):
    return _filter_features(features, lambda row: _value_has(row.get("leisure"), {"park"}) or _value_has(row.get("landuse"), {"grass", "forest"}))


def select_water(features):
    return _filter_features(features, lambda row: _value_has(row.get("natural"), {"water"}) or _row_has_any(row, "waterway"))


def select_lifestyle(features):
    return _filter_features(features, lambda row: _classify_context(row) is not None)


def select_transit(features):
    return _filter_features(
        features,
        lambda row: _value_has(row.get("railway"), {"subway_entrance", "station"})
        or _value_has(row.get("public_transport"), {"station", "platform"})
        or _value_has(row.get("highway"), {"bus_stop"}),
    )


def _filter_features(features, predicate: Callable):
    if features is None or len(features) == 0:
        return None
    mask = [bool(predicate(row)) for _, row in features.iterrows()]
    return features.loc[mask]


def _row_has_any(row, key: str) -> bool:
    value = row.get(key)
    if isinstance(value, list):
        return any(_truthy_osm_value(item) for item in value)
    return _truthy_osm_value(value)


def _truthy_osm_value(value) -> bool:
    if value is None or value is False:
        return False
    text = str(value).strip().lower()
    return text not in {"", "nan", "none", "false"}


def draw_polygons(ax, features, crs, color, alpha, zorder):
    if features is None or len(features) == 0:
        return
    data = features[features.geometry.type.isin(["Polygon", "MultiPolygon"])]
    if len(data) > 0:
        data.to_crs(crs).plot(ax=ax, color=color, linewidth=0, alpha=alpha, zorder=zorder)


def draw_buildings(ax, buildings, crs):
    if buildings is None or len(buildings) == 0:
        return
    data = buildings[buildings.geometry.type.isin(["Polygon", "MultiPolygon"])]
    if len(data) > 0:
        data.to_crs(crs).plot(ax=ax, color=THEME["building"], edgecolor="#C6B9A4", linewidth=0.12, alpha=0.78, zorder=0.7)


def draw_roads(ax, graph) -> None:
    colors, widths = [], []
    for _, _, _, data in graph.edges(keys=True, data=True):
        color, linewidth = road_style(data.get("highway", "road"))
        colors.append(color)
        widths.append(linewidth)
    ox.plot_graph(graph, ax=ax, node_size=0, edge_color=colors, edge_linewidth=widths, edge_alpha=0.95, bgcolor=THEME["bg"], show=False, close=False)


def draw_walkways(ax, graph) -> None:
    edges = ox.graph_to_gdfs(graph, nodes=False, fill_edge_geometry=True)
    if edges.empty or "highway" not in edges.columns:
        return
    data = edges[edges["highway"].apply(_is_walkway)]
    if not data.empty:
        data.plot(ax=ax, color="#B88268", linewidth=0.62, alpha=0.55, linestyle=(0, (2.0, 3.0)), zorder=4.2)


CONTEXT_POI_STYLES = {
    "eat_drink": {"color": "#C98B55", "marker": "o", "size": 34},
    "shop": {"color": "#8F7F5D", "marker": "D", "size": 30},
    "culture": {"color": "#6F8F73", "marker": "^", "size": 42},
}


def draw_context_pois(ax, features, crs) -> None:
    points = _thin_points(_collect_context_points(features, crs), min_gap=72, limit=52)
    for category, style in CONTEXT_POI_STYLES.items():
        selected = [point for point in points if point["category"] == category]
        if selected:
            ax.scatter([p["x"] for p in selected], [p["y"] for p in selected], s=style["size"], marker=style["marker"], color=style["color"], edgecolors=THEME["panel"], linewidths=0.75, alpha=0.78, zorder=5.4, clip_on=True)


def draw_transit(ax, features, crs, fonts) -> None:
    points = _collect_transit_points(features, crs)
    subway = _thin_points([point for point in points if point["category"] == "subway"], min_gap=105, limit=10)
    bus = _thin_points([point for point in points if point["category"] == "bus"], min_gap=115, limit=16)
    if subway:
        ax.scatter([p["x"] for p in subway], [p["y"] for p in subway], s=96, marker="s", color="#4F8EA7", edgecolors=THEME["panel"], linewidths=1.2, alpha=0.9, zorder=7.0, clip_on=True)
        font = FontProperties(fname=fonts["bold"], size=6.5) if fonts and fonts.get("bold") else None
        for point in subway:
            ax.text(point["x"], point["y"], "M", color=THEME["panel"], fontsize=6.5, fontproperties=font, ha="center", va="center", zorder=7.2, clip_on=True)
    if bus:
        ax.scatter([p["x"] for p in bus], [p["y"] for p in bus], s=42, marker="^", color="#7FA7AE", edgecolors=THEME["panel"], linewidths=0.75, alpha=0.68, zorder=5.7, clip_on=True)


class LabelPlacer:
    def __init__(self, ax, pad_px: float = 4):
        self.ax = ax
        self.pad_px = pad_px
        self.occupied: list[Bbox] = []
        self._refresh()

    def _refresh(self) -> None:
        self.ax.figure.canvas.draw()
        self.renderer = self.ax.figure.canvas.get_renderer()
        self.axes_bbox = self.ax.get_window_extent(self.renderer)
        self.label_bounds = self.axes_bbox.padded(-14)
        for text in self.ax.texts:
            if text.get_visible() and text.get_text():
                self.add_bbox(text.get_window_extent(self.renderer))

    def add_bbox(self, bbox: Bbox) -> None:
        self.occupied.append(bbox.padded(self.pad_px))

    def reserve_point(self, x: float, y: float, radius_px: float = 18) -> None:
        sx, sy = self.ax.transData.transform((x, y))
        self.add_bbox(Bbox.from_extents(sx - radius_px, sy - radius_px, sx + radius_px, sy + radius_px))

    def place_annotated(self, x, y, text, offsets, *, color, fontsize, fontproperties=None, zorder=10, weight_stroke=3.2, alpha=1.0):
        for dx, dy in offsets:
            artist = self.ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords="offset points", color=color, fontsize=fontsize, fontproperties=fontproperties, ha="left" if dx >= 0 else "right", va="bottom" if dy >= 0 else "top", zorder=zorder, alpha=alpha, clip_on=False, path_effects=[path_effects.withStroke(linewidth=weight_stroke, foreground=THEME["bg"])])
            if self._accept(artist):
                return artist
            artist.remove()
        return None

    def place_text(self, x, y, text, *, color, fontsize, fontproperties=None, zorder=6, rotation=0, alpha=1.0, stroke=3.0):
        artist = self.ax.text(x, y, text, color=color, fontsize=fontsize, fontproperties=fontproperties, ha="center", va="center", rotation=rotation, rotation_mode="anchor", zorder=zorder, alpha=alpha, clip_on=False, path_effects=[path_effects.withStroke(linewidth=stroke, foreground=THEME["bg"])])
        if self._accept(artist):
            return artist
        artist.remove()
        return None

    def _accept(self, artist) -> bool:
        self.ax.figure.canvas.draw()
        bbox = artist.get_window_extent(self.ax.figure.canvas.get_renderer()).padded(self.pad_px)
        if not self.label_bounds.contains(bbox.x0, bbox.y0) or not self.label_bounds.contains(bbox.x1, bbox.y1):
            return False
        if any(bbox.overlaps(existing) for existing in self.occupied):
            return False
        self.add_bbox(bbox)
        return True


def draw_road_labels(ax, graph, fonts, placer: LabelPlacer | None = None, preferred_labels: list[str] | None = None, limit: int = 6, large_map: bool = False) -> None:
    edges = ox.graph_to_gdfs(graph, nodes=False, fill_edge_geometry=True)
    if edges.empty or "name" not in edges.columns:
        return
    label_font = FontProperties(fname=fonts["regular"], size=13) if fonts and fonts.get("regular") else None
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    candidates = _rank_road_label_candidates(edges, box(xlim[0], ylim[0], xlim[1], ylim[1]), preferred_labels or ROAD_LABELS, limit=limit, large_map=large_map)
    placed = 0
    for candidate in candidates:
        point, before, after = _road_label_anchor(candidate.line)
        angle = _screen_angle(ax, before.x, before.y, after.x, after.y)
        if angle > 90:
            angle -= 180
        if angle < -90:
            angle += 180
        if placer:
            artist = placer.place_text(point.x, point.y, candidate.name, color="#6F6252", fontsize=13, fontproperties=label_font, zorder=6, rotation=angle, alpha=0.92, stroke=4.2)
            if not artist:
                continue
        else:
            ax.text(point.x, point.y, candidate.name, color="#6F6252", fontsize=13, fontproperties=label_font, ha="center", va="center", rotation=angle, rotation_mode="anchor", zorder=6, alpha=0.92, clip_on=True, path_effects=[path_effects.withStroke(linewidth=4.2, foreground=THEME["bg"])])
        placed += 1
        if placed >= limit:
            break


def _road_label_anchor(line):
    segments = _road_label_segments(line)
    if not segments:
        point = line.interpolate(0.5, normalized=True)
        before = line.interpolate(0.48, normalized=True)
        after = line.interpolate(0.52, normalized=True)
        return point, before, after
    min_segment_length = min(max(line.length * 0.04, 40), 120)
    usable = [segment for segment in segments if segment.length >= min_segment_length] or segments

    def score(segment):
        point = segment.interpolate(0.5, normalized=True)
        distance = line.project(point)
        normalized = distance / max(line.length, 1)
        endpoint_margin = min(normalized, 1 - normalized)
        endpoint_penalty = line.length if endpoint_margin < 0.14 else 0
        return segment.length + endpoint_margin * line.length * 0.35 - endpoint_penalty

    segment = max(usable, key=score)
    point = segment.interpolate(0.5, normalized=True)
    before = segment.interpolate(0.20, normalized=True)
    after = segment.interpolate(0.80, normalized=True)
    return point, before, after


def _road_label_segments(line) -> list:
    lines = list(line.geoms) if hasattr(line, "geoms") else [line]
    segments = []
    for part in lines:
        coords = list(part.coords) if hasattr(part, "coords") else []
        for start, end in zip(coords, coords[1:]):
            segment = LineString([start, end])
            if segment.length > 0:
                segments.append(segment)
    return segments


def _rank_road_label_candidates(edges, view, preferred_labels: list[str], limit: int, large_map: bool) -> list[RoadLabelCandidate]:
    preferred = [label.strip() for label in preferred_labels if label and label.strip()]
    min_length = 300 if large_map else 160
    min_weight = 2.7 if large_map else 1.4
    grouped: dict[str, dict] = {}

    for _, row in edges.iterrows():
        names = list(_road_names(row.get("name")))
        fragments = [fragment for fragment in _visible_road_fragments(row.geometry, view) if fragment.length >= min_length]
        if not names or not fragments:
            continue
        for name in names:
            preferred_match = any(_road_label_matches(name, label) for label in preferred)
            if not preferred_match and not _road_label_name_allowed(name):
                continue
            weight = _road_label_weight(row.get("highway"))
            if weight < (1.4 if preferred_match else min_weight):
                continue
            bucket = grouped.setdefault(name, {"lines": [], "length": 0.0, "weight": 0.0})
            bucket["lines"].extend(fragments)
            bucket["length"] += sum(fragment.length for fragment in fragments)
            bucket["weight"] = max(bucket["weight"], weight)

    candidates: list[RoadLabelCandidate] = []
    for name, data in grouped.items():
        merged = linemerge(data["lines"])
        visible = list(merged.geoms) if hasattr(merged, "geoms") else [merged]
        visible = [line for line in visible if not line.is_empty and line.length >= min_length]
        if not visible:
            continue
        line = max(visible, key=lambda item: item.length)
        manual_boost = 2.8 if any(_road_label_matches(name, label) for label in preferred) else 0.0
        score = data["length"] * (1.0 + data["weight"] * 0.28) + manual_boost * max(data["length"], 900)
        candidates.append(RoadLabelCandidate(name=name, line=line, score=score))
    candidates.sort(key=lambda item: (-item.score, item.name))
    return candidates[: max(limit * 4, limit)]


def _visible_road_fragments(geometry, view) -> list:
    if geometry is None or geometry.is_empty or not geometry.intersects(view):
        return []
    clipped = geometry.intersection(view)
    if clipped.is_empty:
        return []
    parts = list(clipped.geoms) if hasattr(clipped, "geoms") else [clipped]
    return [part for part in parts if hasattr(part, "length") and part.length > 0]


def _road_names(value) -> list[str]:
    values = value if isinstance(value, list) else [value]
    names = []
    for item in values:
        text = str(item).strip()
        if text and text.lower() not in {"nan", "none"}:
            names.append(text)
    return names


def _road_label_weight(highway) -> float:
    if isinstance(highway, list):
        return max((_road_label_weight(item) for item in highway), default=0.0)
    weights = {"motorway": 5.0, "trunk": 4.8, "primary": 4.4, "secondary": 3.7, "tertiary": 3.0, "unclassified": 2.1, "residential": 1.8, "living_street": 1.6, "pedestrian": 1.5, "service": 1.2}
    return weights.get(str(highway), 0.0)


def _road_label_matches(name: str, preferred: str) -> bool:
    return name == preferred or preferred in name or name in preferred


def _road_label_name_allowed(name: str) -> bool:
    blocked_terms = ("快速路", "高架", "隧道", "立交", "内环", "绕城", "高速", "铁路", "城际", "地铁", "专线")
    if any(term in name for term in blocked_terms):
        return False
    if name.endswith("线"):
        return False
    return any(name.endswith(suffix) for suffix in ("路", "街", "巷", "大道", "街道", "桥", "门"))


def road_style(highway):
    if isinstance(highway, list):
        highway = highway[0] if highway else "road"
    if highway in {"footway", "pedestrian", "steps", "path"}:
        return "#C4A17E", 0.5
    if highway in {"primary", "secondary"}:
        return THEME["road_major"], 1.25
    if highway in {"tertiary", "residential", "living_street"}:
        return THEME["road_minor"], 0.8
    return THEME["road_tiny"], 0.42


def _is_walkway(highway) -> bool:
    targets = {"footway", "pedestrian", "steps", "path", "corridor"}
    if isinstance(highway, list):
        return any(str(item) in targets for item in highway)
    return str(highway) in targets


def _collect_context_points(features, crs) -> list[dict]:
    if features is None or len(features) == 0:
        return []
    data = features[features.geometry.notna()].copy()
    if data.empty:
        return []
    data = data.to_crs(crs)
    points = []
    for _, row in data.iterrows():
        category = _classify_context(row)
        name = row.get("name")
        if category is None or name is None or str(name).strip().lower() in {"", "nan"}:
            continue
        point = row.geometry.representative_point()
        points.append({"x": point.x, "y": point.y, "category": category})
    return points


def _collect_transit_points(features, crs) -> list[dict]:
    if features is None or len(features) == 0:
        return []
    data = features[features.geometry.notna()].copy()
    if data.empty:
        return []
    data = data.to_crs(crs)
    points = []
    for _, row in data.iterrows():
        category = None
        if _value_has(row.get("railway"), {"subway_entrance", "station"}) or _value_has(row.get("public_transport"), {"station"}):
            category = "subway"
        elif _value_has(row.get("highway"), {"bus_stop"}):
            category = "bus"
        if category:
            point = row.geometry.representative_point()
            points.append({"x": point.x, "y": point.y, "category": category})
    return points


def _classify_context(row) -> str | None:
    if _value_has(row.get("amenity"), {"cafe", "bar", "pub", "restaurant", "fast_food"}):
        return "eat_drink"
    if _value_has(row.get("shop"), {"boutique", "clothes", "florist", "books", "antiques", "art"}):
        return "shop"
    if _value_has(row.get("tourism"), {"gallery", "artwork", "attraction"}) or _row_has_any(row, "historic"):
        return "culture"
    return None


def _value_has(value, targets: set[str]) -> bool:
    if isinstance(value, list):
        return any(str(item) in targets for item in value)
    return str(value) in targets


def _thin_points(points: list[dict], min_gap: float, limit: int) -> list[dict]:
    selected = []
    min_gap_squared = min_gap * min_gap
    for point in points:
        if all((point["x"] - kept["x"]) ** 2 + (point["y"] - kept["y"]) ** 2 >= min_gap_squared for kept in selected):
            selected.append(point)
        if len(selected) >= limit:
            break
    return selected


def _screen_angle(ax, x1: float, y1: float, x2: float, y2: float) -> float:
    p1 = ax.transData.transform((x1, y1))
    p2 = ax.transData.transform((x2, y2))
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))


def draw_spots(ax, spots: list[Spot], crs, fonts, placer: LabelPlacer | None = None):
    if not spots:
        return
    gdf = gpd.GeoDataFrame([{"display": spot.display, "category": spot.category, "geometry": Point(spot.lon, spot.lat)} for spot in spots], crs="EPSG:4326").to_crs(crs)
    rows = gdf.reset_index(drop=True)
    number_font = FontProperties(fname=fonts["bold"], size=12) if fonts and fonts.get("bold") else None
    label_font = FontProperties(fname=fonts["bold"], size=10.5) if fonts and fonts.get("bold") else None
    if placer:
        for _, row in rows.iterrows():
            placer.reserve_point(row.geometry.x, row.geometry.y, radius_px=22)
    for idx, row in rows.iterrows():
        color = CATEGORY_COLORS.get(row["category"], "#2B7C8E")
        ax.scatter(row.geometry.x, row.geometry.y, s=320, marker="o", color=color, edgecolors=THEME["panel"], linewidths=2.0, zorder=8)
        ax.annotate(str(idx + 1), xy=(row.geometry.x, row.geometry.y), color="#FFF9ED", fontsize=12, fontproperties=number_font, ha="center", va="center", zorder=9)
        if placer:
            placer.place_annotated(row.geometry.x, row.geometry.y, str(row["display"]), _label_offsets_for_point(ax, row.geometry.x, row.geometry.y), color=THEME["text"], fontsize=10.5, fontproperties=label_font, zorder=10, weight_stroke=3.6)


def draw_park_labels(ax, parks, crs, fonts, placer: LabelPlacer | None = None, limit: int = 8) -> None:
    if parks is None or len(parks) == 0 or "name" not in parks.columns:
        return
    data = parks[parks.geometry.type.isin(["Polygon", "MultiPolygon"]) & parks["name"].notna()].copy()
    if data.empty:
        return
    data = data.to_crs(crs)
    view = box(*ax.get_xlim(), *ax.get_ylim())
    rows = []
    for _, row in data.iterrows():
        geom = row.geometry.intersection(view)
        if not geom.is_empty:
            rows.append((geom.area, str(row["name"]).strip(), geom.representative_point()))
    rows = [(area, name, point) for area, name, point in rows if name and name.lower() != "nan"]
    rows.sort(reverse=True, key=lambda item: item[0])
    font = FontProperties(fname=fonts["bold"], size=12) if fonts and fonts.get("bold") else None
    for _, name, point in rows[:limit]:
        if placer:
            placer.place_text(point.x, point.y, name, color="#6F7252", fontsize=12, fontproperties=font, zorder=6.3, alpha=0.88, stroke=4.2)
        else:
            ax.text(point.x, point.y, name, color="#6F7252", fontsize=12, fontproperties=font, ha="center", va="center", zorder=6.3, alpha=0.88, clip_on=True, path_effects=[path_effects.withStroke(linewidth=4.2, foreground=THEME["bg"])])


def _label_offsets_for_point(ax, x: float, y: float) -> list[tuple[float, float]]:
    sx, sy = ax.transData.transform((x, y))
    bbox = ax.get_window_extent(ax.figure.canvas.get_renderer())
    x_frac = (sx - bbox.x0) / max(bbox.width, 1)
    y_frac = (sy - bbox.y0) / max(bbox.height, 1)
    right = [(14, 9), (22, 0), (18, -12), (34, 14), (44, 0), (34, -18)]
    left = [(-14, 9), (-22, 0), (-18, -12), (-34, 14), (-44, 0), (-34, -18)]
    up = [(0, 22), (14, 18), (-14, 18), (28, 24), (-28, 24), (0, 36)]
    down = [(0, -22), (14, -18), (-14, -18), (28, -24), (-28, -24), (0, -36)]
    preferred = []
    if x_frac > 0.72:
        preferred.extend(left)
    elif x_frac < 0.28:
        preferred.extend(right)
    else:
        preferred.extend(up if y_frac < 0.25 else down if y_frac > 0.78 else right + left + up + down)
    preferred.extend([(62, 0), (-62, 0), (0, 52), (0, -52), (72, 24), (-72, 24), (72, -24), (-72, -24)])
    deduped = []
    seen = set()
    for item in preferred:
        if item not in seen:
            deduped.append(item)
            seen.add(item)
    return deduped


def add_title(ax, fonts):
    title_font = FontProperties(fname=fonts["bold"], size=40) if fonts and fonts.get("bold") else None
    ax.text(0.06, 0.94, "巨富长漫游指南", transform=ax.transAxes, color=THEME["text"], fontproperties=title_font, fontsize=40, ha="left", va="top", zorder=30, path_effects=[path_effects.withStroke(linewidth=5, foreground=THEME["bg"])])


def _index_layout(count: int, start_y: float = INDEX_START_Y) -> list[IndexEntryLayout]:
    if count <= 0:
        return []
    gap = min(INDEX_MAX_ITEM_GAP, max(INDEX_MIN_ITEM_GAP, 0.64 / count))
    return [IndexEntryLayout(INDEX_MARKER_X, INDEX_TEXT_X, start_y - idx * gap, start_y - idx * gap, start_y - idx * gap - INDEX_NOTE_OFFSET) for idx in range(count)]


def add_index(ax, spots: list[Spot], fonts, start_y: float = INDEX_START_Y):
    item_font = FontProperties(fname=fonts["bold"], size=12.4) if fonts and fonts.get("bold") else None
    number_font = FontProperties(fname=fonts["regular"], size=10.2) if fonts and fonts.get("regular") else None
    note_font = FontProperties(fname=fonts["regular"], size=8.8) if fonts and fonts.get("regular") else None
    for idx, (spot, layout) in enumerate(zip(spots, _index_layout(len(spots), start_y=start_y))):
        ax.text(layout.marker_x, layout.marker_y, f"{idx + 1:02d}", transform=ax.transAxes, color=THEME["muted"], fontproperties=number_font, fontsize=10.2, ha="center", va="center", zorder=31, bbox={"boxstyle": "square,pad=0.14", "facecolor": THEME["panel"], "edgecolor": "#B8AA95", "linewidth": 0.8})
        ax.text(layout.text_x, layout.name_y, spot.display, transform=ax.transAxes, color=THEME["text"], fontproperties=item_font, fontsize=12.4, ha="left", va="center", zorder=31, path_effects=[path_effects.withStroke(linewidth=3.4, foreground=THEME["bg"])])
        ax.text(layout.text_x, layout.note_y, spot.note, transform=ax.transAxes, color=THEME["muted"], fontproperties=note_font, fontsize=8.8, ha="left", va="center", zorder=31, path_effects=[path_effects.withStroke(linewidth=3, foreground=THEME["bg"])])


def add_footer(ax, fonts):
    footer_font = FontProperties(fname=fonts["regular"], size=8) if fonts and fonts.get("regular") else None
    ax.text(0.94, 0.045, "POI: AMap GCJ-02 -> WGS84 | Basemap: OpenStreetMap / OSMnx", transform=ax.transAxes, color=THEME["muted"], fontproperties=footer_font, fontsize=8, ha="right", va="bottom", zorder=30)


if __name__ == "__main__":
    main()