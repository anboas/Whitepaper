#!/usr/bin/env python3
"""Render Graphviz DOT diagrams to PNG + SVG.

Usage:
  python3 scripts/render_graphviz_diagrams.py --paper-dir papers/acp-ra

Conventions:
- Input directory: <paper-dir>/diagrams-src/*.dot
- Output directory: <paper-dir>/diagrams/
- Output names: same basename with .png and .svg

This is deterministic and intended for CI.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-dir", required=True)
    args = ap.parse_args()

    paper_dir = Path(args.paper_dir)
    src_dir = paper_dir / "diagrams-src"
    out_dir = paper_dir / "diagrams"

    if not src_dir.exists():
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)

    dot_files = sorted(src_dir.glob("*.dot"))
    if not dot_files:
        return 0

    for dot in dot_files:
        base = dot.stem
        png = out_dir / f"{base}.png"
        svg = out_dir / f"{base}.svg"

        # PNG for LaTeX, SVG for the site.
        run(["dot", "-Tpng", str(dot), "-o", str(png)])
        run(["dot", "-Tsvg", str(dot), "-o", str(svg)])

    print(f"Rendered {len(dot_files)} diagram(s) to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
