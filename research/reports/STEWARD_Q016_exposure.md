# Steward report: Q016 exposure-only count (R1)

Data Steward, 2026-09-13. Routed request R1, `research/questions/Q016_two_sided_beta_atr/DECISIONS.md`
"Routed requests -> data-steward" (verbatim, items 1-7), implementing PREREG.md Section 5's R1 and
Section 2's population/funnel. Frozen data only: `research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json` (`v001_sas_candidates.parquet`, `v001_sas_runs.parquet`,
`p001_daily_split.parquet`, `p001_hourly_raw.parquet`) against `research/data/exclusions_v003.json`.
No live query. No `results/` directory was read.

**Protocol observed (binding):** counts only. No touch, no `TWO_SIDED` flag, no return, no tercile
difference, no picks-minus-control difference. `beta60` and `atr_pct` are computed only from bars
dated `<= t` (features, not outcomes). Forward daily/hourly bars over `t+1..t+60` were read **only
to confirm existence** (row counts), never their `o/h/l/c` values against `U`/`D` -- gradeability is
therefore approximated by *complete forward-bar coverage*, never by PREREG Section 2 clause (b)
("`TWO_SIDED=1` already determined by the bars that exist"), because evaluating clause (b) requires
comparing a forward high/low to a level -- an outcome read this report does not perform. This is a
conservative approximation (it can only over-count "ungradeable", never under-count it) and is
flagged wherever it matters. Nothing below decides P1, P2, the DP-21/DP-24 gates, or the Section 8
clause-7 gate; those are `eval.py`'s calls at the decision pass.

---

## Population and method

Calendar: `p001_daily_split` carries **153 sessions, 2026-02-02..2026-09-10** (SPY-derived calendar
equals the full-universe union of trading dates -- verified). **Last matured pick night** (session
`t+60 <= 2026-09-10`): **2026-06-15** (calendar index 92 of 152), confirming the PREREG Section 5
text exactly. Window start 2026-06-01 = calendar index 82. **Matured population = 11 calendar
sessions, 2026-06-01..2026-06-15.**

