---
name: joy-calm-woodcut-zine
description: Transform a photo, theme, sentence, object, mood, or content brief into a calm Japanese/Korean indie-zine poster rendered primarily as an integrated woodcut scene on luminous paper, with structural carved lines, scene-aware color, selective form abstraction, tiny typography, and a generated raster image. Use for poetic editorial posters, photo-to-print transformations, emotional travel imagery, fresh lifestyle graphics, or requests for bright, clear, nostalgic, misty, distant, or semi-abstract woodcut visuals.
---

# Calm Integrated Woodcut Zine Poster

Turn the user's input into:

1. a final four-paragraph image-generation prompt; and
2. a generated raster poster.

Use Standard Mode and generate the image unless the user explicitly asks for prompt-only.

## Visual Identity

Build a fresh Japanese/Korean indie-zine composition rather than an archival kraft-paper collage.

Treat relief carving as a **selective mark-making method inside a contemporary editorial composition**, never as a request to change the whole work into the historical genre of a traditional woodblock print. The style target is light, colored, open, and selectively printed—not a black-and-cream full-page linocut.

## Approved Visual References

Treat `assets/examples/positive/02.png` as the canonical style anchor. Before compiling the prompt, inspect it at full size and read `references/visual-reference-guide.md`. Inspect the other positive examples only when the user explicitly asks for collage/cutouts or when the canonical anchor cannot express an essential requested mood.

Apply a mandatory **reference lock** before every image-generation call:

1. Select `assets/examples/positive/02.png` by default, even when the content is not architectural. It controls spatial abstraction and print construction, not subject matter. Change to another approved example only for an explicit user-requested exception, and keep the selected anchor through the entire run.
2. Do not blend multiple positive examples by default. Multiple style images introduce competing composition, palette, and carving signals and are permitted only when the user explicitly asks to hybridize named examples.
3. Include the user's source image and the selected approved example in the same image-generation reference set when local paths are available. Do not rely on prose alone.
4. Assign explicit roles in the prompt: `CONTENT REFERENCE` supplies only subject identity, essential gesture, and three to five recognizable cues. It does **not** control camera framing, perspective, scale, depth, object count, or photographic composition. `STYLE REFERENCE` controls paper, relief-print construction, spatial compression, hierarchy, negative space, palette behavior, edge dissolution, typography scale, and emotional tempo.
5. State that the style reference is authoritative for rendering and that the content reference is authoritative for what must remain recognizable. Never import objects, words, landmarks, or layout from the style reference.
6. Preserve the user's subject identity but freely redesign its composition. Borrow no objects or words from the style anchor, but follow its visual hierarchy and degree of simplification.

- Use the references to learn visual grammar, not to copy their subjects, wording, or exact layouts.
- Give the approved references priority over generic associations with “woodcut,” “linocut,” “engraving,” “zine,” or “Japanese/Korean style.”
- When generating from a local source photo, include that source and exactly one scene-relevant approved example whenever the image tool supports multiple references.
- Keep the common family resemblance: luminous fibrous paper, generous quiet space, limited fresh inks, flat relief-print color, forms dissolving directly into paper, tiny subordinate type, and calm locally organized carving.
- Default to an **integrated relief-print scene**. Treat sticker collage as an optional exception only when the user explicitly requests stickers, collage, cutouts, or separated photo fragments.
- Do not infer antique book illustration, Victorian engraving, museum-print reproduction, or brown archival ephemera from the word “woodcut.”
- Do not use black as the dominant ink by default. Prefer a **full-strength chromatic dark** such as deep green, mineral blue, blue-gray, or violet-blue. Reserve near-black for tiny accents only. “Chromatic” does not mean pale, gray, translucent, dusty, or low-contrast.

- Use a tall vertical 3:5 poster. Keep roughly 35%-55% of the page as untouched paper, including one coherent quiet area; do not mistake a mostly full-page pale engraving for negative space.
- Keep dense dark ink below roughly 15%-25% of the page, but print that localized ink with firm saturation and clear value contrast. This is an area limit, not an opacity limit. No continuous dark perimeter, carved picture frame, corner foliage frame, or inked border may enclose the composition.
- Use a light woodcut-paper field: carved fibers, subtle block-print grain, faint directional gouges, and matte handmade paper. Keep it airy; never make it brown, muddy, heavy, rustic, or leather-like.
- Convert source photography into a unified relief-print interpretation whose outer contours fade, open, or terminate naturally into the paper. Do not place the scene inside a large white-bordered blob, kiss-cut silhouette, floating photo container, or lifted-paper object by default.
- Preserve the source's recognizable emotional anchor while simplifying secondary details.
- Combine fresh color, sparse typography, and hand-printed imperfections.
- Allow controlled abstraction. The poster should feel interpreted, not merely filtered.

