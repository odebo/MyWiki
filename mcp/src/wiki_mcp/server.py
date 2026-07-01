"""MCP server exposing a Karpathy-style LLM Wiki knowledge base.

Read tools:
- search_wiki: full-text search
- get_page: read a page by slug (optionally a single section)
- list_recent_ingests: parse log.md for recent ingest entries
- list_by_author: filter pages by author
- get_topic: read a topics/ page
- get_hot_cache: read hot.md safely (default: most recent 最近摄入 section + 活跃话题)

Write tools (for cross-agent ingest):
- create_page: write a new concept/opinion/source/topic page
- append_log: append a section to log.md
- update_index_counts: recompute page counts in index.md
- commit_and_push: git add -A && commit && push in the wiki root
"""
from __future__ import annotations

import os
import re
import subprocess
from datetime import date
from pathlib import Path

import yaml

from mcp.server.fastmcp import FastMCP

from . import parse, search

DEFAULT_WIKI_ROOT = os.environ.get("WIKI_ROOT", "")

mcp = FastMCP("wiki-mcp")


def _wiki_root() -> Path:
    return Path(os.environ.get("WIKI_ROOT", DEFAULT_WIKI_ROOT))


LARGE_FILE_THRESHOLD = 20_000  # 20 KB


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n\n[... truncated, {len(text) - limit} more chars]"


@mcp.tool()
def search_wiki(
    query: str,
    limit: int = 20,
    dirs: list[str] | None = None,
) -> str:
    """Full-text search across the wiki.

    Args:
        query: Search term (case-insensitive). Supports multi-word queries.
        limit: Max number of hits to return (default 20).
        dirs: Directories to search. Default: all four (concepts, opinions, sources, topics).

    Returns:
        Markdown list of hits, each with relative path and a snippet of the matching line.
        Use this to discover pages, then call get_page to read full content.

    Examples:
        search_wiki("正念")  # find all pages mentioning 正念
        search_wiki("克里斯坦森 资源配置", dirs=["opinions"])
    """
    if dirs is None:
        dirs = ["concepts", "opinions", "sources", "topics"]
    hits = search.search_wiki(_wiki_root(), query, dirs, limit)
    if not hits:
        return f"No hits for '{query}'."
    lines = [f"**{len(hits)} hits for '{query}':**\n"]
    for h in hits:
        lines.append(f"- `[[{h.slug}]]` ({h.rel_path})\n  > {h.snippet}")
    return "\n".join(lines)


@mcp.tool()
def get_page(slug: str, section: str | None = None) -> str:
    """Read a wiki page by its slug (filename without .md).

    Args:
        slug: Page slug, e.g. "正念冥想-安德烈" or "界限三层次-塔瓦布".
              If the exact slug isn't found, returns top-5 fuzzy matches.
        section: Optional ## section title. If given, returns only that section's body.

    Returns:
        Page content as markdown. For files > 20KB without a section, returns the first
        5KB + a list of available sections so you can call again with section=.

    Examples:
        get_page("正念冥想-安德烈")
        get_page("界限-塔瓦布", section="书籍信息")
    """
    path = parse.find_page_by_slug(_wiki_root(), slug)
    if path is None:
        candidates = parse.fuzzy_match_slug(_wiki_root(), slug, limit=5)
        if not candidates:
            return f"Page '{slug}' not found and no candidates available."
        lines = [f"Page '{slug}' not found. Did you mean:"]
        for c_slug, c_path, score in candidates:
            lines.append(f"- `[[{c_slug}]]` ({c_path})  score={score:.0f}")
        return "\n".join(lines)

    text = path.read_text(encoding="utf-8")
    fm, body = parse.parse_frontmatter(text)

    if section:
        sliced = parse.slice_section(body, section)
        if sliced is None:
            available = parse.list_sections(body)
            return (
                f"Section '## {section}' not found in [[{slug}]]. "
                f"Available sections: {', '.join(available) or '(none)'}"
            )
        header = f"# {slug} → ## {section}\n\n"
        if fm:
            header += f"<frontmatter>\n{fm}\n</frontmatter>\n\n"
        return header + sliced

    # Full page
    if len(text) > LARGE_FILE_THRESHOLD:
        available = parse.list_sections(body)
        truncated = _truncate(text, 5000)
        return (
            f"{truncated}\n\n"
            f"---\n[File is {len(text)} bytes. Available sections: "
            f"{', '.join(available) or '(none)'}]\n"
            f"Call get_page(slug, section='...') to read a specific section."
        )
    return text


