# Q005 elite_thinning -- RED TEAM review

Reviewer: red-team | Date: 2026-09-11 | Run reviewed: 2026-09-11T05:19:36Z
eval.py sha256 8e1d4600...1141 and run_summary.json sha256 bd9b13d6...fed80 -- both confirmed on disk before and after review.

## Decision (plain English, for Haci)

**I'm signing off, but changing the verdict to INCONCLUSIVE.** The configuration verdict (HISTORICALLY_CONFIRMED) doesn't hold up. The fall in elite scores is real as registered (Gate 0 passes). But the configuration changes that eval.py says "bracket the fall" couldn't have caused it:
- Two of them only decide which picks get published (`bear_publish_threshold`/`bear_max_output_cap` on 06-29, `publication_floor` on 07-08). They are not part of the score arithmetic, and they never blocked a single 90+ candidate (29 of 29 and 12 of 12 were published).
- The other two are a flag switch on 07-02 that lasted one night, and its undo on 07-07.

From 06-03 through 09-10 the scoring settings were identical. The only config differences between June (0.47 elite per night) and Jul-Sep (0.20 per night) are those three publication settings. So the fall happened with the scoring settings unchanged.

The test in eval.py splits the whole series at each change date and asks whether it is lower afterwards. The PREREG doesn't license that test, and in a declining series almost any date near the middle passes it. With that test set aside, the PREREG's own fallback applies, and eval.py already computed it: INCONCLUSIVE. The layer-by-layer tables disagree on the top cause (projection one at a time, flow in the cumulative table), and the layers interact heavily (+50.9% interaction).

A config review of the publication gates would target settings that removed zero elite picks. The honest answer is that scores fell across the board and this decomposition can't separate the layers. Nothing in this run needs a re-run; the defect is how eval.py maps its outputs to a verdict, not the numbers.

Independence disclosure: I did not read results/NOTES.md or platform_commits_scoring_agents.txt (not written by eval.py). While checking git state I did see the uncommitted research/BACKLOG.md diff (H-014), which contains Researcher commentary on this same issue. Every finding below is backed by code lines and eval outputs I checked myself.

---

## Findings, ranked by severity

### F1 CRITICAL -- The Channel 3a "brackets the fall" rule is an unlicensed choice, and it alone produces the HISTORICALLY_CONFIRMED verdict
Evidence:
- eval.py:589-601 tests each config change with a *global* split: all nights before the change date vs all nights on/after it (eval.py:590), permutation p <= 0.05 (eval.py:601). It is a test of "the series is lower after date X". It does not test the change:
  - p falls steadily with calendar date (channel3a_config_changes.csv: 05-15 0.062, 06-29 0.0499, 07-02 0.011, 07-07 0.0042, 07-08 0.0017).
  - The four tests that fire share 46 of their 46-51 "after" nights, all on config 181ae113b538. They are one P0-vs-P1 contrast (Gate 0) restated four times.
- eval.py:571 counts every key as behavioural unless it was added with the value False. That includes publication-only gates, and flow_polarity_* parameters added for a feature whose flag was False.
- The local +/-20-night step means are computed (eval.py:598, 609-611) but not used in the decision.
- What fired (channel3a_config_diffs.csv):
  - 06-29: bear_publish_threshold=80 and bear_max_output_cap=5 added.
  - 07-02: enable_fundamental_enrichment / enable_multi_agent_reports / enable_synthesis set false. That config (0fea1355bf26) was live for exactly one included night.
  - 07-07: the exact revert, back to hash 03fa47e1c436.
  - 07-08: publication_floor=80 added.
- None of these can move the primary target:
  - (a) PREREG sec.2 (PREREG.md:46-48) makes elite-candidate primary precisely "because it ... isolates scoring from the publication cap".
  - (b) eval.py's own arithmetic (eval.py:232-251) has no term for any of these keys, yet it reproduces every P1 row's overall_score within 0.01. Residuals occur only on 06-26, which is in P0 (run_summary.reconstruction_check).
  - (c) published_conversion.csv shows 29/29 and 12/12 elite candidates published. The publication gates never removed an elite, even from the secondary target.
  - (d) The configs installed by three of the four firing changes produced an elite on every night they were live: 03fa47e1c436 had 4 nights with 4 elite; 0fea1355bf26 had 1 night with 1 elite (nightly.csv). A change and its exact reversal cannot both be the cause of the same fall.
  - (e) 181ae113b538 (07-08..09-10: 46 nights, 9 elite) equals 56a2dccf4366 (06-03..06-26: 17 nights, 8 elite) plus three publication keys. The fall happened under an unchanged scoring configuration.
