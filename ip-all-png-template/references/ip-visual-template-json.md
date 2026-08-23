# User-Defined IP Visual JSON Template

Use this as the base JSON when the user asks for a reusable spec, prompt schema, or style extraction.

This file is intentionally generic only in the IP identity and palette fields. The base visual style remains fixed: Ian-style minimal white-paper hand-drawn simple-line article illustration.

```json
{
  "style_name": "User Defined IP Ian-style Article Illustration",
  "core_conversion": {
    "from": "fixed creator-specific IP inside an Ian-style simple-line article illustration",
    "to": "user-defined IP character and user-defined palette inside the same base drawing style",
    "rule": "keep the Ian-style clean conceptual white-paper hand-drawn illustration structure, inject only the user's own IP identity and color palette, avoid accidental creator-specific details"
  },
  "canvas": {
    "default_aspect_ratio": "16:9",
    "orientation": "horizontal",
    "usage": "Chinese article body illustration, knowledge explanation image, PNG prompt"
  },
  "fixed_base_drawing_style": {
    "editable": false,
    "summary_cn": "16:9 横版中文文章配图，简笔画风格，纯白背景，大面积留白，像白纸上的手绘概念草图。",
    "rules": [
      "pure white background by default",
      "thin black hand-drawn line art",
      "slightly wobbly natural pen lines",
      "large whitespace",
      "one image explains one core idea",
      "2-4 short handwritten Chinese labels",
      "knowledge explanation image / product sketch / whiteboard doodle feeling",
      "low-tech metaphor objects such as paper box, drawer, funnel, scale, door, ladder, pipe, thread ball, black box, old machine",
      "IP character appears as a small guide, around 8%-12% of canvas width by default",
      "avoid dense Xiaohongshu cards, PPT infographics, commercial posters, 3D renders, and complex architecture diagrams"
    ],
    "only_user_fill_variables": [
      "ip_formula",
      "color_palette"
    ]
  },
  "ip_formula": {
    "required": true,
    "fields": {
      "age": "",
      "gender": "",
      "hair_color": "",
      "hair_length_or_style": "",
      "top_color": "",
      "top_style": "",
      "top_length": "",
      "bottom_color": "",
      "bottom_style": "",
      "bottom_length": "",
      "shoe_color": "",
      "shoe_style": "",
      "shoe_length_or_height": "",
      "optional_accessories": "",
      "optional_companion_pet_or_prop": "",
      "character_temperament": ""
    },
    "spoken_formula_cn": "年龄 + 性别 + 头发颜色长短 + 衣服颜色款式长短 + 裙子/裤子颜色款式长短 + 鞋颜色款式长短"
  },
  "color_palette": {
    "required": true,
    "fields": {
      "main_color": "",
      "secondary_color": "",
      "accent_color": "",
      "background_color": "",
      "forbidden_colors": "",
      "overall_style_keywords": ""
    },
    "rule": "use only the user's palette; do not invent a new brand palette"
  },
  "main_character": {
    "required": true,
    "role": "core conceptual action subject",
    "appearance": {
      "style": "user-defined IP character inside an Ian-style minimal white-paper hand-drawn article illustration",
      "age": "{age}",
      "gender": "{gender}",
      "hair_color": "{hair_color}",
      "hair_length_or_style": "{hair_length_or_style}",
      "top": "{top_color} {top_style} {top_length}",
      "bottom": "{bottom_color} {bottom_style} {bottom_length}",
      "shoes": "{shoe_color} {shoe_style} {shoe_length_or_height}",
      "accessories": "{optional_accessories}",
      "expression": "{character_temperament}, friendly, focused, approachable",
      "rendering": "clean simple-line hand-drawn article illustration, no glossy shading, no over-rendered portrait",
      "default_scale": "small guide character, around 8%-12% of canvas width unless user asks for character-focused image",
      "composition_role": "supporting guide beside the workflow or metaphor object, not the visual centerpiece"
    },
    "actions": [
      "pointing to key idea",
      "carrying notes",
      "sorting content blocks",
      "opening a door",
      "connecting modules with string",
      "repairing a low-tech machine",
      "weighing options",
      "holding sticky notes",
      "guiding the optional companion",
      "operating a metaphor device"
    ],
    "forbidden": [
      "realistic portrait",
      "3D render",
      "generic anime character unrelated to the user formula",
      "paper-doll face",
      "stick-figure face",
      "creepy simplified face",
      "blank expressionless face",
      "mascot-only design",
      "changing the user's age/gender/hair/outfit/bottoms/shoes without request",
      "using creator-specific details not provided by the user"
    ]
  },
  "optional_companion": {
    "required": false,
    "name": "{optional_companion_pet_or_prop}",
    "role": "secondary action helper if provided by the user",
    "actions": [
      "sitting beside the IP character",
      "being held by the IP character",
      "holding a small sign",
      "peeking from an info box",
      "watching the main action",
      "pushing a tiny note",
      "guarding an output object"
    ],
    "rule": "do not add a companion if the user did not define one"
  },
  "visual_style": {
    "keywords": [
      "Ian-style minimal white-paper hand-drawn illustration",
      "simple-line drawing",
      "Chinese article body image",
      "clean conceptual sketch",
      "thin hand-drawn outlines",
      "sparse accent colors",
      "large whitespace",
      "readable handwritten Chinese labels",
      "clever low-tech metaphor"
    ],
    "avoid": [
      "commercial poster unless requested",
      "dense Xiaohongshu knowledge card unless requested",
      "sticker-filled scrapbook",
      "cute card layout unless requested",
      "PPT infographic",
      "formal flowchart",
      "complex architecture",
      "children illustration",
      "dark cyberpunk unless requested",
      "real app screenshot",
      "dense labels",
      "top-left diagram title"
    ]
  },
  "color_distribution": {
    "background": {
      "colors": ["{background_color}"],
      "ratio": "65%-80%",
      "usage": "simple background and whitespace"
    },
    "outline_and_text": {
      "color": "black or user-specified dark neutral",
      "ratio": "18%-30%",
      "usage": "main hand-drawn outlines and readable Chinese text"
    },
    "main_color": {
      "color": "{main_color}",
      "ratio": "2%-10%",
      "usage": "IP clothing, key visual mark, or primary emphasis"
    },
    "secondary_color": {
      "color": "{secondary_color}",
      "ratio": "0%-8%",
      "usage": "secondary notes, small fills, helper marks"
    },
    "accent_color": {
      "color": "{accent_color}",
      "ratio": "0%-6%",
      "usage": "arrows, warnings, key results, active marks"
    }
  },
  "layout": {
    "main_subject_ratio": "main object or workflow 40%-60%; IP character 8%-12% of canvas width by default",
    "blank_space": "45%-55% minimum",
    "label_count": "2-4 short Chinese labels",
    "words_per_label": "2-8 Chinese characters preferred",
    "rule": "one image explains one core idea"
  },
  "composition_patterns": [
    "workflow",
    "system partial",
    "before-after",
    "role state",
    "concept metaphor",
    "method layers",
    "map route",
    "mini comic"
  ],
  "metaphor_objects": [
    "paper box",
    "drawer",
    "old machine",
    "funnel",
    "scale",
    "mailbox",
    "door",
    "well",
    "ladder",
    "pipe",
    "thread ball",
    "gate",
    "turntable",
    "black box",
    "hole punch",
    "noodle press",
    "clothesline",
    "strange desk"
  ],
  "prompt_template": {
    "core": "Generate one standalone 16:9 horizontal Chinese article illustration in an Ian-style minimal white-paper hand-drawn simple-line style. Use a pure white background by default, thin black slightly wobbly line art, sparse user-defined accent colors, large whitespace, and only 2-4 readable handwritten Chinese annotations. Keep the base drawing style fixed; only replace the IP character and color palette. The fixed IP is the user's own character: {age} {gender}, {hair_color} {hair_length_or_style}, wearing {top_color} {top_style} {top_length}, {bottom_color} {bottom_style} {bottom_length}, {shoe_color} {shoe_style} {shoe_length_or_height}, with optional accessories {optional_accessories} and optional companion/object {optional_companion_pet_or_prop}. The IP character must participate in the core conceptual action as a small guide character around 8%-12% of canvas width by default, while the main visual focus stays on the workflow, object metaphor, or structure. Use palette: main {main_color}, secondary {secondary_color}, accent {accent_color}, background {background_color}; avoid {forbidden_colors}. One image explains one core idea. Avoid PPT, formal infographic, realistic portrait, 3D render, generic character unrelated to the formula, complex architecture, dense labels, sticker-filled cards, decorative scrapbook, and top-left diagram titles.",
    "variables": {
      "theme": "",
      "core_idea": "",
      "structure_type": "",
      "ip_character_action": "",
      "optional_companion_action": "",
      "main_objects": [],
      "chinese_labels": []
    }
  }
}
```
