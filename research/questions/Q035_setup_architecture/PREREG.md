# Q035 — setup_architecture: would a setup-specific ranker pick a better eight than the universal 0–100 score?

**Status:** PREREG_DRAFT (lock by committing this file)
**Family:** **F8 System validity** (hypothesis **H-083**, Haci's Master Hypothesis Program **H13**,
*A/B/C architecture*), as filed in BACKLOG.md. DP-29 agrees: the primary endpoint's subject is the
*selection architecture* — which eight of the night's publishable set get the slots — not the level
of the path edge (F1), not calibration (F2), not exits (F6).
**Manifest (the fitted arm's training window, the R1 exposure counts, and nothing else):**
research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA
fa70688bc252d14f8d67e371afafc194731c324e).
**Manifest (prices, the fitted arm's training window only):** research/data/manifest_prices_v001.json
(as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374).
**Successor freezes — the question itself (built and pinned at the decision date, DP-23; §5.3 R3):**
a selection freeze (`sas_candidates` **every row, published and unpublished**, `sas_runs`,
`market_regime_daily`) and a price freeze (**daily** split-adjusted and raw bars for **every candidate
symbol on every in-window night**), covering pick nights **2026-09-15 .. 2027-03-31** with daily bars
through **2027-04-28** (session t+20 of the last included pick night) and ≥ 60 prior sessions before
2026-09-15; a second pair **only if** the single DP-13 extension fires, covering pick nights
**.. 2027-05-13** with bars through **2027-06-11**. No hourly bars are needed (§4.1 reads one level
per row on a daily clock), so this scope is a strict **subset** of the successor freeze Q027, Q031
and Q033 already require, and no additional fetch is created by this lock. **No SPY history beyond
the candidate set is required** — §6 takes its regime strata from `market_regime_daily`, not from a
bar-derived tape partition, so the Alpaca-credentials blocker that deferred Q030 and Q032 does not
reach this question.
**Every night that carries a verdict here is after this lock and exists in no manifest pinned today**
(`pin_at_decision`, DP-23). The successor manifests are named in prose and deliberately not written
as `**Manifest …:**` header lines, because no such file exists yet and the pin step reads every
`**Manifest` line as a path.
**Exclusions:** research/data/exclusions_v003.json (DP-22, the newest file) unioned with the
**add-only successor exclusions file** issued with the successor selection freeze — the identical
four criteria Q027 fixes at its lock (`manual_runs` ∪ `non_session_runs` ∪
`uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10.
The successor file may only **add** nights; no night is removed from a v003 list; the **criteria** are
fixed at this lock even though the **dates** cannot be. Both paths are `eval.py` inputs; no hard-coded
file name, no hard-coded date. DP-04 applies mechanically on top.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14

---

## 1. Hypothesis (plain English)

**If the platform sorted each night's publishable candidates by the signal that is actually driving
each one — flow, projection/technical continuation, or catalyst — instead of by one universal 0–100
score, the eight names it published would reach a target two ATR away more often than the eight the
universal score picks.**

### 1.1 What this question stands on, and what it does not wait for

Two sequencing facts, stated here because H-083's BACKLOG line makes them conditions of registration.

- **H-080 is DEFERRED (2026-09-14, `research/questions/DEFERRED.md`), so no verdict on whether 90 is
  a real boundary is coming, and this question does not wait for one.** H-083's line routes H-080's
  FAIL branch here; that branch will not fire, because H-080 was not registered. Q035 therefore
  **stands on the published v1.6 slate exactly as the platform produces it** — which is the baseline
  H-083 names anyway (§3 B1). Nothing here tests, defends or attacks the 90 line, the 80 publication
  floor or the 8-slot cap: all three are treated as **fixed platform configuration**, identical in
  both arms of every contrast, and a change to any of them inside the window **splits the window at
  that date** (§2.7). A confirmed result here says the *ordering* inside the publishable set can be
  improved; it says nothing about where the set's boundary should sit.
- **Q028 (H-076, structure of the seven layers) decides 2026-09-28, and this question does not wait
  for it either.** H-083's line says Q028's output "feeds H-083's setup definitions"; the setup
  definitions in §2.3 are instead **fixed here, from the code at `fa70688`, and made falsifiable
  inside this question** by Gate 0 limb (e) and R1 limb (e) — the same two degeneracy checks Q028
  would supply (are ≥ 4 layers carrying within-night variation; is the dominant-layer argmax better
  than a coin flip), measured on this question's own frozen population **before** the lock. Q028's
  verdict is read at the decision pass as **corroboration only** and is **never** a ground to
  re-specify the partition, drop a setup or re-label a verdict (§7). If Q028 returns REDUNDANT, the
  honest reading of a NULL here is strengthened, not changed.

### 1.2 The substitution this draft makes, recorded rather than applied silently

H-083's primary is "the within-night control-adjusted L3-touch rate (Q006 `E_t`) of the setup-ranked
top 8 minus the universal-score top 8". **The printed L3 does not exist for the setup arm.** A ladder
is written only for rows the platform publishes (`lane_plans`; the Steward's Q032 funnel counts
`no-lane_plans` as a screen reason for published rows, and unpublished rows have none at all), so a
name the setup ranker promotes has no printed target. Using each arm's own printed levels would make
the target construct **arm-dependent**, which is exactly the confound rule 5's distance match exists
to remove — and PI-009 / H-053 record that the printed ladder is not ATR-scaled in the first place
(`ai_agents/principal_agent.py:530-575`).

The registered target is therefore a **uniform level at 2.0 × the row's own ATR14**, identical in
construction for every row in both arms (§4.1). This is the *stricter* form of H-083's endpoint:
being the same distance in each name's own volatility units on both sides, it cannot smuggle target
*placement* into a claim about *name selection*. The 1.0 ATR and 3.0 ATR versions are pre-declared
descriptive sub-rows that decide nothing in any branch (§4.3).

---

## 2. Population

### 2.1 Source tables (successor freezes; the training window uses the v001 pair)

`sas_candidates` (**every row**, published and unpublished), `sas_runs`, `market_regime_daily`, and
the daily split-adjusted and raw price bars of every candidate symbol.

**No platform outcome column is read anywhere in this question** — not `sas_selection_excursion`, not
`outcome_*`, not `uoa_symbol_daily.fwd_return_*`, not `directional_pct`. Every touch, every ATR and
every close is computed by `eval.py` from the pinned price bars (PI-003: own ATR14 from the bars,
never `atr_pct`; own `C_t` from the bars, never `spot_close`).

### 2.2 The night's publishable set `P_t` — exact filters

This question is about *which eight of a set* get the slots, so the set has to be the one the platform
itself is choosing from. `services/super_agent_select_scoring.py:1509-1548` (`_qualify_lane`, read at
`fa70688`) makes that set explicit: a row is ranked by `overall_score`, dropped if it fails the
threshold (`max(timeframe_threshold, publication_floor)`, :1518), dropped if it fails
`min_completeness` (:1520), and otherwise **selected until the cap is reached — after which the
remaining rows are marked `qualified = False, selected_rank = NULL,
qualification_reason = 'capped_by_max_output'` (:1533-1537)**.

`P_t` = the rows on night `t` that passed every substantive gate and were separated only by the cap:

```sql
SELECT * FROM sas_candidates c
WHERE  c.trading_date = :t
  AND  c.dominant_direction = 'bullish'                       -- §2.4: bull lane only
  AND  c.qualification_reason IN ('selected', 'capped_by_max_output')
  AND  c.trading_date NOT IN (SELECT night FROM exclusions)   -- exclusions_v003 ∪ successor, DP-04
```

- `'selected'` = the published bull slate (identically `qualified IS TRUE AND selected_rank IS NOT
  NULL`, DP-28's predicate — in this code path the two are the same event, :1541-1543).
- `'capped_by_max_output'` = above the publication floor, above the completeness floor, cut **only**
  by the 8-slot cap.
- **Excluded, and counted per night:** `'selected_dark'` (the `publishable=False` lane, :1503-1508 —
  DP-28's actual target, out of every arm), `below_threshold_*`, `below_completeness_*`,
  `graded_subthreshold_v2*`, and every bear-lane row.

**This is a deliberate deviation from the literal text of DP-28** (`qualified IS TRUE AND
selected_rank IS NOT NULL`), and it is §11 item 1. DP-28's stated purpose is to keep **dark-lane** rows
out of every arm, and they are out. But a question about which eight of the publishable set deserve
the slots cannot be run on the eight the platform already chose: under the literal predicate `P_t` *is*
the published slate, both arms are identical by construction, and the hypothesis is untestable. The
deviation is recorded here so the Red Team reviews it with the reason in view.

### 2.3 Setup assignment — deterministic, from 16:05 columns only

Within each night's `P_t`, each of the seven layer subscores — `flow_strength_score`,
`technical_structure_score`, `projection_score`, `catalyst_event_score`, `gex_alignment_score`,
`fundamental_quality_score`, `smart_money_confirmation_score` (`score_details_json` /
`sas_candidates` columns; weights v1.6 = 29/27/24/10/5/5/0) — is standardised **within that night's
`P_t`** to a z-score. The row's **dominant layer** is the argmax of those z-scores.

- A layer whose within-night variance is **zero** (every row equal, the PI-008 forced-zero
  smart-money signature and the `enable_fundamental_enrichment = False` signature) is **excluded from
  the argmax on that night**, and the per-layer count of such nights is printed always.
- Ties in the argmax (exact float equality) break by the v1.6 weight order
  projection > technical > flow > catalyst > fundamental > smart-money > GEX, then by the layer name
  alphabetically. Deterministic, fixed at lock.

Setups, as H-083 names them:

| setup | dominant layer | H-083's name |
|---|---|---|
| **A** | `flow_strength_score` | flow-led |
| **B** | `projection_score` **or** `technical_structure_score` | projection-led continuation |
| **C** | `catalyst_event_score` | catalyst / earnings-driven |
| **O** | `gex_alignment_score`, `fundamental_quality_score` or `smart_money_confirmation_score` | *residual — not a setup* |

`B` carries two layers because "continuation" is the projection/technical pair that the v1.6 weights
put at 29 and 27 and that reads the same price action; splitting them would create a fourth setup
H-083 does not name (DP-25). **`O` is never a setup cell**: it carries no stratum, no calibration row
and no verdict, its rows are ranked by the universal rule (§4.1, `w_O ≡ 0`), and its share of `P_t` is
printed on every table. This is the conservative direction — every row the partition cannot explain is
handed back to the baseline.

**Knowledge time (rule 14).** Every column above is a 16:05 ET write on the pick night, declared in
`freeze_config.availability` and re-confirmed by FREEZE_v001 §7. **No rule-14 exception is requested
or needed (DP-41).** The setup label, the slate and the entry basis are all fixed at 16:05 on night
`t`; every price bar used for an outcome is dated `t+1` or later.

**DP-06 is satisfied by construction, not waived:** setup C reads the catalyst layer, which is a
different feature before and after the 2026-06-01 earnings fix `69ef05f`. The fitted arm's training
window starts **2026-06-01** and the test window starts **2026-09-15**; no row on either side of the
question predates the fix.

### 2.4 Bull lane only — stated, with the reason

The bull lane (cap 8) and the bear lane (cap 5, `bear_publish_threshold`) are scored, thresholded and
capped **separately** (`super_agent_select_models.py:92-97`; `_qualify_lane` is called once per lane).
A re-ranking that mixed them would change the published direction mix, and direction mix is a known
live confound (H-062, bear picks in strong tapes). Q035 re-ranks **inside the bull lane only**: the
bear slate is untouched and byte-identical in both arms, and nothing in this question speaks to bear
picks. `dominant_direction = 'mixed'` rows cannot enter a lane and are excluded and counted (the Q033
§2.4 convention). §11 item 4.

### 2.5 Row-level screens, applied identically to both arms

A row is dropped from `P_t` — and therefore from **both** slates and from the pool mean — if any of:

1. fewer than **60 prior split-adjusted daily sessions** in the price freeze (the standing Q006 §3 B1
   screen; needed for a stable ATR14);
2. **no bar exists at session t+1** (no entry price), or the forward series ends before session t+20
   without the level having been touched — the CTRA truncated-history signature
   (`STEWARD_Q032_exposure.md` §(e)): **ungradeable, not "no touch"**;
3. `ATR14_t` ≤ 0, or a null/non-finite `C_t`, `overall_score` or any of the seven layer subscores;
4. a split-scale payload disagreement between the raw and split-adjusted series at `t` (the Q032
   funnel's `split-scale-screen`).

Every drop is counted per night per reason and printed. A night is **not** dropped because a row was:
the arms are rebuilt from the screened `P_t`, so both are always drawn from the identical set.

### 2.6 Contributing night

A night `t` contributes to a primary iff, after §2.2's filters, §2.5's screens and the exclusions:

- `sas_runs` has a corroborated run for `t` that is not excluded (DP-04, exclusions file), **and**
- `|P_t| ≥ 1` and at least one row of `P_t` is gradeable at 2.0 ATR on the 20-session clock.

**A night on which the two slates come out identical still contributes, with `Δ_t = 0`** (§4.1). It is
real evidence that the architecture changed nothing that night, and excluding those nights would let
a ranker that reorders three nights in ten be reported as though it reordered ten (§11 item 6).

### 2.7 Mid-window split rule — narrower than most, and stated in full

The window splits at the date of any change to: `qualification_threshold`, `publication_floor`,
`max_output_cap`, `min_completeness`, `bear_publish_threshold` / `bear_max_output_cap` (they change
which rows reach the bull lane's cap), `scoring_weights`, `timeframe_weight_multipliers`,
`timeframe_thresholds`, `conflict_penalties`, any layer's scoring function, or
`enable_fundamental_enrichment` / any layer enable-flag. Detected two ways at the decision pass, both
required: the DP-50(a)/(b) commit sweep of the platform repo since `fa70688`, and a per-run
`sas_runs.config_json` hash series. A split means the two segments are reported separately and
neither is pooled; a segment below 20 contributing nights is SUPPRESSED (counts only).
**A change to the candidate universe builder does not split this window** — the universe is upstream of
`P_t`, and both arms draw from whatever it produced.

---

## 3. Baselines — what this must beat

- **B1 — the published v1.6 slate (H-083's own named baseline; the paired primary contrast).** The
  top 8 of the screened `P_t` by `overall_score` under the platform's exact tie-break
  `sorted(key=(-overall_score, symbol))` (`:1509`). Reconstructed rather than taken from
  `selected_rank`, so both arms are built from the identical screened set; the reconstruction's
  agreement with the platform's actual published slate is a Gate 0 limb and an R1 limb (§5.3 (f), §8
  Gate 0.3).
- **B2 — a random 8 from the same night's `P_t`.** 2,000 uniform within-night draws, seed
  `20260914`. Monte Carlo: **adds no n** (rule 6). **Blocking in one direction only:** if the setup
  slate beats B1 but does **not** beat B2 with a CI lower bound above 0, the verdict is labelled
  **`UNIVERSAL_BELOW_RANDOM`** and is **not** reported as evidence for setup-specific ranking — it is
  evidence that the universal score is ordering the publishable set worse than chance, which is
  Q027's subject and is routed there (§7). B2 carries no MPE and can confirm nothing on its own.
- **B3 — the setup-label-shuffled ranker.** The identical ranking rule and the identical `w`, with
  the setup labels permuted **within night** across the rows of `P_t` preserving the night's label
  count vector, 2,000 draws, seed `20260914`. This is the null that says *"blending a layer subscore
  into the ranking helps, but it has nothing to do with the setup"* — the single most likely benign
  explanation of a positive result, and the one H-083's architecture claim has to survive.
  **Blocking in one direction only**, and it supplies the second permutation p (§4.4).
- **B4 — the pool level `R_pool,t`,** the touch rate of the whole screened `P_t` at the same level.
  Printed beside every row as the night's difficulty anchor. **Descriptive; decides nothing.**

Rule 5's distance-matched control is not an add-on here: it is the construction. Every row in both
slates and in all four baselines is asked to travel **2.0 of its own ATRs**, on the same clock, from
the same entry.

---

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

### 4.1 The two slates, the level, the entry, and `Δ_t`

**Entry basis: the session t+1 official 09:30 ET open** (DP-03(b), DP-42). The setup arm promotes
names that were never published, so they have no publication event and no after-hours print; t+1 open
is the only basis that exists on both sides, and rule 5 requires one basis for both.

**Level:** `H_i = C_t,i + 2.0 × ATR14_t,i`, from the row's own pinned split-adjusted close and its own
ATR14 computed from the pinned bars. **Touch** = the session high reaches `H_i` on any session in
`t+1 .. t+20` (DP-09's 20-session clock, DP-42's swing default). **A gap through at the t+1 open is
not a hit** (DP-26): if `open_{t+1,i} ≥ H_i` the row is coded **not a hit** and counted in a printed
`GAPPED_THROUGH` tally. A row whose forward series ends before t+20 without a touch is ungradeable and
was already dropped by §2.5(2).

**The universal slate** `U_t` = B1's top 8 of the screened `P_t` (fewer than 8 if `|P_t| < 8`).

**The setup slate** `S_t` = the top 8 of the screened `P_t` by the setup score

```
S_i = (1 − w_{s(i)}) · overall_score_i  +  w_{s(i)} · L_{s(i),i}
```

where `s(i) ∈ {A, B, C, O}` is §2.3's setup, `L_{s,i}` is the raw 0–100 subscore of that setup's own
layer (for B, whichever of projection/technical was the argmax), and **`w_O ≡ 0` by definition**.
Both `overall_score` and every `L` are on 0–100, so `S_i` is comparable across setups and no slot
allocation rule is needed. Ties break by `overall_score`, then by the platform's own `symbol`
ascending — deterministic, fixed at lock.

**The night's statistic, for each primary:**

```
R_X,t = (# rows of slate X touching H within 20 sessions) / |X_t|
Δ_t   = R_S,t − R_U,t          in percentage points
```

`Δ_t` is exactly H-083's control-adjusted difference with the common term written out: since both
arms are drawn from the same screened `P_t` and carry the identical 2.0-ATR construct, the
distance-matched control term is the same pool on both sides and cancels,
`Δ_t = (R_S,t − R_pool,t) − (R_U,t − R_pool,t)`. **Both excess terms are printed beside `Δ_t`
always**, so the contrast is never read without its level.

**The unit of inference is the night** (rule 6): `Δ_t` is formed per night first, and the endpoint is
`mean_t(Δ_t)` over contributing nights, equally weighted.

### 4.2 The two primaries (`m = 2`, fixed at lock), both two-sided

- **P1 — the fitted ranker** (H-083's form as filed: "fitted once, frozen in the PREREG, tested only
  on prospective nights"). `w_A, w_B, w_C` are chosen **once**, after this file's lock commit, by the
  exhaustive grid in §4.5, and never refit. Endpoint `mean_t(Δ_t)` with those `w`.
  **MPE ±5.0 pp (DP-20, DP-44).**
- **P2 — the pure ranker**, `w_A = w_B = w_C = 1`: within each setup, rank by that setup's own layer;
  `O` rows keep the universal rule. **No fitting, no training data, no artefact, no free parameter —
  fixed in this file at draft.** Endpoint `mean_t(Δ_t)` with `w ≡ 1`. **MPE ±5.0 pp (DP-20, DP-44).**

P2 is registered alongside P1 because it is the form of H13 that cannot be argued with: it is the
A/B/C architecture in its strongest and simplest statement, it always differs from the universal
slate where the layers differ, and it is immune to every criticism of a model fitted on fifty nights.
P1 nests the baseline exactly at `w = 0` and nests P2 exactly at `w = 1`. **Both run on the identical
contributing nights, the identical `P_t`, and the identical screens, and are resampled together night
by night**, so the P1−P2 difference carries their positive correlation rather than an inflated width.

**What ±5.0 pp means here, so the bar is read concretely:** an 8-name slate moves in steps of 12.5 pp,
so 5.0 pp is the setup ranker converting about **one extra name every two and a half contributing
nights**. That granularity is a §10 threat, not a reason to move the MPE. **No MPE is lowered at the
decision pass in any branch.**

### 4.3 Secondaries and descriptive rows — the list closes at lock

Reported always, in every branch, whatever the sign; **none decides any verdict**, none carries an
MPE, and none may be quoted as a confirmation:

1. `R_S,t`, `R_U,t`, `R_pool,t` and both excesses, pooled and per calendar half.
2. The **same three endpoints at 1.0 ATR and 3.0 ATR** on the same 20-session clock. Pre-declared so
   the level cannot be chosen afterwards; 2.0 ATR decides alone.
3. **Reorder rate**: the share of contributing nights on which `S_t ≠ U_t`, the mean number of names
   swapped, and the distribution of `|P_t|`.
4. **Per-setup slot share**: how many of the 8 slots each of A / B / C / O takes in each arm; the O
   share of `P_t`; the per-layer zero-variance night counts from §2.3.
5. **Calibration within setup** (H-083's named secondary): the touch rate of the *published* slate by
   conviction tier (Pro 80–89, Elite 90+) within each setup — does "Pro"/"Elite" mean the same thing in
   a flow-led name as in a catalyst name. SUPPRESSED below 20 contributing nights in a cell.
6. **ATR per trade** (H-083's named secondary): enter at the t+1 open, exit at the first touch of
   `H_i` or at the session-20 close, **no stop** (DP-02 — adverse excursion is measured, never used as
   an exit), realised move in ATR units, per slate, with the **0.25 ATR** reference line printed
   (DP-10). Descriptive because it is not a registered primary; it does not become one at the decision
   pass.
7. **Counter-direction**: the touch rate of `C_t − 2.0 × ATR14` within 20 sessions per slate, and the
   mean adverse excursion in ATR (rule 5: reported, never an exit).
8. The **`GAPPED_THROUGH`** tally, the §2.5 drop counts by reason, and the `mixed`/dark/bear row
   counts.
9. **Fixed-horizon**: the t+20 close-to-close return per slate. Descriptive only, never decides
   (rule 5, DP-01).

### 4.4 Inference

- **CI-1 (registered):** date-clustered (night-level) bootstrap, 2,000 resamples, seed `20260914`.
- **CI-2 (DP-51, a gate — not a footnote):** **episode-clustered**, where an episode is one symbol's
  run of appearances in **either** slate with gaps of ≤ 10 sessions between successive appearances,
  and the bootstrap resamples **episodes and nights jointly**, 2,000 resamples, same seed. **A primary
  that clears MPE on CI-1 and not on CI-2 is INCONCLUSIVE, never CONFIRMED.** It bites here: the same
  symbol can sit in both slates on many consecutive nights with overlapping forward bars.
- **Permutation p₁ (primary):** night-level sign-flip of `Δ_t`, 2,000 draws, seed `20260914`.
- **Permutation p₂ (B3):** the setup-label shuffle of §3 B3, 2,000 draws, same seed.
- **The larger of p₁ and p₂ is the p that enters the BH correction** (§7). Strictly stricter; fixed
  at lock.
- Seed, draw counts and library versions are printed in the results header.

### 4.5 The fitted arm's protocol, complete and closed at draft (P1 only)

**When.** `fit.py` runs **after this file's lock commit and never before** (rule 3). It is the
Researcher's, written once and run once (rule 9); no agent tunes it and no agent's reading of its
output can change this file.

**Training window.** Pick nights **2026-06-01 .. 2026-08-12** on `manifest_v001` /
`manifest_prices_v001` — the maximal stretch that is (a) after DP-06's catalyst fix, so setup C is one
feature throughout, and (b) matured to t+20 on the pinned price freeze. Roughly **50 pick nights**.
**Disjoint from the test window in every respect**: no night, no row and no bar is shared.

**Objective.** `mean_t(Δ_t(w))` over training nights, with §2.2's filters, §2.3's labels, §2.5's
screens and §4.1's level and clock applied exactly as in the test — the identical code path.

**Grid.** `w_A, w_B, w_C ∈ {0, 0.25, 0.50, 0.75, 1.00}`, all 125 combinations, exhaustive and
deterministic (no seed needed). Ties on the objective break to the smallest `w_A + w_B + w_C` (nearest
the baseline), then lexicographically smallest `(w_A, w_B, w_C)`.

**Shrinkage guard, registered here rather than discovered later.** If the best combination's training
objective does **not** exceed the `w = 0` baseline by at least **+5.0 pp** (the same MPE the test
uses), the fit returns `w_A = w_B = w_C = 0`. Fifty nights and 125 combinations is a real overfitting
surface; a deviation the training data cannot support by the MPE is noise and is not carried into a
seven-month test.

**Artefact.** The selected triple is written to `research/questions/Q035_setup_architecture/
setup_model_v001.json`, its sha256 recorded in `DECISIONS.md` and in the results header, and it is
**never refit**. `eval.py` fails loudly on any other hash. The full 125-cell grid surface is written
to `results/fit_grid.json` and is sealed with the rest of `results/` (rule 3); its `w ≡ 1` cell is a
**training-window** value on nights disjoint from the test, so it is not and cannot be P2's answer.

**Early stop (`FIT_RETURNS_UNIVERSAL`).** If the fit returns `w_A = w_B = w_C = 0`, then `S_t ≡ U_t`,
`Δ_t ≡ 0` by construction, and **P1 closes immediately with verdict NULL**, labelled
`FIT_RETURNS_UNIVERSAL` and `HISTORICAL_ONLY` (DP-31 — it is decided from training data, is not
prospective, and licenses nothing: no guide line, no lane rule, no product change, no quotable
number) and `NON_QUOTABLE`. P1 then **leaves the F8 correction set** (the H-074 precedent) and `m`
drops to 1. **P2 is unaffected and the window runs in full.**

**If the artefact cannot be produced at all** (the Researcher's run fails, or the training window
comes up short of 20 contributing nights): **P1 is demoted to descriptive at lock** and P2 carries the
question alone at `m = 1`. This is a pre-registered fallback, not a deferral, and it is why P2 exists.

---

## 5. Sample floors and expected n

### 5.1 Floors (rule 6 as read by DP-21) — no floor is reduced in any branch

| floor | requirement | basis |
|---|---|---|
| **A** | ≥ **80 contributing nights** per primary | DP-21 (80 per primary endpoint, the strict reading) |
| **B** | ≥ **20 contributing nights** in **each** of setups A, B, C, where a setup contributes on a night on which the setup slate places ≥ 1 of its names | rule 6 (20 per cell); the rarest setup binds |
| **C** | ≥ **20 contributing nights** in **each calendar half** (§6) | rule 6; sign stability needs both halves populated |
| **D** | ≥ **30 contributing nights dated after the lock commit** | DP-24; satisfied by construction — every night in the window is post-lock |

Any cell below 20 that is *reported* is **SUPPRESSED** (counts only); the suppression list is fixed at
lock (§4.3) and never removes §8's blocking clauses, whatever a cell's count.

### 5.2 Expected n — measured, not borrowed, and the slower figure is the one used

From `research/reports/STEWARD_Q031_exposure.md` §(a) and independently reconfirmed in
`research/reports/STEWARD_Q032_exposure.md` §(a)(ii), on the identical published-pick funnel and the
identical exclusions: **47 contributing nights / 71 elapsed sessions = 0.6620 per elapsed session**
(t+20-comparable form; 68 non-excluded nights of 71; only 2026-06-02 carries zero valid picks). The
faster t+40-evaluable sub-period rate (0.8710) is **not** used — DP-45 takes the slower measured rate.

| quantity | figure | source |
|---|---:|---|
| Window 2026-09-15 .. 2027-03-31 | **≈ 136 elapsed sessions** (`eval.py` counts the exact figure from the pinned calendar) | derived |
| Projected contributing nights (floor A: 80) | **≈ 90** | 0.6620 × 136 |
| Cushion over floor A | **≈ 10 nights** | derived |
| Per calendar half (floor C: 20) | **≈ 45** | derived |
| Post-lock nights (floor D: 30) | **≈ 90 — all of them** | window is entirely post-lock |
| Rarest-setup rate needed for floor B | **≥ 0.15 / elapsed session**, i.e. ≥ 22.2% of contributing nights placing a name of that setup | 20 / 136 |
| Control-pool depth (unpublished same-night candidates, ≥ 60 prior bars) | min 37, median 53, max 60 | `STEWARD_Q032_exposure.md` §(e) |
| Publishable-set depth `|P_t|` | **UNMEASURED — R1 limb (c)** | — |
| Rarest-setup rate | **UNMEASURED — R1 limb (b)** | — |

**Floor B is the one that can fail, and it is unmeasured today.** Rows scoring ≥ 80 run at ≈ 14.6 per
night across both lanes against ≈ 8.1 published (`STEWARD_Q027_exposure.md` §(d): 702 rows ≥ 80 on 48
nights; `STEWARD_Q032_exposure.md` §(a): 550 published rows on 68 nights), which says the reorder room
is real but says nothing about how it splits three ways. That is why R1 is **BLOCKING FOR LOCK** and
why its shortfall branch is DEFERRED, not a reduced floor.

### 5.3 Routed requests

**R1 → data-steward — counts only, BLOCKING FOR LOCK.** On `manifest_v001` +
`manifest_prices_v001` against `exclusions_v003`, pick nights 2026-06-01 .. 2026-09-10. **No outcome
of any kind:** no touch, no first-touch date, no return, no excursion, no `outcome_*`, no
`sas_selection_excursion`, no `fwd_return_*`, no setup-versus-outcome cross-tab. Forward bars are read
only to establish that a bar exists (§2.5(2)) and to compute ATR14 and `C_t` for the screens. Frozen
data and the read-only platform repo only — **never a live query (DP-50(c))**.

| limb | measurement | gate |
|---|---|---|
| (a) | contributing-night rate on §2.6's funnel, per elapsed session | ≥ **0.59** |
| (b) | per-setup rate: share of contributing nights on which the **pure** ranker (`w ≡ 1`, needs no fit and no outcome) places ≥ 1 name of each of A, B, C — report all three | rarest ≥ **0.15** / session |
| (c) | reorder room: distribution of `|P_t|` | median ≥ **11** and `|P_t| ≥ 9` on ≥ **80%** of contributing nights |
| (d) | reorder rate: share of contributing nights where the pure-ranker slate differs from the reconstructed universal slate; mean names swapped | ≥ **0.50** |
| (e) | partition viability: share of `P_t` rows whose top within-night layer z-score exceeds the runner-up by ≥ 0.25 sd; number of layers with non-zero within-night variance, per night | margin share ≥ **0.60** and ≥ **4** varying layers on ≥ **80%** of nights |
| (f) | reconstruction correctness: agreement between the §3 B1 reconstructed slate and the platform's actual published bull slate, on nights where no row was dropped by §2.5 | ≥ **0.90** |
| (g) | DP-50(a)/(b) sweep since `fa70688` over `services/super_agent_select_scoring.py`, `services/super_agent_select_models.py` and the per-run `config_json` hash series, for any §2.7 quantity | **no change**, or the change dated and named |

**Any limb short ⇒ Q035 goes to `research/questions/DEFERRED.md` at lock with the measured number
named.** The partition is never re-specified on a weaker definition to clear a gate, no floor is
reduced, and no limb is dropped (the Q030 / Q032 precedent).

**R2 → researcher (post-lock; not a lock blocker).** Write `fit.py` and `eval.py` once (rule 9), run
`fit.py` on the training window after the lock commit, produce and hash `setup_model_v001.json`, and
report whether the `FIT_RETURNS_UNIVERSAL` branch fired. §4.5's fallback covers failure.

**R3 → data-steward (due at the decision date, DP-23; not a lock blocker).** The successor selection
and **daily-only** price freezes named in the header, plus the add-only successor exclusions file.

### 5.4 Window, decision date, extension, DEFERRED fallback (DP-43, DP-13)

**The window is prospective-only.** The sealed period is not a panel here for two independent reasons:
the 2026-06-01..08-12 stretch **is P1's training set** and printing it would be a training-set result
dressed as a finding, and P2's value on those same rows is a free look at the answer on the very rows
the fit consumes. **No sealed-period panel is computed for either primary.**

| | |
|---|---|
| Pick nights | **2026-09-15 .. 2027-03-31** (≈ 136 elapsed sessions) |
| Maturity | session t+20 of the last pick night ≈ 2027-04-28, plus a one-week freeze margin |
| **Decision date** | **Monday 2027-05-10** (≈ 7.9 months from lock) |
| Single automatic DP-13 extension, if any floor A–D gate is short **on the counts `eval.py` prints** | pick nights **.. 2027-05-13** (+30 sessions), decided **Monday 2027-06-21** (hard stop, ≈ 9.2 months) |
| Still short after the one extension | **DEFERRED** — never a second extension, never a reduced gate |

Both dates sit inside DP-43's 12-month ceiling. The extension fires on measured counts, never on a
projection or a run-rate. **A shorter window is not chosen to reach a date sooner.**

---

## 6. Split and stratification

- **Training (P1 only, no verdict):** pick nights 2026-06-01 .. 2026-08-12, sealed, §4.5.
- **Test (out-of-sample; decides everything):** pick nights 2026-09-15 .. 2027-03-31, entirely after
  this lock.
- **Calendar halves** (the binding stability check, rule 7): the window's contributing nights split at
  its **63rd elapsed session** (≈ 2026-12-14; `eval.py` derives the exact date from the pinned session
  calendar). Extension nights, if the extension fires, join the second half. Each half must clear 20
  contributing nights (floor C).
- **Regime strata (rule 7, descriptive):** `market_regime_daily` regime on night `t`, restricted to
  nights whose label is knowledge-time-legal by the Q023 / Q032 §(d) test — a v1.2 row dated `t`, not
  `unknown`, not `insufficient`, `created_at` on `t` and `created_at ≤` that night's
  `sas_runs.finished_at`. The window begins 2026-09-15, well after the 2026-06-09 point-in-time
  boundary, so the CLAUDE.md backfill caveat does not reach it. Nights failing the legality test are
  reported in a `REGIME_UNLABELLED` stratum, never dropped from a primary.
  **No primary is defined per regime**, so a DP-50(a) repair to the regime column can move a
  descriptive stability row and can never move a verdict. This is why Q032 / Q033's bar-only SPY
  partition is deliberately **not** used: it would import the Alpaca-credentials blocker (§ header)
  for a stratification that decides nothing.
- **A result counts only if the sign of the primary agrees in both calendar halves** (§8 clause 6).

---

## 7. Multiple testing

- **Primaries in this question: `m = 2`** (P1, P2), **fixed at lock**. It drops to 1 if
  `FIT_RETURNS_UNIVERSAL` fires or P1's artefact cannot be built (§4.5).
- **Family F8 correction set at this lock: 4** — Q033's P1 and P2, plus Q035's P1 and P2. Q030
  (H-074) is DEFERRED and its primary leaves the set while deferred (the H-062 / Q025 precedent);
  Q026, Q028 and Q034 are diagnostics with no primary, no MPE and no q, and enter no correction set.
- Report raw p (the larger of p₁ and p₂, §4.4) and **Benjamini–Hochberg q across the family,
  threshold q ≤ 0.10**.
- Every secondary and descriptive row in §4.3 prints raw p only where a p is meaningful and **enters
  no correction set**, because none of them decides anything.

**What this question does not own, and what no verdict here may be read as confirming:**

- **Q027 (H-073, score ranking validity)** owns whether `overall_score` orders outcomes inside the
  candidate pool at all. Q035 owns whether a *different* ranker builds a better eight. Both can be
  true, both can be false, and a confirmed `Δ` here is **not** a second confirmation of Q027, nor a
  refutation of it. The `UNIVERSAL_BELOW_RANDOM` label (§3 B2) is routed to Q027 and is decided there.
- **H-075 (F1, unregistered)** owns the per-layer ICs and the **leave-one-layer-out** re-ranking.
  Q035's ranker adds a setup-conditional blend; it never removes a layer. Neither strengthens the
  other.
- **Q028 (H-076)** owns the layers' structure and reads no outcome. §1.1 states the relationship:
  corroboration at the decision pass, never a re-specification.
- **Q006** owns the *level* of the published slate's path edge against a matched control; **Q002**
  owns speed; **Q015 / Q018 / Q012 / Q009 / Q010** own band, lane and exit rules on the published
  slate. Q035 changes none of them and confirms none of them: every one of those questions holds its
  slate fixed and varies the rule applied to it, and Q035 holds the rule fixed and varies the slate.
- **Q005** owns the elite-count decomposition; **Q024** owns SAS against external benchmarks, whose
  arms are outside the candidate pool entirely.

---

## 8. Decision rule (numeric, written before unsealing)

`Δ` is in **percentage points of 2.0-ATR touch rate within 20 sessions from the t+1 open**, setup
slate minus universal slate. Both primaries are **two-sided**. **MPE ±5.0 pp** (DP-20, DP-44). **No
MPE, no gate and no floor is lowered at the decision pass in any branch.**

**Gate 0 — construction checks, binary, evaluated before any endpoint is read.** Any failure ⇒ that
primary is **INCONCLUSIVE** and nothing else about it is interpreted. Bounded at **two fix-and-re-run
passes** inside the decision date's hard stop.

1. **Partition viability**, on the in-window population: the §5.3(e) margin share ≥ 0.60 and ≥ 4
   layers carrying non-zero within-night variance on ≥ 80% of contributing nights.
2. **Setup occupancy**: each of A, B, C clears floor B (20 contributing nights). A setup short of 20
   is SUPPRESSED as a stratum; **if two of the three are short, the "A/B/C architecture" is not the
   thing being tested** and both primaries are INCONCLUSIVE, labelled `PARTITION_COLLAPSED`.
3. **Reconstruction correctness**: §5.3(f)'s agreement ≥ 0.90 on undisturbed nights, recomputed
   in-window. Below it, the universal arm is not the platform's slate and nothing is comparable.
4. **Identity checks**: `w = 0 ⇒ S_t ≡ U_t` exactly; `|P_t| ≤ 8 ⇒ S_t ≡ U_t ≡ P_t`; every slate size
   ≤ 8; the 1.0/2.0/3.0-ATR touch sets nested; `GAPPED_THROUGH` rows absent from every hit set. Each
   at relative tolerance 1e-6.
5. **Artefact integrity**: `setup_model_v001.json`'s sha256 matches the value recorded at lock. Any
   mismatch voids the run — `eval.py` fails loudly rather than proceeding.
6. **Reorder rate** (§4.3 row 3) is printed always. **Below 0.25 the primary is INCONCLUSIVE**,
   labelled `NO_ROOM_TO_REORDER`: a ranker that changed the slate on fewer than one contributing night
   in four has not been tested, and reporting that as NULL would be read as "setups do not work" when
   the measurement says "this ranker barely ran" (§11 item 5).

**PROSPECTIVELY_CONFIRMED** (per primary) requires **all** of:

1. **floors A, B, C and D met** (§5.1) on the counts `eval.py` prints;
2. **Gate 0 passes** on all six limbs;
3. the point estimate is **beyond its MPE**: `|mean_t(Δ_t)| > 5.0 pp`;
4. **both CIs exclude 0** — CI-1 **and** CI-2 (DP-51). **Clearing MPE on CI-1 and not on CI-2 is
   INCONCLUSIVE, never CONFIRMED**;
5. **BH q ≤ 0.10** across F8's correction set (§7), on the larger of p₁ and p₂ (§4.4);
6. the point estimate has the **same sign in both calendar halves** (§6), and neither half is beyond
   MPE in the opposite sign;
7. **both blocking companions clear in the same direction as the verdict**: `mean_t(R_S,t − R_B2,t)`
   and `mean_t(R_S,t − R_B3,t)` each with a CI-1 **and** CI-2 bound excluding 0 on the verdict's side.
   A positive `Δ` failing B2 is relabelled **`UNIVERSAL_BELOW_RANDOM`** and is not a confirmation of
   this hypothesis; failing B3 it is relabelled **`LAYER_BLEND_NOT_SETUP`** — the setup labels carried
   no information and what helped was blending a layer subscore into the ranking at all, which is a
   different and simpler product change and is named as such in §9;
8. ≥ **30 contributing nights dated after this file's lock commit** (DP-24) — true of every night in
   the window by construction — reproducing the sign under the **unmodified** `eval.py`.

A verdict meeting 1–7 but not 8 is **HISTORICALLY_CONFIRMED** and carries `HISTORICAL_ONLY`; by
construction that can only arise if the window was truncated, and DP-24's 30 is never reduced to fit
a window.

**A confirmed negative** (`mean_t(Δ_t) < −5.0 pp` with both CIs excluding 0, q ≤ 0.10, sign held in
both halves) is a full verdict, labelled **`SETUPS_WORSE`**, and is ledgered with the same care as a
positive. Clause 7's companions do not block a negative verdict; they are printed beside it.

**NULL** (per primary): floors met, Gate 0 passes, **both CIs include 0**, the point estimate is
inside ±5.0 pp, **and both CIs lie entirely inside ±5.0 pp**. Without that last precision clause "no
difference" could be declared from an uninformative interval. *"The universal 0–100 score picks the
same eight names, as well as any setup-specific ranker does"* is H-083's own FAIL branch, is a real
and useful answer — it defends the scoring architecture — and is ledgered as one.

**INCONCLUSIVE** (per primary): anything else — an estimate inside MPE with a CI wider than ±MPE; an
estimate beyond MPE with a CI including 0; CI-1 and CI-2 disagreeing; the halves disagreeing in sign;
a Gate 0 failure; `PARTITION_COLLAPSED`; `NO_ROOM_TO_REORDER`; or a positive estimate below MPE
(rule 6: positive but below MPE is INCONCLUSIVE, not CONFIRMED).

**A floor shortfall is never INCONCLUSIVE.** Floors A, B, C and D each fire the single automatic
DP-13 extension; still short after it, Q035 goes to DEFERRED (§5.4).

**Question level.** The stronger primary does not carry the question. **H-083's PASS** is the specific
conjunction: **P2 CONFIRMED positive** (the architecture itself, with no fitting to argue about),
with no `UNIVERSAL_BELOW_RANDOM`, `LAYER_BLEND_NOT_SETUP`, `PARTITION_COLLAPSED` or
`NO_ROOM_TO_REORDER` label, **and** P1 not CONFIRMED-negative. **P1 CONFIRMED with P2 NULL** is
reported as what it is — *a particular fitted blend helped; the pure architecture did not* — and is
**not** described as H-083 passing. Any other combination is reported as itself.

**What a confirmed `Δ` does and does not mean (binding on the report).** It means: *"among the names
the platform had already judged publishable on that night, ranking them by the signal that dominates
each one put more names on the slate that travelled two of their own ATRs upward within twenty
sessions, from the next session's open, than ranking them by the universal score did."* It does **not**
mean the picks rose, does **not** mean they reached their printed ladder targets, does **not** mean
money was made, and does **not** say anything about the 80 floor, the 90 line or the 8-slot cap. The
levels `R_S`, `R_U`, `R_pool`, the ATR-per-trade row and the counter-direction row must be quoted
beside it.

---

## 9. If CONFIRMED, what changes on the platform

Nothing subscriber-facing ships before PROSPECTIVELY_CONFIRMED (rule 10), and any number quoted to a
subscriber is W60 (rule 12); every figure in this question is `NON_QUOTABLE` until restated there.

- **EN-018 (behaviour, PROPOSED) is the gated home and this is its gate.** Its two halves separate:
  - the **label half** — A / B / C on the pick card, assigned by §2.3 — is informational and may ship
    on its own merits regardless of the verdict, **flag-off first with a byte-identical checksum on
    the old path** (rule 11), since it changes no ranking and no number;
  - the **ranking half** — per-setup ranking replacing the universal top-8 ordering inside the
    publishable set — ships **only** on P2 CONFIRMED positive with no blocking label (§8), flag-off
    and inert first, then **≥ 20 trading days in shadow** with the old and new slates logged side by
    side, then flipped last (rule 11).
  The publication floor, the completeness floor and the 8-slot cap are **not** touched by either half.
- **`LAYER_BLEND_NOT_SETUP`** licenses a different and smaller change — a layer-weighted re-ranking
  with no setup labels — which is **not** registered here and needs its own PREREG. It is filed as an
  ENHANCEMENTS row, not shipped off this verdict.
- **A line in the Manual Trading Guide** only after PROSPECTIVELY_CONFIRMED, stating the setup a pick
  belongs to and that the slate ordering is setup-conditional. No claim about hit rates without the
  `R_pool` anchor beside it.
- **On NULL:** EN-018's ranking half is **retired** and the finding is ledgered as a defended design
  decision — *the universal 0–100 architecture was tested against its most natural alternative and
  held*. That is a result the desk publishes internally with the same weight as a positive, and it is
  the answer H-083 itself calls PASS-for-the-architecture.
- **On `SETUPS_WORSE`:** EN-018's ranking half is retired and the label half is reviewed, since a
  label that names a worse ordering is a hazard on a card.
- Owner: implementer, via an `IMPLEMENTATION_BRIEF.md` Haci runs in the platform repo. **DP-49 binds
  that brief: no database step is handed to the coding agent**; every check it asks for is satisfiable
  from the repo alone, and the before-snapshot is the pinned parquet.

---

## 10. Known threats to validity (registrar's own list)

1. **The training window is thin (≈ 50 nights) for a fitted ranker.** Mitigated by three *discrete*
   parameters, a 125-cell exhaustive grid, and §4.5's +5.0 pp shrinkage guard. Overfitting shows up as
   an out-of-sample null, not as a false positive — and P2, which is fitted on nothing, is registered
   precisely so the question survives this threat.
2. **The fit reads sealed rows that other locked questions grade on.** It changes no locked PREREG
   (DP-22), produces no verdict on those rows, and its entire output is three numbers pinned before
   any test night exists. Disclosed, not waived.
3. **The 2.0-ATR level is a substitution for the printed L3** (§1.2), forced by the setup arm having
   no ladder. It is the stricter construction, but it means this question does not test the platform's
   *printed* targets at all; Q006 does.
4. **`Δ_t` is granular (multiples of 12.5 pp) with a point mass at exactly 0.** The reorder rate, the
   swap count and the `|P_t|` distribution are printed always, and Gate 0.6 refuses to call a
   near-static ranker NULL.
5. **Setup C may be sparse.** Catalyst carries weight 10 against projection 29 / technical 27 / flow
   24, which is why §2.3 uses within-night z-scores rather than weighted contributions — but a layer
   can still be sparse in its *inputs*. R1 limb (b) and Gate 0.2 measure it before and during.
6. **Three dead or near-dead layers.** GEX carries weight 0 (computed, unused), smart-money is
   forced-zero (PI-008), fundamental enrichment defaults `False`. §2.3 excludes zero-variance layers
   from the argmax and routes their rows to `O`, which is handed back to the baseline; R1 limb (e)
   and Gate 0.1 refuse the question if fewer than four layers vary.
7. **Q028 may show the layers collapse to three factors**, making the A/B split partly arbitrary. This
   question does not wait for that verdict (§1.1) and carries the equivalent check itself; if Q028
   returns REDUNDANT on 2026-09-28, a NULL here reads as better-explained, not as re-specifiable.
8. **H-080 is deferred**, so the 80 floor, the 90 line and the 8-slot cap are untested configuration
   held fixed in both arms (§1.1). A change to any of them splits the window (§2.7).
9. **DP-50(a): one database.** A repair to any layer subscore column rewrites setup labels
   retroactively, and a repair to `overall_score` rewrites the universal slate. The pinned freezes are
   the only defence (rule 4); `DATA_NOTES.md` is swept at the decision pass and a repair dated inside
   the window splits it.
10. **Promoted names never had a conviction card, a ladder or a stop.** Their measured path is a
    stock-path result with no platform-authored plan attached; §9's product change would require the
    platform to write cards for them, which is a build, not a finding.
11. **Bull lane only** (§2.4): nothing here speaks to bear picks, and the bear slate's own ordering is
    untested.
12. **Survivorship in the pool.** §2.5's screens drop truncated-history rows (the CTRA signature) from
    **both** arms identically, but they also shrink `P_t` and can change the universal slate relative
    to what the platform published; Gate 0.3 and R1 limb (f) measure exactly that gap.
13. **Episode dependence is acute** — the same symbol can occupy both slates on many consecutive
    nights. DP-51's CI-2 is a gate on every primary, not a sensitivity.

---

## 11. Open decisions before lock

1. **Whether `capped_by_max_output` rows may enter the arms, against DP-28's literal predicate** —
   Options: A include them (`qualification_reason IN ('selected','capped_by_max_output')`, dark lane
   still excluded) / B keep DP-28 verbatim. Recommendation: A, because under B both arms are the same
   eight rows and the hypothesis cannot be stated, let alone tested.
   Changes: §2.2, §3 B1, §5.3.
2. **Whether the fitted arm P1 is registered at all** — Options: A register both P1 (fitted, H-083 as
   filed) and P2 (pure, parameter-free) at `m = 2` / B register P2 alone at `m = 1`. Recommendation:
   A, because dropping P1 would be re-writing H-083's own "fitted once and frozen" wording (DP-25),
   and P2 already protects the question if the fit fails or returns the baseline.
   Changes: §4.2, §4.5, §7, §8.
3. **The uniform target level** — Options: A 2.0 ATR decides, 1.0 and 3.0 printed / B 1.0 ATR decides
   (nearer the printed L1/L2 band). Recommendation: A, because 1.0 ATR sits inside ordinary noise
   where H-053 expects no selection signal at all, and the level must be fixed before any of the three
   is seen. Changes: §4.1, §4.3.
4. **Lane scope** — Options: A bull lane only, bear slate identical in both arms / B re-rank both
   lanes under one setup model. Recommendation: A, because the lanes have separate thresholds and
   separate caps, and B would let a verdict about ranking be produced by a change in direction mix.
   Changes: §2.4, §4.1, §10.
5. **A ranker that seldom reorders** — Options: A reorder rate < 0.25 ⇒ INCONCLUSIVE
   (`NO_ROOM_TO_REORDER`) / B report it as NULL. Recommendation: A, because a NULL would be read as
   "setup ranking does not help" when the measurement says the ranker barely changed the slate.
   Changes: §8 Gate 0.6.
6. **Nights on which the two slates come out identical** — Options: A contribute with `Δ_t = 0` /
   B excluded, with a restricted endpoint over reordered nights only. Recommendation: A, because the
   product question is whether the architecture improves the published slate, and a night it leaves
   untouched is a night with no improvement; B is printed as a descriptive companion either way.
   Changes: §2.6, §4.3.
7. **The fitted arm's training window** — Options: A 2026-06-01..2026-08-12 (post-DP-06, matured on
   v001, ≈ 50 nights) / B the desk's in-sample split 2026-01-02..2026-05-31 as H-083's line words it.
   Recommendation: A, because setup C reads the catalyst layer and DP-06 makes that a different
   feature before 2026-06-01, so B would fit one of the three setups on a feature the test window does
   not contain. Changes: §4.5, §6, §10 threat 2.
