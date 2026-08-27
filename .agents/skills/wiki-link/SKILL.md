---
name: wiki-link
description: Wiki 双向桥接。前向：对话开始时检索 Wiki 注入上下文。后向：对话产生洞见后提议 ingest 回 Wiki。触发词："查一下"、"我之前了解过"、"帮我想想"，或 Agent 主动判断话题与 Wiki 相关。
---

# Wiki Bridge — Wiki 双向桥接

## 触发条件

**前向注入（对话开始时自动触发）：**
- 用户提问涉及知识/观点/概念，且非纯代码问题
- 用户说"查一下"、"我之前了解过..."、"帮我想想 X"
- 用户提到 Wiki 中可能已有记录的话题

**后向 ingest（对话产生洞见时触发）：**
- 用户说"记录这个"、"值得存下来"、"ingest"
- 对话产生了新洞见、决策、结论——Agent 主动提议

---

## 前向注入流程

### 第 1 步：读取 Wiki 热缓存

读取 `/Users/zhuqichen/Documents/WorkSpace/Asrocky01/MyWiki/hot.md`，获取近期上下文（活跃话题、最近摄入、未解问题）。

### 第 2 步：定位相关页面

读取 `/Users/zhuqichen/Documents/WorkSpace/Asrocky01/MyWiki/index.md`，根据用户提问的关键词在目录中搜索相关页面。

匹配规则：
- 关键词直接出现在页面标题或简介中 → 高相关
- 属于同一话题群（如"Ray Dalio"→ meritocracy/radical-transparency/five-step-process）→ 中相关
- 最多选 3 页注入，优先选高相关
- 若无相关页面，静默跳过（不输出 `[Wiki]` 提示），直接正常回答

### 第 3 步：读取并注入

读取选中的页面，提取核心内容（不超过每页前 50 行），在回答开头告知用户：

```
[Wiki] 找到相关内容：[[页面名A]]、[[页面名B]]
```

然后基于 Wiki 内容 + 用户问题给出回答。若 Wiki 内容与问题高度吻合，直接引用并扩展；若只是背景参考，自然融入即可。

### 前向注入示例

用户问："创意择优是什么意思？"

1. 读 hot.md → 发现 Ray Dalio 是活跃话题
2. 读 index.md → 找到 `[[meritocracy]]`、`[[radical-transparency]]`
3. 读这两页 → 提取核心内容
4. 回答前告知："[Wiki] 找到相关内容：[[meritocracy]]、[[radical-transparency]]"
5. 基于 Wiki 内容回答，不重复用户已知的内容

---

## 后向 ingest 流程

### 第 1 步：识别新洞见

分析本次对话，识别值得保存的内容：
- 新概念、新框架、新决策
- 对已有 Wiki 内容的补充或修正
- 用户明确表达"这个值得记"的内容

排除：
- 纯操作性内容（帮我改个 bug、执行某个命令）
- 已在 Wiki 中有详细记录的内容（无新增）

### 第 2 步：提议页面结构

向用户提议：

```
本次对话产生了以下值得记录的内容：

1. [新洞见摘要] → 建议写入 concepts/XXX.md（新建）
2. [补充内容] → 建议更新 concepts/YYY.md（已有）

确认后执行？
```

### 第 3 步：执行写入

用户确认后，调用 `wiki` skill 执行具体写入操作（遵循 MyWiki/AGENTS.md 的格式规范）。

### 第 4 步：更新 hot.md

写入完成后，追加更新 `/Users/zhuqichen/Documents/WorkSpace/Asrocky01/MyWiki/hot.md` 的"最近摄入"和"活跃话题"部分。

---

## 会话结束时

用户说"结束"/"bye"/"收工"时：

1. **提议更新 context.md**：
   ```
   本次会话结论：
   - [结论1]
   - [结论2]

   要更新到 memory/context.md 吗？
   ```

2. **提议更新 MEMORY.md**：
   将 context.md 的新内容摘要同步到全局 MEMORY.md 的"上次会话关键结论"部分。

---

## 注意事项

- **不要强制触发**：若对话明显是代码任务（改 bug、写函数），跳过前向注入
- **不要重复已知**：若 Wiki 内容用户显然已知（刚讨论过），不必再引用
- **提议而非强制**：后向 ingest 永远先提议，用户确认再执行
- **保持简洁**：`[Wiki]` 提示语要简短，不要打断对话流
