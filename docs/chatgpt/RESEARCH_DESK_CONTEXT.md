# VolatilX Research Desk — structure, process, and current state

Reference document for a ChatGPT project. Written 14 September 2026. Upload this as a project file
alongside the instructions in `PROJECT_INSTRUCTIONS.md`.

Its job is to let someone with no access to the desk's data reason usefully about the desk's work:
propose hypotheses that survive registration, route findings to the right list, and challenge
results without inventing any.

---

## 1. What VolatilX is

A subscription AI trading-intelligence platform. Four products matter for research:

- **Super Agent Select (SAS)** — the flagship. Every trading night it scores a universe of
  candidate stocks and publishes a slate of roughly eight picks, each with a 0–100 `overall_score`,
  a direction, a best timeframe (day / swing / long), a target ladder **L1–L6**, and a stop.
- **AI Picks** — projection-driven bullish and bearish lists.
- **UOA / Whale Watch** — unusual options activity and insider-flow screens. These also feed SAS's
  candidate universe.
- **Execution guidance** — the printed ladder, the scale-out plan, the Conviction Monitor that can
  flag a held pick as EXIT.

**How SAS scores.** Seven weighted layers, version 1.6: projection 29, technical 27, flow 24,
catalyst 10, fundamental 5, smart-money 5, GEX 0 (computed but unused). Timeframe multipliers
change the effective weights. Two modifiers follow: a cross-layer bonus and a conflict penalty.
Publication floor is 80, so nothing below 80 is published on the bull side. The conviction card
maps 80–89 to "Pro" and 90+ to "Elite".

**The ladder is the product's core promise.** L1 is nearest, L6 furthest. Each lane grades on its
own window: day 20 sessions, swing 40, long 60. The desk's objective is built on these, not on
returns — see §3.

---

## 2. What the desk is, and the one-way street

The desk is a separate repository from the platform. It reads the platform's code and a read-only
role on its database; it never writes to either. Changes to the platform happen only through an
implementation brief that Haci runs himself in the platform repo.

**The flow you sit in:**

```
you (ChatGPT)  ->  Haci  ->  the desk's INBOX  ->  a registered question  ->  a verdict
                     \
                      ->  a platform issue / enhancement / trade idea  ->  a prompt  ->  Haci implements  ->  the desk verifies
```

You are upstream of everything. You propose; the desk disposes. You cannot see a result unless Haci
pastes it. **The desk's value is that every number is traceable to a frozen dataset and a
pre-registered plan**, so a number that arrives without that lineage is worse than no number.

**What the desk will not do, ever:** query live tables for a study result, edit a locked
pre-registration, tune a script while looking at its output, or let a figure reach a subscriber on
the strength of a hypothesis.

---

## 3. The objective: the price path, not the return

This is the single most important thing to internalise, and the most common place an outside
proposal goes wrong. **A fixed-horizon return is descriptive and decides nothing.**

What decides is **whether and when the pick's price path first touched a target**, measured the way
the trade is actually taken:

- **First touch of a ladder level** within that level's lane window, from a stated entry.
- **Entry basis is always named**: pick-night after hours, the next session's open, or a next-day
  intraday trigger. A target already passed at entry is not a hit.
- **Every hit-rate claim is compared against a distance-matched control** — same-night candidates
  that were *not* published, given a synthetic target at the same distance in ATR, matched on beta,
  volatility and recent run-up. A hit rate without that control is a description of the market, not
  of the platform.
- **Stops are never assumed as exits.** Adverse excursion and counter-direction touches are
  reported, not applied, unless a question is specifically about the stop.
- **Money is denominated in ATR per trade**, not in R. The desk assumes no stop, so R has no
  denominator. If you think in R, translate: the desk's money unit is the realised ATR of the
  platform's own committed scale-out over a fixed session budget.
- **Speed counts.** *When* a target is touched is part of the claim, not just whether.

---

## 4. The statistical frame

- **The unit of inference is the trading night**, not the stock. Stock rows are aggregated into one
  number per night first. Roughly eight picks a night means eight correlated observations, not
  eight independent ones.
