---
updated: 2026-05-21
sources: []
related: [[Wiki三层目录结构]], [[LLM-Wiki模式]], [[Hot-Cache]]
---

# Wiki 迁移方案

将当前平铺结构（26 页）迁移至 concepts/entities/sources 三层目录 + 新增 hot.md 热缓存。

## 当前状态

```
wiki/（根目录，26 个页面混放）
├── CLAUDE.md
├── index.md
├── log.md
├── 梁宁-产品思维30讲.md     ← source 类
├── 梁宁-增长思维30讲.md     ← source 类
├── 罗胖60秒十年合集.md      ← source 类
├── 罗胖60秒-思维与判断.md   ← source 类（主题分卷）
├── 罗胖60秒-学习与成长.md   ← source 类
├── 罗胖60秒-商业与战略.md   ← source 类
├── 罗胖60秒-社会与趋势.md   ← source 类
├── 罗胖60秒-表达与沟通.md   ← source 类
├── 罗胖60秒-组织与领导力.md ← source 类
├── 同理心.md                ← concept 类
├── 用户情绪四象限.md        ← concept 类
├── 痛点-痒点-爽点.md        ← concept 类
├── 点线面体.md              ← concept 类
├── 用户画像.md              ← concept 类
├── 系统能力与确定性.md      ← concept 类
├── 用户体验五层次.md        ← concept 类
├── 峰终定律.md              ← concept 类
├── 上瘾机制.md              ← concept 类
├── 三级火箭.md              ← concept 类
├── 增强回路与调节回路.md    ← concept 类
├── 破局点.md                ← concept 类
├── 闪电式扩张.md            ← concept 类
├── 组织成长五阶段.md        ← concept 类
├── 战略支点与战略杠杆.md    ← concept 类
├── 玩家地图与增长生态位.md  ← concept 类
└── 一横一纵增长框架.md      ← concept 类
```

## 目标结构

```
wiki/
├── CLAUDE.md          # 不动
├── index.md           # 更新分类
├── log.md             # 不动
├── hot.md             # 新建
│
├── concepts/          # 17 个概念页
│   ├── 同理心.md
│   ├── 用户情绪四象限.md
│   ├── 痛点-痒点-爽点.md
│   ├── 点线面体.md
│   ├── 用户画像.md
│   ├── 系统能力与确定性.md
│   ├── 用户体验五层次.md
│   ├── 峰终定律.md
│   ├── 上瘾机制.md
│   ├── 三级火箭.md
│   ├── 增强回路与调节回路.md
│   ├── 破局点.md
│   ├── 闪电式扩张.md
│   ├── 组织成长五阶段.md
│   ├── 战略支点与战略杠杆.md
│   ├── 玩家地图与增长生态位.md
│   ├── 一横一纵增长框架.md
│   ├── LLM-Wiki模式.md    # 新增（本次 ingest）
│   ├── Hot-Cache.md       # 新增
│   ├── Wiki三层目录结构.md # 新增
│   └── MCP文件系统集成.md  # 新增
│
├── entities/          # 新建：人物实体页
│   ├── 梁宁.md        # 需新建
│   ├── 罗振宇.md      # 需新建
│   └── Andrej-Karpathy.md  # 需新建
│
└── sources/           # 9 个来源摘要页
    ├── 梁宁-产品思维30讲.md
    ├── 梁宁-增长思维30讲.md
    ├── 罗胖60秒十年合集.md
    ├── 罗胖60秒-思维与判断.md
    ├── 罗胖60秒-学习与成长.md
    ├── 罗胖60秒-商业与战略.md
    ├── 罗胖60秒-社会与趋势.md
    ├── 罗胖60秒-表达与沟通.md
    ├── 罗胖60秒-组织与领导力.md
    └── claude-obsidian.md  # 新增（本次 ingest）
```

## 迁移步骤

### 第一步：创建目录（5 分钟）

```bash
cd ~/Documents/WorkSpace/MyWiki
mkdir -p concepts entities sources
```

### 第二步：移动文件

```bash
# concepts（17 个现有概念页）
mv 同理心.md 用户情绪四象限.md 痛点-痒点-爽点.md 点线面体.md \
   用户画像.md 系统能力与确定性.md 用户体验五层次.md 峰终定律.md \
   上瘾机制.md 三级火箭.md 增强回路与调节回路.md 破局点.md \
   闪电式扩张.md 组织成长五阶段.md 战略支点与战略杠杆.md \
   玩家地图与增长生态位.md 一横一纵增长框架.md \
   LLM-Wiki模式.md Hot-Cache.md Wiki三层目录结构.md MCP文件系统集成.md \
   concepts/

# sources（9 个来源摘要页）
mv 梁宁-产品思维30讲.md 梁宁-增长思维30讲.md \
   罗胖60秒十年合集.md 罗胖60秒-思维与判断.md 罗胖60秒-学习与成长.md \
   罗胖60秒-商业与战略.md 罗胖60秒-社会与趋势.md \
   罗胖60秒-表达与沟通.md 罗胖60秒-组织与领导力.md claude-obsidian.md \
   sources/
```

### 第三步：创建 hot.md

新建 `hot.md`，内容参见 [[Hot-Cache]]。

### 第四步：新建 entities 人物页

为 `梁宁`、`罗振宇`、`Andrej-Karpathy` 创建实体页（可在下次 ingest 相关资料时顺带建）。

### 第五步：更新 index.md

按新的三层结构重写 index.md 目录。

### 第六步：更新 CLAUDE.md

在 CLAUDE.md 中添加：
- 读取顺序：`先读 hot.md，再读 index.md，再读具体页面`
- 目录规则：新 concept 页存 concepts/，来源摘要存 sources/，实体页存 entities/

## 关于 Wikilink 断链问题

**Obsidian 中不会断链。** Obsidian 的 `[[文件名]]` 语法按文件名全局解析，与子目录无关。迁移后所有现有链接自动找到新路径，**无需修改任何页面内容**。

纯 markdown 阅读器（如 VSCode Markdown Preview）中链接会断，但 wiki 的主要消费场景是 Obsidian + Claude Code，不影响使用。

## 迁移时机建议

**现在执行**：页面数已达 26，且本次 ingest 新增 6 页，共 32 页，已过临界点。
迁移后每次 ingest 新来源，Claude 自动按三层结构放置文件，无需人工分类。

---

执行迁移请告诉我，我来运行第一到第六步的所有命令。
