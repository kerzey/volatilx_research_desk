> **ALL FIGURES IN THIS REPORT ARE NON_QUOTABLE** (research-only; per PREREG §Type this is a diagnostic decomposition with no subscriber claim, rule 12). Nothing here may be used in marketing, product copy, or a subscriber-facing statement.

# Q005 — elite_thinning: why does SAS publish fewer 90+ picks every month?

**Historical verdict: INCONCLUSIVE.** **Prospective verdict: not available** (PREREG §8 — this is a diagnostic of the past, not an edge; the controller record for this question ends at HISTORICALLY_CONFIRMED / NULL / INCONCLUSIVE).

*Written by the reporter agent. The harness blocked the subagent from creating this file, so the main session placed its text verbatim, with one clarification in the Level 1 paragraph (the two sets of monthly counts).*

---

## Level 1 — for Haci

We asked why SAS's monthly count of elite (90+ score) picks has been falling — 8/13/12/8/3/2 from April through early September across all runs (8/9/12/7/3/2 after dropping the manual-run nights this study excludes; `results/monthly_panel.csv`). Verdict: INCONCLUSIVE. The fall itself is real: elite-candidate rate dropped from 0.50/night (April–June, n=58 nights) to 0.245/night (July–September, n=49 nights), p=0.016 (NON_QUOTABLE). But we cannot pin the cause on one thing. eval.py's mechanical rule flagged a configuration change as the cause; the red team overrode that to INCONCLUSIVE because the flagged config changes only govern which picks get published, never blocked an elite score, and scoring itself was unchanged for the ten weeks that mattered. Nothing changes on the platform from this result. Caveat: the fall, while real, is statistically marginal once night-to-night streakiness is accounted for.

---

## Level 2 — detail

### The verdict on record vs. what eval.py computed

| | verdict | reasoning |
|---|---|---|
| **eval.py mechanical output** | HISTORICALLY_CONFIRMED — configuration (Channel 3a) | Config changes effective 2026-06-29, 07-02, 07-07, 07-08 statistically "bracket" the fall under eval's global before/after split test (run_summary.json `verdict_reason`) |
| **Red team review** | **INCONCLUSIVE (verdict change)** | Those four changes are publication-only gates or a one-night flag toggle plus its own revert; none can move `overall_score`. With Channel 3a set aside, PREREG §8's own fallback applies, and eval.py had already computed it: the distributional branch is INCONCLUSIVE (marginal-top vs greedy-top disagreement). |
| **Controller record (state.json, `historical_verdict`)** | **INCONCLUSIVE** | This is the verdict that stands, per the red team's sign-off note in `state.json` history: *"Red team endorses INCONCLUSIVE (verdict change from eval HISTORICALLY_CONFIRMED-configuration)."* |

This report and the ledger use the controller-recorded verdict, **INCONCLUSIVE**, not eval.py's raw output. The disagreement is stated here rather than smoothed over, because the ledger's job is to record what actually happened in review, not just the final number.

### Why the configuration attribution was rejected

Channel 3a's mechanical rule tests "is the whole series lower after date X" for every config change, at any point in the sample — a test that, in a series that is generally declining, almost any mid-sample date will pass (`p_perm` in `channel3a_config_changes.csv` falls steadily and monotonically with calendar date: 05-15 → 0.062, 06-29 → 0.050, 07-02 → 0.011, 07-07 → 0.004, 07-08 → 0.002). It is not a test of *that specific change*; it is four restatements of the same April–June-vs-July–September contrast that Gate 0 already reports.

Checked against what the changes actually installed (`channel3a_config_diffs.csv`, `published_conversion.csv`):
- **06-29** added `bear_publish_threshold` and `bear_max_output_cap` — publication gates.
- **07-02** disabled three enrichment/report flags for exactly one included night; **07-07** is the exact revert back to the prior config the next trading day. A change and its own undo cannot both be "the cause" of the same fall.
- **07-08** added `publication_floor` — another publication gate.
- **None of these appear in eval.py's own score arithmetic**, which nonetheless reproduces 6,194 of 6,211 candidate rows' `overall_score` to within 0.01 (`run_summary.json` `reconstruction_check`).
- **100% of elite candidates were published in both periods** (29/29 April–June, 12/12 July–September, `published_conversion.csv`) — the publication gates never removed a single elite-scoring row, even from the secondary (published) target.
- Scoring config was **constant from 2026-06-03 through 2026-09-10** (config hash `56a2dccf4366` 06-03..06-26, then `181ae113b538` 07-08..09-10 — the only difference between the two is the three publication keys above). The fall in elite-candidate rate happened while the scoring configuration did not change.
- The **one** config change in the whole window that touches score arithmetic — weights, ATR-elite cap, and timeframe multipliers, effective 2026-05-15 — does **not** bracket the fall (p=0.062) and sits *inside* the April–June baseline period, immediately followed by June, the single best month in the sample (0.571 elite-candidates/night).

