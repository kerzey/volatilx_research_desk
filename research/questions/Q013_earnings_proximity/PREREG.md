# Q013 — earnings_proximity: does a pick whose earnings report lands within three sessions run a worse path than a pick whose report is further out?

**Status:** REGISTERED — locked by committing this file. Every pre-lock decision is recorded in
`DECISIONS.md` (2026-09-13); no item is open.
**Decisions:** DECISIONS.md
**Family:** F4 Price behaviour after selection (hypothesis H-064)
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`, `uncorroborated_publication_runs.trading_dates`) — the newest exclusions file (DP-22); `eval.py` reads the JSON, no hard-coded dates. See §2.
**Measured exposure (`research/reports/STEWARD_Q013_exposure.md`, R1, counts only, 2026-09-13):**
48 matured non-excluded pick nights 2026-06-01..2026-08-12; 383 published → **371 eligible**;
**arm A 44 / arm B 137 / arm C 190**; **23 contributing nights of 48**; B2 matching never binds
(0 of 181 arm-A/B picks below the 3-control floor — every pick matched its full 10); blended
contributing-night rate **0.4510 per session**. **R1(a) PASSED** — the arm-label columns are
live-path 16:05 ET writes, so no rule-14 exception is needed and DP-41's DEFERRED branch does not
fire. **R1(b)** projects both floors inside DP-43's 12-month ceiling, so Q013 is locked, not
deferred. Full funnel and per-cell counts in §5.
**Registered by:** registrar · **Approved by:** desk (DP-46, autonomous run) · **Date:** 2026-09-13

---

## 1. Hypothesis (plain English)

**A SAS pick whose company reports earnings within the next three sessions gives you a worse trade
than a pick from the same night whose report is four to twenty sessions away: it reaches its swing
target L3 less often within twenty sessions of the next open, and it drops further against you
along the way — enough to justify skipping those picks and never holding a spread across the
print.**

BACKLOG H-064 reads: *"Earnings within 0–3 sessions after the pick: deeper drawdown from the open
and a lower L3 touch rate than picks whose report is 4–20 sessions out → skip rule, and no spreads
held across the print — baseline: picks with the next report 4–20 sessions out."* It names the two
arms, the two endpoints, the baseline and the entry ("from the open"), but no entry convention, no
window, no control, no treatment of the picks with no report in sight, and no decision numbers.
This PREREG fixes all of them (§2–§4, §8).

The expected sign is "arm A worse". **Both tests are two-sided**: "picks run *up* into the print"
is an equally tradeable answer and would license the opposite rule, so the verdict carries its
sign.

**What this question is not.** It is not an options question. The stated mechanism — binary event
risk *plus IV crush* — is half about the option structure, and the desk holds no option price
history (research/questions/DEFERRED.md; ENHANCEMENTS.md EN-011). Everything here is the **equity
path**. Nothing in §9 may be written about spread P&L on the strength of this question; the "no
spread across the print" half is supported only insofar as the underlying's path is worse, which is
what §4's Plan X reports descriptively.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are aggregated within a night before
  anything is estimated; every estimator is a within-night difference, so the night's tape is held
  fixed.
- **Source tables (manifest_v001 and its successor), `sas_candidates`:** `qualified`,
  `selected_rank`, `qualification_reason`, `overall_score`, `dominant_direction`, `best_timeframe`,
  `public_payload_json` (lane plans), and the point-in-time earnings fields
  **`days_to_earnings_corrected`**, `days_since_earnings_corrected`, `earnings_phase`,
  `earnings_phase_subtag`, `earnings_event_risk_corrected` (knowledge time in §6.1). `sas_runs`
  (`finished_at`) is used only for the exclusion criterion.
- **Source tables (manifest_prices_v001 and its successor):** `prices_daily_split` (t+1 open,
  forward highs/lows/closes, pick-night close for ATR/beta/run-up, SPY tape, trading calendar) and
  `prices_daily_raw` (split-factor snapping only). `prices_hourly_raw` is used only for the
  descriptive same-session tie-break; it covers published symbols only
  (research/lib/freeze_prices.py:17, :117).
- **Treatment rows (published picks), exact predicate:**
  `qualified IS TRUE AND selected_rank IS NOT NULL` (**DP-28**) — the platform's own exposure
  predicate (volatilx `services/sas_conviction_card.py:105`, `:308-309`). Dark-lane rows
  (`selected_rank` set with `qualified = FALSE`, `qualification_reason = 'selected_dark'`;
  volatilx `services/super_agent_select_scoring.py:1503-1546`) are **not** treatment rows; they are
  counted and they stay in the control pool.
- **Control pool, night t:** the complement of the publication predicate — every same-night
  `sas_candidates` row for which `NOT (qualified IS TRUE AND selected_rank IS NOT NULL)`, dark-lane
  rows included (DP-28; rule 5's "unpublished candidates from the same night"). Each pool row needs
  ≥ 60 prior split-adjusted bars (beta60), ≥ 21 bars (runup20), a t+1 open, and ≥ 20 forward
  sessions in the pinned freeze.
- **Level, exact:** **L3 = `public_payload_json.lane_plans.swing_trading.targets[0]`** — the swing
  lane's first target, the level H-064 names (volatilx `services/sas_conviction_card.py:182-187`).
  **Clock: 20 sessions from entry (DP-09)**; the platform's own 40-session swing window is reported
  alongside, descriptively, wherever it has matured. L1, L2 and L4 are reported descriptively only.
- **Notation** (all prices in the signal-date split basis):
  - `dir` = +1 (bullish `dominant_direction`) / −1 (bearish).
  - `C_t` = the pick's actual regular-session close on night t from `prices_daily_split` (never the
    platform's `spot_close`, stale on re-run nights — DATA_NOTES). Used for ATR, beta60, runup20 and
    matching, **not** as the entry.
  - `ATR_p` = mean of the last 14 true ranges ending at t, from `prices_daily_split`;
    `atr_pct_p = ATR_p / C_t`. The platform's `atr_pct` is corrupted around splits and is never used
    (PI-003; DATA_NOTES).
  - Sessions `s = 1, 2, …` are trading sessions after t, from SPY bars. `O_s`, `H_s`, `L_s`, `Cl_s`
    are that session's official regular-session open, high, low, close.
  - **Entry `E_p = O_1`** (§4). `d_open = dir × (L3 − O_1) / ATR_p`.
- **Arm assignment (the conditioning variable, fixed at 16:05 ET on the pick night; §6.1):**
  - `dtn_p` = `days_to_earnings_corrected` on the pick's own row — calendar days to the next
    scheduled report at or after `trading_date`, stamped at scoring time by the live path
    (volatilx `services/super_agent_select_service.py:396-402`,
    `services/super_agent_select_scoring.py:1436-1444`, `services/earnings_phase.py`).
  - Scheduled report date `ED_p = trading_date + dtn_p` calendar days. **`k_p` = the number of
    trading sessions from t to the first session on or after `ED_p`** (SPY calendar). `k = 0` means
    the report is dated on the pick night itself; `k = 1` means the next session.
  - **Arm A (treatment): `0 ≤ k_p ≤ 3`.** **Arm B (baseline): `4 ≤ k_p ≤ 20`.**
    **Arm C: `k_p > 20`, or `dtn_p` null / `earnings_phase = NO_WINDOW` with no resolvable next
    date.** Arm C is **excluded from the primaries, counted, and reported descriptively** (§3 B4;
    DECISIONS.md item 1: the primaries stay the A-vs-B contrast H-064 writes, and adding an A-vs-C
    primary would be a re-specification, not an application — DP-25). The arms are exactly the ones
    H-064 names, in the units it names (DP-25). Measured on the sealed window: **arm A 44 / arm B
    137 / arm C 190 eligible picks**, `dtn` non-null on all 371, so no row entered arm C for the
    null/unresolvable reason.
  - `k = 0` stays in arm A even though the print may already have happened before the pick-night
    close (the desk holds no before-open / after-close flag, §10 threat 4). That is the hypothesis
    as written (DP-25) and it is the dilutive direction — it puts picks with no forward event risk
    into the treatment arm and makes arm A look more like arm B (DP-45). The per-`k` cells
    (k = 0, 1, 2, 3) are printed.
- **Exclusions (each counted and printed in the results header, never silently dropped):**
  - Nights in **`research/data/exclusions_v003.json`** — `manual_runs.trading_dates` ∪
    `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates` (DP-22).
    `eval.py` reads the JSON; **no date is hard-coded here or in `eval.py`.** Inside a window
    starting 2026-06-01 that removes 2026-06-26, 2026-07-02 and 2026-07-06 on the frozen part; the
    printed figure is the one `eval.py` derives.
  - Any prospective night whose `finished_at` is later than the next session's open (DP-04), applied
    mechanically.
  - Dark-lane rows, from the treatment set only.
  - **Null-ladder picks:** no `lane_plans`, or no swing lane, or no `targets[0]` (FREEZE_v001 §3:
    17 of 915 selected rows have no ladder row at all; PI-006). Excluded and counted.
  - Picks with `outcome_target_invalid` non-null. Excluded and counted.
  - Mixed-direction picks (`dominant_direction` neither bullish nor bearish). Excluded and counted.
  - Missing `O_1`, missing `C_t`, or fewer than 14 prior bars for ATR. Excluded and counted. A night
    is dropped if more than 25% of its eligible picks are missing bars.
  - **Immature:** fewer than 20 forward sessions in the pinned freeze. Excluded and counted.
    Right-censoring is never graded as a non-touch.
  - **Arm C** (above) and picks with **fewer than 3 valid matched controls** (§3 B2). Excluded from
    the primaries and counted; the drop count is a headline number (§10 threat 2).
  - **Not excluded:** `d_open ≤ 0`. A pick whose L3 is already at or through the t+1 open is scored
    `passed_at_entry` and counted as a **non-hit** on the touch endpoint (rule 5; **DP-26**; the
    Q002/Q003/Q006 convention), stays in the denominator, and its MAE is still measured from `O_1`.
    The `passed_at_entry` share is printed **per arm** and both bounding sensitivities are reported
    (§4, §10 threat 3).
- **Contributing night (the unit that counts toward the floors, DP-21):** a non-excluded, matured
  night carrying **≥ 1 eligible arm-A pick and ≥ 1 eligible arm-B pick**, each with ≥ 3 valid
  matched controls. The same definition serves both primary endpoints, so there is one floor and one
  gate. A night carrying only one arm contributes nothing, is counted, and is reported.
  **Arms A and B are therefore jointly the unit and are not separately demotable** (DECISIONS.md
  item 16): a thin arm A shows up as *fewer contributing nights* and is handled by the §5 date
  machinery — single extension, then DEFERRED — never by demoting an arm the estimator cannot do
  without. **DP-43's demotion clause is discharged at lock: nothing in this question is demoted**,
  in either direction, and no demotion happens after lock.
  Measured on the sealed window: **23 contributing nights of 48**.

## 3. Baseline(s) — what this must beat

- **B1 — the backlog baseline, "Y's rate when X did not happen, in the same regime":** **arm-B picks
  from the same night** (report 4–20 sessions out), entered on the same basis, graded identically,
  in the same tape. Every primary is a within-night A-minus-B contrast, so B1 is inside the
  estimator rather than beside it.
- **B2 — the rule-5 distance-matched control (inside both primaries).** For each eligible pick p on
  night t:
  1. Compute `beta60`, `atr_pct`, `runup20` at `C_t` from `prices_daily_split` bars dated ≤ t.
     Standardize by the night's cross-sectional median/MAD over the control pool plus that night's
     picks. Take the **10 nearest** control-pool rows by Euclidean distance, with replacement across
     picks, ties broken by symbol ascending. Matching uses only inputs available at 16:05 ET on the
     pick night. A matched control later found to lack forward bars is **dropped and counted**, never
     replaced by the next-nearest candidate.
  2. Synthetic target for control c: `L3_c = O_{1,c} × (1 + dir_p × d_open_p × atr_pct_c)` — the same
     ATR distance in the same direction, anchored at the control's **own** t+1 open, i.e. the same
     entry basis as the pick, which is what makes the contrast legal under rule 5.
  3. The control is graded with **exactly** the pick's rule: same entry, same 20-session window, same
     "already passed at entry is not a hit" convention, same MAE definition, regular-session daily
     highs (bullish) / lows (bearish), split factors snapped.
  4. A pick with fewer than **3** valid controls is dropped from the primaries and counted.
  5. Control rows never add to inferential n (rule 6).
  **The control pool is not restricted by earnings arm** (DECISIONS.md items 2 and 9): B2's job here
  is to strip out the composition difference between the arms — arm-A names may be more volatile,
  more bearish, or carry differently-placed ladders — not to strip out the earnings event itself,
  which is the thing being tested. **DP-12 does not fire.** DP-12 governs conditioning variables
  that are themselves part of the price path (an overnight gap, a fast start — a move already
  completed when the signal is read). Q013's arm label is a **scheduled calendar event known in full
  at 16:05 ET on the pick night**, fixed before any post-decision bar exists, so nothing requires the
  control to be matched on it, and matching on it would strip out the event under test. The
  unrestricted B2 pool is therefore the primary control by decision, and B3 below is descriptive by
  choice rather than by DP-12 compulsion.
  Measured on the sealed window: the B2 gate **never binds** — every one of the 181 arm-A/B eligible
  picks matched its full 10 nearest controls (0 of 181, 0.0%, below the 3-control floor), per-night
  eligible control pool min 37 / median 54 / max 60.
- **B3 — earnings-arm-matched control (descriptive, never decides).** The same construction with the
  pool restricted to same-night control-pool rows in the **same arm** as the pick (their own
  `days_to_earnings_corrected`, same `k` band). This is the "is it SAS, or is it every stock with a
  print in three days?" panel. It is descriptive because the restricted pool cannot be relied on to
  reach the floor (§5) — and because the skip rule H-064 proposes is a rule about *picks*, not a
  claim about SAS's fault. Measured on the sealed window, B3 is confirmed too thin to carry a
  primary: available same-arm control rows per pick average **8.2 (arm A)** and **26.9 (arm B)**, and
  **24 of 181 picks (13.3%) would carry fewer than 3 valid controls** (arm A 12 of 44 = 27.3%; arm B
  12 of 137 = 8.8%) — against 0.0% under B2 (§10 threat 14).
- **B4 — arm C (descriptive):** picks with no scheduled report within 20 sessions, same night, same
  grading. The "clean" comparison, reported beside B1 so a reader can see whether arm B is itself
  contaminated by event risk.

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Entry basis: the next session's official regular-session open `O_1`** (DP-03(b)), identically for
picks and controls. This is the basis H-064 itself names ("drawdown from the open", DP-25) and it is
the basis on which the decision it proposes is taken — the pick is read at 16:05 ET, the spread is
opened the next morning, and the skip rule fires before that. **DP-11 does not apply**: nothing here
is a position already held when the signal appears; the signal (a scheduled report date) is known
before entry. A level at or through `O_1` is **not a hit** (rule 5; DP-26) and is scored
`passed_at_entry` (§2). **Stops are not assumed anywhere** (DP-02): adverse excursion and
counter-direction touches are measured and reported, never used as exits.

**Per-pick quantities, 20 sessions from entry (DP-09):**

- `Y_p` = 1 if L3 is first touched in sessions 1..20 (`H_s ≥ L3` bullish / `L_s ≤ L3` bearish), else
  0. `passed_at_entry` → `Y_p = 0`.
- `MAE_p` = `max(0, max_{s ≤ 20} dir_p × (O_1 − L_s) / ATR_p)` for bullish, with `H_s` and the sign
  reversed for bearish — the deepest adverse excursion from the entry, in ATR, as a positive depth.
  Measured over all 20 sessions whether or not L3 was touched (no survivor conditioning).
- `x_p = Y_p − mean_{c ∈ B2(p)}(Y_c)` (percentage points) and
  `m_p = MAE_p − mean_{c ∈ B2(p)}(MAE_c)` (ATR) — the control-adjusted forms.

**Primary endpoints (two, pre-specified, BH-corrected within this question):**

- **P1 — the touch rate (H-064's "lower L3 touch rate").** Per contributing night t:
  `Δ1_t = mean_{p ∈ A,t}(x_p) − mean_{p ∈ B,t}(x_p)`. Estimand `P1 = mean_t Δ1_t`, in percentage
  points. Predicted sign: negative.
- **P2 — the drawdown (H-064's "deeper drawdown from the open").** Per contributing night t:
  `Δ2_t = mean_{p ∈ A,t}(m_p) − mean_{p ∈ B,t}(m_p)`. Estimand `P2 = mean_t Δ2_t`, in ATR.
  Predicted sign: positive (arm A deeper).

**Secondary, descriptive, never decides:**

- The **raw (unadjusted) arm contrasts**: the same two estimands with `Y_p` and `MAE_p` in place of
  `x_p` and `m_p`. These are what a trader sees before any control is applied; they are printed
  first in the results table and they decide nothing.
- **B3 (earnings-arm-matched) and B4 (arm C)** versions of both estimands.
- **`passed_at_entry` bounds:** the share per arm, plus both bounding sensitivities — (i) the
  primaries recomputed with `passed_at_entry` picks removed from both arms, and (ii) the primaries
  recomputed scoring `passed_at_entry` as a *favourable* outcome (`Y_p = 1`). The registered rule is
  neither of these; they bracket it (§10 threat 3).
- **Per-`k` cells:** `k = 0 / 1 / 2 / 3` inside arm A and `k = 4–7 / 8–13 / 14–20` inside arm B, each
  printed with its n and SUPPRESSED below 20 contributing nights. The dose-response shape is the most
  informative descriptive output of this question.
- **Plan X — "no position across the print" (the execution half of H-064), reported next to the hit
  rates (rule 5).** Enter at `O_1`; exit at the **first** of: the first touch of L3 (at the L3 price,
  or the session's open if it opens through L3), or the close of the **last session strictly before
  session `k`** (the report session); if neither applies by session 20, exit at `Cl_20`. Result
  `r^X_p = dir × (exit − O_1) / ATR_p`. Reported per arm beside **Plan H** (the same trade held to
  the first L3 touch or `Cl_20`, no earnings exit). There is no stop in either plan.
- **The committed scale-out plan, per arm (rule 5):** `BAND_EXITS` (volatilx
  `scripts/generate_sas_trading_guide.py:89-95`), entered at `O_1`, each fraction exiting at its
  level's first touch (or the better open on a gap through), fractions whose level was at or through
  `O_1` recorded as unfillable, remainder closed at `Cl_20` (truncated and labelled), trailing rules
  ignored, `< 80` not traded. Reported in ATR and percent.
- **Counter-direction path:** the share of picks touching the printed swing-lane `stop` before L3,
  and touching `O_1 − dir × 1.0 × ATR_p` before L3, per arm. Counter levels use the swing lane's
  `stop` (volatilx `services/sas_excursion.py:301-332`), and `sas_excursion.counter_levels_json`
  prices where present (`:269-287`, `computation_version = 'v2'`) — **prices only, never its touch
  dates**, which are on calendar windows. Touches are recomputed from the price freeze. A
  same-session tie is broken with hourly bars for picks; **any tie hourly bars cannot order, and
  every control tie (controls have no hourly bars), counts counter-level-first (DP-27)**, with the
  TIE count printed separately. TIE is never a third category in a printed share.
- **Other levels and the platform's clock:** L1, L2, L4 within their own lane windows, and L3 within
  **40** sessions (the platform's swing window, DP-09's descriptive companion), where matured.
- The platform's close basis (`entry_ref`, volatilx `services/sas_excursion.py:336-354`) version of
  the raw arm contrast, for comparison with anything the platform displays.
- Close-to-close return from `O_1` at T+10 and T+20, direction-adjusted (secondary by rule 5).
- **Composition panel:** per arm, the distribution of `d_open`, `atr_pct`, `beta60`, `runup20`,
  `overall_score`, direction, `best_timeframe`, and the share of picks carrying the platform's own
  `earnings_event_risk_corrected` flag and the projection horizon-guard tags
  `[EARNINGS EVENT IN WINDOW]` / `[EARNINGS RUN-UP]` (volatilx `services/catalyst_scoring.py:71-80`).

**Quotability:** a 20-session basis → **every number here is NON_QUOTABLE** (rule 12).

**Inference.** All at night level.
- **CI (decides):** stationary block bootstrap over the ordered contributing nights, expected block
  length **20 sessions** (20-session forward windows overlap across adjacent nights), 2,000
  resamples, seed 20260913. The date-clustered bootstrap CI is printed alongside.
- **p-values:** within-night arm-label permutation — on each contributing night the A/B labels are
  shuffled among that night's eligible A+B picks and the estimand is recomputed exactly; 10,000
  permutations, seed 20260913. The control set travels with the pick, not with the label.
- Every estimate prints n(contributing nights), n(arm A picks), n(arm B picks), n(arm C),
  n(control rows), n(picks dropped for < 3 controls), n(`passed_at_entry`) per arm, and
  n(excluded, by reason).

## 5. Sample floors, expected n, window and decision date

- **Floors (rule 6 read per DP-21):**
  - ≥ **80 contributing nights per primary endpoint** (§2 definition; both primaries share it). The
    weaker "80 eligible nights with ≥ 20 contributing" reading is not used.
  - ≥ **20 contributing nights** per reported sub-cell; cells below 20 are **SUPPRESSED** — no point
    estimate printed.
  - ≥ **30 contributing nights dated after this file's lock commit** (DP-24) for
    PROSPECTIVELY_CONFIRMED. **Measured against R1(b)'s rate (0.4510 contributing nights/session),
    30 post-lock contributing nights project to 2027-01-25** — comfortably before the 2027-03-22
    decision date, so the post-lock clause is **not** the binding gate (the 80-night floor is) and
    the window end did not have to move for it. **DP-31 therefore does not apply and Q013 is not
    `HISTORICAL_ONLY`**: PROSPECTIVELY_CONFIRMED is reachable from this run by design and no
    successor replication question is drafted. DP-24's 30 is never reduced and DP-31 is never
    invoked to rescue a short window here, because the hypothesis is not about the sealed period.
    The gate itself fires on `eval.py`'s **measured** post-lock count at the decision pass, never on
    this projection.
  - **No floor is ever lowered to reach a date** (DP-21, DP-43).
- **Measured exposure (R1, `research/reports/STEWARD_Q013_exposure.md`, 2026-09-13, counts only —
  no touch, no return, no MAE, no picks-minus-control difference was computed or read).** Pick
  nights 2026-06-01..2026-08-12 (the last night with a matured 20-session forward window),
  **48 matured non-excluded nights** of 51 in the raw window:
  - **Funnel:** 383 published (DP-28) → 375 (−8 with no swing lane at all) → 371 (−4
    `outcome_target_invalid`) → **371 eligible**; 0 removed for mixed direction, 0 for missing `C_t`
    or `O_1` or < 14 ATR bars, 0 immature.
  - **Arms:** **A 44 / B 137 / C 190** eligible picks; `days_to_earnings_corrected` non-null on all
    371.
  - **Contributing nights: 23 of 48.** One matured night (2026-06-02) carries zero eligible picks —
    all 8 published rows lack a swing lane, the same cause Q011's exposure report records.
  - **Per-`k` nights:** arm A 11 / 10 / 8 / 8 for `k = 0 / 1 / 2 / 3`; arm B 23 / 20 / 27 for
    `k = 4–7 / 8–13 / 14–20`. All three arm-B bands already clear the 20-contributing-night floor
    inside the sealed window; the four arm-A cells project past 20 at their own measured per-cell
    rates by **2026-11-16 / 2026-11-30 / 2027-01-11 / 2027-01-11** — every one before the decision
    date, so **no cell is demoted at lock** (DECISIONS.md item 16).
  - **B2 control sets:** every one of the 181 arm-A/B picks matched its full 10 controls; **0.0%**
    below the 3-control floor; per-night eligible control pool min 37 / median 54 / max 60. **B3**
    (arm-matched, descriptive) is thin by contrast: 13.3% of picks below 3 controls (A 27.3%,
    B 8.8%).
  - **Monthly contributing rate:** 10.0% (June) → 70.0% (July) → 87.5% (August, partial); **blended
    0.4510 contributing nights per session**. The seasonality is real, which is why the rate is
    *measured* rather than assumed (see the decision-date bullet).
  - **Composition diagnostics as counts** (§10 threats 2–3): bear share **A 4.5% vs B 2.9%**, gap
    1.6 pp (the 20 pp trigger is **not** tripped); `passed_at_entry` **A 4.5% vs B 0.7%**, gap
    3.8 pp (the 10 pp trigger is **not** tripped). Sealed window only, printed as counts, deciding
    nothing; `eval.py` re-evaluates both on the full window at the decision pass, which is the pass
    that fires the diagnostics.
- **In-sample figures, for context only.** EXPLORE_001 §G (April–May 2026, 35 nights, the broken
  market-wide earnings resolver, arm labels recomputed from the post-hoc corrected backfill):
  **30 picks / 18 nights** with a report 0–3 sessions out and **53 picks / 16 nights** at 4–10
  sessions. Those nights are **outside this question's window** (§6) and the counts are **not a
  projection** for the post-fix period: the catalyst layer became a different feature on 2026-06-01
  (DP-06) and the population of published picks with an imminent print may have moved in either
  direction. They are quoted only to show the question is not obviously empty.
- **Direction the platform's own scoring pushes (relevant to expected n, not to the endpoint):**
  after the fix, an imminent report is a **small bonus, never a penalty** — the catalyst matrix
  scores `PRE_1_3` at 88 for bears and 81 for bulls against a baseline 80, and `EARNINGS_DAY` at
  exactly 80 (volatilx `services/catalyst_scoring.py:49-57`), on a 10%-weight layer. SAS therefore
  does not suppress arm-A picks, and arm A over-represents **bears** (§10 threat 2).
- **Routed requests (Data Steward, counts only; no outcome, no touch, no return, no
  picks-minus-control difference):**
  - **R1(a) — knowledge-time verification, was blocking (DP-41): RETURNED PASS, 2026-09-13.** The
    sealed-window `days_to_earnings_corrected` / `earnings_phase` / `earnings_event_risk_corrected`
    values are **live-path writes** at scoring time (volatilx
    `services/super_agent_select_service.py:396-402`, platform SHA `fa70688b`, matching the
    manifest), not the Phase-0b backfill. Evidence in §10 threat 1. **No rule-14 exception is
    requested or granted; DP-41's DEFERRED branch does not fire.**
  - **R1(b) — exposure: RETURNED, 2026-09-13.** Counts above. **Both floors project inside DP-43's
    12-month ceiling (2027-09-13), so Q013 is locked rather than deferred.**
  - **R2 — successor freezes (DP-23): open, and never a blocker for the lock.** Due at the decision
    date: pick nights after 2026-09-10 through the window end **2027-02-12**, built in time for
    Monday **2027-03-22** (a second pair covering ..2027-03-30, for Monday 2027-05-10, only if the
    DP-13 extension fires). Scope in the freeze-discipline bullet below.
- **Window: pick nights 2026-06-01 .. 2027-02-12** (start = the catalyst fix boundary, DP-06,
  `exclusions_v003.json` `catalyst_layer_regime_change.fixed_from`; end computed at lock by DP-43's
  recipe — 23 contributing nights measured through 2026-08-12, 57 still needed for DP-21's 80, at
  the measured **0.4510 contributing nights/session** → 127 further sessions → **2027-02-12**).
  In-window exclusion dates are read from `exclusions_v003.json`, never hard-coded; on the sealed
  part they are 2026-06-26, 2026-07-02 and 2026-07-06.
- **Decision date: Monday 2027-03-22** (DP-43's fixed recipe; DECISIONS.md item 3, DEFAULTED under
  DP-43). Window end 2027-02-12 **+ 20 sessions maturity** = 2027-03-15 (2027-02-15 Presidents' Day
  closed) **+ a one-week freeze margin** = 2027-03-20 (Saturday) → the first Monday on or after.
  The **80-contributing-night floor is the binding gate**; DP-24's 30 post-lock nights project to
  2027-01-25 and do not move the date out further. The drafted floor of Monday **2027-03-01** stands
  as a floor the projection may push **out** but never pull **in** — 2027-03-22 is three weeks
  later, so it governs; nothing in this schedule is earlier than any date the draft named.
- **Single automatic extension (DP-13), then DEFERRED.** If either gate is short on `eval.py`'s
  measured counts at the decision pass, the window extends **once**, automatically, to pick nights
  **.. 2027-03-30** (= 2027-02-12 + 30 sessions; 2027-02-15 Presidents' Day and 2027-03-26 Good
  Friday closed), and the evaluation re-runs on **Monday 2027-05-10** (2027-03-30 + 20 sessions =
  2027-04-27 + one week = 2027-05-04, first Monday on or after) with the **byte-identical**
  `eval.py`. **There is no hard stop and no second extension:** if a gate is still short after that
  one extension, Q013 goes to **DEFERRED** (`research/questions/DEFERRED.md`, with the measured
  counts). No reduced floor, no under-powered run, and **a gate shortfall is never INCONCLUSIVE**
  (DP-13, DP-21, DP-43). Where the 365/252 calendar convention and exact session counting disagree,
  the **later** date is taken (DP-45), and the closed sessions are named above.
- **DP-43's 12-month ceiling: 2027-09-13.** A projected initial decision date after that would mean
  Q013 is **not locked** and goes to `research/questions/DEFERRED.md` with the date and the measured
  rate named (the H-062 precedent). **The test is passed** — 2027-03-22 is inside the ceiling by
  nearly six months, and even the extension date 2027-05-10 is inside it — so Q013 locks.
- **Gates fire on `eval.py`'s measured counts** from the frozen data at the decision pass, never on
  the projection above, on R1(b), or on a run-rate. `eval.py` is written once (rule 9) and run once.
  **No interim looks.**
  *Why the rate had to be measured rather than assumed:* contributing nights for this question are
  **seasonally clustered** — S&P reporting comes in roughly six-week bursts each quarter, and the
  measured monthly rate swings 10.0% → 70.0% → 87.5%. The projection above uses the **blended
  whole-window** 0.4510/session, the only figure DP-43's recipe admits. The July–August-only rate
  (0.75/session) is **not** used: it would project the 80-night floor to about 2026-12-14, i.e.
  *earlier* than the drafted floor, and a projection may push a date out, never pull it in. Reading
  the June trough (0.10/session) forward would put the floor outside the ceiling, but a one-month
  worst case is a forecast, not a measured run-rate, and the desk does not pre-DEFER a question on a
  forecast. If the rate really does fall back to the trough, the gate comes up short on `eval.py`'s
  measured counts, the single DP-13 extension fires, and DEFERRED follows — the conservative path,
  with no guess needed now.
- **Freeze discipline (DP-23; R2):**
  - Selections for nights ≤ 2026-09-10 stay pinned to `manifest_v001` / `manifest_prices_v001`.
  - Nights after 2026-09-10 enter only through the successor selection freeze (same SQL as v001, same
    exclusion criterion), covering pick nights 2026-09-11 .. **2027-02-12** and frozen after the
    window closes. A second pair (.. 2027-03-30) is built only if the DP-13 extension fires.
  - Forward prices for **all** nights come from the successor price freeze: the same Alpaca queries
    with `end` ≥ the 20th session after the last pick night, and a symbol list covering **every
    candidate on every night in the window, published and unpublished** (B2 needs the unpublished
    symbols' opens and forward bars), **plus hourly bars for published symbols** for the §4
    descriptive tie-break.
  - `eval.py` records every sha256 and prints sealed (≤ 2026-09-10), post-lock and pre-lock night
    counts separately. It takes the window, the manifests, the exclusions path and the output
    directory as **inputs** — no hard-coded date and no hard-coded path — so one byte-identical
    script serves both the decision-date run and the extension run (DP-13).
  - If a successor price freeze omits unpublished-candidate symbols for a night, that night's picks
    lose their controls and the night is excluded from the primaries and counted — never back-filled.
- **Sub-cells** (reported only where they clear 20 contributing nights): bull / bear; score band
  (< 80 / 80–85 / 85–90 / 90+); `best_timeframe`; `d_open` ATR-distance tercile; `atr_pct` tercile;
  tape stratum; regime label; reporting-season block. Bear and 90+ cells are expected to be
  SUPPRESSED (DATA_NOTES: 12 / 8 / 3 / 2 elite picks per month since June; PI-010).

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights from 2026-06-01.**
  *Justification (contamination):* EXPLORE_001 §G tabulated exactly this contrast — L3 hit rate and
  20-session drawdown from the open for the 0–3 vs 4–10 session buckets — on **April–May** picks.
  Those nights are contaminated for this question and are excluded. They are also **pre-fix**: before
  platform commit `69ef05f` (2026-06-01) every candidate carried a bogus market-wide earnings date
  (`catalyst_context.next_earnings_date` ≥ 38 days out for every in-sample candidate), so the
  in-sample arm labels exist only as a post-hoc backfill and are not knowledge-time legal (DP-06;
  DATA_NOTES).
  *Registrar's contamination check on the sealed period, on code and counts only:* a text search of
  `research/reports/weekly/`, `research/reports/daily/` and `research/BACKLOG.md` for any earnings
  figure on nights ≥ 2026-06-01 returned **nothing**. No results directory was read.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date; Half B = after. The sealed (≤ 2026-09-10) vs post-lock (≥ 2026-09-14)
  panel is printed descriptively beside it. `in_sample_end = 2026-05-29` only marks what is excluded.
- **Reporting-season stratum (rule 7's spirit, this question's version):** each contributing night is
  tagged with its reporting-season block (the quarterly earnings cluster it falls in, cut on the
  eligible-night set by the density of arm-A picks, fixed before any outcome is read). A result
  present in only one season block is reported as such and is called out in §8 clause 6.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v003.json` `regime_label_point_in_time_from`; PI-005). It is used only for nights on
    or after that boundary — **read from the exclusions file by `eval.py`, not hard-coded**, and
    2026-06-09 in `v003` — and only with `regime_version = 'v1.2'`. Earlier in-window nights
    (2026-06-01..06-08 under `v003`) carry no legal
    label, are stratified by the SPY proxy only, and are flagged.
  - Primary tape stratum, trailing and legal at 16:05 ET: `tape_t` = sign of SPY's trailing
    20-session return × tercile of SPY's trailing 20-session realized volatility, from
    `prices_daily_split` bars dated ≤ t, terciles cut on the eligible-night set. Cells < 20 nights
    SUPPRESSED.

