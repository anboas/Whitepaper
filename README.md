# Whitepaper

Whitepaper series (LaTeX) — strategic, high-impact briefs.

## What this repo is
A repeatable, auditable (git) workflow for producing LinkedIn-ready PDFs:
- opinionated executive summaries
- falsifiable claims + clear recommendations
- consistent branding and layout

## Build
### GitHub Actions (recommended)
Every push to `main` builds a PDF and uploads it as an artifact (see Actions → `build-pdf`).

### Local
If you have TeX Live installed:
```bash
make pdf
```
Output: `build/whitepaper.pdf`

## Layout
- `tex/whitepaper.tex` — current working paper + template
- `.github/workflows/build-pdf.yml` — CI build

## Change policy
Commits should be small and intentional. Prefer:
- one conceptual change per commit
- message includes the *why* (not just the *what*)
