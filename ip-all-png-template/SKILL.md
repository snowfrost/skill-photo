---
name: ip-all-png-template
description: Generate reusable image prompts for Chinese article illustrations in a fixed Ian-style minimal white-paper hand-drawn sketch style, with only the IP character and color palette left for the user to fill. Use when the user wants article illustrations, PNG prompts, shot lists, knowledge-card illustrations, or wants to turn their own IP role and brand colors into a repeatable simple-line-drawing prompt template.
---

# IP All PNG Template

## Purpose

Create image-generation prompts for Chinese article illustrations with a reusable personal IP character.

This is a delivery-ready template. It keeps the base visual style fixed: Ian-style minimal white-paper hand-drawn conceptual illustration, like a clean simple-line sketch for article body images.

Only the creator-specific parts are removed: fixed creator identity, fixed IP character, fixed companion, and fixed color palette. Before generating prompts, ask the user to fill in their own IP character and color rules, then inject those rules into every prompt.

Default to clean, sparse, conceptual simple-line article illustrations. Do not drift into dense Xiaohongshu card/poster design unless the user explicitly asks for a card, poster, or cover.

This skill is prompt-first. Produce shot lists and single-image prompts. Do not call image generation unless the user explicitly asks to generate images.

## Required Reference

Read `references/ip-visual-template-json.md` when the user needs a structured JSON spec, a reusable style block, or detailed IP constraints.

## Fixed Base Drawing Style

Do not remove or replace the base drawing style. This template always keeps the following visual foundation:

```text
基础画风：
16:9 横版中文文章配图，简笔画风格，纯白背景，大面积留白。
整体像白纸上的手绘概念草图，而不是海报、卡片或正式信息图。
画面以细黑色手绘线条为主，线条略微自然抖动，有手画感。
结构清晰、元素少，一张图只表达一个核心观点。
可以使用少量中文手写标注，通常 2-4 个短标签。
构图偏“知识解释图 / 产品草图 / 白板涂鸦”，用低技术感的隐喻物件表达概念，比如纸盒、抽屉、漏斗、天平、门、梯子、管道、线团、黑箱、旧机器等。
IP 角色只作为小引导者出现，默认占画面宽度 8%-12%，不要成为画面主体。
整体干净、克制、轻松，有一点荒诞的概念表达，但不要做成小红书密集卡片、PPT 信息图、商业海报、3D 渲染或复杂架构图。
```

Only these two parts are user-fill variables:

1. IP character formula.
2. Color palette.

## User-Fill IP Formula

Before writing image prompts, collect or infer the user's IP settings. If the user has not provided them, show this fill-in template and ask them to complete it:

```text
IP character formula:
年龄:
性别:
头发颜色:
头发长短/发型:
衣服颜色:
衣服款式:
衣服长短:
裙子/裤子颜色:
裙子/裤子款式:
裙子/裤子长短:
鞋子颜色:
鞋子款式:
鞋子长短/高度:
可选配饰:
可选陪伴物/宠物/道具:
角色气质:

Color palette:
主色:
辅助色:
强调色:
背景色:
禁用颜色:
整体风格关键词:
```

The IP character should remain fixed across images. The exact character details can change only when the user explicitly updates the formula.

## Core Style

Use this visual direction:

- 16:9 horizontal Chinese article illustration by default.
- Fixed base style: Ian-style minimal white-paper hand-drawn simple sketch.
- Pure white background by default; use another simple background only if the user explicitly asks.
- Thin black hand-drawn line art first; use color sparsely unless the user asks for a richer card/poster style.
- Large whitespace and clear composition, closer to a whiteboard/product sketch or article doodle than a dense poster.
- Sparse Chinese handwritten annotations, usually 2-4 labels.
- One image explains one core action, structure, status, or metaphor.
- The user-defined IP character must participate in the core visual action.
- If the user defines a companion object, pet, or mascot, keep it secondary and supportive.
- Do not change the base drawing style when replacing the IP character or color palette.

## Custom IP Rules

The protagonist must follow the user's filled IP formula:

- Keep age, gender, hair color, hairstyle, clothing, bottoms, shoes, accessories, and overall temperament consistent.
- Use the user's palette as the source of all accent colors.
- Do not introduce a new hairstyle, outfit, companion, or brand color unless the user asks.
- Default character scale: the IP character should be a small guide character, around 8%-12% of the canvas width, unless the user explicitly asks for a character-focused image.
- The IP character should perform the core conceptual action: pointing, carrying, sorting, opening, connecting, repairing, weighing, holding notes, guiding a companion, or operating a low-tech metaphor object.
- If a companion is defined, it may assist, observe, hold a small sign, peek from a module, or sit beside the main action.