### 6.1 Knowledge time (rule 14) — every input declared

| input | source | available | use |
|---|---|---|---|
| `qualified`, `selected_rank`, `qualification_reason`, `dominant_direction`, `overall_score`, `best_timeframe`, L1–L4 and swing `stop` from `lane_plans` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) | population, direction, band, levels |
| **`days_to_earnings_corrected`, `earnings_phase`, `earnings_phase_subtag`, `earnings_event_risk_corrected`** | `sas_candidates` | **pick night, 16:05 ET for rows ≥ 2026-06-01** — written on the live path from the scoring-time catalyst context (`super_agent_select_service.py:396-402`; `super_agent_select_scoring.py:1436-1444`) | **arm assignment (A / B / C)**; the flag itself is descriptive |
| control-candidate pool (non-published rows, night t), including their own `days_to_earnings_corrected` | `sas_candidates` | pick night, 16:05 ET | B2 pool; B3 arm-matched pool |
| `C_t`, ATR14, beta60, runup20, SPY trailing tape | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | matching, distances, stratum |
| regime label (v1.2, nights ≥ 2026-06-09) | `market_regime_daily` | pick night, ~16:05 ET | stratum |
| `finished_at` | `sas_runs` | publication time | exclusion criterion only |
| **entry `O_1`**, forward highs/lows/closes, sessions 1..20 | `prices_daily_split` | after the decision | **outcome only** |
| counter-target prices (descriptive) | `sas_excursion.counter_levels_json` | copied from the publication-time report into a post-hoc table (prices only, never its dates) | descriptive race |

