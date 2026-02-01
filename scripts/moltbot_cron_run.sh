#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/anboas/clawd/Whitepaper"
REPO_SLUG="anboas/Whitepaper"
OPENAI_KEY_FILE="/home/anboas/.secrets/openai_api_key"
ERR_LOG_REL="logs/moltbot-autonomy/errors.jsonl"

cd "$REPO_DIR"

echo "[moltbot] $(date -Iseconds) starting"

# Keep local changes safe
STASHED=0
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "[moltbot] working tree dirty; stashing"
  git stash push -u -m "moltbot-autonomy-$(date -Iseconds)" >/dev/null || true
  STASHED=1
fi

git fetch origin main

git checkout main

git pull --ff-only origin main

export OPENAI_API_KEY="$(cat "$OPENAI_KEY_FILE" 2>/dev/null || true)"
if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "[moltbot] OPENAI_API_KEY empty" >&2
  exit 2
fi

mkdir -p "$(dirname "$ERR_LOG_REL")"

run_and_log() {
  local cmd="$1"
  echo "[moltbot] running: $cmd"

  local tmp
  tmp="$(mktemp)"

  set +e
  bash -lc "$cmd" >"$tmp" 2>&1
  local rc=$?
  set -e

  cat "$tmp"

  if [[ $rc -ne 0 ]]; then
    python3 - <<PY
import json, datetime
path = ${ERR_LOG_REL!r}
cmd = ${cmd!r}
rc = int(${rc})
with open(${""}"$tmp"${""}"!r, "r", encoding="utf-8", errors="replace") as f:
    out = f.read()
rec = {
  "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "cmd": cmd,
  "rc": rc,
  "output": out,
}
with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
PY
    rm -f "$tmp"
    return $rc
  fi

  rm -f "$tmp"
}

run_and_log "python3 scripts/moltbot_issue_intake.py --repo $REPO_SLUG"

export MOLTBOT_MAX_PRS_PER_RUN=2
run_and_log "python3 scripts/moltbot_autonomy.py --repo $REPO_SLUG"

# Auto-merge: only when mergeable + checks green. Do NOT use --auto (requires repo setting).
if command -v gh >/dev/null 2>&1; then
  echo "[moltbot] checking for mergeable PRs"
  gh pr list --repo "$REPO_SLUG" --author @me --state open --json number,mergeable,statusCheckRollup \
    --jq '.[] | @base64' \
  | while IFS= read -r row; do
      [[ -z "$row" ]] && continue
      prjson="$(printf "%s" "$row" | base64 -d)"

      num="$(python3 - <<PY
import json
j=json.loads(${prjson@Q})
print(j["number"])
PY
)"

      mergeable="$(python3 - <<PY
import json
j=json.loads(${prjson@Q})
print(j.get("mergeable"))
PY
)"

      [[ "$mergeable" == "MERGEABLE" ]] || continue

      all_good="$(python3 - <<PY
import json
j=json.loads(${prjson@Q})
roll=j.get("statusCheckRollup") or []
if not roll:
    print("0")
    raise SystemExit
ok=True
for c in roll:
  st=c.get("status")
  conc=c.get("conclusion")
  if st in ("IN_PROGRESS","PENDING","QUEUED"):
    ok=False
    break
  if conc and conc not in ("SUCCESS","SKIPPED","NEUTRAL"):
    ok=False
    break
print("1" if ok else "0")
PY
)"

      [[ "$all_good" == "1" ]] || continue

      echo "[moltbot] merging PR #$num"
      run_and_log "gh pr merge $num --repo $REPO_SLUG --merge --delete-branch"
    done
fi

if [[ "$STASHED" == "1" ]]; then
  echo "[moltbot] restoring stashed changes"
  git stash pop >/dev/null || true
fi

echo "[moltbot] $(date -Iseconds) done"
