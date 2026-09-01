#!/usr/bin/env bash
# 共绩算力 Open API 调用（简易模式：仅需 token，无需 sign_str）
set -euo pipefail

BASE="${SUANLI_BASE_URL:-https://openapi.suanli.cn}"
TOKEN="${SUANLI_TOKEN:?请设置 SUANLI_TOKEN}"

method="${1:?用法: call.sh GET|POST /path [query_or_body]}"
path="${2:?缺少 path，如 /storage/nas/v1/list}"
payload="${3:-}"

if [[ "$path" != /* ]]; then path="/$path"; fi

ts=$(python3 -c 'import time; print(int(time.time()*1000))' 2>/dev/null || echo $(($(date +%s)*1000)))

hdr=(
  -H "token: $TOKEN"
  -H "timestamp: $ts"
  -H "version: 1.0.0"
)

if [[ "$method" == "GET" ]]; then
  url="$BASE/api$path"
  [[ -n "$payload" ]] && url="$url?$payload"
  curl -sS "$url" "${hdr[@]}"
elif [[ "$method" == "POST" ]]; then
  body="$payload"
  if [[ "$payload" == @* ]]; then
    body="$(cat "${payload#@}")"
  fi
  curl -sS -X POST "$BASE/api$path" "${hdr[@]}" \
    -H "Content-Type: application/json" \
    -d "$body"
else
  echo "method 须为 GET 或 POST。加密接口请用 scripts/call_encrypt.py" >&2
  exit 1
fi