- **No rule-14 exception is requested or used, and DP-05 is untouched.** The arm label is a
  scheduled report date known at 16:05 ET on the pick night; every outcome is measured from the next
  session's open onward. Nothing in this question needs a later clock (contrast DP-05(b), which is
  Q008's and does not travel).
- **Binding on `eval.py`:** it freezes the eligible set, the arm labels, the matching inputs and
  every stratum label **before any session-t+1 or later bar is loaded**, and fails loudly if a
  t+1-or-later field is referenced in eligibility, matching or stratification.
- **The pre-fix period is excluded precisely because its arm label is not point-in-time** (§6). The
  same column serves the Phase-0b backfill and the live path, which is why R1(a) was blocking; it
  **returned PASS** on 2026-09-13 (§5; §10 threat 1), and `eval.py` repeats the check at the
  decision pass.
- `sas_excursion` hit/touch columns, `level_hit_dates_json`, `level_hit_steps_json` and every
  `outcome_*` column are **never** inputs — they are outcomes on a different basis and
  `level_hit_dates` can carry manual overrides (volatilx `routers/performance.py:935-970`).
  `uoa_symbol_daily.fwd_return_*` is banned (FREEZE_v001 §5; PI-001).

## 7. Multiple testing

- **Within the question:** **m = 2 primary endpoints (P1, P2)**, Benjamini–Hochberg across the 2
  (DECISIONS.md item 1: arm C stays descriptive, so there is no third primary). The verdict uses q.
  Every secondary prints raw p only, marked "descriptive, does not decide".
