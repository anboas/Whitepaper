#!/usr/bin/env python3
"""LLM-based rubric check (semantic/subjective).

- Uses OpenAI API via OPENAI_API_KEY.
- Designed to be safe-by-default in CI:
  - If OPENAI_API_KEY is missing, exits 0 and prints SKIP.
  - Deterministic checks remain enforced by scripts/rubric_check.py.

Config lives in rubric.yml under checks.llm_semantic.

Exit codes:
- 0 pass / skipped
- 2 fail
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml
import requests


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_latex(text: str) -> str:
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"\\(begin|end)\{[^}]+\}", " ", text)
    text = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", text)
    text = re.sub(r"\{[^{}]*\}", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", default="tex/whitepaper.tex")
    ap.add_argument("--rubric", default="rubric.yml")
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("LLM rubric: SKIP (OPENAI_API_KEY not set)")
        return 0

    tex_path = Path(args.tex)
    rubric_path = Path(args.rubric)
    if not tex_path.exists() or not rubric_path.exists():
        print("LLM rubric: ERROR missing tex or rubric.yml", file=sys.stderr)
        return 2

    cfg = yaml.safe_load(read_text(rubric_path)) or {}
    checks = (cfg.get("checks") or {})
    llm_cfg = checks.get("llm_semantic")
    if not llm_cfg:
        print("LLM rubric: SKIP (checks.llm_semantic not configured)")
        return 0

    requested_model = llm_cfg.get("model", "gpt-4o-mini")
    min_overall = float(llm_cfg.get("min_overall", 0.75))
    categories = llm_cfg.get(
        "categories",
        [
            "tone",
            "clarity",
            "structure",
            "argument_strength",
            "specificity",
            "actionability",
            "evidence_quality",
            "executive_readiness",
        ],
    )

    raw = read_text(tex_path)
    plain = strip_latex(raw)

    system = (
        "You are an exacting writing QA reviewer for executive-grade whitepapers. "
        "Score the document against the requested categories. Be critical, not polite. "
        "Return ONLY valid JSON matching the schema."
    )

    schema = {
        "type": "object",
        "properties": {
            "overall": {"type": "number"},
            "categories": {
                "type": "object",
                "additionalProperties": {"type": "number"},
            },
            "reasons": {
                "type": "object",
                "additionalProperties": {"type": "string"},
            },
            "top_issues": {"type": "array", "items": {"type": "string"}},
            "top_fixes": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["overall", "categories", "top_issues", "top_fixes"],
    }

    user = {
        "categories": categories,
        "scoring": "All scores are 0.0 to 1.0. Overall should be your holistic judgment.",
        "document": plain[:24000],
        "instructions": [
            "Be consistent: 0.8 means publish-ready with minor edits; 0.6 means needs meaningful revision; <0.5 means not ready.",
            "Call out missing reader hooks, vague claims, weak evidence, and unclear recommendations.",
            "Prefer actionable, specific writing. Penalize filler and vague abstractions.",
        ],
        "json_schema": schema,
    }

    def pick_model() -> str:
        # Allow CI to auto-select a Codex-ish model without hardcoding an ID.
        # We never print the full model list.
        req = (requested_model or "").strip().lower()
        if req not in ("auto", "codex", "", None):
            return requested_model

        try:
            mr = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=30,
            )
            if mr.status_code >= 300:
                return "gpt-4o-mini"
            data = mr.json()
            ids = [m.get("id", "") for m in (data.get("data") or []) if isinstance(m, dict)]
            ids = [i for i in ids if i]

            # Prefer anything that looks like codex; then gpt-5/4o; then fallback.
            prefer = [
                lambda s: "codex" in s,
                lambda s: "gpt-5" in s,
                lambda s: "gpt-4o" in s,
                lambda s: "gpt-4.1" in s,
                lambda s: "gpt-4" in s,
            ]
            for rule in prefer:
                cand = [i for i in ids if rule(i.lower())]
                if cand:
                    # pick shortest id (often canonical) to avoid preview variants unless that's all we have
                    cand.sort(key=lambda x: ("preview" in x.lower(), len(x)))
                    return cand[0]
        except Exception:
            pass

        return "gpt-4o-mini"

    model = pick_model()

    # OpenAI Responses API
    payload = {
        "model": model,
        "input": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user)},
        ],
        "text": {"format": {"type": "json_schema", "name": "llm_rubric", "schema": schema}},
        # Try to reduce creative drift.
        "temperature": 0.2,
    }

    r = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=90,
    )

    if r.status_code >= 300:
        print("LLM rubric: ERROR calling OpenAI")
        print(r.status_code, r.text[:2000])
        return 2

    data = r.json()
    # Responses API returns output_text convenience in some SDKs; here parse.
    out_text = None
    for item in data.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    out_text = c.get("text")
                    break
    if not out_text:
        print("LLM rubric: ERROR no output_text in response")
        print(json.dumps(data)[:2000])
        return 2

    try:
        result = json.loads(out_text)
    except Exception as e:
        print("LLM rubric: ERROR invalid JSON from model", e)
        print(out_text[:2000])
        return 2

    overall = float(result.get("overall", 0.0))
    cat_scores = result.get("categories", {}) or {}

    missing = [c for c in categories if c not in cat_scores]
    if missing:
        print(f"LLM rubric: FAIL missing categories: {', '.join(missing)}")
        return 2

    # Enforce minimums
    per_cat_min = llm_cfg.get("min_per_category")
    if per_cat_min is None:
        per_cat_min = 0.60
    per_cat_min = float(per_cat_min)

    failing = [c for c in categories if float(cat_scores.get(c, 0.0)) < per_cat_min]
    ok = (overall >= min_overall) and not failing

    print("LLM rubric results")
    print("=================")
    print(f"Model: {model}")
    print(f"Overall: {overall:.2f} (min {min_overall:.2f})")
    for c in categories:
        print(f"- {c:18} {float(cat_scores[c]):.2f} (min {per_cat_min:.2f})")
    if failing:
        print(f"Failing categories: {', '.join(failing)}")
    print("Top issues:")
    for s in (result.get("top_issues") or [])[:8]:
        print(f"- {s}")
    print("Top fixes:")
    for s in (result.get("top_fixes") or [])[:8]:
        print(f"- {s}")

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
