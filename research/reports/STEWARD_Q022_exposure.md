# STEWARD_Q022_exposure — sector-cluster nights, counts-only exposure (R1)

**Requested by:** decision-maker, `research/questions/Q022_sector_cluster_nights/DECISIONS.md`,
"data-steward — R1 (counts only) — BLOCKING FOR LOCK" (lines 46-49), plus the coordinator's
addition (contributing-night counts per arm/endpoint, run-rate, projected floor dates).
**Basis:** frozen data only — `research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`
(as_of 2026-09-10, platform SHA `fa70688bc252d14f8d67e371afafc194731c324e`) — plus read-only
`git log`/`git show`/`git diff` in the platform repo. **No live query stands behind any number in
this report** (DP-50(c)). **No outcome of any kind is reported**: no touch, no first-touch date,
no return, no excess, no arm difference, no sector-vs-outcome cross-tab. Forward bars are read
only to confirm a bar **exists** (maturity/gradeability accounting).
**Date:** 2026-09-13. **Author:** data-steward.

---

## Headline

- **Sector-blob pin:** the platform's `data/sp500_sectors.json` has exactly **one** commit in its
  entire history (`4171b1a`, 2026-05-17, "Bear distribution engine - phase 0 infrastructure") and
  has never been touched since. sha256 = `c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201`,
  **byte-identical** at manifest SHA `fa70688` and at `4171b1a` (`git diff fa70688 4171b1a -- data/sp500_sectors.json`
  is empty). The "blob in force at window start" and "the content at `fa70688`" are therefore
  **the same object** — DECISIONS item 4's contingency (use the earlier blob if they differ) does
  not engage, and no differing symbols exist to list.
