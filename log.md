# Log

append-only。格式：`## [YYYY-MM-DD] 操作类型 | 简述`

用 `grep "^## \[" ~/wiki/log.md | tail -5` 查看最近 5 条记录。

---

## [2026-05-23] ingest | wiki-book《费曼思考法：5步成为学习高手》（彼得·霍林斯，PDF 47页全量）— 新增 6 页：concepts/费曼学习法 + concepts/内在动机 + concepts/门徒效应 + concepts/思想层次 + entities/richard-feynman + sources/费曼思考法；wiki 75→81页

## [2026-05-23] ingest | wiki-book《人类登月简史》（张天光，142页全量）— 新增 5 页：concepts/渐进式技术攀登 + concepts/阿波罗13号危机创新 + concepts/使命驱动的大工程 + concepts/新太空竞赛 + sources/人类登月简史；wiki 70→75页

## [2026-05-22] ingest | 新增 entities/luo-zhenyu.md（罗振宇）— 基本信息、思想风格、代表性洞见、与得到关系

## [2026-05-22] update | 罗胖60秒·十年合集 全量重新 ingest — 覆盖全十年（2013-2022，2263条），更新7个页面（1个overview+6个主题页）；每页从"2019-2022局部"扩充为"全十年综合"，新增约50+条跨年洞见

## [2026-05-22] ingest | 浅田卓《丰田"一页纸"思考术》— 100页全文，创建5个concepts页+1个entities页+1个sources页；新增：TBP/一页纸框架/What-Why-How/两段式问题解决法/零页纸/浅田卓

## [2026-05-22] ingest | 李想·产品实战16讲（得到课程，16讲全文）

创建 8 个页面：
- concepts/用户价值超越需求 — 核心方法论；用户处境vs需求；用户价值流倒推流程
- concepts/产品三感 — 安全感/价值感/向往感
- concepts/增长节奏 — 0→1 vs 1→10两阶段逻辑；SEV教训；必要性原则
- concepts/复盘方法论 — 先总结优点；对照PEA；Todo落到人；CEO带头
- concepts/组织产品化 — 把组织当产品；PEA评审；产品四步法；成人人格
- concepts/原子级经营 — 原子级拆分；最佳实践提炼；不刷存在感+NPS
- entities/li-xiang — 李想；理想汽车；成长驱动；SEV教训；问界M7危机
- sources/li-xiang-chanpin-shizhan-16jiang — 16讲完整速览+案例索引

---

## [2026-05-22] ingest | First Round — AI 产品定位手册

来源：https://review.firstround.com/positioning-playbook-for-ai-products/

创建 2 个页面：
- concepts/AI产品定位 — 三步框架（有主见POV / 清晰Positioning / 设计战略）
- sources/FirstRound-AI产品定位手册 — 来源摘要页

---

## [2026-05-22] ingest | Ivan Zhao — Steam, Steel, and Infinite Minds

来源：https://www.notion.com/blog/steam-steel-and-infinite-minds-ai

创建 3 个页面：
- concepts/AI作为奇迹材料 — 三层变革框架（个人/组织/经济），钢铁vs蒸汽机隐喻
- concepts/无限心灵管理者 — agent编排者转型，30-40×工程师案例
- sources/Ivan-Zhao-AI奇迹材料 — 来源摘要页

---

## [2026-05-02] init | 知识库初始化

按 Karpathy LLM Wiki 模式创建目录结构。

## [2026-05-13] ingest | 梁宁·增长思维30讲

来源：/Users/zhuqichen/Documents/WorkSpace/dedao/dedao-downloads/course/梁宁·增长思维30讲/MD/（37 个 MD 文件）

创建 8 个概念词条页面：
- 梁宁-增长思维30讲（总览）
- 玩家地图与增长生态位
- 破局点
- 增强回路与调节回路
- 闪电式扩张
- 组织成长五阶段
- 战略支点与战略杠杆
- 一横一纵增长框架

## [2026-05-13] ingest | 罗胖60秒·十年合集

来源：/Users/zhuqichen/Documents/WorkSpace/dedao/dedao-downloads/60s/output/罗胖60秒·十年合集/MD/（2263 个 MD 文件，2013-2022 年）

方式：主题聚合（approach B），按 6 大主题分类提炼

创建 7 个主题词条页面：
- 罗胖60秒十年合集（总览）
- 罗胖60秒-思维与判断
- 罗胖60秒-学习与成长
- 罗胖60秒-商业与战略
- 罗胖60秒-社会与趋势
- 罗胖60秒-表达与沟通
- 罗胖60秒-组织与领导力

## [2026-05-21] ingest | claude-obsidian + Karpathy LLM Wiki 工具链

来源：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
      https://github.com/AgriciDaniel/claude-obsidian

创建 6 个页面：
- LLM-Wiki模式（核心概念）
- Hot-Cache（跨 session 缓存机制）
- Wiki三层目录结构（concepts/entities/sources 分层）
- MCP文件系统集成（Claude 直接读写 vault）
- claude-obsidian（来源摘要，5.3k stars 实现）
- wiki迁移方案（当前 wiki 的迁移规划）

## [2026-05-13] ingest | 梁宁·产品思维30讲

来源：/Users/zhuqichen/Documents/WorkSpace/dedao/dedao-downloads/course/梁宁·产品思维30讲/MD/（41 个 MD 文件）

创建 11 个概念词条页面：
- 梁宁-产品思维30讲（总览）
- 同理心
- 用户情绪四象限
- 痛点-痒点-爽点
- 点线面体
- 用户画像
- 系统能力与确定性
- 用户体验五层次
- 峰终定律
- 上瘾机制
- 三级火箭

## [2026-05-22] ingest | Ray Dalio《原则（全新增订版）》— 273页全文阅读完成

- 来源：.cc-connect/attachments/144892_原则（全新增订版）_【美】瑞·达利欧.pdf
- 新建 sources：ray-dalio-principles.md
- 新建 concepts：meritocracy, radical-transparency, five-step-process, credibility-weighting, pain-reflection-progress, bridgewater-tools（共6页）
- 新建 entities：ray-dalio.md（首个 entities 页面）
- 更新：index.md（统计45页），hot.md

## [2026-05-22] Ingest 李笑来《通往财富自由之路》（得到课程，52个概念）
- 新增 7 个 concept 页面：财富自由、注意力管理、成长率与复利、价值观与刚需、时间重复销售、李笑来投资原则、多维竞争
- 新增 1 个 entity 页面：li-xiaolai
- 新增 1 个 source 页面：li-xiaolai-caifuziyo
- 更新 index.md（+7 concepts, +1 entity, +1 source）

## [2026-05-23] ingest | wiki-book《故事演讲力：商业演讲中的故事策略》（赵金星，156页全量）— 新增 9 页：concepts/故事演讲力-神经科学与决策机制 + concepts/故事思维 + concepts/故事结构工具 + concepts/故事演讲设计系统 + concepts/故事库建设 + concepts/个人品牌故事 + concepts/故事的边界与真诚 + entities/zhao-jinxing + sources/故事演讲力；wiki 81→90页
