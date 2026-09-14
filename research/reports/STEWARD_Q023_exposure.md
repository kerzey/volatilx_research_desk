# STEWARD_Q023_exposure.md — R1 (counts only), Q023 band_80_90_strongly_bullish

**Scope:** Data Steward, routed request R1 (research/questions/Q023_band_80_90_strongly_bullish/DECISIONS.md
"data-steward — R1 (counts only) — BLOCKING FOR LOCK", lines 56-59) plus the Coordinator's exposure-count
addendum. Counts only, no outcome of any kind. Frozen data only: `research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json` against `research/data/exclusions_v003.json`, plus read-only
git log/show against the platform repository at the manifest's pinned SHA (DP-50(c) — never a live
query). Forward bars are read **only** to prove a bar exists (gradeability accounting, §2) — no value
from any forward bar is read.

**Population:** published picks (`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28), `80 <= overall_score < 90`,
pick nights **2026-06-09..2026-09-10** (the whole point-in-time-legal span of `market_regime_daily`,
per the Coordinator's instruction — wider than the PREREG draft's 2026-06-09..2026-08-12), with
`exclusions_v003.json` nights removed and DP-04 late-`finished_at` nights removed.

**Elapsed sessions in window (denominator for every rate, exclusions NOT pre-removed):** N = **65**
(2026-06-09..2026-09-10, cross-validated against both `sas_runs` and SPY's own daily-bar calendar —
they agree exactly).

**Nights excluded from the population** (union of `exclusions_v003.json` in-window + DP-04, 3 nights):
`2026-06-26` (uncorroborated_publication_runs), `2026-07-02` (manual_runs), `2026-07-06` (manual_runs;
this night also independently fails the market_regime legality timestamp test, §4, below — two
separate reasons converge on the same night). No other in-window night trips DP-04.

---

## 1. Headline call

**LOCK proceeds — not DEFERRED — on the sealed-panel measurement.** All three DEFERRED-gate limbs
(DECISIONS item 11) clear comfortably on the 2026-06-09..2026-09-10 measured rate:

| limb | measured (sealed panel) | floor | clears? |
|---|---|---|---|
| contributing nights / elapsed session | **0.9538** (62/65) | >= 0.43 | **YES** |
| rarer-arm (NOTSTRONG) nights / elapsed session | **0.2000** (13/65) | >= 0.11 | **YES** |
| rarer-arm (NOTSTRONG) episodes / elapsed session | **0.0615** (4/65) | >= 0.027 | **YES** |

**But flag this prominently, because it bears directly on whether the prospective window actually
delivers what the sealed panel promises:** the NOTSTRONG arm has not produced a single contributing
night in the **trailing 30 sessions** (2026-07-30..2026-09-10) — one uninterrupted `strongly_bullish`
episode covers the entire second half of the sealed panel (August: 21 STRONG / 0 NOTSTRONG nights;
September to the 10th: 7 STRONG / 0 NOTSTRONG). The whole-period average (0.20/session) clears the
0.11 floor; the **recent trend is 0.00/session**, which does not. This is a fact about the tape, not
an interpretation — reported so the coordinator can weigh it against the ceiling arithmetic below.
At the **drafted** window end (96 sessions, 2027-01-29), the rarer-arm floor is a near-miss on the
whole-period rate alone: expected NOTSTRONG nights = 0.20 x 96 = **19.2 of the 20 needed** — i.e. on
the measured historical rate, the single DP-13 extension is more likely than not to fire, before even
accounting for the trailing-30-session rate of zero.

**DP-50(a) commit sweep since manifest SHA `fa70688`: NONE.** Exactly one platform commit exists between
`fa70688` (the manifest's `platform_git_sha`) and current HEAD — `2d5776c` ("PI-001: floor the legacy
outcome backfill window in-process"), which touches only the nightly-pipeline entrypoint's backfill-window
clamp (`uoa_symbol_daily` maturation, an unrelated table) plus one new pin test. It does **not** touch
`services/market_regime/scorer.py`, `services/sas_conviction_card.py`, the SAS trading-guide generator,
`services/super_agent_select_models.py`, or `services/super_agent_select_scoring.py`. No hysteresis
constant, secular-risk threshold, `BAND_EXITS`/scale-out fraction, weight, timeframe multiplier,
`publication_floor`, or `bear_publish_threshold` changed. No `regime_version` beyond `v1.2` exists
anywhere in the frozen history (`{'v1','v1.1','v1.2'}` only, in-window: `v1.2` on all 65 sessions).
**No `DATA_NOTES.md` entry is needed; DECISIONS item 12's window-split trigger does not fire.**

---

## 2. The §2 funnel (population -> eligible), by month and total

Picks (rows) surviving each step:

| step | 2026-06 | 2026-07 | 2026-08 | 2026-09 | total |
|---|---|---|---|---|---|
| 0 published 80-90 (post night-excl) | 103 | 153 | 167 | 59 | **482** |
| 1 six-level ladder present | 103 | 149 | 163 | 59 | **474** (-8) |
| 2 right-side + monotone ladder | 78 | 146 | 163 | 59 | **446** (-28) |
| 3 outcome_target_invalid null | 78 | 146 | 163 | 59 | **446** (-0) |
| 4 split-scale payload screen pass | 72 | 144 | 158 | 59 | **433** (-13) |
| 5 >= 60 prior daily bars | 72 | 144 | 158 | 59 | **433** (-0) |

Nights (>= 1 surviving pick) surviving each step — every one of the 62 non-excluded nights retains
at least one eligible pick all the way through step 5 (14 Jun + 20 Jul + 21 Aug + 7 Sep = 62), for
every step 0 through 5.

**Eligible-night rate under this funnel: 62/65 elapsed sessions = 0.9538** — higher than the 0.92
borrowed from STEWARD_Q015_exposure.md (different population window and a different, narrower
funnel), and well clear of the 0.85 planning haircut.

**Step 2 detail — wrong-side / non-monotone rate by month** (monotonicity is checked *non-strictly*,
i.e. adjacent flattened levels may tie; the platform's cross-lane ladder-monotonicity fix, commit
`5fa3db4`, 2026-07-06, resolves cross-lane order by clamping, which produces exact ties at lane
boundaries, not strict inequality — a strict test overcounts violations by roughly 4x and was
rejected after inspection of the raw payloads): **2026-06: 24.3%**, **2026-07: 2.0%**,
**2026-08: 0.0%**, **2026-09: 0.0%**. This matches DATA_NOTES's independently-measured pre-fix/post-fix
split (25.71% before 2026-07-06, 0.00% after) — the fix's ship date sits inside June-July of this
population, consistent with the platform commit log.

**Step 3 — outcome_target_invalid:** 0 non-null in this population, any month.

**Step 4 — split-scale payload screen fails:** 13 total (Jun 6, Jul 2, Aug 5, Sep 0) — `entry/C_t`
outside [0.85, 1.15] or a flattened level beyond 20 ATR from `C_t`.

**Step 5 — < 60 prior daily bars:** 0 in this population (every symbol published in the 80-90 band
had a sufficient price history in `manifest_prices_v001`).

**t+60 maturity / gradeability haircut** (separate from the rate above, per instruction — computed
only on the sub-window that has actually matured against the freeze's own end date, 2026-09-10):
only **5 nights (2026-06-09..2026-06-15, 27 eligible picks)** have a full t+1..t+60 forward window
inside `manifest_prices_v001`. Of those 27, **0 (0.0%) fail gradeability** (no missing bar inside
t+1..t+60 for any of them). Small sample — this is a haircut sanity check, not a claim about the
whole window, which is a future prospective window whose own successor freeze will supply maturity.

---

## 3. The arm split and the episodes

Night counts by `market_regime` label, `v1.2` rows only, legal nights, in-window (64 of 65 sessions
carry a legal label — see §4):

| month | `bullish` | `strongly_bullish` |
|---|---|---|
| 2026-06 | 7 | 8 |
| 2026-07 | 7 | 15 |
| 2026-08 | 0 | 21 |
| 2026-09 | 0 | 7 |
| **total** | **14** | **51** |

No other label appears at all in-window: 0 `neutral`, 0 `bearish`, 0 `risk_off`.

`regime_phase` (legal nights): `impulse_up` 56 (14 NOTSTRONG + 42 STRONG), `pullback_in_bull` 8
(all STRONG). **The NOTSTRONG arm is 100% `bullish`-labelled `impulse_up`** — no `neutral`, `bearish`
or `risk_off` night occurs anywhere in the sealed panel, so §8 clause 8's 60%-composition guard is
met trivially (100% >> 60%) and the pooled/`bullish`-only distinction is moot on this data.

**Contributing nights** (legal label + >= 1 eligible pick, post-funnel + not excluded) = **62 total**:
**STRONG 49, NOTSTRONG 13.** Per elapsed session (N=65): total **0.9538**, STRONG **0.7538**,
NOTSTRONG **0.2000**.

**Episodes** (label-series definition, DECISIONS item 4 / Correction #2: a maximal run of consecutive
*sessions* carrying the same legal arm label; a no-legal-label session does not break a run; only the
opposite arm's legal label ends one; counts toward the gate only if it contains >= 1 contributing
night):

| arm | episode (start .. end) | sessions | contributing nights |
|---|---|---|---|
| NOTSTRONG | 2026-06-09 .. 2026-06-11 | 3 | 3 |
| STRONG | 2026-06-12 .. 2026-06-22 | 6 | 6 |
| NOTSTRONG | 2026-06-23 .. 2026-06-26 | 4 | 3 |
| STRONG | 2026-06-29 .. 2026-07-02 | 4 | 3 |
| (no legal label) | 2026-07-06 | 1 | 0 |
| STRONG | 2026-07-07 .. 2026-07-16 | 8 | 8 |
| NOTSTRONG | 2026-07-17 .. 2026-07-20 | 2 | 2 |
| STRONG | 2026-07-21 .. 2026-07-22 | 2 | 2 |
| NOTSTRONG | 2026-07-23 .. 2026-07-29 | 5 | 5 |
| STRONG | 2026-07-30 .. 2026-09-10 | 30 | 30 |

**STRONG: 5 episodes, all gate-counting**, length distribution (sessions) [6, 4, 8, 2, 30],
0.0769/elapsed session. **NOTSTRONG: 4 episodes, all gate-counting**, length distribution
[3, 4, 2, 5], **0.0615/elapsed session** (clears the 0.027 limb by more than 2x). The single
30-session STRONG episode running from 2026-07-30 to the freeze date is what drives the trailing-30
zero noted in §1 — the tape has been in one uninterrupted `strongly_bullish` stretch for the whole
second half of the sealed panel.

---

## 4. Legality audit (every in-window night, `created_at` vs `trading_date` and vs `sas_runs.finished_at`)

Tightened per DECISIONS item 1 / Correction #3: a night's `market_regime_daily` row is legal only if
`regime_version='v1.2'`, `market_regime <> 'unknown'`, `data_quality <> 'insufficient'`, `created_at`
falls on the row's own `trading_date`, **and** `created_at <= that night's own sas_runs.finished_at`.

**Result: 1 failure out of 65 in-window sessions.** The sole failure is `2026-07-06` — `created_at`
2026-07-07 14:23:02 UTC, i.e. written on the next calendar day, so it fails the "own trading_date"
limb independently of the finished_at comparison. This is exactly the FREEZE_v001 §7 late-write
exception, and the night is already excluded from the population via `exclusions_v003.manual_runs`.
`2026-06-26` was NOT a legality failure (it has a normal same-evening regime write; its exclusion is
for an unrelated reason, the uncorroborated-publication signature). **0 nights** carry `unknown`,
`insufficient`, or no `v1.2` row at all. No other night fails either limb of the timestamp test.

---

## 5. Two-label agreement rate (`trading_date = t` vs `effective_for_trading_date = t`)

**64 of 64 legal nights have both labels available. Agreement rate: 89.06% (57/64); disagreement
10.94% (7/64)** — below DECISIONS item 1's now-moot 15% reference point (the sensitivity binds
unconditionally regardless of this rate). All 7 disagreements sit exactly at arm-transition
boundaries (the night a run flips, the strictly-prior label still carries yesterday's regime):

| trading_date | `trading_date=t` label | `effective_for_trading_date=t` label |
|---|---|---|
| 2026-06-12 | strongly_bullish | bullish |
| 2026-06-23 | bullish | strongly_bullish |
| 2026-06-29 | strongly_bullish | bullish |
| 2026-07-17 | bullish | strongly_bullish |
| 2026-07-21 | strongly_bullish | bullish |
| 2026-07-23 | bullish | strongly_bullish |
| 2026-07-30 | strongly_bullish | bullish |

---

## 6. Same-night control-pool sizes (Q006 §3 construction, approximated for a counts-only check)

Approximation used: same-night dark-lane (`qualified` false or `selected_rank` null) `sas_candidates`
rows with >= 60 prior daily bars in `manifest_prices_v001` (the `beta60`/`atr_pct`/`runup20`
computability screen; nearest-neighbour distance ranking itself is not run here — this is a
counts-only exposure check, not the eval). Over the 62 eligible nights: **mean 51.8, median 54,
min 39, max 60.** **100% of nights have >= 3 valid controls; 100% have >= 10.** Consistent with
STEWARD_Q015_exposure.md §8's median 54 / p10 42 / min 37 on an overlapping population.

**CTRA truncated-history signature confirmed:** CTRA's last available daily bar in
`manifest_prices_v001` is **2026-05-06**, yet CTRA still appears as a `sas_candidates` row as late
as **2026-09-10** — i.e. it keeps being scored/appearing as a candidate for four months after its
own price history stops in this freeze. No other symbol in the in-window candidate universe shows
the same signature.

---

## 7. B3 feasibility (`projection_pick_bullish_daily` coverage)

62 nights, exactly **15 symbol-rows per night, 930 symbol-nights total** in-window. **98.17%
(913/930) already carry >= 60 prior daily bars in the existing `manifest_prices_v001`** — a freeze
that was never deliberately scoped to include every projection-bullish symbol. This clears the
>= 80% coverage gate with a wide margin before the successor freeze even adds the explicit
projection-bullish symbol scope that PREREG §5.3 R2 / DECISIONS item 14 requires; B3 is very likely
computable once the successor freeze is built as specified.

---

## 8. Projected floor dates (prospective window from 2026-09-14), and the binding floor

Using the sealed-panel measured rates as the run-rate (no haircut applied here — a haircut is a
policy choice for the registrar/decision-maker, not a Steward computation), and the calendar/holiday
list from DECISIONS item 14 (R2): 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15,
2027-03-26, 2027-05-31, 2027-06-18, 2027-07-05.

| floor | measured rate | sessions needed | projected date |
|---|---|---|---|
| A: 80 contributing nights (both arms) | 0.9538/session | 84 | **2027-01-12** |
| B: 20 rarer-arm (NOTSTRONG) nights | 0.2000/session | 100 | **2027-02-04** |
| C: 30 post-lock contributing nights (DP-24) | 0.9538/session | 32 | **2026-10-27** |
| D: 5 rarer-arm episodes | 0.0615/session | 82 | **2027-01-08** |

**Binding floor (latest of the four): B, at 100 sessions -> window end 2027-02-04.** Carrying that
window end forward through +60 sessions maturity and the +1-week freeze margin, rounded to the first
Monday on/after, lands on **2027-05-10** — coincidentally the same Monday as the PREREG's own drafted
decision date, because the rounding absorbs the roughly 4-session gap between the drafted window end
(2027-01-29, 96 sessions) and the measured-rate binding floor (2027-02-04, 100 sessions). That
coincidence should not be read as confirmation that the drafted schedule is safe: §1 already shows
the whole-period rate leaves floor B a hair short (19.2 of 20) at the drafted 96-session mark, and
the trailing-30-session rate is zero, not 0.20. **7.85 months from the 2026-09-13 lock — inside
DP-43's 12-month ceiling either way.**

---

## 9. What this does and does not decide

This is a counts-only exposure measurement. It does not compute, and this report does not state, any
touch rate, return, excursion, plan result, or regime-vs-outcome relationship. The lock-or-DEFER call
in §1 is mechanical (three limbs against the measured sealed-panel rate); whether Q023 actually locks,
and on what final dates, is settled by the registrar/decision-maker at `record` against the
*prospective* window's own measured counts, not this sealed panel — this report only supplies the
counts DECISIONS item 13 named as blocking.
