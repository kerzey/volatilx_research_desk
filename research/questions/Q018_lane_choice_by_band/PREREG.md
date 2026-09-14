# Q018 — lane_choice_by_band: for the same pick, does the day, the swing or the long-term lane plan make the most money — and does the answer depend on the score band?

**Status:** DRAFT (lock by committing this file)
**Family:** **F6 Exits and execution** (hypothesis **H-051**, filed in F6 in `research/BACKLOG.md`; no re-filing — the primary endpoints contrast three *execution plans* on the same picks, which is F6's subject, DP-29).
**Manifest (definitions, pinned now):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e) · research/data/manifest_prices_v001.json (base_manifest_sha256 b03f355a…bef374).
**Manifest (the population itself):** the successor selection and price freezes named in §5 (DP-23). **Every contributing night in this question is dated after the lock commit** (§6) — v001 supplies definitions, exclusion criteria and the measured run-rates, and supplies **no** graded row to any primary.
**Exclusions:** the **union** of `research/data/exclusions_v003.json` (`manual_runs.trading_dates`, `non_session_runs.trading_dates`, `uncorroborated_publication_runs.trading_dates` — the newest file at lock, DP-22) **and the add-only successor exclusions file** `exclusions_v00N` issued with the successor selection freeze, built by the **identical three criteria** over the post-lock nights (DECISIONS item 4). The successor file may only **add** nights; no night is ever removed from a v003 list, and the criteria are fixed at this lock even though the dates cannot be. DP-04 applies mechanically on top. `eval.py` takes both paths as inputs and reads the JSON — **no hard-coded dates and no hard-coded file name**.
**Measured exposure (Q018's own, R1 returned):** `research/reports/STEWARD_Q018_exposure.md` (2026-09-13; counts only, from the pinned freeze per DP-50(c), no outcome of any kind), which re-derives on Q018's own definitions and matches `research/reports/STEWARD_Q012_exposure.md` **exactly**: **541 published rows on 67 non-excluded nights of 70 elapsed sessions**; **24 of 541 removed (4.4%) — 16 on the ladder/six-target test** (8 of them carrying no lane plan at all, all on 2026-06-02) **and a further 8 on the wrong-side-of-`C_t` (7) and `outcome_target_invalid` (1) tests** — leaving **517 eligible = 495 LOW/HIGH + 21 ELITE + 1 REF**; **66 of 70 elapsed sessions are contributing nights = 0.9429 per elapsed session**, **42 of 70 both-band = 0.6000**, **20 of 70 ELITE = 0.2857 on a declining monthly trend (10 / 6 / 3 / 1)**; **1 REF night in the whole window**; hourly coverage 100% on published-pick symbols.
**Decisions:** DECISIONS.md
**Registered by:** registrar · **Approved by:** desk (DP-46) · **Date:** 2026-09-13

---

## 1. Hypothesis (plain English)

**Take one published pick and trade it three ways — the day-lane plan, the swing-lane plan and the
long-term-lane plan the platform printed for that same pick on that same night — and one of the three
makes more money per trade than the other two; which one wins depends on the pick's score band.**

BACKLOG H-051 reads: *"Lane choice: which lane's plan (day/swing/long) maximises realized return per
score band."* It names no entry, no exit weights, no horizon convention, no baseline and no decision.
This PREREG fixes all of them (§2–§4). No lane is presumed to win; every contrast is two-sided, and
"lane choice is worth less than a quarter of an ATR per trade" is a real, ledgered outcome (§8).

**Why the question is not already answered by the platform.** The three lane plans are written by one
LLM call that is instructed to produce *"three meaningfully different strategies: day trading
(minutes-hours), swing (days-weeks), long-term (weeks-months)"* and to *"choose targets that better
match the horizon"* (volatilx `ai_agents/principal_agent.py:546-554`; the deterministic fallback is a
flat 0.5% / 1.0% step pair at `:897-911`). Those levels then become the ladder L1…L6 — day t1/t2,
swing t1/t2, long t1/t2 (`services/sas_conviction_card.py:182-187`) — and are graded over **20 / 40 /
60 trading days by lane** (`:194`, the 2026-09-05 lane-window ruling). Two consequences make the
question live: the day lane's targets are authored for *minutes-hours* but graded over **twenty
sessions**, and `_enforce_ladder_monotonic` re-sorts the flattened ladder across lanes whenever it is
not price-monotonic (`services/super_agent_select_service.py:195-215`, shipped by `5fa3db4` on
2026-07-06 — before this question's window opens), so **in every payload in the primary window**, by
code, "day" simply *means* the two nearest levels and "long" the two furthest (measured: 0.00%
non-monotonic on the 355 eligible picks published on/after the ship date, against 25.71% on the 140
before it — `STEWARD_Q018_exposure.md` §2; §10 threat 2). Nothing in the platform
measures what a unit of capital earns under each lane's plan, and the one published per-band
schedule (`BAND_EXITS`, `scripts/generate_sas_trading_guide.py:89-95`) is a strategist ruling that
spans all six levels at once and never asks which lane to trade.

**What this question does not test, stated up front.**
- It does not test **stops**. No plan here exits on a stop (rule 5, **DP-02**); the printed lane stops
  and invalidations are measured and reported, never used as exits. Stops as exits are Q009 / Q010.
- It does not test **recycling the freed capital**. A day-lane plan that goes flat in four sessions
  leaves capital idle here; what to do with that capital is Q012's subject, and §4's
  ATR-per-committed-session companion plus §7's overlap note keep the two apart.
- It does not test the **entry price**. All three lanes are entered at the same actionable price
  (§2), so no part of any contrast is an entry effect (Q004 / Q011 own that).
- It carries **no verdict for the 90+ band or for `<80`**: 90+ is a descriptive sub-cell (§5) and
  `<80` is structurally near-absent from publication (1 row in 579 measured). **A verdict here speaks
  for 80 ≤ `overall_score` < 90 only**, and §9 binds the report to say so.

## 2. Population

- **Unit of inference: the trading night** (rule 6) — the **pick night** on which the lane choice
  would be made. Picks are averaged within their pick night first; the estimator is a within-night
  **paired** difference between plans applied to the **same pick**, so the night's tape, the symbol,
  the entry and the direction are all held fixed and only the lane's targets and window differ.
- Source tables (successor selection freezes; definitions from `manifest_v001`): `sas_candidates`
  (`qualified`, `selected_rank`, `overall_score`, `dominant_direction`, `best_timeframe`,
  `public_payload_json` → `lane_plans.{day_trading, swing_trading, longterm_trading}.{targets, entry,
  stop, invalidation}`, `outcome_target_invalid` for the exclusion audit only), `sas_runs`
  (`finished_at`, for the DP-04 exclusion criterion and the descriptive `E_AH` sensitivity).
- Source tables (successor price freezes): `prices_daily_split` (pick-night close, session
  opens/highs/lows/closes, ATR14, beta60, run-up, SPY tape), `prices_daily_raw` (split-factor
  snapping only), `prices_hourly_raw` (the descriptive stop sensitivity and the descriptive `E_AH`
  price only — **no primary endpoint depends on hourly bars**, §4 ordering rule 2).
- **Eligible pick (one pick, three plans):** `qualified IS TRUE AND selected_rank IS NOT NULL`
  (**DP-28**; dark-lane and qualified-false rows never enter any arm), on a non-excluded pick night
  inside the §5 window, with `overall_score` present, a bullish/bearish `dominant_direction`, and
  **all three lane plans carrying both targets** —
  `T_D1, T_D2 = day_trading.targets[0..1]`, `T_S1, T_S2 = swing_trading.targets[0..1]`,
  `T_L1, T_L2 = longterm_trading.targets[0..1]` (`services/sas_conviction_card.py:182-187`) — each
  strictly on the correct side of the pick-night close `C_t` for the pick's direction, **and passing
  the payload price-scale screen** in the exclusions list below. **A pick enters the paired contrasts
  only if it is gradeable in all three lanes**; picks failing that are counted in the funnel and enter
  nothing (pairing is never broken to gain rows).
- **Cohorts (the platform's own bands, `scripts/generate_sas_trading_guide.py:78-84`):**
  **LOW** = 80 ≤ score < 85 · **HIGH** = 85 ≤ score < 90 · **ELITE** = score ≥ 90 (DP-42's definition
  of elite; descriptive only) · **REF** = score < 80 (descriptive only). **LOW ∪ HIGH is the primary
  population.** REF is measured at **1 published row in 579** across the v001 window
  (`STEWARD_Q012_exposure.md` §5), and that single row has a known cause: it is **TJX, 2026-06-11,
  score 79.58**, published **before** the 80-point floor was codified — `1765a6f` (2026-07-07) sets
  `SuperAgentSelectConfig.publication_floor = 80.0` (`services/super_agent_select_models.py:86-91`;
  `STEWARD_Q018_exposure.md` §5), and the measured minimum published bullish score is 79.58 pre-ship
  and 80.14 post-ship, i.e. **no sub-80 bull was published after the floor shipped**. REF is therefore
  structurally absent from this question's window **by code**, not merely thin, and is **SUPPRESSED**,
  printed as a bare count. ELITE is a **descriptive sub-cell** that carries no verdict (§5, §8).
- **Definitions (all prices in the signal-date split basis):**
  `C_t` = the pick's **actual** regular-session close on its pick night from `prices_daily_split`
  (never the platform's `spot_close`, stale on re-run nights — EXPLORE_001 §9);
  `ATR` = ATR14 from `prices_daily_split` bars dated ≤ the pick night (the platform's `atr_pct` is
  corrupted around splits — PI-003 / DATA_NOTES; not used);
  `dir` = +1 bullish, −1 bearish;
  `O_1` = the pick's session t+1 **official** regular-session open (`prices_daily_split.o`) — **the
  entry basis for every plan in this question, picks and controls alike** (**DP-03(b)**; DECISIONS
  item 2, decided 2026-09-13: DP-11 does not apply, since no lane plan here is a position already held
  when the signal appears, and DP-03(a) is scoped to the 90+ band, which is not this population).
  The lane plans' own printed `entry` prices are **not** used to fill: they differ by lane, they are
  limit-style levels that may never trade, and using them would make the lane contrast partly a
  fill-rate contrast (Q011's subject). They are measured and reported descriptively (§4).
  `W_D = 20`, `W_S = 40`, `W_L = 60` sessions = each lane's own grading window
  (`services/sas_conviction_card.py:194`), counted as sessions **t+1 … t+W** from the pick night.
- **Exclusions — each counted per arm and printed in the results header, never silently dropped.
  Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or
  a measurement failure:**
  - nights in the **union of `research/data/exclusions_v003.json` and the add-only successor
    exclusions file** `exclusions_v00N` issued with the successor selection freeze (DECISIONS item 4;
    DP-22 read as "one list, built by one set of criteria" — its "cite the newest file" clause
    presumes a sealed window, and this window postdates every file that exists at lock): for each
    file, `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪
    `uncorroborated_publication_runs.trading_dates`. The successor file applies the **identical three
    criteria** to the post-lock nights and may **only add** nights; no night is ever removed from a
    v003 list, and the criteria are fixed at this lock. `eval.py` takes both paths as inputs and reads
    the JSON; **no date and no file name is hard-coded**.
  - any night whose run `finished_at` is later than the next session's open (DP-04, applied
    mechanically).
  - **null-ladder denominator:** a pick missing any lane plan or any of the six targets → not
    eligible, counted. **Measured on the identical test** (`STEWARD_Q018_exposure.md` headline,
    matching `STEWARD_Q012_exposure.md` §2 row for row): **16 of 541 published rows (3.0%)**, of which
    8 carry no lane plan at all (all on one night, 2026-06-02).
  - picks with `outcome_target_invalid` non-null, or any of the six levels at or through `C_t` at
    publication (`services/super_agent_select_service.py:113-145`) → not eligible, counted. The test
    is made at the close, **before** any session t+1 price exists, so it is identical for all three
    lanes. **Measured: a further 8 of 541 (wrong-side-of-`C_t` 7, `outcome_target_invalid` 1)**, so
    the two tests together remove **24 of 541 (4.4%)** and leave **517 eligible = 495 LOW/HIGH + 21
    ELITE + 1 REF**.
  - **payload price-scale screen** (DECISIONS item 10; `DATA_NOTES.md` 2026-09-13, "`lane_plans` price
    levels are on the wrong split scale for some symbols"). The platform's printed lane levels are
    sometimes built from a **raw, non-split-adjusted** reference price while `C_t` and ATR come from
    `prices_daily_split`, and the wrong-side-of-`C_t` test above does **not** catch it (a 2×–10×
    raw-scale bullish target still sits "above" the split-adjusted close). A pick is eligible only if
    its own payload levels are on the same scale as `C_t`, tested from **pick-night data only** —
    the payload plus `prices_daily_split` bars dated ≤ t — and therefore **before any session t+1 bar
    is loaded** (rule 14; no rule-14 exception is requested or needed, DP-41 untouched):
    **(i)** `ρ = median(the three lane plans' printed entry levels) / C_t` must satisfy
    **0.80 ≤ ρ ≤ 1.25**; a pick carrying no printed `entry` on any lane fails;
    **(ii)** every one of the six targets and all three stops/invalidations must satisfy
    **0.5 ≤ level / C_t ≤ 2.0**;
    **(iii)** ATR backstop: the nearest target's distance `d = dir × (T − C_t)/ATR` ≤ **10 ATR** and
    the furthest ≤ **25 ATR** (the measured clean maxima are 3.325 and 16.163 —
    `STEWARD_Q018_exposure.md` §2).
    A pick failing **any** limb is **dropped from all three arms and from the B2 control construction**,
    counted in the funnel under its own reason code **`payload_scale_mismatch`**, and reported by
    symbol, band and month. It is **never rescaled, repaired or imputed** (§2's measurement-failure
    treatment; PI-003 precedent — a corrupted platform price quantity is not used, not corrected). A
    night losing **> 25%** of its otherwise-eligible picks to the screen is dropped under the 25% rule
    below. The screen applies identically to the sealed descriptive panel (§6). Measured sealed-period
    incidence: **17 of 495 picks (3.4%)** — APH 14 of 14 at ~2.0×, KLAC 10.18×, CRWD 4.07×, MNST
    2.02×; the four named symbols are **not** asserted to be the complete list (§10 threat 15).
  - picks with no session t+1 bar, or missing forward bars inside a lane's window (halt, delisting)
    → ungradeable; the **pick** is excluded from all three arms and counted. This is a **measurement
    failure, not a classifier**: it never moves a pick between arms. A night is dropped if > 25% of
    its eligible picks are ungradeable.
  - symbols with fewer than 60 daily bars dated ≤ t (ATR / beta / run-up undefined) → excluded,
    counted.
  - pick nights whose session **t+60** falls after the last trading date of the pinned successor
    price freeze (immature) → excluded and counted. Maturity comes **from the trading calendar**,
    never from whether a price exists; right-censoring is never graded as a non-touch. The long
    lane's 60 sessions is the binding clock for **every** pick, so all three lanes are measured on
    exactly the same set of nights.
- **Contributing night (the floor unit, DP-21):** a pick night carrying **≥ 1 eligible LOW-or-HIGH
  pick gradeable in all three lanes**. P1, P2 and P3 share this definition. **P4's own contributing
  night is a pick night carrying ≥ 1 such pick in *each* of LOW and HIGH** ("both-band night") and is
  counted and gated separately (§5). A matured night on which no pick survives the funnel is a
  **non-contributing night, not an exclusion**: it never enters `exclusions_vNNN.json`, never counts
  toward any floor, and is printed in the funnel with its cause.

## 3. Baseline(s) — what this must beat

- **B1 (primary baseline, and the cleanest one available): the other two lanes' plans on the same
  pick, same night, same entry, same ATR denominator.** This is "Y's rate when X did not happen" with
  everything but the plan held fixed: one pick, one entry price, three printed plans. Every primary
  endpoint (§4) is a paired contrast against this baseline, which is why no lane may be declared best
  on a single comparison — it must beat **both** others (§8).
- **B2 (rule-5 distance-matched control; binding on what may be *claimed*, §8 clause 8, §9):** for
  each eligible pick, the **10 nearest same-night non-published `sas_candidates` rows** — the
  complement of the DP-28 publication predicate — on `beta60` / `atr_pct` / `runup20` (from
  `prices_daily_split` bars dated ≤ that pick night; standardized by the night's cross-sectional
  median and MAD; Euclidean; with replacement across picks; ties by symbol ascending) — the **Q006 §3
  / Q002 B1 construction verbatim** — each carrying **synthetic lane targets at the same ATR distances
  and the same direction** as the pick's six levels, anchored at the control's **own** pick-night
  close: `T_c = C_c × (1 + dir_p × d_p × atr_pct_c)` with `d_p = dir_p × (T_p − C_{t,p}) / ATR_p`,
  graded under exactly the §4 plans, on the same three windows, from the control's **own** session t+1
  open and own forward bars. The control therefore carries the identical *distance* and *horizon*
  structure with none of the selection, so the control's own lane ordering is the answer to "is this
  just distance and time?". Control rows never add to inferential n (rule 6).
- **B3 (the platform's current behaviour, descriptive):** the pick's own `best_timeframe` lane
  (short → day, swing → swing, long → long — `docs/SAS_EXCURSION_BACKFILL.md:62`), traded under the
  same §4 plan. Each fixed-lane result is printed against this "follow the platform's recommendation"
  arm, which is what a subscriber does today. It is **descriptive and decides nothing**: a fixed-lane
  rule that beats it is interesting, but the primary claim H-051 makes is about the lanes themselves.
  Lane assignment is **measured non-degenerate but skewed short** on this question's own population
  (`STEWARD_Q018_exposure.md` §1, R1 returned 2026-09-13, counts only): on the 495 eligible 80–90
  picks, **short 343 (69.3%) / swing 97 (19.6%) / long 55 (11.1%)**, with all three lanes present in
  **both bands and every month** (LOW 287/87/48, HIGH 56/10/7), and the share whose assigned lane
  differs from each fixed lane **0.3071 from day, 0.8040 from swing, 0.8889 from long**. The weekly
  2026-09-12 §4 counts (474 short / 160 swing / 65 long) are a **different population** — the W20
  population, not the six-level-eligible 80–90 cohort — and may be quoted only as a shared "skewed
  short" shape, never as a ratio against these numbers. B3 stays descriptive (§10 threat 11).
- **B4 (descriptive, cross-question reconciliation):** the same three plans entered at `C_t` (the
  DP-03(a) after-hours proxy, DP-11 — the basis Q007, Q009 and Q015 use) and at `E_AH` (Q004's
  definition verbatim, picks only). Neither decides; both exist so Q018's numbers reconcile with the
  rest of the desk, and both are the sensitivity that shows how much of any day-lane result is the
  overnight gap the entry basis includes or excludes (DECISIONS item 2).

## 4. Objective metric (rule 5 — price path under a named execution plan)

**The plan, identical in shape for all three lanes.** One unit of capital, entered at `O_1`. **50% of
the position exits at the first touch of the lane's t1 and 50% at the first touch of the lane's t2**,
within sessions t+1 … t+W(lane), at the level's price — or at that session's open if the session
opens through the level (a resting exit limit fills at the better price). Anything not exited at a
target — a target never touched inside the window, or a target **unfillable at entry** because it sits
at or through `O_1` in the trade direction (rule 5, DP-26: a target already passed at entry is never a
hit) — closes at the **final close of that lane's window**, `C_{t+W}`. **No stop** (rule 5, DP-02).
The written trailing / max-hold text attached to the guide's band rows is not deterministic enough to
simulate and is ignored (Q011 §4, Q012 §4 precedent).

*Why 50/50 and not the band's own weights:* `BAND_EXITS` distributes weight across all six levels at
once and assigns the 90+ row **zero** weight to both day levels, so it cannot be renormalized into a
day-lane plan at all. A single fixed shape, identical in every lane, is what makes the contrast a
statement about **the lane's targets and horizon** rather than about weights that differ by lane and
band (DP-26: a registrar convention, chosen before any outcome is seen, and not derived from sealed
data).

**Realized result of lane ℓ on pick i (the money, in ATR):**

`r_{ℓ,i} = 0.5 · dir · (x₁ − O_1)/ATR + 0.5 · dir · (x₂ − O_1)/ATR`

where `x_k` = the lane's target price `T_{ℓ,k}` if that target was fillable at entry and first-touched
within the lane's window (at the target price, or at the session's open if the session opened through
it), else `x_k = C_{t+W(ℓ)}`. ATR is the pick's own, so the three lanes share one denominator and the
contrasts are additive ATR per unit of capital committed on the pick night.

**Ordering rules, stated once and applied by `eval.py` with no judgment:**
1. **A level touched intraday on the entry session counts**, provided it was not at or through `O_1`
   at the entry (rule 5, DP-26).
2. **Same-session touches of t1 and t2 inside a lane need no ordering:** each half exits at its own
   level price, so the order does not change `r`. **No primary endpoint depends on hourly bars**; the
   hourly freeze is needed only for the descriptive stop sensitivity and `E_AH` (§5 R2 item iii).
3. **Lanes are independent simulations of the same pick.** There is no interaction between them and
   no shared position; three plans are each measured against the same entry.
4. **Counter-direction levels, the lane's printed stop, the lane's invalidation and maximum adverse
   excursion are measured and reported, never used as an exit** (rule 5, DP-02).
5. **One pick set across every arm and its controls.** A pick dropped by §2's payload price-scale
   screen — or by any other §2 exclusion — leaves all three lane arms **and takes its B2 control set
   with it**, so the paired contrasts and the distance-matched control always describe the same picks.
   Pairing is never broken to gain rows.

**Primary endpoints (four, pre-specified; BH within the question at m = 4 in every branch, §7).**
For night t, over eligible LOW ∪ HIGH picks gradeable in all three lanes:

- **P1 — swing minus day.** `Δ1_t = mean_i [ r_{S,i} − r_{D,i} ]`; estimand **`m1 = mean_t Δ1_t`**,
  ATR per trade.
- **P2 — long minus swing.** `Δ2_t = mean_i [ r_{L,i} − r_{S,i} ]`; estimand **`m2 = mean_t Δ2_t`**.
- **P3 — long minus day.** `Δ3_t = mean_i [ r_{L,i} − r_{D,i} ]`; estimand **`m3 = mean_t Δ3_t`**.
  P3 equals P1 + P2 by construction; it is registered anyway because a *ranking* claim needs the
  extreme pair compared directly, and BH over four partly dependent tests is conservative, never
  permissive (§7).
- **P4 — the band gradient (H-051's "per score band").** On **both-band nights** (§2),
  `Δ4_t = mean_{i ∈ HIGH} [ r_L − r_D ] − mean_{i ∈ LOW} [ r_L − r_D ]`; estimand
  **`m4 = mean_t Δ4_t`**, ATR per trade. Positive = the higher band prefers the longer horizon more
  than the lower band does. **P4's MPE is 0.50 ATR — twice P1–P3's** — because it is a difference of
  differences measured on the thinner both-band nights (Q012 P2 and Q007 §8 precedent; DP-10 permits
  a larger value with a stated reason and never a smaller one).

**Secondary, descriptive, never decides:**
- **the control lane ordering (B2)**: `r_D`, `r_S`, `r_L` on the matched controls and the three
  picks-minus-control differences-in-differences, each with a block-bootstrap CI and raw p. These do
  not change the verdict, and they **bind what may be claimed**: §8 clause 8 and §9.
- **ATR per committed session** — `r_ℓ / W_ℓ` (20 / 40 / 60) — printed beside every primary. This is
  a deterministic rescaling, not a second test; it exists because a lane that wins per trade can lose
  per unit of capital-time, and §9 forbids a guide line that hides that (threat 4).
- **B3**, the `best_timeframe`-follows arm, and each fixed lane minus B3, per band.
- **B4**, the `C_t` and `E_AH` entry bases.
- **the stop sensitivity:** the same three plans with the **lane's own printed stop** as an exit,
  ordered against a same-session target by **DP-27 (stop-first)** using hourly bars where they exist.
  Descriptive by DP-02, printed so the no-stop result can be read honestly; it never decides and
  never licenses a rule here (Q009 / Q010 own stops).
- per-lane **first-touch rates** of t1 and t2 within the lane's own window, picks and controls, from
  `O_1` — the rule-5 hit-rate table the plan result is reported next to — with **sessions-to-first-
  touch** (descriptive, no MPE, DP-44) and the **share unfillable at entry** per lane;
- per-lane **ATR distance** of t1 and t2 (`d = dir × (T − C_t)/ATR`) and its distribution, plus the
  **lane-distance tercile cells** (threat 2). **The share of payloads whose flattened ladder was
  re-sorted across lanes is *not measurable in this window*** and is not registered as an in-window
  secondary: `_enforce_ladder_monotonic` shipped on 2026-07-06, before the window opens, so every
  published ladder here is cross-lane monotonic **by construction** and the pre-re-sort ladder is not
  recoverable from the frozen payload. It is measured **only** on the sealed panel's pre-2026-07-06
  sub-panel (§6), and in-window it is replaced by (a) a per-pick cross-lane ordering check on the
  window's own payloads, printed as a **verification** (expected 0% non-monotonic) and not as a
  mitigation, (b) the per-lane ATR-distance distribution and (c) the lane-distance terciles;
- the counts of the lane plans' printed `entry` prices relative to `O_1` (stray, fill-within-5-sessions
  rate) — the measurement that says how different a lane-entry version of this question would be;
- maximum adverse excursion per lane in ATR; counter-direction touches; lane stop and invalidation
  touch rates;
- **ELITE (90+)** and **REF (<80)** cohorts under all three plans — **descriptive, carrying no
  verdict**, SUPPRESSED below 20 contributing nights on `eval.py`'s own measured count;
- close-to-close return at T+20 / T+40 / T+60 — **fixed-horizon return is secondary and descriptive
  by rule 5 and DP-01, and never decides**, including where it is the form H-051's own wording
  ("realized return") suggests.

**Quotability:** 20 / 40 / 60-session bases → **every number here is NON_QUOTABLE** (rule 12).

**Inference.** Night-level. **CI (decides):** stationary block bootstrap over the ordered contributing
pick nights, expected block length **20 sessions** (the 60-session long-lane windows of adjacent
nights overlap almost completely; the same block length Q012 fixed for the same reason, fixed here
before any result); 2,000 resamples; the date-clustered bootstrap CI is printed alongside.
**p-value:** paired sign-flip permutation on the night contrasts `Δ1_t … Δ4_t`, 10,000 permutations,
seed 20260913. Every estimate prints n(contributing nights), n(contributing nights dated after the
lock commit), n(picks), n(picks gradeable in all three lanes), n(unfillable fractions by lane),
n(never-touched fractions by lane), n(control rows), and n(excluded, by reason — including
`payload_scale_mismatch`, reported by symbol, band and month).

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** and ≥ **20
  contributing nights per reported sub-cell**. A sub-cell below 20 nights is **SUPPRESSED** — no point
  estimate printed, not even "small n, directionally", counts only — and a SUPPRESSED sub-cell does
  **not by itself** make its endpoint INCONCLUSIVE (§8 clause 1). The weaker reading ("80 eligible
  nights with ≥ 20 contributing") is **not** used (DP-21). **No floor is ever lowered to hit a date.**
- **Binding maturity: 60 sessions** from every pick night — the long lane's window, applied to all
  three lanes so that the three arms always share one night set (§2).
- **Measured exposure (DP-50(c): from the pinned freeze, never a live query).**
  `research/reports/STEWARD_Q018_exposure.md` measures this question's own funnel over
  2026-06-01..2026-09-09 — **70 elapsed sessions, of which 67 are non-excluded** (2026-06-26, 07-02
  and 07-06 excluded) — and matches `STEWARD_Q012_exposure.md`'s identical test row for row: **541
  published rows; 24 removed (4.4%) = 16 on the ladder/six-target test + 8 on the wrong-side-of-`C_t`
  (7) and `outcome_target_invalid` (1) tests; 517 eligible = 495 LOW/HIGH + 21 ELITE + 1 REF**;
  **66 of 70 elapsed sessions are contributing nights = 0.9429 per elapsed session** on the 80–90
  population; **42 of 70 both-band nights = 0.6000 per elapsed session**; **20 of 70 ELITE nights =
  0.2857 per elapsed session on a declining monthly trend (10 / 6 / 3 / 1)**; **1 REF night**; hourly
  coverage 100% on published-pick symbols. Those rates are what the projection below uses, **per
  elapsed session** — the denominator is elapsed sessions (calendar minus holidays, exclusions **not**
  pre-removed), and the window's 137 is likewise **elapsed sessions**, which is the matching basis.
  Recomputing on the 67 non-excluded nights would give 0.627 both-band per session, pull the 80th
  both-band night forward and shorten the window — the move DP-43 and DP-45 forbid.
- **Routed request R1 (Data Steward, counts only) — RETURNED 2026-09-13,
  `research/reports/STEWARD_Q018_exposure.md`.** Answered in full from the pinned freeze with no
  outcome of any kind, and it decided no endpoint and moved no date: (a) `best_timeframe` among the
  495 eligible 80–90 picks = **short 343 / swing 97 / long 55**, non-degenerate by band and by month,
  with differs-from-lane shares **0.3071 / 0.8040 / 0.8889** (B3, §3, threat 11); (b) per-lane ATR
  distances on the 478 picks clean of the §2 scale screen — day t1 quartiles 0.237 / **0.367** / 0.526
  through long t2 5.151 / **6.367** / 8.071, with swing t2 ≥ long t1 on 59.62% of picks and day t2 ≥
  long t1 on 1.67% — and the ladder-monotonicity share returned as **two regimes, 25.71% (36/140)
  before 2026-07-06 and 0.00% (0/355) on/after** (threat 2, §4, §6); (c) the share of eligible picks
  with ≥ 1 lane target at or through the session t+1 open, by lane = **day 14.14% (70/495) / swing
  2.02% / long 0.00%** (threat 14; DECISIONS item 3's sensitivity counts); (d) the reconciliation on
  Q018's own contributing-night definitions came back an **exact** match to the borrowed rates
  (0.9429 / 0.6000 / 0.2857, month-by-month identical), so **no date moved and none could have moved
  in** (DP-43, DP-45). Two findings beyond the request — the 2026-07-06 ladder-monotonicity ship and
  the `lane_plans` price-scale mismatch — are now dated `DATA_NOTES.md` entries and are handled in §2
  (the screen), §4, §6 and §10 threats 2 and 15.
- **Routed request R3 (Data Steward, counts only, opened 2026-09-13; non-blocking, can move the
  §5 dates out, never in).** On the pinned freeze, recompute the three rates above **with §2's payload
  price-scale screen applied**, and report how many **nights** — not only picks — the screen removes
  from each of the contributing, both-band and ELITE counts (nights whose only eligible 80–90 pick, or
  only LOW or only HIGH pick, is a scale-mismatch row), plus whether APH / KLAC / CRWD / MNST are the
  complete list on this population. The screen can only **reduce** eligibility, so this can only slow
  the measured rate: if the both-band rate falls below 0.6000 the 80th both-band night is recomputed
  and the window end **moves out**; if it is unchanged, nothing happens. No floor is lowered and no
  date is pulled forward. R3 decides no endpoint.
- **Projection (mechanical, gates nothing).** Window = pick nights **2026-09-14 .. 2027-03-31**, which
  is **137 elapsed sessions** — the same basis the run-rates are measured on (Sep 13, Oct 22, Nov 20,
  Dec 22, Jan 19, Feb 19, Mar 22; holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15,
  2027-03-26):
  - **80 contributing nights (P1, P2, P3):** 137 × 0.9429 ≈ **129**. Reached around 2027-01-22. **Not
    binding.**
  - **80 both-band nights (P4):** 137 × 0.6000 ≈ **82**, the 80th landing at elapsed session 133.3,
    i.e. the **134th session ≈ 2027-03-25**. This is the **binding** endpoint and is what sets the
    window end: the registered end 2027-03-31 is four sessions later (≈ 2 both-band nights of margin,
    **out, never in**), and it clears 80 thinly by construction, since DP-43 sets the window at the
    *earliest* date every primary's floor is projected to be reached. DP-13's automatic +30 sessions
    (≈ 18 further both-band nights) is the stated remedy and needs no new decision.
  - **30 contributing nights dated after the lock commit (DP-24):** **all ~129 are post-lock** — the
    window opens after the lock (§6), so DP-24 is satisfied by construction and
    **PROSPECTIVELY_CONFIRMED is reachable from this run**. DP-31 (HISTORICAL_ONLY) does not apply.
  - **ELITE:** 137 × 0.2857 ≈ 39 nights on a flat extrapolation, far fewer on the observed declining
    trend. ELITE is a **descriptive sub-cell** either way; whether it is printed or SUPPRESSED is
    decided at the decision pass on `eval.py`'s own count against the 20-night floor. **REF is
    SUPPRESSED** (structural, §2). **BH stays at m = 4** in every branch.
  Every gate below is decided on the **measured counts printed by `eval.py`** at the decision pass,
  never on this projection and never on R1, R2 or R3.
- **Window, decision date, extension and DEFERRED fallback (DP-43; DP-13; no outcome is looked at at
  any point):**
  - **Primary window: pick nights 2026-09-14 .. 2027-03-31 inclusive**, after exclusions. *Why it
    starts after the lock:* the sealed period has already been read for this hypothesis (§6), so it is
    not available as a blind test; *why it ends there:* P4's measured 0.6000 both-band nights per
    elapsed session put the 80th both-band night at ≈ 2027-03-25 (DP-43 sizes the window on **every**
    primary's floor), and the registered end is four sessions later. A shorter window that reached a date sooner was not taken (DP-43, DP-45).
  - **Decision date: Monday 2027-07-12.** The 60th session after 2027-03-31 is ≈ 2027-06-25 (holidays
    2027-05-31, 2027-06-18); plus the one-week freeze margin = 2027-07-02; the first Monday on or
    after is 2027-07-05, which is the observed Independence Day market holiday, so the date moves
    **out** to Monday 2027-07-12. The Steward fixes the exact session-count date when building the
    successor freezes, and a correction may move it **out, never in**. `eval.py` is written once
    (rule 9) and run **once**, then. **No interim looks.** The date sits ≈ 9.9 months after lock,
    inside DP-43's 12-month ceiling.
  - **Both gates, per primary endpoint, on measured counts.** An endpoint is evaluated only if it has
    **≥ 80 contributing nights** (P1–P3: a night with ≥ 1 eligible three-lane-gradeable 80–90 pick;
    **P4: a both-band night**) and **≥ 30 contributing nights dated after this file's lock commit**
    (DP-24, satisfied by construction). A shortfall on one endpoint is never covered by another's
    count.
  - **One automatic extension (DP-13; DP-43's +30 sessions), triggered by *any* primary endpoint.**
    If **any of P1–P4** is short of either gate at 2027-07-12 on `eval.py`'s measured counts, the
    window extends **once**, automatically and with no new question, to pick nights **2026-09-14 ..
    2027-05-12** (= 2027-03-31 + 30 sessions), decision date **Monday 2027-08-16** (the 60th session
    after 2027-05-12 is ≈ 2027-08-09, plus the one-week margin, next Monday; the Steward fixes the
    exact date). The trigger is not restricted to P1: this window is sized on **P4's** floor, so a
    P1-only trigger would print P4 INCONCLUSIVE on a one- or two-night miss with the sample weeks
    away. The extended run uses the **unmodified `eval.py`** and the same gates. Both dates are inside
    DP-43's ceiling (9.9 and 11.1 months from lock).
  - **DEFERRED fallback.** If **P1's or P3's** gates are still short after that single extension,
    Q018 goes to **DEFERRED** (`research/questions/DEFERRED.md`, with the measured counts) rather than
    running under-powered. There is no second extension and no gate is reduced. A gate shortfall is
    never an INCONCLUSIVE verdict for P1 or P3.
  - **After the extension, P2 and/or P4 still short while P1 and P3 are met:** that endpoint is
    reported **INCONCLUSIVE (floor)** with its counts and no point estimate; the question still runs
    on the endpoints that meet their gates, and **BH runs across m = 4 regardless**, so no surviving
    endpoint's bar is lowered (Q009 precedent).
  - **What §2's payload price-scale screen may do to these dates.** The screen removes picks, and
    removes a *night* only where every eligible 80–90 pick on it (or every LOW, or every HIGH) is a
    scale-mismatch row; measured sealed incidence is 3.4% of picks. It can therefore only **slow**
    accrual, never speed it. The dates are **not** re-projected downward for it now and are **not**
    moved in on any account; if it bites, the shortfall fires the single DP-13 extension on `eval.py`'s
    measured counts, exactly as a slow tape would. R3 measures the screened rates for the record.
  - **Nothing weakens.** No floor is lowered to hit a date, and a short count never licenses falling
    back to a descriptive endpoint as a verdict.
- **Freeze discipline (DP-23; routed request R2 — due at the decision date, not a blocker for lock).**
  `manifest_v001` / `manifest_prices_v001` supply definitions, exclusion criteria and run-rates only.
  The population enters through successor freezes — **`manifest_v00N` (selections, same SQL, same
  exclusion criterion) covering pick nights 2026-09-14 .. 2027-03-31** (.. 2027-05-12 if the DP-13
  extension fires) and **`manifest_prices_v00N`** with five scope requirements this question cannot
  do without: (i) daily bars for **every candidate symbol, published and unpublished** (B2's control
  rows need their own opens and forward bars), (ii) through **60 forward sessions beyond the last pick
  night**, i.e. ≈ 2027-06-25 (≈ 2027-08-09 extended), (iii) **hourly bars scoped to at least the
  published-pick symbols**, as `manifest_prices_v001` was — needed only for the descriptive stop
  sensitivity and `E_AH`, so a narrower hourly scope costs a secondary, never a primary, and the
  report must say so if it changes; **(iv)** a **successor exclusions file `exclusions_v00N`** issued
  with the selection freeze, applying the **identical three criteria** to the post-lock nights and
  **add-only** (DECISIONS item 4, §2); **(v)** counts, alongside the freeze, of the in-window picks
  failing §2's **payload price-scale screen**, by symbol, band and month, with any night losing > 25%
  of its otherwise-eligible picks flagged — a rising incidence is a platform issue (a PI filing
  distinct from PI-003), never a reason to relax the screen. **DP-50(a)/(b) apply to this window in
  full:** the desk's database is production, so any platform repair that rewrites
  `sas_candidates.public_payload_json`, `best_timeframe`, the lane-plan writer **including its model
  or provider version** (`83b571d`, 2026-07-09, "upgrading agents to gpt 5.6", shows such an upgrade
  landing on `ai_agents/principal_agent.py` as an ordinary commit; a model change moves lane-plan
  generation even against an identical prompt, and whether that commit touched `:546-554` / `:897-911`
  could not be inspected — flagged, not asserted), `_enforce_ladder_monotonic`, `BAND_EXITS` or the
  publication predicate between the lock and the decision pass changes this question's feature
  mid-window; it gets a dated `DATA_NOTES.md` entry, the column is treated as **two features** split
  at the ship date (the DP-06 pattern), and the fix brief names the constraint against this locked
  PREREG before it is written. The DP-50(a) sweep at freeze time must also **confirm explicitly, even
  when the answer is "none",** that no new cross-lane ladder enforcement, publication-floor or
  `best_timeframe` change shipped **inside** 2026-09-14 .. 2027-03-31 — the 2026-07-06 split is a fact
  about the sealed period, not this window. `eval.py` takes the window start and end, the manifest
  paths, **both exclusions-file paths** and the output directory as inputs — **no hard-coded dates,
  manifest names or paths** — so the byte-identical script serves both runs, and it records every
  sha256.
- Sub-cells (LOW / HIGH / ELITE / REF; bull / bear; tape stratum; regime label; `atr_pct` tercile;
  lane-distance tercile; month) are reported only where they clear **20 contributing nights**. REF is
  SUPPRESSED (structural); bear cells are expected to be SUPPRESSED (bear-contributing nights run at
  ≈ 0.157 per session — BACKLOG H-062); ELITE's print-or-suppress status is decided at the decision
  pass on `eval.py`'s own count.

## 6. Test window, split and stratification

- **Test window: prospective only — pick nights ≥ 2026-09-14**, the first session after this file's
  lock commit, through the window end in §5.
  *Justification (one sentence): the sealed period has already been read for this hypothesis.* The
  weekly snapshot of 2026-09-12 ranked the three lanes on Jun–Aug outcomes and wrote the ranking into
  the BACKLOG line for H-051 itself ("in Jun–Aug the short lane was the weakest on T+20 next-open
  return … swing +1.09% … long +0.13%", plus the by-lane share of picks whose L1 was already passed at
  the open), and the desk's standing finding list already carries "short DTE underperforms"
  (CLAUDE.md). A PREREG built on 2026-06-01..2026-09-10 would be testing a lane ordering that has been
  seen, so those nights are **not used for any primary**, and the sealed-period version of every
  primary is printed **only** as an explicitly labelled **post-hoc descriptive panel** that enters no
  verdict, no half, no stratum test and no q (§7, §8).
  **The sealed panel is split at 2026-07-06 and the two halves are never blended** (DECISIONS item 9a;
  `DATA_NOTES.md` 2026-09-13, read at its stricter limb — the alternative "state that it blends two
  mechanisms" is **not** taken). Sub-panel **A = 2026-06-01 .. 2026-07-03**, before `5fa3db4` shipped
  `_enforce_ladder_monotonic`, where there is no cross-lane re-sort at all and **25.71% (36/140)** of
  eligible ladders are non-monotonic; sub-panel **B = 2026-07-07 .. 2026-09-10**, after the ship,
  where the measured share is **0.00% (0/355)**. 2026-07-06 is itself an excluded night in
  `exclusions_v003`, so the boundary needs no tie-break. The 2026-07-07 and 2026-07-08 nights in
  sub-panel B are additionally flagged as the last nights before `83b571d` (2026-07-09) upgraded the
  lane-plan writer's model. Each sub-panel carries §2's payload price-scale screen, is SUPPRESSED
  below 20 contributing nights, and — unchanged — enters **no** verdict, no half, no stratum test and
  no q. **The primary window lies entirely after every one of these ship dates**, so no split falls
  inside it and all four primaries are measured on a single feature regime.
  *What is not contaminated:* the snapshot grouped **different picks** by their assigned
  `best_timeframe` and ranked them on **fixed-horizon return**; this question grades **the same pick
  under all three printed plans** on the path objective. The quantities differ — that is why the
  question is registrable at all — but the direction of "which horizon looked better" has been seen,
  and the blind window is the only honest answer to that (DECISIONS item 1, DEFAULTED under DP-43).
- **Catalyst-layer regime change:** the window sits entirely after the 2026-06-01 fix (platform commit
  69ef05f) — DP-06, no split needed.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing pick-night date **within the post-lock window**; Half B = after. The sealed panel is
  never a half.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7). The whole
    window is after that date, so the point-in-time label is knowledge-time-legal here: used only for
    `regime_version = 'v1.2'` rows written the same evening per their declared availability; a
    later-posted row is treated as missing and the night is stratified by the SPY proxy only, flagged.
  - Primary tape stratum for every pick night, trailing and legal at 16:05 ET: `tape_t` = sign of
    SPY's trailing 20-session return × tercile of SPY's trailing 20-session realized volatility, from
    SPY bars dated ≤ t in `prices_daily_split`. **Tercile cut points are expanding-window** (for night
    t, computed from every session 2026-03-02..t), so no later night's data sets an earlier night's
    stratum. Cells < 20 contributing nights SUPPRESSED.
  - Because the long lane spans 60 sessions, a night's tape stratum labels the **entry**, not the
    holding period; the report says so and prints the SPY path across each stratum's nights. This
    matters more here than in most questions, because the contrast between lanes *is* a contrast
    between exposures of different length (threat 1).
- **Knowledge time (rule 14) — every input declared. Q018 needs no rule-14 exception and requests none
  (DP-05 untouched; DP-41 respected).** All three plans are fully specified at 16:05 ET on the pick
  night; band, levels, ATR, direction and every stratum come from the pick night or earlier; no later
  quantity classifies, filters, matches or stratifies any pick. Fills, touches and window closes are
  **execution and outcome measurement**, the status Q007 §6.1, Q011 §6 and Q012 §6 give them.

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `overall_score`, `dominant_direction` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) | eligibility, band |
  | `best_timeframe` | `sas_candidates` | pick night, 16:05 ET | B3 arm (descriptive) |
  | day / swing / long lane plans: targets, entry, stop, invalidation | `sas_candidates.public_payload_json.lane_plans` | written during the nightly run before `finished_at` (`services/super_agent_select_service.py:155-161`) | the three plans; stop/entry descriptive only |
  | payload lane levels vs `C_t` / ATR14 (the §2 price-scale screen) | `sas_candidates.public_payload_json` + `prices_daily_split` bars ≤ t | pick night, 16:05 ET | **eligibility** |
  | lane windows 20 / 40 / 60 | `services/sas_conviction_card.py:194` | platform constant at the pick date | each plan's clock |
  | `outcome_target_invalid` (audit only) | `sas_candidates` | set at publication for new rows | exclusion |
  | control-candidate pool (non-published rows that night) | `sas_candidates` | pick night, 16:05 ET | B2 |
  | `C_t`, ATR14, beta60, runup20, level ATR distances | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | distances, matching, denominators |
  | SPY tape (trailing return, trailing vol, expanding terciles) | `prices_daily_split`, SPY bars ≤ t | pick-night close | stratum |
  | regime label (v1.2, same-evening rows only) | `market_regime_daily` | pick night, 16:05 ET | stratum |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion; `E_AH` clock (sensitivity) |
  | session t+1 open; sessions t+1..t+60 bars; hourly bars | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **execution and outcome only** |

  **What `eval.py` must enforce:** the eligible-pick set — **including §2's payload price-scale screen,
  which is computed from the payload and `prices_daily_split` bars dated ≤ t and therefore belongs to
  this step** — all three plans' parameters and every stratum label are computed and written to a
  frozen per-pick table **before any session t+1 or later bar is loaded**; the run fails if any
  t+1-or-later field is referenced in eligibility, band assignment, matching or stratification. This
  is also why the alternative treatment of a target at or through `O_1` (drop the pick) is a
  **post-hoc sensitivity and never an eligibility rule**: it would filter the denominator on a session
  t+1 price, which rule 14 forbids and which DP-41 would not grant an exception for (DECISIONS item 3). `sas_selection_excursion` / `outcome_*` / `level_hit_*` columns are
  never inputs (calendar windows, close basis, recomputed weeks later — `services/sas_excursion.py:8-18`,
  `:336-354`); the ladder is read from `public_payload_json` directly.
  `uoa_symbol_daily.fwd_return_*` is **banned** (the May–June freeze is not fixed — FREEZE_v001 §5).

## 7. Multiple testing

- **Within the question:** **BH across m = 4** — P1, P2, P3, P4 — at q ≤ 0.10; the verdict uses q.
  **m = 4 in every branch**: an endpoint short of its floor still has its p computed and included, so
  no surviving endpoint's bar is lowered (Q009 precedent), and m is fixed at lock. **P3 = P1 + P2 by
  construction** and the four tests are positively dependent; BH under positive dependence is
  conservative, and the dependence is disclosed rather than exploited — no "two of the three contrasts
  agreed" is ever counted as two independent confirmations (§8's ranking rule needs *both* of a lane's
  contrasts precisely because they are not independent evidence of the same thing).
- **Across the family: F6 Exits and execution.** F6 holds H-050, H-051, H-052, H-032 and H-066.
  **The F6 correction set, computed at the decision pass over the F6 primaries locked by then:**
  **Q003 (H-052, 2) + Q009 (H-032, 2) + Q012 (H-066, 3) + Q015's 2 F6-companion primaries + Q018
  (H-051, 4) + Q019 (H-050, 2) = 15**; **Q010 is excluded** as Q009's prospective replication, not a
  second F6 question, and H-051 is counted **once**, in F6. Q003 files itself in F6 (its header and
  §7) and Q019 is locked in this same desk cycle with its own §7 already counting Q018's 4, so the
  count is stated symmetrically. **m never falls below 15** — the set may grow as later F6 questions
  lock, never shrink (DP-29, DECISIONS item 11).
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q012 (F6, H-066):** its Plan R (exit at the first L1/L2 touch, 5-session cap, then **redeploy**)
    is the day lane's neighbourhood without a lane frame, and its Plan H is the full six-level
    committed scale-out. Q018 holds capital idle after a lane goes flat and tests **which lane**, not
    **what to do with the freed capital**. The two are **adjacent readings of one idea — that hold
    length should be chosen deliberately — and must never be presented or counted as two
    confirmations**; the Reporter cross-references, and any §9 line from Q018 that touches capital
    turnover must cite Q012's answer rather than assert one.
  - **Q015 (F7, F6 companion):** exit-at-the-L3-touch versus hold-through in the 85–90 band — the same
    band cut, a different axis (when to exit inside one lane, not which lane). Not independent
    evidence of a band gradient; the Reporter reads P4 and Q015's band contrast together.
  - **Q009 / Q010 (F6):** own the printed stop as an exit. Q018's stop arm is descriptive (DP-02) and
    is never a second reading of the whipsaw result.
  - **Q019 (F6, H-050):** owns the Conviction Monitor's EXIT flag as an exit trigger — a signal
    arriving *after* the pick night on a position already held. Q018 chooses among three plans fixed
    at the pick night and reads no post-night signal; the two share the F6 correction set (m = 15) and
    nothing else, and neither is evidence for the other.
  - **Q006 (F1) / Q002 (F7):** own the per-level picks-vs-control touch profile and speed to target.
    Q018's per-lane touch rates and sessions-to-touch are **descriptive** and re-decide nothing.
  - **Q004 (F7) / Q011 (F7):** own the entry basis. Q018 holds the entry fixed at `O_1` for all three
    lanes, so any entry effect differences out of every primary.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1`, `m2`, `m3`, `m4` are night-averaged contrasts in **ATR per trade**, one trade = one unit of
capital in one pick under one lane's plan.

**MPE: 0.25 ATR per trade on P1, P2 and P3** (DP-10, DP-44 — the standing number for a per-trade
ATR-denominated endpoint, not re-argued here); **0.50 ATR per trade on P4**, twice the standing value,
because P4 is a difference of differences on the thinner both-band nights (§4; DP-10 permits a larger
value with a stated reason and never a smaller one). No MPE is invented in money units and none is
asked (DP-44). All four are **two-sided**: no lane is presumed to win, and a result beyond MPE in
either sign is a finding with that sign.

Per endpoint (two-sided; the verdict carries its sign):

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. **contributing nights ≥ 80** for that endpoint (P4 counts both-band nights) **and ≥ 30 dated
     after the lock commit**, on measured counts, **and ≥ 20 contributing nights for any sub-cell that
     is reported** (DP-21) — a sub-cell below floor is **SUPPRESSED** (counts only) and does **not by
     itself** make the endpoint INCONCLUSIVE; rule 7's protection lives in clauses 5 and 6;
  2. `|m| >` that endpoint's MPE — **`|m1|, |m2|, |m3| > 0.25` ATR; `|m4| > 0.50` ATR**;
  3. block-bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 **within the question (m = 4) and within F6** (§7; **m = 15** at lock, recomputed at
     the decision pass over the F6 primaries locked by then and never below 15);
  5. the point estimate has the **same sign in both halves** of the post-lock window, and neither half
     is beyond MPE in the opposite sign;
  6. no tape stratum with ≥ 20 contributing nights is beyond MPE in the opposite sign.
- **Naming a best lane (the composite claim H-051 actually makes).** A lane is declared **best for
  80–90** only if **both** of its pairwise contrasts against the other two lanes are CONFIRMED in its
  favour: long requires `m3 > 0` and `m2 > 0`, both CONFIRMED; swing requires `m1 > 0` and `m2 < 0`,
  both CONFIRMED; day requires `m1 < 0` and `m3 < 0`, both CONFIRMED. **One winning contrast is not a
  winning lane** and is reported as exactly what it is: a two-lane comparison.
- **NULL:** floors met **and** 95% CI includes 0 **and** `|m| < MPE`. "Which lane's plan you trade is
  worth less than a quarter of an ATR per trade" is a real finding — it kills a per-band lane rule,
  says the three LLM-authored plans are not meaningfully different in the way the prompt intends, and
  is ledgered with the same care as a positive.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, a tape stratum with ≥ 20 contributing
  nights beyond MPE in the opposite sign, `0 < |m| ≤ MPE` with the CI excluding 0 ("real but below
  MPE", rule 6), or CI including 0 with `|m| ≥ MPE`. **A floor shortfall on any of P1–P4 first fires
  the single DP-13 extension** (§5). **After** the extension: a shortfall on **P2 or P4** is reported
  **INCONCLUSIVE (floor)** with counts only, while a shortfall on **P1 or P3** sends the question to
  **DEFERRED** and is **not** an INCONCLUSIVE verdict. No gate is reduced at either step.
- **Clause 7 — the capital-time disclosure.** Any endpoint that CONFIRMS in favour of a **longer**
  lane is reported in the same sentence as its **ATR per committed session** (`r/20`, `r/40`, `r/60`)
  and its committed-session counts. Where the per-trade ranking and the per-committed-session ranking
  disagree, the verdict stands as measured **and** the report states, in its first paragraph, that the
  longer lane wins per trade and loses per unit of capital-time, with the cross-reference to Q012.
  This is a binding reporting rule, not a second test.
- **Clause 8 — what may be *claimed*, as opposed to what is CONFIRMED.** The matched control (B2)
  carries the identical ATR distances and the identical windows with none of the selection. A
  **subscriber-facing** statement that VolatilX picks reward a particular lane requires, beyond the
  clauses above, that the **picks-minus-control** difference-in-differences on the confirming contrast
  exceeds **0.50 ATR** with a block-bootstrap 95% CI excluding 0 (raw p printed; this gates wording,
  not the verdict). If the control shows the same lane ordering, the finding is **a fact about
  horizons and target distances in this tape, not a selection edge**: an internal execution rule may
  still follow (it is still Haci's money), but the report must say so in its first sentence and no
  marketing claim may be built on it. This mirrors Q012's P3 clause.
- **The sealed descriptive panel never carries a verdict, and its two sub-panels are never blended.**
  The 2026-06-01..2026-09-10 version of every primary is printed only as the explicitly labelled
  post-hoc panel of §6, in **two** sub-panels split at 2026-07-06 — **A** = 2026-06-01..2026-07-03
  (pre-`5fa3db4`, 25.71% non-monotonic ladders) and **B** = 2026-07-07..2026-09-10 (post-ship, 0.00%)
  — each carrying §2's price-scale screen, each SUPPRESSED below 20 contributing nights, and a single
  blended sealed figure is **never** printed. No clause above is evaluated on either sub-panel: they
  enter no verdict, no half, no stratum test and no q, and no §9 line may cite them.
- **ELITE (90+) and REF (<80) never carry a verdict here** (§1, §2, DP-43). Any statement about them
  is descriptive, printed only if `eval.py` measures ≥ 20 contributing nights for that cell at the
  decision pass and SUPPRESSED otherwise. **BH stays at m = 4** in either case.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run **by design** — every contributing night is
  dated after the lock commit (§5, §6), so DP-24's 30 is satisfied by construction and DP-31 does not
  apply. It still requires the confirming endpoint to meet every clause above on data frozen in the
  successor manifests and never inspected earlier, under the unmodified `eval.py`. No subscriber-facing
  statement before that (rule 10); even then the basis is NON_QUOTABLE until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform prints **three lane plans per pick** and a single `best_timeframe` pill
(`routers/super_agent_select.py:400`, `:449`; `templates/ai_picks.html:2549`), grades the six levels
over 20 / 40 / 60 sessions by lane (`services/sas_conviction_card.py:194`), and publishes **one**
committed scale-out per score band that spans all six levels at once (`BAND_EXITS`,
`scripts/generate_sas_trading_guide.py:89-95`) — a strategist ruling
(`docs/SAS_EXIT_SCHEDULE_L4TRIM_RULING.md`, 2026-07-08), not a measured result. Nothing anywhere
measures what a unit of capital earns under each lane's plan, per band, so nothing today tells a
subscriber which of the three printed plans to trade.

Rules below fire only where §8 licenses one, and only after PROSPECTIVELY_CONFIRMED for anything
subscriber-facing (rule 10):

- **A lane is declared best for 80–90 (both its contrasts CONFIRMED):** a Manual Trading Guide line —
  "for a pick scoring 80–90, trade the <lane> plan" — printed with the measured ATR per trade, the ATR
  per committed session, the committed-session count and the control-adjusted figure beside it.
  Brief: a **flag-off** `recommended_lane` block on the pick card and in the lane payload that marks
  the measured lane for the band, with the existing three-lane display and the `best_timeframe` pill
  unchanged until the flag flips. Ship flag-off with a byte-identical checksum on the old path; shadow
  ≥ 20 trading days (rule 11). **DP-49:** every check that brief hands the **coding agent** must be
  satisfiable from the platform repo alone — the test suite, a pure-function import, `git show --stat`,
  a file diff; anything that reads or writes a table belongs in the brief's verification section,
  addressed to the Data Steward on `$RESEARCH_DB_URL`, or to Haci where a write is required, and a
  "prove file X did not change" check is written as the diff that proves it, never as "run X twice and
  compare".
- **P4 CONFIRMED as well:** the guide line becomes band-dependent inside 80–90 ("80–85 → lane X,
  85–90 → lane Y"), stated only for the two bands measured, and a brief proposes that the conviction
  card's per-band block name the lane rather than only the scale-out.
- **P4 CONFIRMED with the pairwise contrasts NULL:** the lanes are not different on average but the
  *band* changes which one to prefer — reported as a conditional rule only, with both bands' point
  estimates printed, and no single-lane headline.
- **All four NULL:** no change to any lane rule, and a real finding is ledgered: the three
  LLM-authored plans, which the prompt asks to be "meaningfully different"
  (`ai_agents/principal_agent.py:546-548`), are not meaningfully different in money at this size. That
  goes to the Red Team as a candidate platform issue about lane-plan generation and to
  `PLATFORM_ISSUES.md` (DP-07), never as a research finding about the picks. **DP-50(b): that PI entry
  must itself name the in-flight constraint** — a repair to the lane-plan writer
  (`ai_agents/principal_agent.py:546-554`, `:897-911`, **including a model or provider version
  change**), to `_enforce_ladder_monotonic` (`services/super_agent_select_service.py:195-215`), to
  `best_timeframe` or to the publication predicate is **flag-off until Q018's decision date** (the
  PI-011 / Q010 pattern), and if it ships inside the window anyway it takes a dated `DATA_NOTES.md`
  entry and the column becomes **two features split at the ship date** (DP-06 pattern, DP-50(a)).
- **Clause 8 unmet (the control shows the same ordering):** `playbook/` only, no subscriber-facing
  claim, and the report leads with "this is a horizon-and-distance effect available on comparable
  stocks, not a selection edge".
- **Not licensed by any outcome here:** anything about the 90+ band or `<80`; any statement about
  stops as exits (Q009 / Q010); any statement about redeploying freed capital (Q012); and any option
  structure — the desk holds no option prices (`research/questions/DEFERRED.md`, ENHANCEMENTS EN-011),
  and a 20-session plan and a 60-session plan have very different option P&L for the same stock path.
- Owner: implementer. Shadow ≥ 20 trading days before any flip (rule 11).

## 10. Known threats to validity (registrar's own list)

1. **A longer window is more exposure, and a trending tape pays for exposure.** The long lane holds
   three times the day lane's session count, so in a one-way tape "long wins" may be nothing but
   drift. Mitigations, all pre-specified: **B2** runs the identical three plans on distance-matched
   non-published candidates, where the same mechanical advantage appears on both sides, and clause 8
   binds any claim to that comparison; tape strata are reported; ATR per committed session is printed
   beside every primary; the window deliberately spans two calendar quarters.
2. **"Lane" is partly "distance" — and in this window it is *entirely* a matter of ordered distance.**
   Lane targets are LLM-authored with no ATR scaling (`ai_agents/principal_agent.py:546-554`; fallback
   0.5% / 1.0% steps at `:897-911`), and `_enforce_ladder_monotonic`
   (`services/super_agent_select_service.py:195-215`) re-sorts the flattened ladder across lanes
   whenever it is not price-monotonic. The desk's old "historically ~28%" figure is **struck**: it is
   **two regimes, not one** — **25.71% (36/140)** non-monotonic before `5fa3db4` shipped on 2026-07-06
   and **0.00% (0/355)** on and after (`DATA_NOTES.md` 2026-09-13; `STEWARD_Q018_exposure.md` §2) —
   and **the primary window lies entirely in the post-ship regime**. So "the share of payloads
   re-sorted" is **not an available in-window mitigation**: every published ladder here is cross-lane
   monotonic **by construction**, and the pre-re-sort ladder is **not recoverable** from the frozen
   payload. The threat is therefore **stronger**, not weaker, than the draft assumed: in this window
   "day" *is* the two nearest levels, "swing" the middle pair and "long" the two furthest, for **every**
   pick, by code — measured medians 0.367 / 0.593 ATR (day t1/t2), 1.788 / 3.334 (swing), 4.120 /
   6.367 (long), with swing t2 ≥ long t1 on 59.62% of picks. What remains: the per-lane ATR-distance
   distribution, the lane-distance tercile cells, a per-pick cross-lane ordering **verification** on
   the window's own payloads (expected 0% non-monotonic), and above all **B2**, which inherits the
   identical ATR distances and the identical windows with none of the selection, so the control
   contrast *is* the distance-plus-horizon null, and clause 8 binds any claim to it. A CONFIRMED result
   is a statement about **nearest / middle / furthest target pairs on three different clocks, as the
   platform prints them** — which is what a subscriber trades — and the report must not restate it as
   a claim about horizons in general.
3. **No stop, over sixty sessions.** DP-02 forbids assuming stops as exits, so the long-lane arm rides
   drawdowns a real trader would not. MAE, counter-direction touches and the lane's own printed stop
   and invalidation touch rates are printed, and the stop-exit version is reported as a descriptive
   sensitivity (DP-27 ordering) that decides nothing. Any §9 line must say the result is stop-free.
4. **Per trade is not per unit of capital-time.** A day plan that finishes in four sessions frees
   capital this question leaves idle at zero. Clause 7 forces the disclosure and Q012 owns the
   redeploy question; a guide line that hides the distinction is forbidden by §9.
5. **The three arms are nearly perfectly correlated.** One pick, one entry, three overlapping paths:
   the contrasts are tight but the four endpoints are dependent (P3 = P1 + P2). BH is conservative
   under this dependence, §7 discloses it, and §8's ranking rule requires two contrasts precisely
   because they are not independent evidence.
6. **Sixty-session windows overlap across adjacent nights**, so any independence assumption overstates
   precision. Block length is fixed at 20 sessions before any result, and the date-clustered CI is
   printed alongside.
7. **The sealed period has been read for this hypothesis** (weekly 2026-09-12 §4; BACKLOG H-051; the
   standing "short DTE underperforms" finding). The primary window therefore starts after the lock and
   the sealed panel is labelled post-hoc, is split at 2026-07-06 into two sub-panels that are never
   blended, and enters nothing (§6, §8; DECISIONS item 1). Residual exposure: the
   registrar knew, when choosing endpoints, that short horizons had looked weaker on a different
   metric — which is why no sign is presumed anywhere in §8 and why every contrast is two-sided.
8. **HIGH is thin** — 1.7 eligible picks per contributing night and only 62.7% of sessions carry one
   (`STEWARD_Q012_exposure.md` §7) — so P4 is the least precise endpoint, is the one that sets the
   window, and is the one most likely to end INCONCLUSIVE (floor). That cost is accepted rather than
   priced away by dropping the band half of H-051 (DP-43).
9. **Bear picks are rare** (≈ 0.157 contributing nights per session, BACKLOG H-062) and their lane
   plans are sell setups; the bull/bear stratum's bear cell is expected to be SUPPRESSED, so the
   verdict will in practice describe bullish picks. The report says so.
10. **A mid-window platform change would split the feature.** DP-50(a)/(b): the desk reads production,
    so a repair to the lane-plan writer — **including a change to its model or provider version**, not
    only to its prompt or logic; `83b571d` (2026-07-09, "upgrading agents to gpt 5.6") shows such an
    upgrade landing as an ordinary commit on `ai_agents/principal_agent.py`, and a model change can
    move lane-plan generation even against an identical prompt — or to `_enforce_ladder_monotonic`,
    to `best_timeframe`,
    to the publication predicate or to `BAND_EXITS`, shipped between the lock and the decision pass,
    rewrites what the arms mean. The check is mandatory before any such brief is written, the change
    gets a dated `DATA_NOTES.md` entry, and the column is then two features split at the ship date
    (DP-06 pattern). The DP-50(a) sweep at freeze time must say so **explicitly even when the answer
    is "none"** (§5 R2). Open Red Team item: confirm whether `:546-554` / `:897-911` actually changed
    on `83b571d` — `git show` / `git diff` were blocked in the Steward's session, so it is flagged,
    not asserted.
11. **`best_timeframe` might have been degenerate — measured, it is not.** On the 495 eligible 80–90
    picks it runs **short 343 / swing 97 / long 55**, with all three lanes present in both bands and
    every month (`STEWARD_Q018_exposure.md` §1). It is **skewed** short, not degenerate, so B3 remains
    an interpretable "follow the platform" arm — and it stays **descriptive** regardless, because
    H-051's claim is about the lanes themselves.
12. **Matching on three features may not span selection** (Q006 threat 1). Post-match standardized
    mean differences are printed for every control set, and clause 8's requirement is a claim gate,
    not a verdict gate, partly because of this.
13. **Null-ladder denominator and the six-level requirement** remove **16 of 541 published rows
    (3.0%)** on the measured funnel, with a further 8 removed by the wrong-side-of-`C_t` and
    `outcome_target_invalid` tests — **24 in all (4.4%)** (`STEWARD_Q018_exposure.md` headline) —
    small, but the funnel is printed with the verdict, reason code by reason code, and the
    2026-06-02-style all-lanes-missing night is flagged if it recurs.
14. **Unfillable targets are concentrated in the day lane** by construction (the nearest levels are
    the ones an overnight gap passes), and this is now **measured, not expected**: on the sealed
    population, **≥ 1 lane target at or through the session t+1 open occurs on 14.14% (70/495) of
    picks in the day lane, 2.02% in the swing lane and 0.00% in the long lane**, with HIGH 13.70% and
    LOW 14.22% on the day lane; excluding the 17 price-scale-mismatch rows moves the day figure to
    14.64%, so the finding is **not** an artefact of the scale issue (`STEWARD_Q018_exposure.md` §3).
    The chosen treatment rides that half to the lane's window close (§4); the alternative — dropping
    the pick — is printed as a named sensitivity (DECISIONS item 3) that removes **≈ 14% of picks**,
    is reported with that count, and can never be an eligibility rule (§6, rule 14). The per-lane
    unfillable counts are printed with every primary.
15. **The platform's printed lane levels are not always on the split-adjusted price scale.** For some
    symbols the payload's `entry` / `stop` / `targets` / `invalidation` are built from a raw,
    non-split-adjusted reference while `C_t` and ATR come from `prices_daily_split` (`DATA_NOTES.md`
    2026-09-13; distinct from PI-003's `atr_pct` corruption). The wrong-side-of-`C_t` test does **not**
    catch it — a 2×–10× raw-scale bullish target still sits "above" a much smaller split-adjusted
    close — so it would pass eligibility while carrying a distance that was never tradeable. §2's
    price-scale screen is what catches it: such picks are **dropped and counted**, never rescaled.
    Measured sealed incidence **17 of 495 (3.4%)**, concentrated in **APH (14 of 14 picks, ~2.0×,
    systematic across the whole window)** with **KLAC 10.18×, CRWD 4.07×, MNST 2.02×** episodic. Those
    four are **not** asserted to be the complete list — no full sweep has been done — which is why the
    screen is a rule on the ratio and not a symbol blacklist, and why §5 R2(v) and R3 re-measure its
    incidence. A rising incidence is a platform issue (a PI filing distinct from PI-003), never a
    reason to relax the screen.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: **R2** (successor selection and price
freezes, DP-23, due at the 2027-07-12 decision date) and **R3** (counts-only recount of the three
run-rates with §2's price-scale screen applied). Both are **non-blocking for the lock**, decide no
endpoint, and can move the §5 dates **out, never in**.
