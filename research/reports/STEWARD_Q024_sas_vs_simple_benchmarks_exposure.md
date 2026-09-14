# STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md

**Request:** Q024 (`research/questions/Q024_sas_vs_simple_benchmarks/`) DECISIONS.md, "data-steward -- R1
(counts only) -- BLOCKING FOR LOCK", lines 37-40, plus the coordinator's routing note. Counts only, no
outcomes, no touch rates, no returns. Frozen data only (`manifest_v001.json` + `manifest_prices_v001.json`
+ `exclusions_v003.json`), never a live query (DP-50(c)), except the platform-repo `git log`/`git show`
sweep and one attempted live Alpaca metadata check (R1(d)), which could not run this session -- see below.

Do not confuse this with `research/questions/Q024_exposure_attribution/` (a different draft, being
renumbered by the registrar). This report is scoped only to `Q024_sas_vs_simple_benchmarks`.

---

## Headline

- Every arm measurable from frozen data clears the 0.36 floor with room to spare. SPY, SECRAND, MOM20,
  MOM60 and TECH all measure r = 26/46 = 0.5652 contributing nights per elapsed session on the sealed
  panel 2026-07-08..2026-09-10 -- 57 percent above the 0.36 DEFERRED-gate limb. No arm lost a single night
  to its own computability check (step 3); the binding constraint at this rate is the shared baseline
  funnel plus the price freezes own forward-bar horizon (2026-09-10), not any arm-specific shortfall.
- r_min = 0.5652/session, tied across SPY, SECRAND, MOM20, MOM60, TECH. EW (RSP) is not measured below
  floor -- it is unmeasured: RSP is absent from `manifest_prices_v001` and the live Alpaca availability
  check R1(d) asks for could not be run this session (no ALPACA_API_KEY / ALPACA_SECRET_KEY in this
  environment). This is a BLOCKED-PENDING-CHECK status, not a floor failure.
- Lock-or-DEFER call: LOCK is supported for the five measured arms. If R1(d) later returns "RSP not
  retrievable," DECISIONS item 3s own fallback fires (EW deferred as an arm, m falls to 5) -- this still
  clears the "E_min constituent set below three arms then whole question DEFERRED" line, so it does not
  change the lock call, only m.
- Schedule (recommended, using the measured rate, moved OUT per DP-45 since 0.5652 is below the drafts
  0.75 planning haircut): window 2026-09-14..2027-04-07 (142 elapsed sessions, ceil(80/0.5652)), decision
  date Monday 2027-05-17. One DP-13 extension if needed: window end 2027-05-19 (172 sessions), decision
  date Monday 2027-06-28. Both inside DP-43s 12-month ceiling (2027-09-13).
- This 0.5652 figure is itself a conservative floor, not a best estimate, because it is bound to
  `manifest_prices_v001`s own forward-bar horizon (last date 2026-09-10), which lets only 26 of the
  windows 46 nights mature at all. The other proxy computed below -- eligible nights before the maturity
  cutoff, 45/46 = 0.9783/session, with 100 percent (26/26) of the tested nights converting to contributing
  -- says the true future rate (once the successor price freeze 60-session-beyond forward bars remove
  this artifact) is very likely much higher. I report the stricter, directly-measured number as the
  schedule basis and do not extrapolate past what the frozen data supports (DP-50(c); dates move out only).
- RSP feasibility (R1d): UNRESOLVED this session, not fabricated. No live Alpaca credentials were
  available. Code-level check: `research/lib/freeze_prices.py:46`s BENCHMARKS list has no allow/block
  logic; nothing in the platform repo references RSP. Recommend this be the first step when R2 builds
  `manifest_prices_v002`.
- Sector coverage: the platforms working-tree `data/sp500_sectors.json`, LF-normalized, hashes to
  c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201 -- byte-identical to the Q022 pin
  (confirmed via git log --follow: exactly one commit ever, 4171b1a, 2026-05-17). 2,405 entries.
  Published-slate mapping coverage 99.47 percent (BRK.B the only unmapped symbol in this window); B3
  slot-level computability held on 45/45 eligible nights (only 2.3 percent of slots drew unconstrained).
- DP-50(a)/(b) commit sweep since fa70688: none relevant. 4 commits total (2 substantive + 2 merges),
  all dated today (2026-09-13), none touching the publication predicate, publication floor, slate size,
  weights, timeframe multipliers, the lane-plan writer, the ladder/`_enforce_ladder_monotonic`, or any
  repair of historical `sas_candidates`/price rows.

---

## (a) The section 2.3/2.4 funnel, sealed panel 2026-07-08..2026-09-10

