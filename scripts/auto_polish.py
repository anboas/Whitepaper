#!/usr/bin/env python3
"""Iteratively polish the whitepaper using INTENT + LLM feedback.

This is the programmatic loop you described:
- deterministic gates first (intent + rubric)
- then LLM feedback loop until:
  - LLM semantic rubric passes (tier=full), OR
  - no actionable fixes remain, OR
  - max iterations reached

Edits are restricted to tex/whitepaper.tex.

Usage:
  python scripts/auto_polish.py --max_iters 6

Environment:
  OPENAI_API_KEY required
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import requests

TARGET = Path("tex/whitepaper.tex")


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, text=True, capture_output=True)
    return p.returncode, (p.stdout + "\n" + p.stderr)


def die(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 2


def pick_model(api_key: str) -> str:
    try:
        mr = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
        if mr.status_code >= 300:
            return "gpt-5-codex"
        ids = [m.get("id", "") for m in (mr.json().get("data") or []) if isinstance(m, dict)]
        ids = [i for i in ids if i]
        cand = [i for i in ids if "codex" in i.lower()]
        if cand:
            cand.sort(key=lambda x: ("preview" in x.lower(), len(x)))
            return cand[0]
    except Exception:
        pass
    return "gpt-5-codex"


def call_rubric(api_key: str, tier: str) -> dict:
    # Run our own script to keep rubric config centralized.
    code, out = run(["python", "scripts/llm_rubric_check.py", "--tex", str(TARGET), "--rubric", "rubric.yml", "--tier", tier, "--json"])
    if code not in (0, 2):
        raise RuntimeError(out)
    try:
        return json.loads(out.strip().splitlines()[-1])
    except Exception:
        raise RuntimeError(f"Could not parse rubric JSON. Output:\n{out}")


def request_patch(api_key: str, model: str, intent: str, fixes: list[str], file_contents: str) -> str:
    instruction = {
        "task": "Polish the LaTeX whitepaper toward the INTENT definition of done.",
        "constraints": [
            "Return ONLY a unified diff patch.",
            f"The diff MUST modify ONLY {TARGET}.",
            "Do not add new files.",
            "Keep LaTeX compiling (balanced braces, valid commands).",
            "Prefer improving clarity, structure, specificity, evidence, and recommendations.",
        ],
        "intent_md": intent,
        "requested_fixes": fixes,
        "file_path": str(TARGET),
        "file_contents": file_contents,
    }

    payload = {
        "model": model,
        "input": [
            {"role": "system", "content": "You are a meticulous editor. Output only a unified diff."},
            {"role": "user", "content": json.dumps(instruction)},
        ],
    }

    rr = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=180,
    )
    if rr.status_code >= 300:
        raise RuntimeError(f"OpenAI error: {rr.status_code} {rr.text[:1000]}")

    data = rr.json()
    out_text = None
    for item in data.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    out_text = c.get("text")
                    break
    if not out_text:
        raise RuntimeError("No output_text from model")

    patch = out_text.strip()
    return patch


def apply_patch(patch: str) -> None:
    if not patch.startswith("diff --git"):
        raise RuntimeError("Model did not return a git-style unified diff")

    touched = re.findall(r"^diff --git a/(.+?) b/(.+?)$", patch, flags=re.MULTILINE)
    files = set()
    for a, b in touched:
        files.add(a)
        files.add(b)
    files = {f for f in files if f != "dev/null"}
    if files != {str(TARGET)}:
        raise RuntimeError(f"Unsafe patch touches files: {sorted(files)}")

    proc = subprocess.run(["git", "apply", "--whitespace=fix"], input=patch, text=True)
    if proc.returncode != 0:
        raise RuntimeError("git apply failed")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max_iters", type=int, default=6)
    ap.add_argument("--final_tier", default="full", choices=["cheap", "full"]) 
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return die("Missing OPENAI_API_KEY")

    if not TARGET.exists():
        return die(f"Missing {TARGET}")

    # deterministic preflight
    for cmd in (["python", "scripts/intent_validate.py", "--path", "INTENT.md"], ["python", "scripts/rubric_check.py", "--tex", str(TARGET), "--rubric", "rubric.yml"]):
        code, out = run(cmd)
        print(out)
        if code != 0:
            return die("Deterministic preflight failed")

    intent = Path("INTENT.md").read_text(encoding="utf-8", errors="ignore") if Path("INTENT.md").exists() else ""
    model = pick_model(api_key)

    for i in range(1, args.max_iters + 1):
        # First cheap pass to get actionable fixes.
        report = call_rubric(api_key, "cheap")
        fixes = report.get("top_fixes") or []
        overall = report.get("overall")
        print(f"\n[iter {i}] cheap overall={overall} fixes={len(fixes)}")

        if not fixes:
            print("No actionable fixes returned; stopping.")
            break

        contents = TARGET.read_text(encoding="utf-8", errors="ignore")
        patch = request_patch(api_key, model, intent, fixes, contents)
        apply_patch(patch)

        subprocess.run(["git", "add", str(TARGET)], check=False)
        # commit each iteration; caller can squash.
        subprocess.run(["git", "commit", "-m", f"Auto-polish iteration {i}"], check=False)

        # Stop early if final tier passes.
        final = call_rubric(api_key, args.final_tier)
        if final.get("ok"):
            print(f"Reached polished threshold at iter {i} (tier={args.final_tier}).")
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