- **Sample floors:** 80 contributing nights per primary endpoint, 20 nights per stratum cell. A
  cell below its floor is reported as counts only and decides nothing.
- **Confidence intervals** come from a date-clustered or block bootstrap; p-values from permutation
  tests. Since 14 September 2026 every primary also reports an **episode-clustered** interval,
  where an episode is one symbol's run of selections within ten sessions — because the same symbol
  re-selected on consecutive nights shares its forward bars. A result that clears on the first
  interval and not the second is inconclusive, not confirmed.
- **Minimum practical effect (MPE)** is stated before the run. Defaults: **+5.0 percentage points**
  for a touch-rate endpoint, **0.25 ATR** for a per-trade money endpoint, and **double** for a
  difference of differences. "Positive but below the MPE" is inconclusive, not a small win.
- **Multiple testing:** questions are grouped into families and reported with
  Benjamini–Hochberg-adjusted q-values across the family, threshold 0.10.
- **Regime is the dominant variable.** Every result is stratified by the platform's regime label
  and by a calendar split. **April–May 2026 was a strong tape; June–August was not.** A result that
  only holds in one period is not a result. Treat any claim that rests on April–May as unproven.

---

## 5. The four verdicts

| verdict | meaning |
|---|---|
| **NULL** | The effect is absent, or present but below the MPE, with the sample to say so. Ledgered with the same care as a positive. |
| **INCONCLUSIVE** | The sample could not separate the hypotheses, or a required sensitivity failed. |
| **HISTORICALLY_CONFIRMED** | Confirmed on data that existed when the question was locked. |
| **PROSPECTIVELY_CONFIRMED** | Confirmed on at least 30 contributing nights dated *after* the lock. **Only this supports a subscriber-facing claim.** None exists yet. |

**Most questions will return null. That is the design working.** If your proposals never predict a
null, they are not calibrated to this desk.

---

## 6. The lifecycle of an idea

A question moves through a state machine the desk enforces mechanically. It cannot skip a state and
cannot go backwards.

```
IDEA -> PREREG_DRAFT -> PREREG_LOCKED -> DATASET_PINNED -> EVALUATED -> VALIDATED
     -> REDTEAM_SIGNED -> LEDGERED -> HUMAN_APPROVED* -> BRIEF_WRITTEN
     -> IMPLEMENTED* -> LIVE_VALIDATED -> RELEASE_APPROVED*
```

`*` — only Haci can advance these three. Everything else the desk does on its own.

**In words:**

1. **Idea** — from Haci, from a pattern-mining pass over the in-sample split, from a weekly
   snapshot, or from you.
2. **Backlog entry** — restated in a fixed shape: pattern, baseline, sample, why it might be real,
   why it might be noise, source.
3. **Pre-registration** — a document fixing the population, the arms, the primary endpoints, the
   MPE, the window, the decision date, the strata, and the suppression list, **written before any
   sealed data is looked at**.
4. **Lock** — the pre-registration is committed. After this it is never edited. Corrections go to
   the red team, not into the file.
5. **Dataset pinned** — a frozen parquet plus a SHA-256 manifest. Studies read only frozen data.
6. **Run** — one deterministic script, written once, produces the numbers. Nobody tunes while
   looking.
7. **Red team** — an adversarial reviewer who reads only the pre-registration, the script and the
   outputs, never the researcher's notes. Hunts look-ahead bias, denominator errors, regime
   confounds, multiple-testing inflation, baseline mismatches. **It can and does overturn verdicts.**
8. **Ledger** — the verdict goes on the permanent record with its number, its sample and its q-value.
9. **Ship, if it earns it** — ship directly with no flag (DP-59), verify after deploy, grade it live ≥ 30 nights before quoting it.

**Autonomous mode.** Since 13 September 2026 the desk works its own queue without asking Haci:
it registers and locks questions itself, settles the decisions it used to ask about, applies a
conservative default when it cannot choose cleanly, and lists every such default on the board for
him to overturn. His moments are: read the board, ask for a prompt, implement, ask the desk to
verify, and the three human-only states above.

---

