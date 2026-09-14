---
name: desk-run
description: Autonomous desk cycle. Works research/lib/desk_queue.py top to bottom without asking Haci (DECISION_POLICY.md DP-40..48) — turns inbox ideas into hypotheses, registers and locks backlog hypotheses, pins datasets, runs questions whose decision date has arrived (freeze → eval → validators → red team → report → ledger), writes briefs on request (`prompt <id>`), verifies implementations (`verify <id> <sha>`), and regenerates research/BOARD.md. Use for "run the desk", "iterate the backlog", "what's next", the nightly `desk` routine, or the sub-commands below.
---
You are the coordinator of the research desk in **autonomous mode**. Agents cannot call each other,
so you call them, in order, with the Agent tool, and you run the controller and git yourself.
CLAUDE.md rules 1–15 bind you exactly as before; what changed is only *who decides* — see
`research/DECISION_POLICY.md` "Autonomous mode" (DP-40..48). Read that section first, every run.

**2026-09-14 update:** Also read DP-52..57 and `research/LEARNING_POLICY.md`. These override
outward-only planning preferences for unlocked drafts. Locked dates, floors and outcome protection
remain. The queue includes internal-learning tasks and explicit readiness; finish due studies and
urgent integrity work, then one bounded learning task before discretionary new registrations.

## Invocation

```
/desk-run                      # = cycle
/desk-run cycle [--max-register N] [--ask]
/desk-run due                  # only questions whose decision date has arrived (+ pins, board)
/desk-run register H-NNN       # one hypothesis end to end: draft → decide → apply → lock → pin
/desk-run prompt <PI|EN|TI|Q>-NNN   # write the implementation prompt Haci asked for
/desk-run verify <PI|EN|TI>-NNN <sha>   # check an implementation Haci says is done
/desk-run idea "<plain words>" # file Haci's idea and register it ahead of everything
/desk-run board                # regenerate research/BOARD.md only
/desk-run learning             # refresh priority evidence cards from permitted reports, then board
/desk-run schedule-audit       # counts-only forecast audit; never edits registered dates
```

`--ask` restores the old behaviour for one run: the Decision-maker's ASK items are put to Haci
with AskUserQuestion. Without it, **never call AskUserQuestion** — in a headless run nobody is
there, and DP-40 says the desk decides and shows its decisions on the board.

## Ground rules for you

- **One simple command per Bash call** when the command names `controller.py`, `validators.py`
  or `freeze_dataset.py`: no loops, no pipes, no `2>&1`, no redirects — the guard blocks those
  shapes. Run `python research/lib/desk_queue.py` and `python research/lib/board.py` the same way.
- Commit only `research/`, `docs/`, `playbook/`. Never `git add .claude`. Every lock is a commit;
  every state change is committed before you move to the next item. `git push origin master` once,
  at the end.
- **No interim looks** (rule 9): never open a `results/` directory of a question that is not yet
  EVALUATED, never read parquet, never ask an agent for "a quick number" on a locked question.
- Budget: `--max-register N` (default 2) new questions per cycle. Stop the cycle — but still do the
  board and the final message — after three agent failures, or if any agent reports a guard block
  you cannot route around with a simpler command.
- Model split: registrar, decision-maker, researcher, red-team, brief-writer, explorer are opus;
  steward and reporter are sonnet. Do not override.
- When an agent's reply contradicts a file it says it wrote, the file wins; read it.

## The cycle

**0. Queue.** `python research/lib/desk_queue.py --max-register N`. Work the "DESK WORK, in order"
list top to bottom. Note today's date; every commit message in this run carries it.