## Calm Tempo Invariant

Keep every poster fundamentally calm. This rule overrides scene, color, abstraction, and composition choices.

- Express bright weather as serene joy, warmth, clarity, or spacious optimism—not excitement, speed, impact, or celebration frenzy.
- Let the eye settle before it travels. Use stable spacing, gentle asymmetry, soft repetition, unhurried hierarchy, and clear resting areas.
- Use strong color as a quiet field or balanced block, never as a visual alarm.
- Use dense short carving to deepen tone without creating acceleration. Keep directional marks slow, interrupted, and locally grouped.
- Depict traffic, wind, waves, crowds, action, and urban density through restrained rhythm and selective cues rather than kinetic effects.
- Avoid urgent diagonals, aggressive convergence, rapid zigzags, motion streaks, impact bursts, visual shouting, frantic scatter, harsh contrast jumps, and tightly competing focal points.

## Scene and Emotion Router

Analyze the image before choosing style. Infer the dominant subject, weather, light, season, distance, human activity, and emotional temperature. Choose one primary atmosphere and optionally one supporting atmosphere.

### Bright day / good weather

- Feel clear, optimistic, open, gently playful, and peacefully radiant.
- Use luminous cyan, sky blue, lemon yellow, fresh green, tangerine, or warm pink.
- Increase color coverage and contrast; allow two to four vivid inks.
- Use crisp relief boundaries, buoyant spacing, quiet small type, and balanced open shapes.

### Mountain / high landscape

- Feel distant, elevated, cold-clear, spacious, and quietly powerful.
- Emphasize vertical reach, thin air, sharp silhouettes, snow, ridges, or layered distance.
- Prefer glacial cyan, cobalt, mineral blue, ice white, silver gray, with one clean warm counterpoint when useful.
- Abstract ridges into cut-paper planes, contour bands, carved lines, or geometric altitude marks.

### Sunset / evening light

- Feel warm, nostalgic, slow, intimate, and time-worn without becoming gloomy.
- Use persimmon orange, apricot, dusty coral, plum, twilight blue, or amber.
- Use softer edges, overlapping transparent inks, longer shadows represented as flat shapes, and restrained film-like grain.
- Favor memory fragments, paired panels, or fading silhouettes.

### Fog / mist / rain haze

- Feel solitary, suspended, quiet, ambiguous, and spacious.
- Use cool white, pale cyan, blue gray, ink black, muted violet, with one isolated saturated accent.
- Reduce detail, separate objects with empty space, and let forms dissolve into woodcut grain or incomplete contours.
- Use sparse or partially obscured typography.

### Seaside / water

- Infer whether the scene is sparkling, windy, calm, wintry, or stormy.
- Translate water into carved wave lines, cyan print fields, repeated bands, or abstract current shapes.
- Treat people, boats, fishing rods, shorelines, or reflections as rhythmic marks rather than documentary detail.

### City / architecture

- Infer pace, era, density, and light.
- Reduce buildings to carved silhouettes, windows, clocks, signs, street ribbons, or stacked print blocks.
- Use structure and repetition while retaining breathing room; never recreate the entire skyline as a full-bleed photograph.

### People / intimate moments

- Preserve pose, gesture, distance, and relationship before facial detail.
- Use paired silhouettes, integrated figure groups, hand-cut contour echoes, or simplified clothing color fields.
- Avoid beautification, fashion-ad styling, or synthetic facial reconstruction.

If several routers apply, choose the one that controls emotion first and use the second to control form. Example: a mountain at sunset uses sunset for warmth and nostalgia, mountain for height and geometric ridges.

## Abstraction Dial

Choose an abstraction level automatically from the source and request.

- **A1 — Recognizable relief figure:** Preserve the main subject and simplify only the background. Use for people, landmarks, and important documentary moments.
- **A2 — Interpreted fragment:** Preserve the central subject, replace secondary detail with carved lines, color planes, silhouettes, cropped shapes, or texture windows.
- **A3 — Atmospheric abstraction:** Retain only two or three identifying cues. Convert the rest into woodcut marks, torn color fields, contour bands, repeated symbols, or spatial rhythm. Use for fog, light, weather, memory, motion, and conceptual prompts.

Default to **A2.5 — A2 recognition with A3 transformation**. Preserve only three to five identity anchors from the source and abstract at least one substantial region—typically 30%-50% of the main visual cluster—into carved planes, interrupted contours, exposed-paper voids, repeated structural marks, or compressed depth bands. Use A1 only for intimate faces, irreplaceable documentary details, or explicit realism requests. Use full A3 when atmosphere matters more than literal objects.

## Abstraction Discipline

Interpret the source rather than reproducing the complete photograph.