- **Across the family:** **F4 Price behaviour after selection** (assigned by the primary endpoint's
  subject — the price path after selection, DP-29) holds H-030 (→ Q007), H-031 (→ Q008), H-033,
  H-034 and H-064 (this file) — H-063 is *merged into Q007* and H-032 was re-filed to F6 with
  Q009/Q010, so neither is counted here (DP-29). Registered F4 questions at this lock: **Q007 (4
  primaries), Q008 (3 primaries), Q013 (2 primaries)** = **9 primary endpoints**, verified against
  those files. Q009/Q010 are F6, Q011 is F7 and **Q012 is F6** (re-filed from F7 under DP-29), so
  none of them enters F4's count. The Reporter applies BH across all primary endpoints of
  registered-and-run F4 questions and prints both q's.
- **Overlaps (not duplicates; never presented as independent evidence):**
  - **Q007 (F4, gap at open):** same nights, same picks, a different conditioning variable, and a
    pick-night-close entry. An earnings print inside the window is one reason a pick gaps; the two
    reports are cross-referenced, never counted twice.
  - **Q008 (F4, fast start → L4):** same nights, different conditioning variable and level.
  - **Q011 (F7, day-1 dip limit):** same L3 level and a 20-session clock, different entry rule.
  - **Q006 (F1):** reports L3 unconditionally against the same style of control.
  - **H-041 (F5, unregistered):** repeat selection *within 10 days before* earnings — a different
    decision (selection persistence), overlapping population. If it is ever registered, its overlap
    with Q013 is declared there.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`P1 = mean_t Δ1_t` is in percentage points of L3 touch rate; `P2 = mean_t Δ2_t` is in ATR.