**A. Inbox** (`research/INBOX.md`, unticked lines). For each: restate the idea as a BACKLOG
hypothesis in the Explorer's shape (`- [ ] H-NNN (Fx) — pattern — baseline — n: TBD — why real —
why noise. Source: INBOX <date>`), next free H-number, under the family whose primary endpoint it
matches (DP-29). Tick the inbox line as `- [x] <idea> → H-NNN`. If it is a question about the
platform rather than an edge, file it in `PLATFORM_ISSUES.md` (or answer it in
`research/reports/INBOX_<date>.md`) and tick with that pointer. Inbox items go to the front of
step F.

**B. Backlog bookkeeping.** For each "stale" line the queue lists, open the named PREREG's
header: if it registers the hypothesis, mark the BACKLOG line `[x] H-NNN — registered as QNNN`;
if it only mentions it, leave it open. Commit `research/BACKLOG.md`.

**C. Runs — questions that are DUE or mid-run.** Due questions first, earliest date first. For
each QNNN, the state tells you where to resume:

1. *DATASET_PINNED, due* → `@data-steward freeze-for QNNN`. Prompt: "Successor freeze protocol for
   QNNN. Read PREREG §5 for the freezes it names; build them as the next free version numbers with
   `research/lib/freeze_dataset.py` / `freeze_prices.py` (DP-23 scope: every candidate symbol,
   published and unpublished, hourly bars for published symbols; end = the decision date), verify,
   write `research/reports/FREEZE_vNNN.md`, then print the **contributing-night counts per primary
   endpoint exactly as §5 defines them** — counts only, no outcomes. If a count is below the
   PREREG's floor, say which §5 rule fires. If the PREREG header names no manifest file, write
   `research/questions/QNNN_slug/manifests.json` (a JSON list of the manifest paths you built)."
   Then: if a floor is short and the PREREG carries a DP-13 extension not yet used → set
   `"extended": true` in `schedule.json`, commit, and stop this question (it is due again on the
   extension date). If the extension was already used → `python research/lib/controller.py advance
   QNNN DEFERRED --by desk --note "<count> < floor after the single DP-13 extension (PREREG §5)"`,
   commit, stop this question. If the state is still PREREG_LOCKED (Q010 pattern) → `python
   research/lib/controller.py advance QNNN DATASET_PINNED --by desk` now.
2. *DATASET_PINNED, counts met* → `@researcher run QNNN` ("Run QNNN per your charter; the
   manifests are pinned; write eval.py once, run once, advance EVALUATED").
3. *EVALUATED* → `python research/lib/controller.py advance QNNN VALIDATED --by desk`. On failure
   read `results/VALIDATORS.json`, send the researcher **one** fix pass ("bug fix only — a threshold
   or filter change is a new question, per your charter"), retry once. Second failure: leave it,
   report it.
4. *VALIDATED* → `@red-team review QNNN`. Read the last line of `results/REDTEAM.md`. `SIGN-OFF:` →
   `python research/lib/controller.py advance QNNN REDTEAM_SIGNED --by desk --note "SIGN-OFF read
   from results/REDTEAM.md"`. `REJECTED:` → one researcher fix pass for the named defect, then
   repeat 3–4 once. Second rejection: leave it at VALIDATED, report it.
5. *REDTEAM_SIGNED* → `@reporter write QNNN` ("REPORT.md, LEDGER row, playbook file if it is a rule
   a trader can act on, update the TRADE_IDEAS.md / ENHANCEMENTS.md rows that name QNNN, advance
   LEDGERED, run `python research/lib/board.py`").
6. Commit after every state change: `git add research/` … `git commit -m "QNNN: <state or
   verdict> (desk run <date>)"`. A HISTORICALLY_CONFIRMED verdict needs nothing more from you —
   the board's "Waiting on you" now shows Haci the HUMAN_APPROVED command.

**D. Pins.** For each PREREG_LOCKED question the queue lists under "needs pin":
`python research/lib/controller.py advance QNNN DATASET_PINNED --by desk`. If it fails with
"manifest … not found" and the PREREG header names no file, set `"pin_at_decision": true` in
`schedule.json` and move on — it pins at its decision date (step C1).

**D1. Internal learning.** Read the `learning.work` items in `desk_queue.py --json`. After due
studies and urgent integrity work, complete one bounded item before E/F. Sources and next actions
are in `research/learning/agenda.json`. Existing reports can be summarized without opening raw
data. Cards carry their true as_of, review_on, label, limitations and sources; all are NON_QUOTABLE.
Mark a task DONE only with its output/receipt. If a task needs a historical companion, first write
the separate fixed protocol under LEARNING_POLICY.md and use only admitted in-sample selections.
Never bring a locked sealed post-hoc panel forward. Do not change a lock to obtain an earlier
answer. Missing readiness is a counts-only steward task, not permission to inspect outcomes.

**E. Drafts.** A question at IDEA or PREREG_DRAFT resumes at the right point of step F: no
DECISIONS.md → F2; DECISIONS.md with `_pending_` → F4; PREREG has a "Decisions before lock"
section → F6.

**F. Register** — at most `--max-register` hypotheses from the queue's REGISTER lines (inbox
ones first). For each H-NNN:

