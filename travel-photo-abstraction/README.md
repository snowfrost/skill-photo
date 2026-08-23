# Travel Photo Abstraction Skill

A Codex skill that analyzes a travel or everyday photograph as a visual system, then turns its most distinctive shapes, counts, positions, proportions, colors, directions, depth, and spatial rhythm into a sparse editorial abstraction.

The repository includes the bundled reference library used by the skill and a separate set of watermarked showcase outputs. Users provide their own source photographs when running the skill.

## What it does

- inventories observable visual evidence before generation;
- maps each retained source fact to a minimal abstract mark;
- preserves spatial relationships, asymmetry, occlusion, count groups, and negative space;
- slightly favors distinct source-sampled accent colors when they clarify different visual facts;
- generates a CLEAN abstract panel as a temporary asset, then uses a fail-closed finalizer to compose and pixel-verify the untouched original photograph;
- avoids generic filters, decorative filler, and invented visual content.

## Showcase

The examples below demonstrate different kinds of visual evidence the skill can preserve. During generation, the skill selects 2–4 structurally relevant examples from all 19 bundled references using `references/structural-reference-index.md`. Their relationship logic is binding; obsolete texture, grading, text, and proportions are not.

### Form and silhouette

Reduce a distinctive subject to the smallest recognizable mass, contour, axis, and accent while preserving its position and scale.

| Isolated form | Architectural silhouette | Stable structure + transient light |
|:---:|:---:|:---:|
| ![A hot-air balloon reduced to nested circular color fields](showcase/sky-balloon.png) | ![A harbour vessel reduced to a dark silhouette and reflected strokes](showcase/harbour-silhouette.png) | ![A night castle and fireworks reduced to a stable silhouette and crossing light paths](showcase/night-castle.png) |

### Repetition and spatial rhythm

Preserve count groups, uneven intervals, density, depth, motion, and color ratios rather than turning repeated subjects into a regular pattern.

| Quiet crossings | Bloom veil | Cross current |
|:---:|:---:|:---:|
| ![Several lake boats preserved through their relative positions, scales, and reflections](showcase/quiet-crossings.png) | ![A bouquet reduced to layered color masses, stems, and small accents](showcase/bloom-veil.png) | ![A dense school of fish sampled into directional repeated marks](showcase/cross-current.png) |

### Space, viewpoint, and atmosphere

Let negative space carry the composition while retaining the source horizon, focal coordinates, directional lines, and human scale.

| City below | Rocky coast | Winter tower |
|:---:|:---:|:---:|
| ![A city viewpoint reduced to horizon arcs, tower axis, skyline marks, and a bench](showcase/city-below.png) | ![A coastal fishing scene reduced to horizon bands, figure, rocks, and rod diagonals](showcase/rocky-coast.png) | ![A winter tower and crowd reduced to tiered roof strokes and irregular human marks](showcase/winter-tower.png) |

## Requirements

- Codex with skill support;
- access to the built-in image generation tool;
- Python with Pillow for objective output checks (recommended; the visual review remains mandatory);
- a photograph that you have the right to use.

The skill deliberately stops when the built-in image generation tool is unavailable. Pillow is used only for deterministic composition, exact microtype, and validation—never to draw the abstract motif.

## Install

Download or clone this repository, then copy the `travel-photo-abstraction` folder into your Codex skills directory.

```bash
git clone https://github.com/Evianis/travel-photo-abstraction.git
```

Windows PowerShell:

```powershell
Copy-Item -Recurse ".\travel-photo-abstraction" "$env:USERPROFILE\.codex\skills\travel-photo-abstraction"
```

macOS or Linux:

```bash
cp -R ./travel-photo-abstraction ~/.codex/skills/travel-photo-abstraction
```

Start a new Codex task after installation so the skill can be discovered.

Verify that the complete reference library was installed:

```bash
python travel-photo-abstraction/scripts/check_installation.py travel-photo-abstraction
```

Finalize an artwork with mandatory original-photo validation:

```bash
python travel-photo-abstraction/scripts/finalize_artwork.py original.jpg abstract-panel.png final.png --number "NO. 001" --date "03 AUG 2026" --phrase "QUIET STRUCTURE"
```

## Example prompt

```text
Use $travel-photo-abstraction to analyze my uploaded photograph. Map its most distinctive observable facts to minimal abstract marks, then generate a faithful photo-plus-abstraction editorial study.
```

中文示例：

```text
使用 $travel-photo-abstraction 分析我上传的照片。先把最有辨识度的视觉事实映射为极简抽象符号，再生成照片与抽象图形组合图。
```

## Repository contents

```text
travel-photo-abstraction/
├── SKILL.md
├── agents/openai.yaml
├── assets/style-references/
│   └── memory-reference-* (19-image structural library)
├── scripts/
│   ├── check_installation.py
│   ├── compose_artwork.py
│   ├── finalize_artwork.py
│   └── validate_output.py
└── references/
    ├── analysis-method.md
    ├── structural-reference-index.md
    ├── run-log-template.md
    └── style-guide.md

showcase/
└── watermarked output examples
```

## License

This project is source-available, not open source under the OSI definition. You may install and use an unmodified copy. Modification, derivative works, redistribution, republication, sublicensing, and resale are prohibited. See [LICENSE](LICENSE).

The license does not claim ownership of photographs supplied by users or of generated outputs. Rights in those materials remain subject to their respective owners and applicable platform terms.

The showcase images are provided only as examples of this project's output. Their embedded repository watermark must not be removed.
