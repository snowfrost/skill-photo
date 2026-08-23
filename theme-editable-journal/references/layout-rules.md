# Layout Rules

## Core Structure

- Prefer a route-journal layout for trip sequences: title area, independent center timeline, alternating left-text/right-photo and right-text/left-photo modules.
- Keep the timeline in its own protected column. Use actual DOM elements for dash segments when exporting with html2canvas.
- Pair each text block with its cross-axis photo. Cross-axis paired distance should be visibly closer than unrelated same-side vertical spacing.
- Keep same-side text and photo modules separated enough that they are not read as one pair unless intended.

## Spacing

- Reserve a safe gutter around the timeline; no title, tag, text, or photo may touch it.
- Keep page margins moderate. Wide margins make the poster feel empty; too-tight margins make editing risky.
- Each text block needs enough height for the longest default line plus user edits. Use `overflow-wrap:anywhere`.
- Avoid translucent text boxes as a default. Prefer no text box, with short underlines or soft label strips behind titles only.

## Photos

- Make subjects readable. A photo is too small if the main person, animal, artifact, or exhibit cannot be identified at phone-screen size.
- Do not crop people, animals, artifact tops, signs, or hands unless the crop is intentional and reversible.
- Allow both vertical and horizontal photos. Default `img` should show the complete image; optional crop mode can be enabled by the user.
- Rounded frames can be used, but do not force every photo into the same aspect ratio. Let frame size follow the selected image role.

## Text

- Use short, editable lines. Prefer 1 title plus 1-2 short body lines per module.
- Do not display production notes, photo descriptions, or future shooting suggestions in the poster.
- Use friendly handwritten or rounded display type for parent-child journals; use quieter serif/songti-like type for history; use restrained hand-written type for gallery.
- Keep title and description physically separate. The number badge, title, highlight strip, and body copy must not collide.

## Decoration

- Start clean. Add stickers only after the clean layout works.
- If stickers are used, make them feel hand-drawn, picture-book, comic, field-guide, or printed ephemera depending on theme.
- Place stickers in real empty space: corners, between route modules, or near the title. Never use stickers to fill every gap.
- Theme-specific letter paper is allowed as a fixed background: grid or ruled paper plus subtle printed motifs. Motifs should be moderately dense but low contrast.

## Quality Gate

Before finalizing, inspect the poster and exported PNG:

- No overlap anywhere.
- All photos have clear subjects.
- Timeline markers align with related modules.
- Added modules create enough vertical space and extend the timeline.
- Export matches the live page.
