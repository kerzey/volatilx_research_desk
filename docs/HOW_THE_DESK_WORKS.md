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

## A question's life, and your three moments

```
BACKLOG idea
  → @registrar drafts PREREG.md                 (agent)
  → @decision-maker decide QNNN                 (agent; settles the open decisions from
                                                 research/DECISION_POLICY.md, routes the rest)
  → YOU answer the 1–3 questions it couldn't settle; @registrar apply QNNN folds them in
  → YOU read it, commit it                       ← moment 1: lock
  → controller: PREREG_LOCKED → DATASET_PINNED   (steward)
  → @researcher writes eval.py once, runs it     (agent; no tuning while looking)
  → validators.py mechanical checks              (script)
  → @red-team attacks it                          (agent; sees only PREREG, eval.py, results)
  → @reporter writes REPORT.md + LEDGER row       (agent)
  → verdict: NULL / INCONCLUSIVE / HISTORICALLY_CONFIRMED
  → YOU decide: build it? trade it? drop it?      ← moment 2: HUMAN_APPROVED
  → @brief-writer writes IMPLEMENTATION_BRIEF.md  (agent)
  → YOU run the brief in the platform repo, flag OFF, record SHA  ← moment 3
  → steward grades the dark column ≥ 30 nights → SHADOW_VALIDATED → you flip the flag
```

Only you can do the three ← moments. `research/lib/controller.py` refuses every step whose
predecessor isn't done; agents don't argue with it.

**Trading rules for you** take a shorter path: a HISTORICALLY_CONFIRMED verdict → the Reporter
writes `playbook/PB-NNN_slug.md` with the rule, its n and caveats, marked *trade small until
PROSPECTIVELY_CONFIRMED*. Nothing reaches subscribers until it has held up on nights *after*
the lock date.

## Platform bugs take a different, shorter path

A bug is not a finding. It goes in `research/PLATFORM_ISSUES.md` with evidence, you mark it
`fix` / `research` / `accept`, and `@brief-writer fix-brief PI-NNN` produces a short prompt you
hand to the coding agent in the platform repo. No pre-registration, no shadow period — but the
brief still names a before/after check, and the steward confirms the data changed on the next
freeze. Anything that turns out to be a *behaviour change* to scoring gets promoted to a question.

## The commands you'll actually type

```bash
./scripts/start_desk.sh                  # start (Git Bash; loads .env.research; winpty)
./scripts/start_desk.sh --admin          # maintenance: enforcement files writable
/desk-status                             # where everything is
@registrar draft H-055                   # turn a backlog idea into a PREREG draft
@decision-maker decide Q00N              # settle the draft's open decisions; asks you only the reserved ones
@decision-maker record Q00N <answers>    # write your answers down; generalisable ones become standing rules
@registrar apply Q00N                    # fold DECISIONS.md into the draft
git add research/questions/Q00N_*/PREREG.md && git commit -m "PREREG Q00N locked"
python research/lib/controller.py advance Q00N PREREG_LOCKED --by haci
@data-steward advance Q00N DATASET_PINNED
@researcher run Q00N
python research/lib/validators.py --question Q00N
@red-team review Q00N
@reporter write Q00N
python research/lib/controller.py advance Q00N HUMAN_APPROVED --by haci
@brief-writer Q00N
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
