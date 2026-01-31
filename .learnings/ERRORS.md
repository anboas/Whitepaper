# Errors

## [ERR-20260131-001] moltbot_polish_cycle (OpenAI API 429)

**Logged**: 2026-01-31T08:35:10Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
OpenAI Responses API returned HTTP 429 (rate limit) during overnight polish cycle.

### Error
```
requests.exceptions.HTTPError: 429 Client Error: Too Many Requests for url: https://api.openai.com/v1/responses
```

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
