# Q031 — edge_decay: is the SAS edge deteriorating over time, or is a weak stretch normal variation?

**Status:** PREREG_DRAFT (lock by committing this file)
**Family:** **F2 Calibration** (hypothesis **H-082**, Haci's Master Hypothesis Program **H12**,
*Edge decay*). The primary endpoints' subject is whether a measured edge statistic holds its level
over time, which is calibration of the desk's own claims (DP-29). The `E_t` series additionally
carries a companion correction in **F1** (§7).
**Manifest (sealed post-hoc panel and the borrowed exposure count only):**
research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA
fa70688bc252d14f8d67e371afafc194731c324e).
**Manifest (prices, sealed post-hoc panel only):** research/data/manifest_prices_v001.json
(as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374).
**Successor freezes — the question itself (built and pinned at the decision date, DP-23; §5.3 R2):**
a selection freeze (`sas_candidates` **every row, published and unpublished**, `sas_runs`,
`market_regime_daily`) and a price freeze (daily bars for **every candidate symbol on every in-window
night**), covering pick nights **2026-09-15 .. 2027-04-23** with daily bars through **2027-05-21**
(session t+20 of the last included pick night) and ≥ 60 prior sessions before 2026-09-15; a second
pair **only if** the single DP-13 extension fires, covering pick nights **.. 2027-06-07** with bars
through **2027-07-07**. **Every night that carries a verdict here is after this lock and exists in no
manifest pinned today**, so the population enters only through those successor freezes
(`pin_at_decision`, DP-23 — the Q024 / Q027 pattern). They are named in prose and deliberately not
written as `**Manifest …:**` header lines, because no such file exists yet and the pin step reads
every `**Manifest` line as a path.
**Exclusions:** research/data/exclusions_v003.json (DP-22, the newest file) unioned with the
**add-only successor exclusions file** issued with the successor selection freeze — the identical
**four** criteria Q027 fixes at its lock (`manual_runs` ∪ `non_session_runs` ∪
`uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10.
The successor file may only **add** nights; no night is removed from a v003 list; the **criteria**
are fixed at this lock even though the **dates** cannot be. Both paths are `eval.py` inputs; no
hard-coded file name, no hard-coded date. DP-04 applies mechanically on top.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14 · **Decisions:** DECISIONS.md

---

## 1. Hypothesis (plain English)

**If SAS has an edge at the start of this window, that edge is still the same size at the end of it —
a weak month is normal variation, not the system wearing out.**

BACKLOG **H-082** (Haci's H12) reads: *"Edge decay: is recent weakness temporary or structural —
PASS rolling IC / expectancy recovers or stays within historical variation; FAIL persistent
deterioration across independent windows → retire or retrain the affected component."* It names the
series (H-073's per-night IC, Q006's control-adjusted `E_t`, plus H-075's per-layer ICs for
attribution), the test form (a change-point test with a persistence requirement) and the MPEs
(5.0 pp on `E_t`, ρ 0.05 on the IC). This PREREG fixes the blocks, the estimator, the nulls, the
floors, the schedule and the decision rule.

**Two primaries** (§4), both night-level, both two-sided, one per series:

- **P1 — the ranking series.** `D1ᴬ` = the mean per-night information coefficient in the **second**
  block of the window minus the same quantity in the **first** block. Series `S^A_t` = Q027's `IC_t`
  (Spearman ρ between `overall_score` and the path-outcome rank across every eligible candidate that
  night, at the night's common ATR distance, 20 sessions from the t+1 open). **MPE `|D1ᴬ| ≥ 0.05`**
  in Spearman-ρ units.
- **P2 — the selection series.** `D1ᴮ` = the mean per-night **control-adjusted L3-touch excess** of
  the published slate in the second block minus the first. Series `S^B_t` = Q006 §3's `Delta_t` on
  the DP-09 clock (each pick's own printed L3 distance, ten distance-matched same-night unpublished
  controls at the identical ATR distance, first touch within 20 sessions from the t+1 open).
  **MPE `|D1ᴮ| ≥ 5.0 pp`** (DP-20).

**What the question is *not*.** It does **not** test whether SAS has an edge — that is Q006 (F1,
decides 2026-10-05) and Q027 (F2, decides 2027-04-12). A `STABLE` verdict here means "the series did
not move", which is equally true of an edge that was never there. §8 therefore carries a
**precondition**: if the reference block's own level is below the edge MPE, the endpoint is reported
`NO_EDGE_TO_DECAY` and decides nothing about decay.

**Why the window starts after the lock, and why "since April" is not the question.** The desk has
already read the sealed period for exactly this hypothesis: the weekly §7 rolling four-week 90+
trend, H-010's snapshot of the 90+ return lead fading from April to August, and Q005's measured
halving of the elite-candidate rate (0.50 → 0.245 per night, p = 0.016, cause INCONCLUSIVE). Those
reads are what *motivated* H-082, so a test that uses them as its reference level would be testing
the thing that generated the hypothesis. The sealed stretch prints once as a labelled post-hoc panel
(§6) that enters **no verdict, no block, no CI comparison and no q**, and it is **never** the
reference block. What is registrable, and what this file registers, is whether the edge series
deteriorates across a pre-registered forward window.

**Direction of the claim.** H-082 predicts `D1 < 0` (deterioration). Both primaries are registered
**two-sided**: a confirmed *improvement* would be as consequential — it would mean the sealed-period
weakness was the tape, not the system — and §9 says what each licenses.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Candidate and pick rows are reduced to one
  statistic per night first; nights are the observations; the primaries are contrasts of block means
  over those nights. Control rows never add to n.

### 2.0 Machinery adopted by reference — one construction, two questions

**Series `S^A` is computed with Q027's machinery, adopted verbatim as Q027 registers it at its lock
commit** (`research/questions/Q027_score_ranking_validity/PREREG.md`): §2.1's eligible-row filter
(every scored `sas_candidates` row, published or not, `dominant_direction IN ('bullish','bearish')`,
≥ 60 split-adjusted daily bars ≤ t, gradeable t+1..t+20), §2.2's common ATR distance `d*_t` and its
thin-slate / absent-slate rules, §2.3's entry, clock, `hit_i`, `s_i` and path-outcome rank `u_i`,
§2.4's exclusions, §2.5's contributing-night and episode definitions, and §4.1's `IC_t`. Nothing is
re-specified here. **One machinery, two questions**: Q027 asks whether `IC_t` has a level, Q031 asks
whether that level moves, and the only difference between them is the statistic taken over the night
series — not the funnel, not the distance, not the clock, not the grading.

**Series `S^B` is computed with Q006's machinery** (`research/questions/Q006_control_cohort_path/`
§2 treatment rows, §3 B1 distance-matched control, §4 entry basis), on the **DP-09 clock of 20
sessions** rather than Q006's own 40 — the spread horizon, the same clock `S^A` runs on, so the two
series share one maturity horizon, one successor freeze and one contributing-night calendar. Q006's
40-session version is printed beside it, descriptively, wherever it has matured (DP-09).

`eval.py` **recomputes both series from the pinned freezes**. It never reads another question's
`results/` directory, and no number in this file is inherited from a Q006, Q027 or Q029 output.

### 2.1 Series A — the ranking series `S^A_t`

For each contributing night t (§2.5): `S^A_t = IC_t` = the Spearman rank correlation, over that
night's eligible candidate rows, between `overall_score` and the path-outcome rank `u_i` (touchers
ordered fastest-first, every non-toucher tied below every toucher), with mid-rank tie correction on
both variables. The target for every row is at the night's common distance `d*_t` in that row's own
ATR and direction, and the entry is the session t+1 open (DP-03(b), DP-42). Units: Spearman ρ.

### 2.2 Series B — the selection series `S^B_t`

For each contributing night t, over that night's eligible **published** picks (DP-28:
`qualified IS TRUE AND selected_rank IS NOT NULL`; dark-lane rows are not published and enter only
the control pool):

1. `d_p = dir_p × (L3_p − C_p) / ATR_p`, the pick's **own printed** swing first target in its own
   ATR units (`lane_plans.swing_trading.targets[0]`, volatilx
   `services/sas_conviction_card.py:182-187`), with `C_p` the actual pick-night close from
   `prices_daily_split` and ATR = ATR14 from bars ≤ t (never `spot_close`, never `atr_pct` — PI-003,
   EXPLORE_001 §9). A pick whose L3 is already on the wrong side of `C_p`, or which fails Q027
   §2.4's split-scale payload screen, or whose `d_p` falls outside `[0.25, 10]` ATR, is an **invalid
   target**: excluded and counted (Q006 §2).
2. **Controls:** the **ten nearest** same-night **unpublished** candidates by Euclidean distance on
   (`beta60`, `atr_pct`, `runup20`), each feature standardized by the **night's** cross-sectional
   median and MAD; with replacement across picks within a night; ties broken by symbol ascending
   (Q006 §3 B1 steps 1–3, verbatim). Each control carries a synthetic target at **the same ATR
   distance `d_p` and the same direction**.
3. **Grading:** entry = the session t+1 open for pick and controls alike; a target already through
   the entry price is **not a hit** (rule 5, DP-26) and the row stays in the denominator; first touch
   of the regular-session high (bullish) / low (bearish) within t+1..t+20; a gap through the target
   at an open is a touch; split factors snapped. **No stop, ever** (DP-02).
4. `Delta_p = hit_p − mean over p's ten controls of hit_c`, and
   **`S^B_t` = mean over the night's eligible picks of `Delta_p`**, in percentage points.

**Why `E_t` and not the raw touch rate.** The engine's own target distance moves: R1(c) of
`STEWARD_Q027_exposure.md` measured the night's median printed L3 distance going from ≈ 1.06 to
≈ 2.10 ATR across a single 2026-07-08 publication-gate ship, with no scoring field moving at all. A
raw touch-rate series would fall by construction when the engine aims further, and "the engine aimed
further" is not edge decay. The control is graded at the **same** distance as its pick, so that move
cancels at first order. It is still the leading alternative explanation, and §4.3 prints the
distance series beside the edge series for exactly that reason.

### 2.3 The blocks — fixed at this lock, by session index

The window (§5.2) is **pick nights 2026-09-15 .. 2027-04-23 = 153 elapsed sessions**, cut into three
consecutive, non-overlapping blocks by **elapsed-session index**, fixed here and not reopened. The
cuts are the registered 40 / 40 / 20 proportions applied to the 153-session window and rounded
(0.4 × 153 = 61.2 → 61; 0.8 × 153 = 122.4 → 122):

| block | sessions | projected dates | role | proj. contributing nights, **series A** (measured 0.6761) | proj. contributing nights, **series B** (measured 0.6620) |
|---|---|---|---|---:|---:|
| **W1** | 1 .. 61 | 2026-09-15 .. 2026-12-09 | reference | 41.2 | 40.4 |
| **W2** | 62 .. 122 | 2026-12-10 .. 2027-03-10 | test | 41.2 | 40.4 |
| **W3** | 123 .. 153 | 2027-03-11 .. 2027-04-23 | persistence holdout | 21.0 | 20.5 |

- **The two projection columns are never pooled.** `W1 ∪ W2` = **82.5** contributing nights for
  series A and **80.8** for series B; every block clears DP-21's cell floor of 20 and both series
  clear 80 across `W1 ∪ W2` for their own primary, so **no arm is demoted to descriptive (DP-43) and
  `m = 2` stands** (§7). §2.5 gives the two series their own contributing-night sets and their own
  floors, and each floor is checked against each series separately.
- The dates are the trading calendar's, cross-checked against `STEWARD_Q027_exposure.md`'s own
  arithmetic (session 84 = 2027-01-13, 92 = 2027-01-26, 119 = 2027-03-05) and
  **re-confirmed session by session from the calendar when the successor freeze is built**; a
  correction may move a boundary **out, never in**.
- **Proportions, not dates, are what is registered:** 40% / 40% / 20% of the window's elapsed
  sessions, rounded as above. This is what was applied at `record` when the window lengthened from
  149 to 153 sessions (§5.1), and it is what applies under the single DP-13 extension: on the
  extension path the same proportions give `W1` **1 .. 73** (2026-09-15..2026-12-28), `W2`
  **74 .. 146** (2026-12-29..2027-04-14), `W3` **147 .. 183** (2027-04-15..2027-06-07) — printed
  here so the extension's cuts are fixed blind. The blocks are never re-cut after any outcome is read.
- A night is assigned to a block by its **own pick date**, before any outcome exists. No block
  boundary depends on a measured value.

### 2.4 Exclusions — each counted, printed in the results header, never silently dropped

Q027 §2.4's list is adopted whole and applies to both series: excluded nights (the four-criteria
union above, plus DP-04 late-`finished_at` and non-session nights); `mixed`-direction rows excluded
and counted; rows with fewer than 60 prior split-adjusted bars excluded and counted (the CTRA
truncated-history signature); ungradeable rows excluded and counted, with a night dropped above 10%;
the split-scale payload screen on published rows; immature nights excluded and counted, never graded
as non-touches; a night below 30 eligible rows **non-contributing for `S^A`**, counted, not an
exclusion. Series `S^B` adds one exclusion of its own: a pick with an **invalid target** (§2.2 step
1) is excluded and counted, and a night is **non-contributing for `S^B`** if fewer than **3** valid
picks remain or if any retained pick has fewer than **5** matched controls (a DP-26 convention — the
analogue of Q027's ≥ 30-eligible-rows rule, and the stricter of the two floors on offer, Q006's own
rule being ≥ 1 pick). **R1 measured the contributing-night rate under both forms, and the stricter
one costs nothing:** on the 48 matured nights the matched-control pool depth never fell below 37
(median 54, max 60), so the registered rule, Q006's ≥ 1-pick rule and the drop-the-thin-pick variant
all return the same 47/71, and the only binding night is 2026-06-02, which carries *zero* valid picks
and is already excluded by the `payload_disabled_runs` criterion. That is a measured fact and **not**
a reason the rule could have been relaxed (DP-21, DP-45); the rule is registered exactly as drafted.

