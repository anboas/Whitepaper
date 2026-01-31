#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p logs/moltbot-autonomy
ERROR_LOG="logs/moltbot-autonomy/errors.jsonl"
LAST_LOG="/tmp/moltbot-autonomy-last.log"

utc_ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

append_error_jsonl() {
  local error_text="$1"
  python3 -c 'import json,sys; from datetime import datetime,timezone; print(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00","Z"), "error": sys.stdin.read()}))' \
    <<<"$error_text" >>"$ERROR_LOG"
}

run_all() {
  echo "==> git fetch"
  git fetch origin main

  echo "==> checkout main"
  git checkout main

  echo "==> pull latest main"
  git pull --ff-only origin main

  echo "==> load OPENAI_API_KEY from Vaultwarden"
  export BW_HOST="https://localhost:8222"
  export BW_INSECURE=1
  export BW_EMAIL="anboas@gmail.com"
  export VAULT_OPENAI_SEARCH="OPENAI_API_KEY"
  export OPENAI_API_KEY="$(scripts/vaultwarden_get_openai_key.sh)"
  if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    echo "OPENAI_API_KEY empty" >&2
    return 2
  fi

  echo "==> issue intake"
  python3 scripts/moltbot_issue_intake.py --repo anboas/Whitepaper

  echo "==> autonomy"
  python3 scripts/moltbot_autonomy.py --repo anboas/Whitepaper
}

# Always capture output so we can include it in errors.jsonl
{
  echo "[moltbot] $(utc_ts) starting"
  run_all
  echo "[moltbot] $(utc_ts) done"
} 2>&1 | tee "$LAST_LOG"

# If we got here, success
exit 0
