---
name: theme-editable-journal
description: Generate theme-matched, editable electronic journal/Plog pages from user photo folders for Xiaohongshu/Rednote or personal travel albums. Use when the user provides museum, gallery, zoo, exhibition, city travel, parent-child outing, lifestyle, or non-child travel photos and wants an aesthetic HTML hand-account/poster that automatically matches the photo theme, supports user editing, photo replacement, drag/rotate/scale/crop controls, adding/deleting text or image-text modules, dynamic timeline extension, and WYSIWYG PNG download.
---

# Theme Editable Journal

Create a browser-editable electronic journal from a photo folder. The default deliverable is an HTML app plus local assets that the user can adjust and export as a PNG.

## Workflow

1. Inspect the photos before designing.
   - Use `scripts/photo_inventory.py <photo-folder> --out <work-dir>` to produce a CSV and contact sheet.
   - Reject blurred, low-resolution, screenshot-like, cluttered, or subject-missing photos.
   - Classify usable photos as large scene, person observing, detail, transition, or cover.

2. Choose the visual route from the photo theme.
   - Read `references/style-routing.md` for palette, texture, motif, typography, copy style, and avoid-list.
   - If the theme is mixed, pick one primary style and one restrained accent style. Do not blend unrelated sticker systems.

3. Build the clean editable version first.
   - Use `references/layout-rules.md` before placing modules.
   - Do not add stickers by default. Ask whether to add stickers after a clean version unless the user explicitly requested decorative stickers.
   - Use a theme-specific letter-paper background: the paper texture stays consistent, but the printed motif must match the photos.

4. Implement editing and export.
   - Use `references/editor-spec.md` as the required feature contract.
   - Start from `assets/html-template/` when useful, then adapt style, motifs, dimensions, default modules, and copy.
   - Keep image sources same-origin or data URLs. Export must be complete WYSIWYG PNG.

5. Verify visually.
   - Run a local server for HTML apps and give the URL.
   - Check desktop and narrow viewports when possible.
   - Inspect the exported PNG. The PNG must match the live page, including timeline dashes, background motifs, text, rotated images, and user-adjusted photos.

## Non-Negotiables

- Never allow text/text, image/text, or image/image overlap in the default layout.
- Closer spacing means a pair. Place paired left/right photo and text close to each other; keep same-side unrelated modules farther apart.
- Keep the central timeline independent. It must not pass through content, and it must extend when modules are added.
- Support vertical and horizontal photos without forcing a fixed crop. Default to complete display; crop is optional and reversible.
- Do not use blurred copies of the same photo as filler unless the user explicitly asks for that look.
- Keep copy short, restrained, and editable. Do not include internal notes such as next-time shooting advice in the finished poster.

## Resource Routing

- For theme selection and visual direction: read `references/style-routing.md`.
- For spacing, grouping, typography, and motif rules: read `references/layout-rules.md`.
- For required browser editor behavior and PNG export: read `references/editor-spec.md`.
- For photo inventory and contact sheets: run `scripts/photo_inventory.py`.
- `scripts/photo_inventory.py` requires Pillow (`PIL`). If it is missing, install Pillow in the working environment or use an existing image library to make the same CSV/contact-sheet outputs.
- For a reusable HTML starting point: copy `assets/html-template/` into the project and customize it.
