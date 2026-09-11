#!/usr/bin/env bash
# Third maintenance pass. RUN IN YOUR OWN GIT BASH, not from inside Claude Code.
#
#   cd "/c/Users/sahin/OneDrive/Desktop/VolatilX_Research_Desk"
#   bash docs/admin_pass/apply3.sh
#
# 1. Daily check: the three flag rules (minimum movement, seen-before = OK, RED vs AMBER)
#    now live in a deterministic script, research/lib/daily_check.py. The skill runs it;
#    the scheduled routine runs it directly. Backtest over 13 nights: 10 ALL CLEAR,
#    3 RED nights, 1 AMBER — the old check produced 7-8 RED every night.
# 2. Guards: Alpaca trading servers, SDK and order/position/account routes are blocked.
#    The Alpaca key pair can place orders, not just read prices. Market data
#    (data.alpaca.markets) stays allowed. 44-case suite.
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "repo: $(pwd)"
echo

# --- 1a. daily-check skill -------------------------------------------------------------
cp .claude/skills/daily-check/SKILL.md .claude/skills/daily-check/SKILL.md.bak
cp docs/admin_pass/daily-check.SKILL.md .claude/skills/daily-check/SKILL.md
echo "installed: .claude/skills/daily-check/SKILL.md (backup: SKILL.md.bak)"

# --- 1b. routine: daily runs the script directly ---------------------------------------
python - <<'PY'
import pathlib, re, sys
p = pathlib.Path("scripts/research_routines.sh")
s = p.read_text(encoding="utf-8")
if "research/lib/daily_check.py" in s:
    print("unchanged: routine already runs daily_check.py")
    sys.exit(0)
new = ('    # Deterministic check (research/lib/daily_check.py): no LLM needed for a mechanical\n'
       '    # comparison, same answer every run, seconds instead of ~20 minutes.\n'
       '    python research/lib/daily_check.py > "research/reports/daily/$(date +%F).md"')
s2, n = re.subn(r'    claude -p "/daily-check.*?\n\s*> "research/reports/daily/\$\(date \+%F\)\.md"',
                lambda m: new, s, count=1, flags=re.S)
if n != 1:
    sys.exit("could not find the daily claude invocation in research_routines.sh")
p.write_text(s2, encoding="utf-8")
print("updated:   scripts/research_routines.sh (daily -> daily_check.py)")
PY
bash -n scripts/research_routines.sh && echo "syntax OK"

# --- 2. guards ---------------------------------------------------------------------------
cp .claude/hooks/guard_bash.py  .claude/hooks/guard_bash.py.bak
cp .claude/hooks/guard_write.py .claude/hooks/guard_write.py.bak
cp docs/guard_patches/guard_bash.py  .claude/hooks/guard_bash.py
cp docs/guard_patches/guard_write.py .claude/hooks/guard_write.py
echo "installed: guards (backups: *.py.bak)"
echo
python docs/guard_patches/test_guards.py --installed | tail -1

# --- verify the routine end to end ------------------------------------------------------
echo
echo "--- running the daily routine once ---"
./scripts/research_routines.sh daily
head -3 "research/reports/daily/$(date +%F).md"
echo
echo "Done. Review with: git diff"