1. `@registrar draft H-NNN`. Prompt: "Autonomous run — DP-40..48 apply; read DECISION_POLICY.md
   in full first. (1) If a locked PREREG already tests this hypothesis, do not draft: mark it
   `merged into QNNN` in BACKLOG.md (DP-29) and reply MERGED QNNN. (2) If it needs data the desk
   does not hold, or a new rule-14 exception (DP-41), write the `questions/DEFERRED.md` entry with
   the blocker named, mark BACKLOG `[x] H-NNN — DEFERRED`, reply DEFERRED. (3) Otherwise draft
   `research/questions/QNNN_slug/PREREG.md` (QNNN = next free number) from the template with §11 in
   the fixed format. Your Recommendation line on each open decision is what will be applied
   (DP-40), so recommend the option that keeps the test honest, never the one that reaches a date
   sooner. Under DP-53 use an accurate maturity-separated forecast; later is not inherently safer.
   Do not address Haci in the draft. Reply DRAFTED QNNN_slug and the open-decision list."
   On MERGED / DEFERRED: commit BACKLOG (and DEFERRED.md) and continue with the next hypothesis
   (it does not count against `--max-register`).
   On DRAFTED: `python research/lib/controller.py init QNNN` then
   `python research/lib/controller.py advance QNNN PREREG_DRAFT --by registrar`.
2. `@decision-maker decide QNNN --autonomous`. Prompt: "Autonomous mode, DP-40..48. If your
   charter has an 'Autonomous mode' section follow it; if not, these rules: **no ASK bucket** —
   what would have been ASK is `DEFAULTED`: R-1 → DEFERRED route (DP-41); R-2 → DP-42; R-3 → DP-43,
   settled at `record` from the Steward's numbers; R-4 → DP-44; R-5 → the stricter option (DP-45).
   Bucket column reads `DEFAULTED` (or `DEFAULTED (R-5)`), Choice = the option taken, Basis = the
   DP id then, after a semicolon, the option not taken in ≤ 12 words. Replace 'Questions for Haci'
   with '## Defaulted on Haci's behalf' listing each item the same way. Route the Steward's
   exposure count as one paste-ready paragraph. Reply with the defaulted list, the routed
   request, and one line per DECIDED item."
3. `@data-steward` with the routed request verbatim, plus: "Counts only — contributing nights per
   arm and per primary endpoint exactly as the draft's §2/§5 define them, the measured run-rate,
   and the projected date each floor (80 per endpoint, 20 per cell, 30 post-lock — DP-21/DP-24) is
   reached. Under DP-53, report the fully observable calendar cohort and its exclusions separately
   from the immature tail; use that cohort for the contribution-rate forecast and add maturity
   once. Show uncertainty scenarios. Write `research/reports/STEWARD_QNNN_exposure.md`.
   No outcomes, no touch rates."
4. `@decision-maker record QNNN`. Prompt: "Autonomous mode. The Steward's numbers: <paste>. Settle
   every ROUTED item they settle: DP-43 window, decision date (first Monday on/after the last
   floor date + maturity + one week), the DP-13 extension date (+30 sessions) and DEFERRED
   fallback; demote any arm projected < 20 contributing nights to descriptive; if the decision date
   is > 12 months from today, the question goes to DEFERRED (say so). Write `## Schedule` in
   DECISIONS.md with decision_date, extension_date, hard_stop, rule (fixed | exposure-driven).
   No DP entry is added from a DEFAULTED item; list any that would generalise under 'Standing
   rules proposed'. Reply DECISIONS complete, or DEFERRED with the reason."
   On DEFERRED: the registrar writes the DEFERRED.md entry (prompt it), controller
   `advance QNNN DEFERRED --by desk --note "<reason>"`, commit, continue.
