# Agent CLAUDE.md 模板

这个目录提供一个**聊天机器人 agent 的人格 + 行为规则模板**，配合 [`wiki-mcp`](../) 使用，让 agent 能把 LLM Wiki 当作知识来源、自动 ingest 新内容、回答时引用具体页面。

## 模板是什么

[`agent-CLAUDE.md`](agent-CLAUDE.md) 是一份 Claude Code 项目级 `CLAUDE.md`，定义了一个以 LLM Wiki 为知识来源的 agent。它规定了：

- **身份**：名字、性格、知识来源
- **收到消息时的行为**：先读 wiki 热缓存 → 检索 → 引用页面回答
- **收到文章链接时的行为**：抓取 → ingest 成 concepts/opinions/sources → 更新目录 → 写日志 → git push
- **对话产生新洞见时**：主动提议存回 wiki
- **页面格式**：concepts / opinions / sources 的 frontmatter 和正文模板
- **禁忌**：不凭记忆、不编造引用、不改 raw/

模板里所有路径都用 `<bot-name>`、`WIKI_ROOT` 这类占位符，复制后改成自己的就行。

## 怎么用

### 前置条件

1. 已有 LLM Wiki 仓库（四层结构：`concepts/ opinions/ sources/ topics/`）
2. 已安装 [wiki-mcp](../README.md) 并配好 MCP 客户端
3. 已有聊天机器人桥接工具（推荐 [cc-connect](https://github.com/chenhg5/cc-connect)，支持飞书/Telegram/Slack/Discord 等）

### 三步搭建

#### 1. 复制模板到 agent 工作区

```bash
mkdir -p ~/Documents/WorkSpace/my-bot/<你的机器人名>
cp agent-CLAUDE.md ~/Documents/WorkSpace/my-bot/<你的机器人名>/CLAUDE.md
```

#### 2. 编辑 CLAUDE.md，替换占位符

```bash
cd ~/Documents/WorkSpace/my-bot/<你的机器人名>
# 把所有 <bot-name> 替换成你的机器人名字
sed -i '' 's/<bot-name>/初号机/g' CLAUDE.md   # macOS
# 或 Linux:  sed -i 's/<bot-name>/初号机/g' CLAUDE.md
```

可以再按需调整：
- **性格描述**——改成你想要的语气
- **Ingest 强度**——文章默认 2-4 concepts + 1-2 opinions + 1 source，书的话按 5+4+1（见 wiki-ingest skill）
- **禁忌清单**——按你的偏好增删

#### 3. 配置 cc-connect 指向这个工作区

在 `~/.cc-connect/config.toml` 里：

```toml
[[projects]]
  name = "<你的机器人名>"

  [projects.agent]
    type = "claudecode"

    [projects.agent.options]
      mode = "acceptEdits"   # 允许 ingest 时直接写文件
      work_dir = "/abs/path/to/your-bot-workspace"

  [[projects.platforms]]
  type = "feishu"   # 或 telegram / slack / ...

  [projects.platforms.options]
  app_id = "${FEISHU_APP_ID}"
  app_secret = "${FEISHU_APP_SECRET}"
```

可选：在 `[projects.agent.options]` 加 `system_prompt = "你是 <你的机器人名>，严格遵循工作区 CLAUDE.md 的行为约定。"` 强化人格。

### 启动

```bash
cc-connect daemon start
# 或前台跑：cc-connect run
```

在飞书（或你选的平台）给机器人发条消息，它会：
1. 用 `work_dir` 起 claude CLI
2. 自动加载用户级 wiki MCP（如果配在 `~/.claude.json`）或项目级 `.mcp.json`
3. 读取工作区 `CLAUDE.md` 作为人格和行为规则
4. 收到消息先查 wiki，回答时引用页面

## 关键设计点

### 为什么 agent 工作区不存知识内容

工作区只是 agent 的"驾驶舱"——CLAUDE.md 定义人格，session 状态自动管理。**知识内容全部在 wiki 仓库**，通过 MCP 访问。这样：
- 工作区可以随时重建，不丢任何知识
- 多个 agent 可以共享同一个 wiki
- wiki 仓库可以独立备份、版本控制

### 为什么用 `${ENV_VAR}` 而不是明文 secret

`~/.cc-connect/config.toml` 通常是用户级配置，不在 git 仓库里。但如果你想把 config 提交到 git（比如多设备同步），用 `${FEISHU_APP_SECRET}` 引用环境变量更安全。launchd/systemd 守护进程可以在 plist/unit 文件里注入 env var。

### 为什么 ingest 后要调 `commit_and_push`

`create_page` 只写文件，不提交。`commit_and_push` 一次性 `git add -A && commit && push`，把 ingest 的多个页面原子化推到远端。这样：
- 失败时不会留下半成品 commit
- 远端永远是完整的 ingest 单元

## 自定义扩展

### 加定时自主任务

在工作区放 `HEARTBEAT.md`，cc-connect 会定期触发：

```markdown
# Heartbeat

每天早上 9 点检查：
- wiki 有没有未解问题（hot.md 的"未解问题"段）
- 最近 ingest 的页面有没有 lint 问题
```

### 加技能（Skills）

在工作区 `.claude/skills/` 下放自定义 skill，agent 会按需调用。例如：
- `wiki-ingest` — 书籍 PDF 结构化 ingest（5 concepts + 4 opinions + 1 source）
- `wiki-bridge` — 对话中产生洞见后主动 ingest

### 切换模型

在工作区 CLAUDE.md 里加一句"优先用 opus 处理 ingest，用 sonnet 处理日常对话"，或在 cc-connect config 里设 `model = "opus"`。

## 故障排查

| 现象 | 排查 |
|------|------|
| 机器人不回消息 | `cc-connect daemon status` 看是否在跑；`tail -f ~/.cc-connect/logs/cc-connect.log` 看日志 |
| 回答不引用 wiki | 确认 wiki MCP 已加载——在工作区让 agent 跑 `claude mcp list`，应能看到 `wiki` |
| ingest 后没 push | 确认 wiki 仓库配了 remote——`git -C $WIKI_ROOT remote -v` |
| 微信文章抓不到 | 必须用 Tavily extract，WebFetch 会被微信拦截；确认 `TAVILY_API_KEY` env var 已设 |
| work_dir 不对 | 检查 `~/.cc-connect/projects/<name>.state.json` 里有没有 `work_dir_override` 残留 |

## 相关文档

- [wiki-mcp README](../README.md) — MCP server 本体
- [cc-connect](https://github.com/chenhg5/cc-connect) — 聊天平台桥接工具
- [Karpathy LLM Wiki](https://github.com/karpathy/llm.c) — 知识库模式灵感来源
