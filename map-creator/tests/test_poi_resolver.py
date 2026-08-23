from guide_maps.geocoding.poi_resolver import POIResolver
from guide_maps.geocoding.schemas import AMapPOICandidate


class FakeAMapClient:
    def search_text(self, keyword, city):
        return [
            AMapPOICandidate(
                poi_id="wrong-city",
                name="\u5c0f\u9690\u9152\u9986",
                address="\u4e0a\u6d77\u5e02\u9ec4\u6d66\u533a\u6d4b\u8bd5\u8def",
                province="\u4e0a\u6d77\u5e02",
                city="\u4e0a\u6d77\u5e02",
                district="\u9ec4\u6d66\u533a",
                type="\u9910\u996e\u670d\u52a1;\u9152\u5427;\u9152\u5427",
                typecode="050500",
                lng_gcj02=121.48,
                lat_gcj02=31.23,
            ),
            AMapPOICandidate(
                poi_id="right-one",
                name="\u5c0f\u9690\u9152\u9986(\u5357\u4eac\u5e97)",
                address="\u5357\u4eac\u5e02\u79e6\u6dee\u533a\u6d4b\u8bd5\u8def",
                province="\u6c5f\u82cf\u7701",
                city="\u5357\u4eac\u5e02",
                district="\u79e6\u6dee\u533a",
                type="\u9910\u996e\u670d\u52a1;\u9152\u5427;\u9152\u5427",
                typecode="050500",
                lng_gcj02=118.78,
                lat_gcj02=32.04,
            ),
        ]


def test_resolver_prefers_city_limited_candidate_and_converts_coordinates():
    resolved = POIResolver(FakeAMapClient()).resolve_one("\u5c0f\u9690\u9152\u9986", city="\u5357\u4eac")

    assert resolved.poi_id == "right-one"
    assert resolved.lng_gcj02 == 118.78
    assert resolved.lat_gcj02 == 32.04
    assert resolved.lng_wgs84 is not None
    assert resolved.lat_wgs84 is not None
    assert abs(resolved.lng_wgs84 - resolved.lng_gcj02) > 0.001
    assert resolved.status in {"resolved", "resolved_review"}