## Prompt Workflow

1. Digest the supplied article, topic, outline, or idea.
2. Confirm the user's IP formula and color palette. If missing, ask the user to fill the template in `User-Fill IP Formula`.
3. Identify the strongest visual anchor: core judgment, before/after change, workflow, bottleneck, route, common pitfall, or role-state shift.
4. Choose one structure type:
   - workflow
   - system partial
   - before-after
   - role state
   - concept metaphor
   - method layers
   - map route
   - mini comic
5. Invent a fresh low-tech metaphor using 1-2 objects such as paper box, drawer, old machine, funnel, scale, mailbox, door, well, ladder, pipe, thread ball, gate, turntable, black box, hole punch, noodle press, clothesline, or strange desk.
6. Make the user-defined IP character participate in the core action.
7. Output one prompt per image. Do not merge multiple images into one prompt unless the user asks for a multi-panel mini comic.

## Default Shot List Rules

If the user asks for a 配图方案 or shot list, return 3-6 image ideas by default. For each idea include:

- Placement after which paragraph or section.
- Image theme.
- Core idea.
- Structure type.
- What the IP character does.
- What the optional companion/object does.
- Suggested objects.
- Suggested Chinese labels.

## Single Prompt Template

Use and adapt this template:

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual style:
Ian-style minimal white-paper Chinese article illustration. Pure white background by default. Minimalist thin black hand-drawn line art with slightly wobbly pen lines. Lots of empty space. Sparse handwritten Chinese annotations. Clean conceptual product-sketch feeling, like a simple-line article doodle. Not a poster, not a cute card, not a dense Xiaohongshu layout unless explicitly requested.

User-defined IP character:
{年龄} {性别}, {头发颜色} {头发长短/发型}, wearing {衣服颜色} {衣服款式} {衣服长短}, {裙子/裤子颜色} {裙子/裤子款式} {裙子/裤子长短}, {鞋子颜色} {鞋子款式} {鞋子长短/高度}. Optional accessories: {可选配饰}. Optional companion/object: {可选陪伴物/宠物/道具}. Character temperament: {角色气质}. The IP character should usually be a small guide character, around 8%-12% of the canvas width, not the visual centerpiece. The IP character must perform the core conceptual action.

Color palette:
Main color: {主色}. Secondary color: {辅助色}. Accent color: {强调色}. Background color: {背景色}. Forbidden colors: {禁用颜色}. Overall style keywords: {整体风格关键词}. Use colors consistently and sparsely. Do not invent a new palette.

Theme:
{theme}

Structure type:
{workflow | system partial | before-after | role state | concept metaphor | method layers | map route | mini comic}

Core idea:
{core idea}

Composition:
{where the IP character is, what they do, where the companion/object is, main object, how information or action flows}

Suggested elements:
{element 1} / {element 2} / {element 3} / {element 4}

Chinese handwritten labels:
{label 1} / {label 2} / {label 3} / {label 4} / {optional label 5}

Color use:
White background dominates 65%-80% by default. Black line art dominates structure and text. User-defined main/accent colors appear only on the IP character, key arrows, labels, or emphasis marks. Keep colors sparse unless the user asks for a poster/card.

Constraints:
One image explains only one core structure. Keep the IP character small by default, around 8%-12% of the canvas width, while the main visual focus should be the workflow, object metaphor, system structure, or page mockup. Preserve at least 45%-55% blank space. Use at most 2-4 short Chinese labels. Do not write a top-left diagram title. Do not change the base Ian-style simple-line white-paper drawing style. Do not make it PPT, formal infographic, complex architecture, realistic portrait, 3D render, generic anime character, paper-doll face, stick-figure face, creepy simplified face, blank expressionless face, mascot-only design, childish poster, sticker-filled Xiaohongshu card, dense knowledge card, decorative scrapbook, or cute commercial illustration unless explicitly requested. Do not change the user's IP formula or color palette.
```

## Output

For prompt-only tasks, return:

- A short shot list or prompt list.
- Each prompt as a separate fenced text block.
- A compact note of which prompt is most stable and which is more experimental.

For JSON tasks, use the reference JSON as the base and customize only the fields the user asks to change.
