# Semantic Analysis

Use this file first on every task.

## Goal

Lock the current request into one clean event topic, one color mode, and one bounded object set before planning the picture.

## Extract these fields internally

- `theme`: one sentence describing the specific event or situation to depict
- `actors`: people, animals, vehicles, tools, or other main participants
- `setting`: the visible place or environment
- `must_show`: actions or consequences that must appear on canvas
- `must_not_import`: unrelated objects from old examples, prior turns, or generic scene habits
- `style_anchor`: whether the user provided a reference image or established prompt style that should control layout, line feel, annotation style, and scene arrangement while color is handled separately
- `color_mode`: `monochrome`, `color`, or `custom_palette`
- `palette_note`: blank for monochrome, limited old-paint colors for color, user-specified colors for custom palette
- `text_budget`: 1 to 3 very short handwritten phrases total, with no sequence numbering

## Topic boundary rule

Do not blend multiple cases together unless the user explicitly asks for a combined scene.

If the user mentions one incident, keep every fragment tied to that same incident. Do not add random bystanders, unrelated buildings, background jokes, or props just because they are common in similar images.

## Reference style rule

If the user says the result should look like an earlier prompt, a sample image, or a known doodle style:

- copy the layout logic, line confidence, annotation behavior, and page rhythm first
- treat color as a separate decision controlled only by the current color-mode rules
- do not keep using the older style once the user gives a new visual reference
- prefer exaggerated motion and sillier body language, but still allow a few tiny handwritten cues when they help

## Color mode decision

Apply this priority every time:

1. `custom_palette`: the user names exact colors or a tightly constrained color range
2. `monochrome`: the user explicitly asks for black-and-white
3. `color`: everything else

## Monochrome interpretation

When the user explicitly requests black-and-white:

- keep the background white
- keep the lines black
- allow gray pencil-like scribble fills inside forms
- allow small white unfilled gaps
- prefer hand-scribbled gray texture over clean solid gray blocks
- do not add symbolic or realistic object colors

Water does not become blue. Trees do not become green. Fire does not become red. Clothes can stay white or be filled with rough gray scribble texture.

## Contamination checks

Before moving to scene planning, ask internally:

1. Did I capture the current theme accurately?
2. Did I import any object from another example or prior task?
3. Did I infer colors from real life instead of from the user's request?
4. Did I accidentally widen the topic into a more generic story?
5. Am I relying on arrows, numbering, or too much text instead of actions?

If any answer is yes, narrow the plan before continuing.