Elapsed sessions in window (SPY-bar calendar, `manifest_prices_v001`): 46.
`exclusions_v003.json` (manual_runs union non_session_runs union uncorroborated_publication_runs):
0 dates fall in this window. DP-04 late-finished_at check (every `sas_runs.finished_at` in-window vs
next sessions 09:30 ET / 13:30 UTC open, EDT throughout Jul-Sep): 0 of 46 nights late.

Published slate, any direction, in window: 374 rows / 46 nights (every night in the window published
at least 1 row). By direction: bullish 360, bearish 14, mixed 0.

Pick-level funnel on the 360 bullish published rows (Q024 section-2.4 order):

| step | rule | dropped | cumulative survivors | eligible nights remaining |
|---|---|---:|---:|---:|
| 0 | bullish published rows | -- | 360 | 46 |
| 1 | no swing-lane target (lane_plans.swing_trading.targets[0]) | 0 | 360 | 46 |
| 2 | outcome_target_invalid non-null OR swing T1 wrong side of C_t OR missing C_t | 0 | 360 | 46 |
| 3 | price-scale screen: target/C_t outside [0.5, 2.0] OR implied ATR distance above 12 ATR | 8 | 352 | 46 |
| 4 | fewer than 60 prior daily bars OR no session t+1 open | 8 | 344 | 45 |

- Step 3 drops (8, all fail both legs jointly): APH x7 (2026-07-09, 07-31, 08-05, 08-06, 08-10, 08-11,
  08-12; ratio 2.067-2.266, implied ATR distance 24.0-30.0) plus MNST x1 (2026-07-13; ratio 2.180,
  implied ATR distance 58.4). This reproduces the APH/MNST slice of the APH/KLAC/CRWD/MNST signature
  named in `STEWARD_Q022_exposure.md` (KLAC/CRWD simply do not recur as bullish picks in this shorter
  window); treated as a rule, not a fixed symbol list, per the request.
- Step 4 drops (8): all 8 are the entire 2026-09-10 slate (SNDK, HPE, AMD, MPC, META, ORCL, QCOM, MU)
  -- dropped only because session t+1 (2026-09-11) falls outside `manifest_prices_v001`s horizon, not
  a real screening failure. This removes the whole night (46 to 45 eligible nights); it will not recur
  once the population comes from a freeze whose forward horizon runs past every pick nights t+1 (i.e.
  always, in the live/rolling case).

k_t distribution, 45 eligible nights: k_t=8: 36 nights; k_t=7: 7 nights; k_t=4: 1 night; k_t=3: 1 night.
By month: Jul (n=18) mean 7.39, min 3, max 8; Aug (n=21) mean 7.76, min 7, max 8; Sep (n=6) mean 8.0.

Maturity (section-2.3 step 4, bound to `manifest_prices_v001`s actual last date, 2026-09-10): matured
nights (session t+20 on or before 2026-09-10): 26, spanning 2026-07-08..2026-08-12. Immature nights: 20,
spanning 2026-08-13..2026-09-10 -- a freeze-horizon artifact, not a screening failure: these nights
simply have not had 20 sessions elapse yet as of this freezes as_of date.
Gradeability among matured-night picks (every session t+1..t+20 has a bar for that exact symbol, the
conservative no-shortcut reading Q022 also used): 192/192 = 100 percent.

CONTRIBUTING nights (section-2.3 step 5, the arm-independent floor before any per-arm split): 26 of 46
elapsed sessions = 0.5652/session.

Per-arm computability (section-2.3 step 3), tested across all 45 eligible nights (computability needs
only same-night data, so it is not truncated by the freezes forward-bar horizon the way maturity is):

| arm | computable nights / eligible nights | contributing nights (matured, gradeable, computable) | rate / elapsed session |
|---|---|---:|---:|
| SPY | 45/45 | 26 | 0.5652 |
| SECRAND | 45/45 (0 nights failed; 8 of 344 slots, 2.3 percent, drew unconstrained) | 26 | 0.5652 |
| MOM20 | 45/45 (pool always at or above k_t) | 26 | 0.5652 |
| MOM60 | 45/45 (pool always at or above k_t) | 26 | 0.5652 |
| TECH | 45/45 (pool always at or above k_t) | 26 | 0.5652 |
| EW (RSP) | unmeasurable -- RSP absent from `manifest_prices_v001` | -- | unresolved, see (d) |

No arm shows a computability failure beyond the shared baseline; r_min = 0.5652/elapsed session, tied
across the five measurable arms.

Cross-check / informative upper bound: setting the freeze-horizon maturity cutoff aside, the eligible-
night rate (screens 1-4 only) is 45/46 = 0.9783/session, and 100 percent (26/26) of the nights that were
old enough to test converted to contributing. This says the 0.5652 figure understates the rate the future
window will show once the successor price freeze carries forward bars well past every pick night (R2
spec: 60 sessions beyond the window end) -- but I report 0.5652, the number directly supported by frozen
outcomes-of-existence checks, not the extrapolation, as the schedule basis.