- Identify three to five non-negotiable anchors, such as a mountain silhouette, bridge arch, tower rhythm, person gesture, roof color, horizon, or boat profile. Preserve those anchors and simplify the rest.
- Remove or merge secondary trees, windows, vehicles, rocks, branches, clouds, signs, street furniture, and surface detail. Do not preserve every object merely because it appears in the source.
- Break continuous scenery into two or three integrated visual systems: a dominant structural form, a simplified rhythmic middle layer, and a sparse atmospheric or water field. Let these systems share paper and overlap naturally rather than enclosing them in sticker borders.
- A small duplicated sticker, detached icon, or decorative fragment does not satisfy abstraction by itself. Rebuild the main form: merge, omit, flatten, displace, crop, dissolve, or rescale at least one major region so the central cluster no longer preserves the photograph's complete spatial logic.
- Convert at least one large region into non-photographic structure: contour bands for mountains, repeated hatch rhythms for forests, flat interrupted strips for water, window grids for architecture, or open-paper gaps for snow and fog.
- Let some contours stop early, dissolve into paper, shift registration, or continue as independent marks. Preserve intentional incompleteness.
- Keep abstraction quiet and spatial. Avoid cubist shattering, random geometry, frantic collage, surreal object substitution, and decorative symbols unrelated to the source.
- Preserve the scene's emotional truth and recognizable anchor while reducing documentary completeness.

## Canonical Translation Grammar

Translate the bridge sample's relationships, never its literal subject:

- Choose one dominant structural silhouette to organize the print: for mountains use one simplified ridge or valley wall; for coasts use one shore curve; for cities use one facade, bridge, or street band; for people use one gesture or grouped silhouette.
- Compress depth into at most three visibly different layers. Flatten perspective and remove most intermediate objects instead of tracing the source from foreground to horizon.
- Let the dominant form occupy roughly 18%-35% of the page. It may touch a side edge, but it must not flood most of the page with continuous detail.
- Build secondary layers from abbreviated symbols and repeated marks: small leaf clusters, windows, figures, boats, snow cuts, wave dashes, or roof rhythms. Do not render every rock, crease, tree, footprint, cloud, or vehicle.
- Reserve the darkest ink for the dominant structure and a few anchors. Render distance with sparse broken marks and exposed paper, not with low-opacity photographic tracing.
- Use one small warm or saturated accent when it belongs to the source. Keep people graphic and simplified; do not preserve photographic clothing seams, equipment logos, facial modeling, or accessory detail.
- Preserve the sample's distribution of information: quiet paper first, dominant form second, rhythmic small cues third, microtype last.
- Preserve the sample's light-value hierarchy: most of the page is paper; dark ink is localized; middle values are carried by broken colored lines. Do not invert this into a mostly dark print with cream cuts.
- Match the sample's ink presence: the dominant structure must contain decisively saturated dark lines or blocks, the middle layer must use a clearly visible secondary ink, and at least one small accent should be unmistakably colored when appropriate. Do not fade every layer toward paper.
- Reduce commercial signs, logos, window grids, foliage, and facade ornament to a few anonymous cues unless exact text or branding is explicitly requested. Never faithfully transcribe every visible sign from the source.

## Composition Engine

Select a layout that supports the inferred atmosphere. Avoid repeating the recent visible layout.

- **integrated-arch:** one dominant bridge, roof, ridge, canopy, or structural curve organizes smaller scene rhythms beneath or around it
- **open-relief-field:** the scene prints directly on paper and dissolves at the outer edges without a containing silhouette
- **high-horizon:** small subject low on the page with expansive upper air
- **vertical-ascent:** stacked ridge, tower, tree, or figure shapes emphasizing height
- **memory-bands:** two compressed depth bands with transparent ink overlap
- **cutout-window:** one irregular color shape revealing a photo or texture
- **type-and-object:** understated short type balances one small carved object
- **dissolving-field:** subject transitions into carved lines, mist, dots, or incomplete contours
- **abstract-landscape:** layered print planes suggest a scene without reproducing it literally

Keep the dominant printed structure around 18%-35% of the canvas and total printed information around 45%-65% by default. Expand only when the user explicitly requests density, while preserving a coherent untouched paper region. Keep elements away from extreme edges unless a structural contour needs to enter or leave the page.

## Edge Integration

Make the photographic material read as a scene carved and printed directly onto the page.

