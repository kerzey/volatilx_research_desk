# STEWARD_Q031_exposure.md — R1 (counts only), Q031 edge_decay

**Request:** `research/questions/Q031_edge_decay/PREREG.md` §5.3 R1, and DECISIONS.md "Routed
requests — data-steward — R1 (counts only) — BLOCKING FOR LOCK" (Correction 2). Counts only, no
outcome of any kind: no touch, no first-touch date, no return, no excursion, no `outcome_*` column,
no `sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`, no score-vs-outcome cross-tab.
Forward bars read only to establish that a bar exists (gradeability accounting), never for a value.
Frozen data only — `research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`
against `research/data/exclusions_v003.json`, plus read-only `git log`/`git show`/`git diff` against
the pinned platform repository — never a live query (DP-50(c)). The database credential was unset in
this session; not needed — this task uses frozen data only.

**Population:** pick nights **2026-06-01..2026-09-10**. Denominator for every rate = **elapsed
sessions**, exclusions not pre-removed (Q019/Q022/Q023/Q027 convention).

**Elapsed sessions in window: N = 71** (2026-06-01..2026-09-10), reconfirmed against the SPY daily-bar
calendar in `manifest_prices_v001` and against `sas_runs` (71 rows) — both agree exactly, matching
`STEWARD_Q027_exposure.md`.

**Nights excluded from the population (3):** `2026-06-26` (`uncorroborated_publication_runs`),
`2026-07-02` (`manual_runs`), `2026-07-06` (`manual_runs`). DP-04 late-`finished_at` check re-run:
exactly one night fails, `2026-07-06` — already excluded, so DP-04 adds **0** incremental nights.
**Non-excluded nights: 68.** Identical to `STEWARD_Q027_exposure.md` (same population, same
criteria) — reconfirmed independently here, not copied.

**Matured nights (t+20 <= 2026-09-10, the freeze's own last date): 48 of 68.** Identical set to
`STEWARD_Q027_exposure.md`'s 48 matured nights (2026-06-01..2026-08-12 matured;
2026-08-13..2026-09-10, 20 nights, immature — a freeze-horizon artifact). Both series' contributing-
night rules require maturity to t+20, so **both series draw from the same 48-night population** —
this is also the population R1(e)'s "nights contributing to both series" is measured over.

---

## Headline

- **(e) Series A's contributing-night rate: RECONFIRMED, not corrected.** Independently
  recomputing Q027 §2.5's complete definition (dominant_direction in {bullish, bearish}, >=60
  split-adjusted daily bars <= t, matured to t+20, gradeable, >=30 eligible rows) on this same freeze
  gives **48/71 = 0.6761/elapsed session — bit-for-bit the same count** `STEWARD_Q027_exposure.md`
  reported. No disagreement, so no DP-50(a) finding here.
- **(a) Series B's contributing-night rate under §2.5's registered rule (>=3 valid published picks,
  each with >=5 matched controls): 47/71 = 0.6620/elapsed session.** The **same 47/71** rate holds
  under **all three** tested rules — Q031's registered rule, Q006's weaker rule (>=1 valid pick), and
  the drop-the-thin-pick variant — because in this measured population **the control-pool floor never
  binds** (pool depth ranges 37–60, never below 5 or even 10) and the **only** night that fails any
  form of the rule is `2026-06-02`, which has **zero** valid picks under every rule (all 8 published
  rows lack `lane_plans` entirely — the same night `STEWARD_Q027_exposure.md` flagged for the
  identical reason). **The cost of the stricter floor, measured, is zero on this freeze**: nothing
  about the >=5-controls clause excludes a single additional night.
- **(e) Nights contributing to BOTH series: 47** (all matured nights except `2026-06-02`, which series
  A does contribute on — 42 eligible rows that night — but series B does not).
- **(f) DP-50(a)/(b) commit sweep since `fa70688`: NONE**, reconfirmed independently. `HEAD` is
  unchanged at `d19c9a9` (same as `STEWARD_Q027_exposure.md`'s measurement, same day) — **no new
  commits exist since Q027's sweep**, and the same 4 commits (`2d5776c`, `4775e49`, `22a2e1b`,
  `d19c9a9`) touch none of `services/super_agent_select_scoring.py`,
  `services/super_agent_select_models.py`, `services/sas_conviction_card.py` (full diffstat: `app.py`,
  a new speed-to-target service/router/tests, nightly-pipeline backfill-window clamp — see (f) below).
  **v1.7 is not scheduled inside 2026-09-15..2027-07-12**: `docs/SAS_SCORING_RESEARCH_PLAN.md`
  (drafted 2026-08-26) is explicitly a **PROPOSAL, not a decision record, "owner sign-off required
  before any workstream starts"**, with phases stated in relative weeks, not calendar dates, and no
  commit anywhere in the repo shows the workstream has started. This is a live risk to watch at every
  future sweep, not a cleared one — see (f).