**MPE: P1 = +5.0 pp (DP-20)** exactly — a control-adjusted touch-rate endpoint, and no uplift is
warranted: P1 is a within-night A-minus-B contrast of control-adjusted rates, not an uncontrolled
arm contrast. **P2 = 0.25 ATR (DP-10 via DP-44)** — the standing per-trade ATR number, not re-asked
and not re-unitised. Both are **two-sided** and no money-unit MPE is invented anywhere (DP-44).

Per endpoint (two-sided; the verdict carries its sign):

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. **≥ 80 contributing nights** (§2, §5) **and ≥ 30 contributing nights dated after this file's
     lock commit**. These clauses do not weaken: if either is short at the decision date on
     `eval.py`'s measured counts, the **single automatic DP-13 extension** fires (§5: window
     .. 2027-03-30, re-run Monday 2027-05-10, byte-identical `eval.py`); if a gate is still short
     after that one extension, Q013 goes to **DEFERRED**. A gate shortfall is **not** an
     INCONCLUSIVE verdict. A shortfall on one endpoint is never covered by the other's count;
  2. `|estimate| > MPE`;
  3. block-bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 within the question;
  5. the point estimate has the **same sign in both calendar halves**, and neither half is beyond MPE
     in the opposite sign;
  6. no tape stratum, regime cell or reporting-season block with ≥ 20 contributing nights is beyond
     MPE in the opposite sign.
