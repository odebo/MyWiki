"""Parsing utilities for my-wiki markdown files.

Handles:
- YAML frontmatter extraction
- Wikilink slug resolution ([[页面名]] → file path)
- Section slicing by ## headers
- Fuzzy matching for partial slugs
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml
from rapidfuzz import process, fuzz

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
SECTION_HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class Page:
    """A parsed wiki page."""
    path: Path
    slug: str
    frontmatter: dict
    body: str
    raw: str


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split text into (frontmatter_dict, body). Returns ({}, text) if no frontmatter."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    body = text[m.end():]
    return fm, body


def read_page(wiki_root: Path, rel_path: str | Path) -> Page:
    """Read a markdown file and parse it."""
    path = Path(wiki_root) / rel_path
    raw = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    slug = path.stem
    return Page(path=path, slug=slug, frontmatter=fm, body=body, raw=raw)


def find_page_by_slug(wiki_root: Path, slug: str) -> Optional[Path]:
    """Find a markdown file whose stem matches the slug across the four content dirs.

    Returns the path if exact match found, else None.
    """
    wiki_root = Path(wiki_root)
    for d in ("concepts", "opinions", "sources", "topics"):
        candidate = wiki_root / d / f"{slug}.md"
        if candidate.exists():
            return candidate
    # also check root-level files (hot.md, index.md, log.md)
    root_candidate = wiki_root / f"{slug}.md"
    if root_candidate.exists():
        return root_candidate
    return None


def fuzzy_match_slug(wiki_root: Path, slug: str, limit: int = 5) -> list[tuple[str, str, float]]:
    """Fuzzy-match a partial slug against all page slugs in the wiki.

    Returns list of (slug, relative_path, score) tuples, highest first.
    """
    wiki_root = Path(wiki_root)
    all_slugs: list[tuple[str, str]] = []  # (slug, rel_path)
    for d in ("concepts", "opinions", "sources", "topics"):
        dir_path = wiki_root / d
        if not dir_path.exists():
            continue
        for p in dir_path.glob("*.md"):
            all_slugs.append((p.stem, f"{d}/{p.name}"))
    # include root-level meta files
    for p in wiki_root.glob("*.md"):
        all_slugs.append((p.stem, p.name))

    if not all_slugs:
        return []

    slug_to_path = dict(all_slugs)
    matches = process.extract(
        slug,
        list(slug_to_path.keys()),
        scorer=fuzz.WRatio,
        limit=limit,
    )
    return [(m[0], slug_to_path[m[0]], m[1]) for m in matches]


def slice_section(body: str, section: str) -> Optional[str]:
    """Extract a ## section from page body. Returns None if not found."""
    # Find all section headers and their positions
    headers = list(SECTION_HEADER_RE.finditer(body))
    for i, m in enumerate(headers):
        if m.group(1).strip() == section.strip():
            start = m.end()
            end = headers[i + 1].start() if i + 1 < len(headers) else len(body)
            return body[start:end].strip()
    return None


def list_sections(body: str) -> list[str]:
    """Return all ## section titles in the body."""
    return [m.group(1).strip() for m in SECTION_HEADER_RE.finditer(body)]


def extract_wikilinks(text: str) -> list[str]:
    """Extract all [[wikilink]] targets from text."""
    return WIKILINK_RE.findall(text)


def parse_log_entries(log_text: str, limit: int = 10) -> list[dict]:
    """Parse log.md into structured ingest entries.

    Each entry: {date, raw, line_no}
    """
    entries = []
    lines = log_text.split("\n")
    current_entry: dict | None = None
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+\[(\d{4}-\d{2}-\d{2})\]\s+(.+)$", line)
        if m:
            if current_entry:
                entries.append(current_entry)
            current_entry = {
                "date": m.group(1),
                "title": m.group(2).strip(),
                "raw": line,
                "line_no": i + 1,
            }
        elif current_entry:
            current_entry["raw"] += "\n" + line
    if current_entry:
        entries.append(current_entry)
    return entries[:limit]


def parse_hot_cache_sections(hot_text: str) -> dict[str, str]:
    """Split hot.md into ## sections. Returns {section_title: section_body}."""
    headers = list(SECTION_HEADER_RE.finditer(hot_text))
    sections: dict[str, str] = {}
    for i, m in enumerate(headers):
        title = m.group(1).strip()
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(hot_text)
        sections[title] = hot_text[start:end].strip()
    return sections


def parse_recent_ingest_section(hot_text: str) -> tuple[str, str]:
    """Extract the most recent '## 最近摄入（YYYY-MM-DD）' section from hot.md.

    Returns (date_str, section_body). If not found, returns ("", "").
    """
    sections = parse_hot_cache_sections(hot_text)
    # Find the most recent 最近摄入 section by date
    ingest_sections = [
        (title, body) for title, body in sections.items()
        if title.startswith("最近摄入")
    ]
    if not ingest_sections:
        return "", ""
    # Sort by date descending (date is in parentheses — support both half/full-width)
    def extract_date(title: str) -> str:
        m = re.search(r"[\(（](\d{4}-\d{2}-\d{2})[\)）]", title)
        return m.group(1) if m else ""

    ingest_sections.sort(key=lambda x: extract_date(x[0]), reverse=True)
    title, body = ingest_sections[0]
    return extract_date(title), body
