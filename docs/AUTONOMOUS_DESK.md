# The autonomous desk — what runs by itself, what is still yours

**2026-09-14 update:** The board now starts with internal evidence cards, learning work and
explicit readiness categories. Read [LEARNING_POLICY.md](../research/LEARNING_POLICY.md).
Due studies and urgent integrity fixes lead the cycle; one bounded learning task precedes
discretionary registration. Future schedules distinguish actual attrition from maturation.
The schedule audit proposes planning scenarios without moving locked dates. Internal evidence
does not authorize a subscriber claim or production change.

**The short version.** The desk now works the backlog on its own: it takes the next hypothesis,
drafts the question, settles every pre-registration decision from the rulebook, locks it, pins
the data, waits for the decision date, runs the evaluation once, red-teams it, and writes the
verdict, the ledger row and the lists. Every decision it made on your behalf is listed on
`research/BOARD.md` §7 so you can overturn it. You do four things: read the board; ask for a
prompt (`/desk-run prompt PI-011`); implement it and say so (`/desk-run verify PI-011 <sha>`);
and type the three controller commands nobody else may type. To make it run overnight, apply
`docs/admin_pass/patch6.py` and register one more scheduled task (below).

---

## What changed for you

| Before (2026-09-12) | Now |
|---|---|
| Answer 1–5 questions per PREREG | None. The desk decides by `DECISION_POLICY.md` DP-40..48 and shows each decision on the board. `--ask` brings the questions back for one run. |
| `git commit` the PREREG, then `advance PREREG_LOCKED --by haci` | The desk commits and locks (`--by desk`, DP-46). A lock is still a commit; a locked file is still never edited. |
| `@data-steward advance DATASET_PINNED` | The desk, in the same cycle. |
| Remember every decision date | `schedule.json` in each question folder; `research/lib/desk_queue.py` says what is due; the desk runs it on the date. |
| Mark an issue fix / research / accept, then `@brief-writer fix-brief` | Ask for the prompt: `/desk-run prompt PI-NNN`. Asking *is* the decision (DP-48). |
| Check a fix by hand after implementing | `/desk-run verify PI-NNN <sha>` — the steward runs the brief's before/after check and writes PASS or FAIL. |
| HUMAN_APPROVED, IMPLEMENTED_FLAG_OFF, RELEASE_APPROVED | Still yours. The controller refuses them from anyone else, and that does not change. |
| Ideas by conversation | `research/INBOX.md` (one line each) or `/desk-run idea "…"`. They jump the queue. |

Nothing in CLAUDE.md rules 1–15 changed. Pre-registration before data, frozen data only, nights
as the unit, regime stratification, four verdicts, no judgment in the inner loop — all as before.
The desk is autonomous about *process*, not about *evidence*.

## The board and the lists

`research/BOARD.md` is generated (`python research/lib/board.py`) at the end of every desk run
and by the nightly daily-check, from these files:

| Section | Source file | What it is |
|---|---|---|
| 1. Waiting on you | queue | Only the items that need you, each with the exact command. "Ready when you ask" lists issues you already marked `fix`. |
| 2. Results | `research/LEDGER.md` | Every verdict on record, one line each. |
| 3. Edges | LEDGER + `playbook/` | Proven edges (none yet), and the candidate edges under test with their decision dates. |
| 4. Platform issues | `research/PLATFORM_ISSUES.md` | Defects. Lifecycle: OPEN → HACI_DECIDED → BRIEF_WRITTEN → IMPLEMENTED:<sha> → VERIFIED. |
| 5. Enhancements | `research/ENHANCEMENTS.md` | Things the platform could do. `plumbing` builds now; `behaviour` waits for its gate question, or ships as a flag-off internal tool. |
| 6. Trade ideas | `research/TRADE_IDEAS.md` | Your list: IDEA → UNDER_TEST:QNNN → HISTORICAL → PROSPECTIVE, or KILLED. Each can become an internal tool. |
| 7. Decisions the desk made | each `DECISIONS.md` | Every DEFAULTED item, with the option not taken. |
| 8. Backlog and calendar | `research/BACKLOG.md`, `schedule.json` | What is next, and when each question decides. |

## Running it

**By hand, in a desk session** (`./scripts/start_desk.sh`):

```
/desk-run                              # one full cycle (default: at most 2 new questions)
/desk-run cycle --max-register 5       # drain more of the backlog in one sitting
/desk-run due                          # only what is due today (+ pins, board)
/desk-run register H-062               # one hypothesis end to end
/desk-run prompt EN-001                # write the prompt for an enhancement (or PI-/TI-/Q-)
/desk-run verify EN-001 <sha>          # check it after you implemented it
/desk-run idea "…"                     # file an idea and register it first
/desk-run board                        # regenerate the board only
```

