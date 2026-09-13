# Q014 — uoa_persistence: does a week of repeated unusual-options activity before the pick night make a SAS pick better, and does SAS add anything to the names UOA kept flagging?

**Status:** REGISTERED — decisions applied, locked by committing this file (`PREREG_LOCKED --by desk`, DP-46). Nothing in this file is open.
**Family:** F5 Cross-engine interaction (hypothesis H-040)
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`, `uncorroborated_publication_runs.trading_dates`) — the newest exclusions file (DP-22); `eval.py` reads the JSON, no hard-coded dates.
**Measured exposure (`research/reports/STEWARD_Q014_exposure.md`, 2026-09-13, counts only — no outcome of any kind was computed, rule 3 intact):** on pick nights 2026-06-01..2026-08-12, **48 matured non-excluded nights / 383 published picks → 369 eligible** on 47 nights after the §2.4 funnel; arm split **PERSIST 164 (44.4%) / MID 174 (47.2%) / NONE 31 (8.4%)** on the §2.1 reconstructed three-bucket definition; **E1 contributing nights 22, E2 46**, i.e. measured rates **E1 22/51 = 0.4314** and **E2 46/51 = 0.9020** contributing nights per session — **E1 binds**, and the §5 schedule is computed from E1's rate. Knowledge-time part (a) returned **VERIFIED single application** (§2.1). **Every gate is decided on `eval.py`'s own measured counts at the decision pass**, never on this report or on a projection.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) · **Date:** 2026-09-13
**Decisions:** DECISIONS.md

---

## 1. Hypothesis (plain English)

**When the same stock keeps showing up in the unusual-options screener in the week before it is
picked — three or more of the five sessions before the pick night, with the flow pointing the same
way as the pick — the pick reaches its swing target L3 more often than a look-alike stock does, and
more often than a pick with no such prior flow; and, separately, the picks SAS chose from among those
persistently-flagged names do better than the persistently-flagged names SAS passed over.**

BACKLOG H-040 reads: *"UOA appearances in prior 5 sessions (0 / 1–2 / 3+) × SAS-selected → return —
baselines: 3+ UOA not selected; selected with 0 UOA."* Two things in that line are fixed here rather
than inherited. First, **the endpoint is the path, not the return** (rule 5, DP-01): a fixed-horizon
close-to-close return is computed and printed but decides nothing. Second, **"UOA appearance" is
given an exact, knowledge-time-legal definition** (§2), because the raw presence of a row in
`uoa_symbol_daily` means only "this symbol is in the ~500-name screener universe" and is not a
signal at all.

Two primaries, one per baseline the backlog names:

- **(E1, does prior flow add to a pick)** among **published picks**, is the distance-matched excess
  L3 touch rate higher for the **3+ prior-UOA-days** arm than for the **0 prior-UOA-days** arm, paired
  within night;
- **(E2, does SAS add to prior flow)** among symbols that already had **3+ prior UOA days**, do the
  **published** ones touch L3 more often than the **unpublished** ones carrying a synthetic target at
  the same ATR distance.

No sign is presumed; both tests are two-sided.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night first;
  both estimators are within-night contrasts, so the night's tape is held fixed. Control rows never
  add to inferential n.
- **Source tables (manifest_v001 and its successor):** `sas_candidates` (`qualified`,
  `selected_rank`, `overall_score`, `dominant_direction`, `best_timeframe`, `completeness_score`,
  `public_payload_json` → `lane_plans.swing_trading.targets`, `outcome_target_invalid` for the
  exclusion audit only), `sas_runs` (`finished_at`, for the DP-04 exclusion criterion only),
  `uoa_symbol` (`score_day`, `score_swing`, `score_long`, `label_day`, `label_swing`, `label_long`,
  `oi_confirm_mult` — see the reconstruction rule below).
- **Source tables (manifest_prices_v001 and its successor):** `prices_daily_split` (pick-night close,
  session t+1 open/high/low, forward bars, ATR14, beta60, runup20, SPY tape), `prices_daily_raw`
  (split-factor snapping only). **Hourly bars are not used by any endpoint**: the E2 control pool has
  no hourly coverage, and rule 5 requires one basis on both sides (§4 ordering rule).

### 2.1 The conditioning variable — "a strong same-direction UOA day"

For symbol `s`, session `u` and trade direction `dir` (+1 bullish, −1 bearish):

`strong(s, u, dir) = 1` iff **any** bucket `b ∈ {day, swing, long}` has
`score_b*(s, u) ≥ 70` **and** `label_b(s, u) = BULLISH_FLOW_SETUP` (dir = +1) or `BEARISH_FLOW_SETUP`
(dir = −1).

- `score_b*` is the **16:05-ET value** of the bucket score. `score_day` is frozen as written.
  **`score_swing` and `score_long` are overwritten in place by the next-morning OI-confirmation run**
  — `sym_row.score_swing = score_swing × oi_mult`, `sym_row.score_long = score_long × oi_mult`,
  volatilx `services/uoa_screener.py:2236-2239`, with `oi_mult ∈ {0.90, 1.00, 1.05, 1.10}` stored in
  `oi_confirm_mult` (`:2223-2232`). `eval.py` therefore recovers the point-in-time value exactly:
  `score_b* = score_b / oi_confirm_mult` where `oi_confirm_mult` is non-null, `score_b` otherwise.
  `label_b` is written once at 16:05 from the pre-multiplier score (`:1728-1734`) and is never
  rewritten, so labels are used as frozen. **`oi_confirm_mult` is used only to undo a post-hoc
  mutation and never as a feature** — the reconstructed quantity *is* the 16:05 value. This is the
  reason **Q014 needs no rule-14 exception and requests none** (DP-41; DP-05 untouched).
- The `≥ 70` cut and the direction-matched label are the operationalisation H-040 was seeded with
  (`research/reports/explore/scripts/70_seeds.py:65-83`; EXPLORE_001 §G). They are not re-united or
  re-cut (DP-25, DP-26). The reason a bare label is not enough is recorded there: non-NOISE labels
  cover about half the universe every day.

**Knowledge-time verification of the reconstruction (sealed window, returned before lock).** The
Steward verified on the full frozen population, sessions 2026-05-22..2026-08-12 (56 sessions, 27,840
`uoa_symbol` rows), that the multiplier was applied **at most once per row and stored whenever
applied** — verdict **VERIFIED single application** (`research/reports/STEWARD_Q014_exposure.md` §(a),
counts only): **1,190 non-null multipliers, 0 of them outside {0.90, 1.00, 1.05, 1.10}**; **0 rows in
any month** where the OI pass ran (`oi_confirm_score` / `oi_confirm_ratio` / `oi_confirmed_contracts`
non-null) while `oi_confirm_mult` is null, so the unrecoverable population this question feared **does
not exist in this window**; **0 of 13,646** flow-setup-labelled rows with `score_day` below the
label's own 35 floor, the same zero-inconsistency signature as a bucket never rewritten; and **0 of
16,264 reconstructed `score_swing*`** and **0 of 9,720 `score_long*`** below that floor — including
the single raw `score_long` borderline case, which resolves cleanly under **one** division. The
reconstruction moves **3 of 369** arm assignments (0.8%, all MID→PERSIST by one step: APH 2026-06-05,
APH 2026-06-08, MO 2026-07-24). **Branch (i) of the cascade below therefore governs and the
three-bucket definition stands.** *Residual limitation, disclosed and not resolved:*
`uoa_screener.py:1996-2024` guards its own re-execution unless a force flag is passed, and the frozen
data carries **no run-history table** for that pass (the same absence as PI-004 / PI-012's
`super_agent_select_runs`), so a **forced** manual re-run cannot be positively excluded from the data
alone; nothing in the data shows one, and a second application would have had to produce a compound
multiplier outside the four documented values (**0 observed**) *and* leave all 25,984 reconstructed
label/score pairs consistent. The `updated_at − created_at` gap (median 143.3h with a multiplier vs
120.5h without) is **not usable as a signature** — `updated_at` is bumped by other backfills — and is
cited neither for nor against. Filed as **PI-013** (§10 threat 1); Q014 does not depend on it being fixed.

**Pre-committed cascade (fixed here, before any outcome exists; re-evaluated by `eval.py` over the
whole registered window, pre-lock and post-lock nights alike).** The Steward's verification covers only
the sealed sessions, so `eval.py` re-runs checks (i) and (ii) — the multiplier value distribution, and
the count of rows where the OI pass ran with a null multiplier — over **every** lookback session in the
registered window, per month, **inside the frozen pre-outcome per-pick table §6 already requires it to
build before the first session-t+1 bar is loaded**. Then, deterministically and with no judgment:

1. **(i) Verified** — no multiplier outside {0.90, 1.00, 1.05, 1.10} and no "ran but null" row anywhere
   in the window ⇒ the three-bucket reconstruction above governs, as it does for the sealed nights.
2. **(ii) Not verified** — a single value outside the set, or a single "ran but null" row, on any night
   ⇒ the conditioning variable falls back **automatically and for the whole window** to **`score_day`
   only**, the one bucket `uoa_screener.py:2236-2239` does not rewrite, every other definition in this
   file unchanged.
3. **(iii) `score_day` itself not point-in-time** — it fails its own label-consistency check ⇒ Q014
   would need a new rule-14 exception, the desk grants none (DP-41), the run is **not made** and the
   question goes to `research/questions/DEFERRED.md`.

**Diagnostics `eval.py` prints every run, whichever branch fires:** (a) the count and share of lookback
rows carrying a non-null `oi_confirm_mult` and its value distribution, by month; (b) the number of
`strong` flags and the number of **arm assignments** the reconstruction changes versus the frozen
values; (c) the count of reconstructed scores landing within **±0.5** of the 70 cut, with both readings
of that rounding band printed as a named sensitivity; and (d) the whole conditioning variable rebuilt
on **`score_day` only**, as the §10 threat-1 sensitivity. None of (a)–(d) decides anything.

**Persistence count.** `uoa5_p` = number of sessions among the **5 trading sessions strictly before**
pick night `t` on which `strong(symbol_p, u, dir_p) = 1`. The pick night itself is excluded (the flow
layer already scores it — `services/super_agent_select_scoring.py:512-517`, `:613-617`).

**Arms (DP-25's bins, as the hypothesis writes them):**
`PERSIST` = `uoa5 ≥ 3` · `MID` = `uoa5 ∈ {1, 2}` (descriptive only, monotonicity) · `NONE` = `uoa5 = 0`.

### 2.2 Treatment rows

Every **published** pick — `qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28); dark-lane
(`qualified IS TRUE`, `selected_rank IS NULL`) and qualified-false rows are never treatment rows — on
a non-excluded night in the §6 window, carrying a swing-lane first target.

