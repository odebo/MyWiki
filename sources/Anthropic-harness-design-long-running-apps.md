---
type: source
title: Anthropic：Harness Design for Long-Running Application Development
timestamp: 2026-06-01T00:00:00Z
sources: [https://www.anthropic.com/engineering/harness-design-long-running-apps]
related: [[创意评估循环-生成器与评估器分离]], [[Eval设计-定义成功]], [[临时性思维]]
---

# Anthropic：Harness Design for Long-Running Application Development

来源：Anthropic 工程博客
解读：慢学AI 第22集《Anthropic 解决 AI 味输出，把你的审美注入系统》
时长：6:07

---

## 核心主题

如何解决 AI 在创意任务（前端页面设计）上输出"有 AI 味"、缺乏审美的问题。

---

## 主要论点

1. **创意任务的评估困境**：没有客观标准，模型自评天然偏宽容（裁判即运动员）
2. **解法**：把主观审美拆成 4 个可评分维度（设计质量、原创性、工艺、功能性），前两个权重最高
3. **系统架构**：生成器 + 独立评估器的两阶段循环，过程中出现风格跃迁
4. **临时性原则**：评估机制本身需随模型能力变化而更新

---

## 关键结论

- 平均水平就是 AI 味的本质
- 评估器必须独立于生成器，分工才能真正有效
- 主观不是不可测，是没想清楚"好"是什么
- 每条 eval 标准都要标好退场条件
**主题**：[[AI技术]] [[产品开发]]
