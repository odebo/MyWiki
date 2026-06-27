---
type: concept
title: LLM Wiki 模式
timestamp: 2026-05-25T00:00:00Z
sources: [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f]
related: [[Hot-Cache]], [[Wiki三层目录结构]], [[MCP文件系统集成]], [[claude-obsidian]], [[Software 3.0时代程序员从代码作者变成计算劳动力操作者-Karpathy]]
---

# LLM Wiki 模式

Andrej Karpathy 提出的个人知识库范式。LLM 不再是被动检索者，而是主动维护一个持久化、不断进化的知识图谱。

## 核心思想：知识复利

| 模式 | 流程 | 状态 |
|------|------|------|
| **RAG** | 查询 → 检索原文 → 临时合成 | 无状态，每次从零开始 |
| **LLM Wiki** | 摄入 → 更新持久 wiki → 查询 | 有状态，知识随时间复利 |

> "每个新来源都被整合进去。每次提问都从所有已读内容中提取答案。知识像复利一样积累。"

## 三层架构

```
原始资料层（Raw Sources）
  └── 不可变，用户策展（论文、课程、博客）
        ↓ LLM 提炼
Wiki 层（The Wiki）
  └── LLM 维护的 markdown 文件集，含交叉引用
        ↑ 读取时合成
Schema 层（CLAUDE.md）
  └── 定义 wiki 结构和工作流的配置文件
```

## 三个核心操作

**Ingest（摄入）**
新来源到达 → LLM 读取 → 提取关键信息 → 更新 8-15 个 wiki 页面（摘要、实体页、概念页、交叉引用）

**Query（查询）**
用户提问 → 搜索 index.md 或 hot.md → 定位相关页面 → 合成回答（含 wiki 引用）→ 有价值的分析存回 wiki

**Lint（健康检查）**
定期检查：矛盾内容、孤立页面、过时断言、缺失交叉引用、知识空白

## 为什么 LLM 适合维护 wiki

知识库衰败的原因不是阅读或思考，而是**书记员工作**：
- 更新交叉引用
- 标记互相矛盾的内容
- 保持全库一致性

人会疲惫，LLM 不会。可同时编辑数十个文件，个人规模的持久知识库首次变得可行。

## 两个支撑文件

- `index.md` — 内容导向的全页面目录，查询时先读这里
- `log.md` — 追加写入的时序操作记录

## Schema 是核心差异

Schema（CLAUDE.md/AGENTS.md）是让 LLM 成为"有纪律的 wiki 维护者"而非"通用聊天机器人"的配置文件。它定义目录结构、页面格式、工作流约定。你和 LLM 共同演进它，随时间收敛出适合自己领域的版本。

## 查询的输出形式不止文字

查询答案可以是：Markdown 页面、对比表格、Marp 幻灯片（直接从 wiki 内容生成演示）、Matplotlib 图表。
**关键原则**：有价值的分析直接存回 wiki，不让它消失在对话历史里——探索本身也是知识积累的一部分。

## Memex 联系

本模式精神上承接 Vannevar Bush 1945 年的 Memex 设想——私人的、主动策展的、文档之间的关联链接与文档本身同等重要。Bush 未能解决的问题是"谁来维护"，LLM 解决了这个问题。

## 推荐工具（Karpathy 原文）

- **Obsidian Web Clipper** — 浏览器扩展，将网页文章转为 Markdown 直接送入 raw/
- **本地存储图片** — 防止 URL 失效；Obsidian 绑定快捷键一键下载当前文章所有图片
- **Obsidian 图谱视图** — 查看 wiki 结构全貌，识别枢纽页和孤立页
- **qmd** — 本地 Markdown 搜索引擎，BM25/向量混合搜索 + LLM 重排，有 MCP server 接口
- **Dataview** — Obsidian 插件，对 frontmatter 运行查询生成动态表格

## 延伸实现

- [[claude-obsidian]] — 基于此模式的 Obsidian + Claude Code 完整实现（5.3k stars）
- [[Hot-Cache]] — claude-obsidian 新增的跨 session 上下文缓存机制
- [[Wiki三层目录结构]] — concepts/entities/sources 的目录分层策略
- [[Software 3.0时代程序员从代码作者变成计算劳动力操作者-Karpathy]] — 原作者
**主题**：[[AI技术]] [[产品开发]]
