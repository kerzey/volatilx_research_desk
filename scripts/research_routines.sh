#!/usr/bin/env bash
# Headless research routines. Usage: ./scripts/run_nightly_research.sh daily|weekly
set -euo pipefail
MODE="${1:-daily}"
cd "$(dirname "$0")/.."
set -a; [ -f .env ] && . ./.env; set +a
mkdir -p research/reports/daily research/reports/weekly logs

TOOLS='Read,Grep,Glob,Bash(python research/*),Bash(psql $RESEARCH_DB_URL*),Bash(ls*),Bash(cat research/*),Write'

case "$MODE" in
  daily)
    claude -p "/daily-check" --agent data-steward --allowedTools "$TOOLS" --output-format text \
      > "research/reports/daily/$(date +%F).md"
    REPORT="research/reports/daily/$(date +%F).md" ;;
  weekly)
    claude -p "/weekly-performance" --agent data-steward --allowedTools "$TOOLS" --output-format text \
      > "research/reports/weekly/$(date +%F).md"
    REPORT="research/reports/weekly/$(date +%F).md" ;;
  *) echo "unknown mode $MODE"; exit 1 ;;
esac

# Post the RED lines (or 'all clear') to Discord if a webhook is configured.
if [ -n "${DISCORD_WEBHOOK:-}" ]; then
  SUMMARY=$(grep -E '^(RED|ALL CLEAR)' "$REPORT" | head -20 || true)
  [ -z "$SUMMARY" ] && SUMMARY="Report written: $REPORT (no RED/ALL CLEAR lines found — inspect)"
  python - "$DISCORD_WEBHOOK" "$SUMMARY" << 'PY'
import json, sys, urllib.request
url, text = sys.argv[1], sys.argv[2]
req = urllib.request.Request(url, data=json.dumps({"content": f"**Research desk**\n```\n{text[:1800]}\n```"}).encode(),
                             headers={"Content-Type": "application/json"})
urllib.request.urlopen(req, timeout=15)
PY
fi
