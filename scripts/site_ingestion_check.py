#!/usr/bin/env python3

"""Sanity checks that Whitepaper build outputs are safe/compatible for adamboas.info ingestion.

We intentionally keep this deterministic and dependency-free.

Checks:
- HTML output exists
- No <script> or <iframe>
- No inline event handlers (on*)
- Not empty

This is a belt-and-suspenders check; the site also sanitizes on sync.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


RE_SCRIPT = re.compile(r"<\s*script\b", re.IGNORECASE)
RE_IFRAME = re.compile(r"<\s*iframe\b", re.IGNORECASE)
RE_ONATTR = re.compile(r"\son\w+\s*=\s*['\"]", re.IGNORECASE)


def die(msg: str) -> None:
    raise SystemExit(f"site_ingestion_check: {msg}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-dir", required=True, help="e.g. papers/agentic-force-creation")
    ap.add_argument(
        "--html",
        default=None,
        help="Override expected HTML path (default: build/<paper>/paper.html)",
    )
    args = ap.parse_args()

    paper_dir = Path(args.paper_dir)
    paper_slug = paper_dir.name

    html_path = Path(args.html) if args.html else Path("build") / paper_slug / "paper.html"
    if not html_path.exists():
        die(f"missing HTML output at {html_path}")

    html = html_path.read_text(encoding="utf-8", errors="strict")

    if RE_SCRIPT.search(html):
        die(f"{paper_slug}: HTML contains <script>")
    if RE_IFRAME.search(html):
        die(f"{paper_slug}: HTML contains <iframe>")
    if RE_ONATTR.search(html):
        die(f"{paper_slug}: HTML contains inline event handler attributes (on*)")

    text_len = len(re.sub(r"<[^>]*>", "", html).strip())
    if text_len < 200:
        die(f"{paper_slug}: HTML looks too small ({text_len} chars of text)")

    print(f"site_ingestion_check: OK ({paper_slug})")


if __name__ == "__main__":
    main()
