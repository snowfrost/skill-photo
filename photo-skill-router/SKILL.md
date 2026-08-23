---
name: photo-skill-router
description: skill-photo 套件的总路由引导。当用户提出照片风格化、海报、明信片、zine、贴纸、邮票、地图、插画配图、IP 提示词、摄影场景设计、审美分析等需求、但不确定该用套件里哪个具体 skill 时，由本 skill 先理解需求、匹配到最合适的子 skill，再通过 @skill:<目标skill> 触发执行。属于 skill-photo 套件的入口引导，不直接处理图像，只负责路由与触发。
---

# photo-skill-router（照片套件路由引导）

## 职责

1. **理解需求**：读取用户的原始需求，提取「意图」（要什么效果/产物）与「输入」（照片/主题/描述/参考）。
2. **匹配 skill**：对照下方路由表，选出最合适的一个子 skill。
3. **确认与触发**：一句话告知用户将使用哪个 skill 及原因；若需求模糊，最多问一轮关键选项（如风格、语言、输出形式），然后通过 `@skill:<目标skill目录名>` 触发该 skill 的工作流。
4. **多步需求**：若需求需要先后使用多个 skill（例如先 `aesthetic-extractor` 分析审美、再用某生成类 skill），按依赖顺序依次触发。

## 路由表

### 海报 / 演示类
| 用户需求 | 目标 skill |
|---|---|
| 高级编辑感 3:4 竖版海报（Liminal Frame 构图） | `liminal-editorial-posters` |
| 拓印/民俗图录/古物拓片风格海报（3:4、上下 1:1、几何骨架、木刻拓印质感） | `ink-rubbing-poster` |
| 极简诗意纸纹理 zine 海报（大留白、单色点缀、实验排版） | `gc-minimal-zine-poster-v0-3` |
| 平静木刻版画 zine / 主题氛围版画 | `joy-calm-woodcut-zine` |
| 像素风格海报 / 像素画提示词 | `pixel-style-poster-skill` |
| 干净竖版编辑风抽象艺术作品 | `photo-abstract-editorial` |
| 日常照片 → "正在播放"音乐记忆海报 | `photo-now-playing` |
| 横向翻页网页 PPT / 演示文稿（HTML） | `guizang-ppt-skill` |

### zine / 明信片 / 贴纸 / 邮票类
| 用户需求 | 目标 skill |
|---|---|
| 照片 → 杂志感明信片 | `photo-to-zine-postcard` |
| 照片 → 单张场景蒸馏 zine | `scene-distillation-zine-v1-3` |
| 照片 → 场景合集 zine（多场景汇聚） | `scenes-gathered-zine-v1-3` |
| 旅行照片 → 可收藏记忆贴纸卡 | `travel-memory-sticker-card` |
| 照片 → 邮票档案 / 邮票风格收藏册 | `make-photo-stamp-archive` |

### 照片重塑 / 焕新 / 抽象 / 场景设计类
| 用户需求 | 目标 skill |
|---|---|
| 普通照片/日常快照焕新、提升质感 | `photo-revival` |
| 旅行照片抽象化、意象化 | `travel-photo-abstraction` |
| 影像转译 / 重编 / 视觉叙事改写 | `visual-memory-translator` |
| 摄影场景设计（中文，参数/器材/案例配方） | `photodesign-skill-zh` |
| 摄影场景设计（英文） | `photodesign-skill-en` |

### 插画 / 手绘 / 图解类
| 用户需求 | 目标 skill |
|---|---|
| 中文文章配图（Ian 小黑手绘风、纯白纸面） | `ian-xiaohei-illustrations` |
| 把自有 IP 角色 + 品牌色做成可复用线稿提示词模板 | `ip-all-png-template` |
| 漫画风格图解 / 知识图解生成 | `comic-guide` |
| 粗糙 MS Paint 风事件解释图 / 事故示意图 | `paint-doodle` |

### 提示词 / 分析 / 地图 / 期刊类
| 用户需求 | 目标 skill |
|---|---|
| 审美拆解、风格提取、设计原则、提示词学习 | `aesthetic-extractor` |
| 自然语言生成可商用城市打卡地图（GIS+GPT） | `map-creator` |
| 主题可编辑电子期刊 / 杂志排版 | `theme-editable-journal` |

## 路由规则

1. **意图契合度优先**：先看用户要什么「产物」（海报/明信片/贴纸/地图…），再考虑风格与输入，命中唯一时直接触发。
2. **候选多个时**：按「产物匹配 > 风格匹配 > 语言偏好（中/英）> 输入类型」排序；仍并列时向用户一句话确认。
3. **语言偏好**：中文需求默认中文类 skill（如 `photodesign-skill-zh`）；用户明确要英文版才走英文类。
4. **明确边界**：本套件只路由「照片/视觉类」需求；若需求明显不属于本套件（纯文本写作、办公、投资等），不强行套用，直接说明应使用其他套件。
5. **触发方式**：确认后使用 `@skill:<目标skill目录名>` 调用；目标 skill 的 SKILL.md 是权威流程，本路由只负责指路，不替代其执行。

## 说明

- 本 skill 随 skill-photo 套件分发，安装到 `~/.workbuddy/skills/` 后即可作为照片类任务的统一入口。
- 路由表若与套件内实际 skill 不一致，以对应 skill 目录下的 SKILL.md 为准。