@mcp.tool()
def list_recent_ingests(limit: int = 10) -> str:
    """List recent ingest entries from log.md.

    Args:
        limit: Number of entries to return (default 10).

    Returns:
        Markdown list of recent ingests with date and description.
        Each entry shows the book/source title and the page delta (e.g. "1696→1706页").
    """
    log_path = _wiki_root() / "log.md"
    if not log_path.exists():
        return "log.md not found."
    text = log_path.read_text(encoding="utf-8")
    entries = parse.parse_log_entries(text, limit=limit)
    if not entries:
        return "No ingest entries found in log.md."
    lines = [f"**Recent {len(entries)} ingests:**\n"]
    for e in entries:
        # Extract just the first line (the title) for compactness
        title_line = e["raw"].split("\n", 1)[0]
        lines.append(f"- {title_line}")
    return "\n".join(lines)


@mcp.tool()
def list_by_author(
    author: str,
    types: list[str] | None = None,
) -> str:
    """List all pages by a specific author.

    For opinions, matches the 'opinion_of' frontmatter field.
    For concepts/sources, matches the author name in filename or 'sources' frontmatter field.

    Args:
        author: Author name (partial match, case-insensitive). E.g. "克里斯坦森", "安德烈".
        types: Page types to search. Default: opinions, concepts, sources.

    Returns:
        Markdown list grouped by type, with slug and a snippet.

    Examples:
        list_by_author("克里斯坦森")
        list_by_author("安德烈", types=["opinions"])
    """
    if types is None:
        types = ["opinions", "concepts", "sources"]
    hits = search.filter_by_author(_wiki_root(), author, types)
    if not hits:
        return f"No pages found for author '{author}'."
    # Group by type
    by_type: dict[str, list[search.SearchHit]] = {}
    for h in hits:
        t = h.rel_path.split("/", 1)[0]
        by_type.setdefault(t, []).append(h)
    lines = [f"**Pages by '{author}' ({len(hits)} total):**\n"]
    for t in types:
        if t not in by_type:
            continue
        lines.append(f"\n### {t} ({len(by_type[t])})\n")
        for h in by_type[t]:
            lines.append(f"- `[[{h.slug}]]` — {h.snippet[:120]}")
    return "\n".join(lines)


@mcp.tool()
def get_topic(topic: str) -> str:
    """Read a topic aggregation page from topics/.

    Topic pages aggregate related opinions/concepts/sources and serve as the
    graph's middle layer. Use this to explore a theme.

    Args:
        topic: Topic name (slug or display name). E.g. "个人成长", "心理学".

    Returns:
        Topic page content. If exact match not found, returns fuzzy candidates.

    Examples:
        get_topic("个人成长")
        get_topic("心理学")
    """
    # Try exact match first
    topic_path = _wiki_root() / "topics" / f"{topic}.md"
    if not topic_path.exists():
        # Fuzzy match within topics/
        topics_dir = _wiki_root() / "topics"
        if not topics_dir.exists():
            return f"topics/ directory not found."
        candidates = []
        for p in topics_dir.glob("*.md"):
            score = _similarity(topic, p.stem)
            if score > 50:
                candidates.append((p.stem, p.name, score))
        candidates.sort(key=lambda x: x[2], reverse=True)
        if not candidates:
            return f"Topic '{topic}' not found."
        lines = [f"Topic '{topic}' not found exactly. Candidates:"]
        for slug, name, score in candidates[:5]:
            lines.append(f"- `[[{slug}]]` (topics/{name})  score={score:.0f}")
        return "\n".join(lines)

    text = topic_path.read_text(encoding="utf-8")
    if len(text) > LARGE_FILE_THRESHOLD:
        fm, body = parse.parse_frontmatter(text)
        available = parse.list_sections(body)
        truncated = _truncate(text, 5000)
        return (
            f"{truncated}\n\n---\n[File is {len(text)} bytes. "
            f"Available sections: {', '.join(available) or '(none)'}]"
        )
    return text


def _similarity(a: str, b: str) -> float:
    """Simple similarity score for fuzzy topic matching."""
    from rapidfuzz import fuzz
    return float(fuzz.WRatio(a, b))