- **Branch call (§5.1's demotion rule, DP-43): BRANCH (ii) fires — the window end moves out for
  both series; nothing is demoted; `m = 2` stands.** Series B's measured rate (0.6620/session) is
  **below** the 0.6723/session "nothing changes" threshold (Correction 1: 80 across the first 119
  sessions), so **branch (i) does not fire**. Recomputing the window end as the **later** of the two
  series' own floor dates — checked **per block, not as a total over the window** (Correction 1) —
  gives a new window end of **153 elapsed sessions (2027-04-23)**, decision date **Monday
  2027-06-07**, **8.7 months from the 2026-09-14 lock**, comfortably inside DP-43's 12-month ceiling
  (2027-09-14). **Branch (iii) (demotion) does not fire.** Full arithmetic below.

---

## (a) Series B's contributing-night rate, three forms

Restricted to the 48 matured nights (§2.5 requires maturity to t+20 for both series).

| rule | contributing nights | rate (elapsed sessions) |
|---|---:|---:|
| **Registered (§2.5): >=3 valid published picks, each with >=5 matched controls** | **47 / 71** | **0.6620** |
| Q006's weaker rule: >=1 valid published pick (with >=1 matched control) | 47 / 71 | 0.6620 |
| Drop-the-thin-pick variant: drop any pick with <5 controls, contributing if >=3 valid picks remain | 47 / 71 | 0.6620 |

**Why all three agree exactly.** Pool depth (unpublished candidates surviving the >=60-bar and
gradeability screens) is **uniform within a night** — the pool a pick draws its 10 nearest controls
from does not depend on which pick is matching to it (no direction or other pick-specific filter
narrows the pool, per Q006 §3 B1 / Q031 §2.2 step 2) — and pool depth never falls below 37 on any of
the 48 matured nights (see (b)). So the >=5- and >=10-control floors never bind, and "drop the thin
pick" never drops anything: the only binding constraint in this population is the **valid-pick
count**, which is 0 on exactly one night (`2026-06-02`) and >=4 on every other matured night. All three
rules therefore collapse to "does the night have >=3 (or >=1) valid picks" on this freeze, and the
answer flips on the same single night regardless of which threshold (1 or 3) is used, because
`2026-06-02` has zero valid picks, not a thin count.

By month: June (20 nights) 19/20 contributing (the one miss is `2026-06-02`); July (20 nights) 20/20;
August (8 nights) 8/8.

## (b) Matched-control pool depth

Pool = unpublished `sas_candidates` rows on night t (not `qualified IS TRUE AND selected_rank IS NOT
NULL`) with >=60 prior split-adjusted daily bars and gradeable to t+20 (bars cover t+1..t+20, no gap) —
the same population screens series A's eligible-row funnel uses, restricted to unpublished rows, with
no direction filter (Q006 §2's control-pool definition carries none).

**Per night: min 37, median 54, max 60** (mean 49.8), across all 48 matured nights.
**Nights with pool depth < 10: 0. Nights with pool depth < 5: 0.** The pool never comes close to
either floor — the smallest pool (37, on `2026-06-01`) is still 7.4x the registered floor.

**Per pick:** identical to the per-night figure for every pick on that night — the pool is a
night-level quantity, not a pick-level one, because nothing in §2.2 step 2's matching narrows the pool
by the pick's own direction or features before the nearest-10 selection. This is stated explicitly
because R1(a) was designed to reveal a cost that, measured, is zero.

## (c) Invalid-target count

Published rows on the 48 matured nights: **383** (`qualified IS TRUE AND selected_rank IS NOT NULL`).
`d_p = dir_p x (L3_p - C_p) / ATR_p`, `L3_p` = `lane_plans.swing_trading.targets[0]`, `C_p` = the
pick-night close from `prices_daily_split`, ATR = desk-computed ATR14 from bars <= t (never `atr_pct`,
never `spot_close` — PI-003).

| category | rows | reason |
|---|---:|---|
| valid | 348 | passes all four checks below |
| no `lane_plans` at all | 8 | all 8 on `2026-06-02` — `analysis_status="disabled"` signature, same night `STEWARD_Q027_exposure.md` flagged |
| wrong side (`d_p <= 0`) | 2 | L3 already on the wrong side of `C_p` |
| split-scale payload screen fails (entry ratio outside [0.85, 1.15] **and** a flattened lane level >20 ATR from `C_p`, jointly) | 19 | Q027 §2.4's screen, reused verbatim |
| `d_p` outside `[0.25, 10]` ATR | 6 | validity bound |
| **total invalid** | **35** | — |

348 + 35 = 383, reconciles exactly. Every invalid row is excluded from its night's valid-pick count
and counted here, never silently dropped (per §2.4).

## (d) Valid-pick-per-night distribution

Across the 48 matured nights: **min 0, median 8.0, max 10** (mean 7.25). Excluding the one
zero-valid-pick night (`2026-06-02`): **min 4** (three nights: `2026-06-18`, `2026-07-30`,
`2026-07-31`), median 8.0, max 10 (`2026-07-10`, a night with more than 8 published rows — consistent
with the `publication_floor` config change in-window widening the published slate on some nights).
**The >=3 floor is cleared by every contributing night with room to spare**: only 3 of the 47
contributing nights sit as low as 4, none between 1 and 3.

## (e) Series A reconfirmation and both-series overlap

Series A's contributing-night definition (Q027 §2.5, adopted verbatim) was **independently
recomputed** from `v001_sas_candidates.parquet` and `p001_daily_split.parquet` — not copied from
`STEWARD_Q027_exposure.md` — and returns **48/71 = 0.6761/elapsed session**, matching exactly.
**Stated as confirmed, not assumed**: the two counts of the same definition on the same freeze agree,
so this is not a DP-50(a) finding.

**Nights contributing to series A but not series B: 1** (`2026-06-02` — 42 eligible candidate rows,
clears series A's >=30 floor, but 0 valid published picks). **Nights contributing to series B but not
series A: 0** (series A contributes on all 48 matured nights; series B's population is a subset).
**Nights contributing to both: 47.**

## (f) DP-50(a)/(b) commit sweep and v1.7 schedule check

`fa70688bc252d14f8d67e371afafc194731c324e` reconfirmed as ancestor of `HEAD`
(`git merge-base --is-ancestor`, read-only, against the pinned platform repository). **`HEAD` is
unchanged at `d19c9a9`** — the same commit `STEWARD_Q027_exposure.md` measured on this same date
(2026-09-14) — so this is not a new sweep result, it is a reconfirmation that **zero commits have
landed since**:

| commit | date (ET) | touches the three named SAS files? |
|---|---|---|
| `2d5776c` PI-001: floor the legacy outcome backfill window | 2026-09-13 | No — nightly-pipeline entrypoint + test only |
| `4775e49` merge PR #26 | 2026-09-13 | — |
| `22a2e1b` EN-002: speed-to-target internal card (flag off) | 2026-09-13 | No — new files only (`services/sas_speed_to_target.py`, `routers/admin_sas_speed.py`, `app.py` +2 lines, docs, tests); confirmed via `git diff --stat` neither scoring nor conviction-card file appears |
| `d19c9a9` merge PR #27 | 2026-09-13 | — |

**Answer: NONE.** No weight, timeframe multiplier, `qualification_threshold`, ATR-elite cap,
GEX-missingness offset, scoring enable-flag, `publication_floor` or `bear_publish_threshold` changed
in the platform code since `fa70688`.

**v1.7 schedule check (`docs/SAS_SCORING_RESEARCH_PLAN.md`):** drafted 2026-08-26, explicitly headed
*"Status: PROPOSAL — not a decision record... Owner sign-off required before any workstream starts."*
The sequencing table is in **relative weeks** (Phase 1 wk 1-2 ... Phase 5 wk 8+: assemble v1.7 -> >=4
weeks shadow-parallel dark -> promotion review), with **no calendar anchor** and **no commit anywhere
in the repo showing the workstream has started** (the sweep above is clean). **No v1.7 promotion date
is scheduled inside 2026-09-15..2027-07-12 — or anywhere else — because no start date exists to count
weeks from.** This is stated as an absence of a schedule, not a guarantee: promotion criterion 5 in
the plan itself requires >=4 weeks dark shadow-parallel with zero incidents before any flip, and even a
same-day sign-off today would put the earliest possible promotion around wk 12+ (approx mid-December
2026, inside the window) — so R1(f)'s commit sweep should be repeated at every future freeze per
§5.3 R2(vi) and DECISIONS item 13, not assumed clear from this reading alone.

---

## Branch determination (§5.1, Correction 1)

**Threshold for "nothing changes" (branch i): >=0.6723 contributing nights per elapsed session**
(80 across the first 119 sessions — the per-block floor, not 100 over 149, per Correction 1).
**Measured series-B rate: 0.6620/session. 0.6620 < 0.6723 -> branch (i) does not fire.**

**Branch (ii) test: does a window end recomputed as the later of the two series' own floor dates,
checked per block, still decide inside DP-43's 12-month ceiling (2027-09-14)?**

Projected date each floor is first reached, at each series' own measured rate:

| floor | series | rate | sessions needed (own funnel) | date |
|---|---|---:|---:|---|
| A: >=80 contributing across `W1UW2` (DP-21) | A | 0.6761 | 119 | 2027-03-05 |
| A: >=80 contributing across `W1UW2` (DP-21) | B | 0.6620 | 121 | 2027-03-09 |
| B: >=20 contributing in `W3` (DP-21 cell floor) | A | 0.6761 | +30 (total 149) | 2027-04-19 |
| B: >=20 contributing in `W3` (DP-21 cell floor) | B | 0.6620 | +31 (total 152, own funnel) | 2027-04-22 |
| C: >=30 dated after lock commit (DP-24) | A | 0.6761 | 45 | 2026-11-16 |
| C: >=30 dated after lock commit (DP-24) | B | 0.6620 | 46 | 2026-11-17 |

Series B's own two floors, summed independently (121+31=152 sessions), are **not** the answer,
because one set of 40/40/20 block cuts must satisfy **both** floors for the **slower** series
**simultaneously** — the exact arithmetic Correction 1 exists to police (a naive 100/rate or a
sum-of-independent-floors reading understates the window by 1-3 sessions here, the same class of
error as the original draft's 0.671 slip). Solving for the smallest total window `S` such that
`round(0.8*S)*0.6620 >= 80` **and** `(S - round(0.8*S))*0.6620 >= 20` simultaneously:

| S (sessions) | `W1UW2` | `W3` | series B contributing in `W1UW2` | series B contributing in `W3` | both floors met? |
|---:|---:|---:|---:|---:|---|
| 149 (original) | 119 | 30 | 78.8 | 19.9 | no |
| 152 | 122 | 30 | 80.8 | 19.9 | no (W3 short) |
| **153** | **122** | **31** | **80.8** | **20.5** | **yes — minimal S** |

**Recomputed window: pick nights 2026-09-15..2027-04-23 = 153 elapsed sessions** (up from 149), blocks
re-cut at the registered 40/40/20 proportion: `W1` sessions 1-61 (2026-09-15..2026-12-09), `W2` 62-122
(2026-12-10..2027-03-10), `W3` 123-153 (2027-03-11..2027-04-23). Series A clears both floors inside
this same window with room to spare (`W1UW2` at 0.6761/session projects 82.5 contributing; `W3`
projects 21.0).

**Decision date:** window end 2027-04-23 + 20 sessions maturity = 2027-05-21, + one calendar week
= 2027-05-28, first Monday on or after = 2027-05-31 — **a listed market holiday (Memorial Day)** — so
the next Monday, **Monday 2027-06-07**, is the decision date. **8.7 months from the 2026-09-14 lock —
inside DP-43's 12-month ceiling (2027-09-14) by 3.3 months.**

**Branch (ii) fires.** The window end moves out for both series (2026-09-15..2027-04-19 ->
2026-09-15..2027-04-23; one window, one freeze, one set of blocks, out only, never in), the decision
date moves out (Monday 2027-05-24 -> Monday 2027-06-07), the blocks are re-cut at the same 40/40/20
proportion applied to the longer window, and **`m = 2` stands — series B is not demoted.** Branch
(iii) (demotion to descriptive, `m = 1`) does **not** fire: an admissible window that reaches 100
contributing nights for series B (80 + 20+ = 101 at the recomputed cuts) exists well inside the
ceiling.

**Floor C (DP-24, >=30 dated after lock commit) is non-binding for either series** at the recomputed
window — satisfied by session 46 (2026-11-17) at the latest, versus a window end of session 153
(2027-04-23).

**No sub-cell projection is requested by R1 and none is printed here** — R1's sub-cell flag request
(§5.3's final sentence) concerns Q031's own §4.3 panels, which have not been re-derived from this
count; that is a `record`-stage task for the Registrar/Decision-maker, not this report.

---

## What this does and does not decide

This is a counts-only exposure measurement. No touch rate, return, excursion, plan result, or
score-vs-outcome relationship appears anywhere above. The registered contributing-night rule for
either series **does not change** on this measurement — only the window end, the decision date, and
whether `m = 2` or `m = 1` do, per §5.1's demotion rule (settled at lock, DP-43). I report the branch
the counts imply; the Registrar/Decision-maker applies it at `record` and locks the file. The DP-13
extension and DEFERRED fallback remain in the file exactly as registered, keyed to `eval.py`'s own
measured counts at the (now 2027-06-07) decision pass — nothing here fires either of those, they are
unaffected mechanisms, not measured here.
