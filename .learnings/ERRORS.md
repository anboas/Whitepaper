# Errors

## [ERR-20260201-001] autonomy-error-logging

**Logged**: 2026-02-01T01:35:41.437804+00:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Bash heredoc was malformed while appending JSONL error logs, causing an unnecessary command failure.

### Error
```
/bin/bash: warning: here-document delimited by end-of-file (wanted `PY`)
NameError: name 'PY' is not defined
```

### Context
- Intended to append a JSON line to `logs/moltbot-autonomy/errors.jsonl` after an autonomy run failure.
- Used `python3 - <<'PY' ... PY >> file` inside a longer bash command; delimiter placement/quoting was wrong.

### Suggested Fix
Use a single `python3 -c` that opens the file in append mode, or ensure the heredoc delimiter is on its own line with no trailing whitespace, and avoid mixing heredoc with output redirection.

### Metadata
- Reproducible: yes
- Related Files: logs/moltbot-autonomy/errors.jsonl
- Tags: bash, heredoc, logging

---
