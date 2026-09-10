# Hypothesis Backlog

Families group questions for multiple-testing correction. A hypothesis becomes a question
only after the Registrar drafts a PREREG and Haci commits it.

## F1 — Selection edge
- [x] H-001 → Q001 control cohort (registered)
- [ ] H-002 Near-miss cohort: candidates scoring 65–70 vs 70–75 — baseline: adjacent band — n: TBD — mechanism: threshold is arbitrary — noise risk: small band
- [ ] H-003 Layer ablation: drop each weighted layer, re-rank, out-of-sample return — baseline: full v1.6 — n: all published nights — mechanism: dead layers add noise

## F2 — Calibration
- [ ] H-010 Score-band monotonicity under fixed exit rule — baseline: adjacent band — mechanism: score should order expected return
- [ ] H-011 Confidence label (high/medium/low) vs realized return — baseline: label shuffled
- [ ] H-012 Conflict penalty validity: penalized candidates vs unpenalized at same base score

## F3 — Unused signals
- [ ] H-020 GEX alignment (weight 0) vs day-lane outcome — baseline: GEX-missing picks
- [ ] H-021 IV/RV ratio at selection vs realized return by lane — new data needed
- [ ] H-022 Opportunistic vs routine insider buys inside window — new data needed

## F4 — Price behaviour after selection (Explorer seeds)
- [ ] H-030 Day-1 gap >2% at open vs flat open → subsequent realized return
- [ ] H-031 L1 within 2 days → L4 probability
- [ ] H-032 Stop-hit then target within window (whipsaw rate) by stop distance
- [ ] H-033 L4 touched → retrace to L2 → re-advance (Haci's example 1)
- [ ] H-034 Sector cluster nights (≥4 of 8 same sector) vs diversified nights

## F5 — Cross-engine interaction
- [ ] H-040 UOA appearances in prior 5 sessions (0 / 1–2 / 3+) × SAS-selected → return (Haci's example 2) — baselines: 3+ UOA not selected; selected with 0 UOA
- [ ] H-041 Repeat selection within 10 days before earnings → post-earnings return (Haci's example 3) — expected n very small; broaden to all picks with earnings in window first

## F6 — Exits and execution
- [ ] H-050 Conviction Monitor exit vs fixed +10d hold
- [ ] H-051 Lane choice: which lane's plan (day/swing/long) maximises realized return per score band
- [ ] H-052 Repeat-selection streak length vs continuation (extends existing finding)