**No outcome column is ever an input.** `outcome_*`, `sas_selection_excursion.*` and `level_hit_*`
are not joined; `uoa_symbol_daily.fwd_return_*` is banned outright (FREEZE_v001 §5). Every outcome
here is computed from pinned bars, which is also the only way the unpublished control rows can be
graded at all (FREEZE_v001 §4: 0 of 5,572 non-qualified rows sealed).

### 2.5 Contributing night, and the episode (DP-51)

- **Contributing night, series A:** Q027 §2.5's complete definition, unchanged — a non-excluded
  in-window night, matured to t+20, with ≥ 30 eligible rows, both terciles non-empty and a defined
  `d*_t`. Measured rate **0.6761 per elapsed session (48/71)**.
- **Contributing night, series B:** a non-excluded in-window night, matured to t+20, with ≥ 3 valid
  published picks each carrying ≥ 5 matched controls (§2.4). Measured rate **0.6620 per elapsed
  session (47/71)** — `research/reports/STEWARD_Q031_exposure.md` (a), R1, closed (§5.3).
- **The two series have their own contributing-night sets and their own floors.** A night that
  contributes to one and not the other is printed in both funnels and is never back-filled. On the
  sealed stretch R1(e) measured **47 nights contributing to both** of the 48 / 47 (series A / series
  B) — the two sets are close but not identical, and no floor, projection or block count in this file
  pools them.
- **Episode (DP-51, the H-070 unit):** one **symbol's** run of appearances — as an eligible candidate
  row for `S^A`, as a published pick for `S^B` — with gaps of ≤ 10 sessions between successive
  appearances; 11 or more sessions starts a new episode. Episodes are the second resampling unit in
  §4.4. Q027 R1(e) measured the structure this answers on the sealed stretch: 400 symbols, 811
  episodes, **70% of symbols recurring across more than one episode**, longest episode 44 appearances
  over 71 sessions.

## 3. Baselines — what this must beat

There is always a baseline. For a decay question the baseline is **the series' own behaviour when
nothing changed**, and it takes three forms, all registered here:

