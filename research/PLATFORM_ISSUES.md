# Platform issues register

Defects and hazards in the VolatilX platform that the desk has found while doing its own work.
This is the follow-up list Haci asked for. It is separate from the LEDGER (verdicts on research
questions) and the BACKLOG (hypotheses). Anything here that becomes a *behaviour change* to
scoring or selection still goes through a research question and a full IMPLEMENTATION_BRIEF
(CLAUDE.md rule 11). Plain bug fixes take the short route below.

## How an issue gets fixed

1. Desk finds it, records it here with evidence (`path:line`, dates, a reproducing query).
2. Haci decides: **fix** (bug — short route), **research first** (it might be a feature, not a
   bug), or **accept** (document and move on).
3. Short route: `@brief-writer fix-brief PI-NNN` produces `research/briefs/PI-NNN_slug.md` — a
   self-contained prompt for the coding agent in the platform repo, with the reproducing query,
   the expected behaviour, a test, and a rollback. No feature flag is needed for a fix that
   restores intended behaviour, but the brief still names a before/after check.
4. Haci runs the brief in the platform repo, records the PR / SHA here, and the steward
   confirms on the next freeze that the data changed as expected. Then status → `VERIFIED`.

Statuses: `OPEN` · `HACI_DECIDED:<fix|research|accept>` · `BRIEF_WRITTEN` · `IMPLEMENTED:<sha>` · `VERIFIED` · `ACCEPTED`

| ID | Severity | Status | Issue |
|---|---|---|---|
| PI-001 | high | IMPLEMENTED:2d5776c | `uoa_symbol_daily.fwd_return_*` still ~95% degraded; 30d relapsed to 0% from 07-27 — brief: `research/briefs/PI-001_fwd_return_backfill_window.md` |
| PI-002 | high | HACI_DECIDED:fix | No coverage watchdog fires on PI-001 (none found in the codebase by that name) |
| PI-003 | med | HACI_DECIDED:fix | `atr_pct` corrupted around splits (ATR computed on raw bars) |
| PI-004 | med | HACI_DECIDED:fix | Manual re-runs indistinguishable from nightly runs in `super_agent_select_runs` |
| PI-005 | med | HACI_DECIDED:accept | `market_regime_daily` not point-in-time before 06-09 (backfilled) |
| PI-006 | low | HACI_DECIDED:fix | 16 published picks have no target ladder |
| PI-007 | low | HACI_DECIDED:fix | `industry` populated for only 12% of candidates |
| PI-008 | low | HACI_DECIDED:accept | Smart-money layer weight forced to 0; CLAUDE.md weights text says 5 |
| PI-009 | research | HACI_DECIDED:research | L1/L2 targets sit inside one day's range (median 0.31 / 0.55 ATR) — targets are not ATR-scaled |
| PI-010 | research | HACI_DECIDED:research | Elite (90+) count falling: Apr 8 · May 13 · Jun 12 · Jul 8 · Aug 3 · Sep 2 |
| PI-011 | high | HACI_DECIDED:fix | Printed swing stop on the wrong side of the pick-night close for 67 of 382 published picks (17.5%) |
| PI-012 | med | HACI_DECIDED:research | 2026-06-26: three qualified, ranked picks the night's own run audit does not record; no run-history table |
| PI-013 | med | OPEN | `uoa_symbol_daily.score_swing` / `score_long` overwritten in place by the next-morning OI-confirmation pass; no point-in-time copy |
| PI-014 | high | OPEN | Conviction Monitor's polarity arm silent since 2026-06-01: `polarity_unavailable_coverage_low` on 100% of in-scope rows, 0 polarity HOLD/EXIT rows — the EXIT tier is the technical arm alone |
| PI-015 | high | OPEN | Projection layer (v1.6 weight 29, the largest) unscored — `available: false` — on 72.2% of published and 74.3% of capped main-lane rows; `overall_score` is a six-layer blend on ~3 of 4 picks |

## Detail

