# Whitepaper

Whitepaper series (LaTeX) — strategic, high-impact briefs.

## What this repo is
A repeatable, auditable (git) workflow for producing publish-ready artifacts:
- opinionated executive summaries
- falsifiable claims + clear recommendations
- consistent branding and layout
- automated rubric gating + multi-target builds (PDF + HTML)

## Build
### GitHub Actions (recommended)
Every push / PR runs:
- **rubric gate** (fails if the draft is obviously not ready)
- PDF build
- HTML build

Artifacts are uploaded from Actions → `build-whitepaper`.

### Local
If you have TeX Live installed:
```bash
make pdf
```

If you also have `pandoc`:
```bash
make html
```

Rubric gate:
```bash
make rubric
```

Outputs:
- `build/whitepaper.pdf`
- `build/whitepaper.html`

## Rubric gating
Rubric is defined in `rubric.yml` and enforced by `scripts/rubric_check.py`.
This is a **deterministic**, low-drama quality bar meant to catch:
- TODO/TBD/FIXME left in
- missing Executive Summary / Recommendations
- missing sources/refs markers
- too-short drafts

## Layout
- `tex/whitepaper.tex` — current working paper + template
- `rubric.yml` — publishability rubric
- `scripts/rubric_check.py` — rubric evaluator
- `.github/workflows/build-pdf.yml` — CI build

## Change policy
Commits should be small and intentional. Prefer:
- one conceptual change per commit
- message includes the *why* (not just the *what*)
