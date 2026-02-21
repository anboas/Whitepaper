#!/usr/bin/env python3
"""Helpers for multi-memo layout."""

from __future__ import annotations

from pathlib import Path


def list_memo_dirs(root: Path = Path("memos")) -> list[Path]:
    if not root.exists():
        return []
    out: list[Path] = []
    for p in sorted(root.iterdir()):
        if not p.is_dir():
            continue
        if p.name.startswith("_"):
            continue
        if (p / "tex" / "memo.tex").exists() and (p / "MEMO.yml").exists():
            out.append(p)
    return out
