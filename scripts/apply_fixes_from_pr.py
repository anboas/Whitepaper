#!/usr/bin/env python3
"""Apply requested fixes from PR comments.

Trigger model:
- PR must be labeled `apply-fixes`.
- User leaves one or more PR comments starting with `FIX:`.

Behavior:
- Runs an LLM to generate a unified diff patch LIMITED to tex/whitepaper.tex.
- Applies patch, commits to the PR branch, and pushes.

Safety constraints:
- Only edits tex/whitepaper.tex
- Rejects patches touching other files
- If patch fails to apply, exits non-zero so workflow can comment back

Requires:
- OPENAI_API_KEY
- GITHUB_TOKEN (for fetching comments)
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


def sh(*cmd: str) -> str:
    return subprocess.check_output(list(cmd), text=True).strip()


def git(*cmd: str) -> str:
    return sh("git", *cmd)


def die(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 2


def strip_latex(text: str) -> str:
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"\\(begin|end)\{[^}]+\}", " ", text)
    text = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", text)
    text = re.sub(r"\{[^{}]*\}", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--pr", required=True, type=int)
    ap.add_argument("--file", default="tex/whitepaper.tex")
    ap.add_argument("--model", default="auto")
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    gh_token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not api_key:
        return die("Missing OPENAI_API_KEY")
    if not gh_token:
        return die("Missing GITHUB_TOKEN")

    owner, repo = args.repo.split("/", 1)

    # Fetch PR comments
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{args.pr}/comments"
    r = requests.get(url, headers={"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"}, timeout=30)
    if r.status_code >= 300:
        return die(f"Failed to fetch comments: {r.status_code} {r.text[:500]}")
    comments = r.json()

    fix_blocks: list[str] = []
    for c in comments:
        body = (c.get("body") or "").strip()
        if body.startswith("FIX:"):
            fix_blocks.append(body[len("FIX:"):].strip())

    if not fix_blocks:
        print("No FIX: comments found; nothing to do.")
        return 0

    target = Path(args.file)
    if not target.exists():
        return die(f"Target file not found: {target}")

    original = target.read_text(encoding="utf-8", errors="ignore")

    def pick_model() -> str:
        req = (args.model or "").strip().lower()
        if req not in ("auto", "codex", ""):
            return args.model
        try:
            mr = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
            if mr.status_code >= 300:
                return "gpt-5-codex"
            ids = [m.get("id", "") for m in (mr.json().get("data") or []) if isinstance(m, dict)]
            ids = [i for i in ids if i]
            # prefer codex
            cand = [i for i in ids if "codex" in i.lower()]
            if cand:
                cand.sort(key=lambda x: ("preview" in x.lower(), len(x)))
                return cand[0]
        except Exception:
            pass
        return "gpt-5-codex"

    model = pick_model()

    instruction = {
        "task": "Apply requested edits to the LaTeX whitepaper file.",
        "constraints": [
            "Return ONLY a unified diff patch.",
            "The diff MUST modify ONLY tex/whitepaper.tex.",
            "Do not add new files.",
            "Keep LaTeX compiling (do not break braces/commands).",
        ],
        "requested_fixes": fix_blocks,
        "file_path": str(target),
        "file_contents": original,
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
        timeout=120,
    )
    if rr.status_code >= 300:
        return die(f"OpenAI error: {rr.status_code} {rr.text[:1000]}")

    data = rr.json()
    out_text = None
    for item in data.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    out_text = c.get("text")
                    break
    if not out_text:
        return die("No output_text from model")

    patch = out_text.strip()
    if not patch.startswith("diff --git"):
        return die("Model did not return a git-style unified diff")

    # Ensure patch only touches target file
    touched = re.findall(r"^diff --git a/(.+?) b/(.+?)$", patch, flags=re.MULTILINE)
    files = set()
    for a, b in touched:
        files.add(a)
        files.add(b)
    files = {f for f in files if f != "dev/null"}
    if files != {str(target)}:
        return die(f"Unsafe patch touches files: {sorted(files)}")

    # Apply
    proc = subprocess.run(["git", "apply", "--whitespace=fix"], input=patch, text=True)
    if proc.returncode != 0:
        return die("git apply failed")

    # Commit
    git("add", str(target))
    if git("status", "--porcelain") == "":
        print("Patch applied but no changes detected")
        return 0

    git("commit", "-m", "Apply PR FIX comments")
    git("push")

    print("Applied fixes and pushed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
