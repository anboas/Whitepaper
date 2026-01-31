# papers/

Each whitepaper lives in its own folder so multiple papers can be developed in parallel.

## Structure
```
papers/
  <paper-id>/
    INTENT.md        # what this paper is + definition of done
    PAPER.yml        # variables/metadata (title/author/date/etc.)
    tex/paper.tex    # LaTeX source (single source)
    assets/          # optional images
    requirements/    # optional additional constraints
    rubric.yml       # optional per-paper overrides (else root rubric.yml)
```

## Conventions
- `<paper-id>` should be a stable slug (e.g. `ai-writing-loop`).
- `tex/paper.tex` is the entrypoint for builds.
- Root CI loops over all `papers/*` directories automatically.
