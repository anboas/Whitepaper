# Writing

This folder is the source tree for short-form and medium-form writing that gets synced to the public site.

## Types
- `notes/` — short-form posts (quick, tight), source-of-truth in Markdown.
- `memos/` — metadata mirror in Markdown for site collection indexing.

Memo content source-of-truth is now LaTeX under `memos/<slug>/tex/memo.tex`.

## How it publishes (end-to-end)
- Source lives in `anboas/Whitepaper`.
- Notes publish from `writing/notes/*.md` directly.
- Memos publish from the LaTeX memo pipeline:
  - source: `memos/<slug>/tex/memo.tex` + `memos/<slug>/MEMO.yml`
  - CI workflow: `build-memos.yml` (PDF + HTML + hash manifest)
  - site sync: pulls `memo-<slug>` artifacts into `public/memos/` and `src/generated/memos/`
- `writing/memos/*.md` remains as metadata mirror so the Astro `writing` collection keeps one unified index.

## Formats
### Notes (source-of-truth)
Markdown with YAML frontmatter:

```md
---
title: "..."
date: 2026-02-06
status: published   # published | draft
type: note
summary: "..."
tags:
  - tag
---

Body...
```

### Memos (source-of-truth)
- `memos/<slug>/MEMO.yml` for metadata
- `memos/<slug>/tex/memo.tex` for canonical content/layout

## Conventions
- Notes: filename becomes slug on the site.
  - Example: `writing/notes/why-trust-scopes.md` → `/writing/why-trust-scopes/`
- Memos: folder name becomes slug.
  - Example: `memos/2026-02-17-dont-put-frontier-ai-under-itar/` → `/writing/2026-02-17-dont-put-frontier-ai-under-itar/`
- Use `status: draft` in note frontmatter or `MEMO.yml` to keep content off the public site.
- Keep titles punchy and specific.

## Publish / draft toggle
- `status: published` → shows up on the public site under `/writing/`
- `status: draft` → does not get a public page generated on the site
- For memos, status is read from `memos/<slug>/MEMO.yml` and mirrored into `writing/memos/<slug>.md` during sync.
