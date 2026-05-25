---
updated: 2026-05-25
sources: [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f]
related: [[LLM-Wiki模式]], [[Andrej-Karpathy]], [[Wiki三层目录结构]], [[Hot-Cache]]
---

# LLM Wiki（Karpathy gist）

原文：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
作者：Andrej Karpathy
性质：idea file，设计为直接粘贴给 LLM Agent 使用，描述模式而非具体实现

---

## 核心主张

大多数人用 LLM 处理文档的方式是 RAG：上传文件 → 查询时检索片段 → 临时生成答案。知识没有积累，每次提问都从零开始。

**LLM Wiki 不同**：LLM 增量构建并维护一个持久 wiki——结构化、互相链接的 markdown 文件集。新来源到达时，LLM 读取它、提取关键信息，整合进已有 wiki（更新实体页、修订概念摘要、标注矛盾、加强综合）。**知识编译一次，持续更新，而非每次查询重新发现。**

> "cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read."

---

## 三层架构

**Raw Sources（原始资料）** — 不可变，用户策展。LLM 只读，从不修改。

**The Wiki** — LLM 生成并维护的 markdown 文件目录。摘要页、实体页、概念页、对比、综述。LLM 拥有这一层的完整写权限。

**The Schema**（CLAUDE.md / AGENTS.md）— 告诉 LLM wiki 结构是什么、约定是什么、摄入/查询/维护的工作流。这是让 LLM 成为"有纪律的 wiki 维护者"而非"通用聊天机器人"的关键配置文件。你和 LLM 共同演进它。

---

## 三个操作

**Ingest** — 新来源 → LLM 读取 → 与用户讨论要点 → 写摘要页 → 更新 index → 更新相关实体/概念页 → 追加 log。一个来源可能触及 10-15 个 wiki 页面。

**Query** — 搜索 index.md 定位相关页 → 读取 → 合成回答（可以是 markdown 页、对比表、Marp 幻灯片、图表）→ **有价值的答案存回 wiki**，不让分析消失在对话历史里。

**Lint** — 定期健康检查：矛盾内容、孤立页面（无入链）、过时断言、缺失交叉引用、有提及但无独立页面的重要概念、可用网络搜索填补的数据空白。

---

## 为什么有效

> "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping."

人类放弃 wiki 的原因：维护负担增速 > 价值增速。LLM 不厌倦、不遗忘交叉引用、一次可编辑 15 个文件，维护成本趋近于零。

精神上承接 Vannevar Bush 1945 年的 **Memex** 设想——私人的、主动策展的知识库，文档间的关联链接与文档本身同等重要。Bush 未解决的是"谁来维护"，LLM 解决了。

---

## Index 与 Log 的分工

- `index.md` — 内容导向，全页面目录 + 一行摘要 + 分类。查询时先读这里定位页面。
- `log.md` — 时序导向，追加写入。格式 `## [YYYY-MM-DD] ingest | 标题` 便于 grep 解析。

---

## 工具推荐

- **Obsidian** — wiki 的阅读/编辑 IDE，图谱视图直观展示结构
- **Obsidian Web Clipper** — 浏览器扩展，网页 → Markdown 直入 raw/
- **本地存图片** — 绑定快捷键批量下载，防 URL 失效
- **qmd** — 本地 Markdown 混合搜索（BM25+向量+LLM 重排），有 MCP server，wiki 规模增大后的搜索基础设施
- **Dataview** — Obsidian 插件，对 frontmatter 运行动态查询
- **Marp** — Markdown 幻灯片格式，Obsidian 有插件，直接从 wiki 内容生成演示文稿

---

## 与用户 MyWiki 的对应

| Karpathy 定义 | MyWiki 实现 |
|---|---|
| Raw Sources | `raw/` |
| The Wiki | `concepts/` + `entities/` + `sources/` |
| Schema | `MyWiki/CLAUDE.md` |
| index.md | `index.md` |
| log.md | `log.md` |
| Hot Cache（扩展）| `hot.md` |

MyWiki 在 Karpathy 原始模式基础上增加了 `hot.md`（跨 session 热缓存）和三层目录结构（concepts/entities/sources 分层），是对原模式的具体实例化。
