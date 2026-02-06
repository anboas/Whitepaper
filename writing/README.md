# Writing

This folder is the **source of truth** for short-form and medium-form writing that gets synced to the public site.

## Types
- `notes/` — short-form posts (quick, tight)
- `memos/` — medium-form briefs (still concise, but structured)

## How it publishes (end-to-end)
- Source lives here in `anboas/Whitepaper` under `writing/`.
- The public site repo (`anboas/adamboas.info`) has a scheduled workflow named **`sync-whitepaper`** that:
  - downloads the latest successful Whitepaper paper artifacts (PDF + HTML) from GitHub Actions, and
  - clones the Whitepaper repo and copies `writing/notes/**/*.md` + `writing/memos/**/*.md` into the site’s content collection.
- On the site, everything shows up under **/writing**:
  - Notes + memos render as Markdown pages.
  - Papers render from synced pandoc HTML and link to the synced PDF.

## Format
Each note/memo is Markdown with YAML frontmatter:

```md
---
title: "..."
date: 2026-02-06
status: published   # published | draft
type: note          # note | memo
summary: "..."      # optional

tags:
  - tag
---

Body...
```

## Conventions
- **Filename becomes slug** on the site.
  - Example: `writing/notes/why-trust-scopes.md` → `/writing/why-trust-scopes/`
- Use `status: draft` for anything you don’t want published yet (this is the publish/draft toggle).
- Keep titles punchy and specific.

## Publish / draft toggle
- `status: published` → shows up on the public site under `/writing/`
- `status: draft` → does not get a public page generated on the site
