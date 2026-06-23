---
updated: 2026-05-21
sources: [https://github.com/AgriciDaniel/claude-obsidian]
related: [[LLM-Wiki模式]], [[claude-obsidian]], [[Hot-Cache]]
---

# MCP 文件系统集成

通过 MCP（Model Context Protocol）让 Claude Code 直接读写 Obsidian vault 文件，消除复制粘贴。

## 问题：手动复制粘贴的摩擦

没有 MCP 时的工作流：
1. 在 Obsidian 打开文件 → 复制内容
2. 粘贴给 Claude → Claude 分析
3. 复制 Claude 输出 → 粘贴回 Obsidian

MCP 后：Claude 直接操作文件，用户只需发指令。

## 两种集成方式

### 方式 A：Obsidian Local REST API（推荐）

需要在 Obsidian 安装 **Local REST API** 社区插件。

```bash
claude mcp add-json obsidian-vault '{
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp-obsidian"],
  "env": {
    "OBSIDIAN_API_KEY": "your-api-key",
    "OBSIDIAN_HOST": "127.0.0.1",
    "OBSIDIAN_PORT": "27124",
    "NODE_TLS_REJECT_UNAUTHORIZED": "0"
  }
}' --scope user
```

优点：通过 Obsidian API，操作完全符合 vault 规范（触发 Obsidian 事件、更新索引等）

缺点：需要 Obsidian 保持运行

### 方式 B：直接文件系统访问（更简单）

```bash
claude mcp add-json obsidian-vault '{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@bitbonsai/mcpvault@latest", "/path/to/wiki"]
}' --scope user
```

优点：不依赖 Obsidian 运行，纯文件操作

缺点：绕过 Obsidian，不触发插件事件

## 配置位置

```
~/.claude/settings.json    # --scope user，全局生效
或
wiki/.claude/settings.json # 仅对 wiki 目录生效（推荐）
```

## 配置后的能力

Claude 可以：
- 直接读取任意 wiki 页面
- 创建新页面（自动写入正确位置）
- 更新 frontmatter（updated 日期等）
- 批量检查交叉引用
- 执行 lint，直接修复问题

## 与 VSCode 的协作

```
VSCode Terminal
  └── Claude Code（通过 MCP 读写 wiki/）
          ↕ 同一目录
Obsidian
  └── 实时显示 Claude 的写入结果
      Graph View 自动更新
```

Claude 在 VSCode 里写文件，Obsidian 里立刻可见，实现"AI 写、人看"的流畅分工。
**主题**：[[产品开发]] [[AI技术]]