### PI-001 — fwd_return freeze not fixed
**Evidence:** FREEZE_v001 §5. `fwd_return_30d_pct` coverage 99% → 0% from 2026-05-20;
14d from 06-12; 5d from 06-26; writes resume 07-06 at ~5% of baseline; 30d back to 0% for
`trading_date ≥ 07-27`, well past maturation. CLAUDE.md said "fixed" — corrected 09-10.
**Desk impact:** none now — the desk computes forward returns from its own price freeze.
**Platform impact:** anything on the product that reads these columns (UOA performance surfaces)
is showing mostly nulls. **Recommend: fix.**
**Implemented 2026-09-13, `2d5776c`** — `resolve_backfill_window()` clamps any caller's window into
[65, 100] sessions in-process, so the stale Azure WebJob wrapper can no longer shorten it; the
effective window is now printed on every run. Two files, no scoring path touched.
**MERGED, DEPLOY UNKNOWN (corrected 2026-09-14).** `2d5776c` is on `main` via merge commit `4775e49` (PR #26, "Merge pull request #26 from kerzey/fix/pi-001-backfill-window-floor", 2026-09-13 18:02:57 -0500); `git show --stat 4775e49` confirms exactly the two files the brief named (`scripts/run_nightly_pipeline.py`, `tests/test_nightly_pipeline_backfill_window.py`) and nothing else. Whether this has reached the production WebJob (brief §3 Step A') and whether a nightly has run it are unknown to the desk from a read-only git+DB check. See `research/reports/VERIFY_PI-001.md` §8 for the 2026-09-14 pass -- verdict PENDING, not VERIFIED.

**Residual hole — one reconciled statement (2026-09-13, after two verify passes disagreed).**
Both passes counted correctly; they counted different sets, and both summaries were imprecise.
Recomputed once more from `research/data/v001_uoa_symbol.parquet`, counting only dates whose
30-session window had closed by the freeze `as_of` 2026-09-10:

| set | dates | missing cells | range |
|---|---|---|---|
| due and **zero** 30d coverage | **35** | **17,402** | 2026-04-15 .. 2026-07-29 |
| due and partially filled, under 95% | 15 | 7,098 | the ~24-symbol bulletin trickle |
| **all** due dates under 95% | **50** | **24,500** | 2026-04-15 .. 2026-07-29 |
| of the zero set, **cannot** be reached by any nightly window | 15 | 7,460 | 2026-04-15 .. 2026-06-08 |

The second pass's headline "36 dates / 17,896 cells" double-counts: its own date list enumerates
35 dates including the 2026-04-15 / 04-17 pair, then adds that pair again in the caption. Its list
is right and matches this recount exactly. The first pass's "15 dates / 7,460 cells" is the subset
no nightly can ever reach, and was stated as though a deploy had already landed. It had not.

**Sweep range: `--start-date 2026-04-15 --end-date 2026-07-29`.** Wider is free here — the backfill
is NULL-only, so dates that would have self-healed are simply skipped — and it makes the result
independent of when the deploy lands. Use this range, not either narrower one. Still Haci's call,
still never `--force`.

**Not `VERIFIED`:** merge, deploy, one nightly, then the read-only coverage check, in that order.
Full working in `research/reports/VERIFY_PI-001.md` §6 and §7.

**On the `patch7.py` flag raised by the second pass:** staging an enforcement-file edit as a script
under `docs/admin_pass/` for Haci to run is the desk's documented mechanism for rule-15 files —
patch4, patch5 and patch6 all do it, and `docs/HOW_THE_DESK_WORKS.md` names it. The desk did not
run it. Haci applied it himself on 2026-09-13, before establishing that the research URL and
production are one database; patch7 has since been corrected and now replaces its own superseded
section on the next `--apply`.

### PI-002 — no watchdog caught PI-001
**Evidence:** a ~95% shortfall persisted for 3+ months. `grep` for a fwd_return coverage
watchdog finds only `scripts/phase2_signals/feasibility.py:7`, a one-off feasibility note.
**Recommend: fix** — a nightly coverage check with a threshold (the desk's own
`research/lib/daily_check.py` shows the shape: trailing median, floor, RED on a drop).

### PI-003 — ATR corrupted around splits
**Evidence:** EXPLORE_001 §9. BKNG `atr_pct` up to 0.49 (true ≈ 0.04–0.06), CVNA up to 0.55.
Cause: ATR over raw bars spanning a split. The W60 grader already de-splits bars
(`scripts/backfill_w60_outcomes.py:185-193`); the ATR path does not.
**Platform impact:** any ATR-based target or sizing on a recently split name is wrong for ~14
sessions. **Recommend: fix**, reusing the grader's de-split.

### PI-004 — manual runs look like nightly runs
**Evidence:** runs for 05-11, 05-12, 05-13, 05-14, 07-06 finished after the next session had
opened (`finished_at`), with mixed-date `spot_close` (TER 07-06: −9.6%). Haci confirms these
were manual development re-runs. Nothing in `super_agent_select_runs` marks them as such.
**Desk impact:** handled by `research/data/exclusions_v001.json`.
**Recommend: fix (small)** — a `run_kind` column (`nightly` / `manual` / `backfill`) written by
the entry point, so the next manual run is self-declaring. Also lets the product hide manual
runs from subscriber-facing history.

### PI-005 — regime history backfilled
**Evidence:** FREEZE_v001 §7. Three `regime_version` rows per date for 01-02..06-08, all
written 06-02 / 06-08. Live same-night writes only from 06-09.
**Recommend: accept**, with the desk rule "regime-stratify from 06-09 only". Nothing to fix
going forward; the label is now written on the night.

### PI-006 — picks without a ladder
16 published picks lack lane targets in `public_payload_json`. A subscriber saw a pick with no
plan. **Recommend: fix** — publication should require all three lanes' targets, or mark the
pick as plan-pending.

### PI-007 — `industry` mostly empty
12% populated. Blocks sector-cluster questions (H-034) and any sector-aware product feature.
**Recommend: fix** — populate from the fundamentals source already used for `fundamental_quality`.

### PI-008 — smart-money weight is zero
`services/super_agent_select_scoring.py:709-710` forces the weight to 0 when
`enable_smart_money_enrichment` is off; the column has been null since April. Not a bug — a
disabled feature — but CLAUDE.md's "smart-money 5" and any marketing of a seven-layer score
overstate it. **Recommend: accept + docs**, or decide whether to enable.

### PI-009 — targets are distance, not forecast *(research first)*
EXPLORE_001: L1/L2 median 0.31 / 0.55 ATR from the close. The strategist prompt asks for two
targets per lane with no volatility scaling (`ai_agents/principal_agent.py:530-575`). If the
sealed period confirms H-053, the change is ATR-scaled target placement — a scoring/plan
behaviour change, so: PREREG → verdict → HUMAN_APPROVED → full brief with a shadow ladder.
**Haci's view (2026-09-10):** near targets being reachable by other stocks is expected; the
differentiator is *how fast* SAS picks reach them. Product direction if that holds: quick
L1/L2 exits and capital recycling on sub-elite picks, deeper holds on elite picks, and
strategies built on speed. Registered as H-065 / H-066; the research question tests speed
against a distance-matched control, unconditionally, before any target redesign.

### PI-010 — elite is thinning *(research first)*
Published 90+ picks per month fell from 12–13 (May–Jun) to 3 (Aug) and 2 (Sep to the 10th);
the candidate median score fell 67.3 → 62.7 on 09-10 (daily check). Haci wants to know why.
Candidates: score-distribution drift after the 06-01 catalyst fix, weaker tape, GEX nulls
(+5 completeness offset), or universe changes. This is a Registrar question (calibration
family F2), not a fix.

### PI-011 — printed stop on the wrong side of the entry
**Evidence:** STEWARD_Q009_exposure §R1(a). 67 of 382 published picks with a swing lane and an L3
(pick nights 2026-06-01..08-12, matured) carry a printed swing `stop` on the **wrong side of the
pick-night close** — for a bullish pick, a stop above the close, i.e. already breached at publication.
**Cause (read-only):** the stop is written by the Principal Strategist off the lane `entry`, which may
stray more than 5% from spot (`services/super_agent_select_service.py:101-111`), and is passed into
`public_payload_json` **unvalidated** (`:94-95`, `:158`), while targets *are* checked against spot and
entry (`:113-152`). It is shown to subscribers on the report card
(`report_center_frontend/components/ReportCard.tsx:254-255`).
**Desk impact:** these picks are excluded from Q009, which therefore speaks for 303 of 383 published
picks (79%).
**Recommend: fix** — a side-and-distance guard on the written stop, mirroring the existing target
guard. **Timing note:** rule 11 applies with unusual force here — a stop-side guard must not go
flag-on before Q010's decision date, or Q010 would be replicating Q009 on a different population
(Q010 §10.6).

### PI-012 — 2026-06-26: ranked picks the run audit does not record
**Evidence:** STEWARD_Q009_exposure §R3 ruling 1. The frozen `sas_candidates` table holds 11 qualified
rows with a `selected_rank` for that trading date; the run's contemporaneous `stats_json` records 8,
all bullish. The three extra bearish rows (DPZ, COIN, AAPL) carry complete lane plans, including swing
stops, with the payload `rank` matching the outer `selected_rank`. It is the only night in 113 with
this mismatch.
**Desk impact:** the whole night is excluded (`exclusions_v003.json`, `uncorroborated_publication_runs`);
usable nights 103 → 102. Q006 and Q007 are locked citing earlier exclusions files and include that
night — flagged to the Red Team for their reviews, never edited.
**Recommend: research first** — the write path cannot be reconstructed from the desk side, because
`super_agent_select_runs` is updated in place with no run-history table. Two questions for the platform:
what wrote those rows, and should there be an append-only run-history/audit table — its absence is what
makes this and the KT-audit re-run nights unrecoverable rather than merely detectable.

### PI-013 — UOA scores rewritten next morning with no audit trail
**Evidence:** Registrar draft of Q014 (H-040), 2026-09-13. volatilx `services/uoa_screener.py:2236-2239`
multiplies `score_swing` and `score_long` in place by `oi_mult` (0.90 / 1.00 / 1.05 / 1.10, stored in
`oi_confirm_mult`, `:2223-2232`) during the next-morning open-interest confirmation pass, and the
bulletin's lists are re-ranked from the mutated scores (`:2245-2303`). `label_*` is written once,
pre-multiplier (`:1728-1734`). The row therefore carries the *morning* score under a column that
every downstream reader treats as the 16:05 ET screener output. FREEZE_v001 §7 flagged the OI lag
for older rows only.
**Desk impact:** any study conditioning on `score_swing` / `score_long` must divide out
`oi_confirm_mult` to recover the pick-night value (Q014 PREREG §2.1 does exactly that; no rule-14
exception needed because the multiplier is stored). Rows where `oi_confirm_mult` is null cannot be
told apart from unconfirmed ones.
**Recommend: fix** — keep the 16:05 score in its own column (`score_swing_pt`, `score_long_pt`) or write
the confirmed score to a new column and leave the original untouched; either way the point-in-time
value must survive. Fix, not research: no behaviour changes, only where a value is stored.

### PI-014 — the Conviction Monitor's polarity arm has been dark since 2026-06-01
**Evidence:** `research/reports/STEWARD_Q019_exposure.md` §6 and §8, counts only, on the pinned
freeze (`manifest_v001`, table key `conviction_monitor`, 3,339 rows; no live query, DP-50(c)).
`polarity_unavailable_coverage_low` appears in `reason_codes_json` on **100% of in-scope monitor rows
in every month 2026-06 through 2026-09**, with **0 exceptions**; `polarity_tier` is `WATCH` on
**every** row dated ≥ 2026-06-01 (0 HOLD, 0 EXIT); the only 35 polarity-EXIT and 53 polarity-HOLD rows
in the whole freeze are in **May 2026**, when the arm still worked (80.3% unavailable then, so it was
already degrading). Consequence: **284 of 284** primary EXIT flags on pick nights
2026-06-01..2026-08-26 fired via the technical arm alone, on a tier that prints EXIT for **61%** of
published picks within five sessions.
**This is not the 2026-05-16 polarity rollback.** `docs/POLARITY_ROLLBACK_2026_05_16.md` disabled
v1.6 polarity **in SAS scoring** by flipping `SuperAgentSelectConfig.flow_polarity_enabled` to
`False`. The monitor does not read that flag — it recomputes polarity locally
(`services/conviction_monitor_service.py:906-937`, `:1177-1186`) — and it kept writing polarity
HOLD/EXIT rows for two weeks *after* the rollback shipped, dying at the 2026-05-31 / 06-01 boundary.
A "working as intended" reading of the silence is wrong.
**Cause (read-only, and not in the monitor):** the monitor's tier code has not changed since
**2026-05-16** — `git log --follow services/conviction_monitor_service.py` returns exactly three
commits, all that day (13234cc / baf17b8 / 2cb7a7e), and nothing since; `scripts/run_conviction_monitor.py`
and `routers/conviction_monitor.py` show no commits since the manifest SHA `fa70688`. So this is an
**input** failure, not a logic change. The gate is `services/conviction_monitor_service.py:184-185` —
`coverage is None or coverage < config.polarity_coverage_threshold → ("WATCH", ["polarity_unavailable_coverage_low"])`
— where `coverage_ratio = decomp_premium_total / contract_premium_total` (`:928-937`) is built by
`services/symbol_context_builder.py:136-175` from **`uoa_contract_daily.buy_premium` /
`sell_premium` / `premium_total`**. A 100% failure means the **aggressor decomposition** is empty or
near-empty for the monitored symbols on every date since 2026-06-01, or `premium_total` has been
inflated relative to it. Same table family as **PI-001** (`uoa_symbol_daily` write degradation from
2026-05-20, still ~5% of baseline) and still uncovered by any watchdog (**PI-002**) — the third silent
UOA-side degradation, and the first to reach a paid surface's logic.
**Reproducing check — for the Data Steward on `$RESEARCH_DB_URL`, read-only.** `uoa_contract_daily` is
**not** in `manifest_v001`, so this is an operational diagnosis, not a study input and not a brief's
before-snapshot; it is addressed to the Steward and never to the coding agent (DP-49). By month from
2026-04-01, over the SAS published-pick symbols: the share of `uoa_contract_daily` rows with
`buy_premium + sell_premium > 0`, the median `(buy_premium + sell_premium) / premium_total`, the row
count per date, and the date the median first falls below `polarity_coverage_threshold`. Plus, from
the read-only platform repo, `git log --follow services/symbol_context_builder.py` and any change to
`ConvictionMonitorConfig`'s polarity thresholds between 2026-05-20 and 2026-06-10 — R1 item (7) dated
the monitor service only, so the builder and the config are the two unexamined code paths. If a fix is
briefed, pin that coverage aggregate in the successor freeze so the before/after is reproducible
(DP-50(c)).
**Desk impact:** Q019 (locked 2026-09-13, decision 2027-05-24) tests "the Conviction Monitor's EXIT
tier" and therefore tests **the technical arm alone** for the life of its window; the restriction is
written into its §1/§8/§9 and travels with the verdict (Q019 DECISIONS #10). No other locked question
reads this table.
**Recommend: fix — and fix the input, not the gate.** The coverage threshold is doing its job;
lowering it would publish a polarity tier computed from a fraction of the premium. **DP-50(b) timing
constraint, named here as the policy requires:** restoring polarity changes which picks receive
`EXIT` — a column a locked PREREG reads — so the PI-011 / Q010 pattern applies and the choice is
Haci's. **Either** the restoration is held **flag-off until Q019's decision date, 2027-05-24**; **or**
it ships with a dated `DATA_NOTES.md` entry (column, date range, ship SHA), Q019's window start moves
to the first pick night after the ship and its schedule is recomputed at the measured 0.6885
nights/session — ≈ 8 months to refill the floor — and if that pushes the decision date past
**2027-09-13**, Q019 goes to DEFERRED (Q019 DECISIONS #12(a), DP-43's ceiling). On the arithmetic, a
ship before ≈ **2027-03-08** is survivable and one after it is not. **The desk does not ask for the
fix to be held**: a live surface with one of its two arms silent is worse than a research question
that may have to restart. The cost is written here so the choice is made with it in view.

### PI-015 — the projection layer, v1.6's largest weight, is unscored on three of every four picks
**Filed 2026-09-14 by the registrar (autonomous run, DP-40..48), on the decision-maker's
recommendation at `research/questions/Q035_setup_architecture/DECISIONS.md`, "Platform issue
recommended to the Registrar" (DP-48). Severity high, status OPEN. Recommendation only — the decision
is Haci's, and `HACI_DECIDED` stays unset until `/desk-run prompt PI-015`.**

**Measured numbers, and where the desk read them.** `research/reports/STEWARD_Q035_exposure.md`
(Headline and limbs (a), (c), (f)), on the pinned `manifest_v001`, pick nights 2026-06-01..2026-09-10:
**72.2% of 579** `selected` bull-lane rows and **74.3% of 692** `capped_by_max_output` rows carry
`score: null, available: false, reasons: ["Projection context unavailable"], weight: 0.0` in
`score_details_json.weighted_dimensions.projection`; **not** concentrated in one timeframe (short,
swing and long all 71–79%); read directly off the frozen rows before any Q035 screen touched them.
**Second, independent desk measurement of the same hole:**
`research/questions/Q029_layer_value_ablation/PREREG.md` records `projection_score` non-null on
**62.74%** of its segment rows, clearing 70% in **no month measured** (49.44% → 65.11% peak,
plateauing below the floor from July) — which is why Q029 registered `projection` as **UNEVALUABLE**
on its E1 and E2 endpoints. Two questions, two populations, one gap. *(Related but not new:
`smart_money_confirmation_score` is null on 100% of all 6,479 frozen rows — that is PI-008's weight-0
layer, recorded here only because it is what made Q035's completeness screen reading-dependent.)*

**Why it is high, and the one thing the check must settle.** The published ranking is produced by a
seven-layer v1.6 blend in which projection carries 29 of 100 points. On roughly three of every four
published picks that layer is absent with `weight: 0.0`. **The desk cannot tell from the frozen
payload alone whether the remaining six weights are renormalized or the layer simply contributes
zero**, and the two have opposite consequences: renormalization means the published ranking is, most
nights, a **six-layer score** that is not the documented v1.6 blend; a plain zero means every affected
row is silently docked up to 29 points relative to the rows that do have projection, so a pick's rank
depends on whether its projection context happened to load. Either way the ranking every
subscriber-facing surface rests on is not the one the weights table describes, and no watchdog fires
(PI-002's family).

**Desk impact.** Q035 (H-083, setup architecture) is **DEFERRED** — `research/questions/DEFERRED.md`,
"Q035 / H-083" — because the night's publishable choice set cannot be reconstructed under a
completeness screen when three-quarters of it fails that screen: median `|P_t|` **5** against a floor
of 11, reorder rate **0.2683** against 0.50, and the reconstruction limb's registered population
**empty (0 of 41 nights)**. Q029 carries `projection` as UNEVALUABLE on two endpoints for the life of
its window.

**The platform check — repo-only, no database step (DP-49).** Everything below is satisfiable from the
read-only platform repo by the coding agent: (i) trace the writer of `available: false` /
`"Projection context unavailable"` in `services/super_agent_select_scoring.py` (the projection
subscore path around `:925` and the no-projection-origin / no-projection-context branch at
`:711-712`) back to the projection context builder and the `ai_agents/projection_expert` path, and
state in the brief which of three it is — a missing upstream projection row, a config flag or coverage
threshold, or an exception swallowed into the unavailable branch; (ii) `git log --follow` on the
projection scoring path, the projection context builder and the projection agent from 2026-04-01, to
date the step-up (the desk's own two measurements suggest it predates 2026-06-01 and worsens through
July); (iii) resolve the renormalize-vs-zero question **from the code**, and state the answer
explicitly; (iv) a pure-function unit test that feeds a synthetic projection context to the scorer and
asserts `available: true` with a non-null score, plus `git show --stat` proving no other scorer file
changed. **The coverage before/after is the Data Steward's, on the pinned parquet (`manifest_v001`)
and the successor freeze (DP-50(c))** — the brief names that parquet as the before-snapshot and never
asks anyone to capture one.

**DP-50(b) ship timing — named, decision left to Haci.** A repair rewrites `projection_score`
historically, and with it every setup label and `overall_score` derived from it. In-flight **locked**
questions that read the projection subscore: **Q029** layer value ablation — `projection_score` is a
Tier-1 layer with its own `E3_projection` endpoint and a **fixed and closed** EVALUABLE / DEAD /
UNEVALUABLE register that its schedule note says is "never revised", decision **2027-04-12**, hard
stop **2027-05-24**; **Q028** layer signal independence — `projection_score` is a Tier-1 column and
part of the object of the test, decision **2026-09-28**, hard stop **2026-10-12**; **Q026**
point-in-time integrity — `projection_score` read in its committed `eval.py`, decision **2026-09-21**,
hard stop **2026-10-05**. Every question that reads `overall_score` or the published slate is touched
as well (Q027 and Q031 share Q029's 2027-05-24 hard stop), because an unavailable layer changes the
blend that produces both. **The constraint the brief should carry: flag-off until 2027-05-24**, the
latest in-flight hard stop — or, if Haci wants it sooner, the repair ships and Q026, Q028, Q029, Q027
and Q031 each split at the ship date under DP-06 / DP-50(a), which **Q029 cannot absorb** (its
register is closed at `record` and would have to be re-derived, i.e. Q029 defers). The two nearest
dates are cheap: **Q026 2026-10-05 and Q028 2026-10-12** pass within a month, after which only the
2027-05-24 cohort binds. This is the trade-off, stated; the decision is Haci's under DP-48, and the
desk files nothing further until `/desk-run prompt PI-015`.

**Recommend: fix — the input, and then the documentation.** Restore projection coverage; and state in
the same change which of renormalize-or-zero the scorer does today, because that is what decides
whether the shipped ranking ever matched the documented v1.6 blend. If the answer turns out to be
"renormalize, deliberately", the second half is a weights-table and docs correction (the PI-008
pattern), not a scoring repair. Either way, **the behaviour change that would follow from Q035's
hypothesis is not what is asked for here** — this is a completeness fix, and any change to how the
slate is *ordered* still needs a research question and a full brief (rule 11).
