#!/usr/bin/env python3

"""Extract the <body> contents from Pandoc standalone HTML into a fragment.

We use this so the site repo can ingest a stable, style-free fragment.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


BODY_RE = re.compile(r"<body[^>]*>(?P<body>.*)</body>", re.IGNORECASE | re.DOTALL)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="Input HTML (standalone)")
    ap.add_argument("dst", help="Output HTML fragment")
    args = ap.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)

    html = src.read_text(encoding="utf-8", errors="strict")
    m = BODY_RE.search(html)
    if not m:
        raise SystemExit(f"extract_pandoc_body: could not find <body> in {src}")

    body = m.group("body").strip()

    # Strip any <style> blocks lingering inside body.
    body = re.sub(r"<style\b[^>]*>.*?</style>", "", body, flags=re.IGNORECASE | re.DOTALL).strip()

    # Remove Pandoc-generated title pages / frontmatter blocks.
    # Prefer an explicit anchor if present.
    m_exec = re.search(r"<h[12]\b[^>]*id=\"executive-summary\"[^>]*>", body, flags=re.IGNORECASE)
    if m_exec:
        body = body[m_exec.start():].lstrip()
    else:
        # Fallback: drop everything before the first major heading.
        m2 = re.search(r"<h[12]\b[^>]*>", body, flags=re.IGNORECASE)
        if m2:
            body = body[m2.start():].lstrip()

    # Extra cleanup: if a title-block header remains, remove it.
    body = re.sub(r"<header\b[^>]*id=\"title-block-header\"[^>]*>.*?</header>", "", body, flags=re.IGNORECASE | re.DOTALL).lstrip()

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(body + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
