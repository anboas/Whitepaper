#!/usr/bin/env python3
"""Download the latest successful PDF artifact for a paper from GitHub Actions.

Requires:
- `gh` authenticated with access to the repo

Usage:
  python3 scripts/get_latest_paper_pdf.py --repo anboas/Whitepaper --paper agentic-force-creation

Prints the absolute path to the downloaded PDF on stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


def sh(*cmd: str) -> str:
    return subprocess.check_output(list(cmd), text=True).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--paper", required=True)
    ap.add_argument("--workflow", default="build-papers")
    ap.add_argument("--branch", default="main")
    args = ap.parse_args()

    runs_raw = sh(
        "gh",
        "run",
        "list",
        "--repo",
        args.repo,
        "--workflow",
        args.workflow,
        "--branch",
        args.branch,
        "--status",
        "completed",
        "--limit",
        "30",
        "--json",
        "databaseId,conclusion,createdAt,displayTitle",
    )
    runs = json.loads(runs_raw)
    run_id = None
    for r in runs:
        if (r.get("conclusion") or "").lower() == "success":
            run_id = int(r["databaseId"])
            break
    if not run_id:
        raise SystemExit("No successful build-papers run found")

    artifact_name = f"paper-{args.paper}"
    out_dir = Path("outgoing") / "pdf" / args.paper / str(run_id)
    out_dir.mkdir(parents=True, exist_ok=True)

    subprocess.check_call(
        [
            "gh",
            "run",
            "download",
            str(run_id),
            "--repo",
            args.repo,
            "-n",
            artifact_name,
            "-D",
            str(out_dir),
        ]
    )

    pdfs = sorted(out_dir.rglob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"No PDF found in downloaded artifact {artifact_name} for run {run_id}")

    # Prefer a file named paper.pdf if present.
    for p in pdfs:
        if p.name.lower() == "paper.pdf":
            print(str(p.resolve()))
            return 0

    print(str(pdfs[0].resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
