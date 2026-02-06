#!/usr/bin/env python3
r"""Preprocess LaTeX for pandoc HTML conversion.

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
# (no html escaping needed)
from pathlib import Path


def tabularx_to_markdown_table(tabular_block: str) -> str:
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

        # Emit a pandoc-readable pipe table (markdown). Pandoc will turn this into a real <table>.
    def esc(cell: str) -> str:
        return cell.replace("|", "\\|").strip()

    header_row = "| " + " | ".join(esc(c) for c in header_clean) + " |"
    sep_row = "| " + " | ".join(["---"] * len(header_clean)) + " |"
    body_md = ["| " + " | ".join(esc(c) for c in r) + " |" for r in body_rows]

    out = ["\n\n<!-- begin:generated-table -->\n", header_row + "\n", sep_row + "\n"]
    out.extend([row + "\n" for row in body_md])
    out.append("<!-- end:generated-table -->\n\n")
    return "".join(out)


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
        return tabularx_to_markdown_table(inner)

    # Capture the contents between begin/end tabularx, but keep the wrapper out.
    text2 = re.sub(
        r"\\begin\{tabularx\}\{\\textwidth\}\{[^}]*\}(.*?)\\end\{tabularx\}",
        lambda m: tabularx_to_markdown_table(m.group(1)),
        text,
        flags=re.DOTALL,
    )

    dst.write_text(text2, "utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
