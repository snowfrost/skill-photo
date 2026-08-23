# Make Photo Stamp Archive

[简体中文](README.md) · **English** · [日本語](README.ja.md)

Make Photo Stamp Archive is a Codex Skill that turns one or more supplied photos into quiet archival composites: a faithfully preserved photograph joined directly to a warm-white paper panel with a compact, subject-specific hand-pressed seal.

The callable skill name is `make-photo-stamp-archive`.

## Core Capabilities

- Preserves the source photograph, including people, faces, objects, architecture, text, color relationships, and scene logic.
- Uses a clean, straight direct splice—landscape left/right by default, with top/bottom layouts available on request.
- Designs circular, square-framed, panoramic, arched, or custom-silhouette seals around the source subject.
- Renders tactile dry ink, worn halftone, uneven pressure, broken edges, and restrained registration error.
- Supports focused revisions to seal shape, border, scale, position, ink color, caption, paper age, and splice orientation.
- Produces one independent finished composite for each supplied photo.

## Visual System

- **Photo panel:** faithful and realistic, approximately 55% of the default canvas.
- **Paper panel:** clean warm off-white stock with subtle fibers and light scan residue, approximately 45% of the canvas.
- **Seal group:** compact and corner-positioned, occupying about 30% of the paper panel.
- **Negative space:** roughly 70% of the paper panel remains quiet and empty.
- **Caption:** small faded typewriter text placed near the seal, never over it.
- **Mood:** restrained, graphic, tactile, archival, and memory-like.

The result is always one flat composite—not a book mockup, scrapbook, before/after board, pasted miniature photograph, or decorative poster presentation.

## Examples

| Example 01 | Example 02 |
| --- | --- |
| ![Archival photo and stamp composite 01](https://github.com/user-attachments/assets/5fd44aba-e5f1-4f24-9271-89e850f171c5) | ![Archival photo and stamp composite 02](https://github.com/user-attachments/assets/27fb0c46-d67f-4404-bbaf-e73e27f8202c) |

| Example 03 |
| --- |
| ![Archival photo and stamp composite 03](https://github.com/user-attachments/assets/9515aac2-448b-4426-ad34-70b88edc590a) |

## Requirements

- Codex or another Skill-compatible runtime.
- Image-reading capability for inspecting source photos.
- Image generation or editing capability for producing and revising the final composite.

No API key, external font, script, or additional runtime asset is included in this Skill package. Final image quality and source-photo fidelity depend on the image model available in the host environment.

## Installation

```bash
git clone https://github.com/Dlcccc71913/skill-make-photo-stamp-archive.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill-make-photo-stamp-archive \
  "${CODEX_HOME:-$HOME/.codex}/skills/make-photo-stamp-archive"
```

Restart Codex if the Skill does not appear immediately.

## Usage

```text
Use $make-photo-stamp-archive to turn this photo into a direct-splice archival artwork with a custom seal.
```

For a focused revision:

```text
Keep the photo panel unchanged. Make only the seal 10% smaller and move it to the upper-right corner.
```

## Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── prompt-template.md
├── README.md
├── README.en.md
├── README.ja.md
└── LICENSE
```

## License

[MIT](LICENSE)
