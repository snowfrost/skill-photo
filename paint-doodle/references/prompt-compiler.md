# Prompt Compiler

Assemble the final image prompt only after analysis, scene planning, object degradation, and style selection are complete.

## Prompt structure

Build the prompt in this order:

1. one sentence naming the exact event topic
2. one sentence describing the 2 to 6 visible fragments and page layout
3. one sentence describing the crude object style, exaggerated actions, and sparse short text
4. one color-mode clause
5. one anti-polish clause

Keep the final prompt concrete and visual. Avoid abstract commentary about symbolism, emotion, or design theory.

## Layout anchor

When the target style resembles a reference doodle page, explicitly mention:

- one white page with several scattered mini-scenes
- large blank areas between scene fragments
- repeated appearances of the same person or object across the page
- 1 to 3 tiny hand-written Chinese phrases total
- no arrows
- no numbered captions
- thin shaky mouse lines instead of thick painterly brushwork
- exaggerated gestures and looser page placement
- rough scribble color texture, broken contours, and visible correction strokes

## Required color clause

For default color output, include this exact text:

```text
a few harsh default MS Paint palette colors,
crude failed bucket fills,
color bleeding outside broken outlines,
accidental white gaps,
wrong regions filled,
no gradients,
no shading,
no professional color harmony
```

## Required monochrome clause

When the user explicitly asks for black-and-white, replace the color clause with this exact text:

```text
black outlines with messy gray pencil-scribble fills on a plain white canvas,
no color anywhere,
gray hand-scribbled fill texture is allowed,
no gradients,
no soft rendered lighting,
no material rendering,
no polished grayscale painting
```

## Custom palette clause

When the user names colors explicitly:

- replace the palette wording with the user-approved colors only
- keep the rest of the failure traits from color mode
- mention any requested background color explicitly
- if the background is not white, replace `accidental white gaps` with wording about unfilled gaps revealing the background color

Example pattern:

```text
red and black only, crude failed bucket fills, color bleeding outside broken outlines, accidental white gaps, wrong regions filled, no gradients, no shading, no professional color harmony
```

## Anti-polish ending

End with a short reminder like:

```text
looks like a genuine amateur MS Paint explanation doodle with loose scattered mini-scenes, exaggerated actions, a few tiny handwritten notes, and no arrows or numbered captions, not a polished comic or storybook illustration
```

When the user asks for an even rougher result, add wording such as:

```text
extra scratchy linework, messy repeated color strokes, broken contour corrections, and obvious half-finished scribble texture
```

## Compile check

Before using the prompt, confirm:

1. the topic matches the user request exactly
2. the fragments stay within 2 to 6 visible beats
3. the color clause matches the current task, not an earlier one
4. monochrome tasks contain no hidden color wording
5. the prompt avoids arrows and numbered captions
6. the prompt keeps text sparse rather than wordless
7. the prompt still sounds like a doodle explanation page, not stylized art direction
8. the page feels airy and white enough instead of overly filled or panelized
