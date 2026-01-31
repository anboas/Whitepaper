#!/usr/bin/env python3
"""Helpers for multi-paper layout."""

from __future__ import annotations

from pathlib import Path


def list_paper_dirs(root: Path = Path("papers")) -> list[Path]:
    if not root.exists():
        return []
    out: list[Path] = []
    for p in sorted(root.iterdir()):
        if not p.is_dir():
            continue
        if p.name.startswith("_"):
            continue
        if (p / "tex" / "paper.tex").exists():
            out.append(p)
    return out
