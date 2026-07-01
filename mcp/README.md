# wiki-mcp

A [Model Context Protocol](https://modelcontextprotocol.io) server that exposes a [Karpathy-style LLM Wiki](https://github.com/karpathy/llm.c) — a markdown knowledge base structured as `concepts/ opinions/ sources/ topics/` — to LLM clients such as Claude Code, Claude Desktop, or any MCP-compatible agent.

The server is **wiki-agnostic**: point it at any directory that follows the four-layer convention via the `WIKI_ROOT` environment variable, and your agent gets read + write access to the knowledge graph.

## Wiki layout convention

```
my-wiki/
├── concepts/   # abstract concept pages (definitions / frameworks / tools)
├── opinions/   # strong propositional claims (one proposition per page)
├── sources/    # source summaries (one per original material)
├── topics/     # topic aggregation pages (the graph's middle layer)
├── hot.md      # cross-session context cache
├── index.md    # full directory listing
└── log.md      # append-only operation log
```

Wikilinks use the `[[slug]]` convention where `slug` is the filename stem (no `.md`).

## Quick start

```bash
# Run from source (no install)
uv run wiki-mcp

# Or install once and run anywhere
uvx --from git+https://github.com/zhuqichen/wiki-mcp wiki-mcp
```

The server speaks MCP over stdio. Point your MCP client at it (examples below).

## Configuration

### Claude Code / Claude Desktop

Add to your client's MCP config (e.g. `~/.claude.json` or a project-level `.mcp.json`):

```json
{
  "mcpServers": {
    "wiki": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/zhuqichen/wiki-mcp", "wiki-mcp"],
      "env": {
        "WIKI_ROOT": "/absolute/path/to/your/wiki"
      }
    }
  }
}
```

For local development, replace the `uvx` line with a direct path:

```json
{
  "mcpServers": {
    "wiki": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/wiki-mcp", "wiki-mcp"],
      "env": {
        "WIKI_ROOT": "/path/to/your/wiki"
      }
    }
  }
}
```

### cc-connect (Feishu / Telegram / Slack / ...)

If you bridge a messaging platform to Claude Code via [cc-connect](https://github.com/zhuqichen/cc-connect), the spawned Claude Code subprocess inherits the MCP config above. No cc-connect changes are needed — just make sure `work_dir` points at your wiki (so the project-level `.mcp.json` is picked up) or that the wiki server is registered at user level.

## Tools provided

### Read tools

| Tool | Purpose |
|------|---------|
| `search_wiki` | Full-text search (ripgrep-accelerated, Python fallback). Returns hits with snippets. |
| `get_page` | Read a page by slug, optionally a single `## section`. Fuzzy slug matching when exact match fails. |
| `get_topic` | Read a `topics/<name>.md` aggregation page. |
| `get_hot_cache` | Read `hot.md` safely — defaults to the latest ingest section + active threads. |
| `list_recent_ingests` | Parse `log.md` for recent ingest entries. |
| `list_by_author` | Filter pages by author across opinions / concepts / sources. |

### Write tools

| Tool | Purpose |
|------|---------|
| `create_page` | Create a new page under `concepts/` `opinions/` `sources/` `topics/`. Refuses path traversal and accidental overwrites. |
| `append_log` | Append a new entry to `log.md` (append-only operation log). |
| `update_index_counts` | Recompute page counts in `index.md` and update the summary line. |
| `commit_and_push` | Run `git add -A && git commit && git push` in the wiki root. |

The intended workflow: an LLM agent reads with the read tools, and when it produces a new insight it uses the write tools to ingest it back into the wiki — typically guided by a `wiki-ingest` skill in the host agent (Claude Code).

## Design notes

- **Size-protected reads**: Files > 20 KB return the first 5 KB + a list of `## sections`. Call `get_page(slug, section="...")` to drill in.
- **Fuzzy slug matching**: `get_page("正念冥想")` returns top-5 candidates by `rapidfuzz` score when the exact slug is missing.
- **Path-safe writes**: `create_page` rejects slugs containing `/` or `\`, and refuses to overwrite existing pages unless `overwrite=True`.
- **Frontmatter-aware**: `get_page` parses YAML frontmatter and renders it inside `<frontmatter>...</frontmatter>` for the model.
- **Reads never touch git**: only `commit_and_push` runs git. Read tools are side-effect-free.

## Development

```bash
# Run tests
uv run pytest

# Run server in dev mode (logs to stderr)
WIKI_ROOT=/path/to/your/wiki uv run wiki-mcp
```

Layout:

```
src/wiki_mcp/
├── server.py    # MCP tool definitions
├── parse.py     # frontmatter / section / slug helpers
└── search.py    # ripgrep + Python fallback search
tests/
└── test_parse.py
```

## License

MIT — see [LICENSE](LICENSE).
