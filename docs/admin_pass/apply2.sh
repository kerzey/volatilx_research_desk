#!/usr/bin/env bash
# Second maintenance pass. RUN IN YOUR OWN GIT BASH, not from inside Claude Code.
#
#   cd "/c/Users/sahin/OneDrive/Desktop/VolatilX_Research_Desk"
#   bash docs/admin_pass/apply2.sh
#
# Three defects, all found by smoke-testing the scheduled routines. The daily job limped
# through by luck; the weekly job produced a non-report both times.
#
# 1. BROKEN SLASH COMMANDS. Git Bash rewrites any argument that looks like a POSIX path when
#    handing it to a native Windows .exe, and claude.exe is one:
#        claude -p "/weekly-performance"  ->  claude -p "C:/Program Files/Git/weekly-performance"
#    The first weekly report is literally the agent saying "this looks like a stray path
#    fragment, not an instruction". Daily only worked because the agent guessed the intent
#    from the mangled string. Verified:
#        $ python -c "import sys; print(sys.argv[1])" /weekly-performance
#        C:/Program Files/Git/weekly-performance
#        $ MSYS_NO_PATHCONV=1 python -c "import sys; print(sys.argv[1])" /weekly-performance
#        /weekly-performance
#    The scheduled tasks run through the same Git Bash, so they inherited the bug.
#
# 2. WRONG AGENT FOR THE WEEKLY JOB. The routine ran /weekly-performance as --agent
#    data-steward, whose charter ends "You do not draw conclusions about edges." With the
#    prompt fixed it correctly refused: "That's a question for @reporter - the weekly
#    performance snapshot is result interpretation, not data stewardship." The weekly job now
#    runs with no --agent (a plain session still reads CLAUDE.md and the skill). The daily
#    job keeps --agent data-steward, which its skill explicitly asks for.
#
# 3. TOOLS TOO NARROW FOR THE WEEKLY JOB. weekly-performance works from the frozen parquet,
#    but the allowlist only permitted `Bash(python research/*)` - which matches
#    `python research/lib/db.py` and nothing else. Reading a parquet needs `python -c`, so the
#    weekly job could not open its own data. Widened for the weekly invocation only; the hooks
#    and the read-only DB role still apply.
#
# Also: in a headless run the data-steward cannot write files (its `tools:` grants no Write,
# and no allowed Bash pattern permits a redirect), so it opened the daily report with an
# apology and fenced the real report in a code block. Both prompts now say print, don't write
# - the file comes from the script's own stdout redirect.
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "repo: $(pwd)"

python - <<'PY'
import pathlib, sys
p = pathlib.Path("scripts/research_routines.sh")
s = p.read_text(encoding="utf-8")
orig = s

# --- fix 1: stop MSYS mangling the slash command ---
if "MSYS_NO_PATHCONV" not in s:
    anchor = 'set -a; [ -f .env.research ] && . ./.env.research; set +a'
    if anchor not in s:
        sys.exit("could not find the env-sourcing line in research_routines.sh")
    s = s.replace(anchor, anchor + "\n\n"
                  "# Git Bash rewrites POSIX-looking arguments when passing them to a native Windows\n"
                  "# .exe, turning \"/daily-check\" into \"C:/Program Files/Git/daily-check\".\n"
                  "export MSYS_NO_PATHCONV=1\n"
                  "export MSYS2_ARG_CONV_EXCL='*'", 1)
    print("fix 1: MSYS_NO_PATHCONV export added")
else:
    print("fix 1: already applied")

# --- fix 3: a wider allowlist for the weekly job only ---
if "WEEKLY_TOOLS=" not in s:
    anchor = [ln for ln in s.splitlines() if ln.startswith("TOOLS=")]
    if not anchor:
        sys.exit("could not find the TOOLS= line")
    tools_line = anchor[0]
    s = s.replace(tools_line, tools_line + "\n"
                  "# weekly-performance reads the frozen parquet, which needs `python -c`;\n"
                  "# `Bash(python research/*)` alone matches only research/lib/*.py invocations.\n"
                  "WEEKLY_TOOLS='Read,Grep,Glob,Bash(python*),Bash(ls*),Bash(cat research/*),Write,Edit'", 1)
    print("fix 3: WEEKLY_TOOLS added")
else:
    print("fix 3: already applied")

# --- fix 2 + headless note: rewrite both invocations ---
note_daily = ("\\n\\nHeadless run: print the finished report to stdout and nothing else. Do not attempt "
              "to write, edit or commit any file - the caller redirects stdout to the report path. "
              "Begin with the RED lines; no preamble about tooling or access.")
# The weekly skill appends hypotheses to BACKLOG.md by design, so it keeps that one write.
note_weekly = ("\\n\\nHeadless run: print the finished report to stdout - the caller redirects stdout "
               "to research/reports/weekly/<date>.md, so do not write that file yourself. The one file "
               "you may edit is research/BACKLOG.md, to append hypotheses as the skill describes. Commit "
               "nothing. Begin with the report itself; no preamble about tooling or access.")

old_daily = 'claude -p "/daily-check" --agent data-steward --allowedTools "$TOOLS" --output-format text'
new_daily = f'claude -p "/daily-check{note_daily}" --agent data-steward --allowedTools "$TOOLS" --output-format text'
old_weekly = 'claude -p "/weekly-performance" --agent data-steward --allowedTools "$TOOLS" --output-format text'
new_weekly = f'claude -p "/weekly-performance{note_weekly}" --allowedTools "$WEEKLY_TOOLS" --output-format text'

if old_daily in s:
    s = s.replace(old_daily, new_daily, 1); print("fix: daily invocation updated")
else:
    print("fix: daily invocation already updated")
if old_weekly in s:
    s = s.replace(old_weekly, new_weekly, 1); print("fix 2: weekly invocation updated (no --agent, wider tools)")
else:
    print("fix 2: weekly invocation already updated")

if s != orig:
    p.write_text(s, encoding="utf-8")
    print("written: scripts/research_routines.sh")
PY

bash -n scripts/research_routines.sh && echo "syntax OK"
echo
echo "Re-test with:  ./scripts/research_routines.sh weekly   (then daily)"
echo "Review with:   git diff scripts/research_routines.sh"
