#!/usr/bin/env python3
r"""Preprocess LaTeX for pandoc HTML conversion.

Pandoc's LaTeX reader doesn't reliably convert tabularx tables.
We rewrite tabularx environments into plain tabular so Pandoc can convert them.

Scope: best-effort for our house style tables (tabularx -> tabular)
and yamlblock code environments.

Usage:
  pandoc_preprocess_tex.py in.tex out.tex
"""

from __future__ import annotations

import re
import sys
# (no html escaping needed)
from pathlib import Path


def tabularx_to_tabular(inner: str, colspec: str) -> str:
    """Convert tabularx to plain tabular (Pandoc handles tabular better)."""

    # Replace X with a reasonable paragraph width. We keep the first p{...} as-is.
    safe_colspec = " ".join(colspec.strip().split()).replace('X', 'p{0.37\\textwidth}')

    # Preserve content; tabularx body already contains row breaks (\\) and may include \hline.
    inner = inner.strip() + "\n"
    return f"\\begin{{tabular}}{{{safe_colspec}}}\n{inner}\\end{{tabular}}\n"


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    text = src.read_text("utf-8", errors="ignore")

    # Capture tabularx colspec + inner and convert to tabular.
    # tabularx colspec contains nested braces (p{...}), so a generic regex is painful.
    # We match our known house style and convert it.
    text2 = re.sub(
        r"\\begin\{tabularx\}\{\\textwidth\}\{p\{0\.26\\textwidth\}X X\}(.*?)\\end\{tabularx\}",
        lambda m: tabularx_to_tabular(m.group(1), r"p{0.26\\textwidth} X X"),
        text,
        flags=re.DOTALL,
    )

    # Convert yamlblock -> verbatim (pandoc LaTeX reader reliably turns this into a code block).
    def yamlblock_to_verbatim(m: re.Match) -> str:
        inner = m.group(1)
        return "\n\\begin{verbatim}\n" + inner.strip() + "\n\\end{verbatim}\n"

    text2 = re.sub(
        r"\\begin\{yamlblock\}(.*?)\\end\{yamlblock\}",
        yamlblock_to_verbatim,
        text2,
        flags=re.DOTALL,
    )

    dst.write_text(text2 + "\n", "utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
