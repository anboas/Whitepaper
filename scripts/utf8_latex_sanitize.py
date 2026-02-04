#!/usr/bin/env python3
"""UTF-8 hygiene for LaTeX sources.

Goal: prevent pdfTeX / LaTeX unicode pitfalls by ensuring TeX inputs stay
ASCII-clean (or at least free of the common smart punctuation characters).

Usage:
  - Check (CI):  python3 scripts/utf8_latex_sanitize.py --check
  - Fix in-place: python3 scripts/utf8_latex_sanitize.py --fix

By default, scans LaTeX inputs in:
  tex/**/*.tex
  papers/**/tex/**/*.tex
  **/*.{tex,bib,cls,sty}
excluding build artifacts and .git.

This is intentionally conservative: it only rewrites *known* punctuation
characters that routinely break pdfTeX; it does not try to be a general
unicode-to-latex transpiler.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable

SKIP_DIRS = {".git", "node_modules", "build", "out", "dist"}

# Common troublemakers for pdfTeX.
REPLACEMENTS = {
    "\u2018": "`",   # left single quote
    "\u2019": "'",   # right single quote / apostrophe
    "\u201C": "``",  # left double quote
    "\u201D": "''",  # right double quote
    "\u2013": "--",  # en dash
    "\u2014": "---", # em dash
    "\u2026": "\\ldots{}",  # ellipsis
    "\u00A0": " ",  # NBSP
    "\u202F": " ",  # narrow NBSP
    "\u2007": " ",  # figure space
    "\u2009": " ",  # thin space
}

# Characters we consider unacceptable in LaTeX inputs for this repo.
FORBIDDEN_CHARS = set(REPLACEMENTS.keys())


def iter_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    exts = {".tex", ".bib", ".cls", ".sty"}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in exts:
            yield p


def sanitize_text(s: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    out = s
    for ch, repl in REPLACEMENTS.items():
        n = out.count(ch)
        if n:
            counts[ch] = n
            out = out.replace(ch, repl)
    return out, counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Fail if forbidden UTF-8 punctuation is present")
    ap.add_argument("--fix", action="store_true", help="Rewrite files in-place")
    args = ap.parse_args()

    if args.check == args.fix:
        ap.error("Specify exactly one of --check or --fix")

    root = pathlib.Path(".").resolve()

    dirty: list[tuple[pathlib.Path, dict[str, int]]] = []
    for p in iter_files(root):
        raw = p.read_text(encoding="utf-8")
        _, counts = sanitize_text(raw)
        if counts:
            dirty.append((p, counts))

    if args.check:
        if dirty:
            print("UTF-8 punctuation found in LaTeX inputs (use --fix):")
            for p, counts in dirty:
                details = ", ".join(f"{repr(k)}×{v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))
                print(f"- {p}: {details}")
            return 2
        return 0

    # --fix
    changed = 0
    for p, _counts in dirty:
        raw = p.read_text(encoding="utf-8")
        out, counts = sanitize_text(raw)
        if out != raw:
            p.write_text(out, encoding="utf-8")
            changed += 1
            details = ", ".join(f"{repr(k)}→{repr(REPLACEMENTS[k])}" for k in counts.keys())
            print(f"fixed: {p} ({details})")

    if changed == 0:
        print("No changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