@mcp.tool()
def get_hot_cache(section: str | None = None) -> str:
    """Read hot.md — the cross-session context cache.

    By default returns ONLY the most recent '## 最近摄入（date）' section plus
    '## 活跃话题' (if present). This avoids dumping the 100KB+ full file.

    Args:
        section: Specific ## section title to read. Use this to access other sections
                 like '未解问题', '知识库状态', or a specific dated '最近摄入（YYYY-MM-DD）' section.

    Returns:
        Section content as markdown.

    Examples:
        get_hot_cache()  # latest ingest + active threads
        get_hot_cache("未解问题")
        get_hot_cache("最近摄入（2026-06-29）")
    """
    hot_path = _wiki_root() / "hot.md"
    if not hot_path.exists():
        return "hot.md not found."
    text = hot_path.read_text(encoding="utf-8")

    if section:
        sections = parse.parse_hot_cache_sections(text)
        if section in sections:
            return f"## {section}\n\n{sections[section]}"
        # Fuzzy match section title
        candidates = [
            (title, _similarity(section, title)) for title in sections
        ]
        candidates.sort(key=lambda x: x[1], reverse=True)
        if candidates and candidates[0][1] > 60:
            matched_title = candidates[0][0]
            return (
                f"Section '{section}' not found exactly. "
                f"Closest match: '{matched_title}'\n\n"
                f"## {matched_title}\n\n{sections[matched_title]}"
            )
        return (
            f"Section '{section}' not found. Available: "
            f"{', '.join(list(sections.keys())[:10])}"
        )

    # Default: latest 最近摄入 section + 活跃话题
    date, latest_body = parse.parse_recent_ingest_section(text)
    if not latest_body:
        return "No '最近摄入' section found in hot.md."

    parts = [f"## 最近摄入（{date}）\n\n{latest_body}"]

    sections = parse.parse_hot_cache_sections(text)
    for title in sections:
        if "活跃话题" in title:
            parts.append(f"\n\n## {title}\n\n{sections[title]}")
            break

    return "".join(parts)


VALID_PAGE_TYPES = ("concepts", "opinions", "sources", "topics")


def _valid_slug(slug: str) -> bool:
    """Slug is safe if non-empty, not '.'/'..', and contains no path separators."""
    if not slug or slug in (".", ".."):
        return False
    return not any(c in slug for c in "/\\")


@mcp.tool()
def create_page(
    page_type: str,
    slug: str,
    body: str,
    frontmatter: dict | None = None,
    overwrite: bool = False,
) -> str:
    """Create a new wiki page under concepts/ opinions/ sources/ or topics/.

    Refuses path traversal and accidental overwrites unless overwrite=True.

    Args:
        page_type: One of "concepts", "opinions", "sources", "topics".
        slug: Filename without .md. E.g. "正念冥想-安德烈". Must not contain "/" or "\\".
        body: Markdown body (without frontmatter). Frontmatter is prepended if provided.
        frontmatter: Optional dict serialized as YAML frontmatter. Common keys:
            - concepts/sources: updated, sources, related
            - opinions: updated, opinion_of, topic, sources, related
        overwrite: If False (default), refuse to overwrite an existing page. Set True to replace.

    Returns:
        Success message with relative path, or error description.

    Examples:
        create_page("opinions", "期待就是责备-山下英子", body, frontmatter={
            "updated": "2026-06-30", "opinion_of": "山下英子",
            "topic": "断舍离", "sources": [[俯瞰力-山下英子]],
            "related": [[入口浪费甚于出口浪费-山下英子]]
        })
    """
    if page_type not in VALID_PAGE_TYPES:
        return f"Invalid page_type '{page_type}'. Must be one of {VALID_PAGE_TYPES}."
    if not _valid_slug(slug):
        return f"Invalid slug '{slug}'. Must be non-empty and contain no '/' or '\\'."
    if slug.endswith(".md"):
        slug = slug[:-3]

    target = _wiki_root() / page_type / f"{slug}.md"
    if target.exists() and not overwrite:
        return (
            f"Page already exists: {page_type}/{slug}.md. "
            f"Call with overwrite=True to replace."
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    content = body
    if frontmatter:
        fm_yaml = yaml.safe_dump(
            frontmatter, allow_unicode=True, sort_keys=False, default_flow_style=False
        ).strip()
        content = f"---\n{fm_yaml}\n---\n\n{body}"

    target.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} bytes to {page_type}/{slug}.md"


