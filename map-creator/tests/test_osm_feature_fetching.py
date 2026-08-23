import geopandas as gpd
from shapely.geometry import Point

from guide_maps.rendering import osm_context_style as style


def test_combined_osm_features_can_be_split_by_layer():
    features = gpd.GeoDataFrame(
        [
            {"building": "yes", "geometry": Point(0, 0)},
            {"leisure": "park", "geometry": Point(1, 1)},
            {"natural": "water", "geometry": Point(2, 2)},
            {"amenity": "cafe", "geometry": Point(3, 3)},
            {"railway": "subway_entrance", "geometry": Point(4, 4)},
        ],
        crs="EPSG:4326",
    )

    assert len(style.select_buildings(features)) == 1
    assert len(style.select_parks(features)) == 1
    assert len(style.select_water(features)) == 1
    assert len(style.select_lifestyle(features)) == 1
    assert len(style.select_transit(features)) == 1


def test_fetch_map_features_combines_tags(monkeypatch):
    calls = []

    def fake_fetch(point, dist, tags, key):
        calls.append((point, dist, tags, key))
        return "features"

    monkeypatch.setattr(style, "fetch_features", fake_fetch)

    result = style.fetch_map_features((31.2, 121.4), 1200, include_lifestyle=True, include_transit=True)

    assert result == "features"
    assert len(calls) == 1
    _, _, tags, key = calls[0]
    assert tags["building"] is True
    assert "amenity" in tags
    assert "railway" in tags
    assert key == "map_features_lifestyle_transit"