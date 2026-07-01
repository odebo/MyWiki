# wiki-mcp 远程部署方案

## 0. 先想清楚：你真的需要远程吗？

远程 MCP 的唯一价值是「**当你本机不在时，别的设备/人也能访问**」。问自己三个问题：

1. 你会在手机/平板/另一台电脑上，让 agent 访问这份 wiki 吗？
2. 有没有别人需要跟你共享同一份 wiki？
3. 有没有定时任务（比如凌晨自动 ingest）需要 server 一直在线？

**三个都否 → 不要上远程**。本地 stdio 已经最优，本文件可以不看。

只要有一个 yes，继续往下看。

---

## 1. 三种方案对比

| 方案 | 月成本 | 永远在线 | 改造量 | 适合 |
|---|---|---|---|---|
| **A. Cloudflare Tunnel + 本机** | ¥0 | ❌（Mac 关了就没） | 极小 | 想从手机临时访问，Mac 通常开着 |
| **B. VPS（小鸡）** | ¥30–50 | ✅ | 中等 | 想要真正随时可用 |
| **C. 家里的树莓派/迷你主机** | ¥0（电费忽略） | ✅（只要不断电） | 中等 | 有闲置设备、不想月付 |

**推荐 B（VPS）**：成本最低的「真·永远在线」方案。下面详细写 B，A 和 C 在末尾简述。

---

## 2. 方案 B：VPS 部署（推荐）

### 2.1 你需要准备什么

| 项目 | 选什么 | 备注 |
|---|---|---|
| 一台 VPS | Hetzner CX22 / Vultr / DigitalOcean Droplet | 1 vCPU / 1GB RAM 足够 |
| 系统 | Ubuntu 22.04 LTS | 别用最新版，求稳 |
| 一个域名（可选） | 任意注册商，¥70/年 | 不要域名也行，用 Cloudflare Tunnel 免费子域名 |
| git 凭证 | GitHub Deploy Key（写权限） | 让 VPS 能 push 回 wiki 仓库 |

### 2.2 真实成本

| 项 | 一次性 | 月度 |
|---|---|---|
| Hetzner CX22 | ¥0 | €3.29 ≈ ¥26 |
| 域名（可选） | ¥70/年 ≈ ¥6/月 | — |
| HTTPS 证书 | ¥0（Let's Encrypt） | — |
| Cloudflare | ¥0 | — |
| **合计** | ¥0–70 | **¥26–32/月** |

不用域名、用 Cloudflare Tunnel 免费子域名 → **每月 26 元**。

### 2.3 架构

```
[手机/另一台电脑上的 Claude/Codex]
              │ HTTPS
              ▼
      [Cloudflare Tunnel]  ← 免费提供 HTTPS + 隐藏 VPS IP
              │
              ▼
      [VPS: wiki-mcp HTTP server :8787]
              │
              ▼
      [VPS: ~/my-wiki/  (git repo)]
              │ git push/pull
              ▼
        [GitHub: wiki 仓库]
              │
              ▼
      [你的 Mac: git pull 拿到最新]
```

关键点：**wiki 的「真身」还是 GitHub 仓库**。VPS 和 Mac 都只是 clone，靠 git 双向同步。

### 2.4 必须改造的代码

当前 wiki-mcp 是 stdio + 直接读写本地文件。远程化要改三处：

#### 改造 1：传输方式 stdio → HTTP

`server.py` 末尾的 `mcp.run()` 改成：

```python
def main():
    mcp.run(transport="http", host="127.0.0.1", port=8787)
```

FastMCP 自带 HTTP transport，不用额外写 web server。

#### 改造 2：加访问鉴权

公网暴露的 MCP 必须加 token，否则任何知道 URL 的人都能读写你的 wiki、执行 git push。FastMCP 支持 Bearer token：

```python
from mcp.server.auth import AuthProvider  # 简化示意

mcp = FastMCP("my-wiki", auth=TokenAuthProvider(tokens=os.environ["WIKI_MCP_TOKENS"].split(",")))
```

客户端配置里带 `Authorization: Bearer <token>` 头。

#### 改造 3：git 同步逻辑

VPS 上的 wiki 是 clone 副本，会有「Mac 改了 → VPS 没拉到」「VPS ingest 了 → Mac 没拉到」的同步问题。两个方向都要处理：

- **VPS ingest 后**：`commit_and_push` 已经会 push 到 GitHub，✅ 现成
- **VPS ingest 前**：需要先 `git pull` 拿 Mac 上的最新改动 → 加一个新工具 `sync_from_remote()`，或让 `commit_and_push` 内部先 pull 再 push

建议加一个 `sync()` 工具：

```python
@mcp.tool()
def sync() -> str:
    """git pull && git push,同步远端改动。ingest 前后都建议调用。"""
```

---

## 2.5 部署步骤（VPS 端）

