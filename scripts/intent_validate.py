#!/usr/bin/env python3
"""Validate INTENT.md exists and contains key fields.

This is a deterministic guardrail. It prevents running expensive automation
against an undefined paper.

Exit codes:
- 0 pass
- 2 fail
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="INTENT.md")
    args = ap.parse_args()

    p = Path(args.path)
    if not p.exists():
        print(f"ERROR: missing {p}. Create it to define the paper.", file=sys.stderr)
        return 2

    txt = p.read_text(encoding="utf-8", errors="ignore")

    # Required headings
    required_headings = [
        r"^##\s+0\)\s+Identity\s*$",
        r"^##\s+1\)\s+Intent\s*\(what this paper does\)\s*$",
        r"^##\s+2\)\s+Definition of done",
        r"^##\s+3\)\s+Required sections\s*$",
        r"^##\s+5\)\s+Notes / source material\s*$",
    ]
    missing = []
    for pat in required_headings:
        if not re.search(pat, txt, flags=re.MULTILINE):
            missing.append(pat)

    # Required identity fields
    required_fields = ["Title:", "Author name:", "Date:"]
    missing_fields = [f for f in required_fields if f not in txt]

    if missing or missing_fields:
        print("INTENT validation: FAIL")
        if missing_fields:
            print("Missing fields:")
            for f in missing_fields:
                print(f"- {f}")
        if missing:
            print("Missing required headings (regex):")
            for m in missing:
                print(f"- {m}")
        return 2

    print("INTENT validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
