---
updated: 2026-05-21
sources: [https://github.com/AgriciDaniel/claude-obsidian]
related: [[LLM-Wiki模式]], [[claude-obsidian]], [[wiki迁移方案]]
---

# Wiki 三层目录结构

当 wiki 页面超过 30-50 页时，平铺根目录难以导航。claude-obsidian 提出的 concepts/entities/sources 三层分类策略。

## 三层含义

### `concepts/` — 抽象概念
从来源中提炼的**可复用知识单元**。独立于具体来源，可被多个来源引用。

示例：`同理心`、`增强回路`、`峰终定律`、`Hot-Cache`、`LLM-Wiki模式`

特征：
- 有明确定义
- 跨来源适用
- 概念本身不随时间失效

### `entities/` — 人物 / 组织 / 产品
**现实世界中的具体实体**。记录其背景、观点、与其他实体的关系。

示例：`梁宁`、`罗振宇`、`Andrej-Karpathy`、`claude-obsidian（工具）`

特征：
- 有唯一身份
- 随时间会有新动态（可更新）
- 关系网络丰富

### `sources/` — 来源摘要
每个**原始资料**对应一个摘要页。记录来源内容、提炼出的主要概念、摘要与评价。

示例：`梁宁-产品思维30讲`、`罗胖60秒十年合集`、`claude-obsidian-repo`

特征：
- 与原始文件一一对应
- 作为知识的溯源入口
- 列出该来源衍生的所有 concepts/ 页面

## 完整目录结构

```
wiki/
├── CLAUDE.md          # Schema 配置（根目录，必须）
├── index.md           # 全量目录（根目录）
├── log.md             # 操作日志（根目录）
├── hot.md             # 热缓存（根目录）
│
├── concepts/          # 抽象概念（数量最多）
│   ├── 同理心.md
│   ├── 增强回路与调节回路.md
│   └── ...
│
├── entities/          # 人物/组织/产品
│   ├── 梁宁.md
│   ├── 罗振宇.md
│   └── ...
│
└── sources/           # 来源摘要
    ├── 梁宁-产品思维30讲.md
    ├── 罗胖60秒十年合集.md
    └── ...
```

## Obsidian 中的行为

Obsidian 的 `[[wikilink]]` 按**文件名**解析，与目录层级无关。
迁移到子目录后，所有现有的 `[[同理心]]` 链接**无需修改**，Obsidian 自动找到 `concepts/同理心.md`。

> 前提：文件名在整个 vault 中唯一（避免 concepts/ 和 entities/ 下有同名文件）。

## 何时迁移

- 页面数 < 30：平铺即可，无需分层
- 页面数 30-80：迁移到三层结构，同时更新 index.md
- 页面数 > 80：可在三层内继续细分（如 `concepts/产品/`、`concepts/AI/`）

当前知识库（26 页）已接近迁移临界点，详见 [[wiki迁移方案]]。
