# Writing

This folder is the source of truth for short-form and medium-form writing that gets synced to the public site.

## Types
- `notes/` — short-form posts
- `memos/` — medium-form briefs

## Format
Each file is Markdown with frontmatter:

```md
---
title: "..."
date: 2026-02-06
status: published   # or draft
type: note          # note | memo
summary: "..."      # optional

tags:
  - tag
---

Body...
```
