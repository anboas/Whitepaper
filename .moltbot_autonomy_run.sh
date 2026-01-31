#!/usr/bin/env bash
set -euo pipefail
cd /home/anboas/clawd/Whitepaper

mkdir -p logs/moltbot-autonomy

TS=$(date -Is)
export TS
LOGTMP=$(mktemp)

export OPENAI_API_KEY="$(cat /home/anboas/.secrets/openai_api_key)"
if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "OPENAI_API_KEY empty" >&2
  exit 2
fi
export MOLTBOT_MAX_PRS_PER_RUN=2

echo "[$TS] running moltbot_autonomy.py" | tee "$LOGTMP"
set +e
python3 scripts/moltbot_autonomy.py --repo anboas/Whitepaper 2>&1 | tee -a "$LOGTMP"
CODE=${PIPESTATUS[0]}
export CODE
set -e

if [ "$CODE" -ne 0 ]; then
  TB=$(python3 - "$LOGTMP" <<'PY'
import sys
p=sys.argv[1]
with open(p,'r',encoding='utf-8',errors='replace') as f:
    lines=f.read().splitlines()
start=None
for i,l in enumerate(lines):
    if l.startswith('Traceback (most recent call last):'):
        start=i
if start is not None:
    text='\n'.join(lines[start:])
else:
    text='\n'.join(lines[-120:])
print(text)
PY
)
export TB

  python3 - <<PY
import json,os
path='logs/moltbot-autonomy/errors.jsonl'
os.makedirs(os.path.dirname(path), exist_ok=True)
entry={
  'ts': os.environ.get('TS'),
  'repo': 'anboas/Whitepaper',
  'command': 'python3 scripts/moltbot_autonomy.py --repo anboas/Whitepaper',
  'exit_code': int(os.environ.get('CODE','0')),
  'error': os.environ.get('TB','')
}
with open(path,'a',encoding='utf-8') as f:
  f.write(json.dumps(entry,ensure_ascii=False))
  f.write('\n')
PY

  echo "Autonomy run failed (exit $CODE); logged to logs/moltbot-autonomy/errors.jsonl" >&2
  rm -f "$LOGTMP" || true
  exit "$CODE"
fi

rm -f "$LOGTMP"
