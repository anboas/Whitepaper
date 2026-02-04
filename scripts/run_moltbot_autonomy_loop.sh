#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

LOGDIR="logs/moltbot-autonomy"
ERRORLOG="$LOGDIR/errors.jsonl"
mkdir -p "$LOGDIR"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

log_error_json() {
  local stage="$1"; shift
  local exit_code="$1"; shift
  local msg="$1"; shift || true
  local traceback="${1-}"

  STAGE="$stage" EXIT_CODE="$exit_code" MSG="$msg" TRACEBACK="$traceback" TS="$(ts)" \
  python3 - <<'PY' >> "$ERRORLOG"
import json, os

data = {
  "ts": os.environ.get("TS"),
  "stage": os.environ.get("STAGE"),
  "exit_code": int(os.environ.get("EXIT_CODE") or 0),
  "error": os.environ.get("MSG") or "",
}
traceback = os.environ.get("TRACEBACK") or ""
if traceback:
  data["traceback"] = traceback
print(json.dumps(data, ensure_ascii=False))
PY
}

run_and_capture_stderr() {
  local stage="$1"; shift
  local tmp_err
  tmp_err="/tmp/moltbot_${stage}_stderr_$$.log"

  if ! "$@" 2> >(tee "$tmp_err" >&2); then
    local code=$?
    local tb
    tb="$(tail -n 400 "$tmp_err" | sed -e 's/\r$//')"
    log_error_json "$stage" "$code" "command failed" "$tb"
    exit "$code"
  fi
}

# Some scripts intentionally exit 0 even when they encounter recoverable errors
# (e.g., OpenAI 429 rate limits) to avoid cron hard-failure loops. For those,
# we capture combined output and log error markers ourselves.
run_and_capture_output_and_scan() {
  local stage="$1"; shift
  local tmp_out
  tmp_out="/tmp/moltbot_${stage}_out_$$.log"

  # tee combined output to file (stdout+stderr)
  set +e
  "$@" > >(tee "$tmp_out") 2>&1
  local code=$?
  set -e

  # If non-zero, treat as failure.
  if [[ $code -ne 0 ]]; then
    local tb
    tb="$(tail -n 400 "$tmp_out" | sed -e 's/\r$//')"
    log_error_json "$stage" "$code" "command failed" "$tb"
    exit "$code"
  fi

  # If output contains explicit failure markers, log them (but do not fail cron).
  if grep -E "apply_requested_changes FAILED:|FATAL ERROR:|Runner fatal error:" -n "$tmp_out" >/dev/null 2>&1; then
    local tb
    tb="$(tail -n 400 "$tmp_out" | sed -e 's/\r$//')"
    log_error_json "$stage" 0 "error marker detected in output" "$tb"
  fi
}

# --- Pull latest main ---
git fetch origin main
# ensure we're on main
git checkout main
# fast-forward only to avoid accidental merges
git pull --ff-only origin main

# --- Stabilized secrets (local key file) ---
export OPENAI_API_KEY="$(cat /home/anboas/.secrets/openai_api_key)"
if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  log_error_json "secrets" 2 "OPENAI_API_KEY empty"
  exit 2
fi

# --- Intake issues labeled moltbot ---
run_and_capture_stderr "issue_intake" python3 scripts/moltbot_issue_intake.py --repo anboas/Whitepaper

# --- Execute PR autonomy (rate-limit safe) ---
export MOLTBOT_MAX_PRS_PER_RUN=2
run_and_capture_output_and_scan "autonomy" python3 scripts/moltbot_autonomy.py --repo anboas/Whitepaper

# --- Guardrail: only allow paper.tex modifications (autonomy) ---
changed_files="$(git diff --name-only)"
if [[ -n "$changed_files" ]]; then
  disallowed="$(echo "$changed_files" | grep -Ev '^papers/[^/]+/tex/paper\.tex$' || true)"
  if [[ -n "$disallowed" ]]; then
    log_error_json "guardrail" 3 "Disallowed file modifications detected; restoring" "$disallowed"
    git restore --worktree --staged .
    exit 3
  fi
fi
