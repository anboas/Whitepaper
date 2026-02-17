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


def _guess_col_count(colspec: str, body: str) -> int:
    # Most generated longtable specs repeat p{...}; use that first.
    count = len(re.findall(r"p\{", colspec))
    if count > 0:
        return count

    # Fallback: infer from first row.
    m = re.search(r"^(.*?)\\\\", body, flags=re.DOTALL)
    if m:
        return max(1, m.group(1).count("&") + 1)
    return 2


def longtable_to_tabular(colspec: str, body: str) -> str:
    """Convert longtable to plain tabular for more reliable Pandoc HTML conversion.

    Pandoc's LaTeX reader can leak longtable internals (colspec/minipage/booktabs markers)
    into HTML text for complex generated longtables. We normalize to a simple tabular.
    """

    ncols = _guess_col_count(colspec, body)
    # Pandoc reliably converts simple alignment specs (l/c/r) to HTML tables.
    # Width-bearing p{...} specs in preprocessed LaTeX can leak as literal text.
    safe_colspec = "".join(["l" for _ in range(ncols)])

    cleaned = body

    # Strip wrappers used by pandoc-generated longtables.
    cleaned = re.sub(r"\\begin\{minipage\}\[b\]\{\\linewidth\}\\raggedright\s*", "", cleaned)
    cleaned = re.sub(r"\\end\{minipage\}", "", cleaned)

    # Remove longtable-only control rows/markers.
    cleaned = re.sub(r"\\(toprule|midrule|bottomrule)\\noalign\{\}\s*", "", cleaned)
    cleaned = re.sub(r"\\endhead\s*", "", cleaned)
    cleaned = re.sub(r"\\endlastfoot\s*", "", cleaned)

    # Normalize repeated whitespace-only lines.
    lines = [ln.rstrip() for ln in cleaned.splitlines()]
    lines = [ln for ln in lines if ln.strip()]
    cleaned = "\n".join(lines).strip() + "\n"

    return f"\\begin{{tabular}}{{{safe_colspec}}}\n{cleaned}\\end{{tabular}}\n"


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

    # Convert longtable -> tabular (for reliable HTML conversion).
    text2 = re.sub(
        r"\\begin\{longtable\}\[\]\{@\{\}(.*?)@\{\}\}(.*?)\\end\{longtable\}",
        lambda m: longtable_to_tabular(m.group(1), m.group(2)),
        text2,
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
