<div align="center">

# 🗺️ Map Creator

### 商用级城市打卡地图生成 Skill

将城市、地点列表或 POI 数据转换为可复查的 GIS 地图，并可进一步生成风格化地图海报。

<p>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-2ea44f.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  <img alt="Codex Ready" src="https://img.shields.io/badge/Codex-Ready-111111.svg">
</p>

<p>
  <a href="#核心能力">核心能力</a> ·
  <a href="#生成效果">生成效果</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#使用方式">使用方式</a> ·
  <a href="#配置">配置</a> ·
  <a href="#项目结构">项目结构</a>
</p>

</div>

![长宁工业记忆打卡地图](docs/images/changning-industrial-memory-map.jpg)

> 从地点解析、坐标校正和 GIS 渲染，到 GPT Image 风格化输出，Map Creator 提供一条可复查、可复用的城市导览地图制作流程。

## 它解决什么问题

制作一张城市导览地图，通常需要反复处理地点检索、坐标系转换、地图数据下载、道路与建筑渲染以及视觉风格统一。Map Creator 把这些步骤组织成适合 Codex / Agent 调用的工具链，同时保留中间 POI 数据，方便人工检查和修正。

## 核心能力

| 能力 | 说明 |
| --- | --- |
| 地点解析 | 根据城市和地点名查询 POI，并保留地址、区县、候选结果与置信度 |
| 坐标对齐 | 将高德返回的 GCJ-02 坐标转换为 WGS84，以匹配 OpenStreetMap |
| GIS 渲染 | 使用 OSMnx / OpenStreetMap 绘制路网、建筑、公园、水体和地点标记 |
| 数据复查 | 将解析结果保存为 POI JSON，可在正式渲染前人工确认 |
| 海报风格化 | 可选用 GPT Image 将 GIS 草稿转换为手绘风等视觉海报 |
| 本地缓存 | 缓存 OSM 数据，减少相同区域重复生成时的网络请求 |

## 生成效果

### 巨富长漫游指南

![巨富长漫游指南](docs/images/jufuchang-walking-guide.png)

## 工作流程

```text
城市 + 地点列表 / POI JSON
            |
            v
     地点解析与坐标转换
            |
            v
      OpenStreetMap GIS 草稿
            |
            v
   GPT Image 风格化（可选）
            |
            v
       城市导览地图海报
```

## 快速开始

### 1. 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `config.example.json` 为 `config.local.json`，然后填写需要使用的服务：

```json
{
  "amap": {
    "api_key": "你的高德地图 Web 服务 API Key",
    "timeout": 12
  },
  "gpt_image": {
    "api_key": "你的 OpenAI API Key",
    "model": "gpt-image-2",
    "endpoint": "https://api.openai.com/v1/images/edits",
    "template": "prompts/map_style_templates/01_手绘风城市导览地图.md",
    "output_dir": "outputs/stylized",
    "output_format": "png",
    "size": "1536x1024",
    "timeout": 120
  }
}
```

也可以使用环境变量：

```powershell
$env:AMAP_KEY="你的高德 key"
$env:OPENAI_API_KEY="你的 OpenAI key"
```

`config.local.json` 已被 `.gitignore` 忽略，请勿提交真实 API Key。

### 3. 生成地图

```bash
python -m guide_maps.cli.create_gis_map --city 上海 --places "SLAB TOWN" "村口大树" "ALWAYS Coffee&Bar" --title "上海街区导览地图"
```

地图草稿默认输出到 `outputs/posters/`。

## 使用方式

### 从已有 POI JSON 生成地图

```bash
python -m guide_maps.cli.create_gis_map --city 上海 --poi-json guide_maps/examples/sample_pois.json --title "巨富长漫游指南"
```

### 解析地点并保存 POI JSON

```bash
python -m guide_maps.cli.create_gis_map --city 南京 --places "地点1" "地点2" --title "南京小酒馆地图" --save-poi-json outputs/poi_sets/nanjing_bars.json
```

也可以只进行地点解析：

```bash
python -m guide_maps.cli.resolve_pois --city 南京 --names "地点1" "地点2" --output outputs/poi_sets/nanjing.json
```

