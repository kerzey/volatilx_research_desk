# QNNN — <slug>

**Status:** DRAFT | LOCKED (commit <hash>) | RUN | CLOSED
**Family:** <family name from BACKLOG.md>
**Manifest:** research/data/manifest_vNNN.json (as_of: YYYY-MM-DD)
**Registered by:** registrar · **Lock authority:** desk (DP-46) · **Date:** YYYY-MM-DD

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
- Primary: <named ladder target reached within k sessions from the stated entry>, against
  a same-night distance-matched control. State the numeric contrast and MPE (DP-20/DP-10).
- Entry: <DP-03/DP-11 basis>. A target passed at entry is not a hit. Stops are not assumed exits
  unless the hypothesis explicitly studies an exit plan (DP-02). State first-touch ordering rules.
- Default L3 clock: 20 sessions (DP-09). Other endpoints justify their own maturity windows.
- Report speed and adverse excursion; fixed-horizon return is descriptive. If an execution plan
  is named, report its realized result alongside the path. Do not imply option or portfolio profit
  from target-touch rates alone.
- W10/W20 are NON_QUOTABLE. Subscriber-facing claims require prospective confirmation and the
  W60 exposure policy; W60 maturity alone is not claim approval.

## 5. Sample floors and expected n
- Unit: trading night, not stock rows or control draws. At least 80 contributing nights per primary
  endpoint, 20 per reported cell (DP-21), and 30 post-lock contributing nights for prospective
  confirmation (DP-24). Define contributing separately for every endpoint.
- Counts-only funnel: <elapsed / eligible / old-enough-to-mature / gradeable / contributing /
  post-lock contributing>, with source manifest and count date.
- Forecast rate: <contributing nights / fully observable calendar sessions, exclusions retained>.
  Add <k> maturity sessions once; never estimate attrition from an immature tail (DP-53).
- Planning scenarios and justified margin: <...>. Precision/power assumptions at the MPE,
  including dependence, multiplicity and strata: <...>. Floors alone do not guarantee precision.
- Interim look (DP-58) — registered here or not at all: <none | 60 contributing nights per primary
  endpoint, projected <date>>. Boundary: `p_perm < 0.005`, point estimate clearing the MPE, and both
  DP-51 CIs excluding the MPE. Success-only, never futility. The 20-per-cell and 30-post-lock floors
  bind unchanged, so 60 total with a cell under 20 continues. The decision date below does not move.
- Collection end <date>; decision <date>; single DP-13 extension <date>; hard stop <date>.
  Define exact counts-only extension/DEFERRED branch. Do not inspect effects to choose an extension.
- Write schedule.json with decision_date, extension_date, hard_stop, rule, extended, check_from
  and pin_at_decision. State each prospective freeze's delivery and required bar scope (DP-23).

## 6. Split and stratification
- In-sample <dates>; sealed <dates>; prospective <dates after lock>. Disclose all prior exposure
  to each cohort; previously inspected data cannot be claimed as independent confirmation.
- Stratify by knowledge-time-valid regime and preregistered calendar periods. Respect engine
  changes, the 2026-06-01 catalyst split and the 2026-06-09 regime availability cutoff.
- Define consistency requirements and suppression rules now; absence of an observed regime is
  not evidence of robustness. Historical companions live outside this question and cannot unseal it.

## 7. Multiple testing
- Cells/variants evaluated: <count>. Family size at time of registration: <count>.
- Report raw p and Benjamini–Hochberg q across the family; threshold q ≤ 0.10.

## 8. Decision rule (numeric, written before unsealing)
- CONFIRMED: <explicit numeric effect, CI and MPE criterion>, q ≤ 0.10, all sample, validity and
  registered consistency gates met. State whether historical or prospective confirmation is possible.
- Report date/block-clustered and episode-clustered uncertainty (DP-51); a claim clearing only
  the first is INCONCLUSIVE. Define resampling, overlap handling, seeds and family correction.
- NULL: <registered rule that rules out the claimed meaningful benefit with sufficient precision>.
  A CI including zero alone does not establish no effect.
- INCONCLUSIVE: uncertainty cannot distinguish meaningful benefit from no benefit, inconsistent
  periods, or a specified validity failure. Counts shortfall follows §5's extension/DEFERRED rule.
- Fixed look: <date>, deciding at α <0.05 | 0.048 when a DP-58 interim is registered>. Interim look:
  <none | <date>, DP-58 boundary — success only>. No unregistered interim outcome look, ever. Any other
  sequential design preregisters boundaries, dependence assumptions and multiplicity before any
  prospective outcome.

## 9. If CONFIRMED, what changes
<a line in the Manual Trading Guide / a lane rule / a flag in SAS config / a marketing claim type>
Owner: implementer. Flag off, prove inert, shadow validation ≥ 30 nights. HUMAN_APPROVED,
IMPLEMENTED_FLAG_OFF and RELEASE_APPROVED retain their human-only gates. A hypothesis is not a
defect repair. State DP-50 dependencies on every affected in-flight experiment.

## 10. Known threats to validity (registrar's own list)
- <look-ahead risk, e.g. regime label finalized after the fact>
- <denominator risk>
- <regime confound>
- <prior exploration, engine changes, repeated symbols/overlapping paths, missing controls>

### Internal learning output (DP-52/55)
Evidence card: <what existing permitted evidence can say now / limits / next review date>.
Historical companion: <separate protocol path or not feasible and why>. No locked outcomes are
opened for this output, and it cannot promote a controller verdict or subscriber claim.

## 11. Open decisions before lock
<Only what research/DECISION_POLICY.md does not settle; cite DP-ids inline where it does.
 Resolved by `@decision-maker decide QNNN`, folded back by `@registrar apply QNNN`.>
1. **<decision in one line>** — Options: A <…> / B <…>. Recommendation: A, because <one line>.
   Changes: §<n>, §<m>.
