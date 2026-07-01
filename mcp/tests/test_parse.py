"""Tests for parse.py — run with `pytest`."""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from wiki_mcp import parse


@pytest.fixture
def tmp_wiki(tmp_path: Path) -> Path:
    """Create a minimal wiki structure for testing."""
    (tmp_path / "concepts").mkdir()
    (tmp_path / "opinions").mkdir()
    (tmp_path / "sources").mkdir()
    (tmp_path / "topics").mkdir()

    (tmp_path / "concepts" / "正念冥想-安德烈.md").write_text(
        "---\nupdated: 2026-06-29\nsources: [raw/x.pdf]\nrelated: [[其他]]\n---\n\n"
        "# 正念冥想\n\n核心定义...\n\n## 与已有知识的关联\n\n关联内容。\n",
        encoding="utf-8",
    )
    (tmp_path / "opinions" / "冥想的悖论-安德烈.md").write_text(
        "---\nopinion_of: 安德烈\ntopic: 心理学\n---\n\n# 命题\n\n主张内容。\n",
        encoding="utf-8",
    )
    (tmp_path / "topics" / "心理学.md").write_text(
        "---\ntype: topic\n---\n\n# 心理学\n\n## 相关观点\n\n- [[冥想的悖论-安德烈]]\n",
        encoding="utf-8",
    )
    (tmp_path / "hot.md").write_text(
        "---\ntype: hot-cache\n---\n\n# Hot Cache\n\n"
        "## 最近摄入（2026-06-29）\n\n最新一段。\n\n"
        "## 最近摄入（2026-06-28）\n\n旧一段。\n\n"
        "## 活跃话题\n\n话题1。\n",
        encoding="utf-8",
    )
    (tmp_path / "log.md").write_text(
        "---\ntype: log\n---\n\n"
        "## [2026-06-29] ingest | 《界限》— 5c+4o+1s；1706→1716页\n\n"
        "## [2026-06-28] ingest | 《开始冥想》— 5c+4o+1s；1688→1698页\n",
        encoding="utf-8",
    )
    return tmp_path


def test_parse_frontmatter(tmp_wiki: Path) -> None:
    text = (tmp_wiki / "concepts" / "正念冥想-安德烈.md").read_text(encoding="utf-8")
    fm, body = parse.parse_frontmatter(text)
    # yaml may parse as datetime.date — accept either str or date
    assert str(fm["updated"]).startswith("2026-06-29")
    assert "核心定义" in body


def test_find_page_by_slug_exact(tmp_wiki: Path) -> None:
    path = parse.find_page_by_slug(tmp_wiki, "正念冥想-安德烈")
    assert path is not None
    assert path.name == "正念冥想-安德烈.md"


def test_find_page_by_slug_not_found(tmp_wiki: Path) -> None:
    path = parse.find_page_by_slug(tmp_wiki, "不存在")
    assert path is None


def test_fuzzy_match_slug(tmp_wiki: Path) -> None:
    matches = parse.fuzzy_match_slug(tmp_wiki, "正念", limit=3)
    assert matches
    slugs = [m[0] for m in matches]
    assert "正念冥想-安德烈" in slugs


def test_slice_section(tmp_wiki: Path) -> None:
    page = parse.read_page(tmp_wiki, "concepts/正念冥想-安德烈.md")
    section = parse.slice_section(page.body, "与已有知识的关联")
    assert section is not None
    assert "关联内容" in section


def test_slice_section_not_found(tmp_wiki: Path) -> None:
    page = parse.read_page(tmp_wiki, "concepts/正念冥想-安德烈.md")
    section = parse.slice_section(page.body, "不存在的小节")
    assert section is None


def test_list_sections(tmp_wiki: Path) -> None:
    page = parse.read_page(tmp_wiki, "concepts/正念冥想-安德烈.md")
    sections = parse.list_sections(page.body)
    assert "与已有知识的关联" in sections


def test_extract_wikilinks() -> None:
    text = "see [[页面A]] and [[页面B]] for more."
    links = parse.extract_wikilinks(text)
    assert links == ["页面A", "页面B"]


def test_parse_log_entries(tmp_wiki: Path) -> None:
    text = (tmp_wiki / "log.md").read_text(encoding="utf-8")
    entries = parse.parse_log_entries(text, limit=5)
    assert len(entries) == 2
    assert entries[0]["date"] == "2026-06-29"
    assert "界限" in entries[0]["title"]


def test_parse_hot_cache_sections(tmp_wiki: Path) -> None:
    text = (tmp_wiki / "hot.md").read_text(encoding="utf-8")
    sections = parse.parse_hot_cache_sections(text)
    assert "最近摄入（2026-06-29）" in sections
    assert "活跃话题" in sections


def test_parse_recent_ingest_section(tmp_wiki: Path) -> None:
    text = (tmp_wiki / "hot.md").read_text(encoding="utf-8")
    date, body = parse.parse_recent_ingest_section(text)
    assert date == "2026-06-29"
    assert "最新一段" in body