## 7. The four lists — routing a finding correctly

Getting this wrong is the most common error. Each list has a different destination.

| list | what belongs in it | id | what happens next |
|---|---|---|---|
| **BACKLOG.md** | A hypothesis about the market or the platform's behaviour that could be **true or false**, and that data could settle. | `H-NNN` | Becomes a registered question, or is deferred with the blocker named. |
| **PLATFORM_ISSUES.md** | A **defect**. Something is broken, missing, silently wrong, or conflates two things. Not a question — there is nothing to test. | `PI-NNN` | Haci marks it fix / research / accept. Asking for the prompt is the decision. |
| **ENHANCEMENTS.md** | Something the platform **could do and does not**. Split into *plumbing* (no subscriber-visible number changes; buildable now) and *behaviour* (changes what is scored, selected or shown; **gated on a research verdict**). | `EN-NNN` | Same route as a fix, but a behaviour enhancement waits for its gate. |
| **TRADE_IDEAS.md** | A rule **Haci** might trade, in his own account. Carries an evidence status and, separately, the tool the platform would need. | `TI-NNN` | Never subscriber-facing until a prospective verdict exists. |

**The test:** if it could be false, it is a hypothesis. If it is already false and just needs
fixing, it is an issue. If nothing is wrong but something is missing, it is an enhancement. If it
changes what Haci does at the screen tomorrow, it is a trade idea. **One finding often generates
one of each** — a defect, the question it raises, the feature that would fix it, and the rule Haci
trades meanwhile. Say so when that happens.

---

## 8. The families

Questions are grouped for multiple-testing correction. A hypothesis belongs to the family of its
**primary endpoint's subject**, not its topic.

| family | subject |
|---|---|
| **F1** | Selection edge — does picking these names beat not picking them? |
| **F2** | Calibration — does the score mean what it says? |
| **F3** | Unused signals — GEX, IV/RV, insider timing. |
| **F4** | Price behaviour after selection — gaps, fast starts, earnings proximity, slate concentration. |
| **F5** | Cross-engine interaction — UOA and SAS together. |
| **F6** | Exits and execution — stops, lanes, recycling, monitor exits. |
| **F7** | Path, entry timing and volatility — Haci's own trading style. |
| **F8** | System validity — integrity, discovery, architecture, objective choice. |

---

## 9. The seven-point screen — run this before proposing any hypothesis

Two of these kill most ideas. Work points 2 and 3 first.

1. **Is it a hypothesis at all?** Could it come back false? If not, route it to §7's other lists.

2. **Exposure arithmetic — will the event ever happen often enough?**
   Estimate how many nights per trading session carry the event. The floor is 80 contributing
   nights, and the desk will not wait more than about twelve months from lock. So the event needs
   roughly **0.3 or more contributing nights per session** to be registrable. Worked failures:
   - A bear-pick question measured 0.157 per session. Projected decision date: about 22 months past
     the ceiling. Deferred.
   - An earnings-repeat question measured about 0.185 on the honest unit. Deferred.
   - An elite-threshold question found the median night carries **no** candidate above 90 at all.
   - A whole class of questions dies here. If you cannot sketch the arithmetic, say so.

3. **Does the control actually exist?**
   Almost every endpoint is a contrast. The comparison group must exist **on the same night**, or
   the contrast is a calendar comparison in disguise. Worked failure: an exposure-attribution
   question wanted picks matched on sector, size, beta, momentum and volatility. The candidate pool
   is about 57 names a night across eleven sectors, so the median pick had five to seven
   same-sector neighbours, and the five-feature caliper then passed only **7.6%** of picks. **No
   night in 46 ever carried three valid matches.** Deferred, and the platform fix — retain a larger
   candidate universe — is now a filed enhancement.

4. **Knowledge time.** A feature may only be used if it existed at 16:05 ET on the pick night. Three
   known traps: the regime label has no point-in-time value before 9 June 2026 (it was backfilled);
   the UOA swing and long scores are **overwritten in place** by a next-morning confirmation pass;
   the ladder excursion table is recomputed weeks later. If your idea needs a number that only
   exists the next morning, it needs an exception the desk cannot grant itself — only Haci can.

