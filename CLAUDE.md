# Wiki Schema

你维护一个个人知识库。以下是完整规则。

## 目录结构

```
~/wiki/
├── CLAUDE.md       # 本文件，Schema（随 git 同步到所有设备）
├── index.md        # 所有页面目录，查询时先读这里
├── log.md          # 操作日志（只追加）
├── raw/            # 原始资料（只读，不修改）
│   └── assets/     # 图片等附件
└── *.md            # wiki 页面，直接放根目录
```

## 触发条件

**仅在以下情况操作 wiki，其他任务不加载：**

- "记录这个" / "存到 wiki" / "ingest"
- "查一下 wiki" / "我对 X 了解多少"
- "整理知识库" / "lint wiki"

## Ingest（添加新资料）

1. 将资料存入 `raw/`（文件名英文，如 `karpathy-llm-wiki.md`）
2. 读取资料，与用户讨论核心要点
3. 创建或更新相关 wiki 页面（一次可能涉及多个页面）
4. 更新 `index.md`
5. 追加 `log.md` 一条记录
6. git commit & push

## Query（查询）

1. 先读 `index.md` 定位相关页面
2. 读取具体页面，综合回答
3. 有价值的分析结论存为新页面，不要让它消失在对话历史里

## Lint（健康检查）

检查：页面间矛盾、孤立页面（无入链）、过时内容、缺失交叉引用。

## 页面格式

```markdown
---
updated: YYYY-MM-DD
sources: [raw/xxx.md]
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
