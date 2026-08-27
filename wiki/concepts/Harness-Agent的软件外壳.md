---
related:
- '[[运行时可组合性]]'
- '[[会话即事件日志]]'
- '[[FDE-Agent时代PMF]]'
sources:
- https://mp.weixin.qq.com/s/xkC1aenHFNSH2BxyzLDfcA
updated: '2026-08-14'
---

# Harness：Agent 的软件外壳

**Agent = Model + Harness。**

Model 是大语言模型本身；Harness 是包裹在模型外层的"软件壳"，封装了一个 Agent 运行所需的全部非模型能力：

- 工具调用（文件读写、Shell、搜索、网页）
- Skills 系统
- 会话管理与上下文压缩
- 沙箱与存储
- Agent 循环（推理→调用→观察→再推理）
- 调度、子 Agent、工作流

在传统 Agent 产品（如 Codex、Claude Code 的闭源形态）中，Harness 由厂商封装好、藏在后方，普通用户只接触产品表面，能自定义的只有 Skill、MCP 等少数入口。DeepSeek Harness 的激进之处在于：把上述所有能力全部做成插件，连 UI 本身都是插件，于是整层 Harness 都可被自定义、热插拔。

理解 Harness 这一层的存在，是理解"为什么同一个模型在不同产品里能力差异巨大"的关键——模型相同，Harness 不同，Agent 表现就不同。

**来源**：[[速通DeepSeekHarness-卡兹克]]