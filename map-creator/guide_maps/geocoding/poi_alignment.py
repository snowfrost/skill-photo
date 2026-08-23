"""POI frame and alignment checks."""

from __future__ import annotations

from dataclasses import dataclass, field

import geopandas as gpd
from shapely.geometry import Point, box


CITY_BOUNDS = {
    "南京": (118.30, 31.55, 119.25, 32.45),
    "南京市": (118.30, 31.55, 119.25, 32.45),
    "上海": (120.85, 30.65, 122.20, 31.90),
    "上海市": (120.85, 30.65, 122.20, 31.90),
}


@dataclass
class AlignmentIssue:
    code: str
    message: str


@dataclass
class AlignmentResult:
    input_name: str
    status: str
    in_frame: bool
    city_bounds_ok: bool
    issues: list[AlignmentIssue] = field(default_factory=list)


def compute_frame_bounds(pois: list[dict], padding_m: int = 800, min_width_m: int = 1800, min_height_m: int = 1400):
    valid = [poi for poi in pois if poi.get("lng_wgs84") is not None and poi.get("lat_wgs84") is not None]
    if not valid:
        raise ValueError("No valid POI coordinates")
    gdf = gpd.GeoDataFrame(
        [{"geometry": Point(float(poi["lng_wgs84"]), float(poi["lat_wgs84"]))} for poi in valid],
        crs="EPSG:4326",
    )
    projected = gdf.to_crs(gdf.estimate_utm_crs())
    minx, miny, maxx, maxy = projected.total_bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    width = max(maxx - minx + padding_m * 2, min_width_m)
    height = max(maxy - miny + padding_m * 2, min_height_m)
    frame = box(cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2)
    return gpd.GeoSeries([frame], crs=projected.crs).to_crs("EPSG:4326").iloc[0]


def validate_alignment(pois: list[dict], city: str, frame, fetch_roads: bool = False):
    bounds = CITY_BOUNDS.get(city)
    results: list[AlignmentResult] = []
    for poi in pois:
        name = str(poi.get("input_name") or poi.get("resolved_name") or "")
        lng = poi.get("lng_wgs84")
        lat = poi.get("lat_wgs84")
        issues: list[AlignmentIssue] = []
        if lng is None or lat is None:
            issues.append(AlignmentIssue("missing_coordinate", "Missing WGS84 coordinate"))
            results.append(AlignmentResult(name, "error", False, False, issues))
            continue
        point = Point(float(lng), float(lat))
        in_frame = frame.contains(point) or frame.touches(point)
        if not in_frame:
            issues.append(AlignmentIssue("outside_frame", "POI is outside the render frame"))
        city_ok = True
        if bounds is not None:
            min_lng, min_lat, max_lng, max_lat = bounds
            city_ok = min_lng <= float(lng) <= max_lng and min_lat <= float(lat) <= max_lat
            if not city_ok:
                issues.append(AlignmentIssue("outside_city_bounds", "POI is outside expected city bounds"))
        results.append(AlignmentResult(name, "ok" if not issues else "error", in_frame, city_ok, issues))
    return results, None
