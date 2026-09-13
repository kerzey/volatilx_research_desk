# QNNN — <slug>

**Status:** DRAFT | LOCKED (commit <hash>) | RUN | CLOSED
**Family:** <family name from BACKLOG.md>
**Manifest:** research/data/manifest_vNNN.json (as_of: YYYY-MM-DD)
**Registered by:** registrar · **Approved by:** haci · **Date:** YYYY-MM-DD

## 1. Hypothesis (plain English, one sentence)
<e.g. "SAS picks that hit L1 within two trading days go on to reach L4 more often than picks that take longer.">

## 2. Population
- Source table(s) in manifest: <...>
- Filters (exact): <direction, score band, timeframe, dates, completeness, qualification>
- Exclusions: <null-ladder rows? immature W60? symbols on blacklist?> — state whether excluded or kept, and why.

## 3. Baseline(s) — what this must beat
- B1: <same-universe cohort without the condition, same date range, same regime mix>
- B2 (if selection edge is in question): random-8 draw from the qualified universe per night, 1,000 resamples.

## 4. Objective metric
- Direction-adjusted realized return under exit rule **E-<id>**:
  <e.g. "enter next-open, exit at first of: L2 touch / stop / 10 trading days">
- Descriptive only (never decides): touch-hit rate, MFE, days-to-hit.
- Windows: W60 (quotable) and W20 (NON_QUOTABLE) — state which decides.

## 5. Sample floors and expected n
- Per cell n ≥ 20; total n ≥ 100.
- Steward's coverage estimate: total ≈ <n>, per regime ≈ <n / n / n>.
- If expected n < floor → DEFERRED, revisit on <date>.

## 6. Split and stratification
- In-sample: trading dates <start> to <mid>; out-of-sample: <mid+1> to <end>.
- Stratify by `market_regime_daily.regime` and by calendar half.
- A result counts only if direction and sign agree in both halves.

## 7. Multiple testing
- Cells/variants evaluated: <count>. Family size at time of registration: <count>.
- Report raw p and Benjamini–Hochberg q across the family; threshold q ≤ 0.10.

## 8. Decision rule (numeric, written before unsealing)
- CONFIRMED: <metric> − <baseline> > <x> with 95% CI excluding 0, q ≤ 0.10, holds in both halves.
- NULL: CI includes 0 in the full sample with n ≥ floor.
- INCONCLUSIVE: n below floor, or halves disagree in sign.

## 9. If CONFIRMED, what changes
<a line in the Manual Trading Guide / a lane rule / a flag in SAS config / a marketing claim type>
Owner: implementer. Shadow period before flip: ≥ 20 trading days.

## 10. Known threats to validity (registrar's own list)
- <look-ahead risk, e.g. regime label finalized after the fact>
- <denominator risk>
- <regime confound>

## 11. Open decisions before lock
<Only what research/DECISION_POLICY.md does not settle; cite DP-ids inline where it does.
 Resolved by `@decision-maker decide QNNN`, folded back by `@registrar apply QNNN`.>
1. **<decision in one line>** — Options: A <…> / B <…>. Recommendation: A, because <one line>.
   Changes: §<n>, §<m>.
