---
name: aesthetic-extractor
description: Analyze one or more images to extract their aesthetic style, why they look good, design principles, visual elements, and reusable prompt vocabulary. Use when the user provides an image, moodboard, poster, illustration, photo, UI screenshot, product shot, interior image, social post, or visual reference and asks to improve taste, deconstruct aesthetics, summarize style, learn design logic, or generate prompts for a similar look.
---

# Aesthetic Extractor

## Overview

Turn visual references into teachable aesthetic analysis and practical generation guidance. Explain what can be observed, what is inferred, why it works, and which prompt terms are essential for recreating a similar mood or style.

## Core Workflow

1. Inspect the image before analyzing. If multiple images are provided, analyze each image first, then synthesize shared style DNA.
2. Separate observation from inference. Use "visible" for what is directly seen and "likely/inferred" for style labels, era, medium, or intent that cannot be verified from the pixels alone.
3. Describe the aesthetic in layers:
   - Overall style and mood
   - Core aesthetic judgment or visual insight
   - Subject and scene design
   - Composition and spatial structure
   - Color palette and contrast
   - Light, shadow, and atmosphere
   - Texture, material, surface, and detail density
   - Typography, layout, and graphic language when present
   - Cultural, genre, platform, or art-historical references when relevant
4. Start the response with two one-sentence summaries: first the style, then the most important aesthetic judgment.
5. Explain why it looks good through design principles, not generic praise.
6. Extract reusable prompt vocabulary and generation constraints.
7. Give the user one compact prompt recipe and one optional negative prompt or avoidance list.

## Output Structure

Use this structure unless the user requests another format:

### 1. 风格一句话

Give a concise style summary in Chinese. Include medium, mood, and the most distinctive visual signature.

### 2. 关键审美判断一句话

Give the most important insight in one sentence: the core design judgment that explains the image's beauty. Make it teach the user how to see the image.

Good examples:

- "这张图高级的地方不是细节多，而是用大面积留白把孤独感和空间感放大。"
- "它的美感来自动静对抗：稳定的村庄托住了翻涌的天空。"
- "真正决定质感的是克制的低饱和配色，而不是某一个具体元素。"

### 3. 这张图好看的原因

List 4-7 concrete reasons. Tie each reason to a visible design choice:

- Composition: balance, rhythm, framing, negative space, hierarchy, symmetry/asymmetry, depth, leading lines.
- Color: palette discipline, temperature contrast, saturation control, value contrast, accent color.
- Light: direction, softness, highlight placement, shadow shape, glow, haze, reflections.
- Detail: focal detail versus quiet areas, texture contrast, handcrafted imperfections, material realism.
- Emotion: narrative tension, intimacy, restraint, scale, nostalgia, freshness, elegance, playfulness.

Avoid vague claims like "高级感" unless you define what creates it.

### 4. 设计原理拆解

Name the principles and explain how the image applies them. Prefer concrete phrasing:

- "大面积低信息背景让主体拥有呼吸感。"
- "高明度背景 + 低饱和主体让画面显得安静。"
- "重复的几何边缘建立秩序，局部有机纹理打破机械感。"

### 5. 元素清单

Extract reusable elements:

- Subject / 主体
- Setting / 场景
- Composition / 构图
- Palette / 色彩
- Lighting / 光线
- Material / 材质
- Camera or perspective / 镜头视角
- Graphic or typography elements / 图形与字体, if any
- Finishing / 后期质感, such as grain, bloom, paper texture, film tone, sharpness, blur

### 6. 生成相似美感的必备提示词

Split prompt terms into tiers:

- 必备词: Without these, the image would lose the core style.
- 加分词: Useful refinements that strengthen the look.
- 慎用词: Words that may push the result away from the reference.

Provide bilingual prompt vocabulary when useful:

```text
中文关键词: ...
English keywords: ...
```

### 7. 可直接使用的提示词

Write a ready-to-use prompt that captures the image's style without copying private identity or protected characters. Keep it modular:

```text
[主体], [场景], [构图], [光线], [色彩], [材质/细节], [风格/媒介], [镜头/渲染], [后期质感]
```

If the image contains a living person, private person, logo, copyrighted character, or identifiable brand, avoid instructing direct replication. Extract general visual traits instead.

### 8. 避免跑偏

Add 3-6 negative prompt terms or practical warnings. Focus on common failure modes: over-saturation, messy background, harsh contrast, plastic skin, extra text, cluttered details, generic stock-photo lighting, incorrect era, wrong medium.

## Analysis Standards

- Be specific. Replace "很有氛围" with the concrete cause: low contrast haze, warm rim light, large negative space, shallow depth of field, muted palette, etc.
- Teach taste. Explain the design logic so the user learns how to see, not just what to type.
- Make the key aesthetic judgment sharp and memorable. It should be a transferable rule of seeing, not a recap of the style sentence.
- Preserve ambiguity. If the style could be "Japanese minimalism" or "Scandinavian editorial," say what visual evidence supports each, then choose the stronger reading.
- Do not invent unseen details. If the image crop hides context, say so.
- Do not overfit to one label. Prefer "style stack" such as "editorial product photography + soft brutalist set design + muted warm neutrals."
- When comparing multiple images, identify common denominators and outliers.

## Prompt Extraction Rules

When deriving generation prompts:

1. Start with stable visual grammar: subject, composition, palette, light, material, medium.
2. Add style references only when they are visually justified.
3. Prefer descriptive terms over named artists unless the user explicitly asks for artist-like references.
4. Use camera and rendering terms only when relevant:
   - Photo: focal length, depth of field, film grain, natural light, studio light, editorial photography.
   - Illustration: brushwork, line weight, gouache, watercolor, risograph, flat vector, ink wash.
   - 3D/product: octane render, clay material, subsurface scattering, global illumination, bevels.
   - UI/graphic: grid system, typography weight, spacing, icon style, card density, contrast ratio.
5. Include constraints that preserve taste: restrained palette, clean negative space, coherent material, controlled detail, single focal point.

## Tone

Write in clear Chinese by default. Keep the analysis readable for non-designers, but use precise design vocabulary. If the user asks for a prompt only, still include a brief reason for the essential words so the prompt teaches the aesthetic logic.
