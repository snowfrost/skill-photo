# Visual Evaluation

Run this checklist internally before calling the image generation tool.

## Required gate

Do not generate until every check passes.

## Checklist

1. Is the current theme accurate?
2. Did any unrelated object from another case slip in?
3. Did the plan split into 2 to 6 visible event fragments?
4. Did the prompt use the current user-required color mode?
5. If the user did not explicitly ask for black-and-white, did the prompt stay colorful by default?
6. If the user did ask for black-and-white, did the prompt switch to black outlines plus rough gray scribble fills instead of pure flat black-only rendering?
7. Did the plan avoid arrows and visible sequence numbers?
8. Did the plan keep text very sparse without dropping to zero when tiny labels would help?
9. Did the result avoid looking like a comic, storyboard, or children’s picture book?
10. Does the image still feel like a real failed drawing attempt?
11. Are the actions exaggerated enough to explain themselves without labels?

## Common failures and fixes

- Too polished:
  remove composition language, remove expressive lighting, simplify objects further, worsen line quality
- Too colorful in a default task:
  only treat this as a problem when the user explicitly requested black-and-white; otherwise default color is correct
- Too stark in a monochrome task:
  replace pure black fills with rough gray scribble texture and keep the background white
- Too neat:
  add broken outlines, misfills, repeated strokes, uneven spacing, and warped shapes
- Too crowded:
  reduce secondary objects and keep only event-critical items
- Not obviously event-based:
  strengthen the visible action in each fragment instead of adding more labels
- Too wordy:
  remove labels, captions, and speech bubbles first; solve clarity with pose and repetition
- Too silent:
  add 1 to 3 tiny handwritten cues, but keep them short and unnumbered
- Too instructional:
  remove arrows and sequence numbers completely

## Final standard

The picture should feel like someone tried to explain a real event quickly in old MS Paint and did a bad job, while still leaving the event understandable.
