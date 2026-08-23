from guide_maps.geocoding.amap_cli_client import _candidate_from_item, _extract_items


def test_extract_items_accepts_common_cli_shapes():
    assert _extract_items({"pois": [{"name": "小隐酒馆"}]}) == [{"name": "小隐酒馆"}]
    assert _extract_items({"data": [{"name": "星巴克"}]}) == [{"name": "星巴克"}]


def test_candidate_from_cli_item_parses_gcj02_location():
    candidate = _candidate_from_item(
        {
            "id": "poi-1",
            "name": "小隐酒馆",
            "address": "科巷1号",
            "city": "南京市",
            "district": "秦淮区",
            "type": "体育休闲服务;娱乐场所;酒吧",
            "location": {"lng": 118.795041, "lat": 32.039812},
        }
    )

    assert candidate is not None
    assert candidate.name == "小隐酒馆"
    assert candidate.city == "南京市"
    assert candidate.lng_gcj02 == 118.795041
    assert candidate.lat_gcj02 == 32.039812
