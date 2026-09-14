# STEWARD_Q025_exposure — exposure-attribution counts-only report (R1)

**Requested by:** decision-maker, `research/questions/Q025_exposure_attribution/DECISIONS.md`,
"data-steward — R1 (counts only) — BLOCKING FOR LOCK" (item 16, routed request, items i-viii).
**Question:** Q025 (H-068, exposure attribution), registered under this filename after renumbering
from the draft's `Q024` (see DECISIONS item 1). `Q024_sas_vs_simple_benchmarks` is a different
question (H-067) and is not touched by this report or by the freeze work behind it.
**Basis:** frozen data only — `research/data/manifest_v001.json` (frozen_at 2026-09-10T22:31:32Z,
platform SHA fa70688bc252d14f8d67e371afafc194731c324e) + `research/data/manifest_prices_v001.json`
— plus read-only git log/git show/git diff in the platform repo. **No live query stands
behind any number in this report** (DP-50(c)). **No outcome of any kind is reported:** no touch,
no first-touch date, no return, no excess, no cross-tab of any exposure against any outcome.
Forward bars are read only to confirm a bar exists (maturity/gradeability accounting), never
for a value. **No post-match balance of any kind is reported** — no SMDs, no matched-pair
comparisons; that is Section 8 clause 7 and belongs to eval.py at the decision pass (DP-45; Q022
DECISIONS number 16; this DECISIONS number 9 and the routed-request prohibition, verbatim).
**Date:** 2026-09-13. **Author:** data-steward.

---

## Headline

- The gate does not clear. Measured E2 (binding) contributing-night rate = 0.000 per elapsed
  session (0 of 25 matured nights; 0 of 46 in-window elapsed sessions on the quasi-eligible
  proxy). E1's rate is identical, 0.000, for the same reason: E2's population is a subset of
  E1's and E1 itself never reaches 3 qualifying picks on a single night either. This is far
  below the 0.35-per-session floor PREREG Section 5 sets for locking. Per Section 5 and DECISIONS
  item 16, the call this measurement decides is DEFERRED, not a resize. No date is projected
  inward; per DP-45 nothing here licenses moving any date in, and none is licensed to move out
  either, because there is no positive rate to size a window on.
- Why it collapses to zero, mechanically, not as an artifact: the hard sector block already
  shrinks the same-night control pool to a median of roughly 5-7 names (Q022 Section e precedent,
  reconfirmed here); on top of that pool, the five-feature caliper (beta60, atr_pct, mom20, mom60,
  size, each at 1.5 standardised units) passes on 7.6% of matured published picks (15 of 197) —
  and because those 15 survivors are scattered thinly across 46 nights (max simultaneous survivors
  on any single night: 2, never 3), zero nights ever clear the "3-or-more picks with a valid B1
  set" contributing-night bar. The by-sector drop share (fewer than 3 controls) ranges from 85.7%
  (XLF, XLI) to 100% (XLB, XLC, XLRE, XLU, XLY) — see section (d).
- B4 (the Q006 construction) is not the constraint. On the same matured population, B4 is valid
  (10 of 10 nearest, no caliper) for 100% of picks (197 of 197) — reproducing Q022 Section f's
  "the unrestricted construction is universal" finding under this question's own window. The
  entire shortfall is B1's hard-sector-plus-caliper construction, exactly the construction Section
  11 item 3 chose knowing it was the stricter of two options.