- **NULL:** floors met **and** the 95% CI includes 0 **and** `|estimate| < MPE`. "An imminent report
  says nothing about the path" is a real finding and is ledgered with the same care.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, `0 < |estimate| ≤ MPE` with the CI
  excluding 0 ("real but below MPE", rule 6), or a CI excluding 0 in a direction no half supports.
  **A sub-cell below 20 contributing nights is SUPPRESSED** — counts printed, no point estimate —
  and does **not by itself** make an endpoint INCONCLUSIVE (DP-21; the locked Q007 §8 clause 1
  wording). The stratification protection stays exactly where rule 7 puts it: clause 5 (same sign in
  both calendar halves) and clause 6 (no stratum with **≥ 20 contributing nights** beyond MPE in the
  opposite sign). Neither is weakened, and no floor is lowered and no arm or cell demoted after lock.

**Question-level reading (pre-specified, so nobody argues after the fact):**

| P1 (touch) | P2 (drawdown) | label | what it licenses |
|---|---|---|---|
| CONFIRMED negative | CONFIRMED positive | **"the print costs you both ways"** | the full §9 package: card flag, guide line, and a candidate execution gate — subscriber-facing only after PROSPECTIVELY_CONFIRMED |
| CONFIRMED negative | NULL / INCONCLUSIVE | **"fewer targets reached, no measurable extra drawdown"** | a `playbook/` line and a card flag; **no** claim about risk or drawdown |
| NULL / INCONCLUSIVE | CONFIRMED positive | **"same target rate, a rougher ride"** | a `playbook/` sizing note and the "no position across the print" line; **no** skip rule on the touch rate |
| CONFIRMED positive (either endpoint in the hypothesis-opposite sign) | | **"earnings run-up"** | nothing ships on this run; the opposite rule is registered as its own prospective question before anything changes |
| NULL | NULL | **"an imminent print does not change the path"** | EN-014 is closed as a research item; the existing display note stands; ledgered |
| otherwise | | **INCONCLUSIVE** | nothing ships |

