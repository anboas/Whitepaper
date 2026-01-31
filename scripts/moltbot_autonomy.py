#!/usr/bin/env python3
"""Moltbot Autonomy Loop (local operator, not GitHub Actions).

Principles
- CI (GitHub Actions) remains deterministic: validate intent, build PDFs, publish artifacts.
- Moltbot handles autonomy: interpreting PR body requests, generating/updating papers, pushing commits.

This script is designed to be run periodically (cron) on the operator machine.

Current behavior (v1)
- Scans open PRs.
- For PRs touching exactly one paper (papers/<id>/...), it will:
  - Read PR body for fenced code blocks / FIX: lines as explicit requests.
  - If the PR includes a requirements file describing insertions, it may apply deterministic edits.
  - If a new paper has INTENT.md but no tex/paper.tex, it will generate an initial draft via OpenAI.

Safety
- Only modifies files under papers/<paper-id>/tex/paper.tex (and creates it if missing).
- Will not delete or rewrite unrelated files.

Env
- Requires `gh` authenticated locally.
- Requires OPENAI_API_KEY for generation.

Usage
  python scripts/moltbot_autonomy.py --repo anboas/Whitepaper
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
import yaml


def sh(*cmd: str) -> str:
    return subprocess.check_output(list(cmd), text=True).strip()


def run(cmd: list[str], check: bool = False) -> tuple[int, str]:
    p = subprocess.run(cmd, text=True, capture_output=True)
    out = (p.stdout or "") + ("\n" if p.stderr else "") + (p.stderr or "")
    if check and p.returncode != 0:
        raise RuntimeError(out)
    return p.returncode, out


def now_ms() -> int:
    return int(time.time() * 1000)


def openai_model(api_key: str) -> str:
    # Prefer a codex model if available; fall back.
    try:
        r = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
        if r.status_code < 300:
            ids = [m.get("id", "") for m in (r.json().get("data") or []) if isinstance(m, dict)]
            cand = [i for i in ids if i and "codex" in i.lower()]
            if cand:
                cand.sort(key=lambda x: ("preview" in x.lower(), len(x)))
                return cand[0]
    except Exception:
        pass
    return "gpt-5-codex"


def openai_generate_latex(api_key: str, model: str, intent_md: str, requirements_md: str) -> str:
    prompt = {
        "task": "Write a complete LaTeX paper.tex for this paper folder.",
        "constraints": [
            "Output ONLY LaTeX (no markdown fences).",
            "Must compile as standalone article.",
            "Use clear sections, strong executive summary, and references section.",
            "Do not invent citations; if you cite, do so conservatively.",
        ],
        "intent_md": intent_md,
        "requirements_md": requirements_md,
    }

    payload = {
        "model": model,
        "input": [
            {"role": "system", "content": "You are a senior defense-oriented technical writer. Output only LaTeX."},
            {"role": "user", "content": json.dumps(prompt)},
        ],
    }

    rr = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=300,
    )
    rr.raise_for_status()

    data = rr.json()
    out_text = None
    for item in data.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    out_text = c.get("text")
                    break
    if not out_text:
        raise RuntimeError("No output_text from OpenAI")

    tex = out_text.strip()
    if not tex.startswith("\\documentclass"):
        # best-effort strip any accidental wrappers
        m = re.search(r"(\\documentclass\[.*?\].*|\\documentclass\{.*?\}.*)", tex, re.S)
        if m:
            tex = tex[m.start():].strip()
    return tex


def extract_requests(pr_body: str) -> list[str]:
    reqs: list[str] = []
    if not pr_body:
        return reqs
    for m in re.finditer(r"```\s*([\s\S]*?)\s*```", pr_body):
        block = m.group(1).strip()
        if block:
            reqs.append(block)
    for ln in pr_body.splitlines():
        if ln.strip().startswith("FIX:"):
            reqs.append(ln.strip()[len("FIX:"):].strip())
    return reqs


@dataclass
class PR:
    number: int
    head_ref: str
    base_ref: str
    title: str
    body: str


def list_open_prs(repo: str) -> list[PR]:
    raw = sh("gh", "pr", "list", "--repo", repo, "--state", "open", "--limit", "50", "--json", "number,headRefName,baseRefName,title,body")
    data = json.loads(raw)
    prs: list[PR] = []
    for it in data:
        prs.append(
            PR(
                number=int(it["number"]),
                head_ref=it["headRefName"],
                base_ref=it["baseRefName"],
                title=it.get("title") or "",
                body=it.get("body") or "",
            )
        )
    return prs


def pr_files(repo: str, number: int) -> list[str]:
    raw = sh("gh", "api", f"repos/{repo}/pulls/{number}/files", "--paginate")
    arr = json.loads(raw)
    return [f.get("filename") for f in arr if f.get("filename")]


def detect_single_paper(filenames: list[str]) -> str | None:
    dirs = set()
    for fn in filenames:
        m = re.match(r"^(papers/[^/]+)/", fn)
        if m:
            dirs.add(m.group(1))
    if len(dirs) == 1:
        return sorted(dirs)[0]
    return None


def checkout_pr_branch(repo: str, pr: PR) -> None:
    # Fetch branch and check out locally.
    run(["git", "fetch", "origin", f"{pr.head_ref}:{pr.head_ref}"], check=False)
    run(["git", "checkout", pr.head_ref], check=True)
    run(["git", "pull", "--ff-only", "origin", pr.head_ref], check=False)


def load_autopilot_cfg(paper_dir: Path) -> dict[str, Any]:
    p = paper_dir / "AUTOPILOT.yml"
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8", errors="ignore")) or {}


def read_requirements(paper_dir: Path) -> str:
    req_dir = paper_dir / "requirements"
    if not req_dir.exists():
        return ""
    parts: list[str] = []
    for fp in sorted(req_dir.glob("*.md")):
        parts.append(f"# {fp.name}\n" + fp.read_text(encoding="utf-8", errors="ignore").strip())
    return "\n\n".join([p for p in parts if p.strip()])


def ensure_generated_paper(paper_dir: Path, api_key: str) -> bool:
    """Generate tex/paper.tex if missing. Returns True if modified."""
    tex_path = paper_dir / "tex" / "paper.tex"
    if tex_path.exists() and tex_path.stat().st_size > 2000:
        return False

    intent = (paper_dir / "INTENT.md").read_text(encoding="utf-8", errors="ignore") if (paper_dir / "INTENT.md").exists() else ""
    reqs = read_requirements(paper_dir)

    if not intent.strip():
        return False

    tex_path.parent.mkdir(parents=True, exist_ok=True)
    model = openai_model(api_key)
    tex = openai_generate_latex(api_key, model, intent, reqs)
    tex_path.write_text(tex + "\n", encoding="utf-8")
    return True


def commit_if_dirty(msg: str) -> bool:
    code, out = run(["git", "status", "--porcelain"], check=True)
    if not out.strip():
        return False
    run(["git", "add", "-A"], check=True)
    run(["git", "commit", "-m", msg], check=False)
    return True


def push_branch(branch: str) -> None:
    run(["git", "push", "origin", branch], check=False)


def pr_checks_green(repo: str, number: int) -> tuple[bool, str]:
    """Return (ok, reason)."""
    raw = sh(
        "gh",
        "pr",
        "view",
        str(number),
        "--repo",
        repo,
        "--json",
        "isDraft,mergeable,statusCheckRollup",
    )
    data = json.loads(raw)
    if data.get("isDraft"):
        return False, "draft"
    if (data.get("mergeable") or "").upper() != "MERGEABLE":
        return False, f"mergeable={data.get('mergeable')}"

    rollup = data.get("statusCheckRollup") or []
    if not isinstance(rollup, list):
        return False, "no-check-rollup"

    bad = []
    pending = []
    ok_states = {"SUCCESS", "SKIPPED", "NEUTRAL"}
    for c in rollup:
        st = (c.get("state") or "").upper()
        name = c.get("name") or c.get("context") or "(unnamed)"
        if st in ok_states:
            continue
        if st in {"PENDING", "EXPECTED"}:
            pending.append(name)
        else:
            bad.append(f"{name}:{st}")

    if bad:
        return False, "failing=" + ",".join(bad)
    if pending:
        return False, "pending=" + ",".join(pending)
    return True, "ok"


def merge_pr(repo: str, number: int) -> tuple[int, str]:
    return run(
        [
            "gh",
            "pr",
            "merge",
            str(number),
            "--repo",
            repo,
            "--squash",
            "--delete-branch",
        ],
        check=False,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/repo")
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()

    repo_root = Path(__file__).resolve().parents[1]
    os.chdir(repo_root)

    log_dir = repo_root / "logs" / "moltbot-autonomy"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "runs.jsonl"

    run_summary = {"ts": now_ms(), "repo": args.repo, "prs": []}

    prs = list_open_prs(args.repo)
    for pr in prs:
        files = pr_files(args.repo, pr.number)
        paper = detect_single_paper(files)
        if not paper:
            continue

        paper_dir = repo_root / paper
        cfg = load_autopilot_cfg(paper_dir)
        autonomous = bool(((cfg.get("mode") or {}).get("autonomous")) )
        requested = extract_requests(pr.body)

        # Trigger condition: AUTOPILOT.yml says autonomous OR PR body includes explicit request blocks.
        if not (autonomous or requested):
            continue

        pr_rec: dict[str, Any] = {"number": pr.number, "paper": paper, "actions": []}

        # Safety: we only auto-generate if API key is available.
        if api_key:
            checkout_pr_branch(args.repo, pr)

            changed = ensure_generated_paper(paper_dir, api_key)
            if changed:
                pr_rec["actions"].append("generated tex/paper.tex")

            if commit_if_dirty(f"Moltbot: generate/update {paper}"):
                push_branch(pr.head_ref)
                pr_rec["actions"].append("pushed commits")

            # Auto-merge by default if checks are green.
            ok, reason = pr_checks_green(args.repo, pr.number)
            pr_rec["checks"] = {"ok": ok, "reason": reason}
            if ok:
                code, out = merge_pr(args.repo, pr.number)
                if code == 0:
                    pr_rec["actions"].append("merged")
                else:
                    pr_rec["actions"].append("merge_failed")
                    pr_rec["merge_error"] = out[-2000:]

        run_summary["prs"].append(pr_rec)

    log_path.open("a", encoding="utf-8").write(json.dumps(run_summary) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
