# Haci's Master Hypothesis Program — filed 2026-09-14

Haci's words, pasted into the session on 2026-09-14 from his own Claude + ChatGPT analysis, with the
instruction "add these hypotheses into our backlog to run in research desk". Part 1 is his table
verbatim. Part 2 is where each item went and why. Part 3 is what the desk changed to carry them.

## 1. The program, verbatim

VolatilX Research Desk — Master Hypothesis Program

| ID | Structural question | PASS | FAIL | What we do |
|---|---|---|---|---|
| H0 | Point-in-time integrity: Did every input actually exist when SAS made the prediction? | Zero material leakage | Any material future-data contamination | Stop everything, repair pipeline, rerun from zero |
| H0B | Independent signal episodes: Is performance still strong when repeated same-symbol selections are clustered rather than counted independently? | Edge survives episode clustering / clustered bootstrap | Advantage disappears materially | Historical sample was overstating independence |
| H1 | Project NULL: Does full VolatilX beat a dumb model and matched random portfolios? | ≥ +0.10R/trade incremental expectancy vs NULL, positive OOS in ≥2 independent windows, CI preferably >0 | No economically meaningful OOS advantage | Current full SAS has no demonstrated incremental edge |
| H2 | Attribution: Is performance actual alpha rather than market/sector/momentum/beta exposure? | Positive residual alpha after market, sector, size, momentum, vol controls; stable OOS | Residual alpha ≈ 0 | SAS is mainly repackaging known exposures |
| H3 | Ranking validity: Does higher SAS score really mean better expected outcome? | Mean daily Spearman IC ≥0.05, positive in ≥60% OOS windows, top tier materially beats bottom tier | IC ~0 / unstable / materially non-monotonic | Stop presenting score as precise conviction ranking |
| H4 | Discovery: Can VolatilX find major opportunities before they move? | Candidate-universe recall materially exceeds random/base-universe expectation, ideally ≥2× lift | Best future movers rarely enter VolatilX universe | Candidate generation is the bottleneck, not SAS ranking |
| H5 | Ingredient value: Which agents contain independent predictive information? | Agent has stable OOS IC and/or removal materially hurts net expectancy | Agent adds no incremental OOS value | Remove/demote redundant agents |
| H6 | Signal independence: Are 10 agents actually 10 signals, or repeated versions of 3–4 factors? | Low/moderate conditional redundancy + incremental contribution | Highly correlated agents and no incremental information | Collapse architecture into fewer factors |
| H7 | Selection vs execution: Where does economic value come from? | Quantify incremental R from selection and execution independently | — | Determines whether Product A, Product B, or both deserve focus |
| H8 | Founder vs Robot vs Dumb: Can the edge actually be harvested? | Robot VolatilX beats NULL after costs and risk; founder comparison becomes diagnostic | Robot does not beat NULL | Backtest/prediction quality isn't becoming realizable returns |
| H9 | Regime conditionality: Does SAS have edge only in identifiable environments? | Same frozen strategy works reliably in predefined regimes and fails/weakens predictably elsewhere | Regime partitions don't reproduce OOS | Don't invent regime explanations for bad periods |
| H10 | Threshold stability: Is 90 a real boundary or just a historical artifact? | 90 or nearby range remains near-optimal across independent walk-forward windows | Optimal cut moves substantially between windows | Eliminate hard threshold concept; use categorical setups |
| H11 | Direction vs expansion: Does VolatilX predict direction better than magnitude? | Direction remains stable while target/magnitude varies systematically with environment | Both degrade together | Selection itself is deteriorating |
| H12 | Edge decay: Is recent weakness temporary or structural? | Rolling IC/expectancy recover or remain statistically within historical variation | Persistent deterioration across independent windows | Retire/retrain affected component |
| H13 | A/B/C architecture: Do setup-specific models outperform universal 0–100 scoring? | Frozen categorical setups materially improve OOS expectancy/calibration/stability | Universal score performs equally or better | Keep scoring architecture |
| H14 | Economic objective: What does VolatilX actually predict best? | Determine strongest stable objective among return, direction, target-before-stop, R, MAE, etc. | No objective has persistent edge | Product A should not be marketed as predictive system |

## 2. Where each item went

Family is by the primary endpoint's subject (DP-29). "Diagnostic" means the Q005 shape: a
PASS / FAIL or a decomposition with no MPE, entering no Benjamini–Hochberg correction set. The
queue order is `research/lib/desk_queue.py` PRIORITY; all sixteen sit ahead of everything else
under DP-47 because they are Haci's own items.

