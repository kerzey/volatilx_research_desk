# Q019 — conviction_monitor_exit: when the Conviction Monitor flags a recent pick EXIT, is closing it at the next open worth more than holding to the tenth session?

**Status:** PREREG_DRAFT (lock by committing this file, `PREREG_LOCKED --by desk`, DP-46). **The conditionality is spent: R1 is answered and the lock is unconditional.** On `research/reports/STEWARD_Q019_exposure.md` (counts only, pinned freeze, DP-50(c)) the Steward measured `A` = **42** matched-contributing nights over **61** elapsed sessions 2026-06-01..2026-08-26 → `r` = **0.6885** per elapsed session, under the §2 NOFLAG-at-`s` definition and the §3 same-window control bound. The `r ≥ 0.26` ceiling test is **passed**; the last tier-logic ship is **2026-05-16**, fifteen days *before* the window start, so the start stays **2026-06-01**; and the drafted window end, decision date and extension date **stand unmodified**, because a faster rate never pulls a date in (DP-43, DP-45).
**Decisions:** DECISIONS.md
**Claim scope, measured at lock and carried by every restatement of the verdict (§1, §8, §9):** over this window the Conviction Monitor's EXIT tier is **the technical arm alone**, it is a **day-1 or day-2** event, and the matched estimate speaks for **ordinary-damage** flags only.
**Family:** **F6 Exits and execution** (hypothesis **H-050**, filed in F6 in `research/BACKLOG.md`). DP-29 is unambiguous here: both primaries contrast two *exit plans* on the same positions, which is F6's subject — the ground on which Q009 and Q012 were re-filed. H-050 is counted once, in F6.
**Manifest (selections + monitor):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e) — table key `conviction_monitor` (`SELECT * FROM conviction_monitor_daily WHERE trading_date <= :as_of`; 3,339 rows, FREEZE_v001 §1).
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`, `uncorroborated_publication_runs.trading_dates`) — the newest exclusions file (DP-22) — **unioned with the add-only successor exclusions file issued with the successor selection freeze** (DECISIONS #5): the identical three lists built by the identical criteria over the post-2026-09-10 nights, which may only **add** nights and may never remove one from a v003 list. The **criteria** are fixed at this lock; the **dates** cannot be, because the window runs eight months past v003. `eval.py` reads both files as inputs — no hard-coded file name, no hard-coded date.
**Registered by:** registrar · **Approved by:** desk (DP-46) · **Date:** 2026-09-13

---

## 1. Hypothesis (plain English)

**When the Conviction Monitor prints EXIT on a pick you are already holding, selling it at the next
morning's open beats holding that position to its tenth session — and it beats selling any pick that
had already fallen just as far by the same day.**

BACKLOG H-050 reads, in full: *"Conviction Monitor exit vs fixed +10d hold."* It names no trigger
field, no exit price, no baseline, no population and no decision. This PREREG fixes all of them
(§2–§4). No sign is presumed; both primaries are two-sided, and a confirmed negative — the monitor's
EXIT flag marks names that recover, so acting on it costs money — is a finding of the same weight and
retires a live product surface.

**The second half of that sentence is the question.** A pick that earns an EXIT tier has usually
already moved against the thesis: the technical arm fires on structure breaks, level breaches, bias
flips and indicator reversals measured *against the qualifying-day snapshot*
(volatilx `services/conviction_monitor_service.py:328-620`), all of which are functions of the price
path since the pick night. The conditioning variable is therefore **part of the price path**, so
**DP-12 governs**: the primary contrast is against a control **matched on the damage already done**,
and the total (unmatched) effect is **descriptive and licenses no rule**. Without that, a positive
result would say no more than "stocks that have fallen keep falling, so exiting after a fall pays" —
a momentum fact available without the Conviction Monitor, and not a claim this platform may make
about it. DP-12's cost travels with the rule: the matched pool is smaller, flagged picks with no
valid control are dropped and counted, and the sample floor arrives later.

**Two endpoints are primary** (§4), both on the stretch the exit rule avoids — from the open of the
session after the flag to the close of the pick's tenth session — and both against the same
damage-matched control:

- **(P1, the money)** the flagged pick's **avoided move**, in ATR, minus the damage-matched
  unflagged pick's avoided move over the identical calendar stretch;
- **(P2, the path)** the flagged pick's **adverse-first rate** — touches −1 ATR before +1 ATR from
  the exit basis — minus the damage-matched unflagged pick's rate at the identical ATR distance.

**Both must confirm in the same sign for any rule to follow** (§8). P1 alone is a money result on a
fixed terminal; P2 is the rule-5 path result and is what makes the claim about the *path* rather than
about one closing price.

**What the sentence above is allowed to mean — three population restrictions, measured before any
outcome was seen and carried wherever the verdict is restated** (REPORT, LEDGER, the §9 guide line,
any brief, any board line; DECISIONS #10, rule 10). They are **scope, not gates**: they change no
threshold, no arm, no MPE and no clause of §8.

  1. **Technical-arm-only.** Over this window the Conviction Monitor's EXIT tier *is* its technical
     arm: **284 of 284** primary flags on pick nights 2026-06-01..2026-08-26 fired via
     `technical_overall_tier`, `polarity_tier` is `WATCH` on **every** row dated ≥ 2026-06-01
     (0 HOLD, 0 EXIT), and `polarity_unavailable_coverage_low` sits on **100%** of in-scope rows with
     0 exceptions (`STEWARD_Q019_exposure.md` §6, §8). The verdict therefore speaks about a one-armed
     tier, and the §4 arm decomposition is reported as **not measurable in this window, with the
     reason** — never as "the technical arm carries all the information", which would be a claim about
     the tier logic where the fact is about data availability.
  2. **A day-1 or day-2 event.** Under the primary trigger the age decay (`:50-56`, `:807-811`)
     softens a day-3-to-5 EXIT to WATCH before it is shown: 223 first flags at day 1, 61 at day 2,
     **zero** at days 3–5. The claim is about what the monitor prints in the first two sessions after
     a pick, not about a five-day watch.
  3. **Ordinary-damage flags only.** 195 of 284 flagged picks (**68.7%**) are dropped for want of a
     caliper-matched control, and the dropped tail is systematically the more damaged one (mean `dam`
     **−0.94** ATR vs **−0.17** for the retained). This is DP-12's cost, paid and printed rather than
     softened — the 0.25 ATR caliper is **not** widened to retain the tail — and it means **no claim
     of any kind is made about the worst drawdowns**.

## 2. Population

- **Unit of inference: the trading night** (rule 6), and the night is the **pick night `t`** — the
  night the position was opened and the night on which selection correlations live. Pick rows are
  aggregated within a night first. A signal-date-clustered bootstrap is computed alongside and the
  **wider** of the two CIs decides (§4), because flags arriving on one bad session across several
  pick nights are a second correlation the pick-night clustering does not absorb.
- **Source tables (manifest_v001 and its successors):** `sas_candidates` (`qualified`,
  `selected_rank`, `overall_score`, `dominant_direction`, `best_timeframe`,
  `outcome_target_invalid` for the audit only), `sas_runs` (`finished_at`, DP-04),
  `conviction_monitor` (`trading_date`, `original_pick_date`, `symbol`, `days_since_qualified`,
  `overall_tier`, `age_adjusted_severity`, `polarity_tier`, `technical_overall_tier`,
  `reason_codes_json`, `polarity_details_json`, `technical_signal_count_json`, `created_at`,
  `updated_at`).
- **Source tables (manifest_prices_v001 and its successors):** `prices_daily_split` (pick-night
  close, session closes and opens, forward bars, ATR14, beta60, run-up, SPY tape),
  `prices_daily_raw` (split-factor snapping only), `prices_hourly_raw` (same-session ordering of the
  ±1 ATR race).
- **Positions in scope:** every **published** pick — `qualified IS TRUE AND selected_rank IS NOT
  NULL` (DP-28); dark-lane rows are in no arm — on a non-excluded pick night `t` in the §6 window.
  **Not elite-only.** The Conviction Monitor is an Elite-gated *surface*
  (`routers/conviction_monitor.py:32`, plan slug `omega`), but the job monitors **every qualified
  pick with no score filter** (`services/conviction_monitor_service.py:1043-1051`); the service
  docstring's "Elite picks" is pre-80-floor wording, not a filter. The population is therefore all
  published picks; 90+ and the 80–85 / 85–90 bands are reported sub-cells (§4), never arms.
- **Monitor rows in scope, per pick:** rows with `original_pick_date = t`, `symbol` matching, and
  `trading_date = s` where `s` is a **session in `t+1 … t+5`**. The job itself covers the previous 5
  **business** days and filters day 6+ and day 0 (`:1029-1052`, `:1172-1175`), so later rows are
  structurally absent; where a holiday falls inside the window the monitor's 5 weekdays are fewer
  than 5 sessions, which is why the window is stated in sessions from the trading calendar and the
  row's own `trading_date` is authoritative, never `days_since_qualified`.
- **Arm assignment, decided at the exit moment and never revisited:**
  - **FLAG** — the pick has ≥ 1 in-scope monitor row with **`age_adjusted_severity = 'EXIT'`**. The
    **signal session `s`** is the **earliest** such row's `trading_date`. `age_adjusted_severity` is
    the field the product surfaces: the panel sorts and counts on it
    (`routers/conviction_monitor.py:157-168`, `:181-184`), and the age decay softens a day-3-to-5
    EXIT to WATCH before it is shown (`:50-56`, `:807-811`), so under this trigger a flag is in
    practice a day-1 or day-2 event — **measured, not expected: 223 day-1 and 61 day-2 first flags,
    zero at days 3–5**, and **284 of 284** fired via `technical_overall_tier` alone (§1 restrictions 1
    and 2). The **undecayed** `overall_tier = 'EXIT'` trigger is a registered **secondary arm** (§4)
    that prints raw p and never decides.
  - **NOFLAG at session `s`** — a pick is an eligible control **for a flag dated `s`** if it has
    ≥ 1 in-scope monitor row **dated ≤ `s`** and **none of its rows dated ≤ `s`** is `EXIT` under the
    trigger field. Rows dated **after `s`** are written at 16:02 ET on later days and are **never
    read** to select a control: defining the cohort over the pick's whole future window would select
    controls partly on the fact that they were *never subsequently flagged*, which is a look-ahead in
    arm assignment (rule 14 on this question's own per-decision reading, §6) and a survivorship filter
    that flatters the hypothesis. A control that is flagged on a **later** session stays in the pool
    for `i`'s window and is graded with no early exit — which is exactly the choice a holder faces at
    the open of `s+1`: sell the flagged one, or hold a comparable one that has fallen as far and has
    not been flagged **yet**. This is the literal "X did not happen (yet)" cohort and it **includes
    WATCH and UNKNOWN rows** (§3 B2; DECISIONS #2, Correction 1). The repair makes the control pool
    larger and the expected contrast smaller; that is a consequence, not the reason.
  - A published pick with **zero** in-scope monitor rows is **excluded and counted** — it is neither
    flagged nor unflagged, and the freeze records more published rows (915) than `qualified IS TRUE`
    rows (907) across the full history (FREEZE_v001 §1), so the monitor's own load predicate can
    miss a published pick. **Measured in-window: 0 of 465** published picks on the 58 matured
    non-excluded nights have zero in-scope rows — the full-history gap does not reproduce in this
    sub-window (`STEWARD_Q019_exposure.md` §1). The monthly print stays: it is a diagnostic against
    which the successor nights are compared, not a claim.
- **Definitions (all prices in the signal-date split basis):**
  `C_t` = the pick's **actual** regular-session close on pick night `t` from `prices_daily_split`
  (never the platform's `spot_close`, stale on re-run nights — EXPLORE_001 §9);
  `ATR` = ATR14 from `prices_daily_split` bars dated ≤ `t` (the platform's `atr_pct` is corrupted
  around splits — DATA_NOTES / PI-003; not used);
  `dir` = +1 bullish / −1 bearish from `dominant_direction`;
  **`X` = the entry = `C_t`** — DP-11's construction verbatim: this question measures what happens to
  a position that is **already held** when the signal appears, so the entry is the pick-night
  regular-session close as the proxy for the DP-03(a) after-hours fill, applied identically to picks
  and controls. `X` sets the descriptive plan results and the matching variable; **the two primary
  estimands are entry-free by construction** (§4), so no verdict here turns on the entry basis;
  **`B` = the exit basis = `Open_{s+1}`**, the regular-session open of the session after the signal
  session — the first moment the flag is executable (§6, knowledge time);
  **`dam` = the damage already done** `= dir × (Close_s − C_t) / ATR`, the direction-adjusted move
  from entry to the close of the signal session, in ATR. `Close_s` exists at 16:00 ET on `s`, two
  minutes before the monitor writes and a session before the exit; it is legal at the exit decision.
- **Exclusions — each counted and printed in the results header, never silently dropped. Every
  exclusion uses only inputs available at the decision it governs, the trading calendar, or a
  measurement failure:**
  - pick nights in **`research/data/exclusions_v003.json`** (`manual_runs` ∪ `non_session_runs` ∪
    `uncorroborated_publication_runs`) **unioned with the add-only successor exclusions file** issued
    with the successor selection freeze (DECISIONS #5) — the identical three lists, the identical
    criteria, covering the post-2026-09-10 nights, **add-only**: a night may be added, never removed
    from a v003 list. On the sealed portion those are **2026-06-26**, **2026-07-02**, **2026-07-06**.
    `eval.py` reads both JSONs as inputs; **no file name and no date is hard-coded** (DP-22).
  - any prospective pick night whose `finished_at` is later than the next session's open (DP-04).
  - **monitor rows that are not point-in-time**, dropped row by row and counted: a row whose
    `created_at` is not on its own `trading_date` before the next session's open, or whose
    `updated_at` postdates `created_at` by more than one minute. The monitor deletes and reinserts a
    date's rows rather than updating them (`services/conviction_monitor_service.py:1097-1101`) and
    the entry point accepts `--trading-date` for an arbitrary past date
    (`scripts/run_conviction_monitor.py:38-62`), which would write *that day's* price action under an
    older `trading_date`; the guard is what makes the declared 16:02 ET availability checkable per
    row rather than assumed. A pick that loses its only flag row to this guard leaves the FLAG arm
    and is excluded and counted, never silently moved to NOFLAG. (Measured precedent: the monitor's
    only known late writes are 2026-05-12..05-15, outside the window — `KT_AUDIT` §2.) **Measured
    in-window: 0 failures** — all 160 guard failures in the 3,339-row freeze are May 2026, pre-window,
    and 0 of the 838 / 881 / 821 / 311 June–September rows fail either clause
    (`STEWARD_Q019_exposure.md` §5). No pick in the sealed portion loses its only flag row to the
    guard. The guard still runs row by row on the successor nights, and its counts are printed.
  - picks with missing forward bars in `s+1 … t+10`, or no `Open_{s+1}`, or fewer than 60 daily bars
    dated ≤ `t` → ungradeable; excluded and counted. A night is dropped if > 25% of its eligible
    picks are ungradeable.
  - **flagged picks with no valid damage-matched control** (§3 B2) → excluded and counted, with the
    distribution of their `dam` printed. This is DP-12's stated cost and it is paid, not softened.
    **Measured on the sealed portion: 195 of 284 (68.7%)**, mean `dam` **−0.94** ATR against **−0.17**
    for the retained, dropped share falling by month (75.9% → 74.0% → 55.9%) — §1 restriction 3, and
    the reason the verdict speaks for ordinary-damage flags only. The caliper is not widened.
  - pick nights whose session `t+10` falls after the last trading date of the pinned price freeze
    (immature) → excluded and counted. Maturity comes from the trading calendar, never from whether
    a price exists; right-censoring is never graded as a non-touch.
- **Contributing night (the floor unit, DP-21), identical for both primaries:** a pick night `t`
  carrying **≥ 1 eligible FLAG pick that is gradeable and has ≥ 1 valid matched control**. A matured
  night with no such pick is a **non-contributing night, not an exclusion**, and is printed in the
  funnel with its reason. **Measured on the sealed portion: 42 of 58 matured non-excluded nights
  contribute** (89 matched flagged picks out of 284 flagged, out of 465 published) — the `A` that §5's
  schedule is checked against.

## 3. Baseline(s) — what this must beat

- **B1 (the alternative the hypothesis names): the same position held to the close of session
  `t+10`.** Two plans, one position, one tape, paired within pick (§4, Plan H). "+10d" is taken from
  H-050 as written — ten trading sessions, not calendar days, not re-united (DP-25).
- **B2 (the primary control, DP-12): damage-matched picks unflagged *as of `s`*, same session, graded
  over the identical calendar stretch.** For each FLAG pick `i` with signal session `s`, the control
  pool is every published pick that is **NOFLAG at `s`** (§2: ≥ 1 in-scope monitor row dated ≤ `s`,
  none of its rows dated ≤ `s` EXIT under the trigger field; rows after `s` are never read) carrying
  an in-scope monitor row on **the same session `s`**, drawn from **any pick night that satisfies the
  same §6 window bound and the same §2 exclusion tests as `i`'s own** — so the pool is not confined to
  `i`'s own eight picks, but it can never contain a pick made under a different tier logic or a
  different catalyst layer (DP-06 / DP-50(a); the arms must differ in *whether the flag fired* and in
  nothing else). The bite is small by construction — a control must carry a monitor row on `s`, so its
  pick night is within five weekdays of `i`'s — and one-directional: the pool can only shrink. Subject
  to:
  (a) `|dam_c − dam_i| ≤ 0.25 ATR` (the caliper — the damage already done is matched, not merely
  adjusted for); (b) `|age_c − age_i| ≤ 1` weekday of the monitor's own `days_since_qualified`;
  (c) `c ≠ i` and `symbol_c ≠ symbol_i`. From the survivors take the **5 nearest** on standardized
  (`atr_pct`, `beta60`, `runup20`) — night-cross-sectional median and MAD, Euclidean, ties by symbol
  ascending, with replacement across picks. Each control is graded on **`i`'s own calendar window**
  — exit basis `Open_{s+1}`, terminal the close of **`i`'s** session `t+10` — using the control's own
  `dir` and its own `ATR`, so the two arms differ in **whether the flag fired** and in nothing else.
  Controls **never add to inferential n** (rule 6). Post-match standardized mean differences on
  `dam`, `atr_pct`, `beta60`, `runup20` and `overall_score` are printed for every night.
  **Both arms are published picks**, which is deliberate: they share the freeze's hourly-bar coverage
  (measured at 100% of published-symbol forward sessions on the comparable Q015 population,
  `STEWARD_Q015_exposure.md` §7), so the DP-27 tie path is rare and symmetric rather than
  systematically biting one side (Q015 threat 14's failure mode is avoided by construction).
  **Confirmed for this question's own arms:** all 61 distinct FLAG-arm symbols and all 67 distinct
  control-arm symbols in the sealed matched set are in the hourly universe, 0 missing
  (`STEWARD_Q019_exposure.md` §9). **Measured pool size** at a given `s`: 14.5 candidates on average
  from ≈ 4.2 distinct originating pick nights (min 2, max 23) — materially richer than threat 7's
  eight-picks-per-night framing, which is why the match rate is what it is.
- **B3 (sensitivity, never decides): the HOLD-only control pool** — the same matching with the pool
  restricted to picks whose trigger-field tier is `HOLD` **as of `s`** (conviction intact at the exit
  moment, read on rows dated ≤ `s` only, exactly as B2). B2, not B3, is primary: the baseline rule is
  "Y when X did not happen", and restricting the pool to the cleanest cohort would compare a flagged
  pick against a hand-picked healthy one and inflate the contrast (DECISIONS #2).
- **B4 (the total effect; descriptive, licenses no rule — DP-12): the unmatched contrast** — flagged
  picks against *all* picks NOFLAG **at `s`** on the same session with no `dam` caliper (the §2
  knowledge-time reading governs every arm, matched or not), and the within-pick raw
  plan difference on flagged picks with no control at all. Printed beside every primary, labelled
  *"total effect: includes the move that had already happened; descriptive, does not decide"*.

## 4. Objective metric (rule 5 — the price path from a stated basis, measured the way it is traded)

**The exit moment.** The monitor writes at **16:02 ET** on session `s`
(`docs/AZURE_WEBJOBS_AUTOMATION.md` cron `0 02 16 * * 1-5`; freeze availability `16:02`,
`lag_sessions: 1`, "next-session signal; feature only for t+1 decisions"; confirmed row by row in
FREEZE_v001 §7). Two minutes after the closing bell is not a closing price a holder can take, so the
**exit basis is `B = Open_{s+1}`**, the first executable moment, for picks and controls alike. The
session-`s` close is printed as a **picks-only descriptive sensitivity**, explicitly labelled *not
executable*, and it never decides.

**The two plans (neither uses a stop — rule 5, DP-02; adverse excursion is reported, not traded):**
- **Plan C (the tested rule):** hold from `X = C_t`; on the first flag session `s`, exit the whole
  position at `B = Open_{s+1}`. A pick that is never flagged is never exited early.
- **Plan H (the baseline, B1):** hold from `X = C_t` to the **close of session `t+10`**, whatever
  happens in between.
- `r_plan = dir × (exit − X) / ATR`, and the per-pick plan difference is
  `Δr_i = r_{C,i} − r_{H,i} = −dir_i × (Close_{t+10,i} − Open_{s+1,i}) / ATR_i`.
  **The entry cancels exactly**, so the primary estimands do not depend on the DP-11 entry choice;
  `X` remains the reference for `dam`, for the descriptive plan results and for the excursion panel.
  `Δr_i` is the **avoided move**: positive means the stretch the rule skipped went against the
  position.

**Primary endpoints (two, pre-specified, BH-corrected within the question and across F6 — §7).**
For pick night `t`, `mean_F[·]` is the mean over that night's eligible FLAG picks and, for each such
pick, `mean_M[·]` is the mean over its matched controls (the pick's control mean enters once, so a
pick with 5 controls does not outweigh a pick with 1):

- **P1 — the money (avoided move, damage-matched, ATR per trade).**
  `Δ1_t = mean_F[ Δr_i − mean_M[ Δr_c ] ]`; estimand `m1 = mean_t Δ1_t`, in **ATR per flagged
  trade**, over contributing nights. `Δr_c` is the control's avoided move over `i`'s own window.
- **P2 — the path (adverse-first race, damage-matched, percentage points).**
  From `B`, with levels `B + dir × 1.0 × ATR` (favourable) and `B − dir × 1.0 × ATR` (adverse),
  over sessions `s+1 … t+10`: `ADV_i = 1` if the adverse level is touched **before** the favourable
  one, else 0 (neither touched → 0). Levels are set *from the exit basis*, so no level can be passed
  at entry (rule 5). `Δ2_t = mean_F[ ADV_i − mean_M[ ADV_c ] ]`; estimand `m2 = mean_t Δ2_t`, in
  percentage points. The levels are **1× each row's own ATR from its own basis**, so picks and
  controls carry a target at the identical ATR distance — distance-matched by construction
  (the Q016 / Q017 construction).

**Ordering rules, stated once, applied by `eval.py` with no judgment:**
1. **Same-session adverse and favourable touches** are ordered from `prices_hourly_raw`, converted to
   the signal-date split basis (`eval.py` asserts basis agreement per symbol-date and fails loudly).
   Where one hourly bar holds both, or the symbol has no hourly bars, the pair counts
   **adverse-first — DP-27 applied literally and symmetrically to both arms**. The count resolved by
   this rule is printed per arm, and the opposite reading is a named sensitivity that never decides.
   Applying DP-27's *principle* per arm (the reading less favourable to the hypothesis, which differs
   in sign between arms) was rejected: an arm-dependent tie rule is manipulable, and on a difference
   of rates the symmetric rule is second-order.
2. **A gap through a level at the open is a touch** at that level, and a gap through at `s+1`'s own
   open is a touch in the first graded session.
3. The **first** flag ends Plan C. There is no re-entry, no second exit and no use of later monitor
   rows, whatever they say.

**Secondary, descriptive, never decides (each prints raw p only):**
- **the rule-5 execution report:** Plan C's and Plan H's realized ATR per trade from `X` (not only
  their difference), the **portfolio / intention-to-treat** version over *all* eligible published
  picks (flagged picks exit at `B`, unflagged hold to `t+10`) against holding every pick to `t+10`,
  and the flag rate that scales the one into the other;
- **B4**, the total (unmatched) effect, and **B3**, the HOLD-only pool;
- the **undecayed trigger** `overall_tier = 'EXIT'` — the same two endpoints, the same matching, a
  separate arm — which is what says whether the age decay (`:50-56`, `:807-811`) discards
  information;
- the **WATCH-or-worse** trigger, with the share of its rows whose only reason code is an
  availability code (`polarity_unavailable_coverage_low`, `qualifying_snapshot_unavailable_*`,
  `today_snapshot_unavailable_*`) printed beside it — WATCH conflates "conviction weakened" with "our
  data was missing" (`:184-185`, `:663-682`), which is why it is not the primary trigger;
- **which arm fired:** polarity-driven flags (`polarity_tier = 'EXIT'`) versus technical-driven
  (`technical_overall_tier = 'EXIT'`) versus both, each as a sub-cell at ≥ 20 contributing nights —
  the read that says whether one of the two arms carries all of the information. **Registered and
  kept, and recorded at lock as NOT MEASURABLE IN THIS WINDOW, with the reason:** polarity contributed
  **0 of 284** primary flags over 2026-06-01..2026-08-26, `polarity_tier` is `WATCH` on every row
  dated ≥ 2026-06-01, and `polarity_unavailable_coverage_low` is present on 100% of in-scope rows with
  0 exceptions — the polarity-only and both cells are **structurally empty, not thin**, and waiting
  cannot fill them. "Not measurable" and "measured zero difference" are different results and this
  file distinguishes them: the decomposition is **never** restated as "the technical arm carries all
  the information", which would be a claim about the tier logic where the fact is about data
  availability (§1 restriction 1, DECISIONS #9, #10). `eval.py` prints the firing-arm composition
  **by month and by half** so §8 clause 5's both-halves test is read with the composition in view;
- horizons **`t+5`** and **`t+20`** in place of `t+10` for both plans, and the **race window fixed at
  10 sessions from `s`** instead of the remaining hold — the two shape sensitivities;
- the **session-`s` close** exit basis (picks only, not executable);
- sessions from `s+1` to the adverse and favourable touches; **maximum adverse and maximum favourable
  excursion** in ATR from `X` over `t+1 … t+10` for both arms; counter-direction touches — reported,
  never an exit (DP-02);
- sub-cells at ≥ 20 contributing nights: score band (**`< 80` / 80–85 / 85–90 / 90+** — the residual
  `< 80` cell exists because the population is *every published pick*, DP-28's predicate carries no
  score floor, and the freeze holds one published row at **79.58** (TJX, 2026-06-11); the band
  decomposition is exhaustive so that no pick is silently absent from it, and that row stays in the
  population and in both primaries, never dropped to tidy the list), bull / bear, `dam` tercile,
  **age 1–2 versus 3–5** (**empty by the age decay's design under the primary trigger — 42 of 42
  matched-contributing nights are day 1–2 and there is no day-3-to-5 primary flag at all** — so the
  cell is printed only under the registered undecayed secondary, where it is floor-tested at the
  decision pass like any other descriptive sub-cell; the sealed portion holds 14 / 11 / 7 picks at
  days 3 / 4 / 5), `atr_pct` tercile, tape stratum, regime label;
- close-to-close return from `X` at `t+10` — **fixed-horizon return is descriptive by rule 5 and
  never decides**;
- the **drop rate for want of a matched control**, with the `dam` distribution of the dropped and the
  retained, printed **by month and by half** (§1 restriction 3, DP-12's cost made visible over time).

**SUPPRESSED at lock — five sub-cells, counts only** (DECISIONS #6 and #9, fixed now on the Steward's
measured splits and **never revisited**, because DP-43 says demotion is decided at lock and not once
counts are visible). No point estimate, no q-value, no sign, no "directionally" — the printed counts
and nothing else:

- *accrual-based, projected to the registered window end (≈ 160 contributing nights), not merely to
  the 80-night floor:* **direction = bearish** (3 of 42 → ≈ 11), **score band 90+** (2 of 42 → ≈ 8,
  and PI-010's thinning elite count makes even that optimistic), **score band `< 80`** (1 of 42 → ≈ 4);
- *structural, not an accrual gap and never cured by waiting:* **firing arm = polarity-only** and
  **firing arm = both** (0 of 284), and **primary-trigger age 3–5** (0, by design).

The three cells that clear comfortably are unaffected (80–85 ≈ 148, 85–90 ≈ 46, all three `dam`
terciles ≈ 72 / 84 / 91). **Suppression restricts affirmative reporting only.** A suppressed cell keeps
its printed counts, is **never** removed from **§8 clause 6** (a tape stratum with ≥ 20 contributing
nights beyond MPE in the opposite sign still blocks CONFIRMED, and the sign must hold in every such
stratum — measured counts, not this list, decide which strata qualify) or from **clause 7**, never by
itself makes an endpoint INCONCLUSIVE (§8 clause 1), and is never a route to an easier CONFIRMED. A
cell suppressed here stays suppressed **even if it clears 20 measured nights at the decision pass** —
the stricter state, and the one that cannot be re-argued once the numbers are in view.

**Quotability:** every window here is ≤ 20 sessions → **every number in this question is
NON_QUOTABLE** (rule 12).

**Inference.** Night-level. **CI (decides):** the **wider** of (a) a stationary block bootstrap over
the ordered contributing pick nights, expected block length **5 sessions** (the graded windows are
≤ 10 sessions and overlap across adjacent pick nights; shorter than the 10 used for 20-session
questions, fixed here before any result), and (b) a bootstrap clustered on the **signal session `s`**,
2,000 resamples each, seed 20260913. Taking the wider is deterministic and conservative and is chosen
here, not after seeing which is wider. **p-value:** permutation on the night contrasts — paired
sign-flip, 10,000 permutations — plus, printed second, a **within-(session `s`, `dam`-stratum) flag-label
shuffle** across eligible picks. Every estimate prints n(contributing nights), n(contributing nights
dated after the lock commit), n(flagged picks), n(matched controls), n(picks dropped for no control),
n(resolved by ordering rule 1), n(excluded, by reason).

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** — P1 and P2
  share the §2 definition — and ≥ **20 contributing nights per reported sub-cell**. A sub-cell below
  20 is **SUPPRESSED** (counts only, no point estimate) and does not by itself make its endpoint
  INCONCLUSIVE (§8 clause 1). **Five sub-cells are SUPPRESSED at lock** on the Steward's measured
  splits and are not revisited at the decision pass (§4; DP-43 decides demotion at lock, never once
  counts are visible). **The two arms themselves are not demotable:** a night missing an eligible FLAG
  pick *or* its matched control is **non-contributing** (§2), never a thin arm, so DP-43's demotion
  clause reaches the sub-cells only. The weaker reading of rule 6 is not used. **No floor is ever
  lowered to hit a date.**
- **Binding maturity: 10 sessions** from the pick night.
- **Exposure: none had ever been measured for this table, so R1 was blocking for lock — and it is now
  answered.** Nothing in the desk's reports counted monitor tiers: EXPLORE_001 touched
  `conviction_monitor` only to print its shape, columns and two head rows
  (`research/reports/explore/scripts/69_inspect_aux.py`), and recorded one fact —
  *"`conviction_monitor` starts 2026-05-12"* (§9). **R1 answered 2026-09-13**,
  `research/reports/STEWARD_Q019_exposure.md`, counts only on the pinned freeze (DP-50(c)):
  **`A` = 42** matched-contributing nights over **61** elapsed sessions (June 12 / July 12 / August
  18), **`r` = 0.6885 per elapsed session**, computed under the §2 NOFLAG-at-`s` definition and the §3
  same-window control bound. The **0.35 planning rate below is kept visible** because it is what set
  the dates: at the measured rate the registered window projects ≈ **160** contributing nights against
  an 80-night floor — roughly **2× the floor by construction, not by accident** — and no date moves in
  for it (DP-43, DP-45).

**R1 — routed to the Data Steward, was BLOCKING FOR LOCK; ANSWERED 2026-09-13,
`research/reports/STEWARD_Q019_exposure.md`** (counts only; no outcome of any kind — no touch, no
race, no return, no plan result, no tier-versus-outcome cross-tab). Kept verbatim below as the record
of what was asked before any number was seen. On pick nights 2026-06-01..2026-08-26 after the §2
funnel:
  1. matured pick nights, eligible published picks, and published picks with **zero** in-scope
     monitor rows (the `qualified`/`published` gap);
  2. **FLAG picks and FLAG nights** under the primary trigger (`age_adjusted_severity = 'EXIT'`,
     first row in sessions `t+1 … t+5`), and separately under the undecayed `overall_tier` trigger;
  3. **matched-contributing nights** — nights with ≥ 1 flagged pick that clears the §3 B2 caliper
     with ≥ 1 control — and the **rate per *elapsed* session** (Correction 3), by month;
  4. flagged picks dropped for no valid control, with their `dam` distribution;
  5. monitor rows failing the §2 point-in-time guard, by month;
  6. `technical_overall_tier = 'UNKNOWN'` and polarity-unavailable shares, by month;
  7. **the platform git history of the tier logic** — `git log --follow services/conviction_monitor_service.py`
     in the read-only platform repo — dating every change to the tier rules (the "Fix 1–6" work:
     the ATR breach buffer `:86`, the info/weak recategorisation `:388-446`, the dedupe `:627-638`,
     the concurrence rollup `:736-785`, the aged-TF cap `:98-104`). The evidence available to the
     registrar puts that work at the monitor's launch (the debug harness
     `scripts/_debug_conviction_monitor_mrna.py` targets MRNA 2026-05-11/05-12, the first monitored
     dates), but it is not verified, and a tier column that changed meaning mid-window is two
     features, not one (DP-06 pattern, DP-50(a)).

  **Answered:** (1) 58 matured non-excluded nights, 465 published picks, **0** with zero in-scope
  monitor rows, 0 without `C_t`, 0 short of 60 prior bars, 0 flagged picks without forward bars, 0
  nights over the 25%-ungradeable rule; (2) **284** primary FLAG picks on **57** of 58 nights (day 1
  223, day 2 61, days 3–5 zero) and **316** under the undecayed trigger on all 58; (3) **A = 42**,
  **`r` = 0.6885**/elapsed session (0.571 / 0.545 / 1.000 by month); (4) **195 of 284 (68.7%)** dropped
  for no control, dropped `dam` mean −0.94 vs retained −0.17; (5) **0** point-in-time guard failures
  in-window (all 160 in the freeze are May 2026); (6) `technical_overall_tier = 'UNKNOWN'` ≤ 0.75% and
  falling to 0, `polarity_unavailable_coverage_low` on **100%** of in-scope rows every month; (7) the
  tier logic has **three** commits ever, all **2026-05-16** (13234cc / baf17b8 / 2cb7a7e) — the
  "Fix 1–6" work is bundled there, **before** the window start, so the start does **not** move.

- **The window start is `max(2026-06-01, the first pick night after the last dated change to what the
  tier means)`** — and "a dated change" means **a tier-logic ship *or* the restoration of a
  structurally-unavailable input**, the date taken from the ship SHA and its `DATA_NOTES.md` entry
  (DECISIONS #3 and #12(a); DP-06, DP-50(a)). The mirror case is not hypothetical here: the polarity
  arm has been dead since before the window (§1 restriction 1), and a dated ship that brings it back
  changes **which picks receive `EXIT`** exactly as a logic change would. An **undated** recovery —
  coverage returning on the vendor side with no SHA — moves **nothing**: there is no date to split on
  and the desk will not invent one; it is printed by month instead (§4). The rule can only push the
  start later, never earlier, the whole schedule is then recomputed at the measured rate, and if the
  recomputed decision date lands after **2027-09-13** Q019 goes to `research/questions/DEFERRED.md`
  rather than the ceiling being stretched. At `r` = 0.6885 a restart costs ≈ 8 months, so a ship
  before ≈ **2027-03-08** is survivable and one after it is not.
  **Measured: no such change exists inside the window** (R1 item 7), so the start stays **2026-06-01**.
- **Planning rate and schedule (DP-43). The 0.35 rate below is the *planning* assumption that set
  these dates; `A` = 42 and `r` = 0.6885 are the measurement that confirmed them and moved none of
  them in:**
  - Matured in-window pick nights on the pinned freeze: **2026-06-01..2026-08-26** (the +10 maturity
    cutoff on `manifest_prices_v001`; FREEZE_v001 §2 fixes the same date for the platform's own T+10
    column) — **61 elapsed sessions** (calendar minus holidays, **exclusions not pre-removed**, which
    is the lower rate and therefore the longer window — Correction 3), of which **58** survive the
    three in-window exclusions as gradeable pick nights.
  - **Planning rate `r_plan` = 0.35 matched-contributing nights per *elapsed* session** → ≈ 20
    contributing nights assumed in the freeze; 60 more at 0.35/elapsed session = **172 sessions**
    beyond 2026-08-26 ≈ 249 calendar days (the desk's mechanical 365/252 conversion) →
    **2027-05-03**. **Measured instead: `A` = 42 accrued and `r` = 0.6885**, which projects the 80th
    contributing night near **2026-11-14** and an equivalent decision near **2026-12-05** — both
    informational only. **A date is never pulled in** (DP-43, DP-45): the registered end stands, the
    question is over-powered by ≈ 2×, and that cost is named on the board rather than paid by moving a
    locked date.
  - **Primary window: pick nights 2026-06-01..2027-05-03 inclusive**, after exclusions. The end is
    where the planning rate projects the 80th contributing night, not where a date would be
    convenient. A shorter window that reached a date sooner was rejected (DP-43, DP-45).
  - **Decision date: Monday 2027-05-24.** 2027-05-03 + 10 sessions maturity ≈ 2027-05-17, + one week
    freeze margin = 2027-05-24, first Monday on or after = 2027-05-24 — **8.4 months from the
    2026-09-13 lock**, inside DP-43's 12-month ceiling. The Steward fixes the exact session-count
    date when building the successor freezes. `eval.py` is written once (rule 9) and run **once**,
    then. **No interim looks.**
  - **The DP-43 ceiling test — settled, and the lock is unconditional.** Solving
    `1.4484 × (80 − A)/r + 21 ≤ 383` days (2026-08-26 → 2027-09-13) gives **`r ≥ 0.26`** at
    `A = 58r` and a 2026-06-01 start. The Steward measured **`r` = 0.6885**, far above it, so the
    DEFERRED branch is **closed** and Q019 locks on the **unmodified drafted schedule**. Had `r` come
    in below 0.26 the question would have gone to `research/questions/DEFERRED.md` at `record` with
    the projected date named (H-062 precedent) rather than the ceiling being stretched; had it come in
    between 0.26 and 0.35 both dates would have moved **out**. Faster than 0.35 changes nothing.
  - **Both gates, per primary endpoint, on measured counts.** Evaluation proceeds only if **each**
    primary has **≥ 80 contributing nights** and **≥ 30 contributing nights dated after this file's
    lock commit** (DP-24), printed by `eval.py` from the frozen data. At the **measured** rate the
    80th contributing night lands near **2026-11-14** and DP-24's 30th post-lock night near
    **2026-11-15** — both about six months before the decision pass, with ≈ 111 post-lock contributing
    nights projected by the window end — so neither gate is binding; **PROSPECTIVELY_CONFIRMED is
    reachable from this run by design, DP-31 does not apply, and no successor replication question is
    needed.** Gates fire on `eval.py`'s measured counts at the decision pass, never on R1, on this
    projection or on a run-rate.
  - **One automatic extension (DP-13; DP-43's +30 sessions).** If any gate is short at the decision
    date on `eval.py`'s measured counts, the window extends **once**, automatically and with no new
    question, by 30 sessions — on the drafted schedule to pick nights **2026-06-01..2027-06-15**,
    decision **Monday 2027-07-12** — run with the **byte-identical, unmodified `eval.py`** and the
    same gates.
  - **DEFERRED fallback.** If a gate is still short after that single extension, Q019 goes to
    DEFERRED with the measured counts rather than running under-powered. There is no second
    extension, no reduced floor, and a gate shortfall is **not** an INCONCLUSIVE verdict (§8). On the
    measured rate this is remote; it is kept because the gate fires on counts, not on a rate.
  - **The one live route back to DEFERRED** is the window-start rule above: a **dated** change that
    restores a structurally-unavailable input, or otherwise alters which picks receive `EXIT`, shipping
    inside the window. It moves the start, the schedule is recomputed at the measured rate, and past
    **2027-09-13** the answer is DEFERRED. The desk does not ask for such a fix to be held on Q019's
    account; the cost is written down so the choice is made with it in view.
- **Freeze discipline (DP-23; routed request R2 — due before the decision pass, not a blocker for
  lock).**
  Nights ≤ 2026-09-10 stay pinned to `manifest_v001` / `manifest_prices_v001`; later nights enter only
  through `manifest_v002` (same SQL, **including the `conviction_monitor` table key**, same exclusion
  criterion) and `manifest_prices_v002` (same Alpaca queries), with the daily symbol list covering
  **every candidate on the new nights, published and unpublished**, plus **hourly bars for published
  symbols** (ordering rule 1), carrying **10** forward sessions beyond the last included pick night
  (20 where the `t+20` sensitivity is computed). A second pair is built **only if** the DP-13
  extension fires. The successor selection freeze carries the `conviction_monitor` rows **with
  `created_at` and `updated_at`**, so the §2 point-in-time guard runs row by row on the new nights
  exactly as on the pinned ones, and it is issued with the **add-only successor exclusions file**
  (DECISIONS #5). **Two further clauses, counts only** (DECISIONS #8, #12): **(vi)** with each
  successor freeze the Steward reports, by month, the `polarity_unavailable_coverage_low` share, the
  `polarity_tier` distribution, the `technical_overall_tier = 'UNKNOWN'` share and the firing-arm split
  of primary flags — §1's claim scope is a **measured** restriction, not an assumption, so it is
  re-measured on the successor nights; **(vii)** the **dated SHA** of any change that restores polarity
  coverage or otherwise alters which picks receive `EXIT`, with a dated `DATA_NOTES.md` entry naming
  the column and the date range — that date fires the window-start move above, mid-flight, with the
  DEFERRED branch live; an undated drift fires nothing. `eval.py` takes the window bounds, the manifest
  paths, the exclusions-file paths and the output directory as inputs — **no hard-coded dates, manifest
  names or paths** — records every sha256, and prints pre-lock and post-lock night counts separately.

## 6. Test window, split and stratification

- **Test window: sealed + prospective — pick nights 2026-06-01 .. 2027-05-03** (the start confirmed by
  R1 — the last dated change to the tier's meaning is 2026-05-16 — and movable only later, and only by
  the §5 window-start rule; the end movable only outward, by the single DP-13 extension to
  **2027-06-15**). The sealed nights are **in** the window and are not contaminated for
  this hypothesis: no desk output has ever crossed a monitor tier with an outcome (§5), H-050 predates
  every sealed read, and the trigger field, the 10-session horizon and the ±1 ATR levels come from
  the product, from H-050's own wording (DP-25) and from desk convention (DP-26) respectively — none
  was chosen after seeing a number. The window also sits entirely after the 2026-06-01 catalyst fix
  (DP-06; `exclusions_v003.json` `catalyst_layer_regime_change`; platform commit `69ef05f`) and
  entirely after the monitor's 2026-05-12 launch and the late-write outage of 2026-05-12..05-15
  (`KT_AUDIT` §2), which the exclusions file removes in any case.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date (re-derived from the final window at the decision pass); Half B = after.
  `in_sample_end = 2026-05-29` marks only what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v003.json` `regime_label_point_in_time_from`). It is used only for nights ≥ 2026-06-09,
    only `regime_version = 'v1.2'`, and only where the row is a same-evening write; a later-posted row
    is treated as missing. Nights 2026-06-01..06-08 carry no legal label and are stratified by the SPY
    proxy only, flagged.
  - Primary tape stratum for every night, trailing and legal at the pick night's close:
    `tape_t` = sign of SPY's trailing 20-session return × tercile of SPY's trailing 20-session
    realized volatility, from SPY bars dated ≤ `t` in `prices_daily_split`. **Tercile cut points are
    expanding-window**, so no later night's data sets an earlier night's stratum. Cells < 20
    contributing nights SUPPRESSED.
  - Because an exit rule is mechanically flattered by a falling tape, the tape stratum carries a
    **hard §8 clause** here, not merely a reporting duty (§8 clause 6).