- Remove the photograph's rectangular boundary and avoid replacing it with a large closed irregular boundary.
- Let foliage, sky, distant buildings, water marks, snow, mist, and fine contours taper or disappear into untouched paper.
- Use exposed paper **inside and between** forms, not as a uniform cream outline surrounding the entire scene.
- Add print grain, halftone, woodblock hatch, limited ink layers, and slight misregistration.
- Keep shadows minimal and graphic. Never use glossy vinyl shine, thick 3D drop shadows, or product-mockup lighting.
- Let the scene dissolve into abstract lines, sparse marks, or color fields when using A2 or A3.
- Use separated fragments only when conceptually necessary or explicitly requested. Never add a duplicate mini-scene merely to imitate collage.

## Selective Relief Hierarchy

Make visible carved linework a defining feature of every result. Use it structurally rather than as a uniform filter.

- Every main subject must contain clearly legible relief-cut lines at normal viewing size: contour cuts, directional hatching, parallel gouges, broken cross-cuts, or short pressure-varied strokes. Paper grain, halftone dots, photographic noise, and distressed ink do not count as carved linework.
- Use flat separated ink fields and exposed paper between line systems, but never let flat fill or halftone replace the carved structure of mountains, trees, architecture, water, or foreground terrain.
- Preserve three texture zones: open paper or quiet ink; medium directional hatching that explains form; dense short cuts and compact crosshatching at focal ridges, shadow turns, structural joints, and dark accents. Make all three zones visible at thumbnail scale.
- Let line direction follow form: cuts wrap or descend along mountain planes, run horizontally with calm water, climb architectural edges, branch through foliage, and compress around shadow. Avoid arbitrary scratches floating across the subject.
- Use a mixture of short and medium structural strokes. Keep most marks compact, but allow medium-length contour or hatch groups when they describe an actual plane, arch, ridge, road, wave, or building edge. Do not reduce all carving to tiny dots or hairline specks.
- Do not cover mountains, forests, water, architecture, and sky with the same line frequency or grain size. Assign each depth layer a different mark density.
- Avoid a uniformly engraved, stippled, or grain-filtered photo, but do not suppress engraving itself. The result must be constructed from carved contours, directional hatch groups, ink blocks, and exposed paper.
- Give cuts physical weight: irregular pressure, tapered or broken ends, compact clusters, occasional overlaps, and small unprinted gaps. Avoid both hairline-only etching and blunt stamp-like photo filtering.
- Reject results where the subject reads primarily as a photograph with blue duotone, halftone, ink distress, or posterization. Those effects may support the print but cannot replace visible relief-cut drawing.
- Also reject results that read as a conventional full-page linocut or souvenir woodblock: thick black outlines, binary black/cream contrast, carved border, uniformly dense cuts, filled corners, and exhaustive object rendering. Visible carving must remain selective, chromatic, airy, and subordinate to editorial hierarchy.

## Woodcut Atmosphere Engine

Use carved marks and colored block-print fields as the primary carrier of light, air, distance, weather, and emotion—not as decorative background noise. Let a few relief-printed anchors preserve recognition while the surrounding carving interprets atmosphere.

- Give the atmosphere layer a clear visual role and let it occupy 20%-55% of the visual cluster or extend softly into nearby negative space.
- Build tonal depth from carved-line density: sparse marks feel luminous and airy; dense crosshatching feels deep, cold, crowded, or nocturnal.
- Express intensity primarily through the number, density, overlap, and pressure of short carved marks—not through line length. In strong areas, use many short, tight, broken strokes or compact crosshatching; in quiet areas, reduce their frequency and expose more paper.
- Use exposed paper as the brightest value. Carve light out of ink instead of painting soft digital gradients.
- Form color transitions through separated blocks, transparent overprint, broken hatching, and changing line density.
- Connect subject and atmosphere by letting contours dissolve into carving, allowing compact currents or tonal bands to pass through spatial layers, and repeating one contour rhythm across them.
- Keep carving directional and scene-specific:
  - sunshine and clear weather: clustered short rays, small fan-shaped groups, bouncing marks, broad clean color fields;
  - mountains and high places: short ascending cuts, sharp contour bands, sparse broken air marks, layered ridge planes;
  - sunset and nostalgia: dense short hatching near the glow, horizontal broken bands, warm-to-cool overprint, softened fragmented edges;
  - fog, rain, and solitude: drifting curves, interrupted contours, wide uninked gaps, low-density blue-gray veils;
  - water and wind: repeated short wave cuts, gently flowing parallel groups, calm rhythmic breaks, sparse curved drift marks;
  - city and movement: softened street perspective, window grids, repeated light marks, compressed short hatch near the urban core without speed effects.
