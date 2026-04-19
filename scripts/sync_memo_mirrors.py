#!/usr/bin/env python3
"""Sync memo metadata mirrors in writing/memos/*.md from memos/*/MEMO.yml.

Memo source-of-truth lives in:
  - memos/<slug>/MEMO.yml
  - memos/<slug>/tex/memo.tex

The writing markdown files remain collection/index metadata mirrors for site sync.
This script keeps frontmatter aligned while preserving existing markdown body text.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

import yaml


def parse_frontmatter(md_text: str) -> tuple[dict, str]:
    if not md_text.startswith("---\n"):
        return {}, md_text
    m = re.match(r"^---\n([\s\S]*?)\n---\n?", md_text)
    if not m:
        return {}, md_text
    fm_raw = m.group(1)
    body = md_text[m.end() :]
    data = yaml.safe_load(fm_raw) or {}
    if not isinstance(data, dict):
        data = {}
    return data, body


def render_frontmatter(meta: dict) -> str:
    lines: list[str] = ["---"]
    ordered_keys = ["title", "date", "summary", "status", "type", "pdfPath", "audioPath", "tags"]

    for k in ordered_keys:
        if k not in meta:
            continue
        v = meta[k]
        if k == "tags":
            lines.append("tags:")
            tags = v or []
            for t in tags:
                lines.append(f"  - {t}")
        elif k == "date":
            lines.append(f"date: {v}")
        else:
            # force quoted strings for stable rendering
            s = str(v).replace('"', '\\"')
            lines.append(f'{k}: "{s}"')

    lines.append("---")
    return "\n".join(lines) + "\n\n"


def expected_from_memo_yml(data: dict) -> dict:
    out = {
        "title": data.get("title", ""),
        "date": data.get("date", ""),
        "summary": data.get("summary", ""),
        "status": data.get("status", "draft"),
        "type": "memo",
        "pdfPath": data.get("pdfPath", ""),
        "tags": data.get("tags", []) or [],
    }
    audio_path = str(data.get("audioPath", "") or "").strip()
    if audio_path:
        out["audioPath"] = audio_path
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if mirrors are out of sync")
    args = ap.parse_args()

    root = Path("memos")
    mirror_dir = Path("writing/memos")
    mirror_dir.mkdir(parents=True, exist_ok=True)

    changed: list[Path] = []
    checked = 0

    for memo_dir in sorted(root.iterdir() if root.exists() else []):
        if not memo_dir.is_dir() or memo_dir.name.startswith("_"):
            continue

        memo_yml = memo_dir / "MEMO.yml"
        memo_tex = memo_dir / "tex" / "memo.tex"
        if not memo_yml.exists() or not memo_tex.exists():
            continue

        checked += 1

        src = yaml.safe_load(memo_yml.read_text(encoding="utf-8")) or {}
        if not isinstance(src, dict):
            raise SystemExit(f"sync_memo_mirrors: invalid YAML object in {memo_yml}")

        slug = memo_dir.name
        expected = expected_from_memo_yml(src)

        mirror_md = mirror_dir / f"{slug}.md"
        existing = mirror_md.read_text(encoding="utf-8") if mirror_md.exists() else ""
        _existing_meta, body = parse_frontmatter(existing)

        if not body.strip():
            body = (
                "This memo is authored in the LaTeX memo pipeline and rendered from generated artifacts.\n"
            )

        new_text = render_frontmatter(expected) + body.lstrip("\n")
        if existing != new_text:
            changed.append(mirror_md)
            if not args.check:
                mirror_md.write_text(new_text, encoding="utf-8")

    if args.check and changed:
        print("sync_memo_mirrors: out-of-sync mirrors detected:")
        for p in changed:
            print(f"  - {p}")
        return 1

    if args.check:
        print(f"sync_memo_mirrors: OK ({checked} memo(s))")
    else:
        if changed:
            print(f"sync_memo_mirrors: updated {len(changed)} file(s)")
            for p in changed:
                print(f"  - {p}")
        else:
            print(f"sync_memo_mirrors: no changes ({checked} memo(s))")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
