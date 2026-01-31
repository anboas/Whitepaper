#!/usr/bin/env python3
"""Emit a GitHub Actions matrix JSON for available papers.

Usage:
  python scripts/list_papers_json.py > matrix.json

Output format:
  {"paper": ["id1","id2",...]}
"""

from __future__ import annotations

import json
from pathlib import Path

from papers import list_paper_dirs


def main() -> None:
    dirs = list_paper_dirs(Path("papers"))
    ids = [d.name for d in dirs]
    print(json.dumps({"paper": ids}))


if __name__ == "__main__":
    main()