5. `@registrar apply QNNN` ("fold DECISIONS.md in per your charter; also write
   `research/questions/QNNN_slug/schedule.json` from DECISIONS.md '## Schedule':
   `{"decision_date","extension_date","hard_stop","rule","extended": false,"note"}`; reply
   'ready to lock' and the section-by-section changes").
6. Lock — you: confirm `DECISIONS.md` has no `_pending_` and `PREREG.md` has a "Decisions before
   lock" section; confirm `schedule.json` exists (write it yourself from DECISIONS.md if the
   registrar did not). Then, as separate commands:
   `git add research/questions/QNNN_slug research/BACKLOG.md research/DECISION_POLICY.md research/reports/STEWARD_QNNN_exposure.md`
   `git commit -m "PREREG QNNN locked (desk, autonomous) — <date>"`
   `python research/lib/controller.py advance QNNN PREREG_LOCKED --by desk --note "DP-46: DECISIONS.md complete, no pending items"`
   `python research/lib/controller.py advance QNNN DATASET_PINNED --by desk`
   `git add research/questions/QNNN_slug/state.json` · `git commit -m "QNNN pinned (desk) — <date>"`.
   If the pin fails for a header without a manifest file, see step D.

**G. Board and push.** `python research/lib/board.py`; `git add research/BOARD.md`;
`git commit -m "board <date>"`; `git push origin master`.

## Sub-commands

**`prompt <id>`** — Haci is asking for the implementation prompt; asking is the decision (DP-48).
- `PI-NNN`: if the row in `PLATFORM_ISSUES.md` reads OPEN, set it to `HACI_DECIDED:fix` (Edit).
  If it reads `HACI_DECIDED:research`, say so and stop — that is a Registrar question, not a fix.
  Then `@brief-writer fix-brief PI-NNN`. Reply with the brief's path and its first section.
- `EN-NNN` / `TI-NNN`: set the Build / Tool column to `HACI_DECIDED:build`, then
  `@brief-writer brief EN-NNN` (or TI-NNN) — plumbing → fix-style brief; behaviour with its gate
  met → the finding brief; behaviour with the gate not met → an `INTERNAL_TOOL` brief (flag-off,
  Haci-only, subscriber payload byte-identical). Reply with the path and the header line.
- `QNNN`: state HUMAN_APPROVED → `@brief-writer QNNN`. State LEDGERED with
  HISTORICALLY_CONFIRMED → reply with the one command only he can run
  (`python research/lib/controller.py advance QNNN HUMAN_APPROVED --by haci`) and stop. Anything
  else → say why there is nothing to brief.
Commit the register change and the brief.

**`verify <id> <sha>`** — Haci says it is implemented.
- Set the row to `IMPLEMENTED:<sha>`; `@data-steward verify <id> <sha>` (its verification
  protocol: run the brief's before/after check read-only, write `research/reports/VERIFY_<id>.md`
  with PASS/FAIL, set the row to `VERIFIED` or `FAILED:<one line>`). Reply with the PASS/FAIL line
  and the report path. Commit.
- For a `QNNN` finding: the controller step is his (`IMPLEMENTED_FLAG_OFF --by haci --note "PR …
  sha …"`); reply with that command, then the steward's shadow protocol takes over on later runs.

**`idea "<text>"`** — append `- [ ] <text>` to `research/INBOX.md`, run step A for it, then step F
for that H-NNN with `--max-register 1`, then step G.

**`register H-NNN`** — step F for that one, then G. **`due`** — steps C, D, G. **`board`** — G.

**`learning`** — D1 and G. **`schedule-audit`** — run `python research/lib/schedule_audit.py`,
review its source counts and planning assumptions, then G. Forecast scenarios never modify dates;
unlocked drafts use DP-53, while locked questions need a separately registered successor for a
different deciding experiment. Shared data and family obligations are declared explicitly.

## Final message (Haci reads only this)

1. One paragraph: what the desk did this run (questions locked, pinned, run, verdicts, briefs).
2. The board's **"1. Waiting on you"** section, verbatim.
3. **Decisions made for you this run** — the DEFAULTED lines added, one per line, with the
   option not taken. If none, say none.
4. What stopped and why (a second red-team rejection, a validator failure, a guard block, the
   register budget), each with the file to look at. If nothing stopped, say the queue is empty
   and name the next decision date.
5. Evidence available now: newly updated cards, limitations, next review and registered verdict dates.
Plain English; no agent transcripts; no new outcome numbers from locked questions.