- **B1 (primary null, and the CUSUM's null): the same series with time order destroyed, locally.**
  A **circular block permutation** of the ordered night series with expected block length **10
  sessions** (the desk's standing value — Q004 / Q007 / Q009 / Q011 / Q015 / Q023 / Q027 — and a
  registrar convention fixed at lock, DP-26), 10,000 draws, seed 20260914, two-sided. Under it the series has the same marginal distribution and the
  same short-run dependence but no level shift, which is exactly the null "nothing happened over
  time". **This is a deliberate re-specification of H-082's "shuffle nights within episodes"**, and
  the reason is stated rather than buried: a plain shuffle destroys the series' autocorrelation, so a
  slowly-drifting but stationary series would be called a break far too often. The episode is a
  *cross-sectional* clustering unit, and DP-51 puts it where it belongs — in the CIs (§4.4), not in
  the time null.
- **B2 (the "historical variation" band H-082 names): a stationary block bootstrap of the reference
  block `W1`**, expected block length 10 sessions, 2,000 resamples, giving the interval within which
  a later block mean is *ordinary*. The observed `W2` and `W3` means are printed against it. This is
  the literal form of Haci's PASS line ("stays within historical variation") and it is a **reported
  companion, not a substitute for the MPE** — an interval that happens to be wide never lowers the
  bar in §8.
- **B3 (rule 5's distance-matched control, inside both series by construction):** every candidate on
  a night is asked to travel the same number of its **own** ATRs (`S^A`, §2.1), and every control is
  graded at its pick's **own** ATR distance (`S^B`, §2.2). A touch rate from this question is never
  reported without that sentence attached.
- **B4 (the competing-explanation baseline, blocking for a DECAY verdict, §8 clause 7):** the same
  block contrast with `W2`'s and `W3`'s nights **reweighted to `W1`'s composition** on the coarse
  trailing tape sign `tape_sign_t` ∈ {up, down} (the sign of SPY's trailing 20-session return from
  bars ≤ t — knowledge-time legal, and coarse precisely so it is estimable at ~40 nights a block). If
  a fall disappears under reweighting, what moved was the tape, and **that is H-079's question, not
  this one**.
- **B5 (descriptive, never decides): the sealed post-hoc panel** (§6) — both series on pick nights
  2026-06-01..2026-08-12 from `manifest_v001` + `manifest_prices_v001`, split at 2026-07-06. It gives
  the reader a sense of scale and **enters no verdict, no block, no CI comparison and no q**.

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Nothing in this question is decided by a fixed-horizon return.** Both series are built from first
touches of a target at a stated ATR distance from a stated entry, against a distance-matched control.
Close-to-close returns at T+5 and T+20, and the per-night *return* IC, are printed as the series
H-073 explicitly says "print and decide nothing" — and that matters more here than anywhere, because
**the sealed reads that motivated H-082 were returns**.

### 4.1 Per night

`S^A_t` (§2.1, Spearman ρ) and `S^B_t` (§2.2, percentage points), one value each per contributing
night, computed before any block statistic.

### 4.2 Primary endpoints

For each series `S ∈ {A, B}`, with `m̄(W)` the mean of `S_t` over the contributing nights of block W:

- **P1 / P2 — the block contrast:** `D1 = m̄(W2) − m̄(W1)`.
  **MPE: `|D1ᴬ| ≥ 0.05`** (Spearman ρ) and **`|D1ᴮ| ≥ 5.0 pp`** (DP-20).
- **The persistence contrast (blocking, not a third and fourth primary):** `D2 = m̄(W3) − m̄(W1)`,
  in the same units, evaluated against the same MPE. H-082's own rule — *"FAIL declared only if …
  and the deficit persists in the next independent window; a single bad quarter is INCONCLUSIVE by
  construction"* — is registered as §8 clause 5, not as a reported statistic.
- **The change-point clause (blocking, not a primary):** the mean-shift CUSUM over the **whole**
  registered series, `M = max_k |Z_k|` with
  `Z_k = (m̄(1..k) − m̄(k+1..n)) / sqrt(σ̂²(1/k + 1/(n−k)))`, `σ̂²` pooled, the search **trimmed to
  leave ≥ 20 contributing nights on each side** (DP-21's cell floor), p from B1's circular block
  permutation. `τ̂` and its date are printed. This is H-082's named test, kept in the role it can
  honestly fill — *is there a break, and where* — while the magnitude lives on blocks fixed before
  any data existed.

**On the estimator, stated once.** A magnitude read at a **data-chosen** change point is biased away
from zero by the search itself, and its two segments have no sample size known at lock, so no floor
can be written for it. The fixed blocks have both: `D1`'s n is known today, its estimate is unbiased
with respect to any search, and a contrast of an early block against a later one has power against a
**gradual** decline as well as a step — which is the shape PI-010's falling elite count and Q005's
drifting score distribution would produce. The τ̂-based magnitude is printed as a descriptive
companion with its selection caveat attached (§4.3).

**On the MPEs.** `5.0 pp` is DP-20 and `0.05` is Haci's own H3 number, both as H-082 names them
(DP-25). **DP-20's doubling clause is considered and declined, with the reason**: `D1ᴮ` is formally a
difference of differences, but `S^B_t` is already control-adjusted and a full collapse of the edge —
from a level of, say, 8 pp to zero — would be **below a 10.0 pp bar and therefore unconfirmable by
construction**, which is a validity failure rather than conservatism (the Q029 §4.2 reasoning). The
same argument binds harder on the IC, where the level MPE *is* 0.05: a 0.10 decay bar would require
the IC to have exceeded 0.10 and then gone negative. What replaces the doubling, and is strictly
harder than the bare MPE, is **clause 6's level gate** (§8): a decay verdict also requires the later
block's own level to have fallen below the edge MPE. A fall from excellent to good is not a reason to
retire a component. **Neither MPE is lowered at the decision pass in any branch.**

### 4.3 Secondary, stratum and sensitivity output

Everything here prints raw p only and is labelled *"descriptive, does not decide"* — **except the
named blockers** (§8 clauses 5–8), which carry no verdict of their own but block a DECAY verdict.

**The attribution limb (H-082's own third series; descriptive, licenses nothing).** The per-layer
per-night marginal Spearman IC of Q029's `E1ⱼ` — for every layer Q029 registers as evaluable — as its
own night series, with `D1`, `D2` and the CUSUM computed on each. **No MPE, no q, no correction set,
no verdict**: Q029 owns the layer endpoints (DP-29) and a layer that moves here is a *lead* for the
Reporter's synthesis, never a finding. This is what makes a confirmed decay attributable rather than
merely announced, and §9 forbids retiring any component on it alone.

**The "what else moved" panel — mandatory, descriptive, printed as night series across the whole
window beside the two edge series.** Each is a competing explanation for a fall, and each is why a
decay verdict is a beginning and not a conclusion:

- the night's common ATR distance `d*_t` and the distribution of the picks' **own printed** L3
  distances (the "the engine aimed further" explanation — R1(c)'s 1.06 → 2.10 ATR shift);
- the **unconditional touch rate** of the night's candidates and of the control pool (the tape);
- `sas_runs.config_json` field by field per night — weights, timeframe multipliers,
  `qualification_threshold`, both ATR-elite caps, the GEX offset, the enrichment enable-flags,
  `publication_floor`, `bear_publish_threshold` (H-014's "configuration change brackets the fall",
  re-specified there so it can only fire on fields that can mechanically move `overall_score`);
- the **published count**, the **elite (≥ 90) candidate count** and the **score IQR** per night
  (PI-010's falling elite count; Q005's compression, INCONCLUSIVE on cause);
- the per-night eligible-row count, the mixed share, the not-takeable share and the counter-direction
  touch rate at `−d*_t` (reported, never an exit — DP-02).

**Also computed, blocking (§8):** the B4 tape-composition-reweighted `D1` and `D2`; the
`C_t`-entry-basis version of both primaries (DP-03(a) / DP-11) as a named sensitivity; the
**bull-only** version of both primaries; and, for `S^B`, the 40-session companion (DP-09).

**Also computed, descriptive:** the τ̂-based magnitude with its selection caveat; the Spearman ρ
between night index and `S_t` (a monotone-trend read); a rolling 20-night mean of each series, which
is the exact quantity **EN-017** would compute nightly in production; monthly block means; the two
series plotted against each other (a fall in one and not the other is informative and is reported as
such); the per-night return IC and T+5 / T+20 returns (rule 5, DP-01 — they never decide, and no
verdict sentence may lead with them).

**Regime stratification (rule 7).** `market_regime_daily.market_regime` (v1.2 only, the
`trading_date = t` row, legal only where `created_at` falls on that date at or before that night's
own `sas_runs.finished_at` — Q023 §2.2's timestamp test) and `tape_t` (Q027 §6's SPY proxy) are
reported as the **composition of each block**, not as arms: the question is time, and a regime cell
crossed with a block would be far below any floor. The **coarse** `tape_sign_t` reweighting is B4 and
is blocking. A cell with fewer than 20 measured contributing nights is **SUPPRESSED** (counts only);
suppression restricts affirmative reporting and never removes a blocker.

**Quotability:** 20-session basis, W20 research window → **every number in this question is
`NON_QUOTABLE`** (rule 12).

### 4.4 Inference — two CIs per primary (DP-51)

Night-level throughout. Control rows never add to n (rule 6).

- **CI 1 — date-clustered (the registered bootstrap):** resample contributing nights with
  replacement **within each block**, 2,000 resamples, recomputing `m̄(W1)`, `m̄(W2)`, `m̄(W3)`, `D1`
  and `D2`. A **stationary block bootstrap** over the ordered nights within each block (expected
  block length **10 sessions**, fixed at lock) is printed beside it.
- **CI 2 — episode-clustered (DP-51):** resample **symbol-episodes** (§2.5) with replacement **and**
  nights with replacement, jointly; keep the rows in the intersection; recompute each retained
  night's `S_t` from the surviving rows (a night is retained only if it still meets its
  contributing-night rule), then the block means and `D1` / `D2`. 2,000 resamples, same seed. This is
  the CI that absorbs one symbol's overlapping 20-session paths being counted on twenty consecutive
  nights — and it matters more here than in Q027, because a single long episode can sit almost
  entirely inside one block and move that block's mean on its own.
- **DP-51 is a decision rule here, not a footnote: a primary that clears MPE with CI 1 excluding 0
  but CI 2 including 0 is INCONCLUSIVE, never CONFIRMED** (§8 clause 4).
- **p-value (decides, feeds BH):** B1's circular block permutation of the night series, 10,000 draws,
  seed 20260914, two-sided, applied to `D1` — the same null the CUSUM clause uses.
- **Every estimate prints:** contributing nights per block per series; eligible rows (and valid
  picks / matched controls) per night, min / median / max; distinct symbols and **episodes** per
  block with the episode-length distribution; contributing nights dated after the lock commit;
  `d*_t` and printed-distance distributions per block; not-takeable counts; rows and nights excluded
  by reason; and the block-composition table (regime, tape, direction, band).

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** — met by
  `W1 ∪ W2`, the two blocks `D1` contrasts — and ≥ **20 contributing nights per reported cell**, met
  by each of the three blocks and required of every reported sub-cell. The weaker "80 eligible with
  ≥ 20 contributing" reading is not used. **No floor is ever lowered to reach a date.**
- **The persistence holdout `W3` carries the cell floor, 20 contributing nights** (DP-21), and blocks
  at whatever count it has (Q027's treatment of its halves; Q027 DECISIONS #10). The stricter reading
  — `W3` as a second full primary at 80 nights — was considered and is not taken: it requires ~140
  contributing nights per series, puts the initial decision date past DP-43's 12-month ceiling and
  would defer the question whole rather than test it. `D2` can only ever **prevent** a DECAY verdict
  (§8 clause 5) and never produce one, so the 80-night per-primary floor attaches to `D1`, which
  `W1 ∪ W2` carries.
- **DP-24:** ≥ 30 contributing nights dated after the lock commit. **Every** contributing night here
  is post-lock by construction (§6), so DP-24 binds at 30 of the 100 and is not the gate.
  **PROSPECTIVELY_CONFIRMED is reachable from this run by design; DP-31 does not apply and no
  successor replication question is needed.**
- **Binding maturity: 20 sessions**, uniform across every row of both series.
- **Total requirement: 100 contributing nights per series** (80 across `W1 ∪ W2` + 20 in `W3`).

### 5.1 Exposure basis

| quantity | measured | source |
|---|---|---|
| **contributing nights per elapsed session, series A (Q027 §2.5's complete definition)** | **0.6761** (48/71) | `research/reports/STEWARD_Q027_exposure.md` (a) — **borrowed, and named as borrowed**: identical population, identical screens, identical contributing-night rule |
| eligible nights per elapsed session before the freeze's own maturity truncation | 0.9577, with 100% (48/48) of matured nights converting | same, (a) |
| contributing nights per elapsed session, published-pick funnel (indicative for series B only) | 0.9538 (62/65) | `research/reports/STEWARD_Q023_exposure.md` §5 |
| **contributing nights per elapsed session, series B under §2.5's registered rule** | **0.6620** (47/71) | `research/reports/STEWARD_Q031_exposure.md` (a) — measured on `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`, counts only, no live query (DP-50(c)); identical under Q006's weaker ≥ 1-pick rule and under the drop-the-thin-pick variant |

Series A's rate was **re-confirmed bit-for-bit** by an independent recomputation in
`STEWARD_Q031_exposure.md` (e) — 48/71 = 0.6761, the same count of the same definition on the same
freeze — so there is **no DP-50(a) disagreement** to split anything on.

**The schedule is built on the measured rates, and on the slower of the two where they differ**,
exactly as Q027 built its own: the 0.9577 figure is an upper bound obtained by extrapolating past the
price freeze's forward-bar horizon, and DP-45 takes the measured number because the extrapolation is
the one that pulls the decision date **in** (it would decide ≈ 2027-03-29, eight weeks sooner, and
the desk does not buy eight weeks with a number it has not measured). Q023's 0.9538 published-pick
rate is indicative only and is not used either: it counts nights under a weaker contributing-night
rule than §2.5's.

**Lock-or-DEFER gate: CLEARED for both series.** The gate is not a constant: it is DP-43's 12-month
ceiling **solved at the actual lock date and rounded up**, and it is re-solved if the lock date
moves. At the **2026-09-14** lock the ceiling is 2027-09-14, so the last admissible decision Monday
is **2027-09-13**, which admits a last window end of **2027-08-06 = session 225** (2027-08-06 + 20
sessions = 2027-09-03; + one calendar week = 2027-09-10; first Monday on or after = 2027-09-13). At
S = 225 the registered 40/40/20 cuts give `W1 ∪ W2` = 180 sessions and `W3` = 45, so the gate is the
**per-block** maximum, max(80/180, 20/45) = 0.4445 → **≥ 0.45 contributing nights per elapsed
session**. Measured: series A **0.6761** (clear by 52%), series B **0.6620** (clear by 49%). Below
that line Q031 would have gone to `research/questions/DEFERRED.md` unregistered, with the measured
rate and the implied date named.

**Series B's demotion rule, settled at lock (DP-43, "an arm projected below floor is demoted at lock,
never dropped afterwards") — fired, and spent.** The rule was written with three branches fixed
before any count was seen: at a measured series-B rate **≥ 0.6723 contributing nights per elapsed
session** (the **per-block** threshold — 80 across the first 119 sessions, not 100 over the window)
nothing changed; slower, but with a window end at the later of the two series' floor dates still
deciding inside the ceiling, the **window end moved out for both series** (one window, one freeze,
one set of blocks, the 40/40/20 proportions re-applied and the session indices recomputed); slower
still, so that no admissible window reached 100 contributing nights for series B inside the ceiling,
**P2 was demoted to descriptive at this lock**, `m = 1`. **R1 measured 0.6620, so the second branch
fired**: the window end moved out from session 149 to **session 153** (2027-04-23), the blocks were
re-cut at the registered proportions (§2.3), the decision date moved out from Monday 2027-05-24 to
**Monday 2027-06-07**, **`m = 2` stands and P2 is not demoted** — every block of both series projects
≥ 20 contributing nights and both series clear 80 across `W1 ∪ W2`. No fourth branch existed, **no
floor was reduced in any branch**, and the registered contributing-night rule itself did not change
on R1 — only the dates and the demotion turned on it, and the demotion did not fire.

### 5.2 Window, decision date, extension, DEFERRED fallback (DP-43, DP-13; no outcome is looked at)

**Window: pick nights 2026-09-15 .. 2027-04-23 inclusive = 153 elapsed sessions.**
**Decision date: Monday 2027-06-07.** Single DP-13 extension to pick nights **.. 2027-06-07**
(183 sessions), decided **Monday 2027-07-19**, which is also the **hard stop**.

The window end is the **later** of the two series' floor dates at their **own** measured rates,
solved **jointly against one set of rounded 40/40/20 cuts** — not as a sum of independent floor dates
(121 + 31 = 152 is *not* the answer) and not by dividing a total by a rate. **Why 153 and not 152:**
at S = 152 the rounded cuts give `W3` = 30 sessions → 19.9 series-B contributing nights, short of 20.
S = 149 gives 78.8 nights across `W1 ∪ W2`; S = 151 and 152 give a short `W3`; **S = 153 is the
smallest window meeting both per-block floors for both series simultaneously** (80.8 and 20.5 for the
slower series).

| floor | series | rate used | sessions needed | date | binding? |
|---|---|---|---|---|---|
| **A:** ≥ 80 contributing nights across `W1 ∪ W2` (DP-21, per primary) | B (slower) | 0.6620/session | **121** | 2027-03-09 | no — cleared inside `W1 ∪ W2` |
| **A:** ≥ 80 contributing nights across `W1 ∪ W2` (DP-21, per primary) | A | 0.6761/session | **119** | 2027-03-05 | no |
| **B:** ≥ 20 contributing nights in `W3` (DP-21, cell floor) | B (slower) | 0.6620/session | **31** (in `W3`) | 2027-04-23 | **yes — the window end, solved jointly with the 40/40/20 cuts** |
| **B:** ≥ 20 contributing nights in `W3` (DP-21, cell floor) | A | 0.6761/session | 30 (of the 31 `W3` sessions) | cleared one session before the window end | no |
| **C:** ≥ 30 contributing nights dated after the lock commit (DP-24) | B (slower) | 0.6620/session | **46** | 2026-11-17 | no; satisfied by construction (45 for series A) |
| **D:** ≥ 20 contributing nights per *reported* sub-cell | both | — | — | checked cell by cell on measured counts at the decision pass | — |

**Arithmetic, session by session** (holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18,
2027-02-15, 2027-03-26, **2027-05-31** — Memorial Day, the reason the initial decision Monday is
06-07 and not 05-31 — 2027-06-18 (Juneteenth observed), **2027-07-05** (Independence Day observed,
which sets the extension path's t+20 date) and **2027-09-06** (Labor Day, used only in solving the
DP-43 ceiling); the Steward re-confirms every date session by session when the freeze is built, and
**a correction may move a date out, never in**):

- 2026-09-15 is session 1. Session **61 = 2026-12-09**, session **122 = 2027-03-10**, session
  **153 = 2027-04-23**; on the extension path session **73 = 2026-12-28**, **146 = 2027-04-14**,
  **183 = 2027-06-07**. (Session 119 = 2027-03-05 is cross-checked against
  `STEWARD_Q027_exposure.md`.)
- **Decision date.** 2027-04-23 **+ 20 sessions** maturity = **2027-05-21**; **+ one calendar week**
  freeze margin = **2027-05-28**; first Monday on or after = **2027-05-31**, which is **Memorial Day,
  a listed market holiday**, so the decision date is the **next Monday, 2027-06-07**. The holiday
  skip moves the date **out**, which is the only direction DP-43 and DP-45 allow. That is **8.7
  months (266 days) from the lock**, inside DP-43's ceiling (2027-09-14) by 3.3 months. `eval.py` is
  written once (rule 9) and run **once**, then. **No interim looks.**
- **Extension (DP-13; DP-43's +30 sessions).** If any floor is short at 2027-06-07 on `eval.py`'s
  **own measured counts** (never on a projection or a run-rate), the window extends **once**,
  automatically and with no new question, to pick nights **.. 2027-06-07** (session 183), decision
  **Monday 2027-07-19** (session 183 = 2027-06-07, + 20 sessions = **2027-07-07**, 2027-07-05 being
  the observed Independence Day holiday and a 07-06 reading leaving the Monday unchanged; + one week
  = 2027-07-14; first Monday on or after = 2027-07-19). The block proportions (§2.3) are re-applied
  to the longer window — `W1` 1–73, `W2` 74–146, `W3` 147–183, printed at this lock so the
  extension's cuts are fixed blind — and the extended run uses the **byte-identical, unmodified
  `eval.py`**. 10.1 months from lock, inside the ceiling.
- **DEFERRED fallback (the hard stop).** Still short after that single extension → Q031 goes to
  `research/questions/DEFERRED.md` with the measured counts rather than running under-powered. **No
  second extension, no reduced floor, and a floor shortfall is never an INCONCLUSIVE verdict** (§8).
- **`eval.py` is committed no later than 2027-03-08**, with its sha256 recorded, and is not touched
  afterwards. **That is a fixed calendar date, deliberately not moved out** to the new `W2`/`W3`
  boundary of 2027-03-11 when the window lengthened: the earlier date is the stricter one (DP-45).
  The deadline is a validity requirement, not housekeeping: **Q027 and Q029 decide on 2027-04-12 and
  will print the `S^A` series for all but the final three sessions of `W1 ∪ W2`** (Q027's window ends
  2027-03-05; `W2` now ends 2027-03-10), about eight weeks before Q031 decides. Q031's *design* is
  fixed today, but a script written after that date would be written by someone who has seen two
  thirds of the series. §10 threat 6 states the residual risk that remains even so.
- **Pin at the decision date.** The population enters only through §5.3 R2's successor freezes, so
  DATASET_PINNED runs at the decision date on those manifests (`pin_at_decision: true`).
- **Fixed at lock and not reopened at the decision pass:** both MPEs (§4.2, §8); the block
  proportions and roles (§2.3); the ≥ 30-eligible-rows and ≥ 3-valid-picks / ≥ 5-controls
  contributing-night rules; the 10-session block length; the seed 20260914; `m` (§7); the four
  exclusion criteria; the level gate (§8 clause 6); and the `NO_EDGE_TO_DECAY` precondition.
- **If a weights, timeframe-multiplier, `qualification_threshold`, ATR-elite-cap, GEX-offset or
  scoring enable-flag change ships mid-window — including any promotion of the v1.7 score** —
  `overall_score` is **two different features** and
  the series is **two different series**: the window is **cut at the ship date**, the post-ship
  segment becomes the question's window with this whole schedule recomputed from it (**out, never
  in**, same single extension, same ceiling measured from the original lock), the pre-ship segment
  becomes a labelled descriptive panel, and if neither segment reaches the floors inside the ceiling
  the question is **DEFERRED** (DP-06's pattern, DP-50(a)). **This is more consequential here than in
  any other locked question**: a scoring ship inside the window does not merely split the data, it
  supplies a complete alternative explanation for the very fall the question exists to measure
  (H-014). §9 states the flag-off constraint that follows.
- **No such split exists at the lock, checked rather than assumed:** the commit sweep since
  `fa70688` over the three SAS scoring files was **repeated for this question** and returned **NONE**
  (`STEWARD_Q031_exposure.md` (f); `HEAD` unchanged at `d19c9a9`), and **no v1.7 promotion date
  exists** inside 2026-09-15..2027-07-19 — stated as the *absence of a schedule*, not a guarantee,
  which is why the window-cut rule above and §9's flag-off constraint stand and are re-swept at every
  future freeze (§5.3 R2(vi)). Q027's R1(g) found the same: every scoring field is
  constant across all 71 in-window runs of `sas_runs.config_json`, and `outcome_corrections` touch
  `overall_score` / `conflict_penalty` / `dominant_direction` on **0 of 125** rows across the entire
  frozen history. The two `config_json` changes it found are **publication gates**
  (`bear_publish_threshold` 2026-06-29, `publication_floor` 2026-07-08), both live more than two
  months before this window opens. A publication-gate change **inside** the window is not a scoring
  split and does not cut the window, but it moves `d*_t`'s source cohort (1.06 → 2.10 ATR across the
  2026-07-08 ship), so its per-night value is read from `config_json`, the distance series is printed
  across the ship date, and both series are printed split at it as a labelled descriptive panel.

### 5.3 Routed requests

- **R1 → data-steward (counts only) — SATISFIED and CLOSED, 2026-09-14:**
  `research/reports/STEWARD_Q031_exposure.md`. R1 was **blocking for the lock** — not because the
  lock-or-DEFER gate turned on it (series A's measured rate clears that on its own) but because
  **DP-43 settles an arm's demotion at lock and never afterwards**, so §5.1's demotion rule, §7's `m`,
  §2.3's block dates and §5.2's whole schedule all turned on a number no prior desk report had
  measured under §2.5's rule. **Answer:** N = 71 elapsed sessions, 68 non-excluded, 48 matured;
  (a) series B **47/71 = 0.6620**/session under the registered rule and identically under both weaker
  forms; (b) pool depth min 37 / median 54 / max 60, never below 10 or 5; (c) **35 invalid targets of
  383 published rows** (8 no `lane_plans`, 2 wrong-side, 19 split-scale, 6 outside [0.25, 10] ATR),
  reconciling to 348 valid; (d) valid picks per night min 0 (min 4 excluding 2026-06-02), median 8,
  max 10; (e) series A **re-confirmed bit-for-bit at 48/71 = 0.6761**, **47 nights contributing to
  both series**, no DP-50(a) disagreement; (f) commit sweep **NONE**, no v1.7 promotion date inside
  2026-09-15..2027-07-19. Branch (ii) of the demotion rule fired (§5.1). Measured on
  `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`, pick nights
  **2026-06-01..2026-09-10**, denominators in **elapsed sessions** with exclusions not pre-removed
  (the Q019 / Q022 / Q023 / Q027 convention). No outcome of any kind; no live query (DP-50(c)).
  The request as issued, for the record:
  (a) **series B's contributing-night rate** under §2.5 — nights with ≥ 3 valid published picks
  (DP-28's predicate, after the invalid-target and split-scale screens) each carrying ≥ 5 matched
  controls from the §2.2 construction — **and, printed beside it, the same rate under Q006's own
  weaker rule (≥ 1 valid pick, 10 nearest controls)**, so the cost of the stricter floor is visible;
  (b) the **matched-control pool depth**: per night and per pick, how many unpublished candidates
  survive the ≥ 60-bar and gradeability screens, and how often fewer than 10 (and fewer than 5) exist;
  (c) the **invalid-target count** — published picks whose L3 sits on the wrong side of `C_p`, fails
  the split-scale screen, or implies a distance outside `[0.25, 10]` ATR — per night and overall;
  (d) the **valid-pick count per night** distribution (min / median / max), so the ≥ 3 floor can be
  seen against it;
  (e) a repeat of the **DP-50(a)/(b) commit sweep** since `fa70688` over
  `services/super_agent_select_scoring.py`, `services/super_agent_select_models.py` and
  `services/sas_conviction_card.py`, with an explicit answer **even when it is "none"**, plus whether
  any scoring workstream (the v1.7 score named in `docs/SAS_SCORING_RESEARCH_PLAN.md`) is scheduled
  to ship inside 2026-09-15..2027-07-19.
  Series A's rate was **re-confirmed rather than assumed**: a disagreement between two counts of the
  same definition on the same freeze would itself have been a DP-50(a) finding. It agreed.
- **R2 → data-steward (OPEN; due before the decision date; not a blocker for lock; DP-23).** Successor
  freezes covering pick nights **2026-09-15..2027-04-23** with **20 forward sessions** beyond the last
  included pick night (daily bars through **2027-05-21**) and **≥ 60 prior sessions** before
  2026-09-15, delivered before **Monday 2027-06-07**; a second pair **only if** the DP-13 extension
  fires, covering **.. 2027-06-07** with bars through **2027-07-07**, delivered before **Monday
  2027-07-19**, built then and not before. Scope requirements, none optional: **(i)** the daily symbol
  list covers **every candidate symbol on every in-window night, published and unpublished** — the
  control pool of series B and the whole population of series A — never assumed from v001's symbol
  list; **(ii)** `public_payload_json` lane plans are required for published rows (series B's own
  printed L3 and series A's `d*_t`); **(iii)** no hourly bars are required by any endpoint, and the
  Steward says so explicitly rather than building them; **(iv)** an **add-only successor exclusions
  file** on the identical four criteria, its header stating whether the `payload_disabled_runs`
  signature is still present after 2026-09-10; **(v)** rows whose bars are missing are **excluded and
  counted, never back-filled or imputed**; **(vi)** where a successor freeze overlaps an earlier one
  on `sas_candidates`, the rows are compared and `eval.py` **fails loudly** on any disagreement in
  `overall_score`, `conflict_penalty` or `dominant_direction` — a repair that rewrote a score would
  silently re-run this experiment (DP-50(a)). **This freeze is a superset of Q027's R2** (same
  population, window extended from 2027-03-05 to 2027-04-23), so it is built **once** and serves both
  questions where they overlap; R1(f)'s commit sweep is repeated for the period between freezes, with
  an explicit answer even when it is "none" and a dated `DATA_NOTES.md` entry for any repair that
  rewrites historical rows. The Steward re-confirms every §5.2 and §2.3 date **session by session
  from the trading calendar** when the freeze is built, including the block boundaries (session
  **61 = 2026-12-09**, **122 = 2027-03-10**, **153 = 2027-04-23**, and on the extension path
  **73 = 2026-12-28**, **146 = 2027-04-14**, **183 = 2027-06-07**) and the two later holiday dates
  (2027-07-05, 2027-09-06); a correction may move a date **out, never in**.

## 6. Test window, split and stratification

- **Test window: prospective only — pick nights 2026-09-15 .. 2027-04-23** (153 elapsed sessions,
  §5.2; .. 2027-06-07 if the single DP-13 extension fires), opening on the first session after the
  lock commit dated 2026-09-14 (09-15 rather than 09-14, so that no night whose 16:05 ET run may
  precede the lock commit can enter).
- **The split is the question.** `W1` / `W2` (§2.3) *are* the in-sample / out-of-sample split by
  calendar date that rule 7 requires, and `W3` is the second out-of-sample window H-082's own PASS
  line demands. They are fixed at this lock by session index and proportion, before any night exists.
- **The sealed post-hoc panel** (`manifest_v001` + `manifest_prices_v001`, pick nights
  **2026-06-01 .. 2026-08-12** — after the DP-06 catalyst split, and 08-12 is the 20-session maturity
  cutoff of the pinned price freeze) prints both series and every §4.3 panel **once**, labelled, and
  enters **no verdict, no block, no CI comparison, no q and no §9 rule**. It is split at
  **2026-07-06** into sub-panels A = 2026-06-01..2026-07-03 and B = 2026-07-07..2026-08-12 and the
  halves are never blended: `_enforce_ladder_monotonic` shipped on 2026-07-06 (25.71% non-monotonic
  ladders before, 0.00% after — DATA_NOTES, Q018 R1) and `publication_floor` took effect 2026-07-08,
  moving `d*_t` from ≈ 1.06 to ≈ 2.10 ATR. Each sub-panel is SUPPRESSED below 20 contributing nights.
  **The sealed stretch is never the reference block**, for two independent reasons stated once and
  binding: it has been read for this hypothesis (§1), and it sits on the far side of a
  distance-doubling config ship, so a contrast across it would measure the ship.
- **Regime stratification (rule 7)** is §4.3's block-composition reporting plus B4's coarse
  `tape_sign_t` reweighting, which is blocking. The fine cells (`market_regime`'s five labels,
  `tape_t`'s six) are printed as composition counts and suppressed as contrasts below 20 measured
  contributing nights — with the measurement already suggesting how thin they will be: over 48
  measured nights, `bearish` / `neutral` / `risk_off` appeared on **zero** and five of six `tape_t`
  cells projected below 20 over a *longer* window than one block (`STEWARD_Q027_exposure.md`).
- **Knowledge time (rule 14) — every input declared. Q031 needs no rule-14 exception and requests
  none** (DP-05 untouched, DP-41 respected).

  | input | source | available | use |
  |---|---|---|---|
  | `overall_score`, `dominant_direction`, subscores, `qualified`, `selected_rank`, `best_timeframe` | `sas_candidates` (all rows) | pick night, 16:05 ET | ranking variable, eligibility, publication predicate, composition |
  | `public_payload_json.lane_plans.swing_trading.targets[0]` | `sas_candidates` (published rows) | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | `d*_t` (series A) and each pick's own L3 distance (series B) |
  | `C_t`, ATR14, beta60, runup20, adv20, SPY tape and `tape_sign_t` | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | distances, matching, reweighting, strata |
  | `market_regime` (v1.2, `trading_date = t`) | `market_regime_daily` | declared 16:05 ET / lag 0, enforced per night by the Q023 §2.2 timestamp test | composition reporting only |
  | `finished_at`, `config_json` | `sas_runs` | publication time | DP-04 exclusion; the §4.3 config panel |
  | session t+1 open; daily bars t+1..t+20 | `prices_daily_split` | after the pick night | **entry and outcome measurement only** |
  | the **block** a night belongs to | the trading calendar | fixed at this lock | the contrast itself |

  **What `eval.py` must enforce:** the eligible-row set, `d*_t`, every target, every match, every
  block assignment, every episode id and every stratum label are computed and written to a frozen
  per-row and per-night table **before any post-pick-night bar other than the t+1 open is loaded**,
  and the t+1 open is used **only** as the entry price. The run fails if any t+1-or-later field is
  referenced in eligibility, matching, block assignment or stratification.

## 7. Multiple testing

- **Within the question: BH across `m = 2`** — `D1ᴬ` and `D1ᴮ` — at q ≤ 0.10; the verdict uses q.
  `m = 2` is **fixed at lock**: both endpoints carry a verdict in every branch and neither is dropped
  afterwards (dropping one would lower the bar for the survivor), and an endpoint short of floor still
  has its p computed. `m` could have fallen to **1** only under §5.1's demotion rule, which was
  settled at this lock on R1's measured rate and never at the decision pass — **it did not fire**:
  series B measured 0.6620/session, the window end moved out to session 153, and both series project
  above every floor. The persistence contrast `D2`, the CUSUM clause, B4's reweighting and every §4.3
  panel are blockers or descriptions, not endpoints, and enter no correction set.
- **Across the family: F2 Calibration.** F2 holds H-010, H-011, H-012, H-013, H-014, H-073, H-079,
  H-080 and **H-082**, with H-010 and H-012 merged into Q027 (DP-29). The F2 correction set is
  computed at the decision pass over the F2 questions locked by then and **never shrinks below the
  16 primaries standing at this lock**: Q023 (2) + Q027 (2) + Q029's 10 companion IC endpoints
  (Q029 §7's required F2 correction) + Q031 (2) = **16**. Q005 is excluded for the stated reason — a
  diagnostic decomposition with no MPE and no outcome column read at all.
- **`D1ᴮ` additionally carries a companion correction in F1**, where its series lives: Q006 (2) +
  Q024 (6) + Q025 (2, which never shrinks) + Q029 (16) + `D1ᴮ` = **27**. Where an endpoint sits in
  two sets, **the larger q is quoted** — the Q015 / Q020 / Q029 pattern, because a decay test on
  Q006's own statistic is not independent of Q006's.
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q027 (F2)** asks whether `IC_t` has a level; Q031 asks whether the level moves. **They share
    the nights of `W1 ∪ W2` and the entire `S^A` construction.** A confirmed Q027 IC and a Q031
    `STABLE` verdict are one finding stated twice, not two; a Q027 NULL makes Q031's `S^A` endpoint
    `NO_EDGE_TO_DECAY` by §8 clause 1, which is the honest reading and not a second null. Neither may
    be quoted as corroborating the other. Q027 §10 threat 11 names this question as where its series
    is watched over time, which is what it is — not a replication.
  - **Q006 (F1)** is the level of `S^B` on sealed nights 2026-04-01..2026-09-10; Q031 is its movement
    on post-lock nights. Q006's decision on 2026-10-05 lands inside `W1`. Its result **changes nothing
    here** — no block, no MPE, no clause — and this file is locked before it, deliberately
    (DECISIONS.md item 5).
  - **Q029 (F1)** owns the per-layer ICs. Q031's attribution limb computes the same statistic as a
    time series and **licenses nothing about any layer** (DP-29); a layer that moves here is a lead
    for the Reporter, not a finding.
  - **H-079 (F2, unregistered)** owns regime conditionality, which is decay's principal competitor.
    B4's reweighting is a blocker precisely so Q031 cannot claim a tape rotation as decay, and §9
    routes a reweighting-sensitive result to H-079 as evidence rather than treating it as answered.
  - **H-014 (F2, unregistered)** owns the "configuration change brackets the fall" rule. Q031's
    config panel is descriptive input to it, never a test of it.
- Threshold: **q ≤ 0.10**, alongside raw p (rule 8).

## 8. Decision rule (numeric, written before unsealing)

`D1 = m̄(W2) − m̄(W1)` and `D2 = m̄(W3) − m̄(W1)`, per series, over §2.5's contributing nights.
`D1ᴬ` in **Spearman-ρ units**; `D1ᴮ` in **percentage points of control-adjusted L3-touch excess**.
Both primaries two-sided. H-082 predicts `D1 < 0`.

**MPE — `|D1ᴬ| ≥ 0.05`** (Haci's H3 number, applied to the deficit as H-082 names it; the *general*
IC-unit rule is Q027's standing proposal in its DECISIONS.md, not a DP entry, and nothing here
depends on it becoming one). **MPE — `|D1ᴮ| ≥ 5.0 pp`** (DP-20; the doubling clause considered and
declined in §4.2, with clause 6's level gate registered in its place). **Neither MPE is lowered at
the decision pass in any branch**, including one where the CI excludes zero and the point estimate
sits just inside it. That is what an MPE is for (rule 6).

Per endpoint, **DECAY (the CONFIRMED branch, a HISTORICALLY_CONFIRMED verdict on this question's
hypothesis)** requires **all** of:

1. **Precondition — there was an edge to lose.** `m̄(W1) ≥ +0.05` for series A, `≥ +5.0 pp` for
   series B, on the point estimate. If not, the endpoint is reported **`NO_EDGE_TO_DECAY`**, the
   verdict is **INCONCLUSIVE** with that label wherever it is restated, ledgered or quoted, no decay
   claim of any kind is made, and the level question is routed to Q027 (series A) or Q006 (series B).
   A `STABLE` verdict is likewise unavailable in that branch: a flat line at zero is not stability of
   an edge.
2. **Floors, read per series on that series' own contributing nights:** ≥ 80 contributing nights
   across `W1 ∪ W2`, ≥ 20 in each of `W1`, `W2` and `W3`, and ≥ 30 dated after the lock commit
   (DP-21, DP-24), with ≥ 20 **measured** contributing nights for any sub-cell that is *reported*.
   No floor is lowered at the decision pass; a shortfall fires the single DP-13 extension (§5.2).
3. **`|D1| > MPE` with the predicted sign** (`D1 ≤ −MPE` for decay), and the **date-clustered 95% CI
   excludes 0**, with B1's circular block permutation p supporting it.
4. **The episode-clustered 95% CI (DP-51, §4.4) also excludes 0.** A primary that clears MPE on the
   date-clustered CI and not on the episode-clustered one is **INCONCLUSIVE, never CONFIRMED**.
5. **Persistence:** `D2` carries the **same sign** and `|D2| ≥ MPE`. A deficit in `W2` that has
   recovered by `W3` is **INCONCLUSIVE** and is reported in H-082's own words — *a single bad quarter
   is INCONCLUSIVE by construction.*
6. **Level gate:** the later blocks' own level has fallen **below the edge MPE** — `m̄(W2) < +0.05`
   and `m̄(W3) < +0.05` for series A, `< +5.0 pp` for series B. A fall from a large edge to a
   still-material one is reported as **`SHRUNK_NOT_GONE`** — an INCONCLUSIVE verdict on decay that
   licenses a monitor (§9) and nothing else.
7. **Competing explanation (B4):** the tape-composition-reweighted `D1` and `D2` carry the **same
   sign** with `|·| ≥ MPE`. If the fall disappears under reweighting, the verdict is **INCONCLUSIVE**
   labelled **`TAPE_COMPOSITION`** and is routed to **H-079**.
8. **Sensitivities not running the other way:** neither the `C_t`-entry version nor the bull-only
   version of the endpoint is beyond MPE in the **opposite** sign.
9. **The change-point clause:** the CUSUM statistic `M` on the full registered series has permutation
   p ≤ 0.10 under B1. `τ̂` and its date print in every branch, including branches where the clause
   fails.
10. **BH `q ≤ 0.10`** within the question (`m = 2`) **and** within F2 — and within F1 for `D1ᴮ`, with
    the larger q quoted (§7).

- **STABLE (the NULL branch, and H-082's own PASS):** clause 1 met, clause 2 met, `|D1| < MPE` and
  `|D2| < MPE`, and **both** CIs include 0. *"The edge did not deteriorate over 153 sessions"* is a
  real finding with a direct consequence (§9) and is ledgered with the same care as a positive.
- **IMPROVED:** every DECAY clause met with the sign reversed (`D1 ≥ +MPE`, persistence, both CIs,
  q) — reported as such, and it matters: it would say the sealed-period weakness the weeklies printed
  was the tape, not the system.
- **INCONCLUSIVE (per endpoint):** anything else — `NO_EDGE_TO_DECAY` (clause 1), `SHRUNK_NOT_GONE`
  (clause 6), `TAPE_COMPOSITION` (clause 7), a date-clustered CI excluding 0 while the
  episode-clustered CI does not (clause 4), a `W2` deficit that does not persist into `W3`
  (clause 5), `0 < |D1| ≤ MPE` with a CI excluding 0 ("real but below MPE", rule 6), or `|D1| ≥ MPE`
  with a CI including 0. **A floor shortfall is never INCONCLUSIVE** — it fires the single DP-13
  extension, then DEFERRED (§5.2).
- **Question level.** The two series are reported separately and **are not pooled**. A decay in `S^A`
  without one in `S^B` is *"the ranking degraded while the published slate held up"*; the reverse is
  *"the slate degraded while the score still ordered candidates"* — and both are more informative
  than a single headline. A question-level DECAY verdict requires **both** primaries to be DECAY with
  the same sign; one DECAY and one STABLE is reported as a **split result, loudly, with the two
  sentences above**, and licenses only the monitor in §9.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5) — it requires ≥ 30 contributing
  nights dated after this file's lock commit (DP-24, DP-21), which every contributing night here is,
  frozen in the successor manifests and never inspected earlier, reproducing the sign under the
  unmodified `eval.py`. The clause does not weaken. No subscriber-facing statement before that
  (rule 10); even then the basis is `NON_QUOTABLE` until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today nothing in the platform or in the desk watches the edge over time. The weekly prints a rolling
four-week 90+ *return* trend, which is the confounded version of this question, and PI-010's falling
elite count and Q005's INCONCLUSIVE cause are the only standing evidence that anything is drifting.
Rules below fire **only** where §8 licenses them, and nothing subscriber-facing ships before
PROSPECTIVELY_CONFIRMED (rule 10):

- **DECAY confirmed on either series (or both):** (a) **EN-017 is built** — the nightly edge-decay
  monitor already specified in `research/ENHANCEMENTS.md` (append-only table of the per-night IC and
  the control-adjusted L3-touch excess, rolling 20-night mean, CUSUM flag), as an `INTERNAL_TOOL`,
  flag-off, Haci-only, with **this question's measured change-point machinery, block length, seed and
  MPEs as its parameters** rather than invented ones; (b) a **guide line** stating the measured fall
  and its date, `NON_QUOTABLE`, internal; (c) the weekly stops describing any four-week dip as
  "within normal variation" — the measured `W1` bootstrap band (B2) replaces that phrase with a
  number.
- **DECAY confirmed does NOT by itself retire or retrain any component.** H-082's own action line
  says *"retire or retrain the affected component"*, and this question cannot identify one: the
  attribution limb (§4.3) is descriptive by construction and Q029 owns the layer endpoints (DP-29).
  A retirement brief requires **all three**: a DECAY verdict here, a layer whose own series moves with
  it, and Q029's verdict on that layer. Until then the finding is *"the edge fell"*, not *"this
  ingredient broke"*, and §9's language is written to keep it that way.
- **STABLE (both series):** this is H-082's PASS branch and it has a concrete consequence — **the desk
  stops explaining weak stretches as decay.** The measured `W1` variation band becomes a standing
  line in the weekly ("a four-week mean of X is inside the historical band of [a, b]"), the
  retire-or-retrain conversation closes until a later freeze, and **EN-017 is still built** — a
  monitor is worth more when the series is known to be stable, because then a future move means
  something. No subscriber-facing claim of any kind follows from a stable series.
- **`TAPE_COMPOSITION` (clause 7):** routed to **H-079** as evidence, with the reweighted and
  unweighted contrasts printed side by side. It licenses no decay language anywhere and no component
  change.
- **`NO_EDGE_TO_DECAY` (clause 1):** licenses nothing at all, and the report says in its first
  sentence that the question could not be asked of that series because the reference block had no
  edge to lose. It is routed to Q027 / Q006, not treated as a null result about decay.
- **`SHRUNK_NOT_GONE` (clause 6):** the monitor (EN-017) and nothing else.
- **Q031 is in flight from this lock until its decision date, and DP-50(b) applies to the platform in
  the meantime — more tightly than for any other question on the board.** There is one database, and a
  scoring change does not merely rewrite what this question reads, it *becomes* the explanation for
  what it measures. Any platform change to the SAS weights, the timeframe multipliers,
  `qualification_threshold`, the ATR-elite caps, the GEX-missingness offset or the scoring
  enable-flags — **including any promotion of the v1.7 score `docs/SAS_SCORING_RESEARCH_PLAN.md`
  contemplates** — is **flag-off until 2027-06-07** (2027-07-19 if the single DP-13 extension fires),
  which extends Q027's and Q029's identical constraint (2027-04-12 / 2027-05-24) by about **eight**
  weeks, and is the tightest such constraint on the board.
  The constraint is checked before any fix brief is written (the PI-011 / Q010 pattern). If such a
  change ships anyway it takes a dated `DATA_NOTES.md` entry naming the column, the range and the ship
  SHA, and §5.2's window cut applies — out, never in.
- **DP-49 binds every brief this question produces:** each check handed to the **coding agent** must
  be satisfiable from the platform repo alone. Anything that reads or writes a table belongs in the
  brief's verification section, addressed to the Data Steward on `$RESEARCH_DB_URL`, or to Haci where
  a write is required; where a frozen manifest covers the affected table, the brief names that parquet
  as the before-snapshot (DP-50(c)).
- Owner: implementer. Shadow period before any flip: ≥ 20 trading days.

## 10. Known threats to validity (registrar's own list)

1. **A decay test is a low-power instrument, and 153 sessions is one stretch of tape.** Each block
   holds ~40 contributing nights of a night-level statistic whose variance is unknown to the desk
   today — and cannot be known without reading outcomes, which is precisely what pre-registration
   forbids. So the honest expectation is that `INCONCLUSIVE` is the modal verdict, and §8's
   equivalence-shaped NULL branch (`|D1| < MPE` **and** both CIs include 0) is demanding by design.
   The desk does not get to widen the MPE afterwards to convert an inconclusive into a null.
2. **The question is conditional on there being an edge, and that is not yet known.** Q006 decides
   2026-10-05 and Q027 on 2027-04-12; either could return NULL, in which case clause 1 fires and this
   year of waiting yields `NO_EDGE_TO_DECAY`. That is a real cost, accepted knowingly: the alternative
   — waiting for those verdicts — would let them shape this design, and the series cannot be accrued
   retroactively (DECISIONS.md item 5).
3. **Decay and regime are confounded in any single window.** A fall from `W1` to `W2` can be a tape
   rotation, and one window cannot separate them. B4's coarse reweighting is the registered guard and
   it is a **blocker**, not a footnote — but it is coarse (two cells) because fine cells are not
   estimable at 40 nights a block, and a regime shift orthogonal to trailing SPY sign will pass
   through it. H-079 is where the separation is actually made.
4. **A step-change test against a gradual decline.** If the edge erodes smoothly rather than breaking,
   the CUSUM's `τ̂` is arbitrary and its p-value weak. The fixed-block contrast retains power against a
   trend (it contrasts early with late), and the night-index Spearman ρ is printed — but the
   *registered* clause 9 is a break test, and a smooth decline that fails it will be reported as
   INCONCLUSIVE with the trend statistic beside it, not quietly re-labelled.
5. **The engine's own target distance moves.** R1(c) measured `d*_t` doubling across a single
   publication-gate ship with no scoring field changing. The control-adjustment cancels that at first
   order and the distance series is printed beside the edge series, but a distance change large enough
   to move picks and controls differently (a different part of the return distribution) is not fully
   cancelled, and that is stated wherever a fall is quoted.
6. **Two thirds of this series will have been read by the desk before this question decides.** Q027
   and Q029 decide on 2027-04-12 on **all but the final three sessions of `W1 ∪ W2`** (Q027's window
   ends 2027-03-05; `W2` now ends 2027-03-10), about **eight** weeks before Q031 decides — which makes
   the threat slightly smaller than it was drafted, and is recorded rather than quietly enjoyed. The
   design, blocks, MPEs, nulls and
   clauses are fixed at this lock and `eval.py` is committed by 2027-03-08 (§5.2), so no choice in
   this file can be made after seeing them — but the *reading* of Q031's report on 2027-06-07 will be
   done by a desk that already knows how `W1 ∪ W2` looked. The mitigations are structural: no clause
   is reopened at the decision pass, the sub-cell rule is measured rather than chosen, and the Red
   Team reviews against this file, not against the intervening reports.
7. **`W1` is not a neutral reference block.** It is the first ~13 weeks after a lock, on whatever tape
   arrives; nothing makes it the system's "true" level. Every statement this question licenses is
   therefore relative — *"the edge fell from its `W1` level"* — and never *"the edge is below its
   historical norm"*. The sealed panel is printed but is explicitly not the norm (§6).
8. **A scoring ship inside the window does not merely split the data; it explains the result.** §5.2
   cuts the window at any such ship and §9 asks for flag-off until the decision date, but the desk
   does not control the platform's calendar, and a v1.7 promotion mid-window would likely end this
   question rather than split it. R1(e) asks whether any such workstream is scheduled.
9. **Two series that can disagree.** `S^A` is measured over ~50 candidates a night and `S^B` over ~8
   picks; their variances differ by an order of magnitude and their nights are not identical. §8
   forbids pooling them and requires both to move for a question-level verdict, which is strict — but
   it also means the commoner outcome is a split result, and §9 licenses only the monitor for that.
10. **One database (DP-50).** A platform repair between freezes can rewrite the scores and ladders both
    series are built from. Rule 4's pinned manifests are what stands between that and a locked
    question; §5.3 R2's loud cross-freeze comparison is what detects it; and a repair that rewrites
    history inside this window is, for a decay question, indistinguishable from decay unless it is
    logged in `DATA_NOTES.md` on the day it ships.
11. **`W3` is the smallest block and carries a blocking clause.** At 20.5 projected contributing nights
    the persistence contrast is the noisiest number in the file, which cuts both ways: it can fail a
    real decay (INCONCLUSIVE, and the question is re-registrable on later nights) and it can pass a
    spurious one. It is a *blocker on DECAY*, never a route to it, so its noise cannot manufacture a
    positive verdict on its own.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-14). Routed items still open: **R2** — the successor selection and
price freezes, due before the decision date and not a blocker for the lock (DP-23; §5.3). R1 is
satisfied and closed (`research/reports/STEWARD_Q031_exposure.md`, 2026-09-14).