- **Knowledge time (rule 14) — every input declared. Q019 needs no rule-14 exception and requests
  none** (DP-05 untouched; DP-41 respected). Rule 14 binds each decision to its own moment: the
  **selection-side** inputs (population, band, direction, entry) are all 16:05 ET on the pick night,
  and the **exit-side** decision is taken at the open of session `s+1`, by which time the monitor row
  (16:02 ET on `s`, `lag_sessions: 1`, "feature only for t+1 decisions") and `Close_s` (16:00 ET on
  `s`) both exist. Nothing here asks for a later clock on a selection-side input, and no outcome
  quantity classifies, filters, matches or stratifies any pick.

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `overall_score`, `dominant_direction` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) | population, band, direction |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion |
  | `C_t`, ATR14, beta60, `atr_pct`, runup20 | `prices_daily_split`, bars ≤ `t` | pick-night close, 16:00 ET | entry, ATR denominator, matching |
  | `age_adjusted_severity`, `overall_tier`, `polarity_tier`, `technical_overall_tier`, reason codes, `created_at` | `conviction_monitor`, row dated `s` | session `s`, 16:02 ET (freeze availability; FREEZE_v001 §7, verified row-level) | **arm assignment**, point-in-time guard |
  | `Close_s` | `prices_daily_split` | session `s`, 16:00 ET | `dam`, the matching variable |
  | `Open_{s+1}` | `prices_daily_split` | session `s+1`, 09:30 ET | **exit basis `B`**, race levels |
  | daily bars `s+1 … t+10` (`t+20` sensitivity); hourly bars for same-session ordering | `prices_daily_split`, `prices_hourly_raw` | after the exit decision | **outcome measurement only** |
  | regime label (v1.2, nights ≥ 2026-06-09, same-evening rows only); SPY tape | `market_regime`, `prices_daily_split` | pick night, 16:05 ET | stratum |

  **What `eval.py` must enforce:** the eligible-pick set, both arms, `dam`, every matched control and
  every stratum label are computed and written to a frozen per-pick table **before any bar dated after
  session `s` is loaded**; the run fails if any `s+1`-or-later field is referenced in eligibility, arm
  assignment, matching or stratification. `sas_selection_excursion` / `outcome_*` / `level_hit_*`
  columns are never inputs (calendar windows, close basis, recomputed weeks later, v1/v2 duplication —
  `services/sas_excursion.py:8-18`, `:336-354`; DATA_NOTES). `uoa_symbol_daily.fwd_return_*` is
  **banned** (FREEZE_v001 §5).