**What a CONFIRMED P1/P2 does *not* license:** a statement that SAS is at fault or that SAS should
be re-scored. The primaries use an **unrestricted** distance-matched control (§3 B2), so they cannot
separate "SAS picks with a print do worse" from "every stock with a print does worse". That
separation is B3's, and B3 is descriptive. A skip rule needs only the former; a scoring change would
need the latter, registered on its own.

- **PROSPECTIVELY_CONFIRMED:** only after **≥ 30 contributing nights dated on or after the lock
  commit** (DP-24), frozen separately and never inspected earlier, reproducing the sign of every
  confirmed endpoint under the **unmodified `eval.py`**. On R1(b)'s measured rate the window
  supplies these by **2027-01-25**, before the 2027-03-22 decision date (§5), so the prospective
  track is reachable from this run, **DP-31 does not apply**, and Q013 is not `HISTORICAL_ONLY`. No
  subscriber-facing statement before that (rule 10); even then the basis stays NON_QUOTABLE until it
  is restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

**What exists today.** The scoring layer gives an imminent report a small *bonus*: `PRE_1_3` scores
88 (bear) / 81 (bull) against a baseline 80 on the 10%-weight catalyst layer, and `EARNINGS_DAY` is
a strict no-op at 80 (volatilx `services/catalyst_scoring.py:49-57`). `earnings_event_risk` is
computed and persisted but is explicitly **non-scoring**, "surfaced for the Phase 2 execution gate
only" (`services/super_agent_select_scoring.py:1433-1444`) — **that gate does not exist**. The only
subscriber-visible guard is a display payload: `_event_risk_payload` marks `risk_level = "high"` and
`blocking_conflict = true` when `0 ≤ days_to_earnings ≤ 7` (volatilx
`routers/super_agent_select.py:335-385`, rendered in `templates/ai_picks.html:2582`, `:2623`). It is
a note beside the card. It changes **no** lane plan, **no** ladder, **no** scale-out schedule, and
it is keyed to calendar days, not sessions.

- **"The print costs you both ways" (P1 negative and P2 positive):**
  - **EN-014** ships: an earnings-window flag on the pick card keyed to **sessions to the report**,
    with the measured arm-A and arm-B numbers and the matched-control rate beside it (rule 5), and
    the line "no position across the print".
  - A line in the **Manual Trading Guide**: skip a pick whose report is `k ≤ 3` sessions out, or
    plan the exit before the print (Plan X, §4).
  - The **execution gate the code already anticipates**: `earnings_event_risk` becomes an actual
    gate on the published book — a candidate with `k ≤ 3` is either demoted below the publication
    floor or published with a shortened lane plan whose target resolves before the report. The exact
    form comes from a strategist ruling on this question's per-`k` and Plan X tables, not from the
    registrar.
  - Brief against `services/catalyst_scoring.py`, `services/super_agent_select_scoring.py` and the
    card surface. **Ship flag-off with a byte-identical checksum on the old path, shadow ≥ 20 trading
    days (rule 11). Subscriber-facing only after PROSPECTIVELY_CONFIRMED (rule 10).**
- **"Fewer targets reached, no measurable extra drawdown":** the `playbook/` skip line and the card
  flag only. No risk or drawdown language anywhere.
- **"Same target rate, a rougher ride":** a `playbook/` sizing note (half size, or no spread across
  the print) and the Plan X line. No skip rule.
- **"Earnings run-up" (hypothesis-opposite sign):** nothing ships. The opposite rule is a new
  question, registered prospectively before any change.
- **All NULL:** **EN-014 is closed** as a research item and TI-010 is retired; the existing display
  note stands as a courtesy, and the desk stops proposing an earnings skip rule. F4 effort moves to
  H-033 / H-034.
- Owner: implementer.

## 10. Known threats to validity (registrar's own list)

1. **The arm label lives in a dual-purpose column.** `days_to_earnings_corrected` is both the
   Phase-0b backfill target (`scripts/rescore_sas_earnings_corrected.py`, source file ending
   2026-05-30) and the live-path write from 2026-06-01 (`services/super_agent_select_service.py:399`).
   A re-run of the backfill across the sealed window would silently overwrite live values with
   `NO_UPCOMING` / null and would look like "no picks had earnings". **R1(a) was blocking for exactly
   this reason and RETURNED PASS on 2026-09-13** (`research/reports/STEWARD_Q013_exposure.md` §R1(a)):
   the live write block at platform SHA `fa70688b` (matching the manifest) matches the PREREG
   citation exactly; the monthly `earnings_phase` mix swings **NO_WINDOW 83.1% → 19.3% → 70.8% →
   87.4%** across June–September, a real seasonal reporting cluster that a flat backfill cannot
   produce; non-null `days_to_earnings_corrected` holds at **98–100%** by month where a re-run of the
   backfill would write null/`NO_UPCOMING`; and `created_at` clusters **20:00–22:00 UTC on 98.5% of
   the 4,195 sealed rows** (16:00–18:00 ET under EDT), the only two exceptions being 2026-07-02 and
   2026-07-06 — the manual re-run nights already carried in `exclusions_v003.json`. Two disclosures
   ride along, both accepted, neither changing the verdict: (i) `$RESEARCH_DB_URL` was not set in the
   Steward's session, so the row timestamps were read from the frozen parquet's own
   `created_at`/`updated_at` rather than a live query — for historical, already-published,
   already-frozen rows these are the same DB-sourced values, and reading the freeze rather than the
   live table is the stricter course under rule 4, not a substitution; (ii) `earnings_phase_subtag`
   is **100% null** in the sealed window because the live write block never calls `neutral_subtag()`
   — a code-confirmed non-population, not a knowledge-time defect, and this PREREG uses that column
   descriptively only, never for arm assignment. **No rule-14 exception is requested or granted;
   DP-05 is untouched.** The threat stays in the file because **`eval.py` reprints the monthly phase
   distribution and the non-null share, so the same check repeats on the successor freeze at the
   decision pass**; a failure there is a `results/` finding, not a re-opened lock decision.