With Channel 3a set aside, the faithful reading falls through to PREREG §8's distributional fallback, already computed by eval.py:

- **Channel 1 (candidate count) is ruled out as a driver, and in the wrong direction.** Candidates per night *rose* from 54.1 (April–June) to 62.7 (July–September); restored share **−10.8%** [−58.8%, −3.4%], labelled NOT_A_DRIVER. The engine is not seeing fewer names.
- **Channel 2 (overall score distribution shifted down) EXPLAINS most of the shortfall by construction** — restored share **128.0%** [118.9%, 195.2%] — but this is close to a restatement of Gate 0 itself (scores fell broadly; Channel 1 went the wrong way, so "the distribution shifted" is nearly definitional here), not an independent finding.
- **Inside Channel 2, no single scoring layer clears the EXPLAINS bar.** The largest single-layer mover is `projection_score` at **56.0%** [17.5%, 264.2%] — CONTRIBUTES, not EXPLAINS, because its CI lower bound (17.5%) is below the 25% bar. Run the same 14 components in **greedy cumulative** order instead of one-at-a-time, and the top mover is a different layer, `flow_strength_score` (+71.7% incremental at that step). **Marginal top ≠ greedy top, with a +50.9-percentage-point interaction term between the layers** — the PREREG's own disagreement clause (§8) that forces INCONCLUSIVE.
- **Channel 4 (universe/composition) contributes but doesn't explain:** joint reweighting (price/volume/direction) restores 38.0% [12.6%, 196.0%]; margin-only reweighting restores 24.9% [7.6%, 139.2%] — both CONTRIBUTES, both wide CIs.
- **Every other Channel-3 component (technical, flow, catalyst, fundamental, GEX, smart-money confirmation, cross-layer bonus, conflict/missing-data penalties, completeness, best-timeframe mix, ATR-elite cap) is NOT_A_DRIVER** — flat 0% or CI spanning 0.

**Bottom line on attribution:** the shortfall is real and broad-based across scores, but this decomposition cannot separate which layer(s) drove it. That is what INCONCLUSIVE means here — not "no effect," but "the registered channels can't apportion this one."

### Gate 0 — the fall is real, but the red team flags it as fragile (red-team analysis, not registered)

Gate 0 passes exactly as pre-registered: elite-candidate rate fell from **0.500/night (n0=58) to 0.245/night (n1=49)**, rate ratio 0.490, `p_trend_perm=0.016`, `p_rate_perm=0.018`, `p_rate_exact=0.041`, BH q=0.016 (family F2, m=1 — Q005 is the only registered F2 question). This is **not NULL**; the decline is not small-number noise at the registered significance level.

The red team's own (unregistered, hand-computed, labelled as such) checks caution against reading this as a clean signal:
- Nightly elite counts show **streaks**, not independence: lag-1 autocorrelation 0.253 overall (0.256 within April–June, 0.054 within July–September); e.g. 7 elites in 6 nights (05-01..05-08), 6 in 5 nights (05-29..06-03), 7 in 8 nights (06-29..07-10). An AR(1) variance-inflation back-of-envelope (~1.68×) would move the model-based p-values (0.039 trend, 0.041 rate) toward ~0.10.
- Restricting to the **one stretch of genuinely constant scoring config** that straddles the P0/P1 boundary (2026-05-15..06-30 vs July–September) gives an exact conditional test of **p=0.085, one-sided** — not significant at the registered 0.05 bar.
- The April–June baseline itself is not one stable regime: it straddles the 05-15 weight/ATR change, Whale Watch dropping to zero candidates/night on 04-20, and the bearish-projection engine moving from v1 to v2 on 05-19. July–September then sees bearish-projection v1 return alongside v2 (2026-07-02, a *source/universe* change, not a `config_json` key), with the bearish candidate share rising from 30.4% to 38.8%. The "P0 rate applied to P1" baseline this whole decomposition is scored against is therefore drawn from a different mix of engines than P1, which undercuts any single-cause reading even before Channel 3's layer disagreement.

Gate 0 stands as registered (not NULL); this caveat is why the report does not read the fall as a clean, stable signal beyond what Gate 0 formally certifies.

### Stratification (rule 7) — regime and tape

