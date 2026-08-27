---
related:
- '[[Harness-Agent的软件外壳]]'
- '[[运行时可组合性]]'
- '[[会话即事件日志]]'
- '[[Harness做的是基建不是产品-卡兹克]]'
- '[[一切皆插件的代价是劝退普通用户-卡兹克]]'
sources:
- https://mp.weixin.qq.com/s/xkC1aenHFNSH2BxyzLDfcA
updated: '2026-08-14'
---

# 速通 DeepSeek Harness

**作者**：卡兹克（科技自媒体作者，长期跟踪 AI 产品动态，投稿邮箱 wzglyay@virxact.com）。

**出处**：微信公众号文章《从0到1带你速通DeepSeek Harness》。
链接：https://mp.weixin.qq.com/s/xkC1aenHFNSH2BxyzLDfcA

## 内容摘要

文章系统介绍了 DeepSeek 发布的 Harness 系统（开发者预览版），核心要点：

1. **Agent = Model + Harness**。Harness 是包裹模型的软件壳，封装工具、Skills、会话、沙箱、循环、子 Agent、工作流等所有非模型能力。过去这些由厂商封装隐藏，DeepSeek 把它们全部插件化。

2. **Cordis 内核**：DeepSeek Harness 的真正核心，作者已加入 DeepSeek 并发了 88 页论文。内核极度克制，只管插件加载/卸载/依赖管理，支持运行时热插拔且不崩，靠的是**时间可组合性**（副作用可撤销）与**空间可组合性**（依赖可动态重组）两个特性。目的是让 Agent 在运行中不断给自己装卸插件，实现自进化。

3. **一切皆插件**：连 UI 都是可替换插件（社区已有人做皮肤）。模型不锁死 DeepSeek，可接 GLM 等其他提供方。

4. **四种模式**：标准（完整代码 Agent 能力，小白无脑选）/ PTC（程序化工具调用，多次往返压进一次 run_code，省 token，需模型代码规划能力强）/ 极简（仅持久 Bash + 文件编辑器，用于模型基准测试，不宜日常用）/ 创造（标准能力 + 能检查自身 Cordis 环境、试验插件、自造插件挂到运行流程，即"Agent 改造自己"，是 Harness 最核心特点）。

5. **会话即事件日志**：append-only，历史从日志重新推导，带来可观测/可审计/可复现，适合研究。

6. **价格**：DeepSeek V4 Pro 涨价明显（缓存命中价涨 12 倍，高峰输出 27 元/百万 token），性价比从"价格屠夫"下滑，与 GLM、Qwen 3.8 Max 差距缩小；GLM-5.3 即将发布。

7. **社区三方插件推荐**：dsh-at-file（@调用文件）、dsh-genui（渲染图表/表格/Diff/Mermaid）、dsh-automation（自动化）、DSH-better-sidebar（VS Code 式工作台）、ModLens（给纯文本模型补视觉能力）。

8. **作者评价**：理念与插拔概念很棒，但从产品角度对普通用户极不友好（术语多、门槛高、功能少、体验差）；DeepSeek 本质是注重科研探索的团队，slogan"探索未至之境"。

## 关联

**关联概念**：[[Harness-Agent的软件外壳]] [[运行时可组合性]] [[会话即事件日志]]
**关联观点**：[[Harness做的是基建不是产品-卡兹克]] [[一切皆插件的代价是劝退普通用户-卡兹克]]