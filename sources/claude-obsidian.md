---
updated: 2026-05-21
sources: [https://github.com/AgriciDaniel/claude-obsidian]
related: [[LLM-Wiki模式]], [[Hot-Cache]], [[Wiki三层目录结构]], [[MCP文件系统集成]]
---

# claude-obsidian

GitHub: https://github.com/AgriciDaniel/claude-obsidian
⭐ 5.3k stars | MIT | 作者：Agrici Daniel

基于 Karpathy LLM Wiki 模式的 Obsidian + Claude Code 完整实现。目前社区最成熟的方案。

## 定位

> "A running notetaker that builds and maintains a persistent, compounding wiki vault."

不是聊天界面，是自主维护知识库的系统。每次 ingest 创建 8-15 个结构化页面，每次 query 从整个 vault 合成回答。

## 核心创新（相对原始 Karpathy 模式）

1. **[[Hot-Cache]]** — `hot.md` 跨 session 上下文缓存，消除冷启动
2. **[[Wiki三层目录结构]]** — concepts/entities/sources 分层，支持大规模扩展
3. **`/autoresearch`** — 3 轮自主网络研究，自动填补知识空白
4. **Canvas 集成** — Obsidian 画布作为知识图谱可视化层
5. **矛盾检测** — `[!contradiction]` callout，标注跨页面冲突

## 命令速查

| 命令 | 作用 |
|------|------|
| `/wiki` | 初始化或恢复上次 session |
| `ingest [file/url]` | 摄入来源，创建 8-15 页面 |
| `what do you know about X?` | 查询：hot.md → index → 相关页 → 合成 |
| `/save` | 将当前对话存为 wiki 笔记 |
| `/autoresearch [topic]` | 自主研究 3 轮，自动填充知识库 |
| `lint the wiki` | 健康检查：孤立页、断链、知识空白 |
| `update hot cache` | Session 结束时更新 hot.md |

## Session 标准工作流

```
1. /wiki          → 加载 hot.md，恢复上下文
2. ingest [源]    → 创建页面，更新 index
3. 提问           → 从 vault 合成回答
4. /save          → 存档对话
5. update hot cache → 为下次 session 备好上下文
```

## 目录结构

```
wiki/
├── Wiki Map.canvas   # 可视化知识图谱入口
├── hot.md            # 热缓存（跨 session 记忆）
├── index.md          # 全量目录
├── log.md            # 操作日志
├── overview.md       # 执行摘要
├── concepts/         # 抽象概念
├── entities/         # 人物/组织/产品
├── sources/          # 来源摘要
└── meta/             # dashboard、模板
```

## 安装方式（推荐）

```bash
git clone https://github.com/AgriciDaniel/claude-obsidian
cd claude-obsidian
bash bin/setup-vault.sh
# 在 Obsidian 中打开此目录作为 vault
# 在 VSCode 中打开，运行 Claude Code，输入 /wiki
```

## 推荐搭配插件

| 插件 | 用途 |
|------|------|
| Bases | 原生数据库视图，主 dashboard |
| Templater | 自动填充 frontmatter |
| Calendar | 侧边栏日历 + 字数统计 |
| Obsidian Git | 每 15 分钟自动 commit |
| Excalidraw | 手绘注释 |

## 与 VSCode 的集成

- `.cursor/rules` 和 `.windsurf/rules` 已预配置（可参考适配 VSCode）
- 主要工作流通过 **Claude Code**（VSCode 终端）驱动
- Obsidian 作为**阅读和可视化层**，VSCode+Claude 作为**写入层**
- 通过 [[MCP文件系统集成]] 实现无缝读写
**主题**：[[AI技术]] [[产品开发]]