`exclusions_v003.json` (`manual_runs` union `non_session_runs` union `uncorroborated_publication_runs`) has
**zero dates inside 2026-06-01..2026-06-15** (its in-window dates -- 2026-06-26, 2026-07-02,
2026-07-06 -- all fall after the maturity cutoff). All 11 matured sessions have a `sas_runs` row;
DP-04 checked mechanically on all 11 (`finished_at` is same trading-day ~21:0x-21:2x UTC in every
case, well before the next session's ~13:30 UTC open) -- **no DP-04 exclusion fires.** No exposure
population is excluded by any night-level rule in the matured window.

Treatment rows: `qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28) on these 11 nights =
**88 rows, exactly 8 per night.** All 88 are `dominant_direction = bullish` (0 bearish candidates
were published on any of these 11 nights -- a fact about this early-June slice, not an exclusion).
`outcome_target_invalid` is non-null on 4 of the 88 (2026-06-01 MSFT; 2026-06-03 AVGO, CRWD;
2026-06-04 AMAT -- the same E9a-correction rows `STEWARD_Q009_exposure.md` R1 and
`STEWARD_Q011_exposure.md` identified) but **Q016's own Section 2 does not name
`outcome_target_invalid` as an exclusion** (unlike Q009/Q011: this question needs no lane-plan
target at all, per PREREG Section 2 "No ladder filter"), so **these 4 rows are correctly retained
in the eligible population** -- flagged here only so the difference from Q011's funnel is not
mistaken for an inconsistency.

---

## (1) The Section 2 funnel, night by night

| Stage | Removed | Remaining |
|---|---|---|
| Published, matured (60-session), non-excluded, DP-04-clean | -- | 88 |
| Symbol with fewer than 60 daily bars dated `<= t` (beta60/ATR14 undefined) | **0** | 88 |
| No `C_t` (no bar at t) | **0** | 88 |
| Ungradeable (approximated as: missing >=1 daily bar over `t+1..t+60`; clause (b) not evaluated -- outcome read, out of scope) | **0** | 88 |
| **ELIGIBLE** | -- | **88** |

**Every one of the 11 matured nights has 0 ungradeable picks, so 0 nights exceed the 25%
ungradeable threshold.** No night is dropped. `n_bars_leq_t` for the 88 eligible symbols ranges
83-93 (well above 60; these are established large/mid-cap names, all listed since well before
2026-01-31). By symbol and month: 0 drops in every month present (June only, in the matured slice).

**Immature nights (context, not part of the eligible population):** 57 more sessions have already
run and published picks (2026-06-16..2026-09-10, non-excluded) but have **not yet matured** -- their
`t+60` window has not closed against the frozen calendar. These are excluded from the population by
construction (PREREG Section 2), never graded as non-touch, and are the source of the "almost
entirely prospective" framing in PREREG Section 5.

---

## (2) Distribution of `k` (eligible picks per night)

**Matured population (11 nights): `k = 8` on every single night** (min = median = max = 8). Zero
nights with `k < 3`.

**Extended proxy, pick-night-only features, 2026-06-01..2026-09-10 (68 elapsed, non-excluded
sessions; no forward bar read -- `beta60`/`atr_pct` need only bars `<= t`):** every one of the 550
published rows on these 68 nights has a computable `beta60` and `atr_pct` (0 dropped for
insufficient prior history). `k` distribution: `k=4`: 1 night, `k=5`: 1, `k=8`: 54, `k=9`: 11,
`k=10`: 1. **Zero nights with `k<3`.** This is a *projection input only* (it cannot itself certify
gradeability, which needs the forward window to mature), reported because items (3)/(7) ask for the
run-rate "over 2026-06-01 onward," not just the matured slice.

---

## (3) Contributing nights per primary endpoint and per tercile arm

Terciles computed exactly per PREREG Section 2 (sort ascending, ties by symbol, `floor(k/3)` per
band). With `k=8` on every matured night, **band sizes are identical on every night for both
variables: L=2, M=4, H=2.**

| Night | k | P1 (beta60) L/M/H | P1 contributing | P2 (atr_pct) L/M/H | P2 contributing |
|---|---|---|---|---|---|
| 2026-06-01 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-02 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-03 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-04 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-05 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-08 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-09 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-10 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-11 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-12 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |
| 2026-06-15 | 8 | 2/4/2 | Yes | 2/4/2 | Yes |

**P1 contributing nights: 11 / 11 matured. P2 contributing nights: 11 / 11 matured.** Per-arm
(band) contributing-night counts (a night carrying >=1 pick in that specific band): **L=11, M=11,
H=11, for both P1 and P2** -- no arm is thin relative to the others; the population is simply tiny
in absolute terms (11 nights total) because of the 60-session maturity requirement, not because any
arm is starved.

Extended proxy (68 nights, pick-night-only features, maturity not yet confirmed): every night has
`k>=4`, so `floor(k/3)>=1` on every night for both variables -- **68/68 nights would be contributing
for both P1 and P2 once matured**, on today's measured conversion rate.

---

## (4) `beta60` and `atr_pct` distributions

**By pick, matured population (n=88):**

| Variable | min | 25% | median | 75% | max | mean |
|---|---|---|---|---|---|---|
| `beta60` | -1.026 | 0.684 | 1.411 | 2.288 | 4.428 | 1.416 |
| `atr_pct` | 0.0139 | 0.0279 | 0.0394 | 0.0535 | 0.0838 | 0.0409 |

**By night** (min / median / max):

| Night | beta60 | atr_pct |
|---|---|---|
| 2026-06-01 | 0.60 / 2.11 / 4.35 | 0.017 / 0.056 / 0.081 |
| 2026-06-02 | -1.03 / 2.05 / 4.43 | 0.025 / 0.042 / 0.059 |
| 2026-06-03 | -0.15 / 1.79 / 3.08 | 0.027 / 0.044 / 0.059 |
| 2026-06-04 | -0.15 / 1.65 / 3.09 | 0.026 / 0.037 / 0.056 |
| 2026-06-05 | -0.03 / 0.79 / 2.35 | 0.018 / 0.038 / 0.052 |
| 2026-06-08 | 0.68 / 1.30 / 2.18 | 0.020 / 0.037 / 0.061 |
| 2026-06-09 | -0.74 / 0.70 / 3.19 | 0.014 / 0.034 / 0.084 |
| 2026-06-10 | 0.04 / 0.82 / 2.73 | 0.020 / 0.045 / 0.072 |
| 2026-06-11 | -0.26 / 0.36 / 3.11 | 0.020 / 0.027 / 0.072 |
| 2026-06-12 | 0.70 / 1.74 / 2.69 | 0.032 / 0.037 / 0.056 |
| 2026-06-15 | 0.80 / 1.59 / 2.82 | 0.021 / 0.046 / 0.073 |

**By month:** June only (11 of 11 matured nights); no other month has a matured night yet.

---

## (5) B2 pool sizes and coverage -- the Section 8 clause-7 / Section 10.8 gate

Same-night non-published `sas_candidates` rows (complement of the DP-28 predicate, dark-lane rows
included) on the 11 matured nights:

| Night | Total candidates | Published | B2 pool (non-published) |
|---|---|---|---|
| 2026-06-01 | 49 | 8 | 41 |
| 2026-06-02 | 45 | 8 | 37 |
| 2026-06-03 | 45 | 8 | 37 |
| 2026-06-04 | 49 | 8 | 41 |
| 2026-06-05 | 52 | 8 | 44 |
| 2026-06-08 | 52 | 8 | 44 |
| 2026-06-09 | 50 | 8 | 42 |
| 2026-06-10 | 50 | 8 | 42 |
| 2026-06-11 | 52 | 8 | 44 |
| 2026-06-12 | 52 | 8 | 44 |
| 2026-06-15 | 50 | 8 | 42 |
| **Total** | **546** | **88** | **458 (201 distinct symbols)** |

**Coverage:**
- **458 / 458 (100%)** of B2 pool rows have a symbol present in `manifest_prices_v001`'s 436-symbol
  daily universe at all. Checked against the *whole* 113-night candidate history (not just this
  window): **431 of 431 distinct `sas_candidates` symbols ever seen are inside the 436-symbol price
  freeze** -- i.e., as measured today, the price freeze's symbol list already happens to be a
  superset of the entire historical candidate universe, published and unpublished. This is better
  coverage than PREREG Section 10.8 assumed was open; it is **not yet a guarantee for future,
  not-yet-run nights** (a genuinely new candidate symbol could still appear after 2026-09-10).
- **458 / 458 (100%)** have `>= 60` prior daily bars dated `<= t`.
- **455 / 458 (99.3%)** have both a `C_t` bar **and** a complete 60-bar forward window. The 3
  shortfalls are all **CTRA**, on 2026-06-04, 2026-06-05 and 2026-06-11: `CTRA`'s daily bars in
  `p001_daily_split` **stop at 2026-05-06** -- there is no CTRA bar of any kind after that date in
  the entire freeze, so it has no `C_t`, no forward bars and no `runup20` on any night in this
  window despite continuing to appear as an unpublished `sas_candidates` row through 2026-06-11.
  This is a **genuine mid-freeze coverage gap for one symbol**, not a boundary/maturity effect --
  flagged for the successor freeze.
- **455 / 458 (99.3%)** are `runup20`-computable (same 3 CTRA rows fail, needing 21 prior closes
  including `C_t`).
- **Eligible picks (of 88) that can be given a full 10-nearest-neighbour match on
  `beta60`/`atr_pct`/`runup20`: 88 / 88.** Every night's fully-covered B2 pool (34-44 candidates
  after dropping the CTRA rows where they occur) exceeds the 10 needed by a wide margin.

**Bottom line on Section 10.8: B2 is computable on the current freeze for the matured population.**
This does not, by itself, resolve Section 8 clause 7 for the *whole* eventual window (2026-06-01
through 2026-11-13 plus the DP-13 extension) -- that depends on the successor freezes
(`manifest_v002` / `manifest_prices_v002`, PREREG Section 5's routed R2) carrying the same coverage
for every future in-window night's candidate symbols, published and unpublished, which cannot be
confirmed before those symbols exist. **What the successor freeze must add / verify (DP-23):**
1. The daily symbol list extended to every candidate symbol on every night from 2026-09-11 through
   the window end (and the DP-13 extension date, if it fires), published and unpublished -- not
   assumed from today's 436-symbol coverage.
2. Hourly bars for all published symbols on those later nights (today's 227-symbol hourly set is
   scoped to the matured/near-matured history only).
3. A **specific data-quality check on CTRA** (and a scan for any other symbol with the same
   truncated-history signature) before the successor freeze is called complete -- one silently
   truncated symbol here cost 3 of 458 B2 rows; at successor-freeze scale this is worth a targeted
   query rather than discovery-by-exposure-count again.

---

## (6) Hourly-bar coverage, `t+1..t+60`, published symbols

**88 / 88 eligible picks (100%) have a regular-session (13:00-19:00 UTC) hourly bar on all 60 of
their `t+1..t+60` forward sessions** -- 0 gaps, checked by symbol-day existence only (no bar value
read). `p001_hourly_raw` is scoped to exactly the 227 published-pick symbols in the freeze, and this
matured window's 8 symbols/night are entirely inside that set on every one of the 60 forward days
each. Ordering rule 2 (PREREG Section 4) can be resolved without falling back to the adverse-first
default for any picked symbol in this window.

---

## (7) Measured contributing-night run-rate

**Measured (matured + fully checked): 11 contributing nights / 11 elapsed sessions
(2026-06-01..2026-06-15) = 1.00 contributing nights per session, both P1 and P2.** This is a
very small sample (n=11) and the rate is at its structural ceiling only because `k=8` on every
single night so far -- one night with `k<3` would immediately show up as a rate below 1.0, and none
has yet occurred.

**Extended proxy (band-formability only, forward-bar existence not required, 2026-06-01..2026-09-10,
68 elapsed non-excluded sessions): 68 / 68 = 1.00** for both endpoints. This is not a "measured"
contributing-night count (those 57 nights beyond 2026-06-15 have not matured and cannot yet be
certified gradeable), but it is a much larger-sample, protocol-compliant check on the same
underlying quantity (whether a night's published slate has `>=1` pick in each of band H and band L),
and it agrees exactly with the small matured sample. Both numbers point to the same rate, **higher
than the PREREG Section 5 draft's deliberately-haircut 0.85/session projection.**

---

## Projected floor dates (mechanical extrapolation only; decides nothing, per DP-43/DP-45)

Using the measured/extended rate of ~1.00 contributing night per elapsed session (business-day
calendar, 2026 remaining NYSE holidays applied: 2026-11-26, 2026-12-25; no holiday intervenes in the
near-term legs of these calculations):

| Floor (rule) | Need | Basis | Raw Nth-night date | +60-session maturity | +1wk margin, next Monday |
|---|---|---|---|---|---|
| 20 contributing nights per cell (sub-cell reporting floor, DP-21) | 9 more beyond the 11 measured | 20th night in the elapsed/pipeline sequence is already known: 2026-06-30 | 2026-06-30 (already occurred) | 2026-09-24 | **2026-10-05** |
| 80 contributing nights per primary endpoint (DP-21) | 12 more new pick nights beyond the 68 already elapsed/piped | 12th new session after 2026-09-10 | 2026-09-28 | 2026-12-22 | **2027-01-04** |
| 30 contributing nights dated after the 2026-09-13 lock (DP-24, the binding gate) | 30 new pick nights after 2026-09-13 | 30th post-lock session | 2026-10-26 | 2027-01-22 | **2027-02-01** |

All three projected dates sit **before** the PREREG's own draft decision date of **Monday
2027-02-22** (built independently, from the fixed window end 2026-11-13 + 60-session maturity + 1
week margin -- not from this rate). At the rate measured here, the locked window and decision date
carry real margin on every floor; nothing in this exposure count indicates the window needs to
extend. Per DP-43/DP-45 this report does not move the date -- it only supplies the numbers the
decision-maker / registrar use to confirm it at `record`, and a rate *below* projection would be the
only thing licensed to push it out.

**60-session maturity, restated:** every floor date above is dominated by the +60-session wait, not
by how fast new contributing nights accrue -- the population's own volume (`k~8/night`, 100%
tercile-formable) means the accrual side of this question is essentially solved; the maturity clock
is the only real constraint, exactly as PREREG Section 5 frames it ("this question is therefore
almost entirely prospective").

---

## Files

- This report: `research/reports/STEWARD_Q016_exposure.md`.
- No new data files were written; all counts were re-derived from
  `research/data/v001_sas_candidates.parquet`, `research/data/v001_sas_runs.parquet`,
  `research/data/p001_daily_split.parquet` and `research/data/p001_hourly_raw.parquet` against
  `research/data/exclusions_v003.json`. No manifest, exclusions or state file was created or
  modified. The controller was not advanced.
