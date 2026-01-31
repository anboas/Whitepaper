#!/usr/bin/env python3
"""Autopilot for PRs: iterate on the target paper until "polished".

Designed for GitHub Actions on pull_request.

What it does:
- Detects which paper the PR is about (papers/*/tex/paper.tex).
- Validates INTENT + deterministic rubric.
- If AUTOPILOT.yml says autonomous, runs an iterative loop:
  - cheap semantic rubric -> top_fixes
  - patch the LaTeX source (ONLY that file)
  - commit + push to the PR branch
  - stop when full semantic passes OR no actionable fixes OR max_iters

This enables the workflow you described:
open PR -> pipeline writes/commits -> pipeline merges -> PR closes.
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
import yaml


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, text=True, capture_output=True)
    return p.returncode, (p.stdout + "\n" + p.stderr)


def sh(*cmd: str) -> str:
    return subprocess.check_output(list(cmd), text=True).strip()


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


def call_llm_rubric(paper_dir: Path, tier: str) -> dict:
    code, out = run([
        "python",
        "scripts/llm_rubric_check.py",
        "--paper-dir",
        str(paper_dir),
        "--tex",
        "tex/paper.tex",
        "--rubric",
        "rubric.yml",
        "--tier",
        tier,
        "--json",
    ])
    if code not in (0, 2):
        raise RuntimeError(out)
    return json.loads(out.strip().splitlines()[-1])


def get_pr_body(owner: str, repo: str, pr: int, gh_token: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr}"
    r = gh_get(url, gh_token)
    if r.status_code >= 300:
        return ""
    return (r.json().get("body") or "").strip()


def extract_autopilot_requests(text: str) -> list[str]:
    """Extract user-requested changes from PR body.

    Supported forms:
    - Any fenced code block (``` ... ```) is treated as a requested change.
    - Any line starting with "FIX:" is treated as a requested change.
    """
    reqs: list[str] = []
    if not text:
        return reqs
    # fenced blocks
    for m in re.finditer(r"```\s*([\s\S]*?)\s*```", text):
        block = m.group(1).strip()
        if block:
            reqs.append(block)
    # FIX lines
    for line in text.splitlines():
        if line.strip().startswith("FIX:"):
            reqs.append(line.strip()[len("FIX:"):].strip())
    return reqs


def request_patch(api_key: str, model: str, target_path: str, intent_md: str, fixes: list[str], file_contents: str) -> str:
    instruction = {
        "task": "Polish the LaTeX whitepaper toward the INTENT definition of done.",
        "constraints": [
            "Return ONLY a unified diff patch.",
            f"The diff MUST modify ONLY {target_path}.",
            "Do not add new files.",
            "Keep LaTeX compiling (balanced braces, valid commands).",
        ],
        "intent_md": intent_md,
        "requested_fixes": fixes,
        "file_path": target_path,
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
    return out_text.strip()


def apply_patch(target_path: str, patch: str) -> None:
    if not patch.startswith("diff --git"):
        raise RuntimeError("Model did not return a git-style unified diff")

    touched = re.findall(r"^diff --git a/(.+?) b/(.+?)$", patch, flags=re.MULTILINE)
    files = set()
    for a, b in touched:
        files.add(a)
        files.add(b)
    files = {f for f in files if f != "dev/null"}
    if files != {target_path}:
        raise RuntimeError(f"Unsafe patch touches files: {sorted(files)}")

    proc = subprocess.run(["git", "apply", "--whitespace=fix"], input=patch, text=True)
    if proc.returncode != 0:
        raise RuntimeError("git apply failed")


def detect_target_paper(owner: str, repo: str, pr: int, gh_token: str) -> Path:
    files_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr}/files?per_page=100"
    rf = gh_get(files_url, gh_token)
    if rf.status_code >= 300:
        raise RuntimeError(f"Failed to fetch PR files: {rf.status_code} {rf.text[:500]}")
    pr_files = rf.json()

    paper_dirs = []
    for f in pr_files:
        fn = f.get("filename") or ""
        m = re.match(r"^(papers/[^/]+)/tex/paper\\.tex$", fn)
        if m:
            paper_dirs.append(m.group(1))

    paper_dirs = sorted(set(paper_dirs))
    if len(paper_dirs) != 1:
        raise RuntimeError(f"Autopilot requires exactly one paper to be touched; found: {paper_dirs}")

    return Path(paper_dirs[0])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--pr", required=True, type=int)
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    gh_token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not api_key:
        return die("Missing OPENAI_API_KEY")
    if not gh_token:
        return die("Missing GITHUB_TOKEN")

    owner, repo = args.repo.split("/", 1)
    paper_dir = detect_target_paper(owner, repo, args.pr, gh_token)

    pr_body = get_pr_body(owner, repo, args.pr, gh_token)
    requested = extract_autopilot_requests(pr_body)

    autopilot_path = paper_dir / "AUTOPILOT.yml"
    if not autopilot_path.exists():
        print(f"No AUTOPILOT.yml in {paper_dir}; skipping.")
        return 0

    cfg = yaml.safe_load(autopilot_path.read_text(encoding="utf-8", errors="ignore")) or {}
    if not (cfg.get("mode") or {}).get("autonomous", False):
        print("AUTOPILOT disabled; skipping.")
        return 0

    max_iters = int(((cfg.get("iteration") or {}).get("max_iters") or 6))
    models = cfg.get("models") or {}
    model_patch = pick_model(api_key, models.get("patch", "auto"))

    # Deterministic preflight
    for cmd in (
        ["python", "scripts/intent_validate.py", "--paper-dir", str(paper_dir)],
        ["python", "scripts/rubric_check.py", "--paper-dir", str(paper_dir), "--tex", "tex/paper.tex", "--rubric", "rubric.yml"],
    ):
        code, out = run(cmd)
        print(out)
        if code != 0:
            return die("Deterministic preflight failed")

    target_path = str(paper_dir / "tex/paper.tex")
    intent_md = (paper_dir / "INTENT.md").read_text(encoding="utf-8", errors="ignore") if (paper_dir / "INTENT.md").exists() else ""

    # Iterative loop
    for i in range(1, max_iters + 1):
        cheap = call_llm_rubric(paper_dir, "cheap")
        fixes = cheap.get("top_fixes") or []
        # Prepend explicit PR-requested changes so autopilot honors intent.
        if requested:
            fixes = [
                "PR REQUEST (must honor exactly; no rewrites, no removals unless explicitly asked):\n" + "\n\n".join(requested)
            ] + fixes
        print(f"[iter {i}] cheap_ok={cheap.get('ok')} overall={cheap.get('overall')} fixes={len(fixes)}")

        if not fixes:
            print("No actionable fixes; stopping.")
            break

        file_contents = Path(target_path).read_text(encoding="utf-8", errors="ignore")
        patch = request_patch(api_key, model_patch, target_path, intent_md, fixes, file_contents)
        apply_patch(target_path, patch)

        # Commit+push each iteration so the PR updates live.
        subprocess.run(["git", "add", target_path], check=False)
        subprocess.run(["git", "commit", "-m", f"Autopilot polish iteration {i}"], check=False)
        subprocess.run(["git", "push"], check=False)

        full = call_llm_rubric(paper_dir, "full")
        if full.get("ok"):
            print(f"Full rubric passes at iter {i}; stopping.")
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
