# Make Photo Stamp Archive

**简体中文** · [English](README.en.md) · [日本語](README.ja.md)

Make Photo Stamp Archive 是一个 Codex Skill：它可以把一张或多张照片转化为安静、克制的档案拼接作品——一侧忠实保留原照片，另一侧使用暖白纸张与根据主体定制的手工图章，两块画面以笔直边界直接拼接。

调用名称为 `make-photo-stamp-archive`。

## 核心能力

- 忠实保留原照片中的人物、面孔、物件、建筑、文字、色彩关系与场景逻辑。
- 默认采用横向左右直拼，也可按要求改成上下拼接；主分界始终清晰、笔直。
- 根据主体设计圆形、方框、横向全景、拱形或自定义轮廓图章。
- 呈现干墨、磨损网点、压力不均、边缘缺墨与轻微套色偏差等真实手压质感。
- 支持只修改图章形状、边框、大小、位置、墨色、标题、纸张年代感或拼接方向。
- 多张照片会分别生成独立成品，不合并成拼贴画。

## 视觉系统

- **照片区：**忠实、真实，默认约占画布的 55%。
- **纸张区：**干净的暖白档案纸，带轻微纤维与扫描痕迹，默认约占画布的 45%。
- **图章组：**体量小、靠角落放置，约占纸张区的 30%。
- **留白：**纸张区约 70% 保持安静、空白。
- **文字：**在图章附近放置小号褪色打字机文字，不覆盖图章。
- **气质：**克制、平面、可触摸、档案化，像一段被保存的记忆。

最终结果始终是一张平面成品，不会做成书本样机、剪贴簿、前后对比板、缩小照片贴片或装饰性海报展示。

## 作例

| 作例 01 | 作例 02 |
| --- | --- |
| ![照片与图章档案拼接作例 01](https://github.com/user-attachments/assets/5fd44aba-e5f1-4f24-9271-89e850f171c5) | ![照片与图章档案拼接作例 02](https://github.com/user-attachments/assets/27fb0c46-d67f-4404-bbaf-e73e27f8202c) |

| 作例 03 |
| --- |
| ![照片与图章档案拼接作例 03](https://github.com/user-attachments/assets/9515aac2-448b-4426-ad34-70b88edc590a) |

## 运行要求

- Codex，或其他兼容 Skill 的运行环境。
- 能够读取图片，以检查源照片。
- 能够生成或编辑图片，以制作和修改最终成品。

本 Skill 包不包含 API Key、外部字体、脚本或需要额外下载的运行素材。最终画质与源照片保真度取决于宿主环境可用的图像模型。

## 安装

```bash
git clone https://github.com/Dlcccc71913/skill-make-photo-stamp-archive.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill-make-photo-stamp-archive \
  "${CODEX_HOME:-$HOME/.codex}/skills/make-photo-stamp-archive"
```

如果 Skill 没有立即出现，请重启 Codex。

## 使用

```text
使用 $make-photo-stamp-archive，把这张照片制作成带定制图章的档案直拼作品。
```

进行局部修改时：

```text
保持照片区完全不变，只把图章缩小 10%，并移动到右上角。
```

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── prompt-template.md
├── README.md
├── README.en.md
├── README.ja.md
└── LICENSE
```

## 许可证

[MIT](LICENSE)
