# VolatilX Research Desk — Standalone Repo Setup (Windows / VS Code)

A separate repo, `volatilx-research`, where Claude Code agents research the platform and your
trading. The platform repo stays untouched: the desk **reads** it (code, docs, git history),
reads the **production DB** through a read-only role, reads **Azure Blob** through a read-only
token, and writes only inside this repo. Findings that should change the platform come out as
implementation briefs you run in the platform repo with your coding agent. Findings that are
trading rules go into `playbook/`.

```
C:/Users/sahin/Projects/
├── volatilx/                    ← platform repo (untouched, read-only from the desk)
└── volatilx-research/           ← THIS repo
    ├── CLAUDE.md                ← rules every agent reads
    ├── .claude/ agents/ hooks/ skills/ settings.json
    ├── research/ lib/ data/ questions/ reports/ templates/ BACKLOG.md LEDGER.md
    ├── playbook/                ← your trading rules that survived review
    ├── docs/                    ← anything human-written for the desk
    ├── scripts/                 ← db role SQL, Azure SAS, routines, second_opinion.py
    └── .env.research            ← research credentials only (gitignored)
```

---

## Step 1 — Create the repo (5 min)

```powershell
mkdir C:\Users\sahin\Projects\volatilx-research
cd C:\Users\sahin\Projects\volatilx-research
# unzip the kit here so CLAUDE.md, .claude/, research/, scripts/, playbook/ sit at this level
git init
copy .gitignore.append .gitignore
git add -A
git commit -m "research desk v3"
```

Open this folder in a **new VS Code window**. Claude Code in its terminal uses this folder's
`.claude/` and `CLAUDE.md` — nothing from the platform repo's settings applies here.

## Step 2 — Point the desk at the platform code, read-only (5 min)

`.claude/settings.json` already lists `C:/Users/sahin/Projects/volatilx` under
`additionalDirectories` (read) and denies `Edit`/`Write` into it. The bash guard additionally
blocks redirects, `sed -i`, `cp`, `mv`, `rm`, and any non-read-only `git` command aimed at it.
Set the path in your env so the guard and the freeze script know it:

```
CODEBASE_DIR=C:/Users/sahin/Projects/volatilx
```

**Should agents read the codebase? Yes, deliberately.** `services/super_agent_select_scoring.py`
is the only true definition of every subscore; `docs/` holds the audit chain and exposure
policy; `git log` tells the Steward when an engine version changed. Hypotheses and briefs must
cite `path:line`. What agents may not do is change it.

## Step 3 — Credentials (45 min, you)

1. **Read-only DB role** — run `scripts/db/create_research_ro_role.sql` once as the DB owner.
   Check: an `UPDATE … WHERE 1=0` as that role fails with *permission denied*.
2. **Azure** — `scripts/azure/research_sas.sh` (Git Bash) creates a `research` container and
   prints two SAS tokens: prod read+list, research read/write.
3. Create `.env.research` (never `.env`; the desk is denied from reading `.env*` anyway):

```
RESEARCH_DB_URL=postgresql://research_ro:...@host:5432/volatilx?sslmode=require
CODEBASE_DIR=C:/Users/sahin/Projects/volatilx
PROD_BLOB_ENDPOINT=https://<account>.blob.core.windows.net
RESEARCH_CONTAINER=research
PROD_EARNINGS_PREFIX=...
PROD_REPORTS_PREFIX=...
PROD_SAS_TOKEN=...
RESEARCH_SAS_TOKEN=...
OPENAI_API_KEY=sk-...
OPENAI_REVIEW_MODEL=gpt-6-astra
DISCORD_WEBHOOK=
```

Python deps in this repo's venv: `pip install psycopg[binary] pandas pyarrow scipy azure-storage-blob openai`

## Step 4 — Launch and prove the guards work (5 min) — do not skip

In the VS Code terminal (Git Bash):

```bash
cd /c/Users/sahin/Projects/volatilx-research
set -a; . ./.env.research; set +a
claude
```

Then type: `@data-steward run: python research/lib/db.py "UPDATE users SET id=id"`
You must see **BLOCKED by guard_bash**. If you see a hook *error* mentioning `python`, the
interpreter wasn't found and hooks are silently non-blocking: edit the `command:` lines in
`.claude/settings.json` and each `.claude/agents/*.md` to your venv's full `python.exe` path.