`market_regime_daily` is knowledge-time-legal only from **2026-06-09** (backfilled before that; see CLAUDE.md and PREREG §6). Cells below that use it as a stratifier only for nights on/after 06-09; `market_regime_snapshot` (a different, genuinely point-in-time candidate-level field) is a scoring input, not a regime stratifier, and is not conflated with it here.

| stratifier | period | stratum | nights | elite-cand/night | 95% CI |
|---|---|---|---|---|---|
| regime (PIT ≥06-09) | ALL | bullish | 14 | **SUPPRESSED** (n<20) | — |
| regime (PIT ≥06-09) | ALL | strongly_bullish | 50 | 0.340 | [0.220, 0.480] |
| regime (PIT ≥06-09) | P0 | bullish | 7 | **SUPPRESSED** | — |
| regime (PIT ≥06-09) | P0 | strongly_bullish | 8 | **SUPPRESSED** | — |
| regime (PIT ≥06-09) | P1 | bullish | 7 | **SUPPRESSED** | — |
| regime (PIT ≥06-09) | P1 | strongly_bullish | 42 | 0.262 | [0.143, 0.405] |
| SPY tape (trailing 20d) | ALL | down_tape | 28 | 0.464 | [0.286, 0.679] |
| SPY tape (trailing 20d) | ALL | up_tape | 79 | 0.354 | [0.241, 0.468] |
| SPY tape (trailing 20d) | P0 | down_tape | 15 | **SUPPRESSED** | — |
| SPY tape (trailing 20d) | P0 | up_tape | 43 | 0.465 | [0.302, 0.651] |
| SPY tape (trailing 20d) | P1 | down_tape | 13 | **SUPPRESSED** | — |
| SPY tape (trailing 20d) | P1 | up_tape | 36 | 0.222 | [0.111, 0.361] |

The one clean within-stratum comparison that clears the 20-night floor on both sides is the SPY up-tape: 0.465/night (P0, n=43) vs 0.222/night (P1, n=36) — the fall holds inside a constant tape regime. Every P0 regime/tape cell that would let us compare "within the same market regime" is **SUPPRESSED** for having fewer than 20 nights, so a within-regime P0-vs-P1 comparison using `market_regime_daily` is not possible with this sample. May (16 nights) and the first week of September (7 nights) are likewise SUPPRESSED in the month panel for the same floor reason.

### Baseline comparison (PREREG §3)

Baseline is **P0's own elite rate applied to P1's nights**: at the April–June rate of 0.500/night, July–September (49 nights) should have produced 24.5 elite-candidates; it produced 12. Shortfall **S = 12.5**. Every channel above is scored as a share of this S, with 95% CIs from a 2,000-resample date-clustered bootstrap over nights (12/2000 replicates with S≤0 are dropped before CIs are formed — a small conditioning bias the red team flags but does not treat as decisive).

### Month-by-month panel

| month | nights | elite-candidates | elite-cand/night | 95% CI |
|---|---|---|---|---|
| Apr | 21 | 8 | 0.381 | [0.143, 0.667] |
| May | 16 | 9 | **SUPPRESSED** | — |
| Jun | 21 | 12 | 0.571 | [0.333, 0.810] |
| Jul | 21 | 7 | 0.333 | [0.143, 0.524] |
| Aug | 21 | 3 | 0.143 | [0.000, 0.333] |
| Sep (1–10) | 7 | 2 | **SUPPRESSED** | — |
| **P0 (Apr–Jun)** | 58 | 29 | 0.500 | [0.345, 0.655] |
| **P1 (Jul–Sep 10)** | 49 | 12 | 0.245 | [0.143, 0.367] |
| in-sample (≤05-29) | 37 | 17 | 0.459 | [0.270, 0.649] |
| sealed (≥06-01) | 70 | 24 | 0.343 | [0.229, 0.471] |

### What this rules out

- **Not "fewer candidates reaching the engine."** Candidate volume rose (54.1 → 62.7/night); Channel 1 is negative and NOT_A_DRIVER.
- **Not a single identifiable scoring layer.** No Channel-3 component clears the EXPLAINS bar; the two ways of crediting layers (one-at-a-time vs. cumulative) disagree on which layer is biggest, and they interact by +50.9 percentage points.
- **Not the ATR-elite cap, conflict penalty, missing-data penalty, GEX alignment, smart-money confirmation, or completeness** — all flat at 0% restored share in this window.
- **Not a clean, isolated configuration fix.** The only config change touching score arithmetic (05-15) doesn't bracket the fall and precedes the best month in the sample; the four changes that do "bracket" it mechanically are publication-only settings or a one-night toggle and its own revert, and never removed a single elite score from publication (100% published in both periods).

