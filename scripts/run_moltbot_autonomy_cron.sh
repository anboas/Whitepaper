#!/usr/bin/env bash
set -u

REPO_DIR="/home/anboas/clawd/Whitepaper"
ERROR_LOG="$REPO_DIR/logs/moltbot-autonomy/errors.jsonl"

mkdir -p "$(dirname "$ERROR_LOG")"

log_error() {
  local msg="$1"
  local ts
  ts="$(date -Is)"

  # Escape newlines/quotes minimally via python (always available in this repo env)
  python3 - <<PY >>"$ERROR_LOG"
import json, os
print(json.dumps({"ts": os.environ.get("TS"), "error": os.environ.get("ERR")}, ensure_ascii=False))
PY
}

run() {
  cd "$REPO_DIR"

  # Pull latest main
  git fetch origin main
  git checkout main
  git pull --ff-only origin main

  # Stabilized secrets: prefer local key file
  export OPENAI_API_KEY="$(cat /home/anboas/.secrets/openai_api_key)"
  test -n "$OPENAI_API_KEY" || exit 2

  # Intake issues labeled `moltbot`
  python3 scripts/moltbot_issue_intake.py --repo anboas/Whitepaper

  # Execute PR autonomy (rate-limit safe)
  export MOLTBOT_MAX_PRS_PER_RUN=2
  python3 scripts/moltbot_autonomy.py --repo anboas/Whitepaper
}

if ! output="$(run 2>&1)"; then
  ts="$(date -Is)"
  export TS="$ts"
  export ERR="$output"
  python3 - <<'PY' >>"$ERROR_LOG"
import json, os
print(json.dumps({"ts": os.environ.get("TS"), "error": os.environ.get("ERR")}, ensure_ascii=False))
PY
  echo "$output" >&2
  exit 1
fi

# Emit output for cron logs
printf "%s\n" "$output"