## 7. Multiple testing

- **Within the question:** **BH across m = 2** — P1 and P2 — at q ≤ 0.10; the verdict uses q. **`m = 2`
  is fixed at lock**: both primaries carry verdicts in every branch, and an endpoint short of floor
  still has its p computed, so `m` never falls and no bar is lowered for the survivor. Every secondary
  — the undecayed trigger, the WATCH trigger, B3, B4, the arm decomposition, the `t+5` / `t+20`
  horizons, the session-`s` basis and every sub-cell — prints raw p only, marked "descriptive, does
  not decide".
- **Across the family: F6 Exits and execution.** The correction set is **computed at the decision pass
  over the F6 primaries locked by then**. As drafted it is Q003 (2) + Q009 (2) + Q012 (3) + Q018 (4)
  + Q015's **2 F6-companion primaries** + **Q019's 2** = **15**; **Q010 is excluded** as Q009's
  prospective replication of the same hypothesis, not a second F6 question. H-050 is counted once, in
  F6. Q003 is filed **F6** with 2 primaries (its own header and §7), which is why the set is 15 and not
  13; the locked Q018 §7 states the same 15, so the two files agree and neither is restated.
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q015 (H-060)** contrasts exit-at-the-L3-touch against hold-through **inside one band**, on a
    20-session clock, with no monitor input. **Q012 (H-066)** contrasts a quick-exit recycle plan
    against the committed scale-out over a 60-session capital budget. **Q018 (H-051)** contrasts the
    three printed lane plans on the same pick. All four questions, Q019 included, are readings of one
    larger idea — *that the platform exits too late* — and **must never be presented or counted as
    independent confirmations**; the Reporter cross-references. **No endpoint is shared:** Q019 is the
    only one whose exit is triggered by a signal computed after the pick night, and the only one whose
    alternative is H-050's fixed +10-session hold.
  - **Q009 / Q010 (F6)** study the printed *stop* as an exit line. Q019 assumes no stop (DP-02) and
    its adverse level is the desk-standard −1 ATR line, not the printed stop.
  - **Q008 (F4)** conditions on a fast start measured from the path after the pick and notes that the
    monitor "already runs at the right moment of day" (Q008 §9) — but it registers no monitor
    quantity. Q019 is the first question to test one.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1` in **ATR per flagged trade** (the flagged pick's avoided move minus its damage-matched controls');
`m2` in **percentage points** of adverse-first rate (same contrast). Both two-sided; the verdict
carries its sign. H-050 predicts `m1 > 0` and `m2 > 0`.

**MPE: P1 0.25 ATR** (DP-10, DP-44 — the standing number for every per-trade ATR-denominated
endpoint; no uplift proposed), measured **per flagged trade and never rescaled** to a per-toucher or
per-portfolio basis. **P2 +5.0 pp** (DP-20, DP-44 — the standing number for a control-adjusted
touch-rate endpoint).

**Scope of whatever verdict comes out — stated here as scope, not as gates; no threshold below moves
because of it** (§1, DECISIONS #10): the verdict is about **the technical arm alone** (polarity
contributed 0 of 284 flags and its tier is `WATCH` on every in-window row), about a **day-1 or day-2**
flag (zero primary flags at days 3–5), and about **ordinary-damage** flags only (68.7% of flagged
picks dropped for want of a caliper-matched control, the dropped tail the more damaged one). Every
restatement of the verdict carries all three.

Per endpoint:

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. **contributing nights ≥ 80** on the §2 definition **and ≥ 30 dated after the lock commit**
     (DP-24), **and ≥ 20 contributing nights for any sub-cell that is reported** — a sub-cell below
     floor is **SUPPRESSED** (counts only) and does **not** by itself make the endpoint INCONCLUSIVE.
     The five cells SUPPRESSED **at lock** (§4: bearish, 90+, `< 80`, the two polarity firing arms and
     primary-trigger age 3–5) stay suppressed whatever they measure at the decision pass, and their
     suppression restricts **affirmative reporting only** — it removes nothing from clause 6 or
     clause 7 and opens no easier route to CONFIRMED;
  2. `|m| > MPE` (0.25 ATR for P1; 5.0 pp for P2);
  3. the deciding CI — the **wider** of the two bootstraps (§4) — excludes 0;
  4. BH q ≤ 0.10 within the question (m = 2) **and** within F6 (§7);
  5. the point estimate has the **same sign in both halves**, and neither half is beyond MPE in the
     opposite sign;
  6. **no tape stratum with ≥ 20 contributing nights is beyond MPE in the opposite sign**, and the
     result is not carried by a single tape stratum: the estimate must keep its sign in **every** tape
     stratum that clears 20 nights. An exit rule that only pays in a falling tape is a tape bet, not a
     monitor finding;
  7. **the damage-matched form is the verdict.** If the matched estimate is inside MPE while the
     unmatched total effect (B4) is beyond it, the endpoint is **NULL for the Conviction Monitor** and
     the report says so in those words: the flag added nothing to what the drawdown already said
     (DP-12).
- **Both primaries must be CONFIRMED in the same sign for any rule to follow** (§9). P1 CONFIRMED
  with P2 NULL is a money result on one terminal price with no path behind it and licenses nothing;
  P2 CONFIRMED with P1 NULL says the flag marks a worse-shaped path that is not worth 0.25 ATR to act
  on, and likewise licenses nothing. Either mixed case is reported as **split**, not as a partial win.
- **NULL:** floors met **and** the deciding CI includes 0 **and** `|m| < MPE`. "Acting on the
  Conviction Monitor's EXIT flag is worth nothing beyond the damage already done" is a real finding
  and is ledgered with the same care — and it is the finding that would put the surface itself in
  question (§9).
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, a tape stratum beyond MPE in the
  opposite sign or the sign not held across strata, `0 < |m| ≤ MPE` with the CI excluding 0 ("real but
  below MPE", rule 6), or the CI including 0 with `|m| ≥ MPE`. A SUPPRESSED sub-cell is not by itself
  INCONCLUSIVE. **A gate shortfall is not INCONCLUSIVE either**: it fires the single DP-13 extension,
  then DEFERRED (§5).
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5; on the measured rate the 30th
  post-lock contributing night lands ≈ 2026-11-15 and ≈ 111 are projected by the window end) — ≥ 30
  contributing nights dated after this file's lock commit (DP-24, DP-21), frozen in the successor
  manifests, never inspected earlier, reproducing the sign of both confirming endpoints under the
  unmodified `eval.py`. The clause does not weaken. No subscriber-facing statement before that
  (rule 10); even then the basis is NON_QUOTABLE until restated on W60 (rule 12), and it carries the
  three scope restrictions above.

## 9. If CONFIRMED, what changes on the platform

Today the Conviction Monitor **shows a tier and prescribes nothing**. It writes HOLD / WATCH / EXIT
per pick per day (`services/conviction_monitor_service.py:1229-1248`), the panel sorts by
`age_adjusted_severity` and counts the tiers (`routers/conviction_monitor.py:157-204`), and the
subscriber is left to infer what to do; the notes field says "Technical structure broken on one or
more timeframes" (`:1055-1072`), not "close the position". Nothing in `BAND_EXITS`
(`scripts/generate_sas_trading_guide.py:89-95`) or in the Manual Trading Guide references the monitor
at all, and no desk number has ever been attached to it. Rules below fire only where §8 licenses one,
and only after PROSPECTIVELY_CONFIRMED for anything subscriber-facing (rule 10).

**Every line, brief and board entry below carries §1's three population restrictions verbatim beside
the measured number — the tier as measured is the technical arm alone, on days 1–2, for
ordinary-damage flags — because a subscriber-facing sentence inherits the population it was measured
on (rule 10, DECISIONS #10).** A guide line that drops them would claim more than this question tested.

- **P1 and P2 CONFIRMED positive:** a **Manual Trading Guide** line — *"an EXIT tier is an exit: close
  at the next open rather than holding the position out"* — carrying the measured ATR per flagged
  trade **and the damage-matched excess beside it**, the flag rate so a reader knows how often it
  applies, and the three restrictions; and a **flag-off** panel change adding an explicit action line
  to the EXIT row. Brief: an `INTERNAL_TOOL`, flag-off card field showing the measured post-flag
  avoided move, restrictions included in the field's own caption. If the
  **undecayed** secondary is materially stronger than the primary, the brief also proposes surfacing
  `overall_tier` beside `age_adjusted_severity` — the age decay would then be discarding tradeable
  information — but that proposal is explicitly labelled as resting on a secondary and needs its own
  question before anything subscriber-facing.
- **P1 and P2 CONFIRMED negative:** the opposite, and it is the more consequential branch — the flag
  marks names that recover, so the guide records *"an EXIT tier is not an exit"*, the panel copy is
  corrected, and the surface goes to `PLATFORM_ISSUES.md` for a decision about whether it should
  continue to be sold as an exit signal at all. **That PI entry names the DP-50(b) timing constraint
  in the entry itself:** a repair to the tier logic (`conviction_monitor_service.py:328-620`,
  `:736-785`, `:792-804`, or the age decay at `:50-56` / `:807-811`) — or to an input that changes
  which picks receive `EXIT` — is **flag-off until this question's decision date** (the PI-011 / Q010
  pattern); if it ships inside the window anyway it takes a dated `DATA_NOTES.md` entry naming the
  column, the date range and the ship SHA, the tier column becomes **two features split at the ship
  date** (DP-06 pattern, DP-50(a)), and the §5 window-start move fires mid-flight with the DEFERRED
  branch live. Both branches are written into the entry, because the choice between them is Haci's.
- **Split (one primary CONFIRMED, the other NULL):** no rule, no guide line, no brief. The Ledger
  records the split and the Reporter states which half failed.
- **NULL on the damage-matched form with B4 large (§8 clause 7):** no monitor rule ships. The finding
  — "exiting a pick that has already given back `d` ATR pays, with or without the monitor" — is
  ledgered and **registered as its own question**, because a damage-triggered exit rule is a different
  and simpler product than the one H-050 asked about, and it would collide with Q012's and Q015's
  endpoints (§7). Any `PLATFORM_ISSUES.md` entry that follows from this branch carries the same
  DP-50(b) timing constraint, stated in the entry.
- **Both NULL:** no exit change; the guide records that the monitor's EXIT tier does not improve on
  holding to the tenth session once the damage already done is matched, and F6 effort moves to the
  lane and band exit questions already registered.
- Owner: implementer. Ship flag-off with a byte-identical checksum on the old path; shadow ≥ 20
  trading days before any flip (rule 11). **Every check a brief following from this question hands the
  coding agent must be satisfiable from the platform repo alone** — the test suite, a pure-function
  import, `git show --stat`, a file diff. Anything that reads or writes a table belongs in the brief's
  verification section addressed to the **Data Steward** on `$RESEARCH_DB_URL`, or to Haci where a
  write is required; a "prove you didn't change the tier logic" check is written as **the diff that
  proves it**, never as "re-run the monitor and compare" (DP-49). Where this question's pinned freeze
  covers the affected table, the brief names that parquet as the before-snapshot rather than asking
  anyone to capture one (DP-50(c)).

## 10. Known threats to validity (registrar's own list)

1. **The flag is a function of the path, so the naive contrast is a momentum contrast.** This is the
   dominant threat and it is why DP-12's damage-matched control is the primary and §8 clause 7 exists.
   Residual risk: `dam` measures damage at the *close of `s`* in ATR units and does not capture
   *how* the name got there (one gap versus five drifting sessions). The `dam` tercile sub-cell, the
   post-match standardized mean differences and the B4 panel are the reads on what is left.
2. **An early exit is flattered by a falling tape.** Plan C shortens exposure, so in a weak tape it
   wins mechanically. The matched control removes most of this (it exits at the same `Open_{s+1}` over
   the same calendar stretch), and §8 clause 6 requires the sign to hold in every tape stratum with
   20+ nights. Nothing here speaks to the strong April–May tape, which is outside the window.
3. **WATCH conflates "weakened" with "our data was missing."** `polarity_unavailable_coverage_low`
   returns WATCH (`:184-185`), and a missing qualifying-day blob or a failed analyzer call returns
   UNKNOWN per timeframe (`:663-682`). EXIT is not affected — UNKNOWN never promotes to EXIT
   (`:736-785`, `:792-804`) and polarity EXIT needs a real flip — which is exactly why the primary
   trigger is EXIT only and WATCH is a labelled secondary. **Measured (R1 item 6): the polarity gate
   is not a hazard to watch, it has already fired everywhere** — `polarity_unavailable_coverage_low`
   on **100%** of in-scope rows in every month June–September 2026, 0 exceptions, so the polarity arm
   contributes nothing to any tier in this window and the EXIT tier is the technical arm alone (§1
   restriction 1). `technical_overall_tier = 'UNKNOWN'` is negligible (0.75% in June, 0 thereafter),
   and WATCH rows whose *only* reason code is an availability code are ≤ 1.06%. The shares stay
   printed monthly, on the successor nights too (R2 clause vi).
4. **The tier's meaning may change inside the window — and the live version of this threat is not the
   one first anticipated.** Six named dampening changes live in the service (the ATR breach buffer,
   info/weak recategorisation, dedupe, concurrence rollup, aged-TF cap, orientation gate). **Measured
   (R1 item 7): all of them are bundled in three same-day commits dated 2026-05-16, before the window
   start, and nothing has touched the tier logic since** — so the *code* branch of this threat is
   closed for the sealed portion and watched for the rest (R2 clause v). The live branch is its mirror
   image: **an input that has been dead since before the window and could come back inside it.**
   Restoring polarity coverage changes which picks receive `EXIT` exactly as a logic change would, so
   §5's window-start rule covers **any dated change to what the tier means — a tier-logic ship *or* the
   restoration of a structurally-unavailable input** (DECISIONS #11, #12(a)), the date taken from the
   ship SHA and its `DATA_NOTES.md` entry; an **undated** recovery moves nothing and is printed by
   month. The desk cannot see either from the frozen data alone — the rows carry no engine-version
   column, unlike `market_regime` and `sas_excursion` — which is why R2 clauses (vi) and (vii) exist.
5. **Monitor rows are delete-and-reinsert, and the entry point accepts an arbitrary `--trading-date`.**
   A re-run for a past date would write today's price action under that date and the original row
   would be unrecoverable (`:1097-1101`; `scripts/run_conviction_monitor.py:38-62`). The §2
   `created_at` / `updated_at` guard is the defence and its drop counts are printed; **measured
   in-window it drops nothing — 0 failures June–September, all 160 in the freeze are May 2026** — so
   the sealed portion is clean and the guard's job is on the successor nights. Under DP-50 the
   research role reads the same rows the platform writes, so a future repair could rewrite monitor
   history; nights ≤ 2026-09-10 are pinned to `manifest_v001` and are safe by rule 4 (DP-50(d)), and
   **any repair that touches this table — the tier logic, the age decay, or the polarity input that
   feeds it — must be checked against this question's decision date before a fix brief is written, and
   the constraint is named in the issue entry itself, with both branches** (DP-50(b), §9).
6. **The monitor's window is 5 weekdays, not 5 sessions,** and the job is cron'd Mon–Fri
   (`0 02 16 * * 1-5`). Across a holiday the effective age in sessions is shorter than
   `days_since_qualified`. The row's own `trading_date` is authoritative throughout (§2) and
   `days_since_qualified` is used only for the B2 age caliper and the age sub-cell.
7. **The control pool is small before matching — and this threat is realized, not hypothetical.**
   Eight or so published picks per night, five ages, one session; the pool at a given `s` measures
   14.5 candidates across ≈ 4.2 originating pick nights, better than the per-night framing suggests,
   **but the `dam` caliper still empties for the largest drawdowns: 195 of 284 flagged picks (68.7%)
   are dropped for want of a control, and the dropped tail is the more damaged one (mean `dam` −0.94
   vs −0.17 ATR)**. The loss is counted and printed by month and by half; the consequence is §1
   restriction 3 — the answer speaks for **ordinary-damage** EXIT flags and makes no claim about the
   worst drawdowns. The caliper is **not** widened to retain the tail: that would be re-tuning a
   registered definition against measured data (DP-12, cost paid rather than softened).
8. **The published/monitored gap.** The freeze holds more published rows than `qualified IS TRUE` rows
   over the full history (FREEZE_v001 §1) and the monitor loads on `qualified IS TRUE`
   (`:1043-1051`), so some published picks are unmonitorable. They are excluded and counted; the
   exclusion is not random with respect to the publication path, so the rate is printed per month.
   **Measured in-window the gap is zero — 0 of 465 published picks lack an in-scope monitor row** — so
   the full-history figure is not the right prior for this window, and the monthly print stays as the
   diagnostic against which the successor nights are compared rather than as evidence of a problem.
9. **A 10-session terminal is arbitrary** — it is H-050's own number, kept as written (DP-25). The
   `t+5` and `t+20` horizons are printed as sensitivities and never decide; a materially different
   answer across horizons is reported in the decision paragraph.
10. **±1 ATR over a 5-to-9-session stretch may resolve as "neither" often.** P2 counts "neither" as
    not-adverse-first, which is the unconditional form and the honest denominator; the neither-rate is
    printed per arm. The fixed-10-sessions-from-`s` race is the pre-registered alternative shape and
    is descriptive.
11. **No stops are assumed** (rule 5, DP-02). Both plans hold through the adverse level; a reader who
    stops out would see different money and §9 must say so.
12. **Overlapping forward windows across adjacent pick nights** inflate precision. The block length
    (5 sessions) and the two clusterings are fixed here, before any result, and the wider CI decides.

---

## Decisions before lock

Recorded in DECISIONS.md (2026-09-13). Routed items still open: **R2 — the successor freezes
(`manifest_v002` / `manifest_prices_v002`, including the `conviction_monitor` table key, the add-only
successor exclusions file, and clauses (vi) monthly polarity composition and (vii) the dated SHA of
any restoration), routed to the Data Steward, due before the decision pass and not a blocker for lock
(DP-23).** Nothing else is open: the three drafted items were DECIDED on existing policy, one schedule
item was DEFAULTED under DP-43, and the remaining items were settled at `record` on the Steward's
measured counts.
