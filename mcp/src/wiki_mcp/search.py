"""Full-text search across the wiki using ripgrep when available, Python re fallback."""
from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class SearchHit:
    rel_path: str
    slug: str
    snippet: str
    score: float


def _has_rg() -> bool:
    return shutil.which("rg") is not None


def _search_with_rg(wiki_root: Path, query: str, dirs: list[str], limit: int) -> list[SearchHit]:
    """Use ripgrep for fast full-text search. Returns hits sorted by relevance."""
    cmd = [
        "rg",
        "--no-heading",
        "--line-number",
        "--with-filename",
        "--color", "never",
        "--max-count", "3",
        "-i",
        query,
    ]
    paths = [str(wiki_root / d) for d in dirs if (wiki_root / d).exists()]
    cmd.extend(paths)
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10, check=False
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []
    hits: dict[str, list[str]] = {}
    for line in result.stdout.splitlines():
        # format: path:lineno:content
        m = re.match(r"^(.+?):(\d+):(.*)$", line)
        if not m:
            continue
        path_str, _line_no, content = m.group(1), m.group(2), m.group(3)
        try:
            rel = str(Path(path_str).relative_to(wiki_root))
        except ValueError:
            rel = path_str
        hits.setdefault(rel, []).append(content.strip())

    ranked: list[SearchHit] = []
    for rel, lines in hits.items():
        slug = Path(rel).stem
        # Score: more matches + filename match boosts
        score = len(lines) * 1.0
        if query.lower() in slug.lower():
            score += 5.0
        snippet = " ... ".join(lines[:3])[:300]
        ranked.append(SearchHit(rel_path=rel, slug=slug, snippet=snippet, score=score))

    ranked.sort(key=lambda h: h.score, reverse=True)
    return ranked[:limit]


def _search_with_python(wiki_root: Path, query: str, dirs: list[str], limit: int) -> list[SearchHit]:
    """Fallback: scan files with Python re."""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    hits: list[SearchHit] = []
    for d in dirs:
        dir_path = wiki_root / d
        if not dir_path.exists():
            continue
        for p in dir_path.glob("*.md"):
            try:
                text = p.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            matches = pattern.findall(text)
            if not matches:
                continue
            slug = p.stem
            rel = f"{d}/{p.name}"
            # Extract first matching line as snippet
            snippet_lines = []
            for line in text.splitlines():
                if pattern.search(line):
                    snippet_lines.append(line.strip())
                    if len(snippet_lines) >= 3:
                        break
            snippet = " ... ".join(snippet_lines)[:300] or text[:200]
            score = len(matches) + (5.0 if query.lower() in slug.lower() else 0.0)
            hits.append(SearchHit(rel_path=rel, slug=slug, snippet=snippet, score=score))
    hits.sort(key=lambda h: h.score, reverse=True)
    return hits[:limit]


def search_wiki(
    wiki_root: Path,
    query: str,
    dirs: Optional[list[str]] = None,
    limit: int = 20,
) -> list[SearchHit]:
    """Search the wiki. Tries ripgrep first, falls back to Python."""
    if dirs is None:
        dirs = ["concepts", "opinions", "sources", "topics"]
    wiki_root = Path(wiki_root)
    if _has_rg():
        hits = _search_with_rg(wiki_root, query, dirs, limit)
        if hits:
            return hits
    return _search_with_python(wiki_root, query, dirs, limit)


def filter_by_author(
    wiki_root: Path,
    author: str,
    types: Optional[list[str]] = None,
) -> list[SearchHit]:
    """Filter pages by author. For opinions, checks frontmatter 'opinion_of'.
    For concepts/sources, checks filename suffix and frontmatter.

    Returns a list of SearchHit-like objects with slug, rel_path, snippet.
    """
    if types is None:
        types = ["opinions", "concepts", "sources"]
    wiki_root = Path(wiki_root)
    results: list[SearchHit] = []
    author_lower = author.lower()

    # parse frontmatter lazily
    from .parse import parse_frontmatter

    for t in types:
        dir_path = wiki_root / t
        if not dir_path.exists():
            continue
        for p in dir_path.glob("*.md"):
            # Quick filename check first (cheap)
            stem_lower = p.stem.lower()
            filename_match = author_lower in stem_lower

            try:
                text = p.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            fm_match = False
            fm, _ = parse_frontmatter(text)
            if t == "opinions":
                fm_author = fm.get("opinion_of", "")
                if isinstance(fm_author, str) and author_lower in fm_author.lower():
                    fm_match = True
            else:
                # sources/concepts may have author in sources field or title
                sources_field = fm.get("sources", [])
                if isinstance(sources_field, list):
                    for s in sources_field:
                        if isinstance(s, str) and author_lower in s.lower():
                            fm_match = True
                            break

            if not (filename_match or fm_match):
                continue

            # Build a snippet: first 200 chars of body
            _, body = parse_frontmatter(text)
            snippet = body.strip()[:200].replace("\n", " ")
            score = 10.0 if fm_match else 5.0
            if filename_match:
                score += 3.0
            results.append(SearchHit(
                rel_path=f"{t}/{p.name}",
                slug=p.stem,
                snippet=snippet,
                score=score,
            ))
    results.sort(key=lambda h: h.score, reverse=True)
    return results
