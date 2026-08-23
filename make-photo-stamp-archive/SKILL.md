---
name: make-photo-stamp-archive
description: Transform one or more supplied photos into clean direct-splice archival artworks that pair a faithfully preserved photograph with a warm-white paper panel containing a compact hand-pressed custom seal or stamp. Use for requests mentioning 图章、印章、stamp、seal、照片加图章、照片档案、左右拼接、清爽纸张、圆形章、方形章、异形章、建筑轮廓章、主体缩小、移动到角落, or iterative changes to stamp shape, border, scale, position, ink color, caption, paper age, or splice orientation.
---

# Make Photo Stamp Archive

Create one finished raster composite per source photo: a faithful photographic panel directly joined to a quiet paper panel with a compact subject-specific seal.

Read [references/prompt-template.md](references/prompt-template.md) before generating or revising an image.

## Workflow

1. Inspect every local source image with `view_image`.
2. Identify the subject, distinctive silhouette, original color memory, viewpoint, scene geometry, important text, objects, people, animals, occlusions, and visual weight.
3. Lock invariants:
   - preserve the photographic panel faithfully;
   - add, remove, duplicate, recolor, reshape, or relocate nothing;
   - preserve people, faces, age, expressions, hands, clothing, poses, and relationships;
   - preserve signs, numbers, architecture, object counts, and defining markings.
4. Choose the composition:
   - default to a landscape left/right direct splice;
   - use approximately 55% photograph and 45% paper;
   - obey an explicit top/bottom or alternate ratio request;
   - keep the main seam perfectly straight and edge-to-edge.
5. Compose the paper panel:
   - use clean warm off-white paper with subtle fibers and light scan residue;
   - keep it gently archival, not heavily yellowed, dirty, cracked, burned, or antique;
   - reserve about 70% as quiet blank paper;
   - keep the seal-and-caption group at about 30% of the paper panel;
   - place the group in a balancing corner, never centered unless explicitly requested.
6. Choose a subject-specific seal shape:
   - circle or oval for compact rounded subjects, faces, icons, or ceremonial motifs;
   - square frame for signage, dense architecture, storefronts, or when explicitly requested;
   - panoramic ridge for rows, processions, coastlines, or wide landscapes;
   - arch for windows, doors, portals, and vaulted subjects;
   - irregular silhouette for distinctive buildings, vehicles, trees, statues, or objects.
7. Render the seal with dry ink, worn halftone, broken edges, uneven pressure, and slight registration error. Preserve the source's hue relationships with one dominant localized spot color and restrained supporting inks.
8. Add a small faded typewriter caption near, never over, the seal:
   - title: 1–3 uppercase English words;
   - subtitle: 2–4 lowercase image words separated by ` / `.
9. Use the built-in image generation/editing tool. Issue one call per source photo. For revisions, edit the latest accepted composite and change only the requested property.
10. Inspect every result. Verify source fidelity, subject count, seal shape, border completeness, scale, corner, straight seam, paper age, text spelling, color memory, and absence of invented content.

## Seal Rules

- Make the seal visually compressed rather than a miniature pasted photograph.
- Let ink loss and halftone erosion affect the print, not the main panel seam.
- For a square seal, show a complete unmistakably square border on all four sides. Allow slight broken ink, worn corners, uneven pressure, and misregistration; never use a clean digital frame or photo mat.
- For a circular seal, keep the contour visibly circular while allowing restrained dry-ink gaps.
- For a custom silhouette, preserve the subject's defining outline without enclosing it in a generic rectangle.
- Keep signs, numbers, faces, and essential structural features legible enough to identify the source.

## Revision Mapping

- `方形边框` / `square border`: add one complete worn square ink frame around the existing seal motif; preserve scale and position unless asked otherwise.
- `圆形图章` / `circular seal`: recast only the seal within a circular hand-pressed boundary.
- `缩小 10%`: scale the seal-and-caption group down by 10%; preserve all other layout values.
- `移动到左上/右上/左下/右下`: move only the seal-and-caption group within the paper panel.
- `纸张不要那么旧`: reduce yellowing, stains, cracks, and damage; retain subtle warm-white fibers.
- `不要那么规整`: roughen the ink boundary with restrained missing ink and halftone erosion; do not create a torn-paper collage.
- `保留原来的颜色`: strengthen recognizable source hue relationships while keeping the ink system muted.
- `左右拼接` / `上下拼接`: change only the two-panel orientation and reflow the stamp group; keep the boundary straight.

## Guardrails

- Produce one flat composite, not a book mockup, scrapbook, poster presentation, or before/after board.
- Never use a gradient, dissolve, feather, page turn, gutter, overlap, diagonal split, or decorative separator between the two main panels.
- Do not change the source photo to make the seal easier to design.
- Do not let the seal dominate the paper panel or eliminate the quiet negative space.
- Do not add decorative labels, logos, watermarks, dense copy, or invented objects.
- For multiple photos, return one independent finished asset per photo and report every saved path.
