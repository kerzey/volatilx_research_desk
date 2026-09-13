#!/usr/bin/env bash
# Headless research routines. Usage: ./scripts/research_routines.sh daily|weekly|desk
#
#   daily   deterministic operational check (research/lib/daily_check.py)     Mon–Fri 17:45
#   weekly  descriptive performance snapshot (/weekly-performance skill)       Sat 07:00
#   desk    autonomous desk cycle (/desk-run skill): registers and locks       Mon–Fri 19:30
#           backlog hypotheses, runs due questions, regenerates research/BOARD.md
#
# Installed by docs/admin_pass/patch6.py (source copy: docs/admin_pass/research_routines.sh).
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
# desk-run coordinates subagents (Agent), runs the controller, commits and pushes. Subagents keep
# the tools: list in their own frontmatter; guard_bash / guard_write run on every call in -p mode.
DESK_TOOLS='Agent,Read,Grep,Glob,Write,Edit,Bash(python*),Bash(git add research/*),Bash(git add docs/*),Bash(git add playbook/*),Bash(git commit*),Bash(git push origin master*),Bash(git status*),Bash(git log*),Bash(git diff*),Bash(ls*),Bash(cat research/*),Bash(psql $RESEARCH_DB_URL*),Bash(sha256sum*),Bash(wc*)'

SUMMARY=""
case "$MODE" in
  daily)
    # Deterministic check (research/lib/daily_check.py): no LLM needed for a mechanical
    # comparison, same answer every run, seconds instead of ~20 minutes.
    python research/lib/daily_check.py > "research/reports/daily/$(date +%F).md"
    REPORT="research/reports/daily/$(date +%F).md"
    # keep the board's calendar fresh even on days the desk cycle does not run
    python research/lib/board.py >/dev/null 2>&1 || true ;;
  weekly)
    claude -p "/weekly-performance\n\nHeadless run: print the finished report to stdout - the caller redirects stdout to research/reports/weekly/<date>.md, so do not write that file yourself. The one file you may edit is research/BACKLOG.md, to append hypotheses as the skill describes. Commit nothing. Begin with the report itself; no preamble about tooling or access." --allowedTools "$WEEKLY_TOOLS" --output-format text \
      > "research/reports/weekly/$(date +%F).md"
    REPORT="research/reports/weekly/$(date +%F).md" ;;
  desk)
    # Bounded autonomous cycle. Knobs (set in .env.research or the environment):
    #   DESK_MAX_REGISTER  new questions per run (default 1 — each is 4–5 opus subagent calls)
    #   DESK_MAX_TURNS     agentic turns before the run stops (default 400)
    #   DESK_MAX_BUDGET    USD ceiling for the run (default 40); remove the flag if your
    #                      Claude Code version rejects --max-budget-usd
    claude -p "/desk-run cycle --max-register ${DESK_MAX_REGISTER:-1}\n\nHeadless run: nobody is watching. Never ask a question (DP-40). Follow the skill exactly, commit as it says, push at the end, and finish with the board's 'Waiting on you' section verbatim." \
      --allowedTools "$DESK_TOOLS" --permission-mode acceptEdits \
      --max-turns "${DESK_MAX_TURNS:-400}" --max-budget-usd "${DESK_MAX_BUDGET:-40}" \
      --output-format text > "logs/desk-run-$(date +%F).out" || echo "desk-run exited $? (see logs/desk-run-$(date +%F).out)"
    python research/lib/board.py >/dev/null 2>&1 || true
    REPORT="research/BOARD.md"
    SUMMARY=$(sed -n '/^## 1. Waiting on you/,/^## 2\./p' "$REPORT" | grep -v '^## 2\.' | head -25 || true) ;;
  *) echo "unknown mode $MODE"; exit 1 ;;
esac

# Post to Discord if a webhook is configured: RED / ALL CLEAR lines for daily and weekly,
# the board's "Waiting on you" section for desk.
if [ -n "${DISCORD_WEBHOOK:-}" ]; then
  if [ -z "$SUMMARY" ]; then
    SUMMARY=$(grep -E '^(RED|ALL CLEAR)' "$REPORT" | head -20 || true)
  fi
  [ -z "$SUMMARY" ] && SUMMARY="Report written: $REPORT (no RED/ALL CLEAR lines found — inspect)"
  python - "$DISCORD_WEBHOOK" "$SUMMARY" "$MODE" << 'PY'
import json, sys, urllib.request
url, text, mode = sys.argv[1], sys.argv[2], sys.argv[3]
req = urllib.request.Request(url, data=json.dumps({"content": f"**Research desk — {mode}**\n```\n{text[:1800]}\n```"}).encode(),
                             headers={"Content-Type": "application/json"})
urllib.request.urlopen(req, timeout=15)
PY
fi
