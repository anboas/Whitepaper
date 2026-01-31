#!/usr/bin/env python3
"""Deterministic rubric gate for whitepaper readiness.

This is intentionally heuristic and deterministic (no LLM). It catches obvious non-ready
drafts and enforces basic publishability norms.

Inputs:
- A LaTeX file (default tex/whitepaper.tex)
- rubric.yml describing checks + weights

Output:
- Human-readable report
- Exit code 0 if score >= min_total_score else 2

Note: In multi-paper mode, a paper may provide its own rubric.yml.
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
    """Very rough LaTeX -> plain text."""
    text = re.sub(r"%.*", "", text)  # comments
    text = re.sub(r"\\(begin|end)\{[^}]+\}", " ", text)
    # remove common commands and their optional args/braces
    text = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", text)
    text = re.sub(r"\{[^{}]*\}", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9']+", text)


def count_syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    w = re.sub(r"e$", "", w)
    groups = re.findall(r"[aeiouy]+", w)
    return max(1, len(groups))


def flesch_reading_ease(text: str) -> float:
    sents = split_sentences(text)
    w = words(text)
    if not sents or not w:
        return 0.0
    syllables = sum(count_syllables(x) for x in w)
    wps = len(w) / max(1, len(sents))
    spw = syllables / max(1, len(w))
    return 206.835 - (1.015 * wps) - (84.6 * spw)


def passive_voice_ratio(text: str) -> float:
    sents = split_sentences(text)
    if not sents:
        return 0.0

    be = r"(?:am|is|are|was|were|be|been|being)"
    pp = r"(?:\w+ed|known|given|seen|done|built|made|shown|driven|taken|written|proven)"
    pat = re.compile(rf"\b{be}\b\s+(?:\w+\s+)?\b{pp}\b", re.IGNORECASE)

    passive_hits = 0
    for s in sents:
        if pat.search(s):
            passive_hits += 1
    return passive_hits / len(sents)


@dataclass
class CheckResult:
    name: str
    weight: float
    score: float
    details: str


def phrase_present(raw: str, phrase: str) -> bool:
    return re.search(re.escape(phrase), raw, re.IGNORECASE) is not None


def count_pattern_hits(raw: str, patterns: list[str]) -> int:
    hits = 0
    for p in patterns:
        hits += len(re.findall(re.escape(p), raw, re.IGNORECASE))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", default="tex/whitepaper.tex")
    ap.add_argument("--rubric", default="rubric.yml")
    ap.add_argument("--paper-dir", default=".", help="paper directory (for multi-paper layout)")
    args = ap.parse_args()

    base = Path(args.paper_dir)
    tex_path = base / args.tex

    # Prefer paper-local rubric.yml if present.
    rubric_path = base / args.rubric
    if not rubric_path.exists():
        rubric_path = Path(args.rubric)

    if not tex_path.exists():
        print(f"ERROR: missing tex file: {tex_path}", file=sys.stderr)
        return 2
    if not rubric_path.exists():
        print(f"ERROR: missing rubric file: {rubric_path}", file=sys.stderr)
        return 2

    raw = read_text(tex_path)
    plain = strip_latex(raw)

    cfg = yaml.safe_load(read_text(rubric_path)) or {}
    min_total = float(cfg.get("min_total_score", 0.80))
    checks = cfg.get("checks", {}) or {}

    results: list[CheckResult] = []

    # --- Hygiene / structure ---
    if "no_todos" in checks:
        c = checks["no_todos"]
        weight = float(c.get("weight", 0))
        patterns = list(c.get("patterns", []))
        hits = [pat for pat in patterns if re.search(re.escape(pat), raw, re.IGNORECASE)]
        results.append(
            CheckResult(
                "no_todos",
                weight,
                1.0 if not hits else 0.0,
                "No TODO/TBD/FIXME markers" if not hits else f"Found: {', '.join(hits)}",
            )
        )

    if "required_sections" in checks:
        c = checks["required_sections"]
        weight = float(c.get("weight", 0))
        req = list(c.get("required_phrases", []))
        missing = [p for p in req if not phrase_present(raw, p)]
        results.append(
            CheckResult(
                "required_sections",
                weight,
                1.0 if not missing else 0.0,
                "OK" if not missing else f"Missing: {', '.join(missing)}",
            )
        )

    if "has_sources_or_refs" in checks:
        c = checks["has_sources_or_refs"]
        weight = float(c.get("weight", 0))
        any_phrases = list(c.get("required_phrases_any", []))
        min_markers = int(c.get("min_citation_markers", 0))

        has_section = any(phrase_present(raw, p) for p in any_phrases)
        citation_markers = len(re.findall(r"\[[0-9]+\]", raw))
        ok = has_section or (citation_markers >= min_markers)
        results.append(
            CheckResult(
                "has_sources_or_refs",
                weight,
                1.0 if ok else 0.0,
                f"refs_section={'yes' if has_section else 'no'}, citation_markers={citation_markers}",
            )
        )

    if "length_sanity" in checks:
        c = checks["length_sanity"]
        weight = float(c.get("weight", 0))
        min_words = int(c.get("min_words", 0))
        wc = len(words(plain))
        ok = wc >= min_words
        results.append(CheckResult("length_sanity", weight, 1.0 if ok else 0.0, f"word_count={wc}, min={min_words}"))

    # --- Tone / style ---
    if "tone_avoid_hedging" in checks:
        c = checks["tone_avoid_hedging"]
        weight = float(c.get("weight", 0))
        pats = list(c.get("patterns", []))
        max_hits = int(c.get("max_hits", 0))
        hits = count_pattern_hits(raw, pats)
        ok = hits <= max_hits
        results.append(CheckResult("tone_avoid_hedging", weight, 1.0 if ok else 0.0, f"hedge_hits={hits}, max={max_hits}"))

    if "tone_avoid_hype" in checks:
        c = checks["tone_avoid_hype"]
        weight = float(c.get("weight", 0))
        max_exc = int(c.get("max_exclamations", 0))
        max_allcaps = int(c.get("max_allcaps_words", 0))
        exc = raw.count("!")
        allcaps = len(re.findall(r"\b[A-Z]{3,}\b", raw))
        ok = (exc <= max_exc) and (allcaps <= max_allcaps)
        results.append(
            CheckResult(
                "tone_avoid_hype",
                weight,
                1.0 if ok else 0.0,
                f"exclamations={exc}, max={max_exc}; allcaps_words={allcaps}, max={max_allcaps}",
            )
        )

    if "clarity_sentence_length" in checks:
        c = checks["clarity_sentence_length"]
        weight = float(c.get("weight", 0))
        max_avg = float(c.get("max_avg_words_per_sentence", 0))
        max_sent = int(c.get("max_sentence_words", 0))

        sents = split_sentences(plain)
        sent_lens = [len(words(s)) for s in sents] if sents else [0]
        avg = (sum(sent_lens) / len(sent_lens)) if sent_lens else 0.0
        mx = max(sent_lens) if sent_lens else 0
        ok = (avg <= max_avg) and (mx <= max_sent)
        results.append(
            CheckResult(
                "clarity_sentence_length",
                weight,
                1.0 if ok else 0.0,
                f"avg_words_per_sentence={avg:.1f}, max_sentence_words={mx}; limits avg<={max_avg}, max<={max_sent}",
            )
        )

    if "clarity_readability" in checks:
        c = checks["clarity_readability"]
        weight = float(c.get("weight", 0))
        min_fre = float(c.get("min_flesch_reading_ease", 0))
        fre = flesch_reading_ease(plain)
        ok = fre >= min_fre
        results.append(CheckResult("clarity_readability", weight, 1.0 if ok else 0.0, f"flesch_reading_ease={fre:.1f}, min={min_fre}"))

    if "voice_prefer_active" in checks:
        c = checks["voice_prefer_active"]
        weight = float(c.get("weight", 0))
        max_ratio = float(c.get("max_passive_ratio", 1.0))
        ratio = passive_voice_ratio(plain)
        ok = ratio <= max_ratio
        results.append(CheckResult("voice_prefer_active", weight, 1.0 if ok else 0.0, f"passive_sentence_ratio={ratio:.2f}, max={max_ratio:.2f}"))

    # --- Elements / audience fit ---
    if "elements_actionability" in checks:
        c = checks["elements_actionability"]
        weight = float(c.get("weight", 0))
        req_any = list(c.get("required_phrases_any", []))
        min_hits = int(c.get("min_hits", 0))
        hits = sum(1 for p in req_any if phrase_present(raw, p))
        ok = hits >= min_hits
        results.append(CheckResult("elements_actionability", weight, 1.0 if ok else 0.0, f"action_verbs_hit={hits}, min={min_hits}"))

    total = sum(r.weight * r.score for r in results)
    weight_sum = sum(r.weight for r in results) or 1.0
    total_norm = total / weight_sum

    print("Rubric results")
    print("=============")
    for r in results:
        status = "PASS" if r.score >= 1.0 else "FAIL"
        print(f"- {r.name:24} {status}  (weight={r.weight:.2f})  {r.details}")
    print("-------------")
    print(f"Total score: {total_norm:.3f} (min required: {min_total:.3f})")

    return 0 if total_norm >= min_total else 2


if __name__ == "__main__":
    raise SystemExit(main())