```bash
# 1. SSH 登录 VPS
ssh root@<vps-ip>

# 2. 装 uv（Python 包管理器）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. clone wiki 和 wiki-mcp
cd ~
git clone <wiki-repo-url> my-wiki
git clone <wiki-mcp-repo-url> my-wiki-mcp

# 4. 配 git 凭证（Deploy Key）
ssh-keygen -t ed25519 -f ~/.ssh/wiki_deploy_key -N ""
cat ~/.ssh/wiki_deploy_key.pub  # 加到 GitHub repo 的 Deploy Keys,勾选允许写
# 配 ssh config 让 wiki repo 用这个 key

# 5. 装 wiki-mcp
cd my-wiki-mcp && uv sync

# 6. 配环境变量
cat > ~/.wiki-mcp.env <<EOF
WIKI_ROOT=/root/my-wiki
WIKI_MCP_TOKENS=<生成一个长随机字符串>
EOF

# 7. 装 Cloudflare Tunnel(免费,省域名+HTTPS)
# 按 https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
# 配一个 tunnel 把 https://wiki-mcp.<你的>.cfargotunnel.com → http://localhost:8787

# 8. 用 systemd 让 server 常驻
cat > /etc/systemd/system/wiki-mcp.service <<EOF
[Unit]
Description=wiki-mcp
After=network.target

[Service]
ExecStart=/root/.local/bin/uvx --from /root/my-wiki-mcp wiki-mcp
EnvironmentFile=/root/.wiki-mcp.env
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl enable --now wiki-mcp
```

### 2.6 客户端配置

Claude Code（`~/.claude.json` 的 `mcpServers.wiki`）改成：

```json
"wiki": {
  "type": "http",
  "url": "https://wiki-mcp.<你的>.cfargotunnel.com/mcp",
  "headers": { "Authorization": "Bearer <你的token>" }
}
```

Codex（`~/.codex/config.toml`）改成：

```toml
[mcp_servers.wiki]
url = "https://wiki-mcp.<你的>.cfargotunnel.com/mcp"
auth = "Bearer <你的token>"
```

---

## 3. 方案 A：Cloudflare Tunnel + 本机（免费版）

如果你只是偶尔想从手机/笔记本访问，且 Mac 通常开着：

1. 在 Mac 上装 `cloudflared`，配 tunnel 把本地 `localhost:8787` 暴露成 `https://wiki-mcp.xxx.cfargotunnel.com`
2. wiki-mcp 改成 HTTP transport（同 2.4 改造 1）
3. 加 token 鉴权（同 2.4 改造 2）
4. 客户端配置同 2.6

**成本 ¥0**，但 Mac 关机就没。适合「我自己在外面偶尔用一下」。

---

## 4. 方案 C：树莓派/迷你主机在家

跟方案 B 完全一样，只是把 VPS 换成家里的 Pi：

- 一次性投入：树莓派 4B（¥300–500）或 N100 迷你主机（¥600–800）
- 月成本：电费 ¥3–5
- 部署步骤同方案 B
- 用 Cloudflare Tunnel 暴露（家庭宽带没公网 IP 也能用）

**适合**：有闲置设备、不想月付、家里网络稳定。**不适合**：家里常断电/断网、搬家频繁。

---

## 5. 三方案怎么选

| 你的情况 | 选 |
|---|---|
| 只是想试试，Mac 常开 | **A**（免费） |
| 想要真正随时可用，不想折腾硬件 | **B**（¥26/月） |
| 有闲置 Pi，想一次性买断 | **C**（一次性 ¥300–800） |
| 单人单机，本机用得挺好 | **不部署**，本地 stdio 继续用 |

---

## 6. 必须注意的坑

1. **鉴权不能省**。公网 MCP 不加 token = 任何人能读写你 wiki + 触发 git push。最低限度加 Bearer token, ideally 加 IP 白名单。

2. **git 冲突**。Mac 和 VPS 都改了 wiki 但没互相同步 → push 时冲突。建议养成习惯：每端 ingest 前先 `sync()`,ingest 后 `commit_and_push()`。

3. **token 别 commit 进 git**。放 `~/.wiki-mcp.env`,加进 `.gitignore`。

4. **Cloudflare Tunnel 比开端口安全**。不要直接把 VPS 的 8787 端口暴露公网,用 tunnel 套一层。

5. **备份仍是 GitHub**。VPS 挂了不要紧,wiki 真身在 GitHub,重 clone 就回来。

---

## 7. 我的建议

**先别部署**。你目前的本地 stdio 配置完全够用,远程化的真实成本不是钱(¥26/月不算什么),而是**架构复杂度**:

- 要改代码（transport + auth + sync）
- 要运维（VPS 挂了得会排查）
- 要处理 git 同步冲突

这些隐性成本远超 ¥26/月。

**触发远程化的真实信号**：某天你发现「我现在就需要从手机查 wiki,但 Mac 不在身边」——那时候再按方案 A（免费）起步。如果发现一周要用好几次,再升级到 B 或 C。

在此之前,本地 stdio + git push 就是最优解。
