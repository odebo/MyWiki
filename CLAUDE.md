# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

这是一个个人知识库（基于 Karpathy LLM Wiki 模式），同时捆绑了配套的 MCP server 工具。以下是完整操作规则。

## 仓库顶层结构

```
my-wiki/
├── wiki/         # 知识内容（markdown 笔记）— LLM Wiki 主体
│   ├── concepts/
│   ├── opinions/
│   ├── sources/
│   ├── topics/
│   ├── raw/      # 原始资料（只读）
│   ├── hot.md
│   ├── index.md
│   ├── log.md
│   └── .obsidian/  # Obsidian vault 配置（vault root = wiki/）
├── mcp/          # wiki-mcp server 源码（Python，未来可独立开源）
├── .mcp.json     # MCP server 配置（WIKI_ROOT 指向 wiki/）
├── CLAUDE.md     # 本文件
└── .gitignore
```

**关键约定**：所有知识内容都在 `wiki/` 子目录下；`mcp/` 是工具代码，不属于知识内容。下文所有路径如无特别说明，都相对于 `wiki/`。

## 常用命令

```bash
# 同步（操作前拉取，操作后推送）
git pull
git add -A && git commit -m "wiki: <简述>" && git push

# 查看最近操作记录
grep "^## \[" wiki/log.md | tail -5

# 统计页面数
ls wiki/concepts/ wiki/opinions/ wiki/sources/ wiki/topics/ | grep -c ".md"
```

## 知识库结构（wiki/）

四层目录 + 四个根目录元文件。截至 2026-08-14 约 3945 页（1866 concepts / 1686 opinions / 373 sources / 20 topics），且以每次 ingest +10 页的速度持续增长——这是成熟大型知识库，新建/修改页面时务必考虑对现有交叉引用的影响，不要轻率重命名或删除已有页面。

```
wiki/
├── concepts/   # 抽象概念页（定义/框架/工具，中性知识单元）
├── opinions/   # 强命题观点页（一条命题一页，有作者/证据/可挑战性）
├── sources/    # 来源摘要页（每个原始资料对应一页，含作者简介）
├── topics/     # 主题聚合页（20个大主题，连接 opinions/concepts/sources，是图谱的中间层）
├── hot.md      # 热缓存：跨 session 上下文，每次 session 开始先读
├── index.md    # 全量目录，按四层分类列出所有页面
├── log.md      # 追加写入的操作日志（只追加，不删改）
└── raw/        # 原始资料（只读，不修改）；图片等附件在 raw/assets/
```

**图谱拓扑**：index → topics → opinions/concepts/sources（多对多）
- 每个 opinion 在末尾写 `**主题**：[[主题A]] [[主题B]]` 建立反向链接
- 一个节点可以属于多个主题，Obsidian 图谱自动形成网状结构

## 可用 Skills

操作 wiki 时优先调用对应 skill，而不是手动执行：

- `wiki` — 通用查询 / ingest / lint
- `wiki-ingest` — 专门用于书籍 PDF 的结构化 ingest（分章节阅读、逐章提炼）
- `wiki-link` — 对话中产生洞见后，主动 ingest 回 wiki

## 触发条件

**仅在以下情况操作 wiki，其他任务不加载：**

- "记录这个" / "存到 wiki" / "ingest"
- "查一下 wiki" / "我对 X 了解多少"
- "整理知识库" / "lint wiki"

## 读取顺序（每次操作前）

1. 先读 `wiki/hot.md` — 获取近期上下文，避免冷启动
2. 再读 `wiki/index.md` — 定位相关页面
3. 按需读取具体页面

## Ingest（添加新资料）

1. 读取资料，与用户讨论 3 个核心要点（确认再继续）
2. 创建或更新相关 wiki 页面，按类型放置。**书籍 ingest 的默认产出模式是 `5 concepts + 4 opinions + 1 source`**（见 log.md 历史记录），即每本书提炼 5 个核心概念 + 4 条强命题 + 1 页来源摘要；用户未明确指定数量时按此惯例执行：
   - 抽象概念（定义/框架/工具）→ `wiki/concepts/`
   - 强命题/观点（某人对某问题的主张）→ `wiki/opinions/`（末尾加 `**主题**：[[主题名]]`）
   - 来源摘要（含作者简介）→ `wiki/sources/`
   - 新主题出现时更新 `wiki/topics/` 对应页面
3. 更新 `wiki/index.md`
4. 追加 `wiki/log.md` 一条记录
5. git commit & push

## Query（查询）

1. 先读 `wiki/hot.md`，再读 `wiki/index.md` 定位相关页面
2. 读取具体页面，综合回答，注明来源页面
3. 有价值的分析结论存为新页面，不要让它消失在对话历史里

## Lint（健康检查）

检查：页面间矛盾、孤立页面（无入链）、过时内容、缺失交叉引用、opinions/ 缺少对立观点。

## Session 结束

执行 "update hot cache" → 更新 `wiki/hot.md`，记录本次活跃话题、新增页面、未解问题。

## 页面格式

**concepts / sources**：
```markdown
---
updated: YYYY-MM-DD
sources: [raw/xxx.md 或 URL]
related: [[页面A]], [[页面B]]
---

# 页面标题

正文...
```

**opinions**（一条命题一页）：
```markdown
---
updated: YYYY-MM-DD
opinion_of: 作者名
topic: 主题词（用于跨作者聚合）
sources: [[来源 concept 或 source 页]]
related: [[对立观点页]], [[支持观点页]]
---

# 命题标题（强主张，不超过15字）

**主张**：一两句话陈述核心观点。

**反常识在哪**：这个观点打破了什么默认认知。

**核心证据/论据**：作者用什么支撑。

**可被挑战**：什么情况下这个观点会失效或被反驳。

**主题**：[[主题A]] [[主题B]]
```

末尾的 `**主题**：` 行是 opinions 进入 topic 图谱的反向链接，**不可省略**。