- **Window start (Decision item 3's rule, measured):** **2026-07-08**, not 2026-07-06 or
  2026-07-07. `1765a6f` (`publication_floor = 80.0`) ships at **2026-07-07 21:43:53 ET**; that
  night's own run (trading_date 2026-07-07) **started at 17:35:09 ET and finished at 17:46:04 ET —
  before the ship**. The first pick night whose run starts after both `5fa3db4` and `1765a6f` is
  **2026-07-08** (run started 17:19:37 ET). See section (a).
- **Arm split (k_t=8 nights, item-3 window 2026-07-08..2026-09-10, 46 elapsed sessions):**
  **CLUSTER 17, DIVERSIFIED 15, UNDETERMINED 0.** Rarer arm (DIVERSIFIED) rate = **0.326/session**;
  eligible (CLUSTER+DIVERSIFIED) rate = **0.696/session**. Both clear the section-5 DEFERRED-gate
  floors (>=0.085 and >=0.30) by a wide margin.
- **Contributing-night rate, matured sub-window (2026-07-08..2026-08-11, 25 elapsed sessions,
  the last pick night whose full t+1..t+20 forward window is covered by manifest_prices_v001):**
  **18 of 18** k_t=8 CLUSTER/DIVERSIFIED nights convert to "contributing" (9 CLUSTER + 9
  DIVERSIFIED) — rate **0.72/session** overall, **0.36/session** per arm on this small sample.
  The larger (not-yet-fully-matured) in-window arm-eligible sample gives a more robust rate of
  **0.696/session** (rarer arm 0.326/session); both are used below.
- **Lock-or-DEFER call: LOCK.** Neither gate line is close to firing. Q022 does **not** go to
  `DEFERRED.md`.
- **Projected floor dates** (measured rate, calendar-aware, holidays included): rarer-arm floor
  (20 nights) ~ **2026-09-24 to 2026-10-01**; post-lock floor (30 nights, lock ~ 2026-09-14) ~
  **2026-11-10**; **80-total-contributing-night floor ~ 2026-12-14 to 2026-12-17** — this is the
  binding constraint. At the drafted (un-extended) window end (2026-11-13 = 92 elapsed sessions
  from the corrected start), the measured rate projects only **~64 of 80** contributing nights —
  **short**. The single DP-13 extension (already drafted to run through 2026-12-29 = 122 elapsed
  sessions) is projected to be **sufficient** (~85 of 80 needed) — no further "move out" beyond
  the already-drafted extension is indicated. See section (h) and "Schedule projection" below.
- **Mapping coverage:** 429 of 431 distinct symbols ever seen in the frozen candidate table are
  in the pinned mapping (**99.5%**); by published row-count, coverage is **99.6%** overall /
  **99.5%** in-window. The only two unmapped symbols in the entire frozen history are **BRK.B**
  and **BF.B** (dual-class tickers; the mapping's bootstrap script appears not to carry the
  period-suffix format). See section (b).

---

## (a) The sector artifact, the ships, and the DP-50(a)/(b) sweep

**`data/sp500_sectors.json` git history (`git log --follow`):** one commit, ever:

```
4171b1a  2026-05-17T16:09:35-04:00  Haci Sahin  "Bear distribution engine - phase 0 infrastructure"
```

The file has not been modified since. Its `_meta`: `"last_synced": "2026-05-17"`,
`"source": "FMP /profile (bootstrap script)"`. Content at platform SHA `fa70688...` (the
manifest's pinned platform SHA) is **byte-identical** to the content at `4171b1a` (sha256
`c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201` both sides; `git diff` empty).
**No differing symbols to list** — the earlier-blob fallback in DECISIONS item 4 is moot. The
mapping holds **2,405** symbol-to-sector-ETF entries across the 11 SPDR sectors (XLB 95, XLC 95,
XLE 120, XLF 435, XLI 313, XLK 327, XLP 106, XLRE 153, XLU 71, XLV 448, XLY 242).

**Ship timestamps (ET, converted from each commit's own recorded offset) vs. `sas_runs.finished_at`
(UTC, converted to ET) on the adjacent nights:**

| commit | ships (ET) | adjacent night | run started (ET) | run finished (ET) | run vs. ship |
|---|---|---|---|---|---|
| `5fa3db4` (ladder monotonic enforcement) | 2026-07-06 15:13:42 | 2026-07-06 | 16:57:48 (late-finishing manual re-run, excluded) | 17:07:22 | after |
| `1765a6f` (publication floor 80.0) | 2026-07-07 21:43:53 | **2026-07-07** | **17:35:09** | **17:46:04** | **before** -- that night's run finished ~4h before the ship landed |
| `1765a6f` | 2026-07-07 21:43:53 | 2026-07-08 | 17:19:37 | 17:28:56 | **after** |

So the first non-excluded pick night whose run begins after the later of the two population-defining
ships is **2026-07-08**, not 2026-07-06 (excluded anyway, manual re-run) and not 2026-07-07 (that
night's run predates the `1765a6f` ship by about four hours). **This resolves DECISIONS item 3:
`window_start = 2026-07-08`.**

`66cb63d` (industry-rotation-bonus removal) ships at **2026-05-14 10:24:45 ET** -- roughly eight
weeks before the window starts. No part of the window predates it. **Section 10.9 is not
triggered; no further start-date shift is indicated.**

**DP-50(a)/(b) sweep since `fa70688`:** the platform's `main` branch HEAD **is** `fa70688` -- zero
commits have merged to `main` since the freeze SHA. One commit exists on an **unmerged** feature
branch (`fix/pi-001-backfill-window-floor`): `2d5776c` (2026-09-13, "PI-001: floor the legacy
outcome backfill window in-process"), touching only the nightly-pipeline entrypoint script and a
new test file. Per its own commit message: "restatement: none... it only widens which rows the
NULL-only backfill revisits" (uoa_symbol_daily.fwd_return_* backfill-window sizing only, not
merged, not run). **It touches no selection or publication path, no lane-plan writer, and rewrites
no historical `sas_candidates` or price row.** No repair affecting Q022's population, arm label,
or lineage has shipped since the freeze.

---

## (b) Mapping coverage

Post night-exclusion (`exclusions_v003.json`, all three lists), full frozen history:

| population | rows | mapped | coverage |
|---|---|---|---|
| published (`qualified IS TRUE AND selected_rank IS NOT NULL`) | 822 | 819 | 99.64% |
| all candidates (published + dark-lane + non-qualified) | 5,928 | 5,913 | 99.75% |
| unpublished pool only | 5,106 | 5,094 | 99.76% |

Restricted to the item-3 window (2026-07-08..2026-09-10):

| population | rows | coverage |
|---|---|---|
| published | 374 | 99.47% |
| unpublished pool | 2,522 | 99.92% |

**Unmapped symbols, full frozen history, with appearance counts:**
- Published: **BRK.B** -- 3 occurrences (2 of them in-window).
- All candidates (published + unpublished): **BRK.B** -- 8; **BF.B** -- 7.

That is the **entire** unmapped list -- no other symbol in 431 distinct candidates fails the pin.
Coverage loss can only thin the DIVERSIFIED arm (section 2.3's disclosed asymmetry) and at this
scale it does essentially nothing: only one k_t=8 night in the whole report period carries
`u_t=1` (see section d); every other night has `u_t=0`.

---

## (c) k_t distribution (published picks per night, post-exclusion)

Report period 2026-06-01..2026-09-10 (71 elapsed sessions, 68 nights with >=1 published pick):

| k_t | nights |
|---|---|
| 4 | 1 |
| 5 | 1 |
| **8** | **54** |
| 9 | 11 |
| 10 | 1 |

`k_t==8`: 54 nights. `k_t<8` (and >0): **2** nights. `k_t>8`: **12** nights -- confirming, as
Q018's 8.07-picks/night headline implied, that both tails exist and are non-trivial (the `k_t>8`
tail alone is 22% of all-picks nights).

Restricted to the item-3 window (2026-07-08..2026-09-10, 46 elapsed sessions, 46 nights with
data -- every session in this sub-window published at least one pick): k_t=4: 1; k_t=5: 1;
**k_t=8: 32**; k_t=9: 11; k_t=10: 1. Same tails, smaller base.

---

## (d) The arm split (the number this question lives on)

Computed on PREREG section 2.3's rule (k_t=8 primary population only; the pinned mapping; ties on
`m_t` broken by ETF ticker ascending). **Zero UNDETERMINED nights anywhere in the report period**
-- the near-total mapping coverage means every k_t=8 night resolves cleanly to CLUSTER or
DIVERSIFIED.

**Full report period 2026-06-01..2026-09-10 (54 k_t=8 nights; pre-window part informational only):**

| | CLUSTER | DIVERSIFIED |
|---|---|---|
| total | 28 | 26 |
| 2026-06 | 11 | 9 |
| 2026-07 | 5 | 8 |
| 2026-08 | 10 | 9 |
| 2026-09 (to 10th) | 2 | 0 |

`m_t` distribution (all 54): 2 to 7, 3 to 19, 4 to 15, 5 to 7, 6 to 3, 7 to 3.
`u_t` distribution: 0 to 52, 1 to 2.
`dominant_sector_t` on CLUSTER nights (all 54): XLK 23, XLF 3, XLV 2.

**In-window sub-period (from the corrected item-3 start, 2026-07-08..2026-09-10; 32 k_t=8
nights of 46 elapsed sessions):**

| | CLUSTER | DIVERSIFIED |
|---|---|---|
| total | **17** | **15** |
| 2026-07 (from 07-08) | 5 | 6 |
| 2026-08 | 10 | 9 |
| 2026-09 (to 10th) | 2 | 0 |

`m_t` (in-window): 2 to 4, 3 to 11, 4 to 11, 5 to 3, 6 to 1, 7 to 2. `u_t` (in-window): 0 to 31,
1 to 1. `dominant_sector_t` on CLUSTER nights (in-window): **XLK 13, XLF 3, XLV 1.**

**Rates (denominator = elapsed sessions, exclusions not pre-removed, per the Q019 Correction 3
convention):** rarer arm (DIVERSIFIED) = 15/46 = **0.326/session**; eligible (CLUSTER+DIVERSIFIED)
= 32/46 = **0.696/session**. Pre-window (2026-06-01..2026-07-07, 22 k_t=8 nights, informational
only): CLUSTER 11 / DIVERSIFIED 11 -- evenly split, consistent with the in-window pattern.

**Item-6 suppression projection:** projecting the in-window `dominant_sector_t` rates forward to
the 80-floor date (~session 112, section h below): XLK ~ 0.283/session x 112 ~ **32** (clears 20
-- the only dominant-sector cell likely to be reportable); XLF ~ 0.065/session x 112 ~ **7** (stays
SUPPRESSED); XLV ~ 0.022/session x 112 ~ **2** (stays SUPPRESSED). Confirms DECISIONS item 6's
expectation: **every non-XLK `dominant_sector_t` cell is projected to stay below the 20-night
floor at the decision date.**

---

## (e) B3 (sector-matched control) feasibility

Per published pick, same-night **unpublished** candidates carrying the **same sector ETF**, with
>=60 prior daily bars in `prices_daily_split` (dated <= t):

| | full report period (n=550 picks) | in-window (n=256 picks) |
|---|---|---|
| B3 pool size, median | 7 | -- |
| share of picks with >=3 B3 controls | 82.2% | 80.9% |
| picks with 0 B3 controls | 15 (2.7%) | -- |
| nights retaining >=50% of picks with >=3 B3 controls | 67 of 68 | 31 of 32 |

By arm (k_t=8 nights only):

| arm | share of picks with >=3 B3 controls | share with 0 B3 controls |
|---|---|---|
| CLUSTER (full / in-window) | 82.6% / 83.1% | 4.9% |
| DIVERSIFIED (full / in-window) | 80.3% / 78.3% | 1.4% |

Nights retaining >=50% of picks, by arm, in-window: CLUSTER 17/17; DIVERSIFIED 14/15 (one night
fails the >=50% share). **B3 feasibility is good but not universal** -- section 8 clause 7's
EVALUABLE test (each arm >=20 contributing nights under B3 pools **and** >=50% of eligible picks
retaining >=3 same-sector controls) is not yet decidable from counts alone at this stage of
accrual, but nothing here suggests it will fail outright; the risk is concentrated in thin sectors
(Utilities, Real Estate, Materials -- the sectors with the smallest S&P representation), consistent
with PREREG threat #8.

---

## (f) B1 control-pool coverage (Q006 section 3 construction) and the CTRA-signature scan

**B1 (unrestricted same-night unpublished pool, >=60 prior bars):** universal. **100% of picks**
(550 of 550 in the report period) retain >=3 valid matched controls; pool sizes range 37-60
(median 53). B1 is not a binding constraint anywhere in this data.

**CTRA-signature scan** (a symbol whose daily bars stop mid-freeze while it keeps appearing as a
candidate, Q016 section 10.8): **found, and it is literally CTRA.** CTRA's last bar in
`prices_daily_split` is **2026-05-06**; it continues to appear as a **non-qualified** candidate
row through **2026-09-10** -- 19 occurrences in the report period, the most recent on 2026-09-10
itself. **CTRA is never published** (`qualified` is `False` on every occurrence checked) so it
never enters the graded-pick funnel, and its missing bar history already excludes it from every
B1/B3 pool count above (it fails the >=60-prior-bar gate on any date after 2026-05-06, by
construction). No other symbol in the report period shows this pattern. Flagged for the record,
not actioned -- this is a read-only observation, not a repair.

---

## (g) Lane availability and the price-scale screen (DATA_NOTES 2026-09-13)

Report period, 550 published picks:

- **No swing-lane target** (`public_payload_json.lane_plans.swing_trading.targets` empty/missing):
  **8 picks (1.45%)** -- ON, WDC, MU, SMCI, MPC, AMT, CAT, MSFT (one occurrence each).
- **Price-scale screen** (`target/C_t` outside [0.5, 2.0] for the swing T1): **19 of 542 checked
  (3.5%)** -- **APH 15**, CRWD 2, KLAC 1, MNST 1. This reproduces the exact DATA_NOTES/Q018
  signature (APH systematic, ~2.0-2.05x) at a slightly larger count than Q018's 495-pick sample
  (14 APH there) because this period runs three weeks longer.
- **`outcome_target_invalid` non-null:** 4 picks.
- **<60 prior daily bars / no `C_t` / no session t+1 open:** 0 picks (none in this population;
  every published pick already clears this gate).

---

## (h) Contributing-night rate on the matured sub-window

**Maturity boundary, confirmed from the price-freeze calendar:** the last pick night whose full
session t+1..t+20 forward window is covered by `manifest_prices_v001` (as_of 2026-09-10) is
**2026-08-11** (session t+21 = 2026-09-10, the freeze's last date; 2026-08-12's t+21 would be
2026-09-11, not in the freeze). This confirms the PREREG's own "~2026-08-12" estimate to within a
session.

**Matured sub-window: 2026-07-08..2026-08-11, 25 elapsed sessions.** Contributing = CLUSTER or
DIVERSIFIED, matured, and >=5 gradeable picks each with a valid control set (B1; gradeable
approximated conservatively here as: has a swing-lane target, passes the price-scale screen, has
no `outcome_target_invalid`, and has >=60 prior bars -- the desk did **not** use section 2.4's "or
the touch is already determined by the bars that exist" shortcut, since that requires reading bar
**values**, which this counts-only request does not permit):

| arm | k_t=8 nights | contributing nights |
|---|---|---|
| CLUSTER | 9 | 9 |
| DIVERSIFIED | 9 | 9 |
| **total** | **18** | **18** |

**100% conversion** from arm-eligible to contributing on this sample -- no night in the matured
sub-window fell short of 5 gradeable picks. Contributing-night rate = 18/25 = **0.72/elapsed
session** (0.36/session per arm on this n=18 sample). Cross-checked against the larger, not-yet-
fully-matured in-window arm-eligible sample (32 k_t=8 nights / 46 sessions = **0.696/session**,
rarer arm 0.326/session) -- the two estimates agree closely, and since conversion-to-contributing
was 100% on the matured slice, the larger sample's rate is the more robust forward projection.

---

## The section-5 DEFERRED-gate call

| gate | threshold | measured (in-window) | measured (matured sub-window) | result |
|---|---|---|---|---|
| rarer arm / elapsed session | >= 0.085 | 0.326 | 0.36 | **clears by 3.8-4.2x** |
| eligible (CLUSTER+DIVERSIFIED) / elapsed session | >= 0.30 | 0.696 | 0.72 | **clears by 2.3-2.4x** |

**Neither line is close to firing. Q022 LOCKS -- it does not go to `research/questions/DEFERRED.md`.**

## Schedule projection (recomputed at the measured rate; moves out only, per DP-43/DP-45)

Using the more conservative (larger-sample) contributing-night rate of **0.696-0.72/session**:

| floor | need | projected session (from 2026-07-08) | projected pick-night date |
|---|---|---|---|
| 20 rarer-arm contributing nights | 20 | ~56-61 | **2026-09-24 to 2026-10-01** |
| 30 contributing nights post-lock (lock ~ 2026-09-14) | 30 | ~43 sessions after lock | **~2026-11-10** |
| **80 total contributing nights** | 80 | **~112-115** | **2026-12-14 to 2026-12-17** |

The **80-total floor is binding** and is the only one in question. At the PREREG's drafted,
un-extended window end (last pick night 2026-11-13 = 92 elapsed sessions from the corrected
2026-07-08 start), the measured rate projects only **~64-66 of the 80** contributing nights
needed -- **short**, so the decision-pass at 2026-12-21 should be expected to find this gate open
and the single DP-13 extension should be expected to fire. The **already-drafted** extension
(window through 2026-12-29 = 122 elapsed sessions, decision 2027-02-08) is projected to be
**sufficient**, landing at roughly **85 of 80** needed -- comfortably inside DP-43's 12-month
ceiling, with margin. **No date beyond the already-drafted extension is indicated by this
measurement**, and per DP-45 nothing here licenses pulling any date in.

---

## Notes on method (for the record)

- Window start (2026-07-08), the arm split, k_t, and sections (b)/(c)/(d)/(g) use
  `exclusions_v003.json` (all three lists) unioned, exactly as `eval.py` will read it -- no
  hard-coded dates.
- "Elapsed session" denominators are calendar trading sessions from the price freeze's own SPY
  calendar (2026-02-02..2026-09-10, 153 sessions), **not** pre-reduced by exclusions, per the
  Q019 Correction 3 convention, so rates are comparable across questions.
- Future-session dates beyond the freeze's 2026-09-10 boundary are projected using a standard
  NYSE business-day calendar with known 2026 H2 / early-2027 holidays (2026-11-26, 2026-12-25,
  2027-01-01, 2027-01-18) removed; this is a calendar projection, not new price data, and is
  offered only to size the schedule, not as a source of any graded number.
- Gradeability for section (h) is deliberately conservative (existence-only, per the coordinator's
  "no outcome of any kind" instruction) and does not use section 2.4's bar-value shortcut; the
  true contributing-night rate at the eventual decision pass may be equal to or higher than
  measured here, never lower for this reason alone.
- Scratch scripts and intermediate CSVs used to build this report live in the session scratchpad,
  not under `research/questions/` or committed to the repo.