5. **Is the unit right?** One symbol re-selected on four nights before one earnings report is **one**
   outcome, not four. Counting selection rows would enter the same forward bars several times, and
   hardest in the treatment arm. Ask what one independent observation actually is.

6. **Has the answer already been seen?** If a weekly snapshot or a previous run already looked at
   this cut on sealed data, a question built on it is post-hoc for that dataset. The remedy is a
   **prospective-only window** starting after the lock — which is honest but pushes the answer out
   by a year. Say when you think this applies.

7. **Is it already registered?** Thirty-six questions exist. Check §11 before proposing. If it
   overlaps, the right move is usually to say "this is a secondary of Qnnn" rather than a new
   question — and the desk explicitly forbids counting two overlapping questions as two
   confirmations of the same thing.

---

## 10. What the desk already knows — do not re-propose these

**Findings on record:**
- Directional accuracy sits at roughly the base rate.
- "Champion" symbols grade **below** base rate.
- The whale ledger table is empty.
- A regime A/B test found no bonus-day edge.
- The 88–90 band underperforms 90+.
- Re-qualification after a large favourable move is continuation, not exhaustion.
- Short-dated options underperform.
- The only ledgered verdict so far: **why the platform publishes fewer 90+ picks each month** —
  **inconclusive**. The fall is real (elite-candidate rate halved, p = 0.016) but the cause is not
  pinned. The script blamed four configuration changes; the red team overturned that, because none
  of those changes can move a score.

**Known data problems (these are filed issues, not open questions):**
- A forward-return column silently froze and is about 95% degraded; the fix exists but at the time
  of writing sits unmerged on a branch, so production still runs the old code.
- ATR is computed on unadjusted bars, so it is corrupted around splits.
- Manual re-runs are indistinguishable from scheduled runs in the run table, and the run table is
  updated in place, so there is no history.
- The printed swing stop is on the **wrong side** of the pick-night close for 67 of 382 published
  picks — 17.5%.
- The industry column is populated for only 12% of candidates. Sector comes from a separate pinned
  file instead.
- Sixteen published picks have no target ladder at all.
- The GEX pin-risk flag conflates "not pinned" with "not measurable".
- The projection layer — the **largest** weight at 29 — is unscored on about 72% of published rows,
  so the score is usually a six-layer blend, not seven.
- The conviction label is degenerate: its completeness arm never fires on published rows.
- The Conviction Monitor's polarity arm has been silent since 1 June 2026.
- L1 and L2 targets sit inside a single normal day's range — median 0.31 and 0.55 ATR — so they are
  not evidence of anything. Targets are written by a language model from projection levels and are
  **not ATR-scaled**.

---

## 11. Current state, 14 September 2026

**Thirty-six questions. One verdict. Nothing confirmed, nothing ruled out.**

**Answers already scheduled:**

| date | question |
|---|---|
| 21 Sep 2026 | Did every input exist when the prediction was made? *(pass/fail; a fail stops everything)* |
| 28 Sep 2026 | Are the seven scoring layers seven signals or three or four? |
| 5 Oct 2026 | **Does selection beat a distance-matched control from its own universe?** *(the central one)* |
| 12 Oct 2026 | Do picks reach near targets sooner than matched candidates? |
| 26 Oct 2026 | After hours, at the open, or at 10:00 — does the entry matter? |
| Nov–Dec 2026 | Stop whipsaw; the day-1 dip limit; repeat selection; fast start to a deep target. |
| Feb–Apr 2027 | Prospective stop replication; volatility and round trips; concentrated slates; capital recycling; earnings proximity; UOA persistence; **score ranking validity**; **which layers earn their weight**. |
| May–Aug 2027 | **Does the platform beat SPY, equal weight, momentum and a technical rank**; monitor exits; the 80–90 band in strong tapes; **edge decay**; lane choice; direction versus distance; pin risk; **which objective it predicts best**; the 85–90 give-back. |

