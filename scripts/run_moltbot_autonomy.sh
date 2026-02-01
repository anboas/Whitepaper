#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Pull latest main
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git fetch origin main
  git checkout main
  git pull --ff-only origin main
fi

# Stabilized secrets (local key file)
export OPENAI_API_KEY="$(cat /home/anboas/.secrets/openai_api_key)"
test -n "$OPENAI_API_KEY" || exit 2

LOGDIR="logs/moltbot-autonomy"
ERRFILE="$LOGDIR/errors.jsonl"
mkdir -p "$LOGDIR"

json_escape_file() {
  python3 -c 'import json,sys; print(json.dumps(open(sys.argv[1],"r",encoding="utf-8",errors="replace").read()))' "$1"
}

log_error() {
  local step="$1"; local tmpfile="$2"
  local ts
  ts=$(date -Is)
  local err_json
  err_json=$(json_escape_file "$tmpfile")
  python3 - <<PY >> "$ERRFILE"
import json
print(json.dumps({"ts":"$ts","step":"$step","error":json.loads($err_json)}))
PY
}

run_py() {
  local step="$1"; shift
  local tmp
  tmp=$(mktemp)

  set +e
  python3 "$@" 2> >(tee "$tmp" >&2)
  local rc=$?
  set -e

  if [ $rc -ne 0 ]; then
    log_error "$step" "$tmp"
    rm -f "$tmp"
    return $rc
  fi

  rm -f "$tmp"
  return 0
}

# Intake issues labeled moltbot
run_py "issue_intake" scripts/moltbot_issue_intake.py --repo anboas/Whitepaper

# Execute PR autonomy (rate-limit safe)
export MOLTBOT_MAX_PRS_PER_RUN=${MOLTBOT_MAX_PRS_PER_RUN:-2}

# Simple retry/backoff on 429s
attempt=1
max_attempts=3
while true; do
  tmp=$(mktemp)
  set +e
  python3 scripts/moltbot_autonomy.py --repo anboas/Whitepaper 2> >(tee "$tmp" >&2)
  rc=$?
  set -e

  if [ $rc -eq 0 ]; then
    rm -f "$tmp"
    break
  fi

  if grep -q " 429 " "$tmp" || grep -q "Too Many Requests" "$tmp"; then
    log_error "autonomy_429_attempt_${attempt}" "$tmp"
    rm -f "$tmp"
    if [ $attempt -lt $max_attempts ]; then
      sleep_s=$((30 * attempt))
      echo "Autonomy hit 429; backing off ${sleep_s}s (attempt ${attempt}/${max_attempts})" >&2
      sleep "$sleep_s"
      attempt=$((attempt+1))
      continue
    fi
  else
    log_error "autonomy" "$tmp"
    rm -f "$tmp"
  fi

  exit $rc
done

# Guardrail: only allow autonomous edits to papers/<paper>/tex/paper.tex
changed=$(git diff --name-only)
if [ -n "$changed" ]; then
  bad=$(printf "%s\n" "$changed" | awk '!/^papers\/[^\/]+\/tex\/paper\.tex$/{print}')
  if [ -n "$bad" ]; then
    echo "Guardrail violation: non-paper.tex changes detected; reverting these paths:" >&2
    echo "$bad" >&2
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      git checkout -- "$f" || true
    done <<< "$bad"

    ts=$(date -Is)
    python3 - <<PY >> "$ERRFILE"
import json
files = ${bad@Q}.splitlines()
files = [f for f in files if f.strip()]
print(json.dumps({"ts":"$ts","step":"guardrail","error":"Non-paper.tex changes reverted","files":files}))
PY
  fi
fi

echo "Autonomy run complete."
