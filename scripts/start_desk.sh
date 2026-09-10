#!/usr/bin/env bash
# Launch the research desk with credentials loaded, from Git Bash on Windows.
#
# Why winpty: the Claude Code binary is a native Windows console .exe. Started from an
# MSYS/MinGW shell its stdin is a pipe, not a console, so it sees no TTY, falls back to
# --print mode, and exits with:
#   "Error: Input must be provided either through stdin or as a prompt argument"
# winpty gives it a real console. From PowerShell or cmd this is unnecessary.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env.research ]; then
  echo "no .env.research in $(pwd) — see README Step 3" >&2
  exit 1
fi
set -a; . ./.env.research; set +a

: "${RESEARCH_DB_URL:?RESEARCH_DB_URL not set after sourcing .env.research}"

# Deliberate maintenance mode: ./scripts/start_desk.sh --admin
# Only then may enforcement code (.claude/, controller, validators, freeze) be edited.
if [ "${1:-}" = "--admin" ]; then
  export DESK_ADMIN=1
  shift
  echo "DESK_ADMIN=1 — enforcement code is writable this session."
fi

if command -v winpty >/dev/null 2>&1 && [ ! -t 0 ]; then
  exec winpty claude "$@"
fi
exec claude "$@"
