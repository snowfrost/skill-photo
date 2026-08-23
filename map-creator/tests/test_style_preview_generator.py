from pathlib import Path

from PIL import Image

from guide_maps.styling.generate_style_previews import generate_previews


def test_generate_previews_writes_ten_same_size_images(tmp_path):
    source = tmp_path / "source.png"
    Image.new("RGB", (320, 180), (240, 234, 220)).save(source)

    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    for index in range(2, 12):
        (template_dir / f"{index:02d}_style.md").write_text("prompt", encoding="utf-8")

    output_dir = tmp_path / "previews"
    outputs = generate_previews(source, template_dir, output_dir)

    assert len(outputs) == 10
    assert [path.name for path in outputs] == [f"{index:02d}_style.png" for index in range(2, 12)]
    for path in outputs:
        assert path.exists()
        with Image.open(path) as image:
            assert image.size == (320, 180)