- The only change with scoring content (05-15: weights gex 12->0, technical 20->27, projection 26->29, catalyst 8->10; ATR block and ATR component cap enabled) does not fire (p=0.062). It sits inside P0 and was followed by the best month (Jun 0.571 per night).

Most faithful reading of PREREG sec.4 (PREREG.md:114-117) and sec.8 (PREREG.md:206-210):
- The change has to be able to act on the thing that fell.
- The configuration it installs has to be the one in force across the fall.
- This fits sec.4's "discrete cause", sec.10.8 (PREREG.md:261-263), and sec.2's scoring-vs-publication separation.

Verdict under alternative readings (using only numbers eval.py already produced; "hand" means arithmetic on eval outputs, not a re-run):

| Channel 3a reading | Fires? | Verdict |
|---|---|---|
| eval.py: global split, any key | 06-29, 07-02, 07-07, 07-08 | HC-configuration |
| Only keys that can move overall_score, global split | Only the one-night enrichment toggle (07-02) and its revert (07-07), *if* enrichment counts as a scoring flag. Fundamental layer restored share is 6.4%, NOT A DRIVER. | HC-configuration in name only (absurd: names a 1-night config) |
| Only keys that can move overall_score, config in force >= 20 nights | None (05-15 p=0.062) | Distributional -> INCONCLUSIVE |
| Any key, local step at the change date (eval local20 means; hand conditional binomial, 20 vs 20 nights) | None: 06-29 11->9 p=0.41; 07-02 11->6 p=0.17; 07-07 10->5 p=0.15; 07-08 11->4 p=0.059 | Distributional -> INCONCLUSIVE |
| Any reading + PREREG sec.6 stability applied to 3a (see F2) | Cannot reach CONFIRMED | INCONCLUSIVE |

### F2 HIGH -- PREREG sec.6's stability rule is never applied to Channel 3a
- PREREG.md:156-158: "A channel that explains the fall only on one side of one cut is labelled unstable and cannot reach CONFIRMED."
- eval.py:935-942 applies the month and cut rules to the distributional items only. The 3a branch goes straight to the verdict (eval.py:1016-1018).
- All four firing dates fall in the sealed half (after 2026-05-29). The in-sample half has no counterpart (in-sample 17 elite / 37 nights, 0.459). So even the eval.py reading of 3a fails sec.6.
- This is an independent route to "not CONFIRMED".

### F3 HIGH (does not change the registered verdict) -- Gate 0's "the fall is real" is fragile to night-to-night dependence
- Lag-1 autocorrelation of nightly elite counts (hand, from nightly.csv): 0.253 overall, 0.256 within P0, 0.054 within P1. Elite nights come in streaks (05-01..05-08: 7 in 6 nights; 05-29..06-03: 6 in 5; 06-29..07-10: 7 in 8).
- The permutation tests (eval.py:401-409) and the Poisson/exact tests assume nights are exchangeable or independent.
- An AR(1) variance inflation of about (1+rho)/(1-rho) = 1.68 would move the model-based p-values (0.039 trend, 0.041 rate) to about 0.1 (back-of-envelope only).
- Within the constant v1.6 scoring config (05-15..06-30: 14/31, 0.452) vs P1 (12/49, 0.245), the hand exact conditional test gives p=0.085 one-sided.
- Gate 0 passes as registered: Poisson trend and exact rate tests, all p <= 0.05, BH q=0.0159. So the verdict is not NULL. Any report should say the fall is statistically marginal once streakiness and the 05-15 weight change are accounted for.

### F4 MEDIUM -- Distributional-branch choices: eval.py's readings are the faithful ones, but two alternatives would give HC(channel2)
- "Greedy top" is the component with the largest *incremental* share (eval.py:972 -> flow_strength_score, +71.7% at step 3). The greedy order is sorted by marginal share (eval.py:837). Reading "top" as step 1 would therefore always equal the marginal top and make the sec.8 disagreement clause (PREREG.md:202) vacuous. I endorse eval.py's reading.
  - Under the step-1 reading: explains=[channel2_score_distribution] (run_summary), reconstruction 1.28 >= 0.5, month rule met (Jul 142.9%, Aug 120.0%), cut 122.5% -> HC (channel 2).
