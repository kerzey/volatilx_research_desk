# Q008 matched-control expected-n - Data Steward count-only report (R1)

Run: 2026-09-13, data-steward, in response to DECISIONS.md Routed requests, data-steward, R1
(research/questions/Q008_fast_start_l4/DECISIONS.md).
Data: frozen parquet only - research/data/manifest_v001.json (as_of 2026-09-10) plus
research/data/manifest_prices_v001.json (as_of 2026-09-10) plus research/data/exclusions_v002.json.
No live queries were run. This is a pre-lock counting exercise, not Q008 eval.py (that is written
once, after lock, by the Researcher, per rule 9). Q008 stays PREREG_DRAFT; nothing here changes its
state.

Disclosure limits observed, literally, per R1: nothing about L4 read or reported beyond what
session-1/session-2 classification requires (E4 = L4 touched within sessions 1-2, needed to define
"eligible F" and "control-F"); nothing beyond session 2 at all; no return; no adverse excursion; no
picks-minus-control difference or rate comparison on the L1 event anywhere in this report. Raw
per-arm counts only.

Distinction from Q002's S1 (stated per R1, so no reader conflates the two): this count classifies
F/S from the pick-night close `C_t` (DP-11), with a night's void rule at `C_t` (`d1 <= 0` /
`d4 <= 0`) as the only "passed already" exclusion. Q002's S1 is the unconditional L1-within-2-sessions
rate measured from the next-session open `O_1`, with `passed_at_entry` picks excluded on the open
basis. Same underlying picks, overlapping nights, different event, different denominator, not
computed here as a rate, and not comparable to Q002's S1.

---

## 0. Population construction (mechanical, per PREREG Section 2 / R1's restatement)

- Window: pick nights 2026-06-01 through the 2-session maturation cutoff in the price freeze.
  With manifest_prices_v001 ending 2026-09-10, the last pick night with both t+1 and t+2 sessions
  present is 2026-09-08 (not the 40-session cutoff, which would leave only ~28 nights - deliberately
  not applied here, per R1).
- Exclusions applied: exclusions_v002.json manual_runs.trading_dates union
  non_session_runs.trading_dates. Of the 10 excluded dates, only 2026-07-02 and 2026-07-06
  fall inside 2026-06-01..2026-09-08.
- Nights in window after exclusions: 67.
- Treatment predicate: qualified IS TRUE AND selected_rank IS NOT NULL (DP-28).
- Control pool, per night: every sas_candidates row on that night not matching the treatment
  predicate (includes qualified = FALSE rows and dark-lane rows), with >= 60 daily bars dated <= t in
  the price freeze.
- Levels: L1 = lane_plans.day_trading.targets[0], L4 = lane_plans.swing_trading.targets[1],
  read from public_payload_json.
- Entry basis: pick-night close C_t (DP-11), not the next-session open.

---

## (a) K1 / K3 contributing-night count

Definition: nights with >= 1 eligible F pick and >= 1 eligible S pick (F = L1 touched in session 1
or 2, not E4; S = L1 not touched in sessions 1-2).

| | count |
|---|---|
| Nights with >= 1 eligible F pick | 64 |
| Nights with >= 1 eligible S pick | 61 |
| K1/K3 contributing nights (both) | 59 |

Floor: >= 80. Current: 59 / 80 (74%).

---

## (b) K2 contributing-night count

Definition: nights with >= 1 eligible F pick whose control-F set is non-empty.

| | count |
|---|---|
| K2 contributing nights (>= 1 F pick, non-empty control-F set) | 64 |
| Of those, nights that also have >= 1 eligible S pick | 59 |

Floor: >= 80. Current: 64 / 80 (80%).

---

## (c) Per-F-pick control-F set-size distribution

291 eligible F picks in window; each matched to its 10 nearest control-pool rows (standardized
beta60/atr_pct/runup20, night median/MAD over pool plus that night's picks, Euclidean distance,
ties by symbol ascending); each matched control classified F/S/E4 from its own bars using the pick's
ATR distances applied to the control's own close.

| statistic | control-F set size (out of 10 matched) |
|---|---|
| Median | 7 |
| 10th percentile | 4 |
| Minimum | 0 |
| Share of F picks with >= 1 control-F | 289 / 291 = 99.3% |
| Count / share with an EMPTY control-F set (Section 10 threat 2 headline) | 2 / 291 = 0.7% |

Full distribution of control-F set size (0-10) across the 291 F picks:

| set size | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| n picks | 2 | 3 | 5 | 16 | 17 | 27 | 52 | 44 | 47 | 43 | 35 |

---

## (d) Monthly run-rate and projections

Contributing-night rate by calendar month (of the 67 window nights):

