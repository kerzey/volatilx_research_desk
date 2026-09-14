# Steward report: Q017 exposure-only count (R1)

Data Steward, 2026-09-13. Routed request R1, `research/questions/Q017_pin_risk_two_sided/DECISIONS.md`
"Routed requests -> data-steward" (items 1-9, the ninth added under DP-50(a)), implementing
PREREG.md Section 5's R1 and Section 2's population/funnel. Frozen data only:
`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`
(`v001_sas_candidates.parquet`, `v001_sas_runs.parquet`, `v001_gex_symbol.parquet`,
`p001_daily_split.parquet`, `p001_hourly_raw.parquet`) against `research/data/exclusions_v003.json`.
No live query (DP-50(c)). No `results/` directory was read.

**Protocol observed (binding).** Counts only. No touch, no `TWO_SIDED` flag, no return, no arm
difference. Forward daily/hourly bars over `t+1..t+60` were read **only to confirm existence**
(row/date-membership counts), never `o/h/l/c` values against `U`/`D` -- gradeability is therefore
approximated by *complete forward-bar coverage*, the same conservative over-count Q016's R1 used
(it can only over-count "ungradeable", never under-count it). Nothing below decides P1, S2, B3, the
DP-21/DP-24 gates, or the Section 8 clause-7 gate; those are `eval.py`'s calls at the decision pass.
Item (9) is a read-only scan of the platform repository's git history (log/show only), no live DB
read and no code change.

Temporary scripts used to produce these counts live under the session scratchpad, not under
`research/questions/`; no new manifest, exclusions file, or state file was written, and the
controller was not advanced.

---

## Population and method

**Calendar.** `p001_daily_split` carries **153 sessions, 2026-02-02..2026-09-10**. **Last matured
pick night** (session `t+60 <= 2026-09-10`): **2026-06-15** -- identical to `STEWARD_Q016_exposure.md`
(same price freeze, same 60-session clock). **Matured population = 11 sessions, 2026-06-01..2026-06-15.**
**Extended (pick-night-only) population, no forward bar required: 68 elapsed non-excluded sessions,
2026-06-01..2026-09-10** -- identical night count to Q016's R1 (`exclusions_v003.json`
`night_counts_after_exclusions.sealed_from_2026-06-01` = 68).