- The INCONCLUSIVE clauses are checked before HC (eval.py:976-993). Giving HC precedence would also yield HC (channel 2). That contradicts PREREG sec.10.2 (PREREG.md:242-244: disagreement "is INCONCLUSIVE rather than picking the flattering table"). I endorse eval.py's ordering.
- The Channel 2 vs Channel 3 precedence (eval.py:964-970) does not matter in this run, because no Channel 3/4 item is labelled EXPLAINS. Projection is 56.0% but its CI lower bound is 17.5% < 25%.
- Channel 2 EXPLAINS is close to automatic here: Channel 1 is negative because candidates per night rose from 54.1 to 62.7. "Scores slid" therefore restates Gate 0.
- The greedy table is non-monotone (cumulative 149% -> 136% at step 4) with interaction +50.9%. The components are not separable, which supports INCONCLUSIVE.

### F5 MEDIUM -- The P0 baseline mixes engine states
- P0 straddles:
  - the 05-15 scoring-weight/ATR change (27 nights before it, 15 elite; 31 after, 14);
  - whale_watch dropping out on 04-20 (20 per night -> 0);
  - bearish projection v1 -> v2 on 05-19 (nightly.csv).
- On 07-02, bearish projection v1 comes back alongside v2 (15 -> 30 bearish per night; N ~50 -> ~63) and stays for all of P1. The bearish share rose from 30.4% to 38.8% (channel4_descriptors.csv); conflict_penalty p90 rose from 8 to 13.
- The "P0 rate applied to P1" baseline and the Channel 1/2/3/4 reference distributions are therefore drawn from a different universe and weighting than P1. The PREREG handled the catalyst straddle (June-only rerun: identical 8.0%) but not these.
- This is a design limitation, not an eval.py error. It does not change INCONCLUSIVE, but it would undercut any single-cause claim. The 07-02 source change (not a config_json key) is the kind of non-config cause PREREG sec.10.4 warns about.

### F6 MEDIUM -- The +5 GEX-offset component departs from the PREREG definition (eval.py's choice is correct, but not declared as a deviation)
- PREREG.md:100-101 defines firing as "share of rows with a null gex_alignment_score" (P0 31.1%, P1 1.2%).
- eval.py:190, 697 quantile-maps the *recorded* gex_missing_offset_value instead (P0 0.5%, P1 1.2%; channel3_component_distributions.csv). The recorded value is what reproduces 6194/6211 overall_scores. The PREREG definition would add a +5 that P0 scores never contained.
- Under the literal definition the restored share was not computed. It would plausibly be large and could make the offset a spurious EXPLAINS.
- The PREREG sec.9 hypothesis that the offset "stopped firing" is refuted by the recorded data: it rose.
- Required for the report: state this as a PREREG deviation.

### F7 MEDIUM/LOW -- 2026-06-26 is a mixed-state night that is not excluded
- 17 of 52 rows have technical_structure_score (column) differing from the score_details_json subscore by 2.9 to 62.2 points (mean 29). That is not float noise (run_summary.reconstruction_check json_vs_column_mismatches; hand check on the frozen parquet).
- 11 picks were published that night vs the usual 8.
- It looks like a re-run or partial rewrite, so what was known at 16:05 is uncertain. No row that night is >= 90 (max among the mismatched rows is 85.1), so the verdict is unaffected.
- Refer to the Data Steward for the next exclusions file.

### F8 LOW -- Extra exclusion of 2026-04-03
- The PREREG text names 5 manual-run nights (PREREG.md:42-44). eval.py also drops the Good Friday non-session run (eval.py:143-150). It is listed in exclusions_v001.json non_session_runs, with 0 picks published.
- Sensitivity check: Gate 0 still passes (p_trend 0.0245, p_rate 0.0197; gate0.csv).
- The 06-29 3a test at p=0.0499 is borderline and may not survive keeping that night. This is moot given F1.

### F9 LOW -- Bootstrap and CI handling
- 12/2000 replicates with S <= 0 are dropped before the share CIs are formed (eval.py:853-855). Those CIs are therefore conditional on a fall existing (small bias).
- Ratio shares with small S produce very wide CIs (projection [17.5%, 264%]).
- The bootstrap resamples nights (cluster) rather than blocks, despite the autocorrelation in F3. Desk rule 6 allows this, but it understates the uncertainty.

### F10 LOW -- Eleven unregistered formal tests decide the verdict
- PREREG sec.7 (PREREG.md:174-176) says Gate 0 is the only formal test. The 11 Channel 3a permutation tests (eval.py:593-597) are uncorrected.
- Multiplicity alone would not rescue F1 (Bonferroni x11 keeps 07-07 and 07-08). The problem is validity, not multiplicity.
- F2 family BH is correct: Q005 is the only registered F2 question (PREREG headers grepped), m=1, q=0.0159.

