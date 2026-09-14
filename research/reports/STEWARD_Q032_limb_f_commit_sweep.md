# Steward — Q032 lock-gate limb (f): DP-50(a)/(b) commit sweep + v1.7 promotion check

_Generated 2026-09-14. Read-only `git log` / `git show` / ripgrep on the platform repo. No live
DB query. Counts and commit facts only — no outcomes._

**LIMB (f): CLEAR**

**Platform HEAD swept to:** `d19c9a945418b09773baffac37f8d723c8a90a9a` (`d19c9a9`, `main` ==
`origin/main` == `origin/HEAD`) — unchanged since the last Q032 Steward report cited it.

**Sweep windows:**
- Since manifest SHA `fa70688` (`fa70688bc252d14f8d67e371afafc194731c324e`, 2026-09-05): **4
  commits** to HEAD — `2d5776c` (PI-001), `4775e49` (merge #26), `22a2e1b` (EN-002), `d19c9a9`
  (merge #27, = current HEAD).
- Since the platform HEAD recorded in Q032's last Steward report / DECISIONS.md record
  (`d19c9a9`): **0 commits**. HEAD has not moved.

## Per-item table (fa70688..HEAD, 4 commits)

| Item (DECISIONS.md item 9 / PREREG section 5.3 R1(f) list) | File(s) it lives in | Touched in window? | Evidence |
|---|---|---|---|
| SAS layer weights (projection 29 / technical 27 / flow 24 / catalyst 10 / fundamental 5 / smart-money 5 / GEX 0) | `services/super_agent_select_scoring.py` | **none** | File not in the diff of any of the 4 commits (`2d5776c`, `22a2e1b`; merges `4775e49`, `d19c9a9` carry identical stats to their child commits) |
| Timeframe multipliers | `services/super_agent_select_scoring.py` | **none** | same |
| `qualification_threshold` | `services/super_agent_select_scoring.py:1629,1646,1691` | **none** | same |
| `publication_floor` | `services/super_agent_select_scoring.py:1518,1694` | **none** | same |
| `bear_publish_threshold` | `services/super_agent_select_scoring.py:1602,1609,1635,1659` | **none** | same |
| `max_output_cap` | `services/super_agent_select_scoring.py:1647,1699` (plus `bear_max_output_cap:1636,1660`) | **none** | same |
| `min_completeness` | `services/super_agent_select_scoring.py:1520,1531,1697` | **none** | same |
| ATR-elite caps (`atr_elite_block_enabled`, `atr_elite_bull_max_score`, `atr_elite_bear_max_score`) | `services/super_agent_select_scoring.py:1405-1419` | **none** | same |
| GEX offset (v1.5 GEX-missingness compensation, gex_alignment None to +5) | `services/super_agent_select_scoring.py:1379-1381` | **none** | same |
| Scoring enable-flags (e.g. regime_catalyst_gate_enabled) | `services/super_agent_select_scoring.py:1038-1040`, `services/super_agent_select_models.py` | **none** | file not in window diff |
| Lane-plan / conviction-card writer | `services/sas_conviction_card.py` | **none** | file not in window diff |
| `services/super_agent_select_scoring.py` (whole file) | — | **none** | not in any of the 4 commits' `--stat` |
| `services/super_agent_select_models.py` (whole file) | — | **none** | not in any of the 4 commits' `--stat` |
| `services/market_regime/scorer.py` (C1 only) | — | **none** | not in any of the 4 commits' `--stat` |

**What the 4 commits actually touched** (full file list, both directions):
- `2d5776c` / `4775e49` (PI-001, "floor the legacy outcome backfill window in-process"): the
  nightly orchestrator script (its outcome-backfill-window step) and one new pin test. This is the
  fix for the `uoa_symbol_daily.fwd_return_*` freeze CLAUDE.md already logs (FREEZE_v001 section
  5) — it widens the nightly backfill's NULL-revisit window; per its own commit message
  ("Restatement: none. This writes no values; it only widens which rows the NULL-only backfill
  revisits") it rewrites no historical rows by itself (a later nightly run using this code could,
  but no such run has landed as a commit). Not relevant to Q032 regardless: Q032's PREREG bans
  `uoa_symbol_daily.fwd_return_*` and reads no UOA table (DECISIONS.md "Checked and not
  corrections", final paragraph).
- `22a2e1b` / `d19c9a9` (EN-002, "speed-to-target internal card"): `app.py` (+2/-0, one router
  registration), `data/sas_speed_control_reference.json` (new, stub), `docs/README.md` (+1 row),
  `docs/SAS_SPEED_TO_TARGET_INTERNAL.md` (new), `routers/admin_sas_speed.py` (new),
  `services/sas_speed_to_target.py` (new, import-pure, read-only), a new test file. Ships
  flag-off (env flag default OFF), admin-token-gated, internal_only / NON_QUOTABLE. Reads
  level_hit_steps_json and published lane plans; writes nothing, defines no new scoring config,
  and does not touch `sas_conviction_card.py` or any scoring file (commit message: "Every
  subscriber-facing service, router and template is byte-identical to `2d5776c`").

**DP-50(a) — rewrites of historical rows in tables Q032 reads:** none. Neither commit performs
a data write; PI-001 changes future-nightly-run behavior only and touches a column family Q032's
PREREG explicitly excludes. No `DATA_NOTES.md` entry is owed for this sweep.

## v1.7 promotion / scheduling check

- Current SCORING_VERSION constant: "v1.6-flow-polarity-projection-credibility"
  (`services/super_agent_select_scoring.py:15`), matching CLAUDE.md's v1.6 weights note and
  `docs/BEAR_PIPELINE_PROCESS.md:245`. No v1.7 scoring-version string exists anywhere in the
  working tree at HEAD.
- Full-tree, case-insensitive search for "1.7" across *.py / *.md at HEAD: the only scoring-
  adjacent hit is `scripts/backtest_stale_setup_gate.py:1,523`, headed "Backtest harness for the
  v1.7 stale-setup gate (DECOMMISSIONED)" — a different "v1.7" (an internal gate-naming scheme,
  not the SAS SCORING_VERSION). Its own docstring: refuted by its own backtest (flagged
  candidates beat non-flagged by 5-6pp), never shipped, all production-code integration was taken
  back out on 2026-05-16, kept only as a reproducible historical artifact / reusable harness
  shape. Last touched by `4bc3f24` (2026-05-16), four months before the `fa70688` baseline —
  outside the sweep window on both counts, and explicitly dead.
- All other "1.7" hits are unrelated float literals (an ATR-multiplier constant in the indicator
  module, a CSS line-height value in `app.py`, and `super_agent_select_scoring.py:643` a
  "+= 1.7" bucket increment inside timeframe-bucket scoring — not a version or threshold
  constant, not touched in window), and Turkish/English risk-reward copy in the OpenAI-facing
  agent service.
- **Branch/ref sweep** (all local plus remote refs — 34 refs total): every branch checked against
  HEAD via `git log --oneline HEAD..branch`. Two carry commits not on HEAD:
  - `feature/bear-v3-wip` — 2 commits (`e8b28c7`, `b986c80`), both a preservation/state-doc
    commit for stashed WIP; no code diff to any scoring file.
  - `feature/market-regime-stack-v1` — 4 commits (`37d6bcf`, `5da672c`, `b424059`, `8a6afd1`), all
    dated 2026-06-02 — three months before the `fa70688` baseline and stale (no activity since).
    These touch `services/market_regime/consumer.py`, `services/super_agent_select_models.py`
    (+5 lines: an env-flag kill-switch for a regime catalyst gate) and
    `services/projection_picks_regime_apply.py`, shipping the catalyst/bear-release gates OFF by
    default. The functionality is already present on `main` at HEAD (same flag names found live
    in `services/super_agent_select_scoring.py:1038-1040` and three other files) — this branch is
    an orphaned, never-fast-forwarded duplicate of work already on `main`, not a pending
    promotion. It is not a v1.7 workstream and predates the sweep window; flagged here for
    completeness only.
  - All other 15 named branches (bear-engine-phase-0, feat/bear-sas-cart, feature/bear-phase1,
    feature/bear-phase1-closeout, feature/bear-phase1-subthreshold, feature/label-demotion,
    feature/market-brief-v1, feature/market-pulse-v2-regime-ab, feature/morning-fade-indicator,
    feature/sas-excursion-backfill, feature/sas-guide-v1_1, feature/super-agent-close,
    fix/digest-repo-root-path, fix/pi-001-backfill-window-floor,
    feat/en-002-speed-to-target-internal) have 0 commits ahead of HEAD — already merged.
- **Answer:** no v1.7 scoring version, and no change to the SAS weights / timeframe multipliers /
  qualification_threshold / publication_floor / bear_publish_threshold / max_output_cap /
  min_completeness / ATR-elite caps / GEX offset / scoring enable-flags / lane-plan writer /
  market_regime scorer, is scheduled, flagged, on a branch, or referenced in docs/TODOs to ship
  inside 2026-09-15..2027-08-23. This is an absence of a schedule found today, not a permanent
  clearance — re-run at every future freeze (DECISIONS.md re-entry item 5).

## Reconciliation with the prior Q032 record

DECISIONS.md's 2026-09-14 record already stated: "(f) returns NONE: HEAD is unchanged at
`d19c9a9`, no commit since `fa70688` touches the scoring path, the lane-plan writer or
`services/market_regime/scorer.py`, and no v1.7 promotion is scheduled." This sweep confirms that
statement item-by-item, with citations, and finds nothing additional: HEAD is still `d19c9a9`
(zero commits since), the 4 commits since `fa70688` are fully accounted for above, and the v1.7
search now additionally covers all branches/refs (34) and a full-tree string search, neither of
which the prior report enumerated. Limb (f) is **CLEAR**.
