#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p logs/moltbot-autonomy
ERROR_LOG="logs/moltbot-autonomy/errors.jsonl"

ts() { date -Is; }

json_escape() {
  python3 - <<'PY'
import json,sys
print(json.dumps(sys.stdin.read()))
PY
}

log_error() {
  local step="$1"
  local msg="$2"
  local t
  t="$(ts)"
  local msg_json
  msg_json=$(printf "%s" "$msg" | json_escape)
  printf '{"timestamp":"%s","step":"%s","error":%s}\n' "$t" "$step" "$msg_json" >> "$ERROR_LOG"
}

run_step() {
  local name="$1"; shift
  echo "==> ${name}"
  local out
  if ! out=$("$@" 2>&1); then
    echo "$out" >&2
    log_error "$name" "$out"
    return 1
  fi
  echo "$out"
}

# Pull latest main
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Working tree not clean; stashing before pull" >&2
  git stash push -u -m "moltbot-autonomy pre-pull $(ts)" >/dev/null
fi

git fetch origin main
git checkout main

git pull --ff-only origin main

# Load OPENAI_API_KEY from Vaultwarden via bw CLI helper script
export BW_HOST="https://localhost:8222"
export BW_INSECURE=1
export BW_EMAIL="anboas@gmail.com"
export VAULT_OPENAI_SEARCH="OPENAI_API_KEY"

if ! key="$(scripts/vaultwarden_get_openai_key.sh 2>&1)"; then
  echo "$key" >&2
  log_error "vaultwarden_get_openai_key" "$key"
  exit 1
fi
export OPENAI_API_KEY="$key"

run_step "Issue intake" python3 scripts/moltbot_issue_intake.py --repo anboas/Whitepaper
run_step "Autonomy" python3 scripts/moltbot_autonomy.py --repo anboas/Whitepaper
