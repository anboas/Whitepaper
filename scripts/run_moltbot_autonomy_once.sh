#!/usr/bin/env bash
set -euo pipefail

LOGFILE="$(pwd)/logs/moltbot-autonomy/errors.jsonl"
RUNLOG="$(pwd)/logs/moltbot-autonomy/run-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$(dirname "$LOGFILE")"

log_error(){
  local exit_code=$?
  local ts
  ts=$(date -Is)
  {
    echo "[{";
  } >/dev/null 2>&1 || true

  # JSON-safe encode message via python
  local msg_json
  msg_json=$(printf "%s" "${1:-}" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
  printf '{"ts":%s,"exit_code":%s,"error":%s,"runlog":%s}\n' \
    "$(python3 -c "import json; print(json.dumps(\"$ts\"))")" \
    "$(python3 -c "import json; print(json.dumps($exit_code))")" \
    "$msg_json" \
    "$(python3 -c "import json; print(json.dumps(\"$RUNLOG\"))")" >> "$LOGFILE" || true

  echo "Autonomy run failed (exit $exit_code). Logged to: $LOGFILE" >&2
  echo "Run output: $RUNLOG" >&2
  exit "$exit_code"
}

trap 'log_error "Autonomy run failed. Last command: ${BASH_COMMAND}"' ERR

# tee all output
exec > >(tee -a "$RUNLOG") 2>&1

cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Pull latest main
git fetch origin main
git checkout main
git pull --ff-only origin main

# Stabilized secrets (local key file)
export OPENAI_API_KEY="$(cat /home/anboas/.secrets/openai_api_key)"
[[ -n "${OPENAI_API_KEY}" ]] || exit 2

# Intake issues labeled `moltbot`
python3 scripts/moltbot_issue_intake.py --repo anboas/Whitepaper

# Execute PR autonomy (rate-limit safe)
export MOLTBOT_MAX_PRS_PER_RUN=2
python3 scripts/moltbot_autonomy.py --repo anboas/Whitepaper
