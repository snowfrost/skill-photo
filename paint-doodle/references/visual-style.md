# Visual Style

Keep the output in a failed MS Paint look, not a stylized imitation of one.

## Shared style rules

- plain white canvas unless the user explicitly requests a different background color
- thin to medium black mouse-drawn outlines
- hand-drawn wobble and uneven contour closure are more important than tidy legibility
- prefer contours that look retraced, interrupted, and only half-corrected rather than one clean confident line
- use bucket-fill mistakes sparingly unless the user explicitly wants messier fills
- allow rough scribble coloring made from many short repeated strokes instead of clean fills
- leave many interiors unfilled so the page stays airy and white
- visible gaps where regions were not fully closed
- allow color patches to stop short, overshoot edges, or leave stray marks nearby
- occasional overdrawn black dirt patches are allowed, but do not turn the whole page into dense black sludge
- make the linework looser, shakier, and slightly more careless than the earlier version of this skill
- no gradients
- no soft shading
- no realistic lighting
- no material rendering

## Reference page rhythm

When matching the common Chinese "MS Paint explanation doodle" look:

- arrange several mini-scenes loosely across one white page
- keep large empty white areas between drawings
- mix object close-ups with tiny background vignettes
- do not use arrows
- do not use numbered captions
- keep text sparse but present when useful, usually 1 to 3 tiny hand-written notes total
- let the same subject reappear multiple times in different positions
- exaggerate actions, reactions, and gestures
- favor naive confidence over extreme chaos
- make the composition feel tossed onto the page instead of carefully arranged
- let the drawing look like someone kept fixing it with extra strokes but never actually cleaned it up

## Mode: color

This is the default mode.

Limit the palette to 4 to 7 harsh old-software default colors such as:

- black
- red
- blue
- green
- yellow
- brown
- purple

Keep these failure traits:

- wrong region filled
- fill leaking outside outlines
- white gaps left unfilled
- one object changing color across fragments
- blocks of color crossing contour boundaries
- scratchy repeated color strokes instead of uniform polished fill

Do not add:

- gradients
- shading
- soft palettes
- tasteful harmony

## Mode: monochrome

Use this only when the user explicitly asks for black-and-white.

Use only:

- white background
- black lines
- gray pencil-scribble fills and hatchy messy gray shading inside objects
- mostly white interiors outside the key gray scribble zones
- very small accidental black fills or dirty overlaps only when useful
- white accidental gaps

Do not use:

- red
- blue
- green
- yellow
- brown
- purple
- colored labels

Prefer:

- black outlines with loose gray scribble fill texture
- gray fill that looks hand-drawn, uneven, and patchy
- rough gray hatching on large objects like boats, animals, clothes, stones, and water
- black text only

Do not use:

- smooth airbrushed grayscale shading
- polished digital gray rendering
- neat uniform flat gray blocks everywhere

Aim for the feeling of a shaky black doodle on a white page with rough gray pencil-style scribble fills, like a casual hand-drawn monochrome explanation sketch.

## Mode: custom_palette

Obey the user-specified colors first.

Examples:

- `只用红黑`: use red and black only
- `蓝色线条`: lines become blue, other colors remain restricted
- `黑白加一点红色`: mostly black and white with a very small red accent range
- `黄色背景`: allow a yellow background if asked, while keeping the drawing crude

Even in custom palette mode:

- keep outlines rough
- keep fills wrong
- keep overflows and unfilled gaps
- keep the image unshaded
- do not invent extra colors

If the user explicitly requests a non-white background, let failed gaps reveal that background color instead of forcing white gaps everywhere.

## Anti-polish rule

If the result starts looking like a comic panel, children’s illustration, or designer-made naive art, degrade it further. The target is believable drawing failure, not curated ugliness.

If the result becomes too dirty, too dark, or too crowded, simplify it back toward thin outlines, wide white space, and loosely scattered doodles.

If the result explains too much with labels, reduce the text to a few tiny notes and replace the rest with more exaggerated poses, wider spacing, and clearer repeated actions.

If the result still feels too neat, roughen it with more broken contours, messier color strokes, visible correction marks, and slightly sloppier edge control before adding more objects or text.
