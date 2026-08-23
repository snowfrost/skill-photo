from guide_maps.geocoding.workflow import read_place_names


def test_read_place_names_merges_file_and_args_with_dedupe(tmp_path):
    names_file = tmp_path / "places.txt"
    names_file.write_text("\n# comment\nSLAB TOWN\nAlways Coffee\n", encoding="utf-8")

    names = read_place_names(["slab town", "Village Bar", ""], names_file)

    assert names == ["SLAB TOWN", "Always Coffee", "Village Bar"]
