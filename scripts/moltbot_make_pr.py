#!/usr/bin/env python3
"""Create a PR from chat commands, then Moltbot autonomy will pick it up.

This script is meant to be run by Moltbot (you can ask in chat: "open a PR to do X").

What it does
- Creates a branch.
- Adds a request file under papers/<paper>/requirements/ (so the PR has a clear paper-local audit trail).
- Opens a PR with the request embedded in the body as a fenced code block.

Autonomy trigger
- Moltbot autonomy loop triggers on fenced code blocks in PR body.

Usage
  python3 scripts/moltbot_make_pr.py \
    --repo anboas/Whitepaper \
    --paper agentic-force-creation \
    --title "Insert callout quotes" \
    --request "..."

Notes
- Does not apply any edits itself; it creates the PR and relies on the autonomy loop to execute.
"""

from __future__ import annotations

import argparse
import subprocess
import time
from pathlib import Path


def run(cmd: list[str], check: bool = True) -> str:
    p = subprocess.run(cmd, text=True, capture_output=True)
    if check and p.returncode != 0:
        raise SystemExit((p.stdout or "") + ("\n" if p.stderr else "") + (p.stderr or ""))
    return (p.stdout or "").strip()


def slug(s: str) -> str:
    out = []
    for ch in s.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "_", "-", "."):
            out.append("-")
    ss = "".join(out)
    while "--" in ss:
        ss = ss.replace("--", "-")
    return ss.strip("-")[:50] or "change"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--paper", required=True, help="paper id (folder under papers/)")
    ap.add_argument("--title", required=True)
    ap.add_argument("--request", required=True)
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    paper_dir = repo_root / "papers" / args.paper
    if not paper_dir.exists():
        raise SystemExit(f"paper folder not found: {paper_dir}")

    ts = time.strftime("%Y%m%d-%H%M%S")
    branch = f"moltbot/{args.paper}/{ts}-{slug(args.title)}"

    run(["git", "checkout", "main"], check=False)
    run(["git", "pull", "--ff-only"], check=False)
    run(["git", "checkout", "-b", branch])

    req_dir = paper_dir / "requirements"
    req_dir.mkdir(parents=True, exist_ok=True)
    req_path = req_dir / f"moltbot-request-{ts}.md"
    req_path.write_text(
        "# Moltbot Request\n\n" + args.request.strip() + "\n",
        encoding="utf-8",
    )

    run(["git", "add", str(req_path)])
    run(["git", "commit", "-m", f"Request: {args.title}"])
    run(["git", "push", "-u", "origin", branch])

    body = (
        "This PR was opened by Moltbot from chat instructions.\n\n"
        "```text\n" + args.request.strip() + "\n```\n"
    )

    # Use gh api to avoid gh pr edit GraphQL projectCards regression.
    out = run(
        [
            "gh",
            "pr",
            "create",
            "--repo",
            args.repo,
            "--head",
            branch,
            "--base",
            "main",
            "--title",
            args.title,
            "--body",
            body,
        ],
        check=True,
    )
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
