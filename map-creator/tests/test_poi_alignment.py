from guide_maps.geocoding.poi_alignment import compute_frame_bounds, validate_alignment


def test_alignment_frame_contains_valid_nanjing_pois():
    pois = [
        {
            "input_name": "\u5c0f\u9690\u9152\u9986",
            "resolved_name": "\u5c0f\u9690\u9152\u9986",
            "lng_wgs84": 118.7898,
            "lat_wgs84": 32.0418,
        },
        {
            "input_name": "\u65b0\u8857\u53e3",
            "resolved_name": "\u65b0\u8857\u53e3",
            "lng_wgs84": 118.7788,
            "lat_wgs84": 32.0412,
        },
    ]

    frame = compute_frame_bounds(pois, padding_m=800, min_width_m=2500, min_height_m=1800)
    results, _ = validate_alignment(pois, city="\u5357\u4eac", frame=frame, fetch_roads=False)

    assert all(result.in_frame for result in results)
    assert all(result.city_bounds_ok for result in results)
    assert all(result.status == "ok" for result in results)


def test_alignment_flags_out_of_city_coordinate():
    pois = [
        {
            "input_name": "\u9519\u8bef\u70b9",
            "resolved_name": "\u9519\u8bef\u70b9",
            "lng_wgs84": 121.48,
            "lat_wgs84": 31.23,
        }
    ]

    frame = compute_frame_bounds(pois, padding_m=800)
    results, _ = validate_alignment(pois, city="\u5357\u4eac", frame=frame, fetch_roads=False)

    assert results[0].status == "error"
    assert results[0].city_bounds_ok is False
    assert results[0].issues[0].code == "outside_city_bounds"