### What the Red Team challenged and how it resolved

The red team's central challenge — detailed above — was that Channel 3a's "brackets the fall" test is an unlicensed global before/after split that fires on any mid-sample date in a declining series, and that it fired only on settings that provably cannot move `overall_score`. That challenge is resolved in this report by using the controller-recorded verdict, INCONCLUSIVE, rather than eval.py's raw output. Two further findings from the red team's review, reported here as red-team analysis (not part of the registered decision rule): PREREG §6's stability requirement ("a channel that explains the fall only on one side of one cut is labelled unstable") was applied by eval.py to the distributional channels but never to Channel 3a itself — all four firing dates fall entirely in the sealed half, with no in-sample counterpart, which is an independent route to "not CONFIRMED" even on eval's own terms. And Gate 0, while passing as registered, is statistically marginal once streakiness and the mixed April–June baseline are accounted for (detailed above).

### Deviations and process items (for the record)

- **GEX-missingness offset definition.** PREREG §4 defines the offset's "firing rate" as the share of rows with a **null `gex_alignment_score`** (April–June 31.1%, July–September 1.2%). `eval.py` instead quantile-maps the **recorded `gex_missing_offset` value** (April–June 0.5%, July–September 1.2%) — the choice that correctly reproduces 6,194/6,211 candidates' `overall_score`, because the literal PREREG definition would add a +5 to April–June rows that never actually carried it. This is the right computational choice but it is a **PREREG deviation that was not declared** in `eval.py`/`SUMMARY.md`; it is declared here. One consequence: the PREREG's own hypothesis (§9) that the offset "stopped firing" is refuted by the recorded data — the offset's firing rate rose, not fell, from April–June to July–September.
- **An extra exclusion.** `eval.py` drops one additional non-session night (2026-04-03, a Good Friday manual run with 0 published picks) beyond the 5 manual-run nights named in the PREREG text; it is in `exclusions_v001.json`'s `non_session_runs` list. Gate 0 still passes with it included (`p_trend=0.0245`, `p_rate=0.0197`).
- **One mixed-state night not excluded.** 2026-06-26 has 17 of 52 candidate rows where the recorded `technical_structure_score` column disagrees with the same field inside `score_details_json` by up to 62 points — evidence of a partial re-run or rewrite, referred to the Data Steward for the next exclusions file. No row that night scored ≥90, so this does not affect the verdict.
- **Second opinion not run.** `scripts/second_opinion.py` requires `OPENAI_API_KEY`, which is not on CLAUDE.md's credential allowlist (non-negotiable #1: "Never look for, request, or use any other credential"). Running it would also send the PREREG, `eval.py`, and `SUMMARY.md` to a third-party service. This is a genuine conflict between the red-team role's own checklist and CLAUDE.md's credential rule, and it is left for Haci to resolve — it was not run, and the sign-off proceeded without it.
- **A contamination vector, avoided.** The `EVALUATED` state.json note from the researcher directed the red team to `results/NOTES.md` for context. The red team's review states explicitly that it did not read `NOTES.md` (or `platform_commits_scoring_agents.txt`), to keep its findings independent of researcher commentary; every finding in `REDTEAM.md` is backed by code lines and eval outputs the red team checked itself. Researcher notes addressed to the red team are flagged as a process issue to fix, not a finding about the data.

### What this suggests next (not registered — informational only)

- `research/BACKLOG.md` already carries **H-014** (family F2), raised by the Researcher *after* seeing this run's output: a successor Channel-3a rule restricted to changes that can mechanically move `overall_score` and held for ≥20 nights, tested with a local before/after step rather than a global split, plus a corrected (declared) GEX-offset definition. It is listed here for visibility only — it is **not registered**, and because it was raised post hoc against this same run, any successor question built on it is post hoc with respect to `manifest_v001` and must say so, or wait for a later data freeze.
- Outside the registered channels entirely: the platform's `ai_agents/omega_agent.py`, `principal_agent.py`, and `super_agent_select_agent.py` were upgraded to a new model on 2026-07-09 (`results/platform_commits_scoring_agents.txt`), inside the July–September window — a prompt/model change this decomposition cannot see by construction (PREREG threat-to-validity #4). Not evidence of anything here; noted as a gap in what this question can detect.

---

*All figures above are NON_QUOTABLE research-window numbers per PREREG §Type and CLAUDE.md rule 12. This question produces no subscriber-facing claim and authorizes no platform code change. No playbook entry follows from this result — it is a diagnostic of platform scoring behavior, not a hand-tradeable rule.*