| month | total nights | K1/K3 contributing | K1/K3 rate | K2 contributing | K2 rate |
|---|---|---|---|---|---|
| 2026-06 | 21 | 16 | 76.2% | 18 | 85.7% |
| 2026-07 | 20 | 18 | 90.0% | 20 | 100.0% |
| 2026-08 | 21 | 21 | 100.0% | 21 | 100.0% |
| 2026-09 (partial, through 09-08) | 5 | 4 | 80.0% | 5 | 100.0% |
| Total | 67 | 59 | 88.1% | 64 | 95.5% |

Note (flagged, not interpreted): the June rate (76%/86%) is the low point; July-September run near or
at 100%. September's figure is 5 nights only. The overall 67-night average (88.1% / 95.5%) is used
below as the projection rate; a rate this close to a ceiling leaves limited room to rise further and
some room to fall if a future month reverts toward June's rate.

Projected date each endpoint reaches 80 contributing nights (NYSE trading-day calendar, applying
the overall 67-night rate forward from the last matured night 2026-09-08; only known remaining NYSE
holiday in range is Thanksgiving 2026-11-26):

| endpoint | contributing nights still needed | trading days needed at overall rate | projected date |
|---|---|---|---|
| K1/K3 (rate 88.1%) | 21 | 24 | approx 2026-10-12 |
| K2 (rate 95.5%) | 16 | 17 | approx 2026-10-01 |

Projected contributing nights falling in 2026-09-16..2026-10-23 and 2026-09-16..2026-11-30
(this is what Section 8 clause 1's "at least 25 contributing nights dated after the lock commit" is
tested against):

| sub-window | NYSE sessions available | projected NEW K1/K3 contributing | projected NEW K2 contributing |
|---|---|---|---|
| 2026-09-16 .. 2026-10-23 | 28 | approx 24.7 | approx 26.7 |
| 2026-09-16 .. 2026-11-30 | 53 | approx 46.7 | approx 50.6 |

Flag: the K1/K3 projection for 2026-09-16..2026-10-23 (approx 24.7) sits just under the item-9
clause's >= 25 threshold at the overall historical rate - it clears only if the post-lock rate holds
at or above the July-September average (>= ~90%) rather than reverting to June's 76%. This is a
number for the waiting-vs-sample trade-off (R-3), not a recommendation.

Cumulative projected totals by each anchor date, at the overall rate (for reference against the
>= 80-contributing-night floor):

| by date | K1/K3 cumulative | K2 cumulative |
|---|---|---|
| 2026-10-23 | approx 83.7 | approx 90.7 |
| 2026-11-30 | approx 105.7 | approx 114.6 |

---

## (e) Population funnel

Starting from published (treatment-predicate) rows in the 67-night window:

| step | rows removed | rows remaining |
|---|---|---|
| Published rows in window (qualified TRUE, selected_rank not null) | - | 543 |
| No-ladder (missing L1 or L4 in lane_plans) | 14 | 529 |
| Non-bull/bear direction (dominant_direction = mixed) | 0 | 529 |
| Missing C_t or 14-bar ATR history | 0 | 529 |
| Void at C_t (d1 <= 0 or d4 <= 0) | 6 | 523 |
| Non-monotone ladder (d4 <= d1) | 1 | 522 |
| Missing session-1/session-2 bars | 0 | 522 |
| Eligible (pre E4/F/S split) | | 522 |
| E4 (L4 touched within sessions 1-2; set aside, counted, not a primary) | 24 | - |
| Eligible F (primaries) | | 291 |
| Eligible S (primaries) | | 207 |

Reference counts alongside the funnel (not part of the treatment population, reported per R1):

| | count |
|---|---|
| Dark-lane rows in window (qualified FALSE, selected_rank not null) - excluded from both treatment and control | 8 |
| Control-pool candidate rows in window (complement of treatment predicate) | 3408 |
| Control-pool rows usable for matching (>= 60 daily bars, features present) | 3391 |

---

## What this decides

Per R1: only the night set and the decision date. Nothing here decides Q008's design, MPEs,
floors, or verdict - those are fixed in DECISIONS.md before this count returns. If Haci's choice in
item 3 (night set vs. speed) needs these numbers, they are attached here for the single R-3 question
that follows, exactly once, per the Q007 pattern. That is a question for the registrar to register and
the controller to route - not a conclusion drawn here.

---

Method note: this is an ad hoc Data Steward script against the frozen parquet, not a checked-in
eval.py. Matching used the PREREG Section 3 B2 construction (standardized beta60/atr_pct/runup20,
night median/MAD over control pool plus that night's picks, 10-nearest by Euclidean distance, ties by
symbol ascending). beta60 computed as rolling 60-session cov(stock return, SPY return)/var(SPY
return); atr_pct = trailing-14-session ATR / close; runup20 = 20-session close-over-close return.
No results/ directory was read for this task.