---

## (b) The rank pool (B4-B6)

Candidate-pool size per night, all `sas_candidates` rows (any qualification_reason) with 60 or more
prior daily bars in `manifest_prices_v001`, across the 45 eligible nights: min 56, median 63, max 68
(mean 62.7). 0 of 45 nights had a pool smaller than that nights k_t, whether the pool is counted
inclusive of the published picks (per section 3s registered B4-B6 pool) or restricted to non-published
rows only (the stricter section 2.3 step-3 reading) -- both give the same zero-shortfall result.

CTRA truncated-history scan (repeated per `STEWARD_Q023_exposure.md` section 6): reproduced. CTRA
appears as a candidate row 14 times, 2026-08-20..2026-09-10, after its own daily bars in the freeze stop
advancing. It is never qualified or published in this window (qualified is False on all 14 occurrences),
so it never enters the graded funnel above, and its missing bar history already excludes it from every
60-plus-bar pool count in this section, by construction. No other symbol shows this pattern in-window.

---

## (c) Sector coverage for B3

Artifact integrity: the platform repos `git log --follow -- data/sp500_sectors.json` returns exactly one
commit ever (4171b1a, 2026-05-17) -- unchanged since. The working-tree file, byte-content LF-normalized
(Windows checkout CRLF vs the LF blob Git stores -- confirmed by direct comparison, not assumed), hashes
to c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201, matching the Q022 pin exactly.
2,405 mapping entries. The blob was not hand-supplemented to reach this figure.

| population | rows | unmapped rows | unmapped symbols | row-coverage |
|---|---:|---:|---|---:|
| Published slate (any direction, in-window) | 374 | 2 | BRK.B | 99.47 percent |
| Candidate pool (60-plus prior bars, in-window, any qualification_reason) | 2,882 | 4 | BRK.B | 99.86 percent |

BF.B (the other historically-known unmapped symbol) does not appear as a candidate at all in this window.

B3 slot-level detail (344 eligible bullish slots across the 45 eligible nights): 8 slots (2.3 percent)
drew unconstrained because the picks own sector had no same-sector unpublished candidate that night;
2 slots (both BRK.B) drew unconstrained because the picks own symbol is unmapped. 0 of 45 nights failed
the B3 computability requirement outright -- every night had at least one pick with a genuine same-sector
unpublished draw available.

---

## (d) RSP feasibility -- could not be executed this session

R1(d) asks for a live Alpaca bar-availability metadata check (not a data pull, not a pinned artifact).
ALPACA_API_KEY / ALPACA_SECRET_KEY are not present in this sessions environment (confirmed empty before
attempting any call) -- I am reporting this rather than fabricating a yes or no. Two things I could check
without live credentials, both read-only and inside the platform repo:

- `research/lib/freeze_prices.py:46` -- BENCHMARKS = ["SPY", "QQQ", "IWM", "SMH", "DIA"] is a flat
  Python list with no allow-list, block-list, or endpoint-side symbol restriction in the fetch logic;
  nothing in the fetch path treats RSP differently from any other liquid US-listed ETF.
- A repo-wide search for "RSP" in the platform codebase returns no hits other than two unrelated files
  (`data/sp500_sectors.json`, `data/r2k_symbols.txt`) that merely contain the substring incidentally --
  no code anywhere blocks or special-cases RSP.

Neither of these is the live retrievability check R1(d) actually asks for. Recommend this be the first
action when R2 builds `manifest_prices_v002`, so DECISIONS item 3s fallback (defer EW as an arm, m falls
to 5, no proxy substituted) can be resolved before the freeze is built around an assumption.

---

## (e) Bearish share of the published slate, per month

| month | bullish | bearish | mixed | total | bearish share |
|---|---:|---:|---:|---:|---:|
| 2026-07 | 136 | 7 | 0 | 143 | 4.9 percent |
| 2026-08 | 168 | 2 | 0 | 170 | 1.2 percent |
| 2026-09 | 56 | 5 | 0 | 61 | 8.2 percent |
| total | 360 | 14 | 0 | 374 | 3.7 percent |

---

## (f) DP-50(a)/(b) commit sweep since fa70688

fa70688bc252d14f8d67e371afafc194731c324e (2026-09-05T12:04:10-05:00) confirmed as an ancestor of HEAD
(d19c9a945418b09773baffac37f8d723c8a90a9a). 4 commits total between them (2 substantive plus 2 merges),
all dated today, 2026-09-13:

