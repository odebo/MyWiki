---
updated: 2026-06-02
sources: [抖音 Ali厂长《氛围编程已死，欢迎来到Agent工程时代》, Karpathy × 红杉 Stephanie Zhan 对话]
related: [[Andrej-Karpathy]], [[无限心灵管理者]], [[AI时代PM能力体系]], [[FDE前沿部署工程师模式]], [[AI-Harness-工程架构模式]]
---

# Software 3.0 与 Agentic Engineering

Karpathy 2025 年提出的范式描述，将当前 AI 编程时代命名为 Software 3.0，并区分了 Vibe Coding（氛围编程）与 Agentic Engineering（Agent 工程化）两种工作模式。

## Software 三代演进框架

| 时代 | 编程方式 | 核心主体 |
|------|---------|---------|
| Software 1.0 | 人写代码，逻辑由人定义 | 程序员 |
| Software 2.0 | 神经网络从数据中学习（Karpathy 2017 年文章） | 数据 + 模型 |
| Software 3.0 | LLM 本身是计算基底，自然语言是编程接口，Agent 是 Runtime | 语言 + Agent |

Software 3.0 不是预言，是描述现状：现在写代码时，大部分时间是在写 Spec、配 Context、跑测试、Review Diff、管 Agent 权限。程序员写的是给模型看的提示词，模型才是真正在敲键盘的。

## Vibe Coding vs Agentic Engineering

**Vibe Coding（氛围编程）**
- 靠氛围、感觉、运气
- 说"做个东西"，模型给你做，看起来还行，可能能跑
- 只配做原型，不适合生产环境

**Agentic Engineering（Agent 工程化）**
- 需要：Memory、Tools、测试、多 Agent 协作、Sandbox、监控、Code Review、Spec、安全边界
- 一个没有约束的 Coding Agent 不是同事，是一个拥有 Root 权限、精力无限、偶尔会幻觉的出击工程师

> "一个没有约束的 Coding Agent，不是同事，是一个拥有 Root 权限、精力无限、偶尔会幻觉的出击工程师。这不是劳动力策略，这是人质危机。"
> — Karpathy

## 对程序员的影响

- **老程序员反而更焦虑**：经验越深，越难接受 Agent 一次吐 800 行自己没写过的东西。必须 Code Review、必须签字、必须背锅，但看不懂——"不是在编程，是在签字"。
- **独立贡献者 → 多 Agent 编排者**：见 [[无限心灵管理者]]（Ivan Zhao 同一判断）
- **会写代码 ≠ 懂系统**：模型越强，传统意义上的"会写代码"越不能保证你真的理解系统

## 未来图景

不是一个万能 Agent，而是一堆专精 Agent，每个有自己的工具、权限、成功标准。工程师的核心工作变成调度这些 Agent。

市场信号两极：
- GitHub GH600 认证（GitHub Certified Agentic AI Developer）上线，承认这是独立技能
- Atlassian、Coinbase、Cloudflare（裁 1100+）、Salesforce、Snap 等大厂裁员，官方理由"适配 Agentic AI 时代"

## 核心判断

判断力是稀缺品（与 [[AI时代PM能力体系]] 中"决定写什么比写更值钱"一致）：
- AI 没有单纯替代谁，它暴露了那些"看起来在工作、但其实只是在会议之间传话的岗位"
- 光会用 Claude Code，和会工程化使用 Agent，是两件完全不同的事。后者难得多，也值钱得多

> Software 3.0 不是 Slogan。它是程序员从代码作者，变成计算劳动力操作者的那一刻。
