import geopandas as gpd
from shapely.geometry import LineString, box

from guide_maps.rendering.osm_context_style import _rank_road_label_candidates, _road_label_anchor


def test_road_label_anchor_avoids_intersection_vertex():
    line = LineString([(0, 0), (0, 100), (0, 200)])

    point, before, after = _road_label_anchor(line)

    assert abs(point.y - 100) >= 40
    assert before.x == after.x == point.x
    assert before.y < point.y < after.y


def test_road_label_anchor_uses_long_parallel_segment():
    line = LineString([(0, 0), (40, 0), (40, 220), (120, 220)])

    point, before, after = _road_label_anchor(line)

    assert point.x == 40
    assert before.x == after.x == 40
    assert before.y < point.y < after.y


def test_large_map_auto_labels_are_not_manual_whitelist():
    edges = gpd.GeoDataFrame(
        [
            {"name": "短路", "highway": "secondary", "geometry": LineString([(0, 0), (400, 0)])},
            {"name": "主路", "highway": "primary", "geometry": LineString([(0, 10), (2000, 10)])},
            {"name": "小巷", "highway": "residential", "geometry": LineString([(0, 20), (3000, 20)])},
        ],
        crs="EPSG:3857",
    )

    candidates = _rank_road_label_candidates(edges, box(-10, -10, 2500, 100), ["短路"], limit=2, large_map=True)
    names = [candidate.name for candidate in candidates[:2]]

    assert "主路" in names
    assert "短路" in names
    assert "小巷" not in names


def test_manual_road_labels_boost_ranking_without_excluding_others():
    edges = gpd.GeoDataFrame(
        [
            {"name": "长路", "highway": "tertiary", "geometry": LineString([(0, 0), (1000, 0)])},
            {"name": "提示路", "highway": "tertiary", "geometry": LineString([(0, 10), (900, 10)])},
            {"name": "次选路", "highway": "tertiary", "geometry": LineString([(0, 20), (700, 20)])},
        ],
        crs="EPSG:3857",
    )

    candidates = _rank_road_label_candidates(edges, box(-10, -10, 1200, 100), ["提示路"], limit=3, large_map=True)
    names = [candidate.name for candidate in candidates[:3]]

    assert names[0] == "提示路"
    assert "长路" in names


def test_large_map_skips_expressway_and_line_names():
    edges = gpd.GeoDataFrame(
        [
            {"name": "内环南线", "highway": "primary", "geometry": LineString([(0, 0), (2200, 0)])},
            {"name": "清凉门隧道", "highway": "primary", "geometry": LineString([(0, 10), (1800, 10)])},
            {"name": "集庆门大街", "highway": "primary", "geometry": LineString([(0, 20), (1200, 20)])},
        ],
        crs="EPSG:3857",
    )

    candidates = _rank_road_label_candidates(edges, box(-10, -10, 2500, 100), [], limit=3, large_map=True)
    names = [candidate.name for candidate in candidates]

    assert names == ["集庆门大街"]