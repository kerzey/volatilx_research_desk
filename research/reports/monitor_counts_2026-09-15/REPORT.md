# Conviction Monitor — what it is and what it prints (counts only)

**2026-09-15. Operational census, counts and code only — no price, return or touch column was read.
INTERNAL / NON_QUOTABLE.** Prompted by Haci: "I want to understand if the conviction monitor is working.
I ignore it in my trading. Is the overall evaluation correct, which data has significant impact, and if it
is useless we can remove it." Script: `counts.py` in this folder (live read-only session; rule 4 allows
counts for operational checks). Source of truth: volatilx `services/conviction_monitor_service.py`.

## Decision paragraph

The monitor watches each published pick for **five sessions only** and prints one of three tiers, but
**since 2026-06-01 it has printed only two: EXIT or WATCH, never HOLD**, because its options-flow arm has
been dark (PI-014) and the worst-of rollup makes that arm's permanent WATCH the floor. In that state it
rates **67% of picks EXIT within five sessions, 70% of those on day 1**, and **45% of the picks it rates
EXIT are back to a softer tier on a later day.** Whether acting on EXIT is worth money is exactly **Q019**,
locked, decision **2027-05-24**; nothing here opens that. What the census adds is that the question of
"which data matters" has a short answer today: **the tier is driven almost entirely by 30m/1h/4h support
breaks measured against the pick-night snapshot**, i.e. by the price having already fallen. Whether that
carries information *beyond* the fall is the damage-matched test Q019 registers. Two new hypotheses are
filed for what Q019 does not ask (H-097 calibration and reversal, H-098 reason-code mining), and one more
defect is added to PI-014 (HOLD is unreachable).

## 1. How the tier is built (code)

- Two arms per pick per day: an **options-flow polarity** arm (`_polarity_tier_for_direction`, `:172-200`)
  and a **technical** arm over five timeframes 30m/1h/4h/1d/1wk (`:328-735`), each compared with the
  pick-night snapshot: structure (higher-high / higher-low chains), key-level and Fibonacci support
  breaches, Kalman regime and confidence, OBV / MACD flips, Elliott invalidations, overall-bias flips.
- Technical rollup (`_compute_technical_overall_tier`, `:736-790`): EXIT when ≥ 2 timeframes are EXIT, or a
  single 1d/1wk EXIT with ≥ 2 break codes; WATCH when exactly one timeframe is EXIT or ≥ 2 are WATCH; HOLD
  otherwise.
- **Overall = worst of the two arms** (`_worst_tier`, `:792-805`). Decay (`_decay`, `:807-811`): days 1–2
  full severity, days 3–5 one step softer (`age_adjusted_severity`), day 6+ dropped.
- Surface: the "Conviction Monitor" tab on the AI Picks page (`templates/ai_picks.html:1949`, router
  `routers/conviction_monitor.py`). **Nothing else reads it** — not selection, not the conviction card,
  not the plans. It shows a tier and prescribes nothing.

## 2. What it printed, 2026-06-01 .. 2026-09-14

- 588 picks tracked (589 of 604 published picks have monitor rows), 5 rows each; 2,921 rows.
- **Overall tier by day since the pick (rows):**

| day | EXIT | WATCH | HOLD |
|---|---:|---:|---:|
| 1 | 273 | 314 | 0 |
| 2 | 255 | 331 | 0 |
| 3 | 154 | 432 | 0 |
| 4 | 180 | 405 | 0 |
| 5 | 193 | 384 | 0 |

- **Ever EXIT within 5 sessions: 394 of 588 (67%).** First EXIT day: 1 → 270, 2 → 83, 3 → 15, 4 → 14, 5 → 12.
- **EXIT later softened to a non-EXIT tier on a subsequent day: 266 picks (45% of all tracked, 68% of the
  ever-EXIT picks).** Part of that is the day-3 decay step, part is the technicals repairing.
