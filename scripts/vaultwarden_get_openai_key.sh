#!/usr/bin/env bash
set -euo pipefail

# Fetch OPENAI_API_KEY from Vaultwarden/Bitwarden via bw CLI.
#
# Requirements:
# - bw CLI installed (npm i -g @bitwarden/cli)
# - Vaultwarden URL set: BW_HOST (e.g. https://localhost:8222)
# - Credentials provided via env OR local secret files:
#     BW_EMAIL and BW_PASSWORD
#   Recommended: set BW_EMAIL in cron payload and store BW_PASSWORD in /home/anboas/.secrets/bw_password
# - A vault item exists containing the OpenAI key.
#
# How we locate the secret:
# - Search term: $VAULT_OPENAI_SEARCH (default: OPENAI_API_KEY)
# - If item has login.password, use it.
# - Else look for a custom field named OPENAI_API_KEY.

BW_HOST=${BW_HOST:-}
if [[ -z "$BW_HOST" ]]; then
  echo "BW_HOST not set" >&2
  exit 2
fi

BW_EMAIL=${BW_EMAIL:-}
if [[ -z "$BW_EMAIL" ]]; then
  echo "BW_EMAIL not set" >&2
  exit 2
fi

BW_PASSWORD=${BW_PASSWORD:-}
if [[ -z "$BW_PASSWORD" && -f /home/anboas/.secrets/bw_password ]]; then
  BW_PASSWORD=$(cat /home/anboas/.secrets/bw_password)
fi
if [[ -z "$BW_PASSWORD" ]]; then
  echo "BW_PASSWORD not set (and /home/anboas/.secrets/bw_password missing)" >&2
  exit 2
fi

SEARCH=${VAULT_OPENAI_SEARCH:-OPENAI_API_KEY}
FALLBACK_FILE=/home/anboas/.secrets/openai_api_key

# Allow self-signed certs if requested (Vaultwarden local TLS).
# WARNING: only safe for localhost / trusted LAN.
if [[ "${BW_INSECURE:-}" == "1" ]]; then
  export NODE_TLS_REJECT_UNAUTHORIZED=0
fi

# Ensure a clean state (bw refuses server change while logged in)
bw logout --quiet >/dev/null 2>&1 || true

# Configure server
bw config server "$BW_HOST" >/dev/null

# Login non-interactively and capture session
BW_SESSION=$(bw login "$BW_EMAIL" "$BW_PASSWORD" --raw --nointeraction 2>/dev/null || true)
if [[ -z "$BW_SESSION" ]]; then
  # If already logged in, unlock.
  BW_SESSION=$(bw unlock "$BW_PASSWORD" --raw --nointeraction 2>/dev/null || true)
fi
if [[ -z "$BW_SESSION" ]]; then
  echo "Failed to login/unlock via bw" >&2
  exit 3
fi

export BW_SESSION
bw sync >/dev/null || true

pick_first() {
  # NOTE: we must not use a here-doc for the python source here, because that
  # consumes stdin (and we need stdin for the JSON pipe).
  python3 -c 'import json,sys; items=json.loads(sys.stdin.read() or "[]");
if not items: raise SystemExit(1);
print(json.dumps(items[0]))'
}

item=""
for term in "$SEARCH" "openai" "OpenAI" "OpenAI API" "api key"; do
  items_json=$(bw list items --search "$term" --session "$BW_SESSION" 2>/dev/null || echo '[]')
  item=$(echo "$items_json" | pick_first 2>/dev/null || true)
  if [[ -n "$item" ]]; then
    break
  fi
done

if [[ -z "$item" ]]; then
  if [[ -f "$FALLBACK_FILE" ]] && [[ -s "$FALLBACK_FILE" ]]; then
    cat "$FALLBACK_FILE"
    exit 0
  fi
  echo "No vault items found for search: $SEARCH" >&2
  exit 4
fi

key=$(python3 -c 'import json,sys,re
it=json.loads(sys.stdin.read())
login=it.get("login") or {}
if isinstance(login, dict) and login.get("password"):
    print(login["password"]); raise SystemExit(0)
fields=it.get("fields") or []
for f in fields:
    if (f.get("name") or "").strip() == "OPENAI_API_KEY" and f.get("value"):
        print(f["value"]); raise SystemExit(0)
notes=(it.get("notes") or "").strip()
if notes.startswith("sk-"):
    print(notes); raise SystemExit(0)
m=re.search(r"(sk-[A-Za-z0-9_\-]{20,})", notes)
if m:
    print(m.group(1)); raise SystemExit(0)
raise SystemExit(2)
' <<< "$item" || true)

if [[ -z "$key" ]]; then
  echo "Found item but could not extract OPENAI_API_KEY (use login.password or a custom field named OPENAI_API_KEY)" >&2
  exit 5
fi

printf '%s' "$key"