Each new question costs four or five opus subagent runs (registrar, decision-maker twice,
steward, registrar again) — roughly 30–60 minutes of wall clock and a few dollars. A verdict run
(freeze, eval, red team, report) is similar. That is why `--max-register` defaults to 2 by hand
and 1 overnight.

**Overnight** — the third scheduled task, after you apply patch6. In PowerShell (not Git Bash):

```powershell
$action = New-ScheduledTaskAction -Execute 'C:\Program Files\Git\bin\bash.exe' `
  -Argument '-lc "cd /c/Users/sahin/OneDrive/Desktop/VolatilX_Research_Desk && ./scripts/research_routines.sh desk >> logs/desk-$(date +%F).log 2>&1"' `
  -WorkingDirectory 'C:\Users\sahin\OneDrive\Desktop\VolatilX_Research_Desk'
$trigger  = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 19:30
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 4) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName 'VolatilX Research Desk' -Action $action -Trigger $trigger -Settings $settings `
  -Description 'Autonomous desk cycle (/desk-run). Regenerates research/BOARD.md; commits and pushes.'
```

Knobs, in `.env.research` or the environment: `DESK_MAX_REGISTER` (default 1 new question per
night), `DESK_MAX_TURNS` (400), `DESK_MAX_BUDGET` (USD 40 — remove the `--max-budget-usd` flag
from the script if your Claude Code version rejects it). The run's transcript lands in
`logs/desk-run-<date>.out`; the board's "Waiting on you" section is posted to Discord if
`DISCORD_WEBHOOK` is set. The computer must be awake and you logged in, as for the other two
tasks (`docs/RUN_ROUTINES_MANUALLY.md` has the wake-timer fix).

## What the desk decides for you, and how to overturn it

The rules are `DECISION_POLICY.md` DP-40..48. In one line each: it never asks before lock
(DP-40); it never grants a new knowledge-time exception — it defers the question instead (DP-41);
it uses the levels, lanes and entry bases already locked in Q002–Q010 (DP-42); it picks the
window that reaches every sample floor, never the shorter one, and defers anything that would
take more than 12 months (DP-43); it reuses your MPEs and never invents a money-unit one (DP-44);
when it cannot decide without hedging it takes the option *less* likely to confirm (DP-45); it
locks and pins (DP-46); it registers in a fixed order — your inbox first (DP-47); and it treats
your request for a prompt as your approval (DP-48).

To overturn one: the locked question stands (rule 3), so say what you want — "the desk chose
20 sessions for Q011; I trade 10" — and the desk registers a successor question with your
choice. To change a rule for every future question, edit the DP row in place, with the date.

## What to apply (you; enforcement and human files)

```bash
python docs/admin_pass/patch6.py --check     # shows the ten changes, writes nothing
python docs/admin_pass/patch6.py --apply
```

It installs the `/desk-run` skill, the autonomous-mode Decision-maker, adds short sections to the
Registrar (merge / defer / schedule.json), Data Steward (successor freezes; verification),
Brief Writer (EN-/TI- briefs, INTERNAL_TOOL), Reporter (update the lists), Explorer
(enhancements go to ENHANCEMENTS.md), adds an "Autonomous mode" paragraph to CLAUDE.md, replaces
`scripts/research_routines.sh` with the version that has the `desk` mode (old one kept as
`.bak`), and makes one small controller change: when a locked PREREG's header names no manifest
*file* (Q010, whose freezes can only exist at its decision date) the controller reads
`manifests.json` from the question folder, written by the steward. Checksums are still verified.

## Tested today (2026-09-13), and not

- `desk_queue.py` and `board.py` run; the board is committed.
- The desk pinned Q008 (`--by desk`). The identical command for Q009 was refused by the
  permission classifier in this session, not by the desk's own guards — run it yourself once:
  `python research/lib/controller.py advance Q009 DATASET_PINNED --by desk`.
- Q010 cannot be pinned until its decision date (its header names no file); patch6's controller
  fallback is what will let the steward pin it then. Until patch6 is applied it stays
  PREREG_LOCKED, which the queue treats as in flight.
- The first autonomous registration ran end to end on H-058 → **Q011 day-1 dip limit**:
  registrar draft (7 open decisions) → decision-maker (14 decided, 2 defaulted under DP-43, none
  asked) → steward exposure count (369 eligible picks, 47 contributing nights, both limit arms
  clear the 20-night floor) → decision-maker record (decision date 2026-12-14, extension
  2027-02-01) → registrar apply → desk commit → `PREREG_LOCKED --by desk` → `DATASET_PINNED`.
  Zero questions to Haci. Evidence: `research/questions/Q011_day1_dip_limit/DECISIONS.md`
  and board §7.
- **Not tested:** the headless `desk` mode of the routine script. This session had no
  `RESEARCH_DB_URL`, and sourcing `.env.research` is denied to it, so the scheduled run was not
  exercised end to end. Run `./scripts/research_routines.sh desk` once by hand from Git Bash
  before trusting the schedule, and read `logs/desk-run-<date>.out`.