Second check: `@researcher run: echo x > $CODEBASE_DIR/README.md` → must be BLOCKED.

## Step 5 — Hand the setup to Claude Code

Paste:

> Read SETUP_README.md. Steps 1–4 are done; research credentials and CODEBASE_DIR are in the
> shell environment. Do Step 6 (freeze), 7 (controller + PREREG review), and stop before
> Step 8 so I can lock Q001 myself. Cite platform code as path:line whenever you describe a column.

## Step 6 — Freeze the first dataset (Steward)

`@data-steward` inspects schemas with `python research/lib/db.py --describe <table>`, corrects
the SQL in `research/lib/freeze_config.json`, freezes `manifest_v001.json` (parquet + SHA-256,
platform git SHA recorded), and reports coverage, T+10 and W60 maturation cutoffs, null-ladder
share, and which non-qualified candidates lack outcome grading.

## Step 7 — Controller + Q001 review

```bash
python research/lib/controller.py init Q001 --by haci
python research/lib/controller.py advance Q001 PREREG_DRAFT --by registrar
```

Read `research/questions/Q001_control_cohort/PREREG.md`. **Decide the MPE in §5** (placeholder
0.50% net per 10 sessions). Edit anything you disagree with.

## Step 8 — Lock and run

```bash
git add research/questions/Q001_control_cohort/PREREG.md && git commit -m "PREREG Q001 locked"
python research/lib/controller.py advance Q001 PREREG_LOCKED --by haci
```
Then in Claude Code: `@data-steward advance Q001 DATASET_PINNED` → `@researcher run Q001` →
`python research/lib/controller.py advance Q001 VALIDATED` → `@red-team review Q001` →
`@reporter write Q001`. Each step refuses to run if the previous one didn't complete.

## Step 9 — What happens with a finding

- **Platform change:** you `advance QNNN HUMAN_APPROVED --by haci` → `@brief-writer` produces
  `IMPLEMENTATION_BRIEF.md` (flag-off, shadow column, inertness hashes, tests, rollback) → you run
  it in the platform repo with your coding agent → `advance QNNN IMPLEMENTED_FLAG_OFF --by haci
  --note "PR #… sha before=… after=…"` → Steward grades the shadow column ≥30 nights →
  `SHADOW_VALIDATED` → you `RELEASE_APPROVED` → flip the flag.
- **Trading rule for you:** the Reporter writes `playbook/PB-NNN_slug.md` with the rule, n, CI,
  regime caveats and `Status: HISTORICAL — trade small until PROSPECTIVELY_CONFIRMED`.
- **Null:** ledgered. Tells you what not to build and not to market.

## Step 10 — Routines (Windows Task Scheduler)

```powershell
schtasks /Create /TN "VolatilX Research Daily" /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 17:45 ^
  /TR "\"C:\Program Files\Git\bin\bash.exe\" -lc \"cd /c/Users/sahin/Projects/volatilx-research && set -a && . ./.env.research && set +a && ./scripts/research_routines.sh daily\""
schtasks /Create /TN "VolatilX Research Weekly" /SC WEEKLY /D SAT /ST 07:00 ^
  /TR "\"C:\Program Files\Git\bin\bash.exe\" -lc \"cd /c/Users/sahin/Projects/volatilx-research && set -a && . ./.env.research && set +a && ./scripts/research_routines.sh weekly\""
```

## Following the work

`/desk-status` in Claude Code (or `python research/lib/status.py --full`): every question's
state and verdict, backlog counts, RED flags, ledger rows, guard blocks. Ideas in
`research/BACKLOG.md`; a question's life in `research/questions/QNNN_*/` (PREREG → results →
REDTEAM → REPORT → BRIEF); verdicts in `research/LEDGER.md`; your rules in `playbook/`; every
guarded command in `research/reports/hook_audit.log`; every change in `git log`.

Saturday ritual (30 min): `/desk-status` → new REPORTs → weekly report → pick backlog items for
the Registrar → review/commit PREREG drafts. Only you can advance HUMAN_APPROVED,
IMPLEMENTED_FLAG_OFF and RELEASE_APPROVED.

## Order of questions

Q001 control cohort → Q002 band monotonicity → Q003 layer ablation → Q004 GEX alignment →
Q005 confidence calibration → Q006 near-miss cohort → Q007 day-1 gap → *then* weight sweep.
