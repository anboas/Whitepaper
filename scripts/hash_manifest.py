#!/usr/bin/env python3

"""Create a small JSON manifest with sha256 hashes for sync verification."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", default=None, help="(deprecated) paper slug")
    ap.add_argument("--slug", default=None, help="artifact slug")
    ap.add_argument("--kind", default="paper", help="artifact kind (paper|memo|other)")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--html", required=True)
    ap.add_argument("--source-sha", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    slug = args.slug or args.paper
    if not slug:
        raise SystemExit("hash_manifest: pass --slug (or legacy --paper)")

    pdf = Path(args.pdf)
    html = Path(args.html)
    out = Path(args.out)

    if not pdf.exists():
        raise SystemExit(f"hash_manifest: missing pdf: {pdf}")
    if not html.exists():
        raise SystemExit(f"hash_manifest: missing html: {html}")

    manifest = {
        "kind": args.kind,
        "slug": slug,
        "source": {"repo": "anboas/Whitepaper", "sha": args.source_sha},
        "artifacts": {
            "pdf": {"path": str(pdf).replace('\\\\', '/'), "sha256": sha256_file(pdf)},
            "html": {"path": str(html).replace('\\\\', '/'), "sha256": sha256_file(html)},
        },
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"hash_manifest: wrote {out}")


if __name__ == "__main__":
    main()
