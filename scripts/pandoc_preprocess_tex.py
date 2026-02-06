#!/usr/bin/env python3
"""Preprocess LaTeX for pandoc HTML conversion.

Pandoc's LaTeX reader doesn't reliably convert tabularx tables.
We rewrite simple tabularx environments into raw HTML tables so the
exhibition site can render them nicely.

Scope: best-effort for our house style tables (\begin{tabularx}{\textwidth}{...} ... \end{tabularx}).

Usage:
  pandoc_preprocess_tex.py in.tex out.tex
"""

from __future__ import annotations

import re
import sys
from html import escape
from pathlib import Path


def tabularx_to_html(tabular_block: str) -> str:
    # Extract rows like: cell & cell & cell\\
    rows = []
    for line in tabular_block.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("\\"):
            continue
        if line in {"\\hline"}:
            continue
        if "&" in line and line.endswith("\\\\"):
            line = line[:-2]
            cells = [c.strip() for c in line.split("&")]
            rows.append(cells)

    if not rows:
        return tabular_block

    # First row is header if it contains \textbf
    header = rows[0]
    def clean(cell: str) -> str:
        cell = re.sub(r"\\textbf\{([^}]*)\}", r"\\1", cell)
        cell = cell.replace("\\\\", "")
        cell = re.sub(r"\\emph\{([^}]*)\}", r"\\1", cell)
        cell = re.sub(r"\\textquotesingle\s*", "'", cell)
        return cell.strip()

    header_clean = [clean(c) for c in header]
    body_rows = [[clean(c) for c in r] for r in rows[1:]]

    html = ["\\n\\n<!-- begin:generated-table -->", "\\n<div class=\"table-wrap\">", "\\n<table>"]
    html.append("\\n<thead><tr>" + "".join(f"<th>{escape(c)}</th>" for c in header_clean) + "</tr></thead>")
    html.append("\\n<tbody>")
    for r in body_rows:
        html.append("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in r) + "</tr>")
    html.append("</tbody>\\n</table>\\n</div>\\n<!-- end:generated-table -->\\n")
    return "".join(html)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    text = src.read_text("utf-8", errors="ignore")

    # Replace tabularx blocks
    def repl(m: re.Match) -> str:
        block = m.group(0)
        inner = m.group(1)
        return tabularx_to_html(inner)

    # Capture the contents between begin/end tabularx, but keep the wrapper out.
    text2 = re.sub(
        r"\\begin\{tabularx\}\{\\textwidth\}\{[^}]*\}(.*?)\\end\{tabularx\}",
        lambda m: tabularx_to_html(m.group(1)),
        text,
        flags=re.DOTALL,
    )

    dst.write_text(text2, "utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