- Preserve handcrafted irregularity: varied pressure, imperfect edges, small ink gaps, uneven registration, and occasional carved splinters.
- Keep most individual atmosphere strokes short relative to the subject: typically below 3%-6% of the visual cluster's width. Reserve a few longer contours only for an actual road, horizon, fishing line, wave direction, or subject edge.
- Avoid explosive starbursts, speed-line effects, large fans of long rays, spiky halos, uniform texture overlays, synthetic noise, seamless wallpaper patterns, smooth airbrush shading, or carving that does not respond to the scene.
- Balance ink blocks with unmistakable carved drawing. When the image reads as an evenly engraved illustration, vary line direction and density and reopen selected paper gaps; when it reads as a flat stamp or duotone photograph, add structural contour cuts and directional hatch groups before finalizing.

## Woodcut Background

Use a light, fresh woodcut surface instead of kraft paper.

- Base colors: soft white, rice paper, pale oat, cool ivory, mist gray, or lightly tinted blue-white.
- Texture: subtle carved fibers, shallow gouge marks, block-print pressure variation, and sparse ink traces.
- Keep the background luminous and low-contrast so it supports the integrated print.
- Rotate groups of short carving marks to reinforce the scene: upward for height, horizontal for calm water, gently clustered around sunshine, drifting curves for fog or wind.
- Never use dark brown kraft paper, dirty beige, parchment maps, leather texture, scorched edges, heavy stains, or distressed vintage packaging.

## Color System

Choose color from the inferred atmosphere rather than defaulting to one cobalt accent.

- Quiet scenes: one main ink plus one small counter-ink.
- Normal fresh scenes: two or three inks.
- Bright or celebratory scenes: three or four vivid inks with controlled overlap.
- Fog and solitude: mostly light neutrals with one isolated saturated anchor.
- Preserve ink saturation even when adding grain.
- Separate **coverage** from **strength**: untouched paper may occupy 35%-55%, while the ink that is present should normally print at strong, opaque-looking saturation. Never achieve lightness by lowering the opacity of every ink layer.
- Require a usable value ladder: paper white; one clearly visible light or middle colored ink; one firm chromatic dark; and, when supported by the scene, one small saturated warm or contrasting accent.
- Quiet, winter, fog, and solitary scenes may use fewer colors, but must still retain one confident dark anchor and one legible secondary tone. “Calm” means spatially restrained, not washed out.
- At thumbnail scale, the dominant form must separate immediately from the paper. If the main subject, middle layer, and paper merge into one pale beige-gray value, increase ink saturation and local contrast without increasing dark coverage.
- Favor flat printed color, transparent overprint, and paper showing through. Avoid photographic gradients, generic pastel washes, neon glow, and rainbow palettes.
- Color should express weather and emotion, not decorate arbitrarily.

## Typography

- Invent one short poetic phrase if the user supplies no text.
- Keep exact requested wording unchanged.
- Use small serif, rounded grotesk, typewriter, hand-cut, or monospaced typography selected for mood.
- Keep all typography visually subordinate to the carved scene. No word, letter, numeral, or glyph may become the largest element or primary visual anchor.
- Keep the main phrase small, light, and understated; it should normally fit within 8%-20% of the visual cluster's width and remain clearly smaller than the principal structural form.
- Add optional microtext for time, place, wind, temperature, or a field-note fragment.
- Apply offset layers, broken edges, carved fills, or partial occlusion only to small type. Never create oversized initials, giant display letters, poster-scale words, or headline-as-object compositions.
- Keep text short because image models may distort long copy.

## Prompt Compiler

Write the final prompt as four compact paragraphs in this order:

1. Begin with a role-and-style lock: “The user photo is the CONTENT REFERENCE and supplies only subject identity, essential gesture, and three to five recognizable cues; it does not control camera framing, perspective, scale, depth, object count, or photographic composition. Example 02 is the STYLE REFERENCE and is authoritative for luminous fibrous paper, calm negative space, limited flat colored inks, selective integrated relief marks, flattened hierarchy, edge dissolution, and tiny subordinate typography. This is a contemporary editorial zine using relief-carved marks, not a traditional woodblock-print genre image. Translate the sample's relationships to the new subject without copying its bridge, bus, boats, buildings, words, or exact layout.” Then specify canvas, untouched-paper ratio, dominant-form scale, chromatic-dark ink, and directional carving field. Explicitly say: “No large sticker, no white contour enclosing the scene, no floating photo-shaped container, no full-scene photographic tracing, no black-and-cream linocut, no carved border, no full-page dense engraving.”
2. Name three to five recognizable anchors from the CONTENT REFERENCE, then require A2.5 interpretation: choose one simplified dominant silhouette, delete most incidental detail, compress depth to at most three graphic layers, convert supporting objects into abbreviated rhythmic symbols, and transform a substantial region into exposed-paper voids or sparse carved marks. State which photographic details must disappear.
3. Specify the exact color palette, typography, open edge behavior, overprint, and misregistration. State explicitly: “The 15%-25% dark-ink figure controls area only, not ink strength. Print the localized chromatic dark at firm saturation; keep a clearly visible secondary colored ink and one small saturated accent when scene-appropriate. Do not lower all inks toward paper.” Require selective relief-cut drawing with a three-zone hierarchy—open paper, medium directional hatching that explains form, and small dense clusters at focal structures. State that halftone, duotone, distressed ink, photographic grain, binary black/cream cutting, uniform all-over carving, and pale monochrome fading cannot substitute for this hierarchy.
4. Emotional result, flat scanned-paper appearance, preservation requirements, and avoid-list. End by rejecting antique engraving, uniformly etched scenery, vintage-book illustration, generic parchment, and any result that departs from the supplied approved style family.