**Held, with the blocker named:**
- The exposure-matched control does not exist on any night (see §9 point 3).
- The projection layer is too sparse to reconstruct the night's choice set.
- The conviction label's comparison arm cannot exist on the running configuration.
- One question needs a knowledge-time exception only Haci can grant.
- Two were unblocked on 14 September 2026: universe discovery recall, and regime conditionality.

**Deferred hypotheses awaiting data the desk does not hold:** options price history (two ideas),
bear-pick exposure, analyst revisions, Haci's own fill history, and an elite-band threshold search.

---

## 12. Output formats — use these exactly

### A new hypothesis

One line, for `research/INBOX.md`. Haci pastes it; the desk turns it into a numbered backlog entry
on its next cycle.

```
- [ ] <the idea in plain words, one or two sentences — what you think is true and what you would do about it>
```

If you have done the screen in §9, add your working **underneath the line as a separate note**, so
Haci can hand it to the desk:

```
Screen: family <Fx>. Baseline <what it is compared against, same night>. Unit <what one
observation is>. Exposure <your estimate of contributing nights per session, and the arithmetic>.
Knowledge time <what the feature needs and when it exists>. Overlap <which existing question this
touches>. Why it might be real <one sentence>. Why it might be noise <one sentence>.
```

### A platform issue

```
| PI-0NN | high / med / low / research | OPEN | <what is broken, in one sentence, with the file or column if known> |
```

### An enhancement

```
| EN-0NN | plumbing / behaviour | PROPOSED | <gate: the question it waits on, or — > | — | <what it would do and why> |
```

### A trade idea

```
| TI-0NN | IDEA | <the platform tool it would need, or — > | <the rule, in the first person, and what evidence would settle it> |
```

---

## 13. How to be useful in a conversation

**When Haci brings a result**, ask in this order: what was the control, what was the unit, what did
the sealed period alone say, and does it survive the other tape. Then ask what he would *do*
differently — a result that changes no decision is a curiosity.

**When Haci brings a platform observation**, decide whether it is a defect or a question, and say
which. If it is a defect, ask whether any locked question reads the column it touches, because a
repair rewrites the desk's own history — the research database **is** production, separated only by
a read-only role.

**When you generate hypotheses**, prefer ones that:
- are about the **path**, since that is the registered objective;
- have a same-night control that plainly exists;
- concern something the platform already computes but does not use (GEX at weight zero, the
  cross-layer bonus, the conflict penalty, the completeness score);
- would change a decision at the screen, not just a description.

**Good sources of new questions:** what the platform's code does *not* yet do; where two products
disagree about the same symbol on the same night; any place a number is shown to subscribers
without a control beside it; and any layer whose weight is large but whose coverage is poor.

**Push back when:** a result rests on April–May 2026; a cell is under 20 nights; a control is
matched on fewer features than the thing it claims to isolate; a "fix" would rewrite history a
locked question depends on; or a proposal quietly needs tomorrow morning's data.

---

## 14. Vocabulary

| term | meaning |
|---|---|
| **ATR** | Average true range — the desk's unit of distance and of money. |
| **L1–L6** | The published target ladder, nearest to furthest. |
| **lane** | day / swing / long, each with its own grading window (20 / 40 / 60 sessions). |
| **contributing night** | A night that actually supplies an observation to a given endpoint. The floor of 80 is counted in these, not in calendar nights. |
| **MPE** | Minimum practical effect — the smallest difference worth acting on, fixed before the run. |
| **pre-registration (PREREG)** | The locked plan. Written before the data is unsealed, never edited after. |
| **manifest / freeze / pin** | A hashed snapshot of the data a question is allowed to read. |
| **the board** | The desk's single status page: what is waiting on Haci, results, edges, issues, enhancements, trade ideas, defaulted decisions, and the calendar. |
| **red team** | The adversarial reviewer that must sign off before a verdict is recorded. |
| **NON_QUOTABLE** | A research figure that may never reach a subscriber. Most figures are this. |
| **dark lane** | Candidates that qualified but were not published. Excluded from every arm. |
| **knowledge time** | 16:05 ET on the pick night — the cutoff for what a feature may know. |
