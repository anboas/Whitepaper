#!/usr/bin/env python3
"""Validate INTENT.md exists and contains key fields.

Deterministic guardrail.

Exit codes:
- 0 pass
- 2 fail
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def validate_intent(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"ERROR: missing {path}. Create it to define the paper."

    txt = path.read_text(encoding="utf-8", errors="ignore")

    required_headings = [
        r"^##\s+0\)\s+Identity\s*$",
        r"^##\s+1\)\s+Intent\s*\(what this paper does\)\s*$",
        r"^##\s+2\)\s+Definition of done",
        r"^##\s+3\)\s+Required sections\s*$",
        r"^##\s+5\)\s+Notes / source material\s*$",
    ]
    missing = [pat for pat in required_headings if not re.search(pat, txt, flags=re.MULTILINE)]

    required_fields = ["Title:", "Author name:", "Date:"]
    missing_fields = [f for f in required_fields if f not in txt]

    if missing or missing_fields:
        lines = ["INTENT validation: FAIL"]
        if missing_fields:
            lines.append("Missing fields:")
            lines += [f"- {f}" for f in missing_fields]
        if missing:
            lines.append("Missing required headings (regex):")
            lines += [f"- {m}" for m in missing]
        return False, "\n".join(lines)

    return True, "INTENT validation: PASS"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="INTENT.md")
    ap.add_argument("--paper-dir", default=".", help="paper directory (for multi-paper layout)")
    args = ap.parse_args()

    paper_dir = Path(args.paper_dir)
    intent_path = paper_dir / args.path

    ok, msg = validate_intent(intent_path)
    if ok:
        print(msg)
        return 0
    print(msg, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
