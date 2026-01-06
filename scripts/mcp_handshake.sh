#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"
MCP_PATH="${MCP_PATH:-/mcp}"
URL="${BASE_URL}${MCP_PATH}"

ACCEPT_HEADER='Accept: application/json, text/event-stream'
CONTENT_HEADER='Content-Type: application/json'

echo "==> Initializing: ${URL}"

# 1) initialize and capture mcp-session-id from response headers
SESSION_ID="$(
  curl -i -sS -N \
    -H "$ACCEPT_HEADER" \
    -H "$CONTENT_HEADER" \
    -X POST "$URL" \
    --data-binary '{
      "jsonrpc":"2.0",
      "id":1,
      "method":"initialize",
      "params":{
        "protocolVersion":"2025-03-26",
        "capabilities":{"tools":{},"resources":{},"prompts":{}},
        "clientInfo":{"name":"bash-curl","version":"0.0.1"}
      }
    }' \
  | tr -d '\r' \
  | awk -F': ' 'tolower($1)=="mcp-session-id"{print $2; exit}'
)"

if [[ -z "${SESSION_ID}" ]]; then
  echo "ERROR: Could not parse mcp-session-id from initialize response headers"
  exit 1
fi

echo "==> Session: ${SESSION_ID}"

# Helper: POST with session and print only SSE 'data: {...}' JSON payloads
mcp_post() {
  local payload="$1"
  curl -sS -N \
    -H "$ACCEPT_HEADER" \
    -H "$CONTENT_HEADER" \
    -H "mcp-session-id: ${SESSION_ID}" \
    -X POST "$URL" \
    --data-binary "$payload" \
  | sed -n 's/^data: //p'
}

# 2) notifications/initialized
echo "==> Sending notifications/initialized"
mcp_post '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' >/dev/null || true

# 3) tools/list
echo "==> tools/list"
mcp_post '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
