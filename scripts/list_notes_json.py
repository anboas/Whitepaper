#!/usr/bin/env python3
"""Emit a GitHub Actions matrix JSON for published notes."""

from __future__ import annotations

import json
from pathlib import Path

from notes import list_note_files


def main() -> None:
    ids = [p.stem for p in list_note_files(Path("writing/notes"))]
    print(json.dumps({"note": ids}))


if __name__ == "__main__":
    main()
