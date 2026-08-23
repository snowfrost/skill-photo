---
name: paint-doodle
description: Generate rough MS Paint style event explanation images from a user described topic, incident, or absurd scene. Use when asked for 事件解释图, 事件示意图, 事故过程图, 吐槽式重现图, 鼠标乱画风说明图, or intentionally bad hand-drawn visual explanations. Default to a few harsh old MS Paint colors unless the user explicitly asks for black-and-white or explicitly specifies a palette.
---

# Paint Doodle

Follow a documentation-only workflow. Do not create or rely on `scripts/`, `tests/`, `validate_plan.py`, `build_prompt.py`, `run_tests.py`, or Python dependencies. Keep the structured event plan internal.

## Required workflow

1. Read [references/semantic-analysis.md](references/semantic-analysis.md) to lock the topic, subject boundary, and current color mode.
2. Read [references/event-to-scene.md](references/event-to-scene.md) to split the request into 2 to 6 visible event fragments.
3. Read [references/object-degradation.md](references/object-degradation.md) to convert every object into awkward mouse-drawn forms.
4. Read [references/visual-style.md](references/visual-style.md) to enforce the failed MS Paint look and the active color mode.
5. Read [references/prompt-compiler.md](references/prompt-compiler.md) to assemble the final image prompt.
6. Read [references/visual-evaluation.md](references/visual-evaluation.md) and pass the internal checklist before calling any image generation tool.
7. Use [references/examples.md](references/examples.md) only as structural examples. Never inherit objects, layouts, or palettes from an older example.

## Hard rules

- Re-evaluate color mode for every new task.
- Use color priority in this exact order: `custom_palette` > explicit `monochrome` > default `color`.
- Treat `color` as the default whenever the user does not explicitly ask for black-and-white.
- Prioritize the reference drawing language over generic "bad art" language when the user provides a style example or says the result should match an existing prompt style while ignoring color.
- Avoid arrows in the final image.
- Avoid visible sequence numbers such as `1.`, `2.`, `3.` in the final image.
- Keep written explanation text sparse, not absent. Prefer 1 to 3 very short hand-written phrases total, and let poses, spacing, and object repetition carry the rest of the story.
- Push the actions and expressions into a more exaggerated, sillier, and looser direction when matching this doodle style.
- Keep the scene rough, broken, and visibly failed. Do not drift into polished comics, storybooks, editorial illustration, or professional infographic style.
- Keep all lighting, gradients, shading, and realistic material rendering out of the result.
- Keep all planning internal. Do not write intermediate plans to disk.

## Color mode routing

- Use `custom_palette` when the user explicitly names allowed colors, such as `只用红黑`, `蓝色线条`, `黑白加一点红色`, or `黄色背景`.
- Use `monochrome` only when the user explicitly asks for black-and-white, such as `黑白`, `纯黑白`, `不要颜色`, `只用黑白`, or `不要彩色`.
- Use `color` for every other case, including ordinary requests that do not mention color at all.

## Prompt clause requirement

- In default `color`, include this exact clause in the final prompt:

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

- In explicit `monochrome`, replace the color clause with this exact clause:

```text
black outlines with messy gray pencil-scribble fills on a plain white canvas,
no color anywhere,
gray hand-scribbled fill texture is allowed,
no gradients,
no soft rendered lighting,
no material rendering,
no polished grayscale painting
```

- In `custom_palette`, keep the `color` failure traits but rewrite the palette part so it only names the user-approved colors. Never invent extra colors.

## Final reminder

Before generating, confirm internally that the result is about the current topic only, contains 2 to 6 visible event fragments, respects the active color mode, avoids arrows and numbering, keeps text sparse, exaggerates the actions, stays colorful by default, avoids comic polish, and still feels like a genuine failed drawing attempt.
