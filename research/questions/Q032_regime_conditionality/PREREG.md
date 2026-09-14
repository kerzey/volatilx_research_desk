# Q032 — regime_conditionality: does the SAS selection edge exist only in identifiable tape states?

**Status:** PREREG_DRAFT (lock by committing this file)
**Family:** **F2 Calibration** (hypothesis **H-079**, Haci's Master Hypothesis Program **H9**,
*Regime conditionality*). The primary endpoint's subject is whether a measured edge statistic is
conditional on an environment the desk can name in advance, which is calibration of the desk's own
claims (DP-29). Because the endpoint is built on Q006's `E_t`, it additionally carries a **companion
correction in F1** (§7).
**Manifest (sealed post-hoc panel and the borrowed exposure counts only):**
research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA
fa70688bc252d14f8d67e371afafc194731c324e).
**Manifest (prices, sealed post-hoc panel and R1's bounded exposure count only):**
research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374).
**Successor freezes — the question itself (built and pinned at the decision date, DP-23; §5.3 R2):**
**Q027's successor freeze pair, shared** — a selection freeze (`sas_candidates` **every row,
published and unpublished**, `sas_runs`, `market_regime_daily`) and a price freeze (daily bars for
**every candidate symbol on every in-window night**, plus hourly bars for published symbols),
covering pick nights **2026-09-15 .. 2027-03-05** with daily bars through **2027-04-05** (session
t+20 of the last included pick night) and ≥ 60 prior sessions before 2026-09-15; a second pair
**only if** the single DP-13 extension fires, covering pick nights **.. 2027-04-19** with bars
through **2027-05-17**. **Q032 adds exactly one scope requirement to that shared pair: SPY daily
bars (split-adjusted) from 2025-01-02**, because the §2.2 tape proxy needs a 200-session mean and a
250-session volatility-tercile calibration at the *first* in-window night and
`manifest_prices_v001` starts 2026-01-31 (§5.3 R2(i), §11 item 2). **Every night that carries a
verdict here is after this lock and exists in no manifest pinned today**, so the population enters
only through those successor freezes (`pin_at_decision`, DP-23 — the Q024 / Q027 / Q031 pattern).
They are named in prose and deliberately not written as `**Manifest …:**` header lines, because no
such file exists yet and the pin step reads every `**Manifest` line as a path.
**Exclusions:** research/data/exclusions_v003.json (DP-22, the newest file) unioned with the
**add-only successor exclusions file** issued with the successor selection freeze — the identical
**four** criteria Q027 fixes at its lock (`manual_runs` ∪ `non_session_runs` ∪
`uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10.
The successor file may only **add** nights; no night is removed from a v003 list; the **criteria**
are fixed at this lock even though the **dates** cannot be. Both paths are `eval.py` inputs; no
hard-coded file name, no hard-coded date. DP-04 applies mechanically on top.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14

---

## 1. Hypothesis (plain English)

**SAS's published picks beat their same-night look-alikes to the swing target in one kind of tape and
not in another — and the kind of tape can be named in advance, from price bars alone, on the pick
night itself.**

BACKLOG H-079 reads: *"does SAS have an edge only in identifiable environments — PASS the same frozen
strategy works reliably in pre-defined regimes and weakens predictably elsewhere, reproduced OOS;
FAIL the regime partition does not reproduce → do not invent regime explanations for bad periods."*
It names the endpoint (`E_t`, Q006's within-night control-adjusted L3-touch rate, averaged per regime
cell), the MPE (±10.0 pp), the reproduction requirement (same sign in two independent windows, split
at lock), two regime definitions, and the permutation baseline. This PREREG fixes the cells, the
entry, the level, the clock, the window and the decision (§2–§8).

**One primary** (§4), night-level, two-sided:

- **P1 — the interaction.** `G` = the mean per-night control-adjusted L3-touch excess of the
  published slate over its distance-matched same-night controls, averaged over **BENIGN** nights,
  minus the same averaged over **HOSTILE** nights, where BENIGN and HOSTILE are a **bar-only tape
  partition computed from SPY closes dated ≤ t** and fixed at this lock (§2.2). Units: percentage
  points. **MPE ±10.0 pp** (H-079's own number; DP-20's larger-MPE clause for a difference of
  differences — the Q012 P2 / Q018 P4 / Q022 E1 / Q023 E1 precedent).

**The platform's own regime label is registered too, and deliberately not as a primary.** H-079 names
two regime definitions. The second — `market_regime_daily`'s point-in-time label — enters as **C1, a
mandatory blocking companion** (§4.3, §8 clause 6) and never as an endpoint, for a reason that is an
exposure fact rather than a preference: over the entire point-in-time-legal history of that column
the label has taken exactly **two** values (`STEWARD_Q023_exposure.md` §3: 49 `strongly_bullish`
nights and 13 `bullish` nights in 65 sessions; **zero** `neutral`, `bearish` or `risk_off`), so the
only platform-label partition with any exposure is `strongly_bullish` vs `bullish` — **which is
Q023's E1, already locked, on a population that is ~95% of this one** (`publication_floor = 80.0`
since 2026-07-07 and 90+ runs at 2–3 picks a month). Registering it here as a primary would give the
desk a second bite at a locked question's statistic and would double-count it in F2. It is therefore
computed, printed, corrected jointly with Q023's E1, allowed to **block**, and allowed to confirm
nothing (§7, §8 clause 6, §9).

**H-079 predicts `G > 0`** (the edge is real in benign tape and weakens in hostile tape). **P1 is
registered two-sided**: a result beyond MPE with the opposite sign is a confirmed finding with the
opposite sign, and would be more useful still — it would say the desk should stop standing aside in
difficult tape.

**What was already seen, and why the window starts after the lock.** The desk has read the sealed
regime cells: the weekly snapshots of 2026-09-10 and 2026-09-12 printed regime × band returns and
regime-stratified cuts on sealed nights, and those reads are what put H-079 on the backlog. Those
nights are contaminated for this question. They are **not used for any verdict**: the window is
**prospective-only, pick nights 2026-09-15 .. 2027-03-05** (§6), and the sealed stretch is printed
once as a labelled post-hoc panel that enters no verdict, no CI comparison, no half, no stratum test
and no q.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night first; the
  arm is a property of the **night**, so the night is also the unit the arm is assigned to.
- **Source tables (the successor selection freeze, §5.3 R2):**
  `sas_candidates` — `trading_date`, `symbol`, `qualified`, `selected_rank`, `overall_score`,
  `dominant_direction`, `best_timeframe`, `confidence_level`,
  `public_payload_json` → `lane_plans.{day_trading, swing_trading, longterm_trading}.{entry, stop,
  targets}` and `analysis_status`, `outcome_target_invalid` (exclusion audit only),
  `score_details_json` (band-integrity check, §10 threat 7), `context_json`;
  `sas_runs` — `finished_at` (DP-04; and the §2.3 legality timestamp test), `config_json`
  (the weights / publication-gate audit, §10 threat 8);
  `market_regime_daily` — `trading_date`, `regime_version`, `market_regime`, `raw_parent_regime`,
  `regime_phase`, `regime_confidence`, `data_quality`, `asof_close_date`,
  `effective_for_trading_date`, `created_at` — **C1 only, never the primary arm**.
- **Source tables (the successor price freeze, §5.3 R2):** `prices_daily_split` (pick-night close,
  ATR14, beta60, runup20, forward bars to t+40, **and SPY from 2025-01-02 for the §2.2 proxy**),
  `prices_daily_raw` (split-factor snapping only), `prices_hourly_raw` (published symbols; the
  descriptive entry audit — **no endpoint depends on an hourly bar**).

### 2.1 Treatment rows — exact filter

**The two dates below are illustrative of values `eval.py` receives as inputs.** §5.3 R2 requires the
script to take the window start, the window end, the manifest paths, the exclusions-file paths and
the output directory as arguments, with **no hard-coded date, manifest name or path**, so that the
byte-identical script serves the primary run and the DP-13 extension run alike.

```sql
SELECT c.*
FROM   sas_candidates c
JOIN   sas_runs run ON run.trading_date = c.trading_date
WHERE  c.qualified IS TRUE
  AND  c.selected_rank IS NOT NULL                   -- publication predicate, DP-28
  AND  c.trading_date  >= DATE '2026-09-15'          -- §6 window start   (input, illustrative)
  AND  c.trading_date  <= DATE '2027-03-05'          -- §5.2 window end   (input, illustrative)
  AND  c.trading_date NOT IN (<exclusions_v003 ∪ the add-only successor exclusions file:
                               manual_runs ∪ non_session_runs
                               ∪ uncorroborated_publication_runs ∪ payload_disabled_runs>)
```

**No score-band filter.** H-079 is about the published slate, not a band (DP-25); the band split is a
stratum (§6) and the 90+ cell is expected to be SUPPRESSED. **No direction filter:** bull and bear
published picks both enter, direction-adjusted throughout (§2.4), with a **bull-only blocking
companion** (§4.3, §8 clause 7) because bear exposure is thin and graded below base rate (H-062).
Dark-lane rows (`qualified` false or `selected_rank` NULL) are **never** in the treatment arm
(DP-28); they are the control pool (§3 B2) and are counted in the §2.5 funnel.

### 2.2 The arm — a bar-only tape partition, fixed at this lock, computed from SPY closes dated ≤ t

Every input is a split-adjusted SPY daily bar dated **on or before the pick night**, from the pinned
price freeze. Nothing here reads a platform column, so a platform relabelling or a regime-engine
repair cannot move a night between arms (DP-50(a) — this is the point of the definition, not a
side-effect). All cut rules are **registrar-chosen conventions fixed at lock and not derived from any
outcome** (DP-26).

- **`SMA50_t`, `SMA200_t`** = the simple means of SPY's split-adjusted closes over the trailing 50 and
  200 sessions ending at t (inclusive).
- **`trend_t`**:
  - **`UP`** iff `close_t > SMA50_t` **and** `SMA50_t > SMA200_t`;
  - **`DOWN`** iff `close_t < SMA50_t` **and** `SMA50_t < SMA200_t`;
  - **`MIXED`** otherwise.
- **`rvol_t`** = the sample standard deviation of SPY's daily log returns over sessions t−19..t,
  annualised by √252.
- **`vol_t`** = `LOW` / `MID` / `HIGH` by the **expanding-window** terciles of `rvol` over every SPY
  session in the pinned freeze dated ≤ t, requiring **≥ 250 such sessions**; below 250 the night is
  **excluded and counted** (it cannot happen inside the registered window once R2(i) delivers SPY from
  2025-01-02, and the loud exclusion is what proves it). Expanding, never full-sample: no later
  night's volatility may set an earlier night's stratum.
- **The two arms, named in advance (H-079's "the contrast between cells the PREREG names in
  advance"):**
  - **BENIGN** iff `trend_t = UP` **and** `vol_t ∈ {LOW, MID}`;
  - **HOSTILE** otherwise (`trend_t ∈ {MIXED, DOWN}`, or `vol_t = HIGH`, or both).
- **Nine-cell composition is printed** (`trend_t` × `vol_t`, contributing nights per cell, per arm),
  and §8 clause 8 carries a **HOSTILE composition guard**: if any single one of the eight HOSTILE
  cells carries ≥ 80% of HOSTILE contributing nights, the verdict is **restated as being about that
  cell** wherever it is reported, ledgered or quoted, and every §9 sentence names it. This is a
  naming clause, not a floor change: no floor moves in either direction, and the 80% is fixed at lock.

### 2.3 C1's arm — the platform's point-in-time label (companion only)

Adopted **verbatim from Q023 §2.2**: `STRONG` iff `market_regime = 'strongly_bullish'`, `NOTSTRONG`
iff `market_regime ∈ ('bullish','neutral','bearish','risk_off')`, on the `v1.2` row with
`trading_date = t` — the row the platform's own consumer reads to gate a pick scored on t's close
(volatilx `services/market_regime/consumer.py:52-60`). **Legality is a timestamp test, not a date
test**: the row must carry `market_regime <> 'unknown'`, `COALESCE(data_quality,'') <> 'insufficient'`,
`created_at::date = trading_date`, **and** `created_at <= that night's own sas_runs.finished_at`.
A night failing any limb has **no legal platform label**: it is dropped from **C1 only**, counted by
reason code, and **still contributes to P1** — the bar-only proxy needs no platform row. This
asymmetry is stated because it means C1's night count is a subset of P1's and the two are never
compared on different denominators without both being printed.

### 2.4 Levels, entry, clock

- **Direction** `dir` = +1 bullish / −1 bearish from `dominant_direction`. Every distance and every
  touch is direction-adjusted.
- **`C_t`** = the pick's actual regular-session close on pick night t from `prices_daily_split` (never
  the platform's `spot_close`, stale on re-run nights — EXPLORE_001 §9). **`ATR`** = ATR14 from
  `prices_daily_split` bars dated ≤ t (never the platform's `atr_pct` — DATA_NOTES / PI-003).
- **Entry `X` = the session t+1 regular-session open** (DP-03(b), DP-42), for picks and controls
  alike. **A level at or through `X` at the open is not a hit** (rule 5): `hit = 0`, the pick stays in
  the denominator, and the not-takeable count is printed per arm. The **`C_t` basis (DP-03(a) /
  DP-11) is computed and printed as a named sensitivity** and never decides.
- **`L3`** = `lane_plans.swing_trading.targets[0]`, the printed swing first target (volatilx
  `services/sas_conviction_card.py:182-187`); `d_L3 = dir × (L3 − C_t) / ATR` — **each pick's own
  printed distance**, the Q006 / Q023 construction (not Q027's common `d*_t`, which exists because
  Q027's population includes candidates with no printed ladder).
- **Clock: L3 within 20 sessions from `X`** (DP-09 — L3 is the primary level, so the primary clock is
  the 20-session spread horizon). The platform's own 40-session swing window is printed alongside,
  descriptively. **Binding maturity: 40 sessions**, uniform across every eligible pick, so the
  descriptive companion is never right-censored either.

### 2.5 Exclusions — each counted, per arm, printed in the results header, never silently dropped

Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or a
measurement failure. **None can move a night between arms** — the arm is a function of SPY bars alone.

- **Nights** in the union of `exclusions_v003.json` and the add-only successor file (`manual_runs` ∪
  `non_session_runs` ∪ `uncorroborated_publication_runs` ∪ `payload_disabled_runs`), and any night
  whose `finished_at` is later than the next session's open (DP-04), mechanically.
- **Nights with fewer than 250 prior SPY sessions** in the pinned freeze (§2.2) → excluded, counted,
  and loud: inside the registered window this count must be **0** or R2(i) did not deliver.
- **Null-ladder denominator:** no lane plan, no swing lane, or no `targets[0]` → pick excluded and
  counted.
- **Wrong-side or non-monotone ladder at the close:** `L3` at or through `C_t` in the pick's
  direction, the flattened six levels not strictly monotone in the direction, or
  `outcome_target_invalid` non-null → excluded and counted. The whole window sits after platform
  commit `5fa3db4` (2026-07-06, `_enforce_ladder_monotonic`), so a non-zero rate is a loud flag, not
  a silent drop.
- **Split-scale payload screen** (DATA_NOTES, the APH / KLAC / CRWD / MNST finding): a pick is
  excluded and counted if `lane_plans.day_trading.entry / C_t` is outside `[0.85, 1.15]` or
  `|d_L3| > 20`. Decided from pick-night data only, applied identically in both arms.
- **Missing forward bars** inside t+1..t+40 (halt, delisting) → ungradeable, excluded and counted; a
  measurement failure, never a classifier. A night is dropped if > 25% of its eligible picks are
  ungradeable.
- **Fewer than 60 daily bars dated ≤ t** for the pick or a control (ATR / beta60 / runup20 undefined)
  → excluded, counted. The **CTRA truncated-history signature** (`STEWARD_Q023_exposure.md` §6: last
  daily bar 2026-05-06, still appearing as a candidate to 2026-09-10) is caught by this screen; the
  per-night count of candidates dropped for it is printed.
- **Immature nights** — session t+40 after the last trading date of the pinned price freeze →
  excluded and counted. Maturity comes from the trading calendar, never from whether a price exists;
  right-censoring is never graded as a non-touch.

### 2.6 Contributing night, tape-episode, symbol-episode

Three units, deliberately given three names, because two of them are called "episode" elsewhere on
this desk and they are **not the same object**:

- **Contributing night (the floor unit, DP-21):** a non-excluded night in the window carrying a legal
  §2.2 arm label **and ≥ 1 eligible published pick with ≥ 3 valid matched controls**, matured to
  t+40. A night that survives the night-level filters but carries no eligible pick is a
  **non-contributing night, not an exclusion** — printed in the funnel.
- **Tape-episode (the block and permutation unit, §4.4):** a maximal run of consecutive *sessions*
  carrying the same §2.2 arm label; a session with no legal arm label or an excluded night does
  **not** break a run, and only a session carrying the *other* arm's label ends one. It counts toward
  the §8 clause 2 gate only if it contains ≥ 1 contributing night, and it is resampled carrying its
  contributing nights. *Why on the label series:* tape states arrive in runs, so an excluded night
  inside a stretch must not manufacture an extra independent draw — that is the direction that makes
  the gate easier, which is the direction the desk does not take (DP-45). This is Q023 §2.5's
  construction on a different label.
- **Symbol-episode (DP-51 only):** one symbol's run of *published-pick appearances* with gaps of ≤ 10
  sessions between successive appearances. It is a cross-sectional dependence unit and appears
  **only** in the §4.4 second CI. It never blocks, never gates and never defines a night.

## 3. Baseline(s) — what this must beat

- **B1 (primary, the arm baseline): the same slate on HOSTILE nights.** "Y's rate when X did not
  happen", same window, same population, same grading, same control construction. This **is** `G`'s
  second term. There is no version of this question without it.
- **B2 (rule-5 distance-matched control, inside `E_t` by construction): the Q006 §3 construction
  verbatim.** For each eligible pick, the **10 nearest same-night non-published `sas_candidates` rows**
  (the complement of DP-28's predicate) on `beta60` / `atr_pct` / `runup20` computed from
  `prices_daily_split` bars dated ≤ t, standardized by the night's cross-sectional median and MAD,
  Euclidean distance, with replacement across picks, ties broken by symbol ascending. Each control
  carries a **synthetic target at the same ATR distance and direction** as the pick it matches,
  `L3_c = close_c × (1 + dir_p × d_L3,p × atr_pct_c)`, graded from the control's own session t+1 open
  with exactly the §4 rules, same direction, same 20-session window. Controls **never add to
  inferential n** (rule 6). A pick with fewer than **3** valid controls is dropped and counted,
  **never imputed**; the pool is not thin on this population (`STEWARD_Q023_exposure.md` §6: mean
  51.8, median 54, min 39 valid same-night non-published rows; 100% of nights ≥ 10).
- **B3 (the null the p-value is taken against): the pooled edge with arm labels permuted across
  tape-episodes.** H-079's own named baseline. 10,000 permutations, seed 20260914, each preserving
  every tape-episode's length and the night ordering inside it (§4.4).
- **B4 (the second regime definition, blocking, never a verdict): the platform point-in-time label
  contrast** `G_PL` = mean `E_t` over STRONG nights − mean over NOTSTRONG nights, §2.3's arm, same
  picks, same nights, same grading. **B4 is not independent of Q023's E1** and is corrected jointly
  with it (§7); it blocks (§8 clause 6) and licenses nothing (§9).

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Nothing in this question is decided by a fixed-horizon return.** Close-to-close returns at T+5,
T+20 and T+40 from `X` are printed and are **descriptive by rule 5 and DP-01**. This matters more
here than usual: the sealed reads that put H-079 on the backlog were regime-stratified *returns*.

### 4.1 Per pick, per night

- **`hit_p`** = 1 if the regular-session high (bullish) / low (bearish) touches `L3` on some session
  in **t+1..t+20**, else 0. A gap through `L3` at a session open is a touch. A pick whose `L3` is at
  or through `X` at the t+1 open is **not-takeable**: `hit_p = 0`, it stays in the denominator, and
  the count is printed per arm.
- **`ctrl_p`** = the mean of `hit` over that pick's ≥ 3 matched controls, graded identically from each
  control's own t+1 open at the identical ATR distance.
- **`e_p = hit_p − ctrl_p`** — the pick's control-adjusted touch indicator, in rate units.
- **`E_t = mean_{p ∈ P_t} [ e_p ]`** over night t's eligible published picks — **Q006's quantity,
  computed per night** (Q006 §4's `Delta1_t` on the DP-09 20-session clock).

### 4.2 The primary endpoint

- **P1: `G = mean_{t ∈ BENIGN} E_t − mean_{t ∈ HOSTILE} E_t`**, in **percentage points**. `m = 1`.

**MPE ±10.0 pp**, as H-079 filed it. `G` is a **difference of differences** (a control-adjusted rate,
arm minus arm), and DP-20's larger-MPE clause applies with the Q012 P2 / Q018 P4 / Q022 E1 / Q023 E1
precedent: at ~80 nights a 5 pp bar on a difference of differences returns INCONCLUSIVE by
construction rather than by evidence. **The MPE is not lowered at the decision pass in any branch** —
including a branch where it turns a CI-excludes-zero result into INCONCLUSIVE. That is what an MPE is
for (rule 6).

**The level clauses, which are what make this a conditionality test rather than a level test.** Both
are computed on the same nights and both can only *block* or *relabel* a positive, never create one:

- **`NO_EDGE_TO_CONDITION` (§8 clause 3).** If the **pooled** `mean_t E_t` over all contributing
  nights is inside ±5.0 pp (DP-20, the edge MPE), there is no edge for the tape to be conditional on.
  P1 is **INCONCLUSIVE** with that label, decides nothing about regime, and is routed to Q006 and
  Q027 — a flat line at zero split into two flat lines is not a regime finding. (Q031 clause 1 is the
  same idea applied to time; the Q006 decision of 2026-10-05 is the level read and lands inside this
  window, **changing nothing here** — no arm, no MPE, no clause.)
- **`WORKS_IN_BENIGN` vs `HOSTILE_ONLY` (§8 clause 4).** A CONFIRMED `G` is labelled at lock by the
  BENIGN arm's **own** level: `WORKS_IN_BENIGN` iff `mean_{t ∈ BENIGN} E_t > +5.0 pp`; otherwise
  `HOSTILE_ONLY` — the edge is not positive anywhere, it is merely *less negative* in benign tape.
  Both are confirmed findings; §9 says what each licenses, and they are not the same thing.

### 4.3 Secondary and sensitivity output

Everything here prints raw p only and is labelled *"descriptive, does not decide"* — **except the
four named blockers**, which are descriptive in that no verdict rests *on* them but which **block** a
CONFIRMED verdict when they run the other way (§8 clauses 5–7). Suppression restricts **affirmative
reporting only**: it never removes a blocker, and a suppressed cell never by itself makes the
endpoint INCONCLUSIVE.

**Computed, and blocking:**

- **C1 = `G_PL`**, the platform-label contrast (§2.3, §3 B4) — **§8 clause 6**: a CONFIRMED `G` whose
  `G_PL` is beyond 10.0 pp in the **opposite** sign is INCONCLUSIVE. Printed with its own night
  counts, its own tape-episode counts, and the night-level agreement rate between the §2.2 arm and
  the §2.3 arm. The `effective_for_trading_date = t` variant of C1 is printed beside it (Q023's
  binding sensitivity, carried here as information, since C1 itself never confirms).
- **Halves** — H-079's "reproduced with the same sign in two independent windows (first and second
  halves of the prospective window, split at lock)". **Half A = window sessions 1–60, Half B =
  sessions 61–119**, fixed by session index at this lock and re-derived from the trading calendar, not
  from the median contributing-night date (H-079 says *split at lock*; Q031's fixed-block reasoning).
  **§8 clause 5**: same sign in both halves, and neither half beyond MPE in the opposite sign. It
  **blocks at whatever count it has** and is not on the suppression list.
- **Bull-only** `G` (published bullish picks only), with the per-arm direction mix — **§8 clause 7's
  opposite-sign blocker** (H-062: bear picks graded below base rate, so the direction mix is a live
  confound).

**Computed, mandatory in the report, purely descriptive:**

- the **raw (unadjusted)** arm contrast of the L3 touch rate, `mean_{BENIGN} mean_p[hit_p] −
  mean_{HOSTILE} …`, printed beside `G` so the control's work is visible, and the two arms' raw
  control touch rates, which say how much of any gap is simply "everything moves in a calm uptrend";
- the **per-arm levels** `mean_{BENIGN} E_t` and `mean_{HOSTILE} E_t` with their own CIs (clause 4
  reads these);
- the **nine-cell** `trend_t` × `vol_t` composition and, where a cell clears 20 contributing nights,
  its own `E_t` mean — with the **three `trend_t` states** printed as an ordered monotonicity read
  (UP ≥ MIXED ≥ DOWN), descriptive;
- the **`C_t` entry basis** (DP-03(a) / DP-11) for the primary, with not-takeable counts;
- the **40-session** companion of `G` (the platform's own swing window, DP-09);
- per-level **L1…L6 first-touch rates and sessions-to-touch** on each level's own lane window, per
  arm, against the same controls; **maximum favourable and maximum adverse excursion in ATR** from
  `X`; counter-direction touches (reported, never an exit — DP-02);
- **close-to-close returns** at T+5 / T+20 / T+40 from `X` — **descriptive by rule 5 and DP-01**, and
  no verdict sentence may lead with them.

**Sub-cells — the list is FIXED at lock and does not reopen at the decision pass**, subject to R1's
measured counts at `record` (which may only move cells **onto** the list, never off it):

- **SUPPRESSED at lock:** the `90+` band (structural — `publication_floor = 80.0` since 2026-07-07
  and 2–3 elite picks a month, PI-010); **bear-only** as a *reported* cell (it blocks as the bull-only
  companion's complement but is not reported affirmatively); `confidence_level` terciles;
  `best_timeframe` cells; `regime_phase` cells; `d_L3` terciles; `atr_pct` terciles; and any of the
  nine `trend_t` × `vol_t` cells measuring below 20 contributing nights.
- **NOT suppressed:** the two arms; the two halves; the 80–90 band (which is nearly the whole
  population — §10 threat 4); bull-only.
- **Never on the list, because they block rather than report:** C1, the halves, and bull-only.

**Quotability:** 20- and 40-session bases → **every number in this question is `NON_QUOTABLE`**
(rule 12).

### 4.4 Inference

Night-level throughout; control rows never add to n (rule 6). **Two CIs are reported for the primary
and both must clear** (DP-51):

- **CI-1 (registered, decides): tape-episode block bootstrap.** Resample **tape-episodes** (§2.6,
  carrying their contributing nights) with replacement within arm, 2,000 resamples, recomputing the
  arm means from the resampled episodes' nights. A stationary block bootstrap over the ordered
  contributing nights (expected block length **10 sessions**, the desk's standing value, fixed here at
  lock and not chosen after seeing anything) and a plain date-clustered CI are printed alongside and
  are expected to be *narrower*; where they disagree, the tape-episode bootstrap decides.
- **CI-2 (DP-51, decides jointly): symbol-episode-clustered bootstrap.** The bootstrap resamples
  **symbol-episodes** (§2.6) and **nights** jointly, 2,000 resamples. **Clearing MPE on CI-1 and not
  on CI-2 is INCONCLUSIVE, never CONFIRMED** (DP-51). The threat it answers is live here: the same
  handful of symbols recur across consecutive nights inside one tape-episode with almost fully
  overlapping 20-session windows, so a single symbol's run can move one arm's mean on its own.
- **p-value (decides): tape-episode label permutation** (§3 B3), 10,000 permutations, seed 20260914,
  preserving each episode's length and internal night order. A naive night-level label permutation is
  printed alongside, labelled **anti-conservative**, and never decides.
- **Every estimate prints:** contributing nights total and per arm; tape-episodes per arm and their
  length distribution; symbol-episodes and their length distribution; contributing nights dated after
  the lock commit; eligible picks per arm; not-takeable counts; control rows used and picks dropped
  for < 3 controls; post-match standardized mean differences on `beta60` / `atr_pct` / `runup20`;
  exclusions by reason; the nine-cell composition; and the §2.3 legality failures by reason code.

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights** for the primary endpoint and
  ≥ **20 contributing nights per arm**, plus ≥ 20 per *reported* sub-cell. A sub-cell below 20 is
  **SUPPRESSED** — counts only, no point estimate, not even "small n, directionally" — and a
  suppressed sub-cell does not by itself make the endpoint INCONCLUSIVE. The weaker "80 eligible with
  ≥ 20 contributing" reading is not used (DP-21). **No floor is ever lowered to reach a date.** On top
  of the night floors, §8 clause 2 requires **≥ 5 gate-counting tape-episodes per arm**; an episode
  shortfall is a **gate**, handled by §5.2's single extension and then DEFERRED, never an INCONCLUSIVE
  verdict.
- **Neither arm is demotable.** `G` **is** the BENIGN − HOSTILE contrast, so an arm below 20
  contributing nights leaves no endpoint: it is a floor failure — the single DP-13 extension, then
  DEFERRED — never a demotion to descriptive (DP-43's demotion clause has nothing to demote).
- **Binding maturity: 40 sessions**, uniform across every eligible pick.
- **DP-24:** ≥ 30 contributing nights dated after the lock commit. Here **every** contributing night
  is post-lock by construction (§6), so DP-24 binds at 30 of the 80 and is not the gate.
  **PROSPECTIVELY_CONFIRMED is reachable from this run by design; DP-31 does not apply and no
  successor replication question is needed.**

### 5.1 Exposure — what is measured, what is borrowed, and what R1 must supply

**No desk report has ever counted a bar-only tape partition.** The rates below are therefore of three
kinds and each is labelled; R1 (§5.3, **blocking for lock**) replaces the borrowed ones with measured
counts before this file is committed.

| quantity | value used to size | status |
|---|---|---|
| contributing nights per elapsed session (published slate, full funnel) | **0.9538** (62/65) | **borrowed** from `STEWARD_Q023_exposure.md` §1 (80–90 published picks, 2026-06-09..2026-09-10). This population is a **superset** of Q023's, so the true rate is ≥ 0.9538 and the borrow is conservative for floor A. R1(a) re-derives it under *this* funnel. |
| rarer-arm (expected: HOSTILE) nights per elapsed session | **0.20** | **planning placeholder only**, taken from Q023's measured *platform-label* rarer-arm rate — a different variable. It is not evidence about this partition and R1(b) replaces it. |
| rarer-arm contributing nights per gate-counting tape-episode | **3.0** | **planning placeholder**, Q023's measured 3.25 haircut because the bar-only label carries no hysteresis smoothing and its runs are expected to be shorter. R1(b) replaces it. |
| control-pool depth (≥ 3 valid controls per pick) | mean 51.8 / median 54 / min 39; 100% of nights ≥ 10 | **measured**, `STEWARD_Q023_exposure.md` §6, on a population this one contains |

**The one thing R1 cannot measure from the pinned freeze, stated plainly.** `manifest_prices_v001`
carries SPY daily bars from **2026-01-31** (manifest §tables, `start=2026-01-31`), so **`SMA200` does
not exist anywhere in it** and neither does the 250-session tercile calibration. R1(b) therefore
measures the arm split under an **SMA50-only** trend variant (`UP` iff `close_t > SMA50_t`), which is
registered at this lock as a **one-sided bound and used as one**: adding the `SMA50 > SMA200`
condition can only move nights **out of** `UP` and **into** HOSTILE, never the reverse, so the
SMA50-only HOSTILE count is a **lower bound** on the true HOSTILE exposure and the SMA50-only BENIGN
count is an **upper bound** on the true BENIGN exposure. The lock gate (§5.3 R1) is applied to the
**lower-bounded** arm without adjustment and to the **upper-bounded** arm with the explicit statement
that it is an upper bound; **if the upper-bounded arm is the one that fails the gate, Q032 goes to
DEFERRED rather than locking on a bound that runs the wrong way** (DP-45). The registered window's own
labels are unaffected — R2(i) delivers SPY from 2025-01-02, so every in-window night carries a true
`SMA200` and a true 250-session tercile. §11 item 2 carries this choice.

### 5.2 Window, decision date, extension, DEFERRED fallback (DP-43, DP-13; no outcome is looked at)

**Window: pick nights 2026-09-15 .. 2027-03-05 inclusive = 119 elapsed sessions**, after exclusions.
**Decision date: Monday 2027-04-12.** Single DP-13 extension to **2027-04-19** (149 sessions, DP-43's
+30), decided **Monday 2027-05-24**, which is also the **hard stop**: still short there, Q032 goes to
DEFERRED.

**Why exactly Q027's window, session for session.** Q032's endpoint runs on the same nights, the same
entry, the same 20-session clock and the same candidate-plus-control population as Q027, so **one
successor freeze pair serves both** (§5.3 R2) and one maturity horizon governs both. The window is
**longer than this question's own floors require on the planning rates** (§5.1's placeholders put
floor B at ≈ 105 sessions and floor A at ≈ 84), which is the permitted direction: a window is never
shortened to reach a date sooner (DP-43, DP-45), and sharing Q027's freeze removes a build the desk
would otherwise have to schedule twice.

**Floor projections at 119 sessions, on §5.1's rates — every floor projects met inside the primary
window:**

| floor | rate used | sessions needed | projected at 119 sessions |
|---|---|---|---|
| **A:** ≥ 80 contributing nights (DP-21, m = 1) | 0.9538/session (borrowed, conservative) | 84 | **113.5 nights** |
| **B:** ≥ 20 contributing nights in the rarer arm | 7 whole tape-episodes at 0.0667/session (0.20 ÷ 3.0) | 105 | **23.8 nights** |
| **C:** ≥ 30 contributing nights dated after the lock commit (DP-24) | 0.9538/session | 32 | **113.5** (all post-lock by construction) |
| **D:** ≥ 5 gate-counting tape-episodes per arm (§8 clause 2) | 0.0667/session (rarer arm) | 75 | **7.9 rarer-arm episodes** |

Floor B binds, and it rests on the one rate that is a placeholder. **R1 is therefore blocking for the
lock** (§5.3) and every date below moves **out** if R1's measured rate is slower; no date is ever
pulled in (DP-43, DP-45).

**Arithmetic, session by session** (holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18,
2027-02-15, 2027-03-26, 2027-05-31):

- **Window.** 2026-09-15 is session 1. Sep 12 + Oct 22 + Nov 20 + Dec 22 + Jan 19 = 95 at 2027-01-29;
  Feb 19 = 114 at 2027-02-26; Mar 1–5 = **119 at 2027-03-05** (Friday).
- **Decision date.** 2027-03-05 **+ 20 sessions** maturity (Mar 8–12, 15–19, 22–25 (Mar 26 is Good
  Friday), 29–31, Apr 1–2, Apr 5) = **2027-04-05** (Monday); **+ one calendar week** freeze margin =
  2027-04-12; first Monday on or after = **Monday 2027-04-12**. That is **6.9 months from the
  2026-09-14 lock**, inside DP-43's 12-month ceiling. `eval.py` is written once (rule 9) and run
  **once**, then. **No interim looks.**
- **Extension (DP-13; DP-43's +30 sessions).** If any gate — 80 contributing nights, 20 per arm,
  5 tape-episodes per arm, 30 post-lock nights — is short at 2027-04-12 on `eval.py`'s **own measured
  counts** (never on a projection or a run-rate), the window extends **once**, automatically and with
  no new question, to pick nights **2026-09-15 .. 2027-04-19** (session 149), decision date **Monday
  2027-05-24** (2027-04-19 + 20 sessions = 2027-05-17; + one week = 2027-05-24). The extended run uses
  the **byte-identical, unmodified `eval.py`** and the same gates. 8.3 months, still inside the
  ceiling. **The halves are re-cut on the extended window** by the same session-index rule (Half A =
  sessions 1–75, Half B = 76–149), fixed by that rule at this lock.
- **DEFERRED fallback (the hard stop).** If a gate is still short after that single extension, Q032
  goes to `research/questions/DEFERRED.md` with the measured counts rather than running under-powered.
  **No second extension, no reduced gate**, and **a gate shortfall is never an INCONCLUSIVE verdict**
  (§8).
- **Fixed at lock, not reopened at the decision pass:** the §2.2 arm definition and every cut in it;
  the §4.3 suppression list; the 80% HOSTILE composition guard; the ±10.0 pp MPE and the ±5.0 pp
  level lines; the block length; the seeds; the half-split rule; `m = 1`.
- **If a scoring or publication change ships mid-window** (§5.3 R2, §10 threat 8), the window is cut
  at the ship date, the **post-ship** segment becomes the question's window with this whole schedule
  recomputed from it — **out, never in**, subject to the same single extension and the same 12-month
  ceiling measured from the original lock — the pre-ship segment becomes a labelled descriptive panel
  entering no verdict, and if neither segment reaches the gates inside the ceiling the question is
  **DEFERRED** (DP-06, DP-50(a)).

### 5.3 Routed requests

- **R1 → data-steward — counts only, no outcome of any kind, BLOCKING FOR LOCK.** Measured on
  `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`, plus read-only `git log` /
  `git show` in the platform repo — never a live query (DP-50(c)). Over pick nights
  **2026-06-01..2026-09-10** (DP-06's segment; the arm is a 16:05 property with no outcome attached,
  so the widest legal span is used):
  **(a)** the §2.5 funnel re-derived under *this* population (all published picks, ≥ 1 eligible pick
  with ≥ 3 valid controls, matured) → contributing nights per elapsed session, replacing the borrowed
  0.9538;
  **(b)** the **§2.2 arm split under the SMA50-only trend variant** (§5.1): nights per arm, and
  **gate-counting tape-episodes per arm with their length distributions and contributing nights per
  episode** — stating explicitly which arm is the rarer one, and carrying §5.1's bound directions with
  each count;
  **(c)** the **nine-cell** `trend_t` × `vol_t` composition under the same variant, and the first
  session at which SPY has ≥ 250 prior sessions in the freeze (the honest start of the tercile
  calibration);
  **(d)** the night-level **agreement rate** between the §2.2 SMA50-only arm and the §2.3 platform
  label, with the §2.3 legality-failure count by reason code — the direct read on how much independent
  information the second definition carries (§10 threat 2);
  **(e)** the control-pool depth and the CTRA truncated-history scan re-run on this population;
  **(f)** the **DP-50(a)/(b) commit sweep** since manifest SHA `fa70688` — any change to the SAS
  weights, timeframe multipliers, `qualification_threshold`, `publication_floor`,
  `bear_publish_threshold`, `max_output_cap`, `min_completeness`, the ATR-elite caps, the GEX offset,
  the scoring enable-flags, the lane-plan writer, or `services/market_regime/scorer.py` (C1 only) —
  **with an explicit answer even when it is "none"**, and whether the **v1.7** scoring workstream is
  scheduled to ship inside the window.
  **The lock-or-DEFER gate** (DP-43's 12-month ceiling solved at this lock date: the latest admissible
  decision is Monday 2027-09-13, which back-solves through a one-week margin and 20 sessions of
  maturity to a window end of ≈ 2027-08-06, i.e. **225 admissible elapsed sessions**; the inequalities
  are the floors divided by 225, rounded **up**):
  contributing nights **≥ 0.36** per elapsed session; rarer-arm nights **≥ 0.09**; rarer-arm
  gate-counting tape-episodes **≥ 0.023**. All three clear → **Q032 locks**, with §5.2's dates moved
  **out** if the measured rates are slower than §5.1's placeholders and unchanged if they are faster.
  Any limb short → **Q032 goes to DEFERRED** with the measured counts and the re-check trigger
  "the Steward measures ≥ 0.09 rarer-arm contributing nights per elapsed session over a trailing
  quarter", not registered on a weaker partition (a different partition is a different question with
  its own id — DP-45).
- **R2 → data-steward (due at the decision date; not a blocker for lock; DP-23).** **Q027's successor
  freeze pair, shared**, with **one added scope requirement**:
  **(i)** the daily price freeze carries **SPY split-adjusted daily bars from 2025-01-02** through the
  freeze end — without them §2.2's `SMA200` and 250-session tercile do not exist and **no arm can be
  assigned**. If the extended SPY history cannot be obtained at the decision pass (the Q030 / H-074
  provisioning blocker: `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` absent from the desk session), **Q032
  is DEFERRED on that ground** — the partition is **never** re-specified to SMA50-only after the fact,
  because that is a different arm chosen after the data existed.
  **(ii)** the daily symbol list covers **every candidate symbol on every in-window night, published
  and unpublished**, with ≥ 60 prior sessions before 2026-09-15 (B2 needs their closes, beta60,
  atr_pct, runup20 and forward bars) — never assumed from v001's symbol list;
  **(iii)** hourly bars scoped to at least the published-pick symbols, for the descriptive entry audit
  only (no endpoint depends on an hourly bar);
  **(iv)** `market_regime_daily` included, for C1 only;
  **(v)** an **add-only successor exclusions file** applying the identical four criteria to post-lock
  nights; it may add nights and may never remove one;
  **(vi)** rows whose bars are missing are **excluded and counted, never back-filled or imputed**;
  **(vii)** R1(f)'s commit sweep **repeated for the period between the freezes**, with a dated
  `DATA_NOTES.md` entry for any repair that rewrites historical rows, and an explicit answer even when
  it is "none". **DP-50(a) guard:** where the successor freeze overlaps an earlier one on SPY's daily
  bars, the rows are compared and `eval.py` **fails loudly** on any disagreement — SPY's history is
  this question's conditioning variable, and a vendor restatement would silently re-run the
  experiment.
  Every §5.2 date is re-confirmed **session by session from the trading calendar** when the freeze is
  built; a correction may move a date **out, never in**.

## 6. Test window, split and stratification

- **Test window: prospective only — pick nights 2026-09-15 .. 2027-03-05** (119 elapsed sessions;
  .. 2027-04-19 if the single DP-13 extension fires).
  *Justification, and it is not optional here.* The sealed period **has already been read for this
  hypothesis**: the weekly snapshots of 2026-09-10 and 2026-09-12 printed regime-stratified cells, and
  H-079's own BACKLOG line records that the desk has seen them. Those nights are contaminated and are
  **not used for any verdict**. They are printed once, as a **labelled post-hoc panel**
  (pick nights 2026-06-01..2026-08-12, every §4 endpoint, computed from the successor freeze's
  extended SPY history so the §2.2 arm is the registered one), **split at 2026-07-06** — the
  `_enforce_ladder_monotonic` ship, which changes the ladders `d_L3` is read from — entering **no
  verdict, no CI comparison, no half, no stratum test, no q and no §9 rule**. It is largely
  right-censored by its own freeze and every panel endpoint prints its matured-night count beside it;
  immature nights are **counted, never graded as non-touches**.
  The window sits entirely after the 2026-06-01 catalyst fix (DP-06), after the 2026-07-06 ladder
  commit and after the 2026-07-08 `publication_floor` change (DATA_NOTES), so none of the three splits
  DP-06 / DP-50(a) would force falls inside it.
- **Split for "reproduced in two independent windows":** Half A = window sessions 1–60, Half B =
  sessions 61–119, **fixed by session index at this lock** (H-079: *split at lock*), re-derived from
  the trading calendar and re-cut by the same rule if the extension fires (§5.2). The primary must
  carry the same sign in both halves (§8 clause 5). The halves are a **stability clause, not a
  reported stratum**: they block at whatever count they have. `in_sample_end = 2026-05-29` marks only
  what is excluded.
- **Regime stratification (rule 7).** **Regime is the arm here**, so rule 7 is satisfied by the arm
  itself. Two further reads are computed and both are constrained by the §4.3 suppression list: the
  **nine-cell** `trend_t` × `vol_t` composition with per-cell `E_t` where a cell clears 20 contributing
  nights, and the **platform label** as C1 (§2.3) — which is the rule-7 stratum every other question
  on this desk reports, here promoted to a blocking companion.
- **Knowledge time (rule 14) — every input declared. Q032 needs no rule-14 exception and requests
  none** (DP-05 untouched, DP-41 respected).

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `overall_score`, `dominant_direction` | `sas_candidates` | pick night, 16:05 ET | population, strata, direction |
  | lane plans `L1…L6`, `analysis_status` | `sas_candidates.public_payload_json` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | levels, exclusions |
  | SPY split-adjusted daily closes, sessions ≤ t | `prices_daily_split` | pick-night close, 16:00 ET | **the arm** (SMA50, SMA200, 20-session realised vol, expanding terciles) |
  | `C_t`, ATR14, beta60, atr_pct, runup20 | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | distances, matching |
  | control-candidate pool (non-published rows for night t) | `sas_candidates` | pick night, 16:05 ET | B2 |
  | `market_regime`, `data_quality`, `regime_version`, `created_at` | `market_regime_daily`, v1.2, `trading_date = t` | declared 16:05 ET / lag 0 (`freeze_config.availability`), verified FREEZE_v001 §7 for nights ≥ 2026-06-09, enforced per night by §2.3's timestamp test | **C1 only** |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion; §2.3 legality |
  | session t+1 open `X`; daily bars t+1..t+40; hourly bars | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **entry and outcome measurement only** |

  **What `eval.py` must enforce:** the eligible-pick set, the arm label, the control sets and every
  stratum label are computed and written to a frozen per-pick and per-night table **before any
  post-pick-night bar other than the t+1 open is loaded**, and the t+1 open is used **only** as the
  entry price `X` — never to filter, classify, match or stratify. The run fails if any t+1-or-later
  field is referenced in eligibility, arm assignment, matching or stratification.
  `sas_selection_excursion` / `outcome_*` / `level_hit_*` columns are never inputs (calendar windows,
  close basis, recomputed weeks later, v1/v2 duplication — volatilx `services/sas_excursion.py:8-18`,
  `:336-354`; DATA_NOTES). `uoa_symbol_daily.fwd_return_*` is **banned** (FREEZE_v001 §5); no UOA
  table is used.

## 7. Multiple testing

- **Within the question: `m = 1`.** One primary, `G`. **`m = 1` is fixed at lock** and no second
  endpoint is added afterwards. Every secondary in §4.3 prints raw p only, marked *"descriptive, does
  not decide"*; the four blockers block without carrying a q.
- **Across the family: F2 Calibration.** The F2 correction set is computed at the decision pass over
  the F2 questions locked by then and **never falls below the count at this lock**: Q023 (2) +
  Q027 (2) + Q029's 10 companion IC endpoints + Q031 (2) + **Q032 (1) = 17**. Q005 is excluded (a
  diagnostic decomposition with no MPE, no directional primary and no outcome column read).
- **Companion correction in F1.** `G` is built on Q006's `E_t`, so — the Q015 / Q020 / Q029 / Q031
  pattern — it is **additionally** BH-corrected across F1: Q006 (2) + Q024 (6) + Q025 (2) + Q029 (16)
  + Q031's `D1ᴮ` (1) + **Q032's `G` (1) = 28**. **The larger of the two q's is the one quoted and the
  one §8 clause 9 reads.**
- **C1 carries no q of its own and is corrected jointly with Q023's E1.** `G_PL` and Q023's E1 are
  the same statistic on overlapping nights and a ~95%-overlapping population (§1). They are reported
  as **one non-independent pair**, the Reporter cross-references them, and **neither may ever be read
  as confirming the other**.
- Threshold: **q ≤ 0.10**, alongside raw p (rule 8).
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q006 (F1)** owns the *level* of `E_t` — does selection beat the matched control at all. Q032
    owns whether that level is conditional on the tape. `G` can be large while Q006's excess is zero,
    or the reverse; §8 clause 3 (`NO_EDGE_TO_CONDITION`) is the clause that keeps the second case from
    being reported as a regime finding. Q006's 2026-10-05 decision lands inside this window and
    **changes nothing here** — no arm, no MPE, no clause, no date.
  - **Q023 (F2)** is one cell of H-079 under the *other* regime definition, on the 80–90 band. Its E1
    and Q032's C1 are the same statistic (§1, above); Q032's **primary** is a different partition
    computed from bars alone, and that is the whole reason Q032 exists rather than being merged.
  - **Q027 (F2)** shares this window, this freeze, this entry and this clock, and asks whether
    `overall_score` orders outcomes at all. A ranking edge and a regime-conditional selection edge are
    independent claims; neither confirms the other.
  - **Q031 (F2)** asks whether the edge *decays in time*; Q032 asks whether it is *conditional on the
    tape*. They are each other's principal competitor — Q031 §8 clause 7 (`TAPE_COMPOSITION`) routes a
    reweighting-sensitive decay result **to H-079, i.e. to this question**, and Q032 §9 returns the
    favour: a `G` that is large while Q031 reports STABLE is the separation both questions were built
    to make, and a `G` that is large while Q031 reports DECAY is **not** two findings.
  - **Q022 (F4)** uses the identical two-stage shape (within-night control-adjusted rate, then a
    between-night arm contrast) on a different night-level arm (sector concentration). If concentrated
    slates cluster in calm uptrends, the two are reading overlapping structure; neither confirms the
    other.
  - **H-080 (F2, unregistered)** owns the 90 threshold; a suppressed 90+ cell here licenses nothing
    about it.

## 8. Decision rule (numeric, written before unsealing)

`G` is in **percentage points of control-adjusted L3-touch rate within 20 sessions from the t+1 open,
BENIGN minus HOSTILE**, over the contributing nights of §2.6. Two-sided. H-079 predicts `G > 0`.

**MPE ±10.0 pp** (§4.2). The level lines are **±5.0 pp** (DP-20) and appear only in clauses 3 and 4.
**No MPE and no level line is lowered at the decision pass in any branch.**

**HISTORICALLY_CONFIRMED** requires **all** of:

1. **contributing nights ≥ 80**, **≥ 20 per arm**, **≥ 30 dated after the lock commit** (DP-21,
   DP-24), and ≥ 20 for any sub-cell that is *reported*. A sub-cell below 20 is **SUPPRESSED**
   (counts only) and does **not** by itself make the endpoint INCONCLUSIVE. The suppression list is
   fixed at lock (§4.3) and restricts affirmative reporting only: it never removes clauses 5–7's
   blockers, whatever their cell counts;
2. **≥ 5 gate-counting tape-episodes per arm** (§2.6). Fewer means the contrast is a comparison of two
   calendar stretches wearing a tape label. **This is a gate, not a verdict:** an arm below 5 fires
   the **single automatic DP-13 extension** (§5.2); still short after it, Q032 goes to **DEFERRED**.
   No second extension, no reduced gate, and **never an INCONCLUSIVE verdict on this ground**;
3. **an edge exists to be conditional on:** the pooled `mean_t E_t` over all contributing nights is
   **beyond +5.0 pp** (DP-20). Inside it, the verdict is **INCONCLUSIVE** with the label
   `NO_EDGE_TO_CONDITION`, it decides nothing about regime, and it is routed to Q006 and Q027 (§4.2);
4. `|G| > 10.0 pp`, **and the confirmed verdict carries its §4.2 label**: `WORKS_IN_BENIGN` if
   `mean_{t ∈ BENIGN} E_t > +5.0 pp`, otherwise `HOSTILE_ONLY`. Both are confirmations; §9 licenses
   different things from each, and the label travels wherever the verdict is restated;
5. the point estimate has the **same sign in both halves** (§6) and neither half is beyond MPE in the
   opposite sign — H-079's "reproduced with the same sign in two independent windows";
6. **C1 does not contradict it:** the platform-label contrast `G_PL` (§4.3) is **not beyond 10.0 pp in
   the opposite sign**. C1 confirms nothing on its own in any branch;
7. the **bull-only** version (§4.3) is not beyond MPE in the opposite sign;
8. **the HOSTILE arm is not a different question from the one registered:** if any single one of the
   eight HOSTILE cells carries ≥ 80% of HOSTILE contributing nights, the verdict is **restated as
   being about that cell** wherever it appears, and every §9 sentence names it. (A naming clause, not
   a floor reduction. The 80% is fixed at lock and may not be moved in either direction.)
9. **both CIs exclude 0** — the tape-episode block bootstrap (CI-1) **and** the symbol-episode
   bootstrap (CI-2, DP-51). **Clearing MPE on CI-1 and not on CI-2 is INCONCLUSIVE, never
   CONFIRMED.** The tape-episode label permutation p (§3 B3) supports it, and BH **q ≤ 0.10** in
   **both** F2 (m = 17) and F1 (m = 28), with the **larger q** quoted (§7).

- **NULL:** floors and clauses 1–3 met, **and** both CIs include 0, **and** `|G| < 10.0 pp`. *"The
  selection edge is the same size in calm uptrends and in everything else"* is a real finding: it
  **retires regime as an explanation for weak stretches** — H-079's own FAIL action — and it is
  ledgered with the same care as a positive.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, C1 or the bull-only version beyond MPE
  in the opposite sign, `0 < |G| ≤ 10.0 pp` with a CI excluding 0 ("real but below MPE", rule 6), a CI
  including 0 with `|G| ≥ 10.0 pp`, CI-1 and CI-2 disagreeing, or the clause-3 `NO_EDGE_TO_CONDITION`
  label. **A gate shortfall is never INCONCLUSIVE** — not the 80-night floor, not the 20-per-arm
  floor, not the 30-post-lock-night floor, not the 5-episodes-per-arm gate: each fires the single
  DP-13 extension, then DEFERRED (§5.2).
- **What a confirmed `G` does and does not mean (binding on the report).** A CONFIRMED positive `G`
  means *"on nights when SPY is above a rising 50-session mean that sits above its 200-session mean,
  and its 20-session realised volatility is not in the top third of its own history, published picks
  beat their same-night distance-matched look-alikes to the printed swing target by N pp more than on
  other nights"*. It does **not** mean the picks rose more, it does **not** mean money was made, and
  it does **not** mean the platform's own regime label marks the same thing — the raw arm contrast,
  the T+20 returns and C1 are the numbers that speak to those, and all three must be quoted beside it.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5) — it requires ≥ 30 contributing
  nights dated after this file's lock commit (DP-24, DP-21), which every contributing night here is,
  frozen in the successor manifests and never inspected earlier, reproducing the sign of the endpoint
  under the unmodified `eval.py`. The clause does not weaken. No subscriber-facing statement before
  that (rule 10); even then the basis is `NON_QUOTABLE` until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform already conditions on regime in one direction: `allow_bull_earnings_bonus` fires
only when `market_regime ∈ {bullish, strongly_bullish}`, `regime_phase == 'impulse_up'` and
confidence ≥ 0.70 (volatilx `services/market_regime/scorer.py:427-442`), so the engine treats a
strong tape as a reason to score *higher*. **Nothing on the platform computes a bar-only tape state,
and no surface tells a subscriber that the evidence for a pick is weaker tonight than it was last
month.** Rules below fire **only** where §8 licenses them, and nothing subscriber-facing ships before
PROSPECTIVELY_CONFIRMED (rule 10).

- **CONFIRMED positive, labelled `WORKS_IN_BENIGN`:** (a) a **lane rule** in the Manual Trading Guide
  — the measured BENIGN and HOSTILE levels printed side by side with their night and tape-episode
  counts, and the plain statement that the desk's own path evidence is conditional on the tape state
  named in §2.2; (b) an `INTERNAL_TOOL`, flag-off card field showing the night's `trend_t` / `vol_t`
  state and the measured conditional expectation (DP-48 — an internal tool may be briefed at any
  stage); (c) a brief for a **nightly tape-state field** computed from SPY bars alone, shipped
  flag-off with a byte-identical checksum on the old path and shadowed ≥ 20 trading days before any
  flip (rule 11). **A publication gate on HOSTILE nights is not licensed by this question** —
  suppressing picks changes the product's shape and needs its own registered question.
- **CONFIRMED positive, labelled `HOSTILE_ONLY`:** the guide line only, worded as *"the edge is less
  negative in calm uptrends"*, with an explicit sentence that **no regime in this partition is one
  where the edge is positive**. No flag, no card field, no sizing rule, no marketing claim.
- **CONFIRMED negative** (the edge is *larger* in hostile tape): the finding is published with the
  opposite sign, and the desk's own standing habit of discounting difficult stretches is corrected in
  the ledger and in the weekly.
- **NULL:** the desk **stops attributing weak stretches to regime**. Concretely: the weekly's
  regime-stratified panels are labelled as composition, not signal; H-079's FAIL action ("do not
  invent regime explanations for bad periods") becomes a standing line in the Reporter's
  instructions; and the measured HOSTILE-arm band becomes the number that replaces the phrase "it was
  a difficult tape". This is a result, not a non-result.
- **`NO_EDGE_TO_CONDITION` (clause 3):** **nothing changes anywhere**, and the report says so in one
  sentence. The question is routed to Q006 and Q027 and re-enters the queue only if a level is
  established there.
- **C1 licenses nothing in any branch.** No guide line, brief, flag or quoted number may rest on the
  platform-label contrast computed here — it is Q023's endpoint, Q023 decides it on 2027-06-07, and
  this question's copy of it exists only to block.
- **The suppressed cells license nothing.** No guide line, brief, flag or quoted number may cite the
  90+ cell, a bear-only cell, or any cell on §4.3's lock-time suppression list, whatever it shows.
- **Q032 is in flight from this lock until its decision date, and DP-50(b) applies to the platform in
  the meantime.** There is one database, and a repair or a config change rewrites what this question
  reads. Any change to the SAS weights, the timeframe multipliers, `qualification_threshold`, the
  ATR-elite caps, the GEX offset, the scoring enable-flags, `publication_floor`,
  `bear_publish_threshold`, `max_output_cap`, `min_completeness` or the lane-plan writer —
  **including any promotion of the v1.7 score** — is **flag-off until 2027-04-12** (2027-05-24 if the
  extension fires), the same clause and the same dates Q027 and Q029 carry, checked before any fix
  brief is written. A change to `services/market_regime/scorer.py` affects **C1 only** and is a
  DP-06 split for that companion, not for the primary — which is the practical payoff of a bar-only
  arm. If any listed change ships anyway it takes a dated `DATA_NOTES.md` entry naming the column, the
  date range and the ship SHA, and §5.2's window split applies (DP-06, DP-50(a)).
  **DP-49 binds every brief this question produces:** each check handed to the **coding agent** must
  be satisfiable from the platform repo alone — the test suite, a pure-function import, `git show
  --stat`, a file diff. Anything that reads or writes a table belongs in the brief's verification
  section, addressed to the Data Steward on `$RESEARCH_DB_URL`, or to Haci where a write is required;
  where a frozen manifest covers the affected table, the brief names that parquet as the
  before-snapshot rather than asking anyone to capture one (DP-50(c)).
- Owner: implementer. Shadow period before any flip: ≥ 20 trading days.

## 10. Known threats to validity (registrar's own list)

1. **The arm is calendar.** Tape states arrive in long runs, so BENIGN and HOSTILE are two sets of
   calendar stretches and 80 nights are not 80 independent draws. This is the single largest threat.
   It is answered four ways, all pre-specified: the **tape-episode block bootstrap** and
   **tape-episode label permutation** (§4.4); the **≥ 5 gate-counting episodes per arm** gate, which
   is a gate and not a verdict (§8 clause 2); the **both-halves** clause (§8 clause 5); and the
   **episode definition on the label series** (§2.6), so an excluded night inside a stretch cannot
   manufacture an extra independent draw. None makes the threat vanish; together they stop a
   two-stretch contrast being read as 80 independent nights. A tape that simply never leaves one state
   for six months is the **DEFERRED** route, and it is a real and correct outcome (Q023's NOTSTRONG
   arm produced nothing for the 30 sessions before its lock).
2. **The two regime definitions may be the same variable.** `strongly_bullish` requires a low secular
   risk score dominated by the weekly trend gap and the 200DMA distance (`scorer.py:36-39`, `:78-110`)
   — i.e. by trailing SPY price, which is what §2.2 computes directly. If the §2.2 arm and the §2.3
   label agree on ~every night, C1 is not an independent check and Q032 is Q023 with extra picks. R1(d)
   measures the agreement rate **before the lock**, precisely so the desk knows this in advance rather
   than discovering it at the decision pass; the rate is printed beside C1 in every branch, and §8
   clause 6 still binds either way (an agreeing C1 cannot confirm; a disagreeing C1 can block).
3. **The partition is the registrar's, and a different one could give a different answer.** BENIGN =
   `UP` ∧ `vol ∈ {LOW, MID}` is a convention (DP-26), fixed at lock, never derived from an outcome —
   but it is one of many. The nine-cell composition and the ordered three-state trend read are printed
   so a reader can see the partition's internals; **no alternative cut is fitted at the decision pass,
   and a different partition is a different question with its own id** (DP-45).
4. **The population is nearly the whole traded book.** `publication_floor = 80.0` since 2026-07-07 and
   90+ is thin and shrinking, so "the published slate" is in practice the 80–90 band. Every §9
   sentence must say *"the published slate"*, never *"high-scoring picks"*, and the 90+ cell that
   would separate them is SUPPRESSED at lock.
5. **Direction mix.** Bear publications are gated separately (`bear_publish_threshold`) and are
   plausibly commoner in hostile tape, so the arm partly contrasts a bull-heavy book against a mixed
   one. Because bear picks grade *below* base rate in-sample (H-062), this confound pushes **against**
   H-079's predicted sign — the conservative direction — but it is still a confound: the direction mix
   is printed per arm and §8 clause 7 makes the bull-only version binding.
6. **The control absorbs the tape, which is the point and also a limit.** `E_t` is a within-night
   difference, so a night on which everything ran gives `E_t ≈ 0` exactly like a night on which
   nothing did. Q032 therefore cannot say the slate *pays* more in benign tape — only that it beats
   its look-alikes by more. The raw arm contrast and the T+20 returns are printed beside it and are
   descriptive (DP-12: the total effect licenses no rule); a money version of this question would need
   a committed plan endpoint and is not registered here.
7. **Band membership depends on a stored score that has been rewritten before.** The in-sample
   catalyst rescore and the E9a correction batch show `sas_candidates` rows are not immutable.
   `eval.py` re-derives each pick's band from `score_details_json` where the layer subscores are
   present and **fails loudly** on a disagreement with `overall_score` beyond 0.05.
8. **Config drift inside the window.** A change to the weights, multipliers, publication gates or the
   lane-plan writer changes what "a published pick" or "its printed L3" means. Every item is named in
   R1(f) and repeated in R2(vii); `eval.py` prints the per-night `config_json` composition and **fails
   loudly — it does not silently exclude** — if an in-window night's scoring fields differ from those
   in force at lock. A silent exclusion would let the window die quietly; a loud failure cannot
   (DP-45).
9. **One database (DP-50).** A platform repair between freezes can rewrite the rows this question
   reads. The §5.3 R2 cross-freeze comparison fails loudly on disagreement — including on **SPY's own
   daily bars**, which assign the arm, and where a vendor restatement would silently re-run the
   experiment.
10. **Overlapping 20-session windows** inflate precision at this horizon, across nights *and* across
    the same symbol re-selected on consecutive nights. CI-1 handles the first, CI-2 (DP-51) the
    second, and both must clear.
11. **The SPY history the arm needs does not exist in any manifest pinned today.** §2.2 needs 200
    sessions of SMA and 250 sessions of tercile calibration; `manifest_prices_v001` starts 2026-01-31.
    R2(i) is the fix and **its failure is a DEFERRED ground, not a re-specification ground** (§5.3);
    R1's lock gate runs on the SMA50-only one-sided bound described in §5.1. This is the threat most
    likely to stop the question, and it is a provisioning problem (the Q030 / H-074 blocker), not a
    measurement one.
12. **Ladder and payload defects.** Null-ladder, non-monotone and split-scale payloads (DATA_NOTES)
    are excluded and counted; the question speaks only for published picks carrying a complete,
    monotone, correctly-scaled swing target.

---

## Open decisions before lock

1. **Which of H-079's two regime definitions carries the primary.** — Options: A the **bar-only §2.2
   partition** is the single primary (`m = 1`) and the platform label is a blocking companion that
   confirms nothing / B both are primaries (`m = 2`). Recommendation: **A**, because the platform
   label has taken exactly two values in its whole point-in-time-legal history, so its only partition
   with exposure **is** Q023's locked E1 on ~95% of this population — B would give the desk a second
   bite at a locked question's statistic and double-count it in F2.
   Changes: §1, §2.3, §3 B4, §4.2, §4.3, §7, §8 clause 6, §9.
2. **How the lock gate handles SPY's missing 200-session history.** — Options: A R1 measures the arm
   split under an **SMA50-only** variant and the gate is applied to it as the registered one-sided
   bound (lower bound on HOSTILE, upper bound on BENIGN), with R2(i) delivering SPY from 2025-01-02
   for the real window and **DEFERRED** if it cannot / B defer Q032 now until a freeze carrying
   extended SPY history exists. Recommendation: **A**, because the bound runs in the conservative
   direction for the arm the floors bind on, the registered window's labels are unaffected, and the
   fallback if R2(i) fails is DEFERRED rather than a re-specified partition.
   Changes: §5.1, §5.3 R1/R2, §10 threat 11.
3. **How the pooled HOSTILE arm is protected from being one sub-state in disguise.** — Options: A
   pool the eight non-BENIGN cells with the **80% composition guard** that *renames* the verdict
   (§8 clause 8) / B register the HIGH-vol contrast and the not-UP contrast as two separate primaries
   (`m = 2`). Recommendation: **A**, because H-079 filed one primary and two thin arms would fail the
   20-night floor and reach DEFERRED without either being testable; the guard keeps the claim honest
   without splitting the sample.
   Changes: §2.2, §4.3, §8 clause 8, §9.
