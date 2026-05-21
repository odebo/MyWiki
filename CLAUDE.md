# Wiki Schema

你维护一个个人知识库。以下是完整规则。

## 目录结构

```
wiki/
├── CLAUDE.md       # 本文件，Schema（随 git 同步到所有设备）
├── index.md        # 所有页面目录
├── log.md          # 操作日志（只追加）
├── hot.md          # 热缓存（跨 session 上下文，每次 session 开始先读）
├── raw/            # 原始资料（只读，不修改）
│   └── assets/     # 图片等附件
├── concepts/       # 抽象概念页（数量最多）
├── entities/       # 人物 / 组织 / 产品实体页
└── sources/        # 来源摘要页（每个原始资料对应一页）
```

## 触发条件

**仅在以下情况操作 wiki，其他任务不加载：**

- "记录这个" / "存到 wiki" / "ingest"
- "查一下 wiki" / "我对 X 了解多少"
- "整理知识库" / "lint wiki"

## 读取顺序（每次操作前）

1. 先读 `hot.md` — 获取近期上下文，避免冷启动
2. 再读 `index.md` — 定位相关页面
3. 按需读取具体页面

## Ingest（添加新资料）

1. 读取资料，与用户讨论 3 个核心要点（确认再继续）
2. 创建或更新相关 wiki 页面，按类型放置：
   - 抽象概念 → `concepts/`
   - 人物/组织/产品 → `entities/`
   - 来源摘要 → `sources/`
3. 更新 `index.md`
4. 追加 `log.md` 一条记录
5. git commit & push

## Query（查询）

1. 先读 `hot.md`，再读 `index.md` 定位相关页面
2. 读取具体页面，综合回答，注明来源页面
3. 有价值的分析结论存为新页面，不要让它消失在对话历史里

## Lint（健康检查）

检查：页面间矛盾、孤立页面（无入链）、过时内容、缺失交叉引用、entities/ 空缺。

## Session 结束

执行 "update hot cache" → 更新 `hot.md`，记录本次活跃话题、新增页面、未解问题。

## 页面格式

```markdown
---
updated: YYYY-MM-DD
sources: [raw/xxx.md 或 URL]
related: [[页面A]], [[页面B]]
---

# 页面标题

正文...
```

## Git 同步（双设备共享）

操作 wiki 前后执行：

```bash
# 操作前
git -C ~/wiki pull

# 操作后
git -C ~/wiki add -A && git commit -m "wiki: <简述>" && git push
```

若尚未关联远程仓库，跳过 git 步骤并提示用户配置。
