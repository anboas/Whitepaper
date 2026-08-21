#!/usr/bin/env python3
"""Deterministic format checks for paper front-matter + structure.

Goal: ensure every paper follows the same house construction, with no one-off
formatting hacks.

We check two sources of truth:
- papers/<paper>/draft.md (optional): when present, must have a single YAML
  front matter block at top.
- papers/<paper>/tex/paper.tex: must include the shared preamble and call the
  standard cover generator + ToC + execsummary wrapper.

Exit codes:
- 0 pass
- 2 fail
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


_RE_YAML_BLOCK = re.compile(r"\A\s*---\s*\n([\s\S]*?)\n---\s*\n", re.MULTILINE)


def fail(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 2


def _count_front_matter_like_blocks(text: str) -> int:
    """Count YAML blocks anywhere that look like front matter (contain title:)."""
    lines = text.splitlines()
    n = 0
    i = 0
    while i < len(lines):
        if lines[i].strip() == "---":
            j = i + 1
            while j < len(lines) and lines[j].strip() != "---":
                j += 1
            if j < len(lines):
                block = "\n".join(lines[i + 1 : j])
                if re.search(r"^title\s*:", block, flags=re.MULTILINE):
                    n += 1
                i = j
        i += 1
    return n


def check_draft_md(paper_dir: Path) -> tuple[bool, str]:
    p = paper_dir / "draft.md"
    if not p.exists():
        # Not all papers use markdown drafts; that's OK.
        return True, "draft.md: SKIP (not present)"

    txt = p.read_text("utf-8", errors="ignore")

    # Must start with a YAML block.
    m = _RE_YAML_BLOCK.search(txt)
    if not m:
        return False, (
            "FORMAT validation: FAIL\n"
            "draft.md must start with a YAML front matter block delimited by ---\n"
        )

    # Must not contain multiple front-matter-like blocks.
    nblocks = _count_front_matter_like_blocks(txt)
    if nblocks != 1:
        return False, (
            "FORMAT validation: FAIL\n"
            f"draft.md contains {nblocks} front-matter-like blocks; expected exactly 1.\n"
            "This usually indicates duplicate YAML blocks were accidentally pasted into the body."
        )

    # Forbid ingest artifacts.
    if "Imported from Telegram" in txt or "Imported from Telegram draft" in txt:
        return False, (
            "FORMAT validation: FAIL\n"
            "draft.md contains ingest artifact text ('Imported from Telegram ...'). Remove it."
        )

    return True, "draft.md: PASS"


def check_paper_tex(paper_dir: Path) -> tuple[bool, str]:
    p = paper_dir / "tex" / "paper.tex"
    if not p.exists():
        return False, f"FORMAT validation: FAIL\nMissing {p}"

    txt = p.read_text("utf-8", errors="ignore")

    # Shared preamble must be included from repo root.
    if "\\input{tex/paper_preamble.tex}" not in txt:
        return False, "FORMAT validation: FAIL\nMissing \\input{tex/paper_preamble.tex} in tex/paper.tex"

    # Required macros for metadata.
    required_macros = [
        r"\\newcommand\{\\PaperTitle\}",
        r"\\newcommand\{\\PaperSubtitle\}",
        r"\\newcommand\{\\AuthorName\}",
        r"\\newcommand\{\\AuthorRole\}",
        r"\\newcommand\{\\PaperDate\}",
    ]
    for pat in required_macros:
        if not re.search(pat, txt):
            return False, f"FORMAT validation: FAIL\nMissing required metadata macro: {pat}"

    # Cover-page rule and ToC/execsummary wrapper should be present.
    must_contain = [
        r"\\makepapercover",
        r"\\tableofcontents",
        r"\\begin\{execsummary\}",
        r"\\end\{execsummary\}",
    ]
    for pat in must_contain:
        if not re.search(pat, txt):
            return False, f"FORMAT validation: FAIL\nMissing expected front-matter structure token: {pat}"

    forbidden_cover_tokens = [
        r"\\thispagestyle\{empty\}",
        r"ADAMBOAS\.COM\s+\\textbullet\{\}\s+PAPER",
        r"\\Huge\\bfseries\\color\{BrandAccent\}\\PaperTitle",
    ]
    for pat in forbidden_cover_tokens:
        if re.search(pat, txt):
            return False, (
                "FORMAT validation: FAIL\n"
                "Paper source must not hand-write the cover page. Use the shared \\makepapercover macro."
            )

    # Prevent one-off stray sections before the main body section.
    # After \end{execsummary}, the next real sectioning command should be a numbered \section{...}
    # (pandoc converts the first '# ' heading to \section).
    after = txt.split("\\end{execsummary}", 1)
    if len(after) == 2:
        tail = after[1]
        m = re.search(r"\\(section\*?|subsection\*?|subsubsection\*?)\{", tail)
        if m and m.group(1) != "section":
            return False, (
                "FORMAT validation: FAIL\n"
                "Unexpected sectioning immediately after execsummary. Expected the body to begin with a numbered \\section{...}.\n"
                f"Found: \\{m.group(1)}{{...}}"
            )

    return True, "tex/paper.tex: PASS"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-dir", required=True)
    args = ap.parse_args()

    paper_dir = Path(args.paper_dir)
    ok1, msg1 = check_draft_md(paper_dir)
    if not ok1:
        return fail(msg1)

    ok2, msg2 = check_paper_tex(paper_dir)
    if not ok2:
        return fail(msg2)

    print("FORMAT validation: PASS")
    print(f"- {msg1}")
    print(f"- {msg2}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
