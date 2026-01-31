#!/usr/bin/env python3
"""Moltbot issue-driven intake: issues are the command surface.

Why
- Issues are a clean place to ask for work (they are *requests*).
- PRs are the right place to represent the resulting changes (diff + CI + merge).

This script:
- Scans open issues labeled `moltbot`.
- For each unprocessed issue, creates a branch + PR implementing the issue request.
- Comments on the issue with the created PR URL.
- Adds label `moltbot/claimed` to the issue.

Autonomy execution:
- The PR body contains a fenced request block, so `moltbot_autonomy.py` can apply it.

Env
- Requires `gh` authenticated locally.

Usage
  python3 scripts/moltbot_issue_intake.py --repo anboas/Whitepaper
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path


def sh(*cmd: str) -> str:
    return subprocess.check_output(list(cmd), text=True).strip()


def run(cmd: list[str], check: bool = True) -> tuple[int, str]:
    p = subprocess.run(cmd, text=True, capture_output=True)
    out = (p.stdout or "") + ("\n" if p.stderr else "") + (p.stderr or "")
    if check and p.returncode != 0:
        raise RuntimeError(out)
    return p.returncode, out.strip()


def ensure_label(repo: str, name: str, color: str = "5319e7", desc: str = "") -> None:
    # create if missing
    code, _ = run(["gh", "api", f"repos/{repo}/labels/{name}"], check=False)
    if code == 0:
        return
    args = ["gh", "api", f"repos/{repo}/labels", "-f", f"name={name}", "-f", f"color={color}"]
    if desc:
        args += ["-f", f"description={desc}"]
    run(args, check=False)


def parse_issue_body(body: str) -> dict:
    """Expected:

    Paper: <paper-id>
    Request:
      ... (free text)

    If Paper missing, default to agentic-force-creation.
    """
    paper = "agentic-force-creation"
    req = body.strip()
    for line in body.splitlines():
        if line.lower().startswith("paper:"):
            paper = line.split(":", 1)[1].strip() or paper
    return {"paper": paper, "request": req}


def comment_issue(repo: str, number: int, body: str) -> None:
    run(["gh", "api", f"repos/{repo}/issues/{number}/comments", "-f", f"body={body}"], check=False)


def add_labels(repo: str, number: int, labels: list[str]) -> None:
    if not labels:
        return
    # Use POST /issues/{issue_number}/labels to add without clobbering existing labels.
    cmd = ["gh", "api", f"repos/{repo}/issues/{number}/labels", "--method", "POST"]
    for lab in labels:
        cmd += ["-f", f"labels[]={lab}"]
    run(cmd, check=False)


def list_moltbot_issues(repo: str) -> list[dict]:
    raw = sh(
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--state",
        "open",
        "--label",
        "moltbot",
        "--limit",
        "50",
        "--json",
        "number,title,body,labels,url",
    )
    return json.loads(raw)


def has_label(issue: dict, name: str) -> bool:
    labs = issue.get("labels") or []
    for l in labs:
        if isinstance(l, dict) and (l.get("name") == name):
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/repo")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    # Ensure labels exist
    ensure_label(args.repo, "moltbot", color="0052cc", desc="Work requests for Moltbot")
    ensure_label(args.repo, "moltbot/claimed", color="5319e7", desc="Moltbot has opened/claimed a PR")

    issues = list_moltbot_issues(args.repo)
    for iss in issues:
        num = int(iss["number"])
        if has_label(iss, "moltbot/claimed"):
            continue

        parsed = parse_issue_body(iss.get("body") or "")
        paper = parsed["paper"]
        req = parsed["request"]

        ts = time.strftime("%Y%m%d-%H%M%S")
        title = f"{iss.get('title') or 'Moltbot change'}"

        # Create PR using helper script (keeps our conventions consistent)
        cmd = [
            "python3",
            str(repo_root / "scripts" / "moltbot_make_pr.py"),
            "--repo",
            args.repo,
            "--paper",
            paper,
            "--title",
            f"Issue #{num}: {title}",
            "--request",
            f"Source issue: {iss.get('url')}\n\n{req}",
        ]
        try:
            _, out = run(cmd, check=True)
            pr_url = out.strip().splitlines()[-1].strip() if out.strip() else "(created)"
            comment_issue(
                args.repo,
                num,
                "## Moltbot\nI opened a PR for this issue and will execute it autonomously.\n\nPR: " + pr_url,
            )
            add_labels(args.repo, num, ["moltbot/claimed"])
        except Exception as e:
            comment_issue(args.repo, num, "## Moltbot\nFailed to open PR for this issue. Error:\n\n```\n" + str(e)[:1500] + "\n```")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