### F11 LOW -- Knowledge-time details
- No outcome column is loaded (eval.py:156-157).
- Prices are joined backward-only with an assert (eval.py:635-637).
- market_regime_daily is used only from 06-09 (eval.py:167, 315).
- market_regime_snapshot is descriptive only (eval.py:539-541).
- One issue: prices_daily_split is split-adjusted with split factors known when the dataset was pinned, so the Channel 4 price-level terciles (eval.py:641-643) carry hindsight. This affects Channel 4 only, which does not drive the verdict.

### F12 PROCESS
- The EVALUATED note in state.json points the red team to results/NOTES.md. That is a contamination vector; researcher notes should not be addressed to the red team.
- scripts/second_opinion.py was NOT run (checklist item 10, below).

---

## Checklist

- Step 0 validators: PASS. v1-v9 all PASS on my run of `validators.py --question Q005`.
- 1 Population and filters match the PREREG: PASS with deviations.
  - Window, all candidates regardless of qualified, elite definitions (eval.py:41-44, 295-296), P0/P1 cut, and in_sample_end from the manifest all match.
  - Deviations: extra 04-03 exclusion (F8); GEX-offset definition (F6); Channel 3a firing rule invented (F1).
- 2 Look-ahead: PASS. No outcome fields; trailing prices only; PIT regime from 06-09. Minor split-adjustment hindsight in Channel 4 (F11). The 06-26 row mutation is a knowledge-time hazard with no elite impact (F7).
- 3 Denominator: PASS with notes. 6 excluded nights are counted and reported; no ladder/W60 dependence; SUPPRESSED cells are May (16 nights) and Sep (7 nights); the month rule uses only Jul and Aug; 107 >= 80 nights. 12 bootstrap replicates with S <= 0 are dropped (F9).
- 4 Baseline: FAIL for single-cause attribution. The P0 reference mixes weight regimes and source universes (F5); the counterfactual swaps inherit this.
- 5 Regime / calendar: PARTIAL.
  - The fall holds in the SPY up-tape stratum (P0 0.465, n=43 vs P1 0.222, n=36). Down-tape is suppressed in both periods.
  - PIT regime cells in P0 are all suppressed (15 nights), so no within-regime P0/P1 comparison is possible.
  - Channel 3a exists only on the sealed side of the cut (F2).
  - Channel 2 holds in Jul, Aug and across the cut.
- 6 Multiple testing: PASS for Gate 0 (F2 family, m=1, q=0.0159). FAIL for the 11 uncorrected, unregistered 3a tests that decide the verdict (F10).
- 7 Effect size / CI: N/A for MPE; the 20%/50% attribution thresholds serve instead, and eval.py implements them (eval.py:811-821). CIs are clustered on nights; n is counted in nights. Dependence caveat in F3.
- 8 Exit rule: N/A. This is a diagnostic; no outcome or exit is measured.
- 9 Reproducibility: PASS. I backed up results/ and re-ran `python eval.py` (43 s, exit 0, empty stderr). All results files were byte-identical by sha256, and stdout JSON equals run_summary.json.
- 10 Second opinion: NOT RUN.
  - scripts/second_opinion.py needs OPENAI_API_KEY. That credential is not on the CLAUDE.md non-negotiable #1 allowlist ("Never look for, request, or use any other credential").
  - It would also write results/SECOND_OPINION.md, outside the single file I was allowed to write, and send the PREREG, eval.py and SUMMARY.md to a third-party service.
  - The conflict between the red-team definition and CLAUDE.md is for Haci to resolve. If he runs it, its critique should be appended here.

## Required notes for the report / ledger (no re-run needed)
1. State the verdict as INCONCLUSIVE:
   - Channel 3a fired only under an unregistered global-split rule, on publication-only gates and a one-night flag toggle and its revert.
   - Under the faithful reading, the distributional branch applies: marginal top (projection_score) != greedy top (flow_strength_score), with +50.9% interaction.
2. Report that scoring config was constant from 06-03 through 09-10 (only publication keys changed), and that 100% of elite candidates were published in both periods.
3. Declare the GEX-offset deviation (F6), the 04-03 exclusion (F8) and the 06-26 mixed-state night (F7).
4. Caveat Gate 0 for streakiness (F3) and the mixed P0 baseline (F5).
5. Any successor question that re-specifies the 3a rule is post hoc with respect to manifest_v001 and must say so.

SIGN-OFF: INCONCLUSIVE