Make every instruction renderable. Do not include source paths, design analysis, checklist language, or explanations that cannot become pixels.

Before calling the image tool, verify that the call includes the user's local source image and exactly one selected file from `assets/examples/positive/`. Order and label the inputs consistently in the prompt even if the tool itself does not expose image labels. If tool limits prevent including both, preserve the user's source first, then encode the selected example's traits explicitly using `references/visual-reference-guide.md`; do not silently omit the style lock.

## Consistency Protocol

Favor iterative editing when a first pass is close in content but drifts in style. Official image-generation guidance supports using image inputs for edits and using high input fidelity when the available API exposes that option.

- Keep the same approved style anchor across retries. Never solve drift by randomly changing examples.
- On the first call, use the user source plus one style anchor and the four-paragraph prompt.
- If subject fidelity is wrong, restore only the missing identity anchors; never restore the source's complete photographic perspective, framing, object count, surface detail, or tonal modeling.
- If style fidelity is wrong, edit the first result with the same style anchor; request only style correction while freezing subject placement, silhouette, and recognizable content.
- When the result is compositionally correct but uniformly engraved, keep composition, paper, palette, text position, and subject identity fixed; vary line direction and density by depth; reopen selected paper gaps; retain medium directional hatching across readable planes and dense short carving at focal edges and dark accents.
- When the result has too little woodcut texture or resembles a duotone stamped photograph, keep composition and subject fixed; replace photographic grain, halftone dominance, and broad posterized fill with visible carved contours, directional hatch groups, pressure-varied gouges, and compact cross-cuts that follow the subject's actual planes.
- If the available image API exposes input fidelity, use high input fidelity for edits that must preserve faces, logos supplied by the user, architecture, or exact source details. Do not claim this option was used when the tool does not expose it.
- Run the Three-Axis Convergence Loop below for at most two automatic correction passes. Edit the closest result only for local failures; restart once from the original content reference plus canonical style anchor when abstraction or composition fails structurally.
- Treat variation in small carved marks as acceptable; treat changes to paper family, palette logic, negative-space ratio, integrated-print grammar, typography scale, or calm tempo as style drift.
- If the result remains too photographic, keep the locked style anchor, paper, palette, and identity anchors; edit the closest result by deleting secondary detail, opening paper gaps, compressing depth layers, and converting one continuous photographic region into abstract carved or ink-block structure.

## Three-Axis Convergence Loop

Treat **woodcut construction**, **structural linework**, **form-plus-style abstraction**, and **color/ink strength** as four equal hard gates. Do not finalize because only some gates look strong. Inspect every render both at normal size and as a small thumbnail, score each gate independently, and stop only when all four score `2`.

Use this scale:

- `0 — fail`: the required visual language is absent or primarily simulated by a photographic filter.
- `1 — partial`: visible evidence exists, but it is local, decorative, generic, or too weak to control the image.
- `2 — pass`: the feature visibly constructs the main subject and remains legible at thumbnail scale.

### Gate W — Woodcut construction

Score `2` only when selected main forms are built from relief-print logic: carved-away paper, irregular colored ink blocks, pressure-varied gouges, broken edges, compact cross-cuts, and visible unprinted gaps. The page must still read as a luminous contemporary zine. Halftone, duotone, stipple, grain, posterization, an engraved-photo surface, or a conventional black-and-cream full-page linocut cannot earn a pass.

### Gate L — Structural linework

Score `2` only when line groups explain form, material, depth, and light. Require at least two visibly different directional systems and three density zones. Reject one global horizontal texture, evenly distributed micro-scratches, outline-only drawing, or identical hatch behavior across water, rock, foliage, architecture, and sky.

### Gate A — Form and style abstraction

Score `2` only when the source has been visibly decomposed and rebuilt inside the locked style family. Preserve three to five identity anchors, but redesign framing and scale, compress depth to at most three layers, merge or remove secondary objects, and transform the **main form** through simplified planes, interrupted contours, exposed-paper voids, or repeated structural marks. A perspective-faithful full-scene tracing, even without a sticker border, scores `0`. Any complete scene enclosed by a white sticker border or photo-shaped container also scores `0`.

