from pathlib import Path
import json

from guide_maps.styling.gpt_image import default_output_path, render_prompt, style_poster


TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "prompts" / "map_style_templates"
EXPECTED_TEMPLATE_NAMES = [
    "01_手绘风城市导览地图.md",
    "02_赛博朋克霓虹导览地图.md",
    "03_游戏任务关卡地图.md",
    "04_复古探险手册地图.md",
    "05_蓝图工程手绘地图.md",
    "06_日本城市漫游地图.md",
    "07_像素游戏导览地图.md",
    "08_夜游灯光路线地图.md",
    "09_户外徒步等高线地图.md",
    "10_艺术展览策展地图.md",
    "11_极简信息图导览地图.md",
]


def test_render_prompt_replaces_variables(tmp_path):
    template = tmp_path / "template.md"
    template.write_text("Title: {title}\nPlaces:\n{places}\nMeta: {meta}", encoding="utf-8")

    prompt = render_prompt(template, {"title": "南京导览", "places": ["1 小隐", "2 静海寺"], "meta": {"city": "南京"}})

    assert "Title: 南京导览" in prompt
    assert "1 小隐\n2 静海寺" in prompt
    assert '"city": "南京"' in prompt


def test_render_prompt_only_replaces_variables(tmp_path):
    template = tmp_path / "template.md"
    template.write_text("Style stays.\nPlaces: {places}", encoding="utf-8")

    prompt = render_prompt(template, {"places": ["1 小隐"]})

    assert prompt.startswith("Style stays.")
    assert "Places: 1 小隐" in prompt


def test_map_style_templates_include_default_and_ten_style_variants():
    templates = sorted(path.name for path in TEMPLATE_DIR.glob("*.md") if path.name != "README.md")

    assert templates == EXPECTED_TEMPLATE_NAMES


def test_main_map_style_prompt_has_spatial_controls():
    prompt = (TEMPLATE_DIR / "01_手绘风城市导览地图.md").read_text(encoding="utf-8")

    assert "OSM / GIS" in prompt
    assert "{地图主题}" in prompt
    assert "{点位清单}" in prompt
    assert "{重点道路}" in prompt
    assert "{区域标签}" in prompt


def test_all_map_style_prompts_are_generic_and_render_variables():
    variables = {
        "地图主题": "南京咖啡漫游地图",
        "点位清单": ["1 小隐咖啡", "2 梧桐书店"],
        "重点道路": ["中山路", "汉口路"],
        "区域标签": ["玄武湖"],
    }

    for name in EXPECTED_TEMPLATE_NAMES:
        prompt = render_prompt(TEMPLATE_DIR / name, variables)
        assert "南京咖啡漫游地图" in prompt
        assert "1 小隐咖啡\n2 梧桐书店" in prompt
        assert "中山路\n汉口路" in prompt
        assert "玄武湖" in prompt
        assert "{地图主题}" not in prompt
        assert "{点位清单}" not in prompt


def test_missing_key_returns_without_prompt_variables(tmp_path, monkeypatch):
    image = tmp_path / "poster.png"
    image.write_bytes(b"not-a-real-image")
    template = tmp_path / "template.md"
    template.write_text("{title}", encoding="utf-8")
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"template": str(template), "output_dir": str(tmp_path / "styled")}), encoding="utf-8")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GPT_IMAGE_API_KEY", raising=False)

    result = style_poster(image, config_path=config)

    assert result.status == "missing_key"
    assert result.input_path == image.resolve()


def test_dry_run_writes_prompt_when_key_present(tmp_path, monkeypatch):
    image = tmp_path / "poster.png"
    image.write_bytes(b"not-a-real-image")
    template = tmp_path / "template.md"
    template.write_text("Title: {title}", encoding="utf-8")
    variables = tmp_path / "vars.json"
    variables.write_text(json.dumps({"title": "巨富长漫游指南"}, ensure_ascii=False), encoding="utf-8")
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"template": str(template), "output_dir": str(tmp_path / "styled")}), encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    result = style_poster(image, variables_path=variables, config_path=config, dry_run=True)

    assert result.status == "dry_run"
    assert result.prompt_path is not None
    assert "巨富长漫游指南" in result.prompt_path.read_text(encoding="utf-8")


def test_style_poster_reads_variables_with_utf8_bom(tmp_path, monkeypatch):
    image = tmp_path / "poster.png"
    image.write_bytes(b"not-a-real-image")
    template = tmp_path / "template.md"
    template.write_text("Title: {title}", encoding="utf-8")
    variables = tmp_path / "vars.json"
    variables.write_text(json.dumps({"title": "带 BOM 的变量"}, ensure_ascii=False), encoding="utf-8-sig")
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"template": str(template), "output_dir": str(tmp_path / "styled")}), encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    result = style_poster(image, variables_path=variables, config_path=config, dry_run=True)

    assert result.status == "dry_run"
    assert result.prompt_path is not None
    assert "带 BOM 的变量" in result.prompt_path.read_text(encoding="utf-8")


def test_style_poster_writes_image_and_sidecar(tmp_path, monkeypatch):
    image = tmp_path / "poster.png"
    image.write_bytes(b"not-a-real-image")
    template = tmp_path / "template.md"
    template.write_text("Title: {title}", encoding="utf-8")
    variables = tmp_path / "vars.json"
    variables.write_text(json.dumps({"title": "巨富长漫游指南"}, ensure_ascii=False), encoding="utf-8")
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps({"template": str(template), "output_dir": str(tmp_path / "styled"), "output_format": "png"}),
        encoding="utf-8",
    )
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(
        "guide_maps.styling.gpt_image.request_image_edit",
        lambda input_path, prompt, config, api_key: b"styled-image",
    )

    result = style_poster(image, variables_path=variables, config_path=config)

    assert result.status == "styled"
    assert result.output_path is not None
    assert result.output_path.read_bytes() == b"styled-image"
    assert result.sidecar_path is not None
    sidecar = json.loads(result.sidecar_path.read_text(encoding="utf-8"))
    assert sidecar["input_path"] == str(image.resolve())
    assert sidecar["model"] == "gpt-image-2"


def test_default_output_path_uses_input_and_template_names(tmp_path):
    output = default_output_path(
        tmp_path / "poster.png",
        tmp_path / "01_手绘风城市导览地图.md",
        tmp_path / "styled",
        "png",
    )

    assert output.name == "poster__01_手绘风城市导览地图.png"