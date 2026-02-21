#!/usr/bin/env python3
"""Emit a GitHub Actions matrix JSON for available memos.

Usage:
  python scripts/list_memos_json.py > matrix.json

Output format:
  {"memo": ["id1","id2",...]}
"""

from __future__ import annotations

import json
from pathlib import Path

from memos import list_memo_dirs


def main() -> None:
    dirs = list_memo_dirs(Path("memos"))
    ids = [d.name for d in dirs]
    print(json.dumps({"memo": ids}))


if __name__ == "__main__":
    main()