**Night-level exclusions applied (mechanical, `exclusions_v003.json`, read from JSON, no hard-coded
dates).** In the 2026-06-01..2026-09-10 span: `uncorroborated_publication_runs` removes
**2026-06-26** (11 qualified rows); `manual_runs` removes **2026-07-02** (9 rows) and **2026-07-06**
(9 rows). `non_session_runs`'s one date (2026-04-03) falls before the window. **29 published rows
removed across 3 nights** -- reconciles exactly (11+9+9=29). **DP-04 mechanical check** (`finished_at`
later than the next session's ~13:30 UTC open) on all 68 remaining nights: **zero additional
violations** beyond what `exclusions_v003.json` already carries -- no night is excluded by DP-04
alone.

**Published rows (`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28), post night-exclusion:
550** over the 68-night extended population; **88** of those fall in the 11-night matured population
(identical to Q016's R1 count for the same 11 nights -- expected, since Q017 draws from the same
published-pick population before the GEX filter is applied).

---

## (1) The Section 2 funnel

**GEX-computability filter, applied to all 550 extended-population published rows (first-failing
clause, mutually exclusive, in Section 2's order):**

| Failing clause | Rows (first-fail) | Rows (fails this clause, not mutually exclusive) |
|---|---|---|
| `gex_context` empty or `available` false | 13 | 13 |
| null `spot_close` | 0 | 0 |
| `regime not in {POS_GAMMA, NEG_GAMMA}` | 3 | 3 |
| `quality.contracts_used < 1` | 0 (co-occurs with regime failure above) | 3 |
| empty `top_walls` | 0 (co-occurs with regime failure above) | 3 |
| null `nearest_wall.dist_pct` | 0 (co-occurs with regime failure above) | 3 |
| **NOT_COMPUTABLE total** | **16 / 550 (2.9%)** | -- |
| **GEX-computable** | **534 / 550 (97.1%)** | -- |

The 3 "regime not in {POS_GAMMA, NEG_GAMMA}" rows fail all four of clauses 3-6 simultaneously -- the
exact fingerprint of the degraded-snapshot path (`services/gex.py:676-698`): `regime="UNKNOWN"`,
`top_walls=[]`, `contracts_used=0`, `nearest_wall` absent, all written together when spot cannot be
resolved. **QA check: 0 of 137 `pin_risk=TRUE` rows also fail a computability clause** -- pin risk
never co-occurs with NOT_COMPUTABLE in this data, consistent with `_pin_risk` requiring a non-empty
wall list to return `True` at all.

**Downstream funnel stages, whole 68-night extended population (no forward bar needed):**

| Stage | Removed | Remaining |
|---|---|---|
| GEX-computable, published, post night-exclusion | -- | 534 |
| Symbol with fewer than 60 daily bars dated `<= t` | **0** | 534 |
| No `C_t` (no bar at t) | **0** | 534 |
| **PIN / NOPIN split (computable rows)** | -- | PIN 137, NOPIN 397 |

Zero drops for insufficient prior history **in any month** (June/July/August/September all show 0);
these are established large/mid-cap SAS names with long histories in the freeze.

**Matured-window (11 nights, 88 published, 84 GEX-computable) gradeability check:**
`n_fwd_bars` (count of the 60 forward daily bars `t+1..t+60` that exist) is **60/60 for all 84
GEX-computable matured rows -- 0 ungradeable picks, 0 nights exceed the 25% ungradeable threshold.**
**Immature nights (context, not part of the eligible population): 57** -- the 57 sessions
2026-06-16..2026-09-10 (non-excluded) have published picks but have not yet closed their t+60
window; excluded by construction, never graded as non-touch.

---

## (2) Published picks per night with gex_context, PIN/NOPIN split, and the knife-edge distribution

Every one of the 550 extended-population published rows carries a `gex_context` key at all (the
"empty" branch of clause 1 above is 13 rows where it is present-but-`available=false` or truly
absent -- see item (1)); **534 / 550 (97.1%) are GEX-computable.** Per-night arm sizes range 0-9
NOPIN and 0-6 PIN; **59 of 68 nights carry >=1 PIN pick; all 68 carry >=1 NOPIN pick.**

**`|nearest_wall.dist_pct|` distribution, GEX-computable rows (n=534):**

| stat | min | 5% | 10% | 25% | median | 75% | 90% | 95% | max |
|---|---|---|---|---|---|---|---|---|---|
| value | 0.0000 | 0.0004 | 0.0009 | 0.0023 | 0.0053 | 0.0107 | 0.0185 | 0.0273 | 0.0924 |

**Exactly 137 / 534 (25.7%) sit at or inside the 0.25% (0.0025) knife-edge** -- the count matches
the PIN arm size exactly, confirming pin_risk is mechanically abs(dist_pct) <= 0.0025 with no
slack in this data. Band counts either side of the cut: (0, 0.25%] 137, (0.25%, 0.50%] 122,
(0.50%, 1.00%] 126, (1.00%, 2.00%] 101, (2.00%, 5.00%] 43, (5.00%, max] 5 -- the mass thins
out smoothly, no second cluster near the boundary.

**Direction skew, a finding worth flagging for sub-cell demotion (DECISIONS.md item 7):** of 550
extended-population published rows, only **14 are bearish** (536 bullish); of the **137 PIN rows,
0 are bearish** -- every pinned pick in the entire elapsed history to date is bullish. The
bull/bear sub-cell for the PIN arm has **zero** observations so far; whether this persists is a
question for the decision pass, not this count, but it is flagged now so it is not rediscovered
late.

---

## (3) Contributing nights and the run-rate -- the number that decides lock-or-DEFER

**Measured (matured + fully checked, forward-bar existence confirmed, gradeability applied): 10
contributing nights / 11 matured sessions (2026-06-01..2026-06-15) = 0.909 contributing nights per
session.** Only 2026-06-02 fails to contribute (0 PIN picks that night; NOPIN=7).

**Extended proxy (pick-night-only features, no forward-bar/maturity requirement, 2026-06-01..
2026-09-10, 68 elapsed non-excluded sessions): 59 contributing nights / 68 = 0.868 contributing
nights per session.** Both figures agree closely and both sit far above the PREREG planning rate.

| Rate source | Contributing | Sessions | Rate/session |
|---|---|---|---|
| Matured, fully graded | 10 | 11 | **0.909** |
| Extended proxy, pick-night-only | 59 | 68 | **0.868** |
| PREREG draft planning rate (haircut) | -- | -- | 0.35 |
| DP-43 DEFERRED floor | -- | -- | 0.32 |

**Lock-or-DEFER call (DP-43, DP-45): the measured rate (0.868-0.909) is well above 0.35. Per the
PREREG own rule, a measured rate faster than 0.35 licenses nothing -- it does not pull the
decision date in and does not shorten the window. Q017 locks on the schedule already drafted in
DECISIONS.md item 5/6: window 2026-06-01..2027-04-30, decision date Monday 2027-08-09, DP-13
extension date Monday 2027-09-20 (held in reserve, not expected to be needed). No DEFERRED.**

**Projected floor dates (mechanical extrapolation only, decides nothing per DP-43/DP-45; uses the
0.868/session extended-proxy rate and the PREREG own holiday list):**

| Floor | Need | Basis | Projected pick night | +60-session maturity | +1wk margin, next Monday |
|---|---|---|---|---|---|
| 80 contributing nights (DP-21) | 21 more beyond 59 accrued | ~25 more sessions at 0.868/session | ~2026-10-15 | 2027-01-12 | **2027-01-25** |
| 30 contributing nights post-lock (DP-24) | 30 new, from 2026-09-13 | ~35 sessions at 0.868/session | ~2026-10-30 | 2027-01-28 | **2027-02-08** |

**Both projected floor dates sit roughly six months before the drafted decision date of
2027-08-09** -- the window carries large margin at the measured rate. Per DP-43/DP-45 this report
does not move the date; a rate below projection would be the only thing licensed to push it out,
and nothing here indicates that.

---

## (4) B3 (unpublished-candidate pin contrast) and the B2 pool -- matured window (11 nights)

**All candidate rows (published + unpublished), matured window: 546** (88 published, 458
unpublished) -- identical totals to STEWARD_Q016_exposure.md item (5), as expected (same
underlying sas_candidates population before either question own filter).

**GEX-computable: 538 / 546** (84 published, 454 unpublished) -- the 8 NOT_COMPUTABLE (4 published,
4 unpublished) match item (1) clause counts pro-rated to this sub-window.

**B3 -- unpublished, GEX-computable candidates, PIN/NOPIN split: 79 PIN / 375 NOPIN** (454 total).
Per-night: PIN ranges 4-10, NOPIN ranges 27-40 -- every one of the 11 matured nights carries both
arms in the unpublished pool.

**B2 pool (unpublished, GEX-computable, pin_risk=FALSE): 375 rows, 178 distinct symbols**, all
178 carried in the daily price freeze. Per-night pool size ranges **27-40** (min 27, well above the
10 needed). **372 / 375 (99.2%) have all four match features (log C_t, atr_pct, beta60,
runup20) computable; the 3 shortfalls are CTRA on 2026-06-04/06-05/06-11** (see item 7).

**Full 10-nearest-neighbour match feasibility: 84 / 84 (100%) of matured-window eligible published
picks** have a same-night B2 pool of >=10 fully-featured candidates (every night pool is 27+).

**B2 pool (full-feature, n=372) distributions on the four match features:**

| Variable | min | 5% | 25% | median | 75% | 95% | max |
|---|---|---|---|---|---|---|---|
| log C_t | 2.693 | 3.714 | 4.529 | 5.171 | 5.774 | 7.220 | 8.027 |
| atr_pct | 0.0178 | 0.0227 | 0.0343 | 0.0440 | 0.0588 | 0.0767 | 0.0990 |
| beta60 | -1.918 | -0.390 | 0.550 | 1.214 | 1.876 | 2.859 | 3.618 |
| runup20 | -0.285 | -0.134 | -0.021 | 0.055 | 0.166 | 0.397 | 1.057 |

---

## (5) Agreement rate: context_json.gex_context.pin_risk vs v001_gex_symbol.pin_risk

Same symbol-date, extended population (550 published rows, 2026-06-01..2026-09-10, post
night-exclusion): **538 / 550 (97.8%) have a matching row in gex_symbol_daily** at all (12 have
none). Of the 537 rows where **both** the snapshot and the table carry a defined pin_risk:

**Agreement rate: 527 / 537 = 98.1%. Disagreements: 10** (data-quality figure only -- per PREREG
Section 6, the snapshot decides and the row is flagged, never dropped):

| trading_date | symbol | snapshot pin_risk | table pin_risk | dist_pct |
|---|---|---|---|---|
| 2026-06-03 | AVGO | True | False | 0.0016 |
| 2026-06-04 | LLY | False | True | 0.0042 |
| 2026-06-11 | UNH | True | False | -0.0014 |
| 2026-06-25 | JPM | False | True | 0.0071 |
| 2026-07-07 | LLY | True | False | -0.0005 |
| 2026-08-13 | MSFT | True | False | 0.0012 |
| 2026-08-21 | NVDA | True | False | 0.0013 |
| 2026-09-01 | V | True | False | -0.0005 |
| 2026-09-04 | C | True | False | 0.0020 |
| 2026-09-08 | META | False | True | -0.0057 |

All 10 disagreements sit near the 0.25% knife-edge (abs dist_pct 0.0005-0.0071), consistent with
the table being upserted in place by a later same-day or later-day run (services/gex.py:605-629,
:823-840) that saw a shifted wall list -- exactly the hazard Section 6/10.7 describe, not
evidence of a logic change (see item 9).

---

## (6) quality.contracts_used and nearest-wall spacing -- B2 balance diagnostics, per arm

Matured window (11 nights):

| Arm | n | contracts_used (min/25%/median/75%/max) | abs dist_pct (min/25%/median/75%/max) |
|---|---|---|---|
| PIN picks | 20 | 41 / 45 / 48 / 50 / 50 | 0.0000 / 0.0005 / 0.0013 / 0.0018 / 0.0023 |
| NOPIN picks | 64 | 18 / 40.5 / 47.5 / 50 / 50 | 0.0026 / 0.0042 / 0.0097 / 0.0147 / 0.0637 |
| B2 pool (unpub, non-pinned) | 375 | 1 / 34 / 43 / 49 / 50 | 0.0026 / 0.0061 / 0.0104 / 0.0169 / 0.1393 |

PIN picks carry visibly higher and tighter contracts_used (median 48 vs 43.5/43 for NOPIN/B2) --
consistent with Section 10.13 expectation that pinnable names are denser, more heavily-optioned
chains. This is exactly the diagnostic the SMD > 0.25 rule (DECISIONS.md item 2) is meant to
catch; the actual SMD computation is eval.py job at the decision pass, not this count.

---

## (7) B2 price-freeze coverage and the CTRA-signature scan -- the clause-7 feasibility fact

**Matured-window B2 pool: 178 distinct symbols, 178 / 178 (100%) carried in the daily freeze at
all.** Of the 375 B2 pool rows, **372 / 375 (99.2%) have both >=60 prior daily bars dated <= t and
a complete 60-bar forward window; the 3 shortfalls are all CTRA** (2026-06-04, 2026-06-05,
2026-06-11) -- CTRA daily bars in p001_daily_split **stop at 2026-05-06**, exactly the signature
named in the routed request, and cost 3 of 375 rows here (vs. 3 of 458 in Q016 larger unfiltered
pool -- same root cause, smaller base because Q017 GEX filter already removes some CTRA rows
before this count).

**Targeted CTRA-signature scan, entire frozen candidate history (431 distinct symbols, not just
the matured window):** every one of the 431 symbols ever appearing in sas_candidates is present
in the 436-symbol price freeze (**0 candidate symbols missing from the freeze entirely**). Scanning
for "last price bar precedes last candidate appearance" (the CTRA symptom) across all 431 symbols:
**CTRA is the only match** -- last bar 2026-05-06, last candidate appearance 2026-09-10 (i.e., it is
*still* appearing as an unpublished candidate through the end of the current freeze while carrying
no price data for over four months). **No other symbol shows this signature.**

**Feasibility line for Section 8 clause 7 (matured population): EVALUABLE.** The freeze carries the
unpublished symbols 60 prior and 60 forward bars for 99.2%+ of the B2 pool; the sole shortfall
(CTRA, 3 rows) is dropped and counted per DECISIONS.md item 3 (individual control rows lost to a
truncated history are dropped and counted, never imputed, and do not by themselves make the clause
unevaluable). This does not, by itself, guarantee clause 7 for the *whole* eventual window -- that
depends on manifest_prices_v002 (R2) carrying the same coverage for nights not yet run, published
and unpublished, which cannot be confirmed before those candidates exist. R2 item (4) (a targeted
truncated-history check before the successor freeze is called complete) is the standing safeguard.

---

## (8) Hourly-bar coverage, t+1..t+60, published symbols

**84 / 84 (100%) matured-window eligible picks have a regular-session hourly bar on all 60 of their
t+1..t+60 forward sessions** -- 0 gaps, checked by symbol-day existence only (no bar value read).
p001_hourly_raw 227-symbol scope covers every published symbol in this window on every forward
day. Ordering rule 2 (PREREG Section 4, same-session ordering) can be resolved without the
adverse-first default for any picked symbol here.

---

## (9) DP-50(a) -- commits touching services/gex.py inside the window

A read-only history scan of the platform repository (all branches and remotes; log/show only, no
checkout, no edit) for commits touching services/gex.py: **5 commits touch this file in the
entire repository history, all from 2026-01-12 and 2026-03-25** -- 4b9796a (2026-01-12, "adding
gamme exposure"), c259c36/029011f/f0ee0c8 (2026-01-12, "fixing the unknown issu for gex and
uoa" series), 37fe54f (2026-03-25, "adding gex tool and analysis to super agent"). **Zero commits
fall inside Q017 window (2026-06-01 onward) or even between the manifest platform SHA
(fa70688, 2026-09-05) and today (2026-09-13).**

Read at fa70688 (the manifest platform SHA) to confirm the PREREG own line citations:
_pin_risk (services/gex.py:340-344) still reads threshold_pct=0.0025, returns False on an
empty wall list; the degraded-snapshot path (:676-698) still writes regime="UNKNOWN",
top_walls=[], pin_risk=False when spot cannot be resolved; _upsert_unique with
ON CONFLICT DO UPDATE (:605-629, called at :823-840 inside run_gex_nightly) still upserts
GexSymbolDaily in place. **All PREREG line citations verified accurate as of the freeze SHA; no
repair has shipped since. No DATA_NOTES.md entry is required at this time** -- there is nothing to
record under DP-50(a)/(b) because no in-window commit exists. This must be re-checked at the
decision pass and whenever a successor freeze (R2) is built, since a repair could still land
between now and then.

---

## Files

- This report: research/reports/STEWARD_Q017_exposure.md.
- No new data files were written; all counts were re-derived from
  research/data/v001_sas_candidates.parquet, research/data/v001_sas_runs.parquet,
  research/data/v001_gex_symbol.parquet, research/data/p001_daily_split.parquet,
  research/data/p001_hourly_raw.parquet against research/data/exclusions_v003.json, plus one
  read-only platform-repository git-history scan (log/show only). No manifest, exclusions or state
  file was created or modified. The controller was not advanced (per protocol, this is an exposure
  count, not DATASET_PINNED; Q017 has no manifest of its own to pin beyond the ones already
  cited).
