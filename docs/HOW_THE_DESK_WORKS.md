# How to use the research desk — Haci's guide

One page. Where things are, who does what, and what *you* do versus what the agents do.

## The idea in one paragraph

The desk turns "I think SAS picks do X" into a verdict you can defend. It does that by writing
the question down *before* looking at the answer (pre-registration), computing the answer with a
script rather than an opinion, having an adversary check the script, and only then recording a
verdict. Most questions come back NULL or INCONCLUSIVE. That is the desk working: it tells you
what not to build and what not to market.

## The four things that move through the desk

| Thing | Lives in | Owned by |
|---|---|---|
| **Hypotheses** — ideas, grouped in families | `research/BACKLOG.md` | Explorer writes, you pick |
| **Questions** — one locked PREREG, one eval.py, one verdict | `research/questions/QNNN_*/` | Registrar drafts, you lock, Researcher runs |
| **Verdicts** — the permanent memory | `research/LEDGER.md` | Reporter writes after Red Team signs |
| **Platform issues** — bugs and hazards, with their fix status | `research/PLATFORM_ISSUES.md` | Steward/Explorer find, you decide |

Plus two routine outputs that need nobody: the **daily check** (weekdays 17:45,
`research/reports/daily/`) and the **weekly snapshot** (Saturday 07:00, `research/reports/weekly/`).
If the computer was asleep and they didn't run: `docs/RUN_ROUTINES_MANUALLY.md`.

## A question's life, and your moments (autonomous mode, from 2026-09-13)

```
BACKLOG idea (or a line you wrote in research/INBOX.md)
  → /desk-run: @registrar drafts PREREG.md          (agent)
  → @decision-maker decide QNNN --autonomous         (agent; settles everything by
                                                      research/DECISION_POLICY.md DP-01..48;
                                                      what it defaulted for you goes on the board)
  → @data-steward exposure count → @decision-maker record → @registrar apply
  → the desk commits and locks (--by desk), writes schedule.json, pins the data
  → the desk waits for the decision date (no interim looks)
  → @data-steward freeze-for QNNN (successor freezes)  (agent)
  → @researcher writes eval.py once, runs it          (agent; no tuning while looking)
  → validators.py mechanical checks                   (script)
  → @red-team attacks it                               (agent; sees only PREREG, eval.py, results)
  → @reporter writes REPORT.md + LEDGER row, updates the lists, regenerates the board
  → verdict: NULL / INCONCLUSIVE / HISTORICALLY_CONFIRMED
  → YOU decide: build it?                              ← moment 1: HUMAN_APPROVED (controller)
  → /desk-run prompt QNNN → IMPLEMENTATION_BRIEF.md    (agent)
  → YOU run the brief in the platform repo, flag OFF, record SHA  ← moment 2
  → steward grades the dark column ≥ 30 nights → SHADOW_VALIDATED → YOU flip the flag ← moment 3
```

Only you can do the three ← moments; the controller refuses them from anyone else. Everything
before the verdict the desk now does on its own. The full description, the sub-commands and the
overnight schedule are in `docs/AUTONOMOUS_DESK.md`.

**Trading rules for you** take a shorter path: a HISTORICALLY_CONFIRMED verdict → the Reporter
writes `playbook/PB-NNN_slug.md` with the rule, its n and caveats, marked *trade small until
PROSPECTIVELY_CONFIRMED*. Nothing reaches subscribers until it has held up on nights *after*
the lock date.

## Platform bugs take a different, shorter path

A bug is not a finding. It goes in `research/PLATFORM_ISSUES.md` with evidence. You ask for the
prompt — `/desk-run prompt PI-NNN` — and asking *is* your decision: the desk marks it `fix` and
writes `research/briefs/PI-NNN_slug.md`, a short prompt you hand to the coding agent in the
platform repo. When it is in, `/desk-run verify PI-NNN <sha>` and the steward runs the brief's
before/after check. No pre-registration, no shadow period. Anything that turns out to be a
*behaviour change* to scoring gets promoted to a question. Enhancements
(`research/ENHANCEMENTS.md`) and your trade ideas (`research/TRADE_IDEAS.md`) take the same
prompt → implement → verify route; behaviour changes wait for their question's verdict, or ship as
a flag-off internal tool for you only.

## The commands you'll actually type

```bash
./scripts/start_desk.sh                  # start (Git Bash; loads .env.research; winpty)
./scripts/start_desk.sh --admin          # maintenance: enforcement files writable
/desk-run                                # the desk works its queue; ends with "Waiting on you"
/desk-run prompt PI-011                  # you want the implementation prompt (this is your decision)
/desk-run verify PI-011 <sha>            # you implemented it; the desk checks
/desk-run idea "picks that gap up and close red on day 1 are dead money"   # jumps the queue
/desk-status                             # one-screen status (or just read research/BOARD.md)
python research/lib/controller.py advance Q00N HUMAN_APPROVED --by haci     # yours: build a finding
python research/lib/controller.py advance Q00N IMPLEMENTED_FLAG_OFF --by haci --note "PR … sha …"
python research/lib/controller.py advance Q00N RELEASE_APPROVED --by haci   # yours: flip the flag
# the old per-step commands (@registrar draft, @decision-maker decide --ask, @researcher run …)
# still work when you want to drive one step by hand
```

Files a human must edit (agents are blocked): `CLAUDE.md`, `.claude/**`, `research/lib/`
{controller, validators, freeze_dataset, eval_utils}. Use `--admin`, or run the scripts under
`docs/admin_pass/` yourself.

## Data the desk works from

- `research/data/manifest_v001.json` — the SAS tables, frozen 2026-09-10, checksummed.
- `research/data/manifest_prices_v001.json` — Alpaca daily and hourly bars for every
  candidate symbol, so paths and target touches can be measured on pinned prices.
- `research/data/DATA_NOTES.md` — what the tables don't tell you (manual runs, the earnings
  fix, regime backfill, split-corrupted ATR). **Read before any PREREG.**
- `research/data/exclusions_v001.json` — nights every eval.py must drop, machine-readable.
- New freeze = new version number. Manifests are never overwritten.

## Where we are (2026-09-10)

- **Desk:** working end to end; guards tested (44 cases); routines scheduled and smoke-tested.
- **Rule 5:** amended — the objective is now the pick's price path (L1–L6 touches, both
  directions, from a stated entry, against a distance-matched control), the way you trade.
- **Q001:** drafted under the *old* rule 5. Needs its metric rewritten before locking.
- **Backlog:** 30 open hypotheses; the 12 from EXPLORE_001 (H-053–H-064) are the ones aligned
  with your trading style. Top five are ranked in `research/reports/explore/EXPLORE_001.md`.
- **Ledger:** empty. No verdicts yet — nothing has been locked.
- **Platform issues:** 10 registered, none decided.
- **The clock:** June–September has 71 nights, below the 80-night floor. Nights after a lock
  count as clean forward data. Locking sooner is how the desk gets to a quotable claim sooner.