| commit | author date (local, -05:00) | ET (local+1h) | summary | touches Q024 population mechanisms? |
|---|---|---|---|---|
| 2d5776c | 2026-09-13 17:37:25 | 18:37 | PI-001: floor the legacy outcome backfill window in-process | No. The platforms nightly-pipeline runner script only (backfill-window floor), uoa_symbol_daily backfill window. uoa_symbol_daily.fwd_return_* is already a banned Q024 input and this table has no role in SAS candidate generation, scoring, publication or the ladder. |
| 4775e49 | 2026-09-13 18:02:57 | 19:02 | merge PR 26 (PI-001) | -- |
| 22a2e1b | 2026-09-13 20:55:42 | 21:55 | EN-002: speed-to-target internal card (Haci-only, flag off) | No. New read-only internal tool; app.py plus 2/-0 lines, new files only; commit message states every subscriber-facing service, router and template is byte-identical to 2d5776c. |
| d19c9a9 | 2026-09-13 21:01:07 | 22:01 | merge PR 27 (EN-002) | -- |

None of the 4 commits touch the publication predicate, the publication floor, the slate size, the
weights, the timeframe multipliers, the lane-plan writer, the ladder / _enforce_ladder_monotonic, or any
repair of historical `sas_candidates` or price rows. DP-50(a)/(b): none.

---

## Sub-cell suppression flags (for section 4 list), projected to the recommended decision date

Linear projection from the 26 matured contributing nights (192 picks) to the recommended 142-session
window. Small-sample, indicative only (n=26); this is a projection, not a measurement of the future
window, and is reported as such.

| sub-cell | measured nights (of 26) | rate/session | projected nights at 142 sessions | flag |
|---|---:|---:|---:|---|
| score band 80-85 | 26 | 0.565 | 80.3 | ok |
| score band 85-90 | 9 | 0.196 | 27.8 | ok |
| score band 90+ | 3 | 0.065 | 9.3 | SUPPRESS (already pre-suppressed at lock per PREREG) |
| best_timeframe: short | 26 | 0.565 | 80.3 | ok |
| best_timeframe: swing | 19 | 0.413 | 58.7 | ok |
| best_timeframe: long | 13 | 0.283 | 40.1 | ok |
| confidence_level: high | 26 | 0.565 | 80.3 | ok |
| confidence_level: medium | 16 | 0.348 | 49.4 | ok |
| k_t = 8 | 17 | 0.370 | 52.5 | ok |
| k_t = 7 | 7 | 0.152 | 21.6 | marginal (clears 20 by under 2 nights on a 26-night sample) |
| k_t = 4 | 1 | 0.022 | 3.1 | SUPPRESS |
| k_t = 3 | 1 | 0.022 | 3.1 | SUPPRESS |
| top-3 by selected_rank | 26 | 0.565 | 80.3 | ok |
| rest of slate | 25 | 0.543 | 77.2 | ok |
| regime: strongly_bullish (v1.2, same-evening) | 19 | 0.413 | 58.7 | ok |
| regime: bullish (v1.2, same-evening) | 7 | 0.152 | 21.6 | marginal |
| regime: bearish or neutral | 0 | -- | -- | none observed at all -- see caveat below |

Regime-label caveat (binds on section 6 / threat 2): every one of the 26 matured nights carries a
same-evening regime_version='v1.2' row (100 percent coverage -- the window is entirely after the
2026-06-09 point-in-time cutoff, so this is knowledge-time-legal). But 19 of 26 are strongly_bullish and
the remaining 7 are bullish -- zero nights of any other label. This reproduces
`STEWARD_Q023_exposure.md` section 3 finding of a near-degenerate regime label over this stretch. If the
pattern continues into the prospective window, no non-bullish regime cell will ever reach the 20-night
suppression floor, and any "holds across regimes" statement in the eventual report will be structurally
untestable, not merely under-measured.

Tape stratum (SPY trailing-20-session return sign times trailing-vol tercile, expanding-window cut points
per section 6) is not computed in this pass -- it needs the expanding-tercile machinery eval.py will
build, which is a computation, not a count; flagging it as an open item for eval.py rather than
approximating it here.

---

## What this request decides versus what it does not

Per DECISIONS.md item 9 / R1 own framing, this report supplies the counts the DEFERRED gate and schedule
turn on. I do not decide the lock; I report that every measurable arm clears 0.36 by a wide, one-sided
margin, that EW/RSP is unresolved rather than failing, and the schedule arithmetic both ways (measured
0.5652 and the informative 0.9783 upper bound) so the coordinator can apply DP-43/DP-45 move-out-only rule
against the number it decides is the right basis. No outcome, touch, return or arm difference appears
anywhere above.