- Sector artifact verified. data/sp500_sectors.json sha256 = c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201, confirmed by direct hash of the git blob at platform SHA fa70688 (the manifest's pinned SHA) — matches the pin in the PREREG header and DECISIONS item 10 exactly. (A naive hash of the working-tree checkout on this Windows sandbox reads differently, fc13551c..., because of CRLF line-ending translation on checkout — the git blob content, which is what was pinned and hashed originally, is unaffected and byte-identical across fa70688, 4171b1a and the current platform HEAD d19c9a9; git diff between all three on this file is empty.)
- DP-50(a)/(b) sweep: clean. Platform main HEAD is now d19c9a9, four commits ahead of the freeze
  SHA fa70688 (2d5776c, a merge commit, 22a2e1b, another merge commit). None touches the
  selection or publication path, the lane-plan writer, which picks are published, or rewrites any
  historical sas_candidates or price row — see section (a).
- Feature/sector coverage is not the bottleneck: 100% of published picks and 99.4-99.9% of the
  unpublished pool have 60 or more prior bars, computable beta60/mom20/mom60/adv20, and a sector
  mapping (BRK.B is the only unmapped symbol in this window). See section (c).
- Sub-cell enumeration: every one of the 54 direction/band/lane/sector cells is projected below
  the 20-contributing-night floor — trivially, since the endpoint-level contributing-night count
  is 0 everywhere and the richest single cell (bullish, 80-85, short, XLK, 87 picks) never
  produces more than 0 B1-valid picks contributing to a night that also has 2 more. All 54 cells
  are flagged SUPPRESSED for the item-13 suppression list. See section (f).

---

## (a) The sector artifact and the DP-50(a)/(b) sweep

Sector blob. data/sp500_sectors.json has exactly one commit in its history (4171b1a,
2026-05-17), confirmed again here (git log --follow). Direct sha256 of the git blob content at
fa70688:data/sp500_sectors.json (piped straight from git show, not from a checked-out file, to
avoid a Windows CRLF artifact — see Headline) = c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201, matching the PREREG header and DECISIONS item 10 verbatim. git diff fa70688
4171b1a and git diff fa70688 (current HEAD d19c9a9), both restricted to this file, are empty.
No rule-14 exception is engaged; DECISIONS item 10 stands unchanged.

DP-50(a)/(b) sweep, carried forward from fa70688 (2026-09-05 12:04:10 CDT), clean at
2026-09-13. Platform main has advanced 4 commits since the freeze:

| commit | date (author tz) | touches | selection/publication/lane-plan/historical-rewrite? |
|---|---|---|---|
| 2d5776c | 2026-09-13 17:37:25 -0500 | the nightly-pipeline entrypoint script (floors/caps the legacy uoa_symbol_daily.fwd_return_* backfill window in-process), plus 1 new test | No. Backfill-window sizing only for a table this question already bans outright (uoa_symbol_daily, FREEZE_v001 Section 5, PI-007). Touches no sas_candidates row, no lane-plan writer, no price row. Commit's own text: "Restatement: none, it only widens which rows the NULL-only backfill revisits." |
| 4775e49 | merge of 2d5776c into main | merge commit | merge only |
| 22a2e1b | 2026-09-13 20:55:42 -0500 | app.py (2 lines, router registration), a new admin router, a new import-pure speed-to-target service, a stub data reference file, docs | No. EN-002, an internal-only, flag-off (SAS_SPEED_TO_TARGET_INTERNAL, default OFF) admin card; author's own inertness claim: "every subscriber-facing service, router and template is byte-identical to 2d5776c." Read-only, derived-only; no migration, no write path, no nightly job. Control arm is stubbed (AWAITING_Q002) specifically because it would otherwise leak a Q002 primary — orthogonal to Q025. |
| d19c9a9 | merge of 22a2e1b into main | merge commit | merge only |

No repair affecting Q025's population, sector label, exposure features, or lineage has shipped
since the freeze. Both dated commits post-date the freeze (fa70688, 2026-09-05) and the last
in-window pick night's own run (sas_runs.finished_at for 2026-09-10 = 2026-09-10 21:12:36 UTC);
neither is a stale-wrapper-style silent repair. This closes routed-request item (viii).

---

## (b) Window, exclusions, and night count

Pick nights 2026-07-08 through 2026-09-10 inclusive, exclusions_v003.json (all three lists)
applied — no additional night in this window carries a manual_runs, non_session_runs or
uncorroborated_publication_runs flag (the flagged dates all fall before 2026-07-08 except
2026-06-26, also before the window). A direct DP-04 check (sas_runs.finished_at vs. the next
session's open) over all 46 in-window nights finds no run finishing after the next session's
open — every run in this window finishes roughly 21:0x-21:3x UTC the same evening. 46 elapsed
sessions, 46 nights, every session published one or more picks (reproducing the Q022 headline
finding for the identical window). Matured sub-window (last pick night whose session t+21 is
still inside the freeze, the Q022 Section h convention, confirmed against the calendar):
2026-07-08 through 2026-08-11, 25 elapsed sessions (t+21 for 2026-08-11 = 2026-09-10, the
freeze's last date; 2026-08-12's t+21 would be 2026-09-11, not in the freeze) — this matches the
PREREG's own "approximately 2026-08-11" placeholder to the session.

Published picks in window (qualified IS TRUE AND selected_rank IS NOT NULL): 374 (199 in the
matured sub-window, 175 in the not-yet-matured remainder). All 385 distinct candidate symbols
appearing in the window have price bars in manifest_prices_v001 (100% symbol coverage).

---

## (c) Feature-coverage counts, published vs. unpublished pools (item vi)

Full in-window population (374 published; 2,522 unpublished-pool rows — dark-lane plus
non-qualified, the complement of the publication predicate), no maturity restriction (this is a
data-availability count, not an outcome):

| population | n | 60+ prior bars | beta60/mom20/mom60/adv20 all computable | sector mapping present |
|---|---|---|---|---|
| published | 374 | 374 (100.0%) | 374 (100.0%) | 372 (99.5%) |
| unpublished pool | 2522 | 2508 (99.4%) | 2508 (99.4%) | 2520 (99.9%) |

The only unmapped symbol in this window, either side of the publication line, is BRK.B (2
published occurrences, 2 unpublished) — consistent with Q022 Section b's full-history finding
(BRK.B and BF.B are the only unmapped symbols ever; BF.B does not appear in this narrower window).
Feature and sector coverage are not what constrains B1 or B4 — see (d)/(e).

---

## (d) B1 — the hard-sector-block plus five-feature caliper control set (items i, ii)

Constructed exactly as PREREG Section 3 / Section 2.3: same-night unpublished candidates,
hard-blocked to the pick's own sector ETF, standardised within the night (median/MAD across that
night's full candidate universe, published plus unpublished, on rows with all five features
computable), kept only if within 1.5 standardised units on every one of beta60, atr_pct, mom20,
mom60, size, capped at 10 nearest, minimum 3 or the pick is dropped. Pool eligibility requires
the control to itself carry 60+ prior bars, a sector mapping, and forward bars covering the
window (matured), per Section 3's own text — so B1 sizes can only be measured, without
conflating a matching failure with mere data-immaturity, on the 197 matured, sector-mapped,
feature-complete published picks (of 199 matured published picks; the other 2 are the matured
occurrences of BRK.B).

B1 control-set size distribution (matured population, n=197):

| size | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| picks | 110 | 51 | 21 | 7 | 3 | 2 | 2 | 1 |

Overall drop share (fewer than 3 controls): 182 of 197 = 92.4%. This is well above the
approximately 19% loss the PREREG's own Section 10.2 disclosed as the expected cost of the
sector block alone (measured by Q022 as 19.1% same-sector-only loss) — the five-feature caliper,
not the sector block, does essentially all of the additional damage.

By sector ETF (matured population):

| sector | n | median size | mean size | dropped (fewer than 3) | drop share |
|---|---|---|---|---|---|
| XLB | 4 | 0 | 0.25 | 4 | 100.0% |
| XLC | 8 | 0 | 0.25 | 8 | 100.0% |
| XLE | 18 | 0.5 | 0.72 | 17 | 94.4% |
| XLF | 35 | 0 | 1.09 | 30 | 85.7% |
| XLI | 14 | 1 | 1.21 | 12 | 85.7% |
| XLK | 71 | 0 | 0.58 | 67 | 94.4% |
| XLP | 13 | 1 | 1.00 | 12 | 92.3% |
| XLRE | 3 | 0 | 0.00 | 3 | 100.0% |
| XLU | 3 | 0 | 0.33 | 3 | 100.0% |
| XLV | 19 | 1 | 1.16 | 17 | 89.5% |
| XLY | 9 | 1 | 0.78 | 9 | 100.0% |

Loss is not concentrated in thin sectors alone — XLK (the desk's largest, most liquid sector,
n=71 matured picks) drops 94.4%, essentially the same rate as the small sectors. The caliper,
not sector thinness, is the binding constraint (PREREG threat 2 anticipated the sector-thinness
channel specifically; the measured mechanism is different and is disclosed here as such).

Sensitivity (not the primary reading, printed for transparency): if "standardised units" is
read as the conventional robust z-score (MAD scaled by the 1.4826 consistency constant, i.e. a
caliper of roughly 2.22 raw-MAD units instead of 1.5 raw-MAD units), the pick-level B1-valid
share rises from 4.0% to 16.8% of all 374 in-window picks, and the count of nights with 3 or
more simultaneously-valid picks rises from 0 to 12 of 46 — still short of clearing the
0.35-per-session gate when projected the same way. The primary reading below uses the literal,
unscaled median/MAD ("standardised units" = raw (x minus median) divided by MAD), consistent
with no scaling constant being named anywhere in Section 2.3, Section 3 or the Q006 precedent
language it borrows from.

---

## (e) B4 — the Q006-verbatim partial-match control set (item iii)

Constructed exactly as Q006 Section 3 / PREREG Section 3 B4: 10 nearest same-night unpublished
candidates on beta60/atr_pct/mom20 only, standardised the same way, Euclidean, no sector block,
no caliper. Measured on the same 197 matured published picks (plus the 2 matured BRK.B
occurrences, which B4 does not need a sector for — B4 is valid for all 199 matured published
picks):

100% of matured picks (199 of 199) return the full 10-nearest B4 set. Median size = 10, every
pick 3 or more. This reproduces Q022 Section f's finding that the unrestricted, low-dimensional
match is "universal" and confirms that B4 is not what drops picks; B1 is.

---

## (f) Picks carrying both sets — E2's population (item iv)

both_sets = B1 valid (3+) and B4 valid (3+), on the same pick. On the 197 matured, sector-mapped
picks: 15 of 197 = 7.6%. These 15 are scattered across 13 distinct nights (2 nights carry 2 each;
the remaining 11 carry 1 each) — no single night reaches the required 3.

---

## (g) The Section 2.4 funnel (item v)

Published picks in window, n = 374 (independent screens, as in STEWARD_Q022_exposure.md Section
g — not mutually exclusive; a pick can trip more than one):

| reason | count | share |
|---|---|---|
| no swing-lane target | 0 | 0.0% |
| outcome_target_invalid non-null | 0 | 0.0% |
| swing T1 on the wrong side of C_t for the pick's direction | 1 | 0.3% (APH, 2026-07-28, bearish, target above C_t) |
| price-scale screen (target/C_t outside 0.5 to 2.0) | 8 | 2.1% — APH x7 (07-09, 07-31, 08-05, 08-06, 08-10, 08-11, 08-12), MNST x1 (07-13); the same systematic APH signature DATA_NOTES/Q018/Q022 already documented |
| fewer than 60 prior daily bars | 0 | 0.0% |
| no C_t | 0 | 0.0% |
| no session t+1 open | 9 | 2.4% — all 9 are the 2026-09-10 slate (the window's last night; the freeze simply ends there) |
| no sector mapping | 2 | 0.5% — BRK.B x2 |
| immature (session t+20 not yet inside the freeze) | 175 | 46.8% |

Clean, gradeable-by-existence, matured population: 189 of 374 (matured, has session t+1, has a
valid same-side in-scale swing target, no outcome_target_invalid, 60+ prior bars, sector
mapped). This is the population from which the 197-minus-2-BRK.B (about 189) B1-eligible-for-
matching figure in (d)/(f) is drawn (small discrepancies between 189 and 197 are the sector and
price-scale screens counted independently above, not summed).

---

## (h) The contributing-night rate — E1, E2, and the DEFERRED-gate call (item i)

Contributing night (PREREG Section 2.4): an eligible, matured night carrying 3 or more gradeable
picks with a valid B1 set (E1), or additionally a valid B4 set on the same picks (E2).

Measured on the matured sub-window (2026-07-08 through 2026-08-11, 25 elapsed sessions — the
only window over which "contributing" can be measured without reading a bar value that doesn't
exist yet):

| endpoint | contributing nights | elapsed sessions | rate per session |
|---|---|---|---|
| E1 | 0 | 25 | 0.000 |
| E2 (binding) | 0 | 25 | 0.000 |

The per-night B1-valid pick count never reaches 3 anywhere in the 46-night frozen history
(matured or not): the maximum observed on any single night is 2. E2's population (both sets) is
a subset of E1's by construction, so E2 is identically zero.

Cross-checked against the full 46-elapsed-session window using a pre-maturity "quasi-eligible"
proxy (every Section 2.4 screen that does not require a forward bar — swing target present,
in-scale, right-sided, no outcome_target_invalid, 60+ prior bars, sector present, B1/B4
validity — this requires no bar value that postdates the pick night, so it is a legitimate
counts-only measurement on immature nights too): 0 of 46 nights reach 3 or more qualifying picks
for E1 or E2. The two measurements agree: the shortfall is not a maturity artifact.

By month (elapsed sessions in parentheses; matured-only where applicable):

| month | nights | elapsed sessions | matured elapsed sessions | E1 contributing (matured) | E2 contributing (matured) |
|---|---|---|---|---|---|
| 2026-07 | 18 | 18 | 18 | 0 | 0 |
| 2026-08 | 21 | 21 | 7 (through 08-11) | 0 | 0 |
| 2026-09 (to the 10th) | 7 | 7 | 0 | not yet measurable | not yet measurable |
| overall | 46 | 46 | 25 | 0 | 0 |

The DEFERRED-gate call. PREREG Section 5 / DECISIONS item 16: lock only if the binding (E2)
contributing-night rate is 0.35 or more per elapsed session; below that line the question goes to
research/questions/DEFERRED.md with the measured rate and the projected date named, instead of
being locked. Measured E2 rate = 0.000, on both the matured-sub-window measurement and the
full-window proxy. This does not clear the gate, by the largest possible margin. Per DECISIONS
item 16 and Section 5, this measurement is what decides Q025 does not lock — that determination
belongs to the decision-maker at "record," not to this report, but the count it turns on is now
measured and is unambiguous.

Projected floor dates at the one-sided 90% lower bound of the measured rate (the request's own
sizing convention, DP-45 "moves out only"). A point estimate of 0.000 has a one-sided 90% lower
bound of 0.000 as well (a lower confidence bound cannot exceed the point estimate) — at that
bound no floor is ever reached; the projected date is undefined (infinite) within any horizon,
including DP-43's 12-month ceiling (2027-09-14 from a 2026-09-14 lock). For context, not as a
substitute for the gate: the one-sided 90% upper Clopper-Pearson bound on the true rate, given 0
events in 25 matured-night trials, is 1 minus 0.10 to the power (1/25), approximately
0.088 per session — even that optimistic upper read is barely a quarter of the 0.35 gate, and
would still require roughly 80 divided by 0.088, about 909 elapsed sessions (about 3.6 years) to
reach the 80-contributing-night floor for one endpoint alone, without even reaching the
20-per-cell or 30-post-lock floors. No number here supports sizing a window; it supports the
opposite conclusion.

---

## (i) Sub-cell enumeration (item vii)

Direction, score band, best_timeframe lane, and sector ETF, published-pick counts and B1-valid
pick counts, full window (54 non-empty cells; only the 5 largest shown, remainder in the same
pattern):

| direction | band | lane | sector | picks | B1-valid picks | both-sets picks |
|---|---|---|---|---|---|---|
| bullish | 80-85 | short | XLK | 87 | 0 | 0 |
| bullish | 80-85 | short | XLF | 38 | 2 | 2 |
| bullish | 80-85 | short | XLV | 23 | 0 | 0 |
| bullish | 80-85 | swing | XLK | 22 | 1 | 1 |
| bullish | 85-90 | short | XLK | 21 | 1 | 1 |

Only 5 of the 54 cells reach 20 published picks at all; the maximum B1-valid pick count in any
single cell, summed across the entire 46-night window, is 2. Since the contributing-night count
(the unit the 20-night floor is measured in) is 0 for both endpoints everywhere, every one of the
54 cells is flagged SUPPRESSED for the item-13 list, with certainty rather than by projection —
no cell can reach 20 contributing nights without the endpoint-level rate first becoming positive.

---

## Notes on method

- Sector mapping loaded from the pinned blob's "mapping" object (2,405 entries), hashed directly
  from the git blob to avoid the Windows checkout's CRLF translation (see Headline).
- Exposure features (beta60, atr_pct, mom20, mom60, adv20 to size) computed by the Steward from
  prices_daily_split bars dated on or before t, exactly as PREREG Section 2.3 specifies: beta60
  = trailing-60-session OLS slope of the symbol's daily return on SPY's daily return; atr_pct =
  desk-computed ATR14 divided by C_t (never the platform's atr_pct column, which DATA_NOTES flags
  as corrupted around splits); mom20/mom60 = trailing total return; size = log10 of the
  trailing-20-session median dollar volume. Standardisation is the night's cross-sectional
  median/MAD across the full candidate universe (published plus unpublished) with all five
  features computable, recomputed independently for every night.
- "Matured" (forward bars covering the window) uses the Q022 Section h convention — session
  t+21, not t+20, must be inside the freeze — reproducing that report's exact 2026-08-11 boundary
  on this identical window; this is a stricter (later) cutoff than a bare t+20 check and does not
  understate maturity.
- No forward bar value was read anywhere in this report; "matured" and "has session t+1" are
  existence checks against the trading calendar embedded in prices_daily_split, per the routed
  request's "forward bars read only to establish that a bar exists."
- No post-match balance (SMD or otherwise) was computed for either control construction; Section
  8 clause 7 is untouched, per the routed request's explicit prohibition and DP-45.
- Scratch scripts and intermediate parquet/CSV files used to build this report live in the
  session scratchpad, not under research/questions/ or committed to the repo.
