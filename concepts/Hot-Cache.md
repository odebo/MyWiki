---
updated: 2026-05-21
sources: [https://github.com/AgriciDaniel/claude-obsidian]
related: [[LLM-Wiki模式]], [[claude-obsidian]], [[MCP文件系统集成]]
---

# Hot Cache

claude-obsidian 对 Karpathy LLM Wiki 模式的关键补充。解决"LLM 每次 session 都失忆"的根本问题。

## 问题：冷启动损耗

原始 LLM Wiki 模式没有跨 session 记忆机制。每次对话开始时，LLM 需要重新读取 index.md → 定位相关页面 → 重建上下文，造成大量重复开销。

## 方案：`hot.md` 热缓存文件

在 wiki 根目录维护一个 `hot.md`，存储：

```markdown
# Hot Cache — 最近上下文

## 最近摄入
- [日期] 摄入了《XXX》，创建了 N 个页面

## 活跃话题
- 正在研究的主题
- 近期提问集中在哪些领域

## 未解问题
- 还没有答案的问题
- 等待更多来源的知识空白

## Session 末尾更新
- 本次新增/修改了哪些页面
```

## 工作流

```
Session 开始
  └── 读 hot.md（先于 index.md）→ 立即获得近期上下文

Session 进行中
  └── 正常 ingest / query / lint

Session 结束
  └── 执行 "update hot cache" → 更新 hot.md → 下次直接继承
```

## 效果

- **消除冷启动**：LLM 知道上次做了什么，不需要重新问
- **跨 session 连续性**：话题可以跨越多天推进，不丢失进度
- **聚焦活跃区域**：LLM 优先从热区域开始，而不是扫描整个 wiki

## 与 index.md 的分工

| 文件 | 作用 | 更新频率 |
|------|------|---------|
| `index.md` | 全量目录，结构化导航 | 每次 ingest 后 |
| `hot.md` | 近期上下文，工作记忆 | 每次 session 结束 |

## 实践建议

- hot.md 保持简洁，控制在 100 行内，避免每次加载过多
- 内容聚焦"最近 2 周活跃的内容"，过期内容移入正式 wiki 页面
- 可在 CLAUDE.md 中指定：`session 开始时先读 hot.md，再读 index.md`