### Gate C — Color and ink strength

Score `2` only when the page contains a firm chromatic-dark anchor, a clearly legible secondary ink, and scene-appropriate saturated accent color, while untouched paper remains genuinely unprinted. Judge ink **coverage** separately from ink **strength**. A pale beige-gray or low-opacity monochrome result scores `0`, even if it has calm spacing and correct linework. A quiet scene with strong localized ink can score `2`.

After each render:

1. Record `W/L/A/C` scores and one concrete visual reason for every score below `2`.
2. Freeze every passing axis, the style anchor, calm tempo, palette logic, paper family, subject identity anchors, and successful composition decisions.
3. Choose the correction path:
   - **local edit** when all axes score at least `1` and the composition already follows the canonical hierarchy;
   - **composition restart** when `A=0`, the image traces the original camera view, the dominant form occupies more than about 40% of the page with continuous detail, or the page lacks a coherent untouched-paper region. Restart from the original CONTENT REFERENCE plus Example 02, not from the failed render, and explicitly discard its framing and perspective.
4. Apply only the correction clauses for failed axes:
   - failed `W`: replace photographic texture or broad stamped fill with carved voids, relief-cut edges, pressure-varied gouges, compact cross-cuts, and separated ink/paper shapes;
   - failed `L`: replace generic texture with directional, form-following line families differentiated by material and depth; restore open, medium, and dense zones;
   - failed `A`: remove documentary detail and rebuild one major region of the main cluster through merging, flattening, cropping, displacement, dissolution, or non-photographic carved planes—not merely by adding a small extra sticker.
   - failed `C`: keep the same paper area and composition, but strengthen the existing chromatic dark to firm printed saturation, restore a clearly visible secondary ink, and add or revive one small scene-relevant accent; do not solve weakness by increasing total dark coverage.
   - traditional-print drift: restart composition when the render uses a carved frame, dense black perimeter, mostly black/cream palette, filled corners, or exhaustive all-over cutting; restore luminous paper, colored inks, open edges, selective localized carving, and contemporary editorial spacing.
5. Re-score all four axes after the correction. A previously passing axis that regresses becomes failed and must be corrected in the next pass.
6. Stop after all scores are `2`, or after two correction passes. If the limit is reached, return the closest render only if all axes score at least `1`; otherwise state which gate failed instead of claiming style success.

The loop is diagnostic, not additive: do not respond to drift by piling on more paper grain, more tiny lines, more stickers, or more decorative marks. Change the construction logic of the failed axis while preserving the rest.

## Workflow

1. Inspect every user reference image before editing or generating.
2. Inspect Example 02 at full size and lock it as the canonical style anchor. Inspect or select another example only for an explicit exception described in `references/visual-reference-guide.md`.
3. Read `references/visual-reference-guide.md` and extract the emotional anchor and two or three recognizable cues from the user's source.
4. Route the scene through the atmosphere rules.
5. Choose A1, A2.5, or A3 abstraction; use A2.5 by default and state the three to five identity anchors plus the substantial region to abstract.
6. Select an integrated composition, open edge behavior, atmosphere-carving grammar, tonal density, palette, and typography mode.
7. Compile the four-paragraph prompt.
8. Generate the raster image using the user content reference and the single locked style reference, with their roles explicitly stated.
9. Run the Three-Axis Convergence Loop with the same style anchor. Perform targeted edits when any of these are true:
   - the result looks like a brown kraft-paper archival poster;
   - the photo remains an untreated rectangle or becomes a large closed sticker/blob;
   - the mood contradicts the source;
   - the image is fully realistic with no interpreted or abstract element;
   - the source camera framing, perspective, foreground-to-background sequence, or object density remains substantially intact;
   - one mountain, coast, facade, or other form fills most of the page with continuous photographic detail rather than simplified structural mass;
   - the apparent negative space is actually pale etched scenery rather than untouched paper;
   - dense dark ink covers more than roughly one quarter of the page;
   - a black carved border, dark corner foliage, or continuous perimeter encloses the scene;
   - the work reads as a traditional linocut, heritage print, tourist souvenir, or black-and-cream woodblock rather than a contemporary zine;
   - source logos, hotel names, shop signs, facade grids, or foliage are exhaustively transcribed instead of reduced to a few cues;
   - more than five source details compete for recognition or the result preserves the source with documentary completeness;
   - no substantial region has been converted into non-photographic carved, ink-block, contour-band, or exposed-paper structure;
   - the color is muddy, arbitrary, or too weak for a bright scene;
   - every ink layer is pale, gray, beige-shifted, translucent, or too close to the paper value;
   - the dominant structure lacks a firm chromatic-dark anchor or disappears at thumbnail scale;
   - a quiet, foggy, snowy, or solitary scene uses mood as justification for washed-out ink;
   - the composition loses the requested subject.
   - the output resembles antique engraving or an illustrated vintage book more than the approved reference family;
   - the approved style reference was available locally but was not included in the generation call;
   - more than one positive example was supplied without an explicit user request to hybridize them;
   - the prompt did not distinguish CONTENT REFERENCE from STYLE REFERENCE;
   - the final four-paragraph prompt omitted the style-lock opening sentence or the antique-engraving rejection.
   - the entire scene uses one uniform etched texture with no change in direction or density;
   - the subject has no clearly visible carved contours or directional hatch groups at normal viewing size;
   - halftone, duotone, posterization, or distressed ink carries the texture instead of relief-cut lines;
   - a pale mountain, forest, or architectural middle layer loses readability at thumbnail size.
   - `W`, `L`, `A`, or `C` scores below `2`, including regression after a correction.

