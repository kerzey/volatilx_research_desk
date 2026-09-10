# Q001 — control_cohort: does SAS selection add return over random selection from its own universe?

**Status:** DRAFT (lock by committing this file after Haci review)
**Family:** F1 Selection edge
**Manifest:** research/data/manifest_v001.json (as_of: filled by data-steward)
**Registered by:** registrar · **Approved by:** haci · **Date:** 2026-09-__
**Version:** v2 — selection isolated from execution; night-level inference; MPE added.

## 1. Hypothesis
On a typical night, the equal-weight basket of published SAS picks earns a higher
direction-adjusted return over the next ten sessions than a same-size basket drawn at
random from that night's qualified universe.

## 2. Population
- Unit of observation: **the trading night** (one selection decision). Stocks are not
  independent observations.
- Treatment basket, night t: all published SAS picks (rank 1–K_t, K_t ≤ 8), scoring
  versions v1.5/v1.6, from first SAS run through the manifest's T+10 maturation cutoff.
- Qualified universe U_t: every audit-table candidate on night t with overall_score ≥ 70 and
  completeness ≥ 35 (published or not). Secondary universe U′_t: overall_score ≥ 50.
- Direction for every candidate = the direction SAS assigned in the audit record.
- Nights with K_t < 3 or |U_t| < 2·K_t are excluded and counted.
- Delisted / missing-price rows are dropped from the basket and counted; a night is dropped
  if >25% of its basket is missing.

## 3. Controls (all computed per night, same K_t, same exit rule)
- C1 (primary): random K_t from U_t, using SAS direction. 2,000 Monte Carlo draws per
  night → per-night expected control return. **MC draws do not add to inferential n.**
- C2: random K_t from U_t with coin-flip direction — isolates direction skill from selection.
- C3: bottom-K_t by overall_score from U_t — does rank order carry information?
- C4: random K_t from U′_t.

## 4. Metric — one rule for every stock, treatment and control
- R_i,t = Dir_i,t × (Close_{t+10} − Open_{t+1}) / Open_{t+1}.  No stops, targets, ladders,
  or Conviction Monitor. Execution intelligence is tested separately (F6).
- Night return: SAS_t = mean_i R_i,t over the basket; Control_t = MC expectation.
- **Primary endpoint:** Alpha_t = SAS_t − C1_t, net of 10 bps per side (20 bps round-trip).
- Secondary (diagnostic, never decides): T+20 and T+60 variants, median, hit rate of R>0,
  C2/C3/C4 comparisons, regime splits, MFE, L1–L4 touch rates.

## 5. Sample and power
- Expected nights ≈ 90–100 at freeze. Steward fills exact count.
- Smallest effect of interest (**MPE**): +0.50% net per 10-session window
  (placeholder — Haci to confirm). Rough power at n≈100 and σ(Alpha_t)≈4%: ~1.1% detectable
  at 80% power. Effects between 0 and MPE will read INCONCLUSIVE; that is expected.
- Regime cells with < 20 nights are SUPPRESSED.

## 6. Split and stratification
- In-sample: first half of nights by date; out-of-sample: second half.
- Stratify by point-in-time `market_regime_daily.regime` on night t (the label written that
  night, never a revised one — validator V3 enforces).
- Knowledge rule: every joined feature must have available_time ≤ 16:05 ET on night t.

## 7. Inference
- Date-clustered bootstrap over nights (2,000 resamples) for the CI of mean(Alpha_t).
- Sign-flip permutation test on Alpha_t (10,000 permutations) for the p-value.
- For T+20/T+60 secondaries: stationary block bootstrap, block length ≈ horizon/2.
- Family F1 size at registration: 1 primary endpoint. Secondaries are reported with BH q
  but do not enter the decision.

## 8. Decision rule (numeric, before unsealing)
- HISTORICALLY CONFIRMED: OOS mean(Alpha_t) > MPE, clustered 95% CI excludes 0,
  permutation p ≤ 0.05, same sign in both halves, and no regime cell (n≥20) with mean
  Alpha_t < −MPE.
- NULL: full-sample clustered CI includes 0 with n ≥ 80 nights, and |mean| < MPE.
- INCONCLUSIVE: anything else — including "positive but below MPE."
- PROSPECTIVELY CONFIRMED: only after ≥ 30 forward shadow nights (post-lock, untouched)
  reproduce the sign with mean(Alpha_t) > 0.

## 9. If HISTORICALLY CONFIRMED
- Q008 weight sweep unblocked. Claim type "selection edge vs own universe" enters the
  exposure policy **only** after PROSPECTIVE confirmation.
- If NULL: Q008 stays blocked; effort moves to F3 (new information layers).

## 10. Threats to validity
- Regime label revision (V3). Delisting survivorship (counted). Overlapping windows for
  T+20/T+60 (block bootstrap). Nights with tiny U_t (excluded). Thin bearish cohort
  (report bull/bear separately as secondary). Retrospective nature — hence §8 prospective state.
