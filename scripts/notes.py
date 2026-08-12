#!/usr/bin/env python3
"""Helpers for note artifact builds."""

from __future__ import annotations

from pathlib import Path
import re

import yaml


def parse_frontmatter(md_text: str) -> tuple[dict, str]:
    if not md_text.startswith("---\n"):
        return {}, md_text
    m = re.match(r"^---\n([\s\S]*?)\n---\n?", md_text)
    if not m:
        return {}, md_text
    data = yaml.safe_load(m.group(1)) or {}
    if not isinstance(data, dict):
        data = {}
    return data, md_text[m.end() :]


def note_status(path: Path) -> str:
    data, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
    return str(data.get("status") or "published")


def list_note_files(root: Path = Path("writing/notes")) -> list[Path]:
    if not root.exists():
        return []
    out: list[Path] = []
    for p in sorted(root.glob("*.md")):
        if p.name == "README.md":
            continue
        if note_status(p) != "published":
            continue
        out.append(p)
    return out
