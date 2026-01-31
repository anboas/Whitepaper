#!/usr/bin/env python3
"""Apply requested fixes from PR comments.

Trigger model:
- PR must be labeled `apply-fixes`.
- User leaves one or more PR comments starting with `FIX:`.

Target selection (multi-paper aware):
- If exactly one file matching `papers/*/tex/paper.tex` is changed in the PR, that file is targeted.
- Else if a PR comment begins with `TARGET: <path>`, that path is targeted.
- Else fallback to legacy `tex/whitepaper.tex`.

Behavior:
- Runs an LLM to generate a unified diff patch LIMITED to the chosen target file.
- Applies patch, commits to the PR branch, and pushes.

Safety constraints:
- Only edits the chosen target file.
- Rejects patches touching other files.
- If patch fails to apply, exits non-zero.

Requires:
- OPENAI_API_KEY
- GITHUB_TOKEN (for GitHub API)
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


def gh_get(url: str, token: str) -> requests.Response:
    return requests.get(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        timeout=30,
    )


def pick_model(api_key: str, requested: str = "auto") -> str:
    req = (requested or "").strip().lower()
    if req not in ("auto", "codex", ""):
        return requested
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--pr", required=True, type=int)
    ap.add_argument("--model", default="auto")
    ap.add_argument("--fallback", default="tex/whitepaper.tex")
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    gh_token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not api_key:
        return die("Missing OPENAI_API_KEY")
    if not gh_token:
        return die("Missing GITHUB_TOKEN")

    owner, repo = args.repo.split("/", 1)

    # Fetch PR comments
    comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{args.pr}/comments"
    rc = gh_get(comments_url, gh_token)
    if rc.status_code >= 300:
        return die(f"Failed to fetch comments: {rc.status_code} {rc.text[:500]}")
    comments = rc.json()

    fix_blocks: list[str] = []
    target_override: str | None = None
    for c in comments:
        body = (c.get("body") or "").strip()
        if body.startswith("FIX:"):
            fix_blocks.append(body[len("FIX:"):].strip())
        if body.startswith("TARGET:"):
            target_override = body[len("TARGET:"):].strip()

    if not fix_blocks:
        print("No FIX: comments found; nothing to do.")
        return 0

    # Determine target file from PR changed files
    files_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{args.pr}/files?per_page=100"
    rf = gh_get(files_url, gh_token)
    if rf.status_code >= 300:
        return die(f"Failed to fetch PR files: {rf.status_code} {rf.text[:500]}")
    pr_files = rf.json()

    paper_tex_changes = []
    for f in pr_files:
        fn = f.get("filename") or ""
        if re.match(r"^papers/[^/]+/tex/paper\.tex$", fn):
            paper_tex_changes.append(fn)

    if target_override:
        target_path = target_override
    elif len(set(paper_tex_changes)) == 1:
        target_path = paper_tex_changes[0]
    else:
        target_path = args.fallback

    target = Path(target_path)
    if not target.exists():
        return die(f"Target file not found in checkout: {target}")

    original = target.read_text(encoding="utf-8", errors="ignore")

    model = pick_model(api_key, args.model)

    instruction = {
        "task": "Apply requested edits to the LaTeX whitepaper file.",
        "constraints": [
            "Return ONLY a unified diff patch.",
            f"The diff MUST modify ONLY {target_path}.",
            "Do not add new files.",
            "Keep LaTeX compiling (do not break braces/commands).",
        ],
        "requested_fixes": fix_blocks,
        "file_path": target_path,
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
        timeout=180,
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

    proc = subprocess.run(["git", "apply", "--whitespace=fix"], input=patch, text=True)
    if proc.returncode != 0:
        return die("git apply failed")

    git("add", str(target))
    if git("status", "--porcelain") == "":
        print("Patch applied but no changes detected")
        return 0

    git("commit", "-m", f"Apply PR FIX comments ({target_path})")
    git("push")

    print(f"Applied fixes and pushed to {target_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
