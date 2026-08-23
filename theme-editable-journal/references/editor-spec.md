# Editor Specification

Build an HTML app unless the user asks for another format. The app must let the user finish the design without code.

## Required Controls

- Select any editable module by clicking it.
- Drag modules freely when drag layout mode is enabled.
- Edit visible text in place with `contenteditable`.
- Replace selected image from local files; read it with `FileReader` and store as a data URL.
- Transform selected module: scale and rotate.
- Transform selected image crop when crop mode is enabled: crop zoom, crop X, crop Y.
- Toggle crop mode per photo. Crop mode must not permanently discard the original image.
- Add text description module.
- Add image-text module.
- Delete selected module.
- Add a new timeline capsule/route module; its time text and module text must be editable.
- Extend poster height and center timeline automatically when modules are added or moved lower.
- Download current PNG as WYSIWYG.

## Export Rules

- Use local `html2canvas.min.js` or an equivalent local renderer. Do not depend on CDN at export time.
- Do not call `fetch()` during export.
- Ensure every default image is same-origin or data URL before export. Local replacement images should be data URLs.
- Avoid canvas-tainting sources. Set `allowTaint:false`.
- Avoid SVG foreignObject export for the whole page; it caused mismatched rendering in prior work.
- Avoid CSS `border-style:dashed` and complex `repeating-linear-gradient` for central timeline dashes if exact export matters. Use real DOM dash elements.
- Export only the poster area, not the side editor panel.

## Reliable Implementation Notes

- Keep a `selected` element in state and update controls from that element.
- Use CSS custom properties for module scale, photo width, crop height, crop zoom, crop X/Y, and poster height.
- Store transform state on the element style so html2canvas sees the live state.
- Use `data-draggable`, `data-kind`, and `data-time` attributes for predictable selection and timeline regeneration.
- Regenerate timeline dashes based on `--axis-top` and `--axis-height` after layout changes.
- Keep the timeline line and markers separate layers. Markers should remain above the line.
- If an image is not loaded, wait for `decode()` or `load` before export and show a useful error if it fails.

## Verification Checklist

- Replace one photo, drag it, rotate it, scale it, crop it, then export.
- Add one text module and one image-text module; confirm timeline height extends.
- Edit a timeline capsule label; confirm the downloaded PNG shows the edited text.
- Compare live page and PNG for timeline dashes, background motifs, and photo positions.
