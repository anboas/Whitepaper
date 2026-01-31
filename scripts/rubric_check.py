#!/usr/bin/env python3
"""Deterministic rubric gate for whitepaper readiness.

Inputs:
- A LaTeX file (default tex/whitepaper.tex)
- rubric.yml describing checks + weights

Output:
- Human-readable report
- Exit code 0 if score >= min_total_score else 2

This is intentionally dumb-but-reliable: it catches obvious non-ready drafts.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_latex(text: str) -> str:
    # Very rough: remove common commands + braces; keep words for counting.
    text = re.sub(r"%.*", "", text)  # comments
    text = re.sub(r"\\(begin|end)\{[^}]+\}", " ", text)
    text = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", text)
    text = re.sub(r"\{[^{}]*\}", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


@dataclass
class CheckResult:
    name: str
    weight: float
    score: float
    details: str


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", default="tex/whitepaper.tex")
    ap.add_argument("--rubric", default="rubric.yml")
    args = ap.parse_args()

    tex_path = Path(args.tex)
    rubric_path = Path(args.rubric)

    if not tex_path.exists():
        print(f"ERROR: missing tex file: {tex_path}", file=sys.stderr)
        return 2
    if not rubric_path.exists():
        print(f"ERROR: missing rubric file: {rubric_path}", file=sys.stderr)
        return 2

    raw = read_text(tex_path)
    plain = strip_latex(raw)

    cfg = yaml.safe_load(read_text(rubric_path))
    min_total = float(cfg.get("min_total_score", 0.75))
    checks = cfg.get("checks", {})

    results: list[CheckResult] = []

    # no_todos
    if "no_todos" in checks:
        c = checks["no_todos"]
        weight = float(c.get("weight", 0))
        patterns = c.get("patterns", [])
        hits = []
        for pat in patterns:
            if re.search(re.escape(pat), raw, re.IGNORECASE):
                hits.append(pat)
        if hits:
            results.append(CheckResult("no_todos", weight, 0.0, f"Found: {', '.join(hits)}"))
        else:
            results.append(CheckResult("no_todos", weight, 1.0, "No TODO/TBD/FIXME markers"))

    def phrase_present(phrase: str) -> bool:
        return re.search(re.escape(phrase), raw, re.IGNORECASE) is not None

    for key in ("has_executive_summary", "has_recommendations"):
        if key in checks:
            c = checks[key]
            weight = float(c.get("weight", 0))
            req = c.get("required_phrases", [])
            missing = [p for p in req if not phrase_present(p)]
            if missing:
                results.append(CheckResult(key, weight, 0.0, f"Missing: {', '.join(missing)}"))
            else:
                results.append(CheckResult(key, weight, 1.0, "OK"))

    if "has_sources_or_refs" in checks:
        c = checks["has_sources_or_refs"]
        weight = float(c.get("weight", 0))
        any_phrases = c.get("required_phrases_any", [])
        min_markers = int(c.get("min_citation_markers", 0))

        has_section = any(phrase_present(p) for p in any_phrases)
        citation_markers = len(re.findall(r"\[[0-9]+\]", raw))
        ok = has_section or (citation_markers >= min_markers)

        details = []
        details.append(f"refs_section={'yes' if has_section else 'no'}")
        details.append(f"citation_markers={citation_markers}")
        results.append(CheckResult("has_sources_or_refs", weight, 1.0 if ok else 0.0, ", ".join(details)))

    if "length_sanity" in checks:
        c = checks["length_sanity"]
        weight = float(c.get("weight", 0))
        min_words = int(c.get("min_words", 0))
        words = [w for w in re.split(r"\s+", plain) if w]
        wc = len(words)
        ok = wc >= min_words
        results.append(CheckResult("length_sanity", weight, 1.0 if ok else 0.0, f"word_count={wc}, min={min_words}"))

    total = 0.0
    for r in results:
        total += r.weight * r.score

    # normalize if weights don't sum to 1
    weight_sum = sum(r.weight for r in results) or 1.0
    total_norm = total / weight_sum

    print("Rubric results")
    print("=============")
    for r in results:
        status = "PASS" if r.score >= 1.0 else "FAIL"
        print(f"- {r.name:22} {status}  (weight={r.weight:.2f})  {r.details}")
    print("-------------")
    print(f"Total score: {total_norm:.3f} (min required: {min_total:.3f})")

    return 0 if total_norm >= min_total else 2


if __name__ == "__main__":
    raise SystemExit(main())
