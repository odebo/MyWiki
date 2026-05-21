---
updated: 2026-05-21
sources: [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f]
related: [[Hot-Cache]], [[Wiki三层目录结构]], [[MCP文件系统集成]], [[claude-obsidian]]
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

## 延伸实现

- [[claude-obsidian]] — 基于此模式的 Obsidian + Claude Code 完整实现（5.3k stars）
- [[Hot-Cache]] — claude-obsidian 新增的跨 session 上下文缓存机制
- [[Wiki三层目录结构]] — concepts/entities/sources 的目录分层策略