- **Lane, level and clock (DP-42, DP-09).** H-040 names no level, so the swing lane's first target
  **L3** (`public_payload_json.lane_plans.swing_trading.targets[0]`; volatilx
  `services/sas_conviction_card.py:182-187`) on a **20-session clock from the stated entry**. The
  platform's 40-session swing window is reported alongside, descriptively, where it has matured.
- **Definitions** (all prices in the signal-date split basis): `C_t` = the pick's actual
  regular-session close on night `t` from `prices_daily_split` (never the platform's `spot_close`,
  stale on re-run nights); `ATR` = ATR14 from `prices_daily_split` bars dated ≤ `t` (never the
  platform's `atr_pct`, corrupted around splits — DATA_NOTES / PI-003); `dir` = +1 bullish, −1
  bearish from `dominant_direction`; `O_1` = the session t+1 **official** regular-session open;
  `d_close = dir × (L3 − C_t) / ATR` (the **matching distance**, §2.3);
  `d_open = dir × (L3 − O_1) / ATR` (**diagnostic and stratum only**, never a matching distance).

### 2.3 Control pools

- **Pool A (E1's rule-5 distance-matched control).** For each eligible pick: the **10 nearest**
  same-night **non-published** `sas_candidates` rows of the **same direction** with
  `completeness_score ≥ 35`, on `beta60` / `atr_pct` / `runup20` computed from `prices_daily_split`
  bars dated ≤ `t`, standardized by the night's cross-sectional median and MAD, Euclidean, with
  replacement across picks, ties by symbol ascending. This is **the Q006 §3 / Q011 §3 construction
  *plus* a `completeness_score ≥ 35` screen**: no locked question's control pool carries that screen,
  and the deviation is named here rather than left implicit. The screen is 16:05-legal,
  outcome-independent and applied identically to both arms, so it stands (DP-26), and `eval.py` prints
  the number of same-night non-published candidates it removes and the per-pick pool size **before and
  after** it, so any Q006 / Q011 cross-reference is read with the deviation in view. Minimum **3**
  neighbours; a pick with fewer is dropped from E1 and counted. *Measured in the sealed window
  (STEWARD_Q014_exposure.md §(c)): the screen removes **0 of 2,354** candidates — the minimum
  `completeness_score` observed is 65.4 — so Pool A is in practice the locked construction here;
  per-pick pool size min 16 / median 26 / max 30, with **0 of 369** picks below the 3-neighbour
  minimum. The before/after print stays regardless, because the post-lock nights are unmeasured.*
- **Pool B (E2's baseline — "3+ UOA not selected").** For each eligible **PERSIST** pick: the 10
  nearest same-night **non-published symbols that themselves carry `uoa5 ≥ 3` in the pick's
  direction**, on the same three features, same standardization, minimum **3**. The pool is drawn
  from the whole UOA screener universe — a persistently-flagged name that never entered the SAS
  candidate universe is still "3+ UOA not selected" — restricted to symbols with daily bars in the
  pinned price freeze (§5 R2 extends the freeze to that ≈ 500-symbol universe; symbols without bars are
  dropped and counted, **never back-filled**). **Pool B proper cannot carry the `completeness_score`
  screen** — its symbols come from the UOA universe and have no such column; the screen **does** apply
  to the Pool-B **sub-pool** of same-night non-published *SAS candidates* ("SAS saw it and passed"),
  which is reported as a secondary. That asymmetry is disclosed here, not patched. *Measured in the
  sealed window: Pool B per PERSIST pick min 21 / median 56 / max 93, **0 of 164** below the
  3-neighbour minimum, contributing on 46 of 47 nights — E2 can carry a verdict (§10 threat 9 did not
  fire). **71 of 502** UOA symbols (14.1%) have no daily bars in `manifest_prices_v001`, costing **56
  qualifying-but-dropped instances** across the 164 PERSIST picks (mean 0.34, max 2 per pick); closing
  that gap prospectively is what R2(iii)'s widened symbol scope is for.*
- **Synthetic target for every control** (rule 5, identical ATR distance and direction), **Pool A and
  Pool B alike**, the locked Q006 §3 step 3 construction verbatim: measure the pick's distance from its
  **close**, `d_close,p = dir_p × (L3_p − C_{t,p}) / ATR_p`, and place the control's target at
  `L3_c = C_c × (1 + dir_p × d_close,p × atr_pct_c)`, anchored at the control's **own** pick-night
  close and graded from the control's **own** session t+1 open over the **same** 20 sessions, under the
  same "at or through the entry is not a hit" rule. **Why the close basis and not `d_open,p`:** sizing
  the control's target with the pick's *post-gap* distance while grading it from the control's *own*
  open subtracts each control's own gap a second time, so the two sides would not carry the same ATR
  distance, which is exactly what rule 5 requires. Every eligible pick has `d_close,p > 0` by §2.4's
  wrong-side-L3 exclusion, so the construction is always defined. `d_open` survives only as the
  gap-through diagnostic (`d_open ≤ 0`) and as the ATR-distance tercile cell.

### 2.4 Exclusions — each counted per arm and printed in the results header, never silently dropped

Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or a
measurement failure.

- Nights in **`research/data/exclusions_v003.json`** — the union of `manual_runs.trading_dates`,
  `non_session_runs.trading_dates` and `uncorroborated_publication_runs.trading_dates`. In-window
  these are **2026-06-26**, **2026-07-02**, **2026-07-06** (DATA_NOTES). `eval.py` reads the JSON;
  **no date is hard-coded** in this file or in `eval.py` (DP-22).
- Any prospective night whose `finished_at` is later than the next session's open (DP-04).
- **Null-ladder denominator:** picks with no lane plan, no swing lane or no `targets[0]` → excluded
  and counted (Q011's measured funnel: 8 of 383 in the sealed part of this window, all on
  2026-06-02, and 0 cases of a lane present without an L3).
- Picks whose `outcome_target_invalid` is non-null, or whose **L3 is at or through `C_t`**
  (`dir × (L3 − C_t) ≤ 0`) → excluded and counted (measured: 4 and 2 respectively).
- Picks with fewer than 60 daily bars dated ≤ `t` (ATR / beta / runup undefined) → excluded, counted.
- **Lookback coverage:** picks for which any of the 5 prior sessions is missing from `uoa_symbol`, or
  carries fewer than **200** symbol rows that session (half the ~499/night baseline observed in the
  daily checks) → the persistence count is not measurable, pick excluded and counted. Session-level
  UOA row counts are printed by month.
- Picks with no session t+1 bar, or missing forward bars inside t+1..t+20 (halt, delisting) → a
  **measurement failure, not a classifier**: excluded and counted, never moved between arms. A night
  is dropped if > 25% of its picks are ungradeable.
- Nights whose session t+20 falls after the last trading date of the pinned price freeze (immature) →
  excluded and counted. Maturity comes from the **trading calendar**; right-censoring is never graded
  as a non-touch.

**Not excluded:** a pick whose L3 is at or through the **entry** `O_1` (`d_open ≤ 0`, a gap through
the target overnight) is **not a hit** (rule 5; DP-26) and stays in the denominator, with the identical
rule applied to every control against its own synthetic target from its own `O_1`. Excluding them would
filter the denominator on a session-t+1 price (rule 14) and would remove exactly the picks that gapped
to target — plausibly more of them in the PERSIST arm, which is the effect the printed share exists to
expose. The share is printed per arm, and a both-arms-removal sensitivity is printed and **never
decides**.

**Contributing nights (the floor units, DP-21):**
- **E1:** a night carrying **≥ 1 eligible PERSIST pick with ≥ 3 Pool-A controls** *and* **≥ 1 eligible
  NONE pick with ≥ 3 Pool-A controls**.
- **E2:** a night carrying **≥ 1 eligible PERSIST pick with ≥ 3 Pool-B controls**.
Each primary is gated on **its own** count; a shortfall on one is never covered by the other. A
matured night on which no row survives the funnel is **non-contributing, not an exclusion**: it is
never added to `exclusions_vNNN.json` and never counted toward any floor.

**Measured funnel, sealed window** (STEWARD_Q014_exposure.md §(c), counts only): 383 published,
in-window, non-excluded, matured picks → **369 eligible** — 8 with no lane plan / no L3 (all on
2026-06-02), 4 `outcome_target_invalid`, 2 wrong-side L3, and **0** lost to direction, missing `C_t`,
< 60 bars, a missing t+1 bar, a missing forward bar, or lookback coverage. **48 matured nights, 47 with
≥ 1 eligible pick** (2026-06-02 is the single zero-eligible night, the same one Q009 and Q011 lose).

**No arm is demoted; DP-43's demotion clause is discharged at lock and does not reopen.** PERSIST and
NONE are **jointly** E1's contributing-night unit, so at the 80-night floor both arms carry 80 nights
by construction and a thin arm can only show up as a *later decision date* — which is what happened
(measured NONE 8.4%, less than half the in-sample seed's assumed 18%; 25 of 47 nights carry zero
eligible NONE picks; E1's rate 0.4314/session against the drafted 0.65). E2's PERSIST arm contributes
on 46 of 47 nights. **`MID` is descriptive by design** (§3 B4), not by demotion. Sub-cells — bear, the
90+ band, regime, tape and the `prior_pub10 = 0` cell — stay under the standing rule (**< 20
contributing nights ⇒ SUPPRESSED, counts only, no point estimate**) on `eval.py`'s measured counts, and
**the window is never lengthened to rescue a stratum**: §5 sizes it on the two primary gates only. If
the `prior_pub10 = 0` cell is SUPPRESSED, §8 clause 7 makes E1 **INCONCLUSIVE**, which is the
conservative direction. **No demotion after lock, in either direction.**

## 3. Baseline(s) — what this must beat

- **B1 (E1's baseline; H-040's "selected with 0 UOA"):** published picks with `uoa5 = 0`, on the
  **same nights**, same lane, same level, same clock, each adjusted by its own Pool-A control. This is
  "Y's rate when X did not happen, in the same regime" in its cleanest form: same engine, same tape,
  same night, different prior flow.
- **B2 (E2's baseline; H-040's "3+ UOA not selected"):** same-night **unpublished** symbols with
  `uoa5 ≥ 3` in the same direction, distance-matched, carrying a synthetic target at the identical
  ATR distance (Pool B). Without this baseline a high touch rate among persistent picks would only be
  saying "persistent names move".
- **B3 (rule-5 distance-matched control, inside E1):** Pool A. A hit rate without it is descriptive
  (rule 5); it is what makes E1 a contrast of *excesses* rather than of raw rates, and it absorbs the
  volatility and momentum differences between the arms that would otherwise carry the result.
  **Pool A is deliberately not matched on `uoa5`** — matching on the variable under test would strip
  out the whole content of E1. **DP-12 does not fire here:** it governs conditioning variables that are
  themselves part of the forward price path (an overnight gap, a fast start), whereas `uoa5` is built
  entirely from sessions t−5..t−1 and is fixed at 16:05 ET on the pick night, before any post-decision
  bar exists. Pool B *is* matched on `uoa5 ≥ 3`, but by H-040's own design of the second baseline, not
  by DP-12 compulsion.
- **B4 (descriptive, never decides):** the `MID` (1–2 days) arm, for monotonicity; and the raw,
  control-unadjusted PERSIST − NONE difference, printed beside E1 so the size of the control
  adjustment is visible.

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Entry basis: the session t+1 official regular-session open `O_1`** (DP-03(b) — Haci's
option-spread entry), identically for picks, Pool-A controls and Pool-B controls, each from its **own**
t+1 open. **DP-11 does not fire:** nothing here is a position already held when the signal appears —
the persistence count is read at 16:05 ET on the pick night and the trade is opened afterwards. Pool-B
controls come from the UOA screener universe and have neither after-hours prices nor, in general,
hourly bars, and rule 5 requires **one** basis on both sides. The pick-night-close basis
(DP-03(a) / DP-11's `C_t` proxy) is reported as a descriptive sensitivity and **never decides**.

**Hit (the primary object).** From `O_1`, over sessions t+1..t+20 inclusive: `hit = 1` iff the
regular-session high (bullish) / low (bearish) of `prices_daily_split` reaches `L3`. **A target
already at or through the entry is not a hit** (rule 5; DP-26). Controls: the same rule against
`L3_c` from their own `O_1`, where `L3_c` is placed at the pick's **close-basis** ATR distance
`d_close,p` (§2.3) — the same ATR distance on both sides, per rule 5 and the locked Q006 §3 step 3
construction. **No stop is assumed** anywhere (rule 5; DP-02).

**Ordering rule (stated once, applied by `eval.py` with no judgment).** Where a session's bar
contains both `L3` and the counter-direction line used in a *secondary*, the pair counts
**counter-first** — the reading less favourable to the hypothesis (DP-27) — applied identically to
picks and controls. **Daily bars only; hourly bars are used by no endpoint**, because Pool-B symbols
have no hourly coverage and rule 5 requires one basis on both sides — a structural asymmetry that is
**disclosed, not patched**. The count of ambiguous sessions is printed separately, and **TIE is never
a third category in a printed share**.

**Primary endpoints (two; BH within the question — §7).** For pick `p` on night `t`, with
`c̄_A(p)` = the mean hit of `p`'s Pool-A controls and `c̄_B(p)` = the mean hit of its Pool-B controls:

- **E1 — does prior flow add to a pick.**
  `x_p = hit_p − c̄_A(p)`;
  `Δ1_t = mean_{p ∈ PERSIST_t} x_p − mean_{p ∈ NONE_t} x_p`;
  estimand **`m1 = mean_t Δ1_t`, in percentage points**.
- **E2 — does SAS add to prior flow.**
  `y_p = hit_p − c̄_B(p)` for `p ∈ PERSIST_t`;
  `Δ2_t = mean_{p ∈ PERSIST_t} y_p`;
  estimand **`m2 = mean_t Δ2_t`, in percentage points**.

**Secondary, descriptive, never decides:**

- the `MID` arm and the full `uoa5 = 0..5` profile; the raw (control-unadjusted) arm rates;
- E1 and E2 at **L1, L2, L4** on their own lane windows and at **L3 within 40 sessions** (DP-09), and
  the **touch-within-2 / 5 / 10-session** forms; **sessions-to-first-touch** (DP-44: no MPE, does not
  decide);
- the counter-direction race: `L3` before `O_1 − dir × 1.0 × ATR`, and swing counter-level touches
  within 20 sessions — **reported, never used as an exit** (DP-02);
- the **committed L1–L6 scale-out** (`BAND_EXITS`, volatilx `scripts/generate_sas_trading_guide.py:89-95`)
  run per arm, fractions exiting at each level's first touch from `O_1`, the remainder at the t+20
  close, truncated and labelled so;
- the gap-through share (`d_open ≤ 0`) per arm; arm composition on `beta60`, `atr_pct`, `runup20`,
  `dollar_volume_20d`, `overall_score`, `flow_strength_score`, sector where known, with post-match
  standardized mean differences for both pools;
- the **Pool-B sub-pool** restricted to same-night non-published *SAS candidates* ("SAS saw it and
  passed") beside the full Pool B;
- the pick-night-close entry basis (DP-03(a) proxy) for E1 and E2;
- **direction-adjusted close-to-close return at T+5 / T+20 by arm — fixed-horizon return is
  secondary and descriptive by rule 5 and never decides**, whatever H-040's line says.

**Quotability:** every number here rests on a 20- or 40-session basis → **NON_QUOTABLE** (rule 12).

**Inference.** Night-level. **CI (decides):** stationary block bootstrap over the ordered
contributing nights, expected block length **10 sessions** (20-session forward windows overlap across
adjacent nights; Q004/Q007/Q009/Q011 use the same), 2,000 resamples; the date-clustered bootstrap CI
is printed alongside. **p-value:** permutation, 10,000 draws, seed 20260913 — for E1, the arm label
(`PERSIST` / `NONE`) is permuted **within night** across eligible picks, which preserves the night
structure and the control adjustment; for E2, the published / Pool-B label is permuted within the
night's persistent set. Every estimate prints n(contributing nights), n(contributing nights dated
after the lock commit), n(eligible picks per arm), n(controls per pool), n(picks dropped for a thin
pool), n(gap-through), n(ambiguous sessions) and n(excluded, by reason).

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** and ≥ **20
  contributing nights per reported sub-cell**. The weaker "80 eligible with ≥ 20 contributing"
  reading is **not** used. A sub-cell below 20 nights is **SUPPRESSED** — counts only, no point
  estimate, not even "small n, directionally". **No floor is ever lowered to hit a date.**
- **Binding maturity: 20 sessions** (DP-09). The 40-session companions are descriptive and computed
  only where matured.
- **Expected n — measured, not projected.** The Steward's exposure report
  (`research/reports/STEWARD_Q014_exposure.md`, 2026-09-13, R1, **counts only — no touch, no return, no
  MAE, no picks-minus-control difference, no outcome of any kind**) measures this question's own
  population and arms on the sealed window, pick nights **2026-06-01..2026-08-12** (51 elapsed sessions):
  1. **Population funnel (measured, §2.4):** 383 published, in-window, non-excluded, matured picks →
     **369 eligible** on **47** of 48 matured nights; 0 picks lost to lookback coverage or forward
     maturity. UOA universe coverage is stable — 56 sessions, min 489 rows, **0** below §2.4's 200-row
     floor, median 1 symbol entering / 0 leaving per session.
  2. **Arm split (measured, on the §2.1 reconstruction):** **PERSIST 164 (44.4%) / MID 174 (47.2%) /
     NONE 31 (8.4%)**. This **contradicts the in-sample assumption** the draft planned on — EXPLORE_001
     §G's April–May read of **32% PERSIST / 18% NONE**, which was always labelled an assumption from
     nights this question excludes. PERSIST is thicker than assumed; **NONE is less than half as
     thick**, and NONE is what binds E1's per-night joint requirement (25 of 47 nights carry **zero**
     eligible NONE picks). That is why every date below moved out.
  3. **Contributing-night rates (measured, on §2.4's own per-endpoint definitions):** **E1 = 22 / 51 =
     0.4314** nights per session (against the drafted 0.65); **E2 = 46 / 51 = 0.9020** (against the
     drafted 0.88). **E1 binds**; E2 clears both of its own floors months earlier. Pool A and Pool B
     never bind below 3 neighbours anywhere in the window, so E1's count is gated purely by the joint
     PERSIST-and-NONE requirement.
- **Window, decision date, extension and DEFERRED fallback (DP-43; DP-13) — computed at `record` from
  the measured E1 rate on the NYSE session calendar. The drafted floor (window end 2026-11-30, decision
  Monday 2027-01-11, extension Monday 2027-02-22) is superseded and moved out by 12 weeks; a measured
  rate may push a drafted date out, never pull one in (DP-43, DP-45; Q011 item 8).**
  - **Primary window: pick nights 2026-06-01 .. 2027-02-25 inclusive**, after exclusions. Arithmetic:
    58 further E1-contributing nights are needed beyond the 22 measured; 58 / 0.4314 = 134.5 → **135
    sessions** (a fractional session rounds **up**); counting real NYSE sessions from 2026-08-13 — with
    Labor Day, Thanksgiving, Christmas, New Year, MLK and Presidents' Day shut — the 135th session, and
    so the projected 80th E1-contributing night, is **2027-02-25**. No shortening for an earlier date.
  - **Decision date: Monday 2027-04-05** (= 2027-02-25 + **20** sessions maturity, DP-09 = 2027-03-25;
    + one week of freeze margin = 2027-04-01; first Monday on or after). This is 5 calendar days later
    than the Steward's business-day projection of 2027-03-29, and the difference is deliberate: the
    exchange-calendar computation counts the six market holidays in that span and moves the date **out**.
    The Steward re-verifies it against the published 2027 exchange calendar when the successor freezes
    are built and reports any **later** date, never an earlier one. `eval.py` is written once (rule 9)
    and run **once**, then. **No interim looks.**
  - **Both gates, per primary endpoint, on `eval.py`'s measured counts at the decision pass — never on
    R1, never on the projection above, never on a run-rate:** ≥ **80** contributing nights (DP-21)
    **and** ≥ **30** contributing nights dated after this file's lock commit (DP-24). A shortfall on one
    endpoint is never covered by the other's count.
  - **One automatic extension (DP-13; DP-43's +30 sessions), no new question and no ask.** If either
    gate is short at 2027-04-05 on the measured counts, the window extends **once**, automatically, to
    pick nights **2026-06-01 .. 2027-04-09** (= 2027-02-25 + 30 NYSE sessions, Good Friday 2027-03-26
    shut); 2027-04-09 + 20 sessions = 2027-05-07, + one week = 2027-05-14, so the decision date is
    **Monday 2027-05-17**, run with the **byte-identical, unmodified `eval.py`** and the same gates.
  - **12-month ceiling: cleared.** 2027-04-05 is **5.4 months** inside DP-43's 2027-09-13 date, so Q014
    **locks** rather than going to `research/questions/DEFERRED.md`.
  - **DEFERRED fallback.** If a gate is still short after that single extension, Q014 goes to
    `research/questions/DEFERRED.md` with the measured counts rather than running under-powered. There
    is **no second extension**, no reduced gate, and a gate shortfall is **never** an INCONCLUSIVE
    verdict (§8).
  - **DP-24 is not binding and this is not HISTORICAL_ONLY.** 114 of the 135 projected sessions fall
    after the lock commit (21 elapse between 2026-08-13 and the 2026-09-13 lock), projecting ≈ 49 E1
    post-lock contributing nights against the 30 required; E1's post-lock floor alone would decide on
    2027-02-01 and E2's earlier still. **PROSPECTIVELY_CONFIRMED is reachable from this run by design**,
    **DP-31 does not apply**, and no successor replication question is drafted.
  - **Demotion at lock (DP-43): none, and the clause does not reopen** — see §2.4. Sub-cells stay under
    the standing < 20-contributing-night SUPPRESSED rule on measured counts; the **bear cell is expected
    SUPPRESSED** (H-062 measures 0.157 bear-carrying nights per session in this window), as are the 90+
    cell (DATA_NOTES: elite is thin and shrinking) and any regime cell below floor. The window is
    **not** lengthened to rescue a stratum.
- **Routed Steward requests (counts only; no outcome of any kind):**
  - **R1 (knowledge-time verification and exposure) — RETURNED AND CLOSED, 2026-09-13**,
    `research/reports/STEWARD_Q014_exposure.md`, all four parts, protocol observed. Part (a) was
    **blocking** and returned **VERIFIED single application** (§2.1), so branch (i) of the cascade
    governs and Q014 locks in its drafted form; parts (b)–(d) supply the measured arm split, the
    contributing-night counts and pool sizes above, and the UOA universe coverage. Nothing further is
    asked of the Steward for the lock.
  - **R2 (successor freezes, DP-23) — OPEN, never a blocker for the lock; due at the decision date
    Monday 2027-04-05.** Nights ≤ 2026-09-10 stay pinned to `manifest_v001` / `manifest_prices_v001`.
    Later nights enter only through `manifest_v002` (same SQL, same exclusion criterion) and
    `manifest_prices_v002` (same Alpaca queries), covering pick nights after 2026-09-10 through the
    registered window end **2027-02-25** (lookback begins 5 sessions before the window start,
    2026-05-22), with **(i)** `uoa_symbol` for every session from **5 sessions before the window start**
    through the window end, **including `oi_confirm_mult`, `oi_confirm_score`, `oi_confirm_ratio` and
    every `label_*` / `score_*` column** (the reconstruction and its audit need them; none is used as a
    feature); **(ii)** daily bars for **every candidate on every new night, published and unpublished**
    (Pool A); and **(iii)** daily bars for **every symbol appearing in `uoa_symbol` with a directional
    label and a reconstructed `score_b* ≥ 70`** anywhere in the window — **wider than DP-23's default
    candidate-symbol scope** (the UOA universe is ≈ 500 symbols) and **it must not be quietly narrowed**:
    this scope is what Pool B is made of and what closes the measured 71-of-502 price-coverage gap
    prospectively. Forward coverage 20 sessions beyond the last included pick night, 40 where the
    descriptive companion is computed. **Hourly bars are not required by any endpoint.** A second freeze
    pair is built **only if** the DP-13 extension fires, covering through **2027-04-09** and due Monday
    **2027-05-17**. Symbols without bars are dropped from their pool and **counted, never back-filled**;
    a materially truncated Pool B is a **Red Team flag, not a silent redefinition** (§10 threat 9).
    `eval.py` takes window start/end, manifest paths, exclusions path and output directory as arguments
    — no hard-coded dates, names or paths — so one byte-identical script serves both runs, and it
    records every sha256 and prints pre-lock and post-lock night counts separately.

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights ≥ 2026-06-01** through the §5 window end.
  *Why the April–May nights are not used:* EXPLORE_001 ran H-040's persistence construction on the
  in-sample split and reported the arm shares and the pooled matched-control excess into the backlog
  (§G: −0.09 / +0.05 / +0.13 by arm), so those nights are contaminated for this question and are not
  used, **not even as a descriptive panel**. The window also sits entirely after the 2026-06-01
  catalyst-layer fix (DP-06).
  *Contamination check on the sealed period (registrar; no results directory was read):* the desk's
  sealed-period descriptive outputs recorded in `research/BACKLOG.md` and in the weekly reports cover
  score bands, confidence labels, lanes, direction, entry basis and **source membership on the pick
  night** (single- vs multi-engine, weekly 2026-09-12 §§76-77, 175). **None conditions on prior-session
  UOA persistence**, and no desk output has read the 0 / 1–2 / 3+ contrast on nights ≥ 2026-06-01.
  The `≥ 70` cut, the direction-matched label and the 5-session lookback all come from the in-sample
  seed, not from the sealed period.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date; Half B = after. The split point is re-derived from the final window at the
  decision pass. `in_sample_end = 2026-05-29` marks only what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v003.json` `regime_label_point_in_time_from`). It is used only for nights ≥ 2026-06-09,
    only `regime_version = 'v1.2'`, and only where the row is a same-evening write; a later-posted row
    is treated as missing. Nights 2026-06-01..06-08 carry no legal label and are stratified by the SPY
    proxy only, flagged.
  - Primary tape stratum, trailing and legal at 16:05 ET: `tape_t` = sign of SPY's trailing 20-session
    return × tercile of SPY's trailing 20-session realized volatility, from SPY bars dated ≤ `t`.
    **Tercile cut points are expanding-window** (for night `t`, from every session 2026-03-02..t), so
    no later night sets an earlier night's stratum.
  - **Repeat-selection stratum (the Q003 confound, mandatory):** `prior_pub10` = the number of the
    prior 10 sessions on which the same symbol was published. Cells `prior_pub10 = 0` ("new pick") and
    `≥ 1`. A symbol UOA keeps flagging is very likely a symbol SAS keeps picking, and Q003 (H-052)
    already owns the continuation claim; this stratum is what separates the two. **It gates E1's
    verdict, it does not merely stratify it** — §8 clause 7.
  - Further cells, reported only at ≥ 20 contributing nights: bull / bear; score band
    < 80 / 80–85 / 85–90 / 90+; L3 ATR-distance tercile; `atr_pct` tercile.
- **Knowledge time (rule 14) — every input declared. Q014 requests no rule-14 exception and none is
  granted; DP-05 is untouched** (DP-41). DP-05(b)'s later classification clock is Q008's and does not
  travel here. §2.1's reconstruction is an inversion of a known mutation, so the reconstructed quantity
  *is* the 16:05 value; the Steward verified that inversion on the sealed window (VERIFIED single
  application) and `eval.py` re-runs the verification over the whole registered window inside the
  pre-outcome table, with §2.1's pre-committed cascade — three-bucket ⇒ `score_day` only ⇒ DEFERRED —
  firing automatically and deterministically if it ever fails.

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `dominant_direction`, `overall_score`, `completeness_score` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) | population, direction, band |
  | swing lane plan, **L3** (`targets[0]`) | `sas_candidates.public_payload_json` | written during the nightly run before `finished_at` | level |
  | `outcome_target_invalid` | `sas_candidates` | set at publication | exclusion audit only |
  | non-published candidate rows for night `t` | `sas_candidates` | pick night, 16:05 ET | Pool A, Pool B sub-pool |
  | `label_day/swing/long`, `score_day` | `uoa_symbol`, sessions `t−5..t−1` | 16:05 ET on each of those sessions, lag 0 (FREEZE_v001 §7) | persistence count |
  | `score_swing`, `score_long`, `oi_confirm_mult` | `uoa_symbol`, sessions `t−5..t−1` | overwritten next-morning by the OI confirm (`uoa_screener.py:2236-2239`) — **the 16:05 value is reconstructed by dividing out `oi_confirm_mult`** (§2.1) | persistence count |
  | `C_t`, ATR14, beta60, runup20, `atr_pct` | `prices_daily_split`, bars ≤ `t` | pick-night close, 16:00 ET | distances, matching |
  | SPY tape (trailing return / vol, expanding terciles) | `prices_daily_split`, SPY bars ≤ `t` | pick-night close | stratum |
  | `prior_pub10` | `sas_candidates`, nights `t−10..t−1` | those nights, 16:05 ET | stratum |
  | regime label (v1.2, nights ≥ 2026-06-09, same-evening rows) | `market_regime` | pick night, 16:05 ET | stratum |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion only |
  | session t+1 open; sessions t+1..t+20 (t+40 for companions) | `prices_daily_split` | after the pick night | **entry and outcome only** |

  **Banned inputs:** `uoa_symbol_daily.fwd_return_*` (the May–June freeze is not fixed and
  `fwd_return_30d_pct` relapsed to 0% for dates ≥ 2026-07-27 — FREEZE_v001 §5); `oi_confirm_score`,
  `oi_confirm_ratio`, `oi_confirmed_contracts` and every `oi_*` column as a **feature** (next-morning,
  and "next-morning" is optimistic for older rows — FREEZE_v001 §7); `sas_selection_excursion`,
  `outcome_*` and `level_hit_*` columns (calendar windows, close basis, recomputed weeks later —
  volatilx `services/sas_excursion.py:8-18`, `:336-354`); the platform's `atr_pct` and `spot_close`.
  **What `eval.py` must enforce:** the eligible-pick set, both control pools, `uoa5`, the arm labels
  and every stratum label are computed and written to a frozen per-pick table **before any session-t+1
  or later bar is loaded**; the run fails if any t+1-or-later field is referenced in eligibility,
  matching, arm assignment or stratification.

## 7. Multiple testing

- **Within the question: BH across m = 2** — E1 and E2 — at q ≤ 0.10; the verdict uses q. Every
  secondary prints raw p only, marked "descriptive, does not decide". **Both endpoints are primary and
  neither is dropped**: H-040 names both baselines, and E2 is the one test whose failure would stop a
  subscriber-facing claim (the persistently-flagged names SAS passed over doing just as well). Each is
  gated on **its own** ≥ 80 contributing nights and its own ≥ 30 post-lock nights (§5). The number of
  primaries is fixed here and falls on no branch.
- **Across the family: F5 Cross-engine interaction** (DP-29 — the primary endpoint's *subject* is
  whether a second engine's prior-session signal adds information to SAS selection, which is F5's
  definition; the endpoint is a path metric because rule 5 requires that of every question, and that
  does not move it to F4). F5 holds H-040 and H-041 (2 hypotheses). Registered F5 questions at
  registration: **Q014 only** — verified against every `**Family:**` header in `research/questions/`
  and against `research/BACKLOG.md` §F5 — contributing **2 primaries** to the family correction. The Reporter
  applies BH across all primary endpoints of registered-and-run F5 questions and prints both the
  within-question and the within-family q.
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q003 (F6, repeat selection):** persistence in UOA and re-selection by SAS are correlated by
    construction. The `prior_pub10` stratum (§6) is the discriminator, and the two questions' results
    are **never presented or counted as two confirmations**.
  - **Q006 (F1, control-cohort path):** shares the Pool-A construction, most nights and most picks;
    Q006 asks whether picks beat matched controls at all, Q014 asks whether prior flow *sorts* them.
    Cross-referenced, never duplicated.
  - **Q002 (F7, speed):** owns the touch-within-k-sessions claim; the speed forms here are descriptive.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1` and `m2` are in **percentage points** of L3-touch rate. **The MPE follows the estimator's shape,
one per endpoint, not one for both:**

- **E1 — MPE = 10.0 pp.** DP-20's 5.0 pp floor is **raised**, with the reason DP-20 requires: E1 is a
  *difference of differences across two arms with small per-night cells* (measured ≈ 3.5 PERSIST and
  ≈ 0.7 NONE eligible picks per night), the precise shape for which locked **Q007 §8** set 10.0 pp on
  the Q003 §8 precedent. The same estimator shape carries the same bar across questions.
- **E2 — MPE = 5.0 pp.** A single-arm control-adjusted touch-rate excess — exactly **DP-20**'s shape,
  so DP-20's 5.0 pp applies unchanged.

Both are two-sided: H-040 predicts positive values, and a negative result beyond that endpoint's MPE is
a confirmed finding with the opposite sign (it would say persistent prior flow marks *extension*, which
is a skip rule and equally actionable). **No money-unit MPE is invented anywhere, and the
sessions-to-first-touch forms carry no MPE and decide nothing** (DP-44).

Per endpoint, reading "MPE" as **that endpoint's own** number (E1 10.0 pp, E2 5.0 pp):

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. that endpoint's **contributing nights ≥ 80** and **≥ 30 contributing nights dated after the lock
     commit**, on `eval.py`'s measured counts, **and ≥ 20 contributing nights for any sub-cell that is
     reported** (DP-21) — a sub-cell below floor is **SUPPRESSED** (counts only) and does **not by
     itself** make the endpoint INCONCLUSIVE;
  2. `|m1| > 10.0 pp` for **E1**; `|m2| > 5.0 pp` for **E2**;
  3. block-bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 within the question (m = 2);
  5. the same sign in both calendar halves, with neither half beyond that endpoint's MPE in the
     opposite sign;
  6. no tape stratum with ≥ 20 contributing nights beyond that endpoint's MPE in the opposite sign;
  7. **(E1 only)** the effect is not confined to the repeat-selection stratum: the `prior_pub10 = 0`
     cell, where it clears 20 contributing nights, has the same sign as the pooled estimate and a point
     estimate of at least **half E1's MPE (5.0 pp)**. If that cell is SUPPRESSED for want of nights, the
     endpoint is **INCONCLUSIVE**, not CONFIRMED — an effect the desk cannot separate from Q003's known
     continuation finding licenses nothing.
- **NULL:** floors met **and** 95% CI includes 0 **and** `|m|` below that endpoint's MPE (10.0 pp for
  E1, 5.0 pp for E2). "A week of repeated unusual options flow before the pick tells you nothing about
  whether the pick reaches L3" is a real finding and is ledgered with the same care.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign; a tape stratum with ≥ 20 contributing
  nights beyond that endpoint's MPE in the opposite sign; `0 < |m| ≤ MPE` with the CI excluding 0
  ("real but below MPE", rule 6 — 10.0 pp for E1, 5.0 pp for E2); CI including 0 with `|m| ≥ MPE`; or
  clause 7 failing. **A gate shortfall is not INCONCLUSIVE:** it fires the single DP-13 extension, then
  DEFERRED (§5).
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5). It requires ≥ 30 contributing
  nights dated after this file's lock commit (DP-24), frozen in the successor manifests and never
  inspected earlier, reproducing the sign of the confirming endpoint under the unmodified `eval.py`.
  The 30 is never reduced. No subscriber-facing statement before that (rule 10); even then the basis
  is NON_QUOTABLE until restated on W60 (rule 12).
- **What the two endpoints license together, stated before the numbers exist:**
  - **E1 CONFIRMED, E2 CONFIRMED** — prior flow sorts picks *and* SAS selection beats the
    persistently-flagged names it passed over: the full §9 change, including a subscriber-facing claim
    once prospective.
  - **E1 CONFIRMED, E2 NULL** — persistence sorts SAS picks but the persistent names SAS skipped did
    just as well: an **internal ranking input only** (a scoring feature and a card badge), never a
    "UOA persistence list" product, because the selection layer added nothing on top of the flow.
  - **E1 NULL, E2 CONFIRMED** — SAS adds value among persistent names but persistence does not sort
    picks: nothing changes for persistence; the result is a Q006-adjacent statement about selection and
    is reported as such, not as a cross-engine finding.
  - **Both NULL** — no flow-persistence feature is built; the finding is ledgered and F5 effort moves
    to H-041.

## 9. If CONFIRMED, what changes on the platform

Today the platform has **no multi-day flow memory at all**. Every UOA consumer queries a single
`trading_date` (volatilx `services/candidate_universe_builder.py:38-48`,
`services/uoa_screener.py:397`, `:435`, `:1776`; `services/symbol_context_builder.py`), and the SAS
flow layer (weight 24) reads only that night's bucket scores and bulletin membership
(`services/super_agent_select_scoring.py:512-517`, `:613-617`, `:692`). "This name has been flagged
three days running" is information the engine cannot see. That is what makes H-040 worth registering
and what a CONFIRMED verdict would change.

Only where §8 licenses it, and only after PROSPECTIVELY_CONFIRMED for anything subscriber-facing
(rule 10):

- **A `flow_persistence_5d` input to the flow layer** — the §2.1 count, computed at 16:05 ET from the
  prior five sessions — as a cross-layer bonus alongside the existing membership bonus, with the size
  taken from the measured effect and not invented. **Shipped flag-off with a byte-identical checksum
  on the old scoring path, validated in shadow, flipped last** (rule 11); shadow ≥ 20 trading days.
- **A conviction-card and pick-card field** ("strong same-direction flow on N of the last 5
  sessions"), flag-off first, describing the pick rather than promising an outcome.
- **A Manual Trading Guide line** in the same terms as the verdict, printed with its measured excess,
  its control definition and the NON_QUOTABLE label until a W60 restatement exists (rule 12).
- **If E2 is CONFIRMED too:** a UOA Watch lane rule — persistently-flagged names are worth a look in
  their own right, with SAS selection as the sort — and only then a subscriber-facing claim.
- **If the effect is confined to the repeat-selection stratum** (§8 clause 7): **nothing changes**.
  The finding belongs to Q003 and is reported there, not sold twice.
- **All NULL:** no feature, no card field, no guide line; the null is ledgered with the same care and
  F5 moves to H-041.
- Owner: implementer, via an `IMPLEMENTATION_BRIEF.md` Haci runs in the platform repo.

## 10. Known threats to validity (registrar's own list)

1. **The conditioning column is silently rewritten after the fact.** `score_swing` and `score_long`
   are multiplied in place by the next-morning OI-confirmation run (`uoa_screener.py:2236-2239`), and
   the bulletin's own lists are re-ranked with the mutated scores (`:2245-2303`); FREEZE_v001 §7 warns
   the OI lag is "next-morning" only optimistically for older rows. Taking the frozen values at face
   value would put post-16:05 information into a feature. §2.1's reconstruction removes it exactly,
   *provided* `oi_confirm_mult` was applied once per row — and the Steward **verified exactly that** on
   the full sealed population (`STEWARD_Q014_exposure.md` §(a), **VERIFIED single application**: 0 of
   1,190 multipliers outside {0.90, 1.00, 1.05, 1.10}; 0 "ran but null" rows in any month; 0 of 13,646
   `score_day` and 0 of 25,984 reconstructed `score_swing*` / `score_long*` label inconsistencies; 3 of
   369 arm assignments moved). **Branch (i) of §2.1's cascade governs**, and the cascade stays live for
   the post-lock nights the verification could not see: `eval.py` re-runs checks (i) and (ii) per month
   over the whole registered window inside the pre-outcome table, and any failure switches the
   definition automatically to `score_day` only (or, if that fails too, to DEFERRED). `eval.py` also
   prints how many rows carry a non-null multiplier, how many arm assignments the reconstruction
   changes, the ±0.5 rounding band at the 70 cut, and the whole conditioning variable rebuilt on
   `score_day` alone as this threat's named sensitivity. **Residual limitation, disclosed and not
   resolved:** `uoa_screener.py:1996-2024` guards its own re-execution unless a force flag is passed,
   and the frozen data carries **no OI-confirm run-history table** (the same absence as PI-004 /
   PI-012's `super_agent_select_runs`), so a **forced** manual re-run cannot be positively excluded from
   the data alone; nothing in the data shows one, and a second application would have had to produce a
   compound multiplier outside the four documented values (0 observed) *and* leave all 25,984
   reconstructed label/score pairs consistent. The `updated_at − created_at` gap (median 143.3h with a
   multiplier vs 120.5h without) is **not usable as a signature** — `updated_at` is bumped by other
   backfills — and is cited neither for nor against. The underlying platform defect is filed as
   **`PI-013`** (med, OPEN — "`uoa_symbol_daily.score_swing` / `score_long` overwritten in place by the
   next-morning OI-confirmation pass; no point-in-time copy"); **Q014 does not depend on it being
   fixed** and no brief follows from this question.
2. **Persistence is correlated with re-selection** (Q003 / H-052), which is the strongest selection
   pattern the Explorer found. Without the `prior_pub10` stratum this question could simply
   re-discover it. §6 stratifies, §8 clause 7 gates, §9 refuses to change anything if the effect lives
   only there.
3. **Persistence is also a big-liquid-name effect.** Names with heavy, repeated option premium are
   larger, more liquid and more heavily traded than the median candidate. Pool A matches on
   `beta60` / `atr_pct` / `runup20` only; `dollar_volume_20d` and the post-match standardized mean
   differences are printed for both pools so the residual imbalance is visible, and Pool B is drawn
   from the same UOA universe, which largely removes the liquidity gap for E2.
4. **Three matching features may not span selection** (Q006 threat 1). E1 is a *difference* of
   control-adjusted excesses, so a matching bias common to both arms cancels; a bias that differs
   between arms does not, and that is what the composition table is for.
5. **The `≥ 70` cut and the 5-session lookback are conventions, not findings** (DP-26). They come from
   the in-sample seed; the `uoa5 = 0..5` profile is printed so the reader can see whether the bins are
   doing the work, and a different cut is a new PREREG, not a re-run.
6. **Ladder levels are not ATR-scaled** (`ai_agents/principal_agent.py:530-575`), so L3's distance in
   ATR varies widely and part of any touch-rate difference is distance. The controls carry the
   identical ATR distance by construction, and the L3 ATR-distance tercile cell is reported.
7. **One tape.** The window is Jun 2026 – Feb 2027 (Apr 2027 if the extension fires). A sign that appears in only one calendar half
   fails §8 clause 5, and nothing here speaks to the strong April–May tape.
8. **Overlapping 20-session windows** inflate precision; the block length is fixed here (10 sessions)
   and not chosen after seeing results.
9. **Pool B depends on a wider price freeze** (§5 R2(iii)). If it is not built, Pool B collapses to
   non-published SAS candidates and E2 becomes a narrower question than H-040 asked; `eval.py` prints
   the pool composition and the count dropped for want of bars, and a materially truncated pool is a
   Red Team flag, not a silent redefinition. **Measured: this threat did not fire in the sealed
   window** — Pool B is min 21 / median 56 / max 93 per PERSIST pick, 0 of 164 below the 3-neighbour
   minimum, contributing on 46 of 47 nights — but the coverage gap is real and counted: **71 of 502**
   UOA symbols (14.1%) have no daily bars in `manifest_prices_v001`, costing **56 qualifying-but-dropped
   instances** (mean 0.34, max 2 per pick). **R2(iii)'s widened symbol scope is what keeps this threat
   from firing after the lock and must not be narrowed.**
10. **The UOA universe itself changes.** The screener's ~500-name universe is re-resolved nightly
    (`uoa_screener.py:964`); a symbol can leave the universe and score zero strong days for reasons
    unrelated to flow. Per-session row counts and universe turnover are printed.
11. **Bear picks are too rare to carry their own cell** (H-062: 0.157 bear-carrying nights per session
    in this window). The bear cell is expected SUPPRESSED; the direction-matched label definition
    still applies to the few that appear, and no bear-specific claim follows.
12. **Null-ladder and wrong-side-L3 denominators** are excluded and counted; the question speaks only
    for published picks carrying a swing L3 on the correct side of the pick-night close.
13. **The stock path is a proxy for the spread.** Every endpoint is an equity path; the desk holds no
    option prices (`research/questions/DEFERRED.md`; ENHANCEMENTS.md EN-011). Any §9 line about
    spreads must say so.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: **R2 only** — the successor selection
and price freezes (DP-23, with the widened ≈ 500-symbol Pool-B scope), due at the decision date Monday
2027-04-05, covering pick nights through the registered window end 2027-02-25; a second pair only if
the DP-13 extension fires (through 2027-04-09, due Monday 2027-05-17). **R2 does not block the lock.**
**R1 has returned and is closed** (`research/reports/STEWARD_Q014_exposure.md`, 2026-09-13, all four
parts, counts only): its blocking part (a) returned **VERIFIED single application**, so §2.1's cascade
branch (i) governs, and parts (b)–(d) supply §5's measured arm split, contributing-night rates and pool
sizes. Two items were **DEFAULTED on Haci's behalf** under DP-43 and are listed on the board: E2's
status as a second primary rather than a descriptive baseline (item 4), and the window / decision date
/ single extension on the pooled measured E1 rate (item 5, arithmetic settled at `record`). Overturning
a default means a successor question, never an edit to this file.
