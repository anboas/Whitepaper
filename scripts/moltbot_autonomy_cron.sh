#!/usr/bin/env bash
set -euo pipefail

cd /home/anboas/clawd/Whitepaper

log_error() {
  local ts msg msg_json
  ts=$(date -Is)
  mkdir -p logs/moltbot-autonomy
  msg=${1:-"unknown error"}
  msg_json=$(python3 - <<'PY'
import json,sys
print(json.dumps(sys.stdin.read()))
PY
<<<"$msg")
  printf '{"ts":"%s","error":%s}\n' "$ts" "$msg_json" >> logs/moltbot-autonomy/errors.jsonl
}

on_err() {
  local rc=$?
  local cmd=${BASH_COMMAND:-"(unknown)"}
  log_error "command: ${cmd}\npwd: $(pwd)\nrc: ${rc}"
  exit "$rc"
}
trap on_err ERR

# Pull latest main
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repo: $(pwd)" >&2
  exit 1
fi

git fetch origin main
if git show-ref --verify --quiet refs/heads/main; then
  git checkout main
else
  git checkout -b main --track origin/main
fi

git pull --ff-only origin main

# Secrets
export OPENAI_API_KEY="$(cat /home/anboas/.secrets/openai_api_key)"
[[ -n "$OPENAI_API_KEY" ]] || exit 2

# Intake issues labeled moltbot
python3 scripts/moltbot_issue_intake.py --repo anboas/Whitepaper

# Execute autonomy (rate-limit safe)
export MOLTBOT_MAX_PRS_PER_RUN=2
python3 scripts/moltbot_autonomy.py --repo anboas/Whitepaper
