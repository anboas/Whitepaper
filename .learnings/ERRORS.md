# Errors

## [ERR-20260131-001] moltbot_polish_cycle (OpenAI API 429)

**Logged**: 2026-01-31T08:34:54Z  
**Priority**: high  
**Status**: pending  
**Area**: infra

### Summary
OpenAI Responses API returned HTTP 429 (rate limit) during overnight polish cycle.

### Error


### Context
- Repo: /home/anboas/clawd/Whitepaper
- Command: python3 scripts/moltbot_polish_cycle.py --repo anboas/Whitepaper --paper agentic-force-creation --max_fixes 6
- Endpoint: https://api.openai.com/v1/responses

### Suggested Fix
- Add retry w/ exponential backoff + jitter on 429 in scripts/moltbot_polish_cycle.py.
- Optionally cap max wait (e.g., 60-120s) to keep cron runs bounded.
- Consider using a cheaper/faster model at night or reducing request frequency.

### Metadata
- Reproducible: unknown (depends on rate limit window)
- Related Files: scripts/moltbot_polish_cycle.py
- Tags: openai, rate-limit, cron

---

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
