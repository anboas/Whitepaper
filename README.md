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
This is a **deterministic + heuristic** quality bar (no LLM) meant to catch:
- TODO/TBD/FIXME left in
- missing required sections (Executive Summary / Problem / Recommendations / Conclusion)
- missing sources/refs markers
- too-short drafts
- excessive hedging / hype
- overly-long sentences
- too-low readability (approx)
- too much passive voice (heuristic)
- recommendations that aren’t framed as actions

## Human review + AI feedback loop (PR-native)
You can drive the entire iteration loop from GitHub PRs without chatting here:

1) Open a PR (normal).
2) Add label **`full-review`** → triggers **expensive** semantic review and posts results as a PR comment.
3) To request auto-fixes, leave one or more PR comments starting with:
   - `FIX: <what to change>`
4) Add label **`apply-fixes`** → Moltbot will attempt to apply the `FIX:` comments to `tex/whitepaper.tex`, commit, and push to the PR branch.

The deterministic gates always run first; LLM work is layered on top.

## Multi-paper layout
We support multiple papers in parallel under `papers/`.

- `papers/<paper-id>/INTENT.md` — what the paper is + what “polished” means
- `papers/<paper-id>/PAPER.yml` — variables/metadata
- `papers/<paper-id>/tex/paper.tex` — LaTeX entrypoint
- `papers/<paper-id>/rubric.yml` — optional overrides

CI builds all papers via `.github/workflows/build-papers.yml`.

## Layout (legacy single-paper)
- `tex/whitepaper.tex` — legacy single working paper + template
- `INTENT.md` — legacy intent
- `rubric.yml` — publishability rubric
- `scripts/rubric_check.py` — rubric evaluator
- `.github/workflows/build-pdf.yml` — CI build (legacy)

## Change policy
Commits should be small and intentional. Prefer:
- one conceptual change per commit
- message includes the *why* (not just the *what*)
