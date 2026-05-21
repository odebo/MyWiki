# Hot Cache — 最近上下文

> 每次 session 开始先读这里。每次 session 结束执行 "update hot cache" 更新。

---

## 最近摄入（2026-05-21）

- **Karpathy LLM Wiki 模式**（gist）— 创建 `LLM-Wiki模式`、`Hot-Cache`、`Wiki三层目录结构`、`MCP文件系统集成`
- **claude-obsidian**（GitHub repo）— 创建 `claude-obsidian`（来源摘要）、`wiki迁移方案`

## 活跃话题

- LLM Wiki 工具链（Karpathy 模式 + claude-obsidian 实现）
- Obsidian + VSCode 集成最佳实践
- **刚完成：wiki 三层目录迁移**（concepts / entities / sources）

## 未解问题

- entities/ 目录为空，待新建：`梁宁`、`罗振宇`、`Andrej-Karpathy` 实体页
- MCP 文件系统集成尚未实际配置，只有文档
- CLAUDE.md 尚未更新读取顺序规则（hot.md 优先于 index.md）

## 知识库状态

- 总页面：32 页
- 结构：三层目录（concepts 21页 / entities 0页 / sources 10页）+ 根目录元文件
- 最近 commit：wiki ingest claude-obsidian + LLM Wiki 工具链
