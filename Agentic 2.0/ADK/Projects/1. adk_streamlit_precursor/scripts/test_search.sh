#!/usr/bin/env bash
set -euo pipefail

# ---- Config (env overrides supported) ----
API_BASE="${ADK_API_BASE:-http://localhost:8000}"
APP_NAME="${ADK_APP_SIMPLE:-simple}"
USER_ID="${ADK_USER_ID:-test-user}"
SESSION_ID="test-$(date +%s)"
QUESTION="${1:-What is retrieval augmented generation?}"

echo "== Create session =="
curl -sS -X POST "$API_BASE/apps/$APP_NAME/users/$USER_ID/sessions/$SESSION_ID" \
  -H "Content-Type: application/json" -d '{}' | jq . || true

echo
echo "== Ask =="
# Build payload safely using jq (escapes quotes/newlines in $QUESTION)
PAYLOAD=$(jq -n \
  --arg app "$APP_NAME" \
  --arg user "$USER_ID" \
  --arg sid "$SESSION_ID" \
  --arg q "$QUESTION" \
  '{app_name:$app, user_id:$user, session_id:$sid, new_message:{role:"user", parts:[{text:$q}]}}')

# Capture headers and body separately to detect content-type
TMP_HDR=$(mktemp)
TMP_BODY=$(mktemp)

curl -sS -D "$TMP_HDR" -o "$TMP_BODY" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -X POST "$API_BASE/run" \
  --data "$PAYLOAD"

CT=$(grep -i '^content-type:' "$TMP_HDR" | tr -d '\r' | awk '{print tolower($0)}')

echo
echo "== Full response (debug) =="
if echo "$CT" | grep -q 'application/json'; then
  cat "$TMP_BODY" | jq . || (echo; echo "[warn] Body is not valid JSON"; cat "$TMP_BODY")
else
  # Try Server-Sent Events / NDJSON fallback
  # Extract `data: { ... }` lines, strip the prefix, and pretty print as an array
  if grep -q '^data:' "$TMP_BODY"; then
    echo "["
    sed -n 's/^data: //p' "$TMP_BODY" | sed 's/[[:space:]]*$//' | paste -sd, -
    echo "]"
  else
    # last resort: print raw
    cat "$TMP_BODY"
  fi
fi

# Helper: produce a unified JSON array of events for jq parsing below
events_from_body() {
  if echo "$CT" | grep -q 'application/json'; then
    cat "$TMP_BODY"
  else
    if grep -q '^data:' "$TMP_BODY"; then
      echo "["
      sed -n 's/^data: //p' "$TMP_BODY" | sed 's/[[:space:]]*$//' | paste -sd, -
      echo "]"
    else
      # Not JSON nor SSE; emit empty array
      echo "[]"
    fi
  fi
}

echo
echo "== Final assistant text =="
events_from_body | jq -r '
  (.. | objects | select(has("parts")) | .parts[]? | select(has("text")) | .text) // empty
' | awk 'NF{p=$0} END{print p}'

echo
echo "== Search text (queries used by tools) =="
events_from_body | jq -r '
  [
    (.. | objects | .functionCall? | .args?.query?),
    (.. | objects | .function_call? | .arguments?.query?),
    (.. | objects | .tool_request? | .arguments?.query?)
  ]
  | flatten
  | map(select(. != null and . != ""))
  | unique
  | .[]?
' || true

# Cleanup
rm -f "$TMP_HDR" "$TMP_BODY"

echo
echo "== Done =="