@mcp.tool()
def append_log(entry: str) -> str:
    """Append a new section to log.md (append-only operation log).

    Args:
        entry: Markdown for the new entry. Should start with '## [YYYY-MM-DD] title'.
               If it doesn't start with '## ', a header is auto-generated with today's date.

    Returns:
        Success message.

    Example:
        append_log("## [2026-06-30] wiki: ingest 《某书》某作者 — 5 concepts + 4 opinions + 1 source\\n\\n详情...")
    """
    log_path = _wiki_root() / "log.md"
    if not log_path.exists():
        return "log.md not found."
    text = log_path.read_text(encoding="utf-8")
    body = entry.strip()
    if not body.startswith("## "):
        body = f"## [{date.today().isoformat()}] {body}"
    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + body + "\n"
    log_path.write_text(text, encoding="utf-8")
    return f"Appended entry to log.md ({len(body)} chars)"


@mcp.tool()
def update_index_counts() -> str:
    """Recompute page counts in index.md and update the '页面数' / '最后更新' lines.

    Counts markdown files in concepts/ opinions/ sources/ topics/ and rewrites the
    trailing summary line in index.md. Call this after create_page to keep the
    index in sync.

    Returns:
        Success message with the new counts.
    """
    idx_path = _wiki_root() / "index.md"
    if not idx_path.exists():
        return "index.md not found."
    root = _wiki_root()
    counts = {
        "concepts": len(list((root / "concepts").glob("*.md"))) if (root / "concepts").exists() else 0,
        "sources": len(list((root / "sources").glob("*.md"))) if (root / "sources").exists() else 0,
        "opinions": len(list((root / "opinions").glob("*.md"))) if (root / "opinions").exists() else 0,
        "topics": len(list((root / "topics").glob("*.md"))) if (root / "topics").exists() else 0,
    }
    total = sum(counts.values())
    today = date.today().isoformat()
    new_counts_line = (
        f"页面数：{total}（concepts {counts['concepts']} / "
        f"sources {counts['sources']} / opinions {counts['opinions']} / "
        f"topics {counts['topics']}）"
    )
    new_date_line = f"最后更新：{today}"

    text = idx_path.read_text(encoding="utf-8")
    text = re.sub(
        r"页面数：[^\n]*",
        new_counts_line,
        text,
    )
    text = re.sub(
        r"最后更新：[^\n]*",
        new_date_line,
        text,
    )
    idx_path.write_text(text, encoding="utf-8")
    return f"index.md updated: {new_counts_line} / {new_date_line}"


@mcp.tool()
def commit_and_push(message: str) -> str:
    """Run git add -A && git commit && git push in the wiki root.

    Use after create_page / append_log / update_index_counts to publish changes.
    If push fails (e.g. no upstream), the commit is still kept — the returned
    message will include the commit output and the push error so you can retry push.

    Args:
        message: Commit message. Auto-prefixed with 'wiki: ' if it doesn't already start with that.

    Returns:
        Combined stdout/stderr of add/commit/push, or an error description.
    """
    root = _wiki_root()
    if not (root / ".git").exists():
        return f"Not a git repo: {root}"

    msg = message.strip()
    if not msg:
        return "Empty commit message."
    if not msg.startswith("wiki:"):
        msg = f"wiki: {msg}"

    def run(*args: str) -> tuple[int, str]:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return proc.returncode, proc.stdout + proc.stderr

    try:
        rc, add_out = run("add", "-A")
        if rc != 0:
            return f"git add failed:\n{add_out}"
        rc, status = run("status", "--porcelain")
        if not status.strip():
            return "Nothing to commit (working tree clean)."
        rc, commit_out = run("commit", "-m", msg)
        if rc != 0:
            return f"git commit failed:\n{commit_out}"
        rc, push_out = run("push")
        if rc != 0:
            return (
                f"=== add ===\n{add_out}\n=== commit ===\n{commit_out}\n"
                f"=== push (FAILED, rc={rc}) ===\n{push_out}\n"
                f"Commit succeeded locally but push failed. Run "
                f"`git push` manually in {root}."
            )
        return f"=== add ===\n{add_out}\n=== commit ===\n{commit_out}\n=== push ===\n{push_out}"
    except subprocess.TimeoutExpired:
        return "git operation timed out (>120s)."


def main() -> None:
    """Entry point for the wiki-mcp console script."""
    mcp.run()


if __name__ == "__main__":
    main()
