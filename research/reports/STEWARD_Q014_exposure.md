# Steward report: Q014 knowledge-time verification and exposure count (R1)

Data Steward, 2026-09-13. Routed request R1, `research/questions/Q014_uoa_persistence/DECISIONS.md`
"Routed requests -> data-steward -> R1" (verbatim). **Part (a) is BLOCKING for lock; parts (b)-(d)
are the exposure count.** Frozen data only: `research/data/manifest_v001.json`
(`v001_uoa_symbol.parquet`, `v001_sas_candidates.parquet`) and `research/data/manifest_prices_v001.json`
(`p001_daily_split.parquet`), against `research/data/exclusions_v003.json`. No live query. No
`results/` directory exists for Q014 and none was read; PREREG.md and DECISIONS.md were read only.

**Protocol observed (binding): counts only.** Session t+1's official open was read only for pool
construction and the `d_open <= 0` / wrong-side-L3 checks; for sessions >= t+2 only the *existence*
of bars was checked (maturity/coverage), never their values. No touch of any level, no return, no
MAE, no P&L, no picks-minus-control difference and no outcome of any kind was computed. `C_t` is the
`prices_daily_split` regular-session close (never `spot_close`); ATR14 is computed from
`prices_daily_split` bars <= t (never the platform's `atr_pct`, PI-003); `dir` = +1 bullish / -1
bearish from `dominant_direction`.

---

## (a) Knowledge-time verification of `oi_confirm_mult` -- BLOCKING

**Scope:** `uoa_symbol` rows, sessions **2026-05-22 .. 2026-08-12** (window start 2026-06-01 minus 5
sessions, through the last night with a matured 20-session forward window given the price freeze's
last date 2026-09-10) -- 56 sessions, 27,840 rows.

**(i) `oi_confirm_mult` distribution.** Non-null: **1,190 of 27,840 rows (4.27%)**. Confined entirely
to the four documented values, none outside:

| value | count |
|---|---|
| 0.90 | 17 |
| 1.00 | 611 |
| 1.05 | 244 |
| 1.10 | 318 |

**0 rows** carry a value outside {0.90, 1.00, 1.05, 1.10} -- no arithmetic footprint of a second
application surviving in the multiplier column itself (though see the caveat below: the column is
overwritten on every pass, so a second application would not necessarily leave a compound value here
even if it occurred).

**(ii) OI pass ran but multiplier null.** Rows where any of `oi_confirm_score` / `oi_confirm_ratio` /
`oi_confirmed_contracts` is non-null while `oi_confirm_mult` is null: **0 of 1,190 "ran" rows, every
month** (2026-05: 76 ran, 0 null-mult; 06: 456/0; 07: 510/0; 08: 148/0). There is **no** unrecoverable
row in this window -- the ambiguity the PREREG worried about ("rows where `oi_confirm_mult` is null
cannot be told apart from unconfirmed ones") does not manifest as a population of partially-run,
non-recoverable rows; a null multiplier here always means the OI pass did not confirm this row at all.

**(iii) Does `score_day` show the same rewrite?** `score_day` is never touched by
`uoa_screener.py:2236-2239` (only `score_swing`/`score_long` are). Two checks:
- `updated_at - created_at` gap: rows with a non-null `oi_confirm_mult` (median 143.3h) vs. rows
  without (median 120.5h) -- a real but modest difference, and **not usable as a clean signature**:
  `updated_at` is a row-level timestamp bumped by other backfills (e.g. `fwd_return_*` recomputation),
  not exclusively by the OI pass, so this check cannot by itself confirm or rule out a second write to
  `score_day`. Stated as a limitation, not evidence either way.
- Label/score consistency (score below 35 despite a non-NOISE flow-setup label is impossible if the
  label was truly derived from that score): **0 of 13,646** flow-setup-labeled rows have
  `score_day < 35` (the label's own minimum). Same check on the raw, unreconstructed `score_swing`:
  **0 of 16,264**. On raw `score_long`: **1 of 9,720** (a single row where a 0.90 multiplier pushed an
  original score just above 35 to just below it). `score_day` is not distinguishable in this test from
  a bucket confirmed never rewritten -- it shows the same zero-inconsistency signature, and cleaner
  than raw `score_long`'s single borderline case. No sign of the rewrite in `score_day`.

**(iv) Reconstructed `score_b*` vs. frozen `label_b` (full population, not a sample -- stronger than
requested).** `label_b` is written once at 16:05 from the pre-multiplier score and is never rewritten;
a label whose reconstructed score does not reach the label's own 35-floor is evidence of a double
application (reconstruction only undoes one multiplication). Result: **0 of 16,264** `score_swing*`
and **0 of 9,720** `score_long*` reconstructed rows fall below 35 despite carrying a
BULLISH_FLOW_SETUP/BEARISH_FLOW_SETUP label -- including the one raw `score_long` case above, which
resolves cleanly to >= 35 after a single division. **0 label/bias mismatches** in any of the six
checks (raw day/swing/long, reconstructed day/swing/long).

**Arm-assignment impact of the reconstruction.** Reconstruction changes only **3 of 369** eligible
picks' arm assignment (0.8%) vs. taking the frozen values at face value -- all three MID-to-PERSIST
at the margin (APH 2026-06-05, APH 2026-06-08, MO 2026-07-24), each a raw uoa5=3 that reconstructs to
uoa5=2. The correction is small and well-behaved, not a wholesale relabeling.

**Code-level check.** The OI-confirmation entry point (`uoa_screener.py:1996-2024`) guards its own
re-execution against a routine re-run: it returns immediately if that trading date's confirmation
status is already success unless a force flag is passed. A forced manual re-run would bypass this and
multiply a row twice; the frozen data carries **no run-history table** for that pass (same absence as
PI-004/PI-012's `super_agent_select_runs`), so a forced re-run cannot be positively ruled out from the
data alone. No forced re-run is visible in the manifest's code_git_sha/platform_git_sha provenance
either. This is a limitation of what "verified" can mean here, not a finding of a problem.

### Verdict: VERIFIED single application

Weight of evidence -- 0 unrecoverable ("ran but null") rows in any month; 0 multiplier values outside
the documented set; 0 label/score inconsistencies in `score_day`, `score_swing*` or `score_long*`
after reconstruction (vs. 1 borderline case in the raw, unreconstructed `score_long`, which resolves
cleanly under single division); only 3 of 369 arm assignments move under reconstruction, all by one
step at the margin -- together support the multiplier being applied at most once per row and stored
whenever applied. Per DECISIONS.md item 13's pre-committed cascade, branch (i) fires: the Section 2.1
three-bucket reconstruction governs. Q014 is not routed to score_day-only and not routed to
`research/questions/DEFERRED.md`. The one open limitation -- no OI-confirm run-history table, so a
forced re-run cannot be excluded from the data alone -- is disclosed, not resolved; nothing in the
data shows evidence of one.

---

## (b) uoa5 histogram under both definitions, and arm counts

Computed over **369 eligible picks** (funnel in Section (c) below), sessions t-5..t-1 for each pick night.

### Reconstructed (score_b*, three-bucket, Section 2.1 -- the governing definition per (a))

| uoa5 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| count | 31 | 74 | 100 | 78 | 63 | 23 |

Arms: **PERSIST (>=3) = 164 (44.4%)**, MID (1-2) = 174 (47.2%), **NONE (=0) = 31 (8.4%)**.

### score_day only (the item-13 fallback definition -- not the governing one, printed for the
schedule contingency)

| uoa5 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| count | 112 | 59 | 62 | 66 | 47 | 23 |

Arms: PERSIST = 136 (36.9%), MID = 121 (32.8%), NONE = 112 (30.4%). (Not used -- (a) verified the
three-bucket reconstruction; shown only because R1(b) asks for it explicitly.)

**Arm assignments differing between the two definitions** (reconstructed 3-bucket vs. score_day
only): **90 of 369 (24.4%)** -- expected, since score_day alone is a strictly narrower signal than
"any of three buckets." **Arm assignments differing between reconstructed and frozen/raw values**
(the (a) reconstruction-vs-face-value check): **3 of 369 (0.8%)**, detailed in (a) above.

**Note against the PREREG's projection:** EXPLORE_001's in-sample April-May seed projected **32%
PERSIST / 18% NONE** (Section 5). The sealed-window measured split is **44.4% PERSIST / 8.4% NONE** --
PERSIST is thicker than assumed, but **NONE is less than half as thick as projected**, and NONE is
the arm that binds E1's per-night joint requirement (see (c)).

---

## (c) Contributing-night counts, pool sizes and run-rates

### Eligibility funnel (identical construction and result to STEWARD_Q011_exposure.md Section 1
through wrong-side-L3, since Q014 Section 2.2 uses the same publication predicate, lane, level and
clock; Q014 adds the lookback-coverage and forward-maturity steps)

| Stage | Removed | Remaining |
|---|---|---|
| Published, in-window, non-excluded, matured (20-session) | -- | 383 |
| No lane-plan ladder / no L3 (targets[0] null) | 8 | 375 |
| outcome_target_invalid non-null | 4 | 371 |
| Non-bullish/bearish dominant_direction | 0 | 371 |
| No C_t (no bar at t) | 0 | 371 |
| Fewer than 60 daily bars dated <= t (ATR undefined) | 0 | 371 |
| Wrong-side L3 (d_close <= 0) | 2 | 369 |
| No session t+1 bar | 0 | 369 |
| Missing forward bar inside t+1..t+20 (halt/delisting) | 0 | 369 |
| Lookback coverage (a prior session missing from uoa_symbol, or < 200 rows that session) | 0 | 369 |
| **ELIGIBLE (all filters passed)** | -- | **369** |

**Matured nights: 48 (2026-06-01..2026-08-12, non-excluded per exclusions_v003.json, which removes
2026-06-26/07-02/07-06 in-window). Nights with >= 1 eligible pick: 47** (same single zero-eligible
night as Q009/Q011: 2026-06-02, all 8 picks lack a swing lane).

### Pool A (E1's control pool)

Same-night non-published sas_candidates rows, same direction, completeness_score >= 35, on
beta60/atr_pct/runup20 from prices_daily_split bars <= t. **The completeness screen removes 0 rows in
this population** -- every non-published candidate in the window already carries completeness_score
>= 65.4 (min observed), well above the 35 floor; before/after pool size is identical (2,354 = 2,354).
Per-pick same-direction pool size (pre-cap, before selecting the nearest 10): **min 16, median 26, max
30** -- every eligible pick clears the 3-neighbour minimum. **0 of 369 picks (0.0%) fall below the
3-neighbour minimum for Pool A.**

### Pool B (E2's control pool -- the wider UOA-universe baseline)

502 distinct symbols appear in uoa_symbol across the lookback+window range; **431 (85.9%) have daily
bars in the pinned manifest_prices_v001 price freeze; 71 (14.1%) do not** and are dropped from Pool B
eligibility, counted (this is exactly the gap R2(iii)'s widened successor freeze exists to close).
For each of the **164 PERSIST-arm eligible picks**, the same-night, non-published, UOA-universe pool
with uoa5 >= 3 (reconstructed) in the pick's direction and daily bars present: **min 21, median 56,
max 93** -- **0 of 164 PERSIST picks (0.0%) fall below the 3-neighbour minimum for Pool B.** Symbols
that would qualify but lack bars: mean 0.34/pick, max 2/pick, **56 total qualifying-but-dropped
instances across the 164 PERSIST picks** -- Pool B is never actually thin because of this gap in this
window, but it is not zero either. The Pool-B sub-pool restricted to same-night non-published SAS
candidates ("SAS saw it and passed"): min 5, median 10, max 20 per PERSIST pick -- also never below
the 3-neighbour minimum on its own.

### Contributing-night counts (Q014 Section 2.4's own per-endpoint definitions)

| Endpoint | Definition | Contributing nights (of 47 matured-with->=1-eligible) |
|---|---|---|
| **E1** | >= 1 eligible PERSIST pick w/ >= 3 Pool-A controls AND >= 1 eligible NONE pick w/ >= 3 Pool-A controls | **22** |
| **E2** | >= 1 eligible PERSIST pick w/ >= 3 Pool-B controls | **46** |

Since Pool A and Pool B never bind below 3 neighbours anywhere in this window, **E1's count is
entirely gated by the joint presence of >= 1 PERSIST pick and >= 1 NONE pick on the same night** --
and the NONE arm is thin (31 eligible picks total, spread thinly: 25 of 47 nights have **zero**
eligible NONE picks). **E2's count is gated only by >= 1 PERSIST pick existing** (PERSIST is the
largest arm), which nearly every matured night has.

**Per-night detail (Y = contributes to that endpoint):**

| Night | Eligible | PERSIST | NONE | E1 | E2 |
|---|---|---|---|---|---|
| 2026-06-01 | 7 | 6 | 0 | N | Y |
| 2026-06-03 | 6 | 4 | 2 | Y | Y |
| 2026-06-04 | 7 | 4 | 0 | N | Y |
| 2026-06-05 | 7 | 3 | 0 | N | Y |
| 2026-06-08 | 8 | 3 | 1 | Y | Y |
| 2026-06-09 | 8 | 3 | 1 | Y | Y |
| 2026-06-10 | 8 | 4 | 0 | N | Y |
| 2026-06-11 | 8 | 4 | 0 | N | Y |
| 2026-06-12 | 8 | 3 | 1 | Y | Y |
| 2026-06-15 | 8 | 2 | 2 | Y | Y |
| 2026-06-16 | 8 | 4 | 1 | Y | Y |
| 2026-06-17 | 8 | 3 | 0 | N | Y |
| 2026-06-18 | 8 | 5 | 0 | N | Y |
| 2026-06-22 | 8 | 6 | 0 | N | Y |
| 2026-06-23 | 8 | 6 | 0 | N | Y |
| 2026-06-24 | 8 | 4 | 3 | Y | Y |
| 2026-06-25 | 8 | 5 | 0 | N | Y |
| 2026-06-29 | 8 | 3 | 1 | Y | Y |
| 2026-06-30 | 8 | 4 | 0 | N | Y |
| 2026-07-01 | 8 | 3 | 1 | Y | Y |
| 2026-07-07 | 8 | 4 | 1 | Y | Y |
| 2026-07-08 | 8 | 3 | 1 | Y | Y |
| 2026-07-09 | 8 | 4 | 1 | Y | Y |
| 2026-07-10 | 10 | 3 | 3 | Y | Y |
| 2026-07-13 | 8 | 5 | 0 | N | Y |
| 2026-07-14 | 8 | 2 | 0 | N | Y |
| 2026-07-15 | 8 | 5 | 0 | N | Y |
| 2026-07-16 | 8 | 3 | 0 | N | Y |
| 2026-07-17 | 8 | 3 | 0 | N | Y |
| 2026-07-20 | 8 | 4 | 0 | N | Y |
| 2026-07-21 | 9 | 3 | 2 | Y | Y |
| 2026-07-22 | 9 | 4 | 0 | N | Y |
| 2026-07-23 | 8 | 3 | 0 | N | Y |
| 2026-07-24 | 9 | 3 | 2 | Y | Y |
| 2026-07-27 | 8 | 3 | 0 | N | Y |
| 2026-07-28 | 8 | 3 | 1 | Y | Y |
| 2026-07-29 | 8 | 2 | 1 | Y | Y |
| 2026-07-30 | 4 | 1 | 0 | N | Y |
| 2026-07-31 | 5 | 0 | 1 | N | N |
| 2026-08-03 | 8 | 3 | 1 | Y | Y |
| 2026-08-04 | 8 | 2 | 1 | Y | Y |
| 2026-08-05 | 8 | 1 | 1 | Y | Y |
| 2026-08-06 | 8 | 3 | 1 | Y | Y |
| 2026-08-07 | 8 | 3 | 0 | N | Y |
| 2026-08-10 | 8 | 5 | 0 | N | Y |
| 2026-08-11 | 8 | 4 | 1 | Y | Y |
| 2026-08-12 | 8 | 6 | 0 | N | Y |

### Monthly breakdown

| Month | Nights (>=1 eligible) | E1 contributing | E2 contributing |
|---|---|---|---|
| 2026-06 | 19 | 8 | 19 |
| 2026-07 | 20 | 9 | 19 |
| 2026-08 (partial, matured only through 08-12) | 8 | 5 | 8 |
| **Total** | **47** | **22** | **46** |

### Measured run-rate per endpoint

Elapsed sessions 2026-06-01..2026-08-12 inclusive = **51** (same basis as STEWARD_Q009/Q011_exposure.md).

- **E1: 22 / 51 = 0.4314 contributing nights/session** -- well below the PREREG Section 5 projection
  of **0.65/session** (which assumed the EXPLORE_001 in-sample 32%/18% arm split; the measured sealed
  split's thin 8.4% NONE arm is why).
- **E2: 46 / 51 = 0.9020 contributing nights/session** -- above the PREREG's own **0.88/session**
  projection, and, as projected, **not the binding endpoint.**

### Projected floor dates (mechanical extrapolation of the measured June-August rate only; decides
nothing -- every PREREG Section 8 gate fires on eval.py's measured counts at the decision pass)

Using the same two-step construction as STEWARD_Q009/Q011_exposure.md (raw pick-night date via a
business-day calendar, then +20 trading sessions maturity, +7 calendar days freeze margin, next Monday
on or after):

| Floor | Base date | Sessions needed | Raw pick night | + maturity | Decision Monday |
|---|---|---|---|---|---|
| 80 total E1-contributing nights (DP-21) | 2026-08-12 (need 58 more) | 134.5 | 2027-02-17 | 2027-03-17 | **2027-03-29** |
| 30 E1-contributing nights post-lock (DP-24) | 2026-09-13 (lock date) | 69.5 | 2026-12-18 | 2027-01-15 | **2027-01-25** |

**Binding: 2027-03-29** (the later of the two, since both gates must clear on E1's measured rate --
E1 binds, exactly as the PREREG assumed, but at a materially slower rate than assumed). This sits well
inside the **2027-09-13** 12-month ceiling (DP-43): **both floors are projected reachable before the
ceiling**, so Q014 is not headed for DEFERRED on this measured rate alone -- but the projected initial
decision date (**2027-03-29**) is **more than two months later** than the PREREG's drafted floor
(Monday 2027-01-11). Per DECISIONS.md item 5 / Q011 item 8 precedent, **a measured rate may push every
drafted date out, never pull one in** -- this pushes it out. E2's own two floors, computed the same
way at its 0.9020/session rate, land materially earlier and are not binding.

**Is Pool B thick enough for E2 to carry a verdict?** **Yes, comfortably** -- 46 of 47 matured nights
already contribute (98%), the per-pick Pool-B size never drops below 21, and the run-rate (0.90/session)
clears both of E2's own floors well before E1's do. E2 is not what determines Q014's timeline; E1 is.

---

## (d) UOA universe coverage

Per-session uoa_symbol row counts, 2026-05-22 (lookback start) .. 2026-08-12 (window end), 56
sessions: **min 489, median 497, mean 497.1, max 501. 0 of 56 sessions fall below the 200-row
threshold** that would make a pick's lookback unmeasurable (Section 2.4). By month: 2026-05 (2
sessions in range) min/max 496/497; 06 (21 sessions) 495-501; 07 (22) 489-500; 08 (11, partial)
497-499. Universe turnover between adjacent sessions: median 1 symbol entering, 0 leaving (mean
1.33 / 1.27); max 10 entering / 9 leaving on any single adjacent-session pair. The universe is stable
session-to-session; no session-level coverage gap exists anywhere in this window.

---

## Files

- This report: research/reports/STEWARD_Q014_exposure.md.
- No new data files were written; all counts were re-derived from research/data/v001_uoa_symbol.parquet,
  research/data/v001_sas_candidates.parquet and research/data/p001_daily_split.parquet against
  research/data/exclusions_v003.json. No manifest, exclusions or state file was created or modified.
  The controller was not advanced (per protocol, this report does not advance Q014; @registrar apply
  Q014 and the controller's PREREG_LOCKED transition are separate steps, gated on this report's
  part (a)).