## Hard Avoids

Avoid commercial advertising, tourism campaigns, product layouts, logos, CTA, oversized typography, giant initials, display-letter focal points, headline-dominant layouts, large white-bordered stickers, floating scenic blobs, kiss-cut landscape containers, duplicated mini-scenes, traditional black-and-cream linocuts, historical woodblock-print imitation, thick carved borders, dark corner framing, full-page black ink, binary high contrast, washed-out monochrome, pale beige-gray ink, uniformly lowered opacity, low-contrast faded etching, souvenir or heritage-print aesthetics, exhaustive sign transcription, explosive starbursts, long radiating rays, speed-line effects, motion streaks, urgent diagonals, aggressive convergence, frantic scatter, impact graphics, spiky halos, glossy sticker vinyl, scrapbook clutter, generic kawaii decoration, anime characters, cinematic lighting, 3D rendering, photorealistic reconstructions, full-bleed stock photography, muddy kraft paper, vintage packaging, fake handwriting overload, long clean text blocks, arbitrary color, excessive decorative objects, photo-shaped scenes disguised by duotone, generic engraving filters, and token abstraction made only from one tiny duplicated fragment.

## Output

Return the generated image. When the interface permits text after image generation, also provide the final prompt and a brief note containing:

- Mode: Standard
- Atmosphere route
- Abstraction level
- Recipe: layout / edge integration / palette / typography / texture
- One sentence explaining the interpretation

## Quality Gate

Confirm before finalizing:

- Did all four convergence scores reach `W2 / L2 / A2 / C2` after the final full re-check?
- Does the main form itself demonstrate abstraction, rather than outsourcing abstraction to a tiny secondary sticker?

- Does the whole image feel calm and unhurried, even when it is bright, colorful, urban, windy, or active?
- Does the background read as light woodcut paper rather than kraft paper?
- Is dense dark ink localized below roughly one quarter of the page, with no enclosing border or dark corner frame?
- Is that localized chromatic dark firmly saturated rather than diluted, with a visibly distinct secondary ink and suitable accent?
- Does the dominant structure separate clearly from the paper at thumbnail scale?
- Does the result read as a contemporary light editorial zine using selective carved marks—not as a traditional woodblock or linocut print?
- Do the woodcut marks visibly describe light, air, distance, weather, or movement instead of acting as uniform texture?
- Is strong tone built mainly from short dense marks rather than long radiating lines?
- Does the source photo read as an integrated interpreted print rather than a sticker or enclosed photo fragment?
- Does the mood follow the actual weather, light, subject, distance, and activity?
- Is at least one part selectively abstracted?
- Does the result preserve only three to five identity anchors while simplifying or removing secondary detail?
- Is roughly one substantial region visibly non-photographic rather than merely filtered?
- Is the main subject still recognizable where needed?
- Does color communicate emotion and remain fresh at thumbnail scale?
- Is the composition materially different from recent outputs?
- Does the poster retain breathing room and an indie editorial character?
- Is every piece of typography clearly smaller and quieter than the principal structural form?
- Are typography and print imperfections integrated rather than overlaid mechanically?
- Are carved contours and directional hatch groups unmistakably visible, with flat ink and exposed paper supporting rather than replacing them?
- Do foreground, middle distance, and far distance use visibly different mark densities rather than one global etching filter?
- Would the woodcut character remain obvious if paper grain, halftone dots, and photographic noise were removed?
- Did the image generation actually run?
- Was exactly one approved positive example selected and supplied to the image-generation call whenever local paths were available?
- Does the final prompt explicitly distinguish CONTENT REFERENCE from STYLE REFERENCE and make the single positive example authoritative for rendering?
- If a correction was needed, was it an edit of the closest result using the same locked anchor rather than a fresh generation with a different reference?