- The displayed `age_adjusted_severity` is HOLD on 1,221 rows — but only as a decayed WATCH, never as a
  judgement that conviction is intact.

## 3. Which data drives EXIT

Per-timeframe tiers on EXIT rows: the **4h** timeframe is EXIT on essentially every EXIT row; the most
common patterns are 30m HOLD / 1h HOLD / 4h EXIT / 1d EXIT (with 1wk EXIT, WATCH or HOLD). Reason codes
with the largest lift on EXIT rows vs other rows:

| code | on EXIT rows | on other rows |
|---|---:|---:|
| `key_support_breached_1d` | 27% | 0.1% |
| `fib_nearest_support_broken_1d` | 47% | 0.2% |
| `key_support_breached_4h` | 51% | 6% |
| `fib_nearest_support_broken_4h` | 68% | 8% |
| `elliott_start_invalidation_breached_1h` | 26% | 3% |
| `overall_bias_flipped_4h` | 43% | 8% |
| `key_support_breached_1h` | 81% | 16% |
| `fib_nearest_support_broken_30m` | 86% | 20% |

Codes with **no** discrimination (lift ≈ 1): `obv_flipped_bearish_*` on 30m/1h/4h (26–29% on both),
`elliott_pattern_degraded_*`, `confidence_dropped_1step_*` on 30m/1h, `hl/hh_chain_broken_30m`. OBV, the
indicator Haci asked about first, appears on a quarter of rows regardless of tier and so carries nothing
the tier uses. `polarity_unavailable_coverage_low` is on 100% of every row (PI-014).

**Reading.** The EXIT tier is a formal restatement of "price broke the pick-night support on the 1h and 4h
charts". That is a fact about the price path, not an independent signal — which is why Q019 matches on
damage before asking whether EXIT tells you anything more.

## 4. Defects, filed

- **PI-014 addendum — HOLD is unreachable.** With `polarity_tier` fixed at WATCH, `overall_tier =
  worst(WATCH, technical)` can never be HOLD. The one tier that would mean "conviction intact" has been
  impossible to print for three and a half months. 0 HOLD rows since 2026-06-01 confirm it.
- **Possible cause link to PI-020.** The polarity coverage ratio is decomposed buy/sell premium over
  contract premium from `uoa_contract_daily`. PI-020 stores zero-trade rows for every contract the
  truncated page did not reach, which empties the decomposition on liquid names. It cannot be the whole
  story (PI-020 predates June; the arm died at the 05-31/06-01 boundary), so it is a lead for the fix
  brief, not a finding.

## 5. What is already registered, and what is new

- **Q019** (locked 2026-09-13, decision 2027-05-24): does selling at the next open after an EXIT beat
  holding to session 10, against a control matched on the damage already done. Two primaries (money in
  ATR, adverse-first rate). Its verdict is the "is it useful" answer. No interim look was registered before
  its lock and DP-58 cannot be added afterwards.
- **H-097 (F6), new** — calibration and reversal: do WATCH-only, EXIT-then-softened and EXIT-persisting
  picks rank monotonically on the forward path, damage-matched; if the tiers do not order the paths, the
  display is noise even if EXIT-vs-hold turns out positive.
- **H-098 (F6, Explorer first), new** — which reason codes and timeframes carry information about the
  forward path beyond the tier, in-sample only, survivors pre-registered with BH correction.
- **H-095 (F1)**, filed earlier today from the SNDK case: re-selection on the night the monitor says EXIT.

## 6. Plain answer to "remove it?"

Not yet, and not on this census. Removing a live surface is a behaviour change that needs a verdict
(rule 10). The desk can say today that (a) half the monitor is dead (PI-014) and HOLD cannot be printed, (b) the other half is a
support-break detector on intraday charts, and (c) whether that detector is worth acting on is Q019. If
Haci wants an earlier read than 2027-05-24, the route is to fix PI-014 and PI-020 first — otherwise any
new question measures a one-armed monitor fed by truncated flow — and register H-097 with the DP-58
interim look at 60 nights.