POI JSON 会保留输入名、解析名、地址、区县、候选结果、置信度、GCJ-02 坐标和 WGS84 坐标。

### 控制道路名称

提示需要重点显示的道路名，但不将它们作为白名单：

```bash
python -m guide_maps.cli.create_gis_map --city 南京 --poi-json outputs/poi_sets/nanjing_bars.json --title "南京小酒馆地图" --road-labels 长江路 石鼓路 应天大街
```

关闭道路名称：

```bash
python -m guide_maps.cli.create_gis_map --city 南京 --poi-json outputs/poi_sets/nanjing_bars.json --title "南京小酒馆地图" --no-road-labels
```

### 使用 GPT Image 风格化

```bash
python -m guide_maps.cli.style_poster_with_gpt_image --input outputs/posters/<draft>.png
```

指定变量和风格模板：

```bash
python -m guide_maps.cli.style_poster_with_gpt_image --input outputs/posters/<draft>.png --vars outputs/stylized/prompt_dry_runs/vars.json --template prompts/map_style_templates/01_手绘风城市导览地图.md
```

没有 GPT Image API Key 时，GIS 草稿仍然可以正常生成。

## 配置

运行目录可以使用以下环境变量覆盖：

| 环境变量 | 用途 |
| --- | --- |
| `MAP_CREATOR_CACHE_DIR` | OSM 和解析缓存目录 |
| `MAP_CREATOR_OUTPUTS_DIR` | 总输出目录 |
| `MAP_CREATOR_POSTERS_DIR` | GIS 草稿目录 |
| `MAP_CREATOR_STYLIZED_DIR` | 风格化地图目录 |
| `MAP_CREATOR_POI_SETS_DIR` | POI JSON 目录 |

旧的 `OPEN_GUIDE_MAPS_*` 环境变量仍然兼容。

Windows PowerShell 如果中文输出乱码，可以先设置：

```powershell
chcp 65001
$env:PYTHONIOENCODING="utf-8"
```

## OSM 数据和运行速度

地图渲染需要访问 Overpass API，中国大陆网络访问 Overpass 时可能较慢。当前实现会：

- 单独请求一次路网 `graph_from_point()`。
- 将建筑、公园、水体、生活方式 POI 和交通点等 `features_from_point()` 合并为一次请求，再在本地拆分图层。
- 使用 `cache/` 缓存 OSM 数据，同一区域再次生成时通常会更快。

删除 `cache/` 后，下次生成会重新联网获取 OSM 数据。

## 项目结构

```text
map-creator/
|-- README.md                         # 项目说明
|-- LICENSE                           # MIT License
|-- SKILL.md                          # 给 Codex / Agent 使用的操作说明
|-- config.example.json               # 配置模板，不包含真实 Key
|-- requirements.txt                  # Python 依赖
|-- docs/images/                      # README 展示图片
|-- guide_maps/
|   |-- cli/                          # 命令入口
|   |-- core/                         # 配置、缓存、字体和通用工具
|   |-- geocoding/                    # 地点解析、坐标转换和 POI 数据结构
|   |-- rendering/                    # OSM / GIS 地图渲染
|   |-- styling/                      # GPT Image 和本地风格预览
|   `-- examples/                     # 示例 POI 数据
|-- prompts/                          # 地图风格提示词模板
|-- tests/                            # 自动化测试
|-- cache/                            # 运行缓存，可删除
`-- outputs/                          # 运行输出，可删除
```

常见输出目录：

```text
outputs/posters/
outputs/stylized/
outputs/poi_sets/
```

## 测试

```bash
python -m compileall guide_maps tests
python -m pytest tests
```

如果 pytest 在系统临时目录没有权限，可以将临时目录放到项目中：

```powershell
$env:TMP="$PWD\.tmp"
$env:TEMP=$env:TMP
python -m pytest tests
```

当前测试覆盖 POI 解析、坐标转换、地图范围、道路名筛选、OSM feature 合并拆分、GPT Image 提示词和风格预览生成。

## License

本项目基于 [MIT License](LICENSE) 开源。

Copyright © 2026 [Hatari130](https://github.com/Hatari130)