2. **Arm composition.** Post-fix, an imminent report is a bonus that is **four times larger for
   bears** (`PRE_1_3`: +8 bear / +1 bull), so arm A over-represents bear picks — a population the
   desk already suspects behaves differently (H-062). Arm A may also skew toward high-ATR names and
   wider ladders. Mitigations: B2 carries each pick's own direction and ATR distance, so the
   composition is differenced inside the estimator; direction, `d_open` tercile, `atr_pct` tercile
   and band cells are printed; the composition panel (§4) is a headline. **Residual risk:** if arm A
   is almost entirely bearish, P1 and P2 are partly a bear-vs-bull contrast wearing an earnings
   label. **Mandatory diagnostic, not discretionary:** if the bear share of arm A exceeds the bear
   share of arm B by more than **20 pp** on `eval.py`'s measured counts, the direction-restricted
   contrast (bullish picks only) is printed **beside** the primaries — it never replaces them. The
   threshold was fixed before any outcome was read and is not tunable at the decision pass. On the
   sealed window the gap is **1.6 pp** (arm A 4.5% vs arm B 2.9%), so the trigger is not tripped
   there; the same `eval.py` run re-evaluates it on the full window, which is the pass that counts.
3. **`passed_at_entry` cuts toward the hypothesis.** A pick that gaps favourably through L3 at the
   open is scored a non-hit (DP-26), and arm-A picks gap more (a print on the pick night or the next
   morning). That mechanically lowers arm A's touch rate in the hypothesis's direction. It is
   registered this way because a target you cannot buy is not a target, and because the same rule
   grades the controls — but the per-arm share is a headline and **both** bounding sensitivities are
   printed (§4). **Mandatory diagnostic, not discretionary:** if the arm-A `passed_at_entry` share
   exceeds arm B's by more than **10 pp** on `eval.py`'s measured counts, the report **leads with the
   two bounds**, not with the point estimate. The threshold was fixed before any outcome was read and
   is not tunable at the decision pass. On the sealed window the gap is **3.8 pp** (arm A 4.5% vs
   arm B 0.7%), so the trigger is not tripped there; the same `eval.py` run re-evaluates it on the
   full window. Removing `passed_at_entry` picks from the denominator would filter it on a
   session-t+1 price, which rule 14 forbids — hence the registered rule keeps them (DP-26) and the
   two sensitivities only bracket it; **neither decides**.
4. **Before-open vs after-close is unknown.** The desk holds the report *date*, not whether the
   company reports before the open or after the close. So `k = 0` may be a print that already
   happened, and `k = 1` may be a print the entry at `O_1` has already absorbed. This dilutes arm A
   toward arm B (conservative for the hypothesis, DP-45) but it also blurs the dose-response. The
   per-`k` cells expose it. A future version with a BMO/AMC field is a new question, not an edit.
5. **Seasonal clustering.** Contributing nights arrive in quarterly bursts, so the effective number
   of independent observations is smaller than the night count suggests, and the calendar halves can
   split a season. Mitigations: the block bootstrap (expected block 20 sessions), the
   reporting-season stratum, and §8 clause 6.
6. **The ladder may already be earnings-aware.** The projection layer tags targets
   `[EARNINGS EVENT IN WINDOW]` and floors their confidence at "medium" when the target must be held
   across the print (volatilx `services/catalyst_scoring.py:71-80`). Arm-A picks may therefore carry
   systematically different L3 distances, which would make P1 partly a distance effect. B2 matches
   on distance and the `d_open` terciles are printed; the composition panel shows the tag share.
7. **Equity path is a proxy for the trade the rule is about.** The mechanism H-064 names is binary
   risk **plus IV crush**; IV is invisible here. A NULL on the equity path does **not** clear a
   spread held across a print, and a CONFIRMED does not quantify what the spread lost. No §9 line may
   mention option P&L (DEFERRED.md; EN-011).
8. **Scheduled dates move.** The arm label is the date the platform knew at 16:05 ET; a company can
   move the date afterwards, so some arm-A picks did not actually report inside three sessions. This
   is the correct decision-time information — the skip rule would use exactly this label — but it
   attenuates the measured effect toward zero, and the desk cannot quantify the drift with the data
   it holds (the only post-hoc earnings file ends 2026-05-30).
9. **Overlapping 20-session windows** inflate precision. The block length is fixed here at 20
   sessions, not chosen after seeing results.
10. **One tape.** June 2026 – 2027 is one macro stretch, and the regime label is illegal before
    2026-06-09. A sign present in only one half fails §8 clause 5.
11. **Null-ladder denominator** (PI-006) and `outcome_target_invalid` rows: excluded and counted
    (§2).
12. **Dark-lane predicate elsewhere.** Q002, Q004 and Q006 define "published" as
    `selected_rank IS NOT NULL`, which since 2026-07-02 also catches never-published dark rows. This
    question uses DP-28. The difference is small today and grows; flagged for those questions'
    reviews, not fixed here.
13. **Daily-bar definition — verified.** The desk assumes the Alpaca SIP daily `o/h/l` are
    regular-session values; verified in STEWARD_Q007_exposure.md §R3 Part 1 (PASS 40/40) with the
    caveat that the frozen data is hourly, not tick-level. **Binding on `eval.py`:** the 09:30/16:00
    ET boundary is derived **per date with `zoneinfo` (America/New_York)**, never a fixed UTC offset.
14. **Control-pool thinness for B3 — confirmed by measurement.** The arm-matched pool (same night,
    same `k` band) averages **8.2 rows per arm-A pick** and 26.9 per arm-B pick, and **13.3% of
    picks (arm A 27.3%)** would fall below 3 valid controls, against 0.0% under B2
    (`STEWARD_Q013_exposure.md` §3). That is why B3 is descriptive and cannot carry a primary; it
    must never be silently substituted for B2, and nights where B3 is undefined are counted, not
    back-filled.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: R2 (successor freezes, DP-23), due
at the decision date and never a blocker for the lock. R1(a) and R1(b) both returned on 2026-09-13
and are closed.
