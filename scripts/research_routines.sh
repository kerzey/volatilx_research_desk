#!/usr/bin/env bash
# Headless research routines. Usage: ./scripts/run_nightly_research.sh daily|weekly
set -euo pipefail
MODE="${1:-daily}"
cd "$(dirname "$0")/.."
set -a; [ -f .env.research ] && . ./.env.research; set +a

# Git Bash rewrites POSIX-looking arguments when passing them to a native Windows
# .exe, turning "/daily-check" into "C:/Program Files/Git/daily-check".
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'
mkdir -p research/reports/daily research/reports/weekly logs

TOOLS='Read,Grep,Glob,Bash(python research/*),Bash(psql $RESEARCH_DB_URL*),Bash(ls*),Bash(cat research/*),Write'
# weekly-performance reads the frozen parquet, which needs `python -c`;
# `Bash(python research/*)` alone matches only research/lib/*.py invocations.
WEEKLY_TOOLS='Read,Grep,Glob,Bash(python*),Bash(ls*),Bash(cat research/*),Write,Edit'

case "$MODE" in
  daily)
    # Deterministic check (research/lib/daily_check.py): no LLM needed for a mechanical
    # comparison, same answer every run, seconds instead of ~20 minutes.
    python research/lib/daily_check.py > "research/reports/daily/$(date +%F).md"
    REPORT="research/reports/daily/$(date +%F).md" ;;
  weekly)
    claude -p "/weekly-performance\n\nHeadless run: print the finished report to stdout - the caller redirects stdout to research/reports/weekly/<date>.md, so do not write that file yourself. The one file you may edit is research/BACKLOG.md, to append hypotheses as the skill describes. Commit nothing. Begin with the report itself; no preamble about tooling or access." --allowedTools "$WEEKLY_TOOLS" --output-format text \
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