| Haci's | Desk id | Family | Shape | Status on filing | Queue | Existing work it builds on |
|---|---|---|---|---|---|---|
| H0 | H-069 | F8 | diagnostic, Data Steward runs it | open — **runs first** | 1 | FREEZE_v001 §7 (sampled), KT audit (re-run nights), exclusions v002/v003, DP-06 split, PI-005, PI-013 |
| H0B | H-070 | F8 | cross-cutting sensitivity → **DP-51** | open (bookkeeping; the rule is already in force) | 2 | Q003, H-041's event-unit argument, Q023 §2.5 episode bootstrap |
| H1 | H-071 | F1 | — | **merged into Q024** (H-067) | — | Q024 arms + clause-7 money gate; Q006 |
| H2 | H-072 | F1 | — | **merged into H-068 / Q025 (DEFERRED)** | — | Q025's measured 0.000 match rate; re-check trigger; EN-016 |
| H3 | H-073 | F2 | two primaries (IC, tercile contrast) | open; drafts with H-010, H-012 | 3 | H-010 snapshots (sealed, post-hoc), Q005 |
| H4 | H-074 | F8 | one primary (recall lift) | open; needs the Steward's universe price freeze first | 6 | Q022/Q024 sector-blob pin, EN-016, `candidate_universe_builder.py` |
| H5 | H-075 | F1 | two co-primaries per layer | open; drafts with H-003, H-020 | 5 | H-003, H-020, Q005, PI-008 |
| H6 | H-076 | F8 | diagnostic (no outcome column) | open | 4 | Q005's no-outcome argument; H-075 |
| H7 | H-077 | F8 | synthesis by the Reporter, no PREREG | open; first cut after Q006/Q002/Q004/Q011 | 13 | Q006, Q024, Q004, Q011, Q018, Q012, Q015, Q019 |
| H8 | H-078 | F6 | three arms | **new data needed** (Haci's fills) → DEFERRED with the file named; robot-after-costs arm registers after Q006 | 14 | Q024 clause 7, Q006 E2, Q004 |
| H9 | H-079 | F2 | one primary (regime × edge, two windows) | open; prospective | 8 | Q023, rule 7, PI-005 |
| H10 | H-080 | F2 | two primaries (cut dispersion, 90 vs 85–89) | open; may defer on elite exposure | 9 | Q015, PI-010, Q005, H-002 |
| H11 | H-081 | F8 | one primary (interaction), two-sided | open | 10 | Q006, Q002, Q004 |
| H12 | H-082 | F2 | one primary (change-point + persistence) | open; prospective decision | 7 | Q005, H-014, weekly §7, PI-010, **EN-017** |
| H13 | H-083 | F8 | one primary, behaviour | open; after H-076 and H-080; prospective ≈ 12 months | 12 | H-076, H-080, **EN-018** |
| H14 | H-084 | F8 | diagnostic (closed objective list) | open | 11 | Q006 §4, Q002, Q009 |

Two translations the desk made and Haci should know about:

- **R → ATR per trade.** H1, H7 and H14 speak in R. The desk assumes no stop (DP-02), so R has no
  denominator; the money unit is ATR per trade under the platform's committed scale-out (DP-10,
  0.25 ATR MPE). Haci's "+0.10R" is therefore not carried as a number; Q024's clause-7 gate is the
  registered equivalent.
- **"10 agents" → 7 scored layers + 2 modifiers.** SAS v1.6 scores flow, technical, GEX,
  projection, fundamentals, catalyst and smart-money (volatilx `services/super_agent_select_scoring.py:751-1051`),
  then applies a cross-layer bonus (`:1078`) and a conflict penalty (`:1116`). The `ai_agents/`
  modules feed those layers. H-075 and H-076 test the layers as the ingredients and treat the
  agent-level fields in `component_scores_json` as a secondary cut.

## 3. What the desk changed to carry the program

- `research/BACKLOG.md` — H-071, H-072, H-075 under F1; H-073, H-079, H-080, H-082 under F2;
  H-078 under F6; new family **F8 — System validity** with H-069, H-070, H-074, H-076, H-077,
  H-081, H-083, H-084.
- `research/DECISION_POLICY.md` — **DP-51**: every PREREG drafted from 2026-09-14 reports each
  primary with an episode-clustered CI beside the date-clustered one; a primary that clears MPE on
  only the first is INCONCLUSIVE. For PREREGs already locked, the Red Team computes it at sign-off.
- `research/ENHANCEMENTS.md` — EN-017 (edge-decay monitor, plumbing) and EN-018 (setup labels /
  per-setup ranking, behaviour, gated on H-083).
- `research/lib/desk_queue.py` — PRIORITY now leads with H-069..H-078 in the order above.
- `research/INBOX.md` — one ticked line pointing here.

Nothing was registered or locked in this step; the next `/desk-run cycle` drafts H-069 first.
