#!/usr/bin/env python3
"""Build memo-styled note TeX and HTML from a markdown note."""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import re
import subprocess
import tempfile

import yaml

from notes import parse_frontmatter


def latex_escape(value: object) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def readable_date(value: object) -> str:
    if isinstance(value, datetime):
        d = value.date()
    elif isinstance(value, date):
        d = value
    else:
        raw = str(value)
        try:
            d = date.fromisoformat(raw[:10])
        except ValueError:
            return raw
    return f"{d:%B} {d.day}, {d:%Y}"


def strip_leading_title(body: str, title: str) -> str:
    lines = body.lstrip().splitlines()
    if not lines:
        return body
    first = lines[0].strip()
    if first.startswith("# "):
        h1 = first[2:].strip()
        if h1.casefold() == title.strip().casefold():
            return "\n".join(lines[1:]).lstrip() + "\n"
    return body


def pandoc_fragment(markdown: str, to: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as tmp:
        tmp.write(markdown)
        tmp_path = Path(tmp.name)
    try:
        return subprocess.check_output(
            ["pandoc", str(tmp_path), "--from", "markdown+yaml_metadata_block", "--to", to],
            text=True,
        )
    finally:
        tmp_path.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--tex-out", required=True)
    ap.add_argument("--html-out", required=True)
    args = ap.parse_args()

    src = Path(args.input)
    tex_out = Path(args.tex_out)
    html_out = Path(args.html_out)

    data, body = parse_frontmatter(src.read_text(encoding="utf-8"))
    title = str(data.get("title") or src.stem)
    display_date = readable_date(data.get("date") or "")
    body = strip_leading_title(body, title)

    latex_body = pandoc_fragment(body, "latex")
    html_body = pandoc_fragment(body, "html5")

    tex_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.parent.mkdir(parents=True, exist_ok=True)

    tex_out.write_text(
        "\n".join(
            [
                r"\documentclass[11pt]{article}",
                "",
                rf"\newcommand{{\MemoTitle}}{{{latex_escape(title)}}}",
                rf"\newcommand{{\MemoDate}}{{{latex_escape(display_date)}}}",
                r"\newcommand{\MemoLogoPath}{../../../tex/assets/icon-180.png}",
                "",
                r"\input{../../../tex/memo_preamble.tex}",
                "",
                r"\begin{document}",
                r"\MemoRenderHeader",
                "",
                latex_body.strip(),
                "",
                r"\end{document}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    html_out.write_text(html_body.strip() + "\n", encoding="utf-8")
    print(f"build_note_artifacts: wrote {tex_out} and {html_out}")


if __name__ == "__main__":
    main()
