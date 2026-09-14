# Q034 — economic_objective: of the nine ways the desk can measure a pick, which one does VolatilX actually predict best?

**Status:** PREREG_DRAFT (lock by committing this file; `--by desk`, DP-46)
**Decisions:** DECISIONS.md (decision-maker, 2026-09-14, `decide` + `record`; 21 items, 8 corrections)
**Family:** **F8 System validity** (hypothesis **H-084**, Haci's Master Hypothesis Program **H14**,
*Economic objective*), as filed in BACKLOG.md.
**Type:** **DIAGNOSTIC / objective comparison. No primary endpoint, no MPE, no BH, no q-value.**
Every objective is pre-listed here, every one prints whatever its sign, and **none of them decides an
edge**. What the question produces is an **objective-comparison register**: the same picks, the same
matched controls, the same nights, nine pre-registered measurements, one common scale, and a fixed
rule for when the register is allowed to name a winner. **Every number it produces is
`NON_QUOTABLE`** (rule 12) and no branch of it supports a subscriber-facing claim.
**Rule 5 is not moved by this question.** The desk's objective is fixed by how the pick is traded
(rule 5, DP-01); H-084's own text says so. This question reports whether that choice is also where
the measured signal is largest — and if it is not, the consequence is a **new registered question**,
never a change of objective made while looking at the table.
**Manifest (borrowed exposure counts and R1 only — no night that enters the register comes from it):**
research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA
fa70688bc252d14f8d67e371afafc194731c324e).
**Manifest (prices; same scope — R1's bound-direction arm measurement only):**
research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374).
**Successor freezes — the register itself (built and pinned at the decision date, DP-23; §5.3 R2):**
a selection freeze (`sas_candidates` **every row, published and unpublished**, `sas_runs`,
`market_regime_daily`) and a price freeze (daily bars for **every candidate symbol on every in-window
night**, hourly bars for published symbols, **and SPY split-adjusted daily bars from 2025-01-02**),
covering pick nights **2026-09-15 .. 2027-04-30** with daily bars through **2027-07-28** (session
t+60 of the last included pick night, on the corrected holiday list — DECISIONS Correction 1) and
≥ 60 prior sessions before 2026-09-15; a second pair **only if** the single DP-13 extension fires,
covering pick nights **.. 2027-06-14** with bars through
**2027-09-09**. This is Q033's R2 build with the daily tail extended from t+40 to **t+60**, because
this question's deepest objective runs on the long lane's own 60-session window. **Every night that
carries a line in this register is after this lock and exists in no manifest pinned today**
(`pin_at_decision`, DP-23 — the Q027 / Q031 / Q032 / Q033 pattern). The successor manifests are named
in prose and deliberately not written as `**Manifest …:**` header lines, because no such file exists
yet and the pin step reads every `**Manifest` line as a path.
**Exclusions:** research/data/exclusions_v003.json (DP-22 — **verified the newest file on disk** at
this lock: v001, v002, v003 present; it is not edited, `research/data/` is not writable from here)
unioned with the
**add-only successor exclusions file** issued with the successor selection freeze — the identical
**four** criteria Q027 fixes at its lock (`manual_runs` ∪ `non_session_runs` ∪
`uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10. The
successor file may only **add** nights, never remove one from a v003 list; the **criteria** are fixed
at this lock even though the
**dates** cannot be. Both paths are `eval.py` inputs; no hard-coded file name, no hard-coded date.
DP-04 applies mechanically on top. **The fourth criterion is load-bearing here** (DECISIONS item 11):
on a `payload_disabled` night the published slate carries no `lane_plans`, so there is no ladder, no
`d_L3` and no eligible pick for any of the nine — the night is excluded whole rather than entering as
nine zeros (R1 §(e) measured exactly one such night, 2026-06-02, on the exposure period).
**Code read for definitions:** the read-only platform repo at the frozen SHA
`fa70688bc252d14f8d67e371afafc194731c324e` (`git show fa70688:<path>`), never HEAD.
**Script by:** Researcher (rule 9, written once from §4) · **Run by:** Researcher, once, on the
decision date. **No interim looks.** **`eval.py` is committed no later than Monday 2027-04-05**, its
sha256 recorded, and is not touched afterwards (DECISIONS item 16; §5.2) — the extension run uses the
byte-identical file.
**Determinism (rule 9):** fixed RNG seed **`20260914`**; 2,000 resamples for each bootstrap, 10,000
permutations for each per-objective sign-flip reference; `eval.py` prints the seed, the counts and
its library versions in the register header.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14

---

## 1. Hypothesis (plain English, one sentence)

**Among the nine ways the desk can measure what happens to a published pick after it is published, at
least one shows an advantage over the pick's same-night look-alikes that keeps its sign in every
window — and the nine differ enough from one another that one of them can be named the strongest.**

BACKLOG **H-084** is Haci's H14: *"what does VolatilX actually predict best — determine the strongest
stable objective among return, direction, target-before-stop, ATR per trade, MAE / MFE and first
touch; FAIL no objective has persistent edge → Product A should not be marketed as a predictive
system."* It names the population (published picks vs Q006's distance-matched control, from the t+1
open), the nine objectives, the reporting form (one table, a night-bootstrap CI per objective,
sign-consistency across the rule-7 windows), the definition of the answer ("the largest standardised
excess that keeps its sign in every window, named descriptively") and the forking-path guard ("the
list closes at draft and every row prints, whatever its sign"). This PREREG fixes the exact nine
measurements, the common scale they are ranked on, the entry, the clocks, the windows, the estimator,
what "separated" means numerically, and what each branch does and does not license.

**Label mapping, fixed here so the verdict cannot drift:**

| register label | H14 reading | controller verdict |
|---|---|---|
| **SEPARATED** — one objective is named strongest and stable | the strongest stable objective is identified | HISTORICALLY_CONFIRMED |
| **NO_SEPARATION** — at least one objective is stable and non-zero, but no single one separates from the rest | the question is answered "several, indistinguishably" | INCONCLUSIVE |
| **NO_STABLE_OBJECTIVE** — no objective's excess is non-zero and sign-stable | **H14's FAIL** | NULL |

**PROSPECTIVELY_CONFIRMED is not requested in any branch, and the reason is not a window.** The window
*is* prospective and DP-24 is satisfied by construction (§5). It is declined because this question
registers **no primary endpoint, no MPE and no family correction**, and it makes **nine simultaneous
comparisons** on one dataset. A verdict with those properties must not become the basis of a
subscriber-facing claim (rule 10, rule 6's MPE requirement). The verdict therefore carries the fixed
label **`DIAGNOSTIC — no primary, no MPE, no BH`** beside `NON_QUOTABLE` wherever it is restated,
ledgered or quoted, and the only thing a SEPARATED register licenses is **a new PREREG on the named
objective**, with its own MPE, its own family and its own prospective window (§9).

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are reduced to one number per night per
  objective first; nights are the observations. Control rows never add to inferential n.
- **Source tables (the successor selection freeze, §5.3 R2):** `sas_candidates` — `trading_date`,
  `symbol`, `qualified`, `selected_rank`, `overall_score`, `dominant_direction`, `best_timeframe`,
  `confidence_level`, `public_payload_json` → `lane_plans.{day_trading, swing_trading,
  longterm_trading}.{entry, stop, targets}` and `analysis_status`, `outcome_target_invalid`
  (exclusion audit only), `score_details_json` (the band-integrity check, §10 threat 9),
  `context_json`; `sas_runs` — `finished_at` (DP-04), `config_json` (the weights / publication-gate
  audit, §10 threat 8); `market_regime_daily` — `market_regime`, `regime_version`, `created_at`,
  `data_quality`: the platform's point-in-time label, a **registered stability window** in every branch
  (§2.2, DECISIONS item 3) and a composition cross-check, never an arm contrast and never a q (§4.3,
  §4.4).
- **Source tables (the successor price freeze, §5.3 R2):** `prices_daily_split` (pick-night close,
  ATR14, beta60, atr_pct, runup20, the t+1 open, forward bars to t+60, **and SPY from 2025-01-02** for
  the §2.2 cells), `prices_daily_raw` (split-factor snapping only), `prices_hourly_raw` (published
  symbols; the same-session ordering tie-breaks of §4.0 and the descriptive entry audit).

### 2.1 Treatment rows — exact filter

**The two dates below are illustrative of values `eval.py` receives as inputs.** §5.3 R2 requires the
script to take the window start, the window end, the manifest paths, the exclusions-file paths and the
output directory as arguments, with **no hard-coded date, manifest name or path**, so that the
byte-identical script serves the primary run and the DP-13 extension run alike.

```sql
SELECT c.*
FROM   sas_candidates c
JOIN   sas_runs run ON run.trading_date = c.trading_date
WHERE  c.qualified IS TRUE
  AND  c.selected_rank IS NOT NULL                   -- publication predicate, DP-28
  AND  c.trading_date  >= DATE '2026-09-15'          -- §6 window start   (input, illustrative)
  AND  c.trading_date  <= DATE '2027-04-30'          -- §5.2 window end   (input, illustrative)
  AND  c.trading_date NOT IN (<exclusions_v003 ∪ the add-only successor exclusions file:
                               manual_runs ∪ non_session_runs
                               ∪ uncorroborated_publication_runs ∪ payload_disabled_runs>)
```

**No score-band filter** (DP-25: H-084 is about the published slate); band is a stratum and the 90+
cell is SUPPRESSED at lock (§4.4). **No direction filter:** bull and bear published picks both enter,
direction-adjusted throughout, with a **bull-only companion** printed for every objective (H-062: bear
picks graded below base rate in-sample). Dark-lane rows (`qualified` false or `selected_rank` NULL) are
**never** in the treatment arm (DP-28); they are the control pool (§3 B1).

### 2.2 The windows — calendar halves, a bar-only tape partition and the platform-label partition, fixed at this lock

H-084's answer is *"the largest standardised excess that keeps its sign in **every window**"*, so the
windows are part of the definition and are fixed here, in full, not by reference. **Whichever branch
runs, exactly four windows are registered** (DECISIONS item 3, Correction 3): the two calendar halves
and **two arms**, the bar-only tape arms where the SPY history exists and the platform-label arms in
every branch.

- **Calendar halves** (always available): **Half A = window sessions 1–79**, **Half B = sessions
  80–158**, fixed by session index at this lock and re-derived from the trading calendar (re-cut by the
  same rule if the extension fires, §5.2).
- **Tape arms** — the **identical** bar-only partition Q032 §2.2 and Q033 §2.2 register, computed from
  SPY split-adjusted daily bars dated **on or before** the pick night in the pinned price freeze.
  Nothing reads a platform column, so a regime-engine repair cannot move a night between cells
  (DP-50(a)). All cuts are registrar-chosen conventions fixed at lock and never derived from an outcome
  (DP-26):
  - **`SMA50_t`, `SMA200_t`** = the simple means of SPY's split-adjusted closes over the trailing 50 and
    200 sessions ending at t (inclusive).
  - **`trend_t`** = **`UP`** iff `close_t > SMA50_t` **and** `SMA50_t > SMA200_t`; **`DOWN`** iff
    `close_t < SMA50_t` **and** `SMA50_t < SMA200_t`; **`MIXED`** otherwise.
  - **`rvol_t`** = the sample standard deviation of SPY's daily log returns over sessions t−19..t,
    annualised by √252. **`vol_t`** = `LOW` / `MID` / `HIGH` by the **expanding-window** terciles of
    `rvol` over every SPY session in the pinned freeze dated ≤ t, requiring **≥ 250 such sessions**;
    below 250 the night is **excluded and counted** (inside the registered window this count must be
    **0**, or R2(i) did not deliver). Expanding, never full-sample.
  - **The two arms:** **BENIGN** iff `trend_t = UP` **and** `vol_t ∈ {LOW, MID}`; **HOSTILE** otherwise.
  - The **nine-cell** `trend_t` × `vol_t` composition is printed with contributing nights per cell.
- **Platform-label arms** (DECISIONS item 3 — a **registered stability window in every branch**, not a
  cross-check only). For night t: **`STRONG`** iff `market_regime_daily.market_regime =
  'strongly_bullish'` on a **legality-tested v1.2 row** — row dated t, `market_regime` not unknown,
  `data_quality` not insufficient, `created_at` dated t and ≤ that night's `sas_runs.finished_at`
  (Q032 §(d)'s test verbatim) — **`NOTSTRONG`** otherwise. A night failing the legality test carries
  **no** platform-label window and is **counted**. This is rule 7's own column; it is knowledge-time-legal
  for every night of this window (legal from 2026-06-09, FREEZE_v001 §7); R2(iv) delivers it with
  `created_at` and `regime_version` preserved; and Q032 §(d) measured it **non-redundant** against the
  bar-only arm (agreement 49/63 = 77.8%, the HOSTILE nights splitting 11/11). **`eval.py` fails loudly**
  if an in-window night's `regime_version` is not v1.2 (DP-06 / DP-50(a): a scorer repair makes it two
  features and splits this partition at the ship date, leaving the bar-only arms untouched — which is
  the point of registering both).
- **"Every window" = the two halves and the two arms of whichever partition the branch registers**
  (the bar-only arms when R2(i) delivers, the platform-label arms in every branch), each counted
  separately. A window enters the stability test **only where it clears 20 contributing nights** (§5);
  a window below 20 prints its count, leaves the stability test, and is **named** in the register's
  stability line. **The price of that leniency, fixed here** (DECISIONS item 14, Correction 5): a
  window short at the initial decision date fires the **single DP-13 extension** (§5.2), and after that
  extension **no objective may be named strongest unless the branch's full four-window set each clears
  20 contributing nights** — short of that the register's ceiling is **NO_SEPARATION (INCONCLUSIVE)**
  with the missing window named in the sentence (§8). A window shortfall is **not** a DEFERRED ground;
  DEFERRED stays with the ranking-set 80-night floor and Gate 0.
- **If the extended SPY history is not delivered** (the Q030 / H-074 provisioning blocker, §5.3 R2(i)),
  the tape arms print **`UNAVAILABLE`**, the stability test runs on the **two calendar halves and the
  two platform-label arms — four windows, not two** — and **every stability label in the register
  carries the fixed qualifier `STABILITY_WITHOUT_TAPE_ARMS`**, which says what is missing. **On the
  evidence available at this lock that is the branch most likely to run:**
  `STEWARD_Q032_exposure.md` §(g) (2026-09-14) reports `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` absent
  from the desk session, the SPY-from-2025-01-02 probe not attempted and no pinned alternative — the
  same failure that deferred Q032 outright and deferred Q033's P2. It defers nothing here, because no
  endpoint in this register is an arm contrast (DECISIONS item 17). Both branches are registered here,
  before the fact; a data failure may never remove a stability window, and the partition is **never**
  re-specified to an SMA50-only variant after the data exists.

### 2.3 Levels, entry, clocks — common to every objective

- **Direction** `dir` = +1 bullish / −1 bearish from `dominant_direction`. Every distance, every touch
  and every return is direction-adjusted.
- **`C_t`** = the pick's actual regular-session close on pick night t from `prices_daily_split` (never
  the platform's `spot_close` — EXPLORE_001 §9). **`ATR`** = ATR14 from `prices_daily_split` bars dated
  ≤ t (never the platform's `atr_pct` — DATA_NOTES / PI-003).
- **Entry `X` = the session t+1 regular-session open** (DP-03(b), DP-42), for picks and controls alike,
  for **every** objective. The **`C_t` basis (DP-03(a) / DP-11) is computed and printed as a named
  sensitivity for every objective** and never decides.
- **Levels.** `L1…L6` are the flattened lane targets: `lane_plans.day_trading.targets[0..1]` → L1, L2;
  `lane_plans.swing_trading.targets[0..1]` → L3, L4; `lane_plans.longterm_trading.targets[0..1]` → L5,
  L6 (volatilx `services/sas_conviction_card.py:182-195`). **The printed stop** is the **swing-lane**
  `stop` of the called-direction setup (DP-30, Q009 §2 verbatim — the lane whose target, L3, is the
  register's reference level).
- **Lane windows** (rule 5): L1/L2 within **20** sessions of `X`, L3/L4 within **40**, L5/L6 within
  **60**. Where an objective names its own clock (§4.1) that clock governs and is stated in its row.
- **Binding maturity: 60 sessions**, uniform across every eligible pick, so no objective is
  right-censored and every objective is measured on the same picks and the same nights.
- **A level at or through `X` at the t+1 open is not a hit** (rule 5): the indicator is 0, the pick
  stays in the denominator, and the not-takeable count is printed per objective per window. A gap
  through a level at a session open **is** a touch.

### 2.4 Exclusions — each counted, per window, printed in the register header, never silently dropped

Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or a
measurement failure. **None can move a night between windows** — the tape arm is a function of SPY bars
alone and the halves are a function of the calendar alone.

- **Nights** in the union of `exclusions_v003.json` and the add-only successor file, and any night
  whose `finished_at` is later than the next session's open (DP-04), mechanically.
- **Nights with fewer than 250 prior SPY sessions** in the pinned freeze (§2.2) → excluded, counted, and
  loud.
- **Null-ladder denominator:** no lane plan, or a lane whose `targets` an objective needs is absent →
  the pick is excluded from **that objective only**, counted, and stays in every other objective's
  denominator; the per-objective denominators are printed side by side (§4.3's `SET_SENSITIVE` flag is
  what keeps that from quietly changing a ranking).
- **Wrong-side or non-monotone ladder at the close:** any flattened level with `dir × (L − C_t) ≤ 0`,
  the six flattened levels **not monotone non-decreasing in the pick's direction (ties across lanes
  allowed** — the platform's own predicate `_ladder_is_monotonic`,
  volatilx `services/super_agent_select_service.py:180-192` at the pinned SHA `fa70688`: bullish
  `all(b >= a)`, bearish `all(b <= a)`, enforced by `_enforce_ladder_monotonic` at `:195-257`, whose
  docstring records that *"equal prices across lanes are allowed (non-strict monotonicity), as
  duplicates already exist in the book and grading handles them"***), or `outcome_target_invalid`
  non-null → the pick is excluded from every objective and counted.
  **This screen transcribes the platform invariant and reproduces its strictness** (DECISIONS item 21,
  Correction 7): the draft's earlier "strictly monotone" wording was a mis-transcription that would
  have excluded 429 of 550 rows (78%) on the exposure period, 388 of them **ties the platform blesses
  by design**, and would have selected a differently-constituted population (only picks whose six
  levels are all distinct) by accident. Nothing in this PREREG needs strictness: Gate 0(c)'s "T2
  indicator ≤ T1 indicator" holds with equality when `L_k = L_{k+1}`, O8 counts levels, and the book
  already carries duplicates. **Three guards ride with the correction, and none of them loosens
  anything:**
  - **(i) Loud flag.** `eval.py` prints this screen's **own firing rate per window and per objective**
    and **fails loudly** if it exceeds the pre-fix **25.71%** DATA_NOTES measures (36/140 before
    2026-07-06, **0.00%** — 0 of 355 — on/after, under this same non-strict definition). The whole of
    Q034's window sits after the 2026-07-06 `_enforce_ladder_monotonic` ship (§6), so a material rate
    is a **platform-defect flag**, not a silent drop.
  - **(ii) Counted strict companion.** The **strict** variant is printed as a counted companion — rows
    passing non-strict and failing strict — per window and per objective, so the register shows on its
    face what the reading cost and no later reader has to take it on trust. The companion decides
    nothing.
  - **(iii) Ties graded on both levels.** A tied pair `L_k = L_{k+1}` is graded on **both** levels, for
    picks and — through the identical `d_Lk` transfer of §3 B1 — for **controls alike**, so the two
    arms are treated identically and §4.6(c)'s within-lane identity holds with equality.
- **Validity bound** `d_L3 = dir × (L3 − C_t) / ATR ∉ [0.25, 10]` ATR → excluded and counted (Q027 /
  Q031 / Q033 §2.4 verbatim).
- **Wrong-side printed stop:** a swing stop on the wrong side of `C_t` (for a bullish pick, a stop above
  the close) is unusable. The pick is excluded from **O4 only**, counted, and stays in every other
  objective. Q009 §1 measured this at **66 of 371 (17.8%)** of in-sample published picks;
  `STEWARD_Q034_exposure.md` §(d) re-measured it at **103 of 542 valid rows (19.0%; 18.7% of all 550)**
  on 2026-06-01..2026-09-10 — the same signature, the same order — and O4's own contributing-night
  count is printed beside every other row.
- **Split-scale payload screen** (DATA_NOTES, the APH / KLAC / CRWD / MNST finding): excluded and
  counted if `lane_plans.day_trading.entry / C_t` is outside `[0.85, 1.15]` **and** a flattened lane
  level sits > 20 ATR from `C_t` (Q027 §2.4's joint screen, reused verbatim).
- **Missing forward bars** inside t+1..t+60 (halt, delisting) → ungradeable, excluded and counted; a
  measurement failure, never a classifier. A night is dropped if > 25% of its eligible picks are
  ungradeable. The 60-session tail makes this commoner than in the desk's 20-session questions (§10
  threat 6).
- **Fewer than 60 daily bars dated ≤ t** for the pick or a control (ATR / beta60 / runup20 undefined) →
  excluded, counted (the CTRA truncated-history signature, `STEWARD_Q023_exposure.md` §6).
- **Immature nights** — session t+60 after the last trading date of the pinned price freeze → excluded
  and counted. Maturity comes from the trading calendar, never from whether a price exists;
  right-censoring is never graded as a non-touch.

### 2.5 Contributing night, ranking set, episodes

- **Contributing night (the floor unit, DP-21):** a non-excluded in-window night carrying a legal §2.2
  window label and **≥ 3 valid published picks, each with ≥ 5 valid matched controls**, matured to
  t+60. This is Q031 §2.5's series-B rule verbatim — the rule the measured exposure rate in §5.1 was
  counted under (`STEWARD_Q031_exposure.md` §(a)) — with the maturity extended from t+20 to t+60; the
  rate and the rule are not allowed to drift apart, and R1(a) confirms that. A night surviving the
  night-level filters but carrying no eligible pick is a **non-contributing night, not an exclusion**,
  and is printed in the funnel.
- **The ranking set** (DECISIONS item 7, Correction 4) is the set of nights that are **§2.5 contributing
  nights** *and* on which **each of the nine objectives independently carries ≥ 3 valid published picks,
  each with ≥ 5 valid matched controls, after that objective's own exclusions are applied** — **O4**
  after the wrong-side-swing-stop screen, **O5** and **O8** after the requirement of a complete
  six-level ladder across all three lanes (`day_trading`, `swing_trading`, `longterm_trading` each
  carrying two targets), every objective after the shared §2.4 screens. The alternative reading — an
  objective computable for *at least one* pick — is **refused**: it would let a single pick carry an
  objective's night value where the floor asks for ≥ 3, and it is the reading that reaches the floor
  sooner (DP-45). **The ranking set is a subset of the contributing nights by construction**, so the
  80-night floor is projected on the ranking-set rate and never on the wider contributing-night rate
  (§5.1). The per-objective night counts print side by side with the binding objective named. Every
  objective additionally prints its value on its **own** full night set; where
  the two differ by more than **0.05** in the common-scale statistic `D` (§4.2) the row is flagged
  **`SET_SENSITIVE`** and **cannot be named strongest** (§8). The ranking is computed on the ranking
  set only.
- **Symbol-episode (DP-51 only):** one symbol's run of *published-pick appearances* with gaps of ≤ 10
  sessions between successive appearances (the TI-003 / Q003 window). It appears **only** in the §4.5
  second CI; it never defines a night and never gates a floor.
- **Tape-episode (descriptive here):** a maximal run of consecutive *sessions* carrying the same §2.2
  arm label — of **whichever arm partition the branch registers**, the bar-only arms or the
  platform-label arms; an excluded night or a night without a legal label does not break a run. If the
  rarer arm's contributing nights sit in fewer than **3** tape-episodes, every stability label carries the fixed
  qualifier **`ARM_IS_ONE_STRETCH`** — a naming clause, not a floor, because no arm contrast is
  estimated here and no p-value is taken against the arm labels.

### 2.6 What is not read

`sas_selection_excursion.*`, `outcome_*` and `level_hit_*` are **never inputs** (calendar windows, close
basis, recomputed weeks later — volatilx `services/sas_excursion.py:8-18`, `:336-354`; DATA_NOTES).
`uoa_symbol_daily.fwd_return_*` is **banned** (FREEZE_v001 §5). Every touch, excursion and return in
this register is computed by this question's own `eval.py` from the pinned price freeze, and no number
is ever read from another question's `results/`.

## 3. Baseline(s) — what every row of the register is measured against

**There is a baseline inside every objective by construction**, and it is the same one for all nine.
An objective with a raw rate and no control would be descriptive (rule 5); none appears in this
register except as a printed companion.

- **B1 (rule-5 distance-matched control): the Q006 §3 B1 construction verbatim.** For each eligible
  pick, the **10 nearest same-night non-published `sas_candidates` rows** on `beta60` / `atr_pct` /
  `runup20` computed from `prices_daily_split` bars dated ≤ t, standardized by the night's
  cross-sectional median and MAD, Euclidean distance, with replacement across picks, ties broken by
  symbol ascending. Each control carries **every** synthetic construct the nine objectives need, at the
  **identical ATR distances** and the pick's direction, graded from the control's own t+1 open under
  exactly the §2.3 rules: the symmetric ±0.5 ATR band; a full synthetic ladder
  `L_k,c = close_c × (1 + dir_p × d_Lk,p × atr_pct_c)` for k = 1..6; a synthetic stop at the pick's own
  stop distance in ATR; and the same committed exit fractions. Controls **never add to inferential n**
  (rule 6). A pick with fewer than **5** valid controls is dropped and counted, **never imputed**; the
  measured cost of that floor on this population is **zero** (`STEWARD_Q031_exposure.md` §(b): pool
  depth min 37, median 54, no night below 10).
- **B2 (printed beside every row): the control's own level.** For each objective, the matched control's
  own value — the rate, the ATR, the excursion — per window, with its own CI. "Y's rate when X did not
  happen, in the same regime" is exactly this: what a same-night stock SAS looked at and did not publish
  did, at the same distances, on the same bars.
- **B3 (the reference each raw p is taken against): a paired sign-flip permutation** of the night series
  of that objective, 10,000 permutations, seed 20260914. Raw p only; **no q** (§7).
- **B4 (the reference the *ranking* is read against): the joint night bootstrap's argmax distribution.**
  Resampling nights jointly across all nine objectives (§4.5) gives, for each objective, the share of
  resamples in which it is the largest — the **argmax share**. It is the honest measure of how arbitrary
  a winner among nine correlated objectives is, and §8 makes it a blocking condition. Bootstrap and
  permutation draws are Monte Carlo and **never add to n** (rule 6).
- **B5 (descriptive, never a baseline for a label): the unadjusted values.** Every objective's raw pick
  value and raw control value, per window, printed beside the control-adjusted number so the control's
  work is visible.

## 4. Objective metric — the objective-comparison register

**Rule 5 governs what may be *decided*, and this question decides no edge.** Fixed-horizon returns
appear here as **two of the nine pre-listed measurements**, which is what H-084 asks for; they carry no
verdict, and §8 states in terms that **no plan, guide line, brief, flag or quoted number may ever be
written on a fixed-horizon return** (rule 5, DP-01), whatever the register shows. **DP-10, DP-20 and
DP-44 (MPEs) are inapplicable and are cited here to record that they were considered:** there is no
effect to clear, and the thresholds of §8 serve the MPE's role — they are fixed here, before the run,
and are never adjusted afterwards (the Q005 / Q026 / Q028 pattern).

### 4.0 Common definitions, fixed before the run

- Entry `X`, direction `dir`, `ATR`, the six flattened levels, the printed swing stop, the lane windows
  and the 60-session binding maturity are §2.3's, identically for picks and controls.
- **Touch** = the regular-session high (bullish) / low (bearish) reaching the level; a gap through at a
  session open is a touch; a level at or through `X` at the t+1 open is not (§2.3).
- **Same-session ordering.** Where two events of a race (own-side vs counter-side; L3 vs stop) fall on
  the same session and `prices_hourly_raw` cannot order them, the tie is scored **against the pick and
  for the control** — the assignment that makes the excess smaller (DP-27's conservative principle,
  applied to a diagnostic that has no hypothesised direction). Hourly bars exist for published symbols
  only, so control ties are always resolved this way; the counts are printed per objective, per window,
  for picks and controls separately.
- **Sign convention:** every objective is defined so that a **positive excess means the pick did better
  than its controls**. O6 (adverse excursion) is therefore signed `control − pick`; the register prints
  the convention in the row.
- **No winsorization decides anything.** Raw values are used throughout; a 1% / 99% winsorized companion
  is printed for O1, O2, O5 and O7 and never decides.

### 4.1 The nine objectives — the list closes here and every row prints

Per pick `p` on night `t`: `x_p` is the pick's value, `ctrl_p` the mean of the same construction over
that pick's ≥ 5 matched controls, and the night's excess for the objective is
`e_t = mean_{p ∈ P_t} [ x_p − ctrl_p ]`.

| id | objective | `x_p`, exactly | units | clock |
|---|---|---|---|---|
| **O1** | 5-session return | `dir × (close_{t+5} / X − 1)` | fraction of price | 5 |
| **O2** | 20-session return | `dir × (close_{t+20} / X − 1)` | fraction of price | 20 |
| **O3** | direction (path form) | 1 if `X + dir × 0.5 × ATR` is touched **strictly before** `X − dir × 0.5 × ATR`, else 0; an unresolved race scores 0 and stays in the denominator | rate | 20 |
| **O4** | target-before-stop | 1 if `L3` is touched **strictly before** the printed swing stop, else 0 (Q009's race; DP-30's stop; DP-02 — the stop is measured, never used as an exit) | rate | 20 |
| **O5** | ATR per trade, committed plan | realized result of **Plan H** (§4.1.1) from `X`, divided by `ATR` | ATR | 60 |
| **O6** | adverse excursion | `−` (maximum adverse excursion from `X` in ATR); the night excess is `ctrl − pick` so that positive = the pick drew down less | ATR | 20 |
| **O7** | favourable excursion | maximum favourable excursion from `X` in ATR | ATR | 20 |
| **O8** | ladder reach | the count of `L1…L6` first-touched **within each level's own lane window** (L1/L2 ≤ 20, L3/L4 ≤ 40, L5/L6 ≤ 60) | count, 0–6 | 60 |
| **O9** | speed | 1 if `L3` is touched within **5** sessions of `X`, else 0 (Q002's S3) | rate | 5 |

- **O3 is fixed here and is not conditional on any other question's lock** (DECISIONS item 10). The
  band is the symmetric **±0.5 ATR** band from `X`; an **unresolved race scores 0** with the pick kept
  in the denominator; a same-session pair that hourly bars cannot order is scored **against the pick
  and for the control** (§4.0, DP-27) — for picks and matched controls alike. Those three choices were
  settled for this measurement by **Q033 DECISIONS #1 and #2 (2026-09-14)** and hold **whether or not
  Q033 itself locks**: if Q033 goes to DEFERRED on its own counts, O3 keeps this definition and
  `eval.py` cites Q033 DECISIONS #1/#2 rather than a PREREG section that may never exist. The draft's
  "this row moves with Q033's lock" clause is **struck** — a definition that can move after this lock
  is not pre-registered (rule 3). The **±1.0 ATR variant** is a printed companion that decides nothing,
  and **H-081's filed fixed-horizon proxy** (the sign of the 20-session move) is printed beside O3 as a
  named companion and is not one of the nine.
- **O4** is Q009's race definition on the DP-09 clock (L3 within 20 sessions from the entry); the
  40-session companion is printed and is not one of the nine.
- **O8** prints its **six per-level first-touch rates and sessions-to-touch** as sub-rows; those
  sub-rows are companions and **do not enter the ranking** — the ranked object is the single count, so
  that one objective cannot occupy six of the nine ranking slots.

#### 4.1.1 Plan H, for O5 (inherited from Q012 §4, single position, no recycling)

Enter at `X`. Each fraction of `BAND_EXITS[band(pick)]` (volatilx
`scripts/generate_sas_trading_guide.py:89-95`, the pick's **own** band row) exits at the **first touch**
of its level within 60 sessions, at the level price — or at that session's open if the session opens
through the level. A fraction whose level is at or through `X` at entry is **unfillable** (rule 5): it
is recorded, counted, and closed with the remainder. The remainder closes at the session t+60 close.
**No stop** (rule 5, DP-02). The written trailing and max-hold text is not deterministic enough to
simulate and is ignored (the Q011 / Q012 precedent). Controls run the identical plan on their synthetic
ladder at the identical ATR distances with the identical fractions.

### 4.2 The common scale — how nine different units are compared

Rates, fractions of price, ATR and a count cannot be ranked in their native units. The register ranks
on a **unit-free, n-free, within-night standardized excess**, and prints the native-unit excess beside
every row, always.

- For objective `o`, night `t`: `g_{o,t} = ( mean_p x_p − mean_p ctrl_p ) / s_{o,t}`, where `s_{o,t}` is
  the **pooled within-night standard deviation** of that objective's value across the night's eligible
  picks **and** their matched controls. Where `s_{o,t} = 0` the numerator is zero by construction and
  `g_{o,t} = 0`; those nights are counted and printed.
- **`D_o = mean_t(g_{o,t})`** over the ranking set (§2.5), with **both** CIs of §4.5. `D` is what the
  ranking reads.
- **`E_o = mean_t(e_{o,t})`** in the objective's native units, with both CIs, printed beside `D_o` in
  **every table, every window, always**. A register line that quotes `D` without `E` is **malformed**
  (DECISIONS item 1).
- The scale is a Registrar convention fixed at draft (DP-26) and derived from no outcome. Its known
  distortion — a standardized effect is inflated for a near-degenerate binary objective (O9 at 5
  sessions is the candidate) — is §10 threat 2; it is bounded by the printed `E` and the printed raw
  rates (B5), and where an objective's `D` and `E` ranks disagree the register **names the
  disagreement in its own verdict sentence** (§8). It is never used to promote a row (DP-45).
- **The night-series alternative `mean_t(e_t) / sd_t(e_t)` is refused, and on arithmetic rather than
  taste** (DECISIONS item 1): its denominator is the **between-night dispersion of a mean excess**,
  which shrinks as a night's eligible-pick count grows, so it would rank the nine objectives partly by
  **how many picks carry each one** — and the nine have deliberately different denominators here (O4
  loses the wrong-side stops, O5 and O8 the incomplete ladders). `D` ranks on a quantity whose
  denominator is a within-night dispersion of the same picks.

### 4.3 What the register reports, per objective, per window

For each of the nine objectives, in the pooled ranking set and in **each** window of §2.2:
`D` and `E` with both CIs; the raw pick value and the raw control value (B5); the contributing-night
count; the eligible-pick count; the not-takeable count; the unresolved-race and same-session-tie counts;
the raw sign-flip p (B3); the argmax share (B4); the sign in each window; the `SET_SENSITIVE` flag; the
bull-only version; and the `C_t`-entry sensitivity.

**Printed always, entering the ranking never:** the six per-level touch rates and sessions-to-touch; the
counter-direction level touches and the maximum adverse excursion at 40 and 60 sessions (reported, never
an exit — DP-02); the 40-session companions of O4 and of the L3 touch; H-081's fixed-horizon direction
proxy; the ±1.0 ATR band variant of O3; the winsorized companions; the nine-cell `trend × vol`
composition; the **strict-variant ladder-screen companion and the screen's own firing rate** per window
and per objective (§2.4).

**The platform's point-in-time `market_regime_daily` label is a registered stability window *and* a
composition cross-check** (DECISIONS item 3, Correction 3 — amending the draft's "descriptive
composition cross-check only"). Its `STRONG` / `NOTSTRONG` arms are defined in §2.2, carry the same
20-night floor as every other window, and enter the stability test in **every** branch. They
nevertheless **carry no q and define no arm contrast**: no estimate in this register is a difference
between them, and the same statistic on this population as an arm contrast is Q023's locked E1 and
Q032's C1 (§7). Nights failing the v1.2 legality test carry no platform-label window and are counted.

**The objective-correlation panel, printed always and named beside any SEPARATED label.** The **9 × 9**
matrix of Spearman correlations between the nine night series `e_{o,t}`, and the **effective number of
independent objectives** `N_eff = (Σλ)² / Σλ²` of that matrix (Q028's participation ratio). A winner
among nine objectives that behave as three is a weaker statement than a winner among nine that behave
as nine, and §8 requires the register to say which it is.

**Sub-cells — the list is FIXED at lock, was revised once at `record` from R1's measured counts, and is
now CLOSED** (DECISIONS item 13). **No cell was added and none may be removed**: R1 projects no
not-suppressed cell below 20 contributing nights at session 158. **SUPPRESSED at lock** (counts only,
no point estimate): the `90+` band (structural — `publication_floor = 80.0` since 2026-07-07, 2–3 elite
picks a month, PI-010); bear-only as a *reported* cell; `confidence_level` terciles; `best_timeframe`
cells; `d_L3` terciles; `atr_pct` terciles; any of the nine `trend × vol` cells and any window below 20
contributing nights. **NOT suppressed:** the two halves; the two tape arms; the **two platform-label
arms**; the 80–90 band (which is nearly the whole population — §10 threat 5); bull-only. Suppression
restricts **affirmative reporting only and never removes a blocker**: a cell suppressed at lock stays
suppressed even if it clears 20 measured nights at the decision pass, and a cell not suppressed still
needs ≥ 20 **measured** contributing nights to print. The nine ranked rows, the two halves, the two
arms of the registered partition and the bull-only companion are never on the list and block at
whatever count they have.

**Quotability:** **every number in this question is `NON_QUOTABLE`** (rule 12), in every branch, on
every basis.

### 4.4 Stratification the register must print (rule 7)

The rule-7 stratification is **four windows in every branch**: the two calendar halves and the two arms
of §2.2 — the bar-only tape arms where R2(i) delivers the SPY history, and the **platform's
point-in-time `market_regime_daily` arms, which are a registered stability window in every branch**
(DECISIONS item 3) and additionally a composition cross-check. Both partitions run where both are
available. Platform-label nights are used only where the v1.2 legality test of §2.2 passes; the rest
are counted and carry no platform-label window. Neither partition defines an arm contrast and neither
carries a q (§4.3, §7).

### 4.5 Inference — two CIs on every number (DP-51), and one joint resampling

Night-level throughout; control rows never add to n (rule 6).

- **CI-1 (the registered interval).** A stationary block bootstrap over the ordered contributing nights,
  expected block length **10 sessions** (the desk's standing value, fixed at lock), 2,000 resamples,
  percentile 95%, with a plain date-clustered CI printed alongside.
- **CI-2 (DP-51).** A **symbol-episode-clustered** bootstrap resampling symbol-episodes (§2.5) and
  nights **jointly**, 2,000 resamples, percentile 95%. **DP-51 applies here as a gate, not a footnote:**
  a stability or separation condition met on CI-1 and not on CI-2 is **not met** (§8). The threat is
  live — the same handful of symbols recur across consecutive nights with overlapping 60-session
  windows.
- **All nine objectives are resampled together, night by night**, in both bootstraps. This is what makes
  the pairwise comparisons of §8 legitimate: the nine series share the same picks, the same controls and
  the same bars, and independent bootstraps would produce intervals that cannot be compared to one
  another. The **argmax share** (B4) is read off the same joint resamples.
- **Raw p per objective** from B3's paired sign-flip permutation, 10,000 permutations, seed 20260914,
  printed and marked *"raw p, no correction, does not decide"* (§7).
- **Every estimate prints:** contributing nights total, per window and on the ranking set; nights dropped
  from the ranking set and why; symbol-episodes and their length distribution; tape-episodes per arm;
  contributing nights dated after the lock commit; eligible picks; control rows used and picks dropped
  for < 5 controls; post-match standardized mean differences on `beta60` / `atr_pct` / `runup20`;
  exclusions by reason; the nine-cell composition; the 9 × 9 correlation matrix and `N_eff`; seeds,
  resample counts and library versions.

### 4.6 Gate 0 — positive control and construction check (run first, read first)

Every item is a pre-stated, binary, row-level condition. If any fails, the register is **INCONCLUSIVE**
and nothing else in it is interpreted (§8).

(a) **Match quality.** The post-match standardized mean difference between picks and their matched
controls is **|SMD| ≤ 0.25** on each of `beta60`, `atr_pct`, `runup20`, pooled and in each window. The
per-night distribution is printed.
(b) **Nested-window identity.** For every pick and every control, row by row: the L3-touch indicator at
5 sessions ≤ at 20 sessions ≤ at 40 sessions; the L1 indicator at 20 ≤ at 40 ≤ at 60. Any violation is a
script defect.
(c) **Within-lane monotonicity identity.** For every pick and every control, on each lane's own window:
the T2 (deeper) touch indicator ≤ the T1 indicator. Guaranteed by the **non-strict** monotone ladder
screen of §2.4 — the identity **holds with equality** when two levels tie (`L_k = L_{k+1}`, which the
platform's own invariant allows and which §2.4(iii) grades on both levels for picks and controls
alike); any violation is a script defect.
(d) **Denominator identity.** For every objective and every night: hits + misses + per-objective
exclusions = eligible picks, exactly. No silent drop anywhere.
(e) **Range identities.** `MFE_20 ≥ 0` and `MAE_20 ≥ 0` in ATR for every pick and control;
`O8 ∈ {0,…,6}`; O5's realized result lies between the worst and best level-price outcomes of its own
ladder; `s_{o,t} ≥ 0` with the `s = 0` nights counted.
(f) **Sign-convention check.** On a fixed, pre-declared 20-row sample printed in full, the sign of each
objective's excess is shown to mean "the pick did better" in the direction §4.0 declares.

The fix-and-re-run loop is bounded at **two passes inside the hard stop of §5.2**, each recorded with
its diff and date, each reusing the seed. **No Gate 0 target is relaxed to make a pass succeed.**

## 5. Sample floors, expected n, window and schedule

### 5.1 Floors (rule 6 as read by DP-21) — applied in the strictest available form, none waived

This question has **no primary endpoint in the effect-size sense**, so rule 6's floors do not bind in
their usual form. They are applied as follows, and none is waived:

- **An objective row may be reported affirmatively only with ≥ 80 contributing nights** on the ranking
  set (DP-21's per-primary reading, applied per row).
- **A window enters the stability test only with ≥ 20 contributing nights** (DP-21's cell floor). Below
  that it prints its count and nothing else, and the stability line names the window it could not use —
  and **no objective may be named strongest unless the branch's full set of four windows each clears
  20** (§2.2, §8; DECISIONS item 14).
- **≥ 3 valid picks per night, each with ≥ 5 valid matched controls** (§2.5), inside the
  contributing-night rule itself.
- A row or window below its floor is **demoted to a printed count, never dropped and never
  reduced-to-fit** (DP-43's demote-not-drop). **No floor is ever lowered to reach a date.**
- **DP-24** (≥ 30 contributing nights after the lock commit) is satisfied by construction — every
  contributing night here is post-lock — but is **not invoked**: PROSPECTIVELY_CONFIRMED is declined in
  every branch (§1, §8).

**Every rate below is measured. The placeholders the draft was sized on were replaced at `record` by
`STEWARD_Q034_exposure.md` (R1, 2026-09-14, counts only), and not one date moved in** (DECISIONS
Correction 8, item 18): both measured rates are *faster* than the placeholders they replace, and a
faster rate never pulls a date in (DP-43, DP-45).

| quantity | value used to size | status |
|---|---:|---|
| **the scheduling rate** — `min(r_rank,60 , 0.6620)` (DECISIONS item 8) | **0.6620** | **measured, and the cap is the binding half.** `r_rank,60` = the **ranking-set** rate (§2.5) with numerator and denominator over the same t+60-gradeable sub-period = **10/11 = 0.9091** (`STEWARD_Q034_exposure.md` §(b)); 0.6620 = 47/71, the desk's measured published-pick contributing rate (`STEWARD_Q031_exposure.md` §(a), reconfirmed bit-for-bit by `STEWARD_Q032_exposure.md` §(a)(ii)). **No date is ever computed from a rate faster than the desk's own measured published-pick number**, and a rate slower than 0.6620 would govern. Every real loss mechanism stays in the denominator (exclusions, DP-04, null / non-monotone ladder, split-scale payload, wrong-side stop, `d_L3` bound, < 5 valid controls, < 60 prior bars, > 25% ungradeable); **only** freeze-horizon censoring is removed, and only because it cannot occur inside the registered window (R2 delivers t+60 bars for every in-window night). **Footnote:** the measured sub-period (2026-06-01..06-15) sits **before** the 2026-07-06 ladder fix, where the §2.4 screen still fires at 25.71% against **0.00%** inside the registered window, so `r_rank,60` is a **lower bound** for the window actually registered — and the cap governs regardless. |
| contributing nights per elapsed session (published slate, §2.5's rule) | **0.6620** (47/71) | **measured**, `STEWARD_Q031_exposure.md` §(a), on the identical funnel, pick nights 2026-06-01..2026-09-10 against `exclusions_v003`. The measured rate, not Q032's borrowed 0.9538 (DP-45). Maturity there was t+20; the *rate per elapsed session* is unchanged by the t+60 maturity for the **contributing-night** rule — **this is not asserted of the ranking-set rate**, which is measured directly above (Correction 4). On the measured sub-period the two sets **coincide** under the corrected §2.4 screen (the same 10 nights of 11). |
| control-pool depth (≥ 5 valid controls per pick) | min 37, median 54, max 60 | **measured**, `STEWARD_Q031_exposure.md` §(b) — the ≥ 5 floor's measured cost is **zero nights** |
| valid published picks per night (≥ 3 floor) | min 4 on contributing nights, median 8 | **measured**, `STEWARD_Q031_exposure.md` §(d) |
| **the rarer registered window**, on the **lower** of the two partitions (DECISIONS item 9) | **0.1972** contributing nights per elapsed session | **measured**, `STEWARD_Q034_exposure.md` §(c): platform-label **NOTSTRONG 14/71** on Q034's own funnel. The bar-only partition's rarer arm, **HOSTILE 0.3099**/session, is cited from `STEWARD_Q032_exposure.md` §(b) under the registered SMA50-only lower bound rather than re-run. The **lower** of the two governs, because the branch is not fixed until R2(i) is attempted (DP-45). The draft's **0.20 HOSTILE-share planning placeholder is struck.** |
| picks with an unusable printed swing stop (O4 only) | **19.0%** (103/542 valid rows; 18.7% of all 550) | **measured**, `STEWARD_Q034_exposure.md` §(d) on 2026-06-01..2026-09-10, re-measuring Q009 §1's in-sample 17.8% (66/371) — the same signature, the same order |
| picks carrying a complete six-level ladder across all three lanes (O5, O8) | **97.1%** (534/550); nights with < 3 such picks **1 of 68** | **measured**, `STEWARD_Q034_exposure.md` §(e); the one night is 2026-06-02, the `analysis_status = "disabled"` night, which the fourth exclusion criterion removes whole |

**Floor projections at 158 elapsed sessions**, on those measured rates:

| floor | rate used | session first reached | projected at 158 |
|---|---|---:|---:|
| ≥ 80 contributing nights on the **ranking set** | **0.6620**/session (the scheduling rate, measured) | **121** (= 2027-03-09) | **104.6 nights** |
| ≥ 20 contributing nights in the rarer registered window | **0.1972**/session (measured, the lower partition) | **102** (= 2027-02-09) | **31.2 nights** |
| ≥ 20 contributing nights in each calendar half | 0.6620/session | 31 per half | **52.3 per half** |
| ≥ 30 contributing nights after the lock commit (DP-24, satisfied not invoked) | 0.6620/session | 46 | **104.6** |

**Floor A — the ranking set's 80 nights — is the binding floor, at session 121, inside the registered
158.** The draft's "the rarer tape window binds and projects marginal (20.9 against 20)" was the
placeholder's artefact: the arm is measured at **31.2** and is **not** marginal. **Projected
contributing nights at session 158, every registered window, none below 20:** ranking set **104.6**;
Half A **52.3**; Half B **52.3**; platform-label STRONG **109.0**, NOTSTRONG **31.2**; and, if R2(i)
delivers, bar-only BENIGN ≈ **109**, HOSTILE ≈ **49**. Item 14's demotion clause is therefore **not
engaged at projection** and stays in force on `eval.py`'s **own measured counts** at the decision pass:
a window that never reaches 20 nights removes itself from the stability test and is named (§2.2), and
**no objective may be named strongest on a partial four-window set** (§8). A floor reached sooner never
shortens a registered window (DP-45).

### 5.2 Window, decision date, extension, DEFERRED fallback (DP-43, DP-13; no outcome is looked at)

**Window: pick nights 2026-09-15 .. 2027-04-30 inclusive = 158 elapsed sessions**, after exclusions —
the identical window Q027, Q031 and Q033 register (and Q032 registered before it was DEFERRED on
2026-09-14), so one successor build serves all of them.
**Binding maturity 60 sessions**, which is what makes this question's calendar longer than its siblings':
its deepest objective is the long lane's own window and H-084 names it (DP-25 — the Registrar does not
re-unit a hypothesis to reach a date sooner).

- **The trading calendar** (DECISIONS item 6, Correction 1 — the desk's standard holiday list, of which
  the draft omitted one entry): **2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15,
  2027-03-26, 2027-05-31, 2027-06-18** (Juneteenth observed; 2027-06-19 is a Saturday)**, 2027-07-05**
  and **2027-09-06** (the last for the ceiling back-solve only). It does not touch the 158-session
  window count — 2027-06-18 falls after 2027-04-30 — but it moves every +60-session arithmetic that
  crosses June 2027. Every date is re-confirmed session by session from the calendar when the freeze is
  built; **a correction may move a date out, never in.**
- **Window arithmetic:** 2026-09-15 is session 1; 12 at 2026-09-30; 34 at 2026-10-30; 54
  at 2026-11-30; 76 at 2026-12-31; 95 at 2027-01-29; 114 at 2027-02-26; 136 at 2027-03-31; **158 at
  2027-04-30** (Friday).
- **Halves.** Half A = sessions 1–79 = 2026-09-15..2027-01-06; Half B = sessions 80–158 =
  2027-01-07..2027-04-30.
- **Decision date.** 2027-04-30 **+ 60 sessions** maturity = **2027-07-28** (20 sessions to 2027-05-28;
  41 to 2027-06-30 — June carries 22 weekdays less Juneteenth observed 2027-06-18; July carries 22
  weekdays less July 4 observed 2027-07-05, so sessions 42–60 fall in July and **session 60 =
  2027-07-28**, Wednesday); **+ one calendar week** freeze margin = 2027-08-04; first Monday
  on or after = **Monday 2027-08-09**, not a holiday. That is **10.9 months from the 2026-09-14 lock**,
  inside DP-43's 12-month ceiling (which binds the **initial** decision date — DECISIONS item 4).
  `eval.py` is written once (rule 9) and run **once**, then. **No interim looks.**
- **`eval.py` is committed no later than Monday 2027-04-05, with its sha256 recorded, and is not
  touched afterwards** (DECISIONS item 16; rule 9). This question needs the deadline more than any
  other on the desk: its nine rows **are** the endpoints of questions that decide *before* it — Q006
  (2026-10-05), Q002 (2026-10-12), Q027 and Q029 (2027-04-12, on this very window and freeze), Q012
  (2027-03-22), Q033 and Q018 (2027-07-12) — and a script written after any of those passes is a script
  written with part of its own answer in view. 2027-04-05 is the Monday before the earliest sibling
  pass on this window. The extension run uses the **byte-identical, unmodified** file.
- **Extension (DP-13; DP-43's +30 sessions).** If any gate — 80 contributing nights on the ranking set,
  20 in each of the four registered windows, or Gate 0 — is short at 2027-08-09 on `eval.py`'s **own
  measured counts**, the window extends **once**, automatically and with no new question, to pick nights
  **2026-09-15 .. 2027-06-14** (session 188), decided **Monday 2027-09-20** (2027-06-14 + 60 sessions:
  11 sessions to 2027-06-30, 32 to 2027-07-30, 54 to 2027-08-31, then 2027-09-01/02/03 = 55/56/57,
  Labor Day 2027-09-06 skipped, 2027-09-07/08/09 = 58/59/**60** → **2027-09-09**, Thursday; + one week =
  2027-09-16; first Monday on or after = **2027-09-20**). The extended run uses the
  **byte-identical, unmodified `eval.py`** and the same gates. **The halves are re-cut on the extended
  window** by the same session-index rule (Half A = sessions 1–94 = ..2027-01-28, Half B = 95–188),
  fixed by that rule at this lock. **The extended decision is 12.2 months from the lock and is
  permitted**: DP-43's ceiling is written as *"if the **initial** decision date lands more than 12
  months after lock"*, and DP-13's single automatic extension is a Confirmed entry fired on measured
  counts, which a Default does not overrule (DECISIONS item 4). It is never a second look — `eval.py`
  is byte-identical and the gates are unchanged.
- **A window short of 20 contributing nights fires this single extension** (DECISIONS item 14,
  Correction 5 — resolving the draft's contradiction between §2.2 and §5.2 in the strict direction:
  more waiting, never a relaxed test). **After** that single extension, a still-short window prints its
  count, leaves the stability test and is **named**, and the register **runs** — a window shortfall is
  **not** a DEFERRED ground — but **no objective may then be named strongest**, and the register's
  ceiling in that branch is **NO_SEPARATION (INCONCLUSIVE)** with the missing window named (§8).
- **DEFERRED fallback (the hard stop, Monday 2027-09-20).** If the **ranking set's 80-night floor** or
  **Gate 0** is still short after the single extension, Q034 goes
  to `research/questions/DEFERRED.md` with the measured counts rather than running under-powered, with
  the re-check trigger *"the Steward measures ≥ 0.44 ranking-set nights and ≥ 0.11 rarer-window
  contributing nights per elapsed session over a trailing quarter"*, and it is **not** re-registered on
  a thinner objective list — dropping an objective would be re-uniting H-084's own list (DP-25). **No
  second extension, no reduced floor**, and a gate shortfall is **never** an INCONCLUSIVE register (§8).
  The Gate 0 fix-and-re-run loop's own hard stop is the same **Monday 2027-09-20**.
- **Fixed at lock, not reopened at the run:** the nine objectives and their definitions; Plan H; the
  common scale; the §2.2 windows and every cut in them; the suppression list; the separation rule and
  its 0.50 argmax floor; the `SET_SENSITIVE` threshold of 0.05; the block length; the seeds; the
  half-split rule.
- **If a scoring or publication change ships mid-window** (DECISIONS item 12; §5.3 R2, §10 threat 8) —
  a change to the SAS weights, the timeframe multipliers, `qualification_threshold`, the ATR-elite
  caps, the GEX offset, a scoring enable-flag, `publication_floor`, `bear_publish_threshold`,
  `max_output_cap`, `min_completeness`, **`BAND_EXITS`** or the lane-plan writer, **including any
  promotion of v1.7** — the window is cut at
  the ship date, the **post-ship** segment becomes the question's window with this schedule recomputed
  from it — **out, never in**, subject to the same single extension and the same ceiling measured from
  the original lock — the pre-ship segment becomes a labelled descriptive panel entering no register
  line, and if neither segment reaches the floors inside the ceiling the question is **DEFERRED**
  (DP-06, DP-50(a)). `eval.py` prints the per-night `config_json` composition and **fails loudly**
  rather than silently excluding. **`BAND_EXITS` is named explicitly because O5's Plan H is defined by
  it**, which no sibling question's list needed. Running the other way (DP-50(b)): every listed change
  is **flag-off until 2027-08-09** (2027-09-20 if the extension fires), checked before any fix brief is
  written (§9.6). **A change to `services/market_regime/scorer.py` splits the platform-label stability
  partition at the ship date** (§2.2's v1.2 guard) and leaves the bar-only arms untouched.

### 5.3 Routed requests

- **R1 → data-steward — counts only, no outcome of any kind, BLOCKING FOR LOCK — ANSWERED 2026-09-14,
  GATE CLOSED: PASS ON BOTH LIMBS.** `research/reports/STEWARD_Q034_exposure.md` delivers every limb on
  the pinned freezes and the read-only repo, no live query. **Limb (b), the ranking-set rate: 10/11 =
  0.9091** on the t+60-evaluable sub-period → scheduling rate `min(0.9091, 0.6620) =` **0.6620** (item
  8's cap binds) against the **≥ 0.44** floor — **PASS**. **Limb (c), the rarer registered window on the
  lower of the two partitions: platform-label NOTSTRONG 14/71 = 0.1972** (bar-only HOSTILE 0.3099,
  cited) against the **≥ 0.11** floor — **PASS**. Both measured rates are *faster* than §5.1's
  placeholders, so **no date moves in** (DP-45): the registered window end **2027-04-30** and the
  decision date **Monday 2027-08-09** stand exactly as drafted. Also measured: wrong-side swing stop
  **103/550 = 18.7%** and the `d_L3` bound **7/550** (§(d)); complete six-level ladder **534/550 =
  97.1%**, nights with < 3 complete-ladder picks **1/68** (§(e)); the **DP-50 sweep returns NONE** —
  HEAD unchanged at `d19c9a9`, `BAND_EXITS` last touched `b24954c` (2026-07-09), an **ancestor** of the
  pin, v1.7 unscheduled (§(f)), to be re-swept at R2(vii) and **not assumed clear permanently**; and
  the credentials re-check (§(g)) returns **absent**, which is **not a gate here** (DECISIONS item 17)
  and makes `STABILITY_WITHOUT_TAPE_ARMS` the expected branch. **Had the §2.4 screen been read strictly
  (DECISIONS item 21), limb (b) would have measured 0.0909, the 80-night floor would have projected to
  ≈ session 880 — beyond any extension — and the answer would have been DEFERRED**; that is recorded
  here so the ruling's consequence is visible beside the ruling. The request as issued follows, for the
  record. Measured on
  `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`, plus read-only `git log` /
  `git show` in the platform repo — never a live query (DP-50(c)). Over pick nights
  **2026-06-01..2026-09-10**:
  **(a)** the §2.4 funnel and the §2.5 contributing-night rate at a **60-session maturity**, reported
  three ways: (i) numerator and denominator both over the **maximal sub-period whose nights grade to
  t+60** on `manifest_prices_v001` (with that sub-period's last pick night derived from the calendar),
  (ii) the same rule at t+20 for comparability with 0.6620, and (iii) the full-denominator t+60 rate
  for the record;
  **(b)** **the ranking-set rate — the limb that decides** (§2.5, DECISIONS item 7): the same nights,
  further restricted to those on which **each of the nine objectives independently carries ≥ 3 valid
  picks, each with ≥ 5 valid controls**, after that objective's own screen — O4 after the
  wrong-side-swing-stop screen, O5 and O8 after the complete-six-level-ladder requirement, the rest
  after the shared screens — with the per-objective night counts side by side, the binding objective
  named, and the rate in the same three forms as (a). **The schedule is built on `min` of (b)(i) and
  0.6620** (item 8), so a rate faster than 0.6620 changes no date;
  **(c)** **the rarer-window limb, on both candidate partitions** (item 9), because the branch is not
  fixed until the decision pass: for the **platform-label** partition, the nights per arm on Q034's own
  contributing nights under §2.2's legality test, which arm is rarer, its contributing nights per
  elapsed session, and the count of nights failing the legality test; and for the **bar-only tape**
  partition, `STEWARD_Q032_exposure.md` §(b)/(c) **cited rather than re-run** (the SMA50-only bound —
  adding `SMA50 > SMA200` can only move nights out of `UP` and into HOSTILE, so the SMA50-only HOSTILE
  count is a **lower bound** and the BENIGN count an **upper bound**), noting only whether Q034's
  stricter funnel changes the arm counts materially;
  **(d)** the count and share of published picks whose printed **swing stop** is on the wrong side of
  `C_t` (Q009's 17.8% signature), and the count excluded by the `d_L3 ∈ [0.25, 10]` bound — the two
  screens that make O4's and the ladder objectives' denominators differ;
  **(e)** the count and share of published picks with a complete six-level ladder across all three lanes,
  which is O5's and O8's denominator, and the share of nights on which fewer than 3 picks carry one;
  **(f)** the **DP-50(a)/(b) commit sweep** since manifest SHA `fa70688` — any change to the SAS weights,
  timeframe multipliers, `qualification_threshold`, `publication_floor`, `bear_publish_threshold`,
  `max_output_cap`, `min_completeness`, the ATR-elite caps, the GEX offset, the scoring enable-flags,
  **`BAND_EXITS` (`scripts/generate_sas_trading_guide.py:89-95`, which defines O5's Plan H)** or the
  lane-plan writer — **with an explicit answer even when it is "none"**, and whether
  the **v1.7** scoring workstream is scheduled to ship inside the window;
  **(g)** a one-line credential re-check for the record only (`ALPACA_API_KEY` / `ALPACA_SECRET_KEY`
  present in the session). **This limb is not a gate for Q034 and defers nothing** (DECISIONS item 17):
  the probe itself is cited from `STEWARD_Q032_exposure.md` §(g), Q034's tape arms are stability
  *windows* rather than an arm contrast, and both branches are pre-registered — the answer only records
  which branch is expected.
  **The lock-or-DEFER gate.** DP-43's 12-month ceiling solved at this lock date: the latest admissible
  initial decision is Monday 2027-09-13, which back-solves through a one-week margin and **60 sessions**
  of maturity (last t+60 on or before 2027-09-06 → **2027-09-03**, Labor Day 2027-09-06 skipped → window
  end **2027-06-08**) to **184 admissible elapsed sessions** (DECISIONS Correction 2; the draft's 186
  omitted Juneteenth). The inequalities are the floors divided by 184,
  rounded **up**: **ranking-set** nights **≥ 0.44** per elapsed session; rarer registered-window
  contributing nights **≥ 0.11** per elapsed session, applied to the **lower** of the two partitions —
  both re-solved from the trading calendar at `record`. Both clear → **Q034 locks**, with §5.2's dates
  moved **out** if the measured rates are slower and
  unchanged if they are faster. Either limb short → **Q034 goes to DEFERRED** with the measured counts
  and the re-check trigger *"the Steward measures ≥ 0.44 ranking-set nights and ≥ 0.11 rarer-window
  contributing nights per elapsed
  session over a trailing quarter"*. **The 60-session maturity is not shortened to make the gate pass**
  — dropping the long-lane objective would be re-uniting H-084's own list (DP-25) and buying a date with
  the test (DP-43, DP-45).
- **R2 → data-steward (due before the decision date; not a blocker for lock; DP-23) — ROUTED and OPEN
  at this lock; its dates are final, not provisional.** The successor freeze
  pair named in the header — **Q033's R2 build with the daily tail extended to session t+60 of the last
  included pick night**:
  **(i)** **SPY split-adjusted daily bars from 2025-01-02** through the freeze end — without them §2.2's
  `SMA200` and the 250-session terciles do not exist and **no tape window can be assigned**. If the
  extended SPY history cannot be obtained (the Q030 / H-074 provisioning blocker: `ALPACA_API_KEY` /
  `ALPACA_SECRET_KEY` absent from the desk session, reported unresolved by
  `STEWARD_Q032_exposure.md` §(g) on 2026-09-14), the **`STABILITY_WITHOUT_TAPE_ARMS` branch of §2.2
  fires** — the tape arms print `UNAVAILABLE` and the stability test runs on the two calendar halves
  and the **two platform-label arms**, four windows, registered here before the fact — and the
  partition is **never** re-specified to an SMA50-only variant after the
  data exists;
  **(ii)** daily bars for **every candidate symbol on every in-window night, published and
  unpublished**, with ≥ 60 prior sessions before 2026-09-15 and through **t+60 of the last pick night =
  2027-07-28** on the corrected calendar (DECISIONS Correction 1 — the draft's 2027-07-27 was one
  session early), delivered before the **2027-08-09** decision date; on the extension path, through
  **2027-09-09** for a **2027-09-20** decision;
  never assumed from v001's symbol list;
  **(iii)** hourly bars scoped to at least the published-pick symbols — **not purely descriptive**:
  §4.0's same-session ordering of O3's band race and O4's target-versus-stop race reads them, and a
  pair they cannot order is scored against the pick (DP-27), so their coverage is stated explicitly;
  **(iv)** `market_regime_daily` included **with `created_at` and `regime_version` preserved** — under
  DECISIONS item 3 the platform label is a **registered stability window** (§2.2), not only a
  cross-check, and `eval.py` fails loudly on a `regime_version` other than v1.2 for an in-window night;
  **(v)** an **add-only successor exclusions file** applying the identical four criteria to post-lock
  nights; it may add nights and may never remove one, and its header states whether the
  `analysis_status = "disabled"` / no-`lane_plans` signature is still present rather than silently
  returning an empty list;
  **(vi)** rows whose bars are missing are **excluded and counted, never back-filled or imputed**;
  **(vii)** R1(f)'s commit sweep **repeated for the period between the freezes — `BAND_EXITS`
  included, because it defines O5's Plan H** — with a dated
  `DATA_NOTES.md` entry for any repair that rewrites historical rows, and an explicit answer even when it
  is "none"; R1(f) returned NONE at this lock and that is **not assumed to hold permanently**.
  **DP-50(a) guard:** where the successor freeze overlaps an earlier one — including Q033's,
  which shares this window — the rows are compared and `eval.py` **fails loudly** on any disagreement,
  SPY's own daily bars included. Every §5.2 date is re-confirmed **session by session from the trading
  calendar** when the freeze is built, on §5.2's corrected holiday list (2027-06-18, Juneteenth
  observed, is included — 2027-06-19 is a Saturday); a correction may move a date **out, never in**.

## 6. Test window, split and stratification

- **Test window: prospective only — pick nights 2026-09-15 .. 2027-04-30** (158 elapsed sessions;
  .. 2027-06-14 if the single DP-13 extension fires).
  *Justification, and it is stronger here than in any sibling question.* The sealed period is where
  **seven locked questions are still in flight on these very objectives** — Q006 (the L3-touch level,
  decides 2026-10-05), Q002 (speed, 2026-10-12), Q004 (entry basis), Q011, Q012 (2027-03-22), Q015,
  Q018 (2027-07-12), Q009 / Q010 (the stop race) — and this register computes their endpoints on their
  populations. Running it on sealed nights would be an interim look at those questions' data under
  another name (rule 3, rule 9). The sealed period is contaminated for this question on a second ground
  as well: EXPLORE_001 already read in-sample path, speed and level outcomes, and those reads are what
  put "the edge is in speed and deep levels" on the backlog — the exact ranking H-084 asks for.
- **Nothing is computed on sealed nights at all** (DECISIONS item 2): no panel, no companion, no funnel
  count, no `D`, no `E`, no raw rate. This is a deliberate divergence from the sibling questions that
  print a labelled sealed panel, and the ground is specific: Q034's nine rows **are** the registered
  primary endpoints of questions whose decision dates are still ahead (O3 → Q033, O4 → Q009 / Q010,
  O5 → Q012, O8's L3 row → Q006, O9 → Q002, plus Q004, Q011, Q015, Q018), computed on *their*
  populations, on *their* sealed nights, from *their* freeze — a "labelled panel" of those numbers is an
  interim look at locked questions' data under another name, and no label on this file can undo it for
  them (rule 3, rule 9). The sealed numbers for
  these objectives belong to the locked questions that own them and will appear in their reports; the
  Reporter cross-references those **ledgered verdicts** (the H-077 pattern) rather than this register
  pre-empting them.
- The window sits entirely after the 2026-06-01 catalyst fix (DP-06), after the 2026-07-06
  `_enforce_ladder_monotonic` ship (commit `5fa3db4`, an ancestor of the pinned `fa70688`) and after the
  2026-07-08 `publication_floor` change (DATA_NOTES), so
  none of the three splits DP-06 / DP-50(a) would force falls inside it. **That is also why §2.4's
  ladder screen is expected to fire at 0.00% here** — DATA_NOTES measures the platform's own non-strict
  invariant at 25.71% (36/140) before the ship and 0.00% (0/355) on and after — and why a material
  firing rate inside this window is a loud platform-defect flag rather than a silent drop.
- **Stratification (rule 7):** the two calendar halves plus **two arms in every branch** — the bar-only
  tape arms of §2.2 where R2(i) delivers the SPY history, and the **platform's point-in-time regime
  arms, which are a registered stability window in every branch** (DECISIONS item 3) as well as a
  composition cross-check. "Stable" is defined over the halves **and** the arms, four windows (§2.2, §8).
- **Knowledge time (rule 14) — every input declared. Q034 needs no rule-14 exception and requests none**
  (DP-05 untouched, DP-41 respected).

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `overall_score`, `dominant_direction`, `best_timeframe` | `sas_candidates` | pick night, 16:05 ET | population, strata, direction |
  | lane plans `L1…L6`, the printed stops, `analysis_status` | `sas_candidates.public_payload_json` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | levels, stop, `d_L3`, exclusions |
  | SPY split-adjusted daily closes, sessions ≤ t | `prices_daily_split` | pick-night close, 16:00 ET | **the tape window** (SMA50, SMA200, 20-session realised vol, expanding terciles) |
  | `C_t`, ATR14, beta60, atr_pct, runup20 | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | distances, matching, the common scale |
  | control-candidate pool (non-published rows for night t) | `sas_candidates` | pick night, 16:05 ET | B1 |
  | `market_regime`, `regime_version`, `created_at`, `data_quality` | `market_regime_daily`, v1.2 | declared 16:05 ET / lag 0, legal from 2026-06-09 (FREEZE_v001 §7) — legal for **every** night of this window | **the platform-label stability windows** (§2.2, a registered window in every branch) **and** the composition cross-check; never an arm contrast, never a q |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion |
  | session t+1 open `X`; daily bars t+1..t+60; hourly bars | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **entry and outcome measurement only** |

  **What `eval.py` must enforce:** the eligible-pick set, the window labels, the control sets, every
  level, band and stop and every stratum label are computed and written to a frozen per-pick and
  per-night table **before any post-pick-night bar other than the t+1 open is loaded**, and the t+1 open
  is used **only** to place `X` and the constructs anchored on it — never to filter, classify, match or
  stratify. The run fails if any t+1-or-later field is referenced in eligibility, window assignment,
  matching or stratification.

## 7. Multiple testing

**No correction, because nothing here is a hypothesis test with a verdict.** The register reports raw p
per objective (B3) and **no q-value**: there is no primary endpoint, no MPE and no confirmable effect,
so a BH correction would attach to nothing. Q034 is filed in **F8** and, per that family's header in
`research/BACKLOG.md`, **enters no correction set** — F8's correction runs across the members that carry
primaries. **At this lock that membership is Q033's 1, or 2 only if Q033's SPY limb clears**
(DECISIONS item 15, Correction 6): `STEWARD_Q032_exposure.md` (2026-09-14) defers **Q032** outright and
Q033's own decisions defer its **P2** on the same absent Alpaca credentials, and H-074 / Q030 is
DEFERRED — each deferred primary leaves the set while deferred. H-083 joins when it locks; Q026, Q028
and Q034 are diagnostics. **Nothing in Q034's own numbers moves with that count**: a diagnostic that
computes no q is unaffected by the size of a set it does not join, and Q034 changes no other
family's denominator.

**The guards against the forking path are structural, and they are the substance of this question:**

1. **The list of nine closes at draft** (§4.1) and **every row prints in every window, whatever its
   sign** — H-084's own rule.
2. **The sub-cell suppression list is fixed at lock** (§4.3) and does not reopen at the run.
3. **The separation rule** (§8) requires the winner to beat the runner-up's interval on **both** CIs and
   to be the argmax in **at least half** of the joint resamples; a winner that cannot do that is
   reported as `NO_SEPARATION` with the tied leading set named in full.
4. **The 9 × 9 correlation matrix and `N_eff` are printed beside any winner**, so "strongest of nine"
   is never quoted without how many independent things nine objectives actually are.
5. **The register confirms nothing.** A named winner routes a **new** PREREG (§9); it is not, and may
   not be reported as, evidence for any locked question's endpoint.

**Overlaps, stated so that nothing is double-counted as independent evidence.** O3 is Q033's P1; O4 is
Q009's / Q010's race; O5 is Q012's Plan H; O8's L3 row is Q006's E1 on the DP-09 clock; O9 is Q002's S3.
Each of those questions owns its endpoint, carries its own MPE and correction and decides on its own
date. **No row of this register may be read as confirming, strengthening or weakening any of them**, and
none of their verdicts changes any line here. Where a row and a locked verdict disagree, the register
prints both and says the locked question decides — the two are computed on different nights.

## 8. Decision rule (numeric, written before unsealing)

`D_o` is the common-scale excess of §4.2; `E_o` its native-unit companion. Both CIs are §4.5's, and
"both CIs" below means the stated condition holds on **each** of them (DP-51).

**Gate 0 first.** If §4.6's positive control and construction checks do not all pass, the register is
**INCONCLUSIVE** and nothing else in it is interpreted. At most **two** fix-and-re-run passes, each
recorded with its diff and date, each under the same seed, all inside the hard stop **Monday
2027-09-20**. **No Gate 0 target is relaxed to make a pass succeed.**

**Floors first, and a floor shortfall is never a register verdict.** If the ranking set is below 80
contributing nights, the single DP-13 extension fires and then DEFERRED (§5.2) — not INCONCLUSIVE.

An objective `o` is **STABLE** iff:

1. its row carries **≥ 80 contributing nights** on the ranking set;
2. **both CIs of `D_o` exclude 0**;
3. `D_o` carries the **same sign in every window** of §2.2 that clears 20 contributing nights — the two
   calendar halves and the two arms of the partition the branch registers — and no
   such window carries the opposite sign with a CI excluding 0;
4. its **bull-only** version is not of the opposite sign with a CI excluding 0; and
5. it is **not** flagged `SET_SENSITIVE` (§2.5).

**SEPARATED ⇒ HISTORICALLY_CONFIRMED** (labels `DIAGNOSTIC — no primary, no MPE, no BH` and
`NON_QUOTABLE`) — exactly one objective `o*` is named strongest, and only if **all** of:

- **the branch's full set of four windows — the two calendar halves and the two arms of whichever
  partition that branch registers — each clears 20 contributing nights** (DECISIONS item 14). Short of
  that, no objective may be named strongest on any ground and the register's ceiling is
  **NO_SEPARATION (INCONCLUSIVE)** with the missing window named in the verdict sentence: a verdict
  bought with a window shortfall is not a verdict, and the NULL branch stays reachable because H14's
  FAIL is a real finding;
- `o*` is **STABLE**;
- **`D_{o*}`'s lower bound exceeds every other objective's `D` upper bound, on both CIs** — the
  interval-separation condition, applied to the runner-up and therefore to all eight;
- **`o*`'s argmax share ≥ 0.50** in the joint night bootstrap **and** in the episode bootstrap (B4) —
  a winner that is not the largest in at least half the resamples is not a winner;
- the register prints, in the same sentence, **`N_eff` and the 9 × 9 correlation panel**, names
  every objective whose CI overlaps `o*`'s (there must be none, by the interval-separation condition),
  and **names the disagreement if `o*`'s `D` rank and `E` rank differ** (§4.2, §10 threat 2).

**NO_SEPARATION ⇒ INCONCLUSIVE** — at least one objective is **STABLE**, but no objective satisfies the
separation conditions. The register names the **tied leading set** (every STABLE objective whose `D` CI
overlaps the largest `D`'s CI on either CI construction), prints all nine rows, and states in one
sentence that the question's answer is *"several, indistinguishably"*.

**NO_STABLE_OBJECTIVE ⇒ NULL** — no objective is **STABLE**. This is **H14's FAIL reading** and it is a
real finding, ledgered with the same care as a positive: on this window, against same-night look-alikes
matched on beta, volatility and run-up, **none of the nine ways the desk knows how to measure a pick
shows an advantage that survives its own windows**. What it licenses is in §9, and it is less than it
sounds.

**Clauses that bind in every branch:**

- **DP-51 is a gate.** A condition met on CI-1 and not on CI-2 is **not met**. A winner separated on
  CI-1 and not on CI-2 is `NO_SEPARATION`, never SEPARATED.
- **No MPE exists** (DP-10 / DP-20 / DP-44 inapplicable, §4). The thresholds — 80 nights, 20 nights,
  0.50 argmax, 0.05 `SET_SENSITIVE`, |SMD| ≤ 0.25 — serve the MPE's role and are fixed here, before the
  run. **None is lowered at the run in any branch.**
- **A fixed-horizon winner changes nothing about how the desk measures.** If `o*` is **O1 or O2**, the
  register reports it plainly and it **routes** (§9); **no plan, guide line, lane rule, brief, flag or
  quoted number may be written on a fixed-horizon close-to-close return** (rule 5, DP-01), and rule 5's
  objective is not amended by this or any other branch.
- **`STABILITY_WITHOUT_TAPE_ARMS` and `ARM_IS_ONE_STRETCH`** (§2.2, §2.5) travel with every label they
  qualify, wherever it is restated. The first replaces the draft's `STABILITY_ON_HALVES_ONLY`
  everywhere (DECISIONS item 3, Correction 3): the branch it names runs **four** windows, not two, and
  the old name would misdescribe what ran.
- **The 0.50 argmax floor, the 0.05 `SET_SENSITIVE` threshold and the 10-session block length are fixed
  at this lock and none is lowered at the run in any branch** (DECISIONS item 5).
- **PROSPECTIVELY_CONFIRMED is not requested in any branch** (§1). The verdict's fixed labels are
  `DIAGNOSTIC — no primary, no MPE, no BH` and `NON_QUOTABLE`, used verbatim in `research/LEDGER.md`,
  in the register, in any synthesis and anywhere else the verdict is quoted.
- **What a SEPARATED register does *not* mean, stated in the verdict sentence itself.** It does not mean
  the named objective is tradeable, that its excess clears any cost, or that the platform predicts it
  *well* — only that, among the nine, it is the one whose measured advantage is largest and
  sign-stable on this window. The size question belongs to the question §9 routes.

## 9. If SEPARATED (and if NO_SEPARATION, and if NO_STABLE_OBJECTIVE), what changes

**Opening, and it is the whole of the consequence section: no guide line, no lane rule, no playbook
entry, no product change, no marketing claim and no quotable number follows from any branch of this
question.** It carries no primary, no MPE and no correction, and every number in it is `NON_QUOTABLE`
(rule 12). Rule 5's objective is not moved by it (H-084's own text, §4).

**What it does change, all internal:**

1. **SEPARATED routes exactly one new PREREG.** The named objective `o*` becomes the primary endpoint of
   a **new registered question** — its own MPE in `o*`'s units (DP-10 / DP-20 / DP-44 as applicable), its
   own family and BH set, its own prospective window after that lock, and this register's definitions
   inherited verbatim. **That question, and only that question, can confirm anything about `o*`.** If
   `o*` is already the primary of a locked question (O3 → Q033, O4 → Q009 / Q010, O5 → Q012, O8's L3 row
   → Q006, O9 → Q002), the routing note says so and **no new question is registered** — the answer is
   that the desk is already measuring the right thing, which is the most likely useful outcome of this
   whole exercise.
2. **It is an input to the Reporter's H-077 synthesis** (`SYNTHESIS_selection_vs_execution.md`), which
   assembles selection value and execution value **from ledgered verdicts only**. This register is cited
   there as the objective-comparison panel, labelled, never as a verdict about either.
3. **An `INTERNAL_TOOL` `EN` is filed** proposing that the desk's weekly check print the nine-objective
   table on the trailing quarter, so that a drift in *which* objective carries the signal is visible
   without a study. Flag-off, Haci-only, never subscriber-facing (DP-48, rule 11).
4. **NO_STABLE_OBJECTIVE does not retract a claim by itself.** H14's FAIL sentence — "Product A should
   not be marketed as a predictive system" — is a claim about the *level* of the selection edge, and the
   questions that own that level are **Q006** and **Q024** (F1). This register is reported **beside**
   their ledgered verdicts, never instead of them; if they are NULL and this register is
   NO_STABLE_OBJECTIVE, the Reporter says so in one paragraph and the marketing consequence follows from
   **their** verdicts under rule 10.
5. **A `SET_SENSITIVE` or floor-short row is a measurement finding**, routed to the Steward as a
   coverage note (which objective the freeze cannot support and why), and to `PLATFORM_ISSUES.md` where
   the cause is a platform defect — a missing lane, an unusable printed stop, a non-monotone ladder —
   with the measured counts attached (DP-07, DP-48). **DP-49 binds every brief that follows:** each
   check handed to the coding agent must be satisfiable from the platform repo alone.
6. **Q034 is in flight from this lock until its decision date, and DP-50(b) applies to the platform in
   the meantime.** Any change to the SAS weights, timeframe multipliers, `qualification_threshold`, the
   ATR-elite caps, the GEX offset, the scoring enable-flags, `publication_floor`,
   `bear_publish_threshold`, `max_output_cap`, `min_completeness`, `BAND_EXITS` or the lane-plan writer —
   **including any promotion of the v1.7 score** — is **flag-off until 2027-08-09** (2027-09-20 if the
   extension fires), the same clause Q027, Q029, Q031, Q032 and Q033 carry, checked before any fix brief
   is written. If a listed change ships anyway it takes a dated `DATA_NOTES.md` entry naming the column,
   the date range and the ship SHA, and §5.2's window split applies (DP-06, DP-50(a)).
- Owner: implementer for any `EN` that follows. Shadow period before any flip: ≥ 20 trading days
  (nothing in this question reaches a flip on its own).

## 10. Known threats to validity (registrar's own list)

1. **Nine objectives on one dataset is a garden of forking paths, and no q-value is computed.** This is
   the central threat and it is answered structurally, not statistically: the list closes at draft, every
   row prints, the winner must separate on both CIs and hold the argmax in half the resamples, the tied
   leading set is named when it cannot, and **nothing is confirmed by this question at all** — the only
   output that travels is a routing decision to a question that carries a real MPE and a real correction.
2. **The common scale flatters near-degenerate objectives.** A standardized effect divides by a pooled
   within-night sd, which is small for a rate near 0 or 1 (O9 at 5 sessions may be one such). The native
   `E` prints beside every `D`, the raw pick and control rates print beside both (B5), and a winner whose
   `D` and `E` ranks disagree is named in the register's own sentence. It is not excluded — the rank is
   `D`'s by registration — but it cannot be quoted without the disagreement.
3. **The nine objectives are not nine independent things.** O4, O8's L3 row and O9 all contain "did L3
   get touched"; O7 contains most of O2 and O3. A winner among correlated measures is far less
   surprising than a winner among independent ones. The 9 × 9 matrix and `N_eff` are printed and named
   beside any winner (§4.3, §8), and this is the reason the argmax share exists.
4. **The control removes the tape only to the extent of a three-feature match.** Every objective inherits
   that limit. Post-match SMDs per feature are a Gate 0 condition (≤ 0.25) and the raw rates print beside
   the adjusted ones.
5. **The population is nearly the whole traded book.** `publication_floor = 80.0` since 2026-07-07 and
   90+ is thin, so "the published slate" is in practice the 80–90 band. Every sentence in the register
   must say *"the published slate"*, never *"high-scoring picks"*, and the 90+ cell is SUPPRESSED.
6. **The 60-session maturity costs calendar and exposes the register to survivorship.** A 60-session tail
   catches more halts, delistings and corporate actions than the desk's 20-session questions. Missing
   bars are an exclusion, counted, never a non-touch; the exclusion counts print per objective; and the
   calendar cost is paid in the decision date rather than by shortening H-084's own list (DP-25, DP-45).
7. **The rarer window was sized on a placeholder, and the placeholder is gone** (DECISIONS Correction 8).
   The draft projected it marginal at 20.9 nights against 20 on a 0.20 HOSTILE-share planning figure
   that was never evidence about this partition. R1 measured Q034's own funnel before the lock: the
   rarer registered window runs at **0.1972** contributing nights per elapsed session (platform-label
   NOTSTRONG, the lower of the two partitions; bar-only HOSTILE 0.3099), projecting **31.2** nights at
   session 158 — **not marginal**, and floor A (the ranking set's 80 nights, session 121) binds
   instead. The threat is not retired, only answered by measurement: if a window nevertheless fails to
   reach 20 at the decision pass it removes itself from the stability test, is **named**, and **cannot
   silently weaken a label** — because no objective may be named strongest on a partial four-window set
   (§8, DECISIONS item 14).
8. **Config drift inside the window.** A change to the weights, the publication gates, `BAND_EXITS` or
   the lane-plan writer changes what "a published pick", "its printed L3" and "the committed plan" mean.
   Every item is named in R1(f) and repeated in R2(vii); `eval.py` prints the per-night `config_json`
   composition and **fails loudly — it does not silently exclude** — if an in-window night's scoring
   fields differ from those in force at lock.
9. **Band membership depends on a stored score that has been rewritten before.** `eval.py` re-derives
   each pick's band from `score_details_json` where the layer subscores are present and **fails loudly**
   on a disagreement with `overall_score` beyond 0.05.
10. **Overlapping forward windows inflate precision**, across nights and across the same symbol
    re-selected on consecutive nights — worse here than anywhere on the desk, because the windows are 60
    sessions long. CI-1 handles the first, CI-2 (DP-51) the second, and **both must hold** for every
    condition in §8.
11. **One database (DP-50).** A platform repair between freezes can rewrite the rows this question reads.
    The R2 cross-freeze comparison fails loudly on disagreement, including on SPY's own daily bars and on
    the rows Q033's freeze shares with this one.
12. **The SPY history the tape windows need does not exist in any manifest pinned today, and on today's
    evidence it is the branch most likely to run.** `STEWARD_Q032_exposure.md` §(g) (2026-09-14) reports
    the Alpaca credentials absent and the probe unattempted. R2(i) is the
    fix; its failure fires the pre-registered **`STABILITY_WITHOUT_TAPE_ARMS`** branch rather than a
    re-specified partition — and that branch still runs **four** windows, because the platform-label
    arms are a registered stability window in every branch (§2.2, DECISIONS item 3). The draft's
    fallback, which would have dropped to the two calendar halves, is **refused**: removing windows can
    only make STABLE easier to reach, and a data failure may never buy a CONFIRMED-side verdict
    (DP-45). This is a provisioning problem (the Q030 / H-074 blocker), not a measurement one.
13. **Ladder, stop and payload defects.** Null-ladder, **non-monotone in the platform's own non-strict
    sense** (§2.4 — ties across lanes are not a defect and are graded on both levels), wrong-side-stop
    and split-scale
    payloads (DATA_NOTES, Q009 §1) are excluded and counted, per objective; O4's and O8's denominators
    are therefore smaller than the others' and the `SET_SENSITIVE` flag is what keeps that from moving a
    ranking quietly. Measured on the exposure period: wrong-side swing stop **18.7%**, complete
    six-level ladder **97.1%**, `d_L3` bound **7/550** (`STEWARD_Q034_exposure.md` §(d), §(e)). The
    monotonicity screen's own firing rate prints per window and per objective and **fails loudly above
    25.71%**, against a post-ship measured 0.00%.
14. **A diagnostic can be read as a verdict by a later reader.** The fixed labels of §8, carried into the
    ledger and into any synthesis, are the defence; §9's opening sentence is the second.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-14; `decide` and `record` passes — 21 items, 8 corrections, all
applied above). Routed items still open: **R2, the successor selection and price freezes** (§5.3 R2,
DP-23) — due before the decision date, not a blocker for lock. R1 is answered and its lock gate is
CLOSED: **PASS on both limbs**.
