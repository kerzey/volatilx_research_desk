# Q029 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 8 items (+ 11 items decided or routed here: the two routed requests named in §5.3 / §5.4, the borrowed Q027 exposure basis, and eight the draft settles silently or leaves to `record`)
**`record` pass: 2026-09-14 by decision-maker (autonomous)**, on `research/reports/STEWARD_Q029_feasibility.md` (R1b, counts only) and on Q027's settled `DECISIONS.md` / `schedule.json` (R1, borrowed). Every ROUTED item those two settle is settled below; **nothing in this file is `_pending_`**. Seven rows are added (21–27) and nine corrections (7–15).

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14) — in scope.

## The `record` headline (2026-09-14, after R1b and Q027's R1)

**Q029 LOCKS, with the ablation limb alive: `m = 16`, not 10.**

**Gate 0 (item 17's trigger) did not fire, and the reading is stated rather than hedged.** R1b(d)
measures **84.77%** whole-freeze reconstruction from 2026-04-01 and **100.00%** on the
**2026-06-01..2026-09-10 segment — 68 of 68 nights, every night at or above 99%, zero exceptions**.
The shortfall is one mechanism, dated: rows before ~2026-05-11 carry an **8-key**
`score_details_json` with no `atr_elite_block_applied` and no GEX-missingness offset, and every
non-reconstructing row resolves to a residual of exactly **+5.00** — the desk's `fa70688` formula
applied to an engine two ships older. **The determination is made on the segment** (Correction 3,
DECIDED at `decide`, which already names Gate 0 as one of the "coverage and arithmetic facts" it
scopes; DP-06 / DP-50(a): the pre-v1.5 rows are a **different feature**, not a residual error). The
literal whole-freeze reading is **degenerate here** and is refused for a reason, not for convenience:
it would declare the limb unevaluable on rows that are outside the question's window, written by an
engine the question never reads, and **structurally absent from the prospective window, which is
post-v1.5 by construction**. Item 17's own reason — *an arithmetic the desk cannot reproduce cannot
carry a verdict* — is **satisfied** on the population `eval.py` will read, and the in-window gates
(≥ 99% per night, ≥ 95% whole-window, 0.05 tolerance, the 1% replay gate) are **unchanged and
un-relaxed**; the replay disagrees on **0.00%** of segment nights (the 12 discordant nights are all
April, all pre-dating the 2026-07-02 bear-lane split, all explained). **No PI is filed** (§17's PI
branch is not reached; the −7.00 residual tail is confined to the same partial-schema era and is a
formula-vintage artefact of the desk's rehearsal, not a platform defect — DP-07 not engaged).

**The register is closed. `m = 16`** — above the draft's expected 12–15, inside Correction 1's bound
of 21. **EVALUABLE ×3:** `flow_strength`, `technical_structure`, `gex_alignment` (ADDITION, weight
**12.0 measured**), `fundamental_quality` (REMOVAL side), `catalyst_event`. **`projection`: E3 only**
— its subscore is non-null on **62.74%** of segment rows and clears 70% in **no month measured**
(peak 65.11%), so E1/E2 are UNEVALUABLE; E3 is unaffected (the 70% clause binds E1/E2 and
ADDITION-E3 only). **`smart_money_confirmation`: DEAD ×3** (0.00% non-null everywhere, 0 distinct
values, flag False on all 102 nights, E3 ≡ 0 by mechanical identity). **No REMOVAL/ADDITION split
survives:** flow / technical / projection / catalyst are REMOVAL on 68 of 68 segment nights, gex is
ADDITION on 68 of 68, and `fundamental_quality`'s single ADDITION night (2026-06-02) projects to
**1.2 contributing nights** — UNEVALUABLE, not in `m` (item 16); that night is also the
`payload_disabled_runs` signature Q027 excludes whole. **`fundamental_quality` is a REMOVAL layer**,
contrary to the draft's "DEAD or ADDITION-only" expectation: `enable_fundamental_enrichment` measures
**True on 67 of the 68 segment nights**.

**Dates are Q027's, adopted whole and out only.** Q027's R1 measured **0.6761 contributing nights per
elapsed session** (48/71) against the **≥ 0.36** gate — **clear by 88%, both questions lock**.
**Window pick nights 2026-09-15..2027-03-05 (119 elapsed sessions) · decision Monday 2027-04-12 ·
single DP-13 extension to window end 2027-04-19 (session 149) decided Monday 2027-05-24 (hard stop) ·
then DEFERRED.** 6.9 and 8.3 months from a 2026-09-14 lock, inside DP-43's 12-month ceiling
(2027-09-14) — **no DEFERRED**. Every date moved **out** from the provisional 2027-03-08 / 2027-04-19,
because 0.6761 is slower than the borrowed 0.9538; the 0.9577 eligible-night proxy is **not** used for
any date. **Floor B binds where floor A binds — session 119** — because every limb of E3's
contributing-night rule measures at 100% on the segment (Gate 0 68/68; replay 0.00%; B4 control pool
min 39 ≥ 10). **Item 10 joins the DEFAULTED list** (the date moved out, as DP-43 requires).

**The near-miss pool's min of 0 costs nothing, and the reason is a distinction that had to be made
explicitly:** Correction 2's **≥ 10 distinct** floor is on **B4's distance-matched control pool**
(that night's eligible rows in neither slate — measured mean 51.8, **min 39**), **not** on **B3's
near-miss pool** (min 0, median 8, max 26). Read the other way it would strike roughly half the
nights and defer the question on a bookkeeping artefact. `k_{t,j} ≤ |near-miss pool|` by construction,
so B3's draw is **always feasible**; an empty pool forces `k = 0`, and item 7 already counts
identical-slate nights (`ΔE = 0`) as contributing. **Zero nights are lost** (Correction 12).

**BH, final:** within the question **`m` = 16**, fixed and never revised. **F1 = Q006 (2) + Q024 (6) +
Q025 (2) + Q029 (16) = 26.** **F2 companion on E1ⱼ/E2ⱼ = Q023 (2) + Q027 (2) + 2L = 10 → 14**, and the
**larger of the two q's decides**. The larger `m` is the **stricter** denominator for every endpoint in
the question.

**The suppression list is Q027's, transferred whole and closed** — same funnel, same population, same
window, same per-cell counts. **SUPPRESSED (8):** `tape_t` `up_low` / `down_high` / `up_high` /
`down_mid` / `down_low`, and the three `market_regime` labels absent from the measurement
(`bearish` / `neutral` / `risk_off`). **NOT suppressed:** `tape_t` `up_mid`, `market_regime`
`strongly_bullish` and `bullish`, all three `best_timeframe` cells (E1/E2 only), **bull-only and
bear-only**, published versus unpublished. §4.4's drafted expectations (bear-only and all six `tape_t`
cells suppressed) are **struck** — the registered rule is a measured count, not an expectation
(Correction 13). **No primary is demoted; no floor, gate, MPE or denominator was weakened anywhere in
this pass.**

## The headline (at `decide`, 2026-09-14 — kept as written, superseded above where R1b and Q027's R1 answer it)

**Q029 does not lock on its own measurement. It locks on Q027's.** §2.0 adopts Q027's population,
`d*_t`, entry, clock and contributing-night rule by reference, so the funnel is the same funnel and
the exposure count is the same count: **R1 is read from `research/reports/STEWARD_Q027_exposure.md`,
item (a), and is not re-routed.** Q027's lock-or-DEFER inequality — **≥ 0.36 contributing nights per
elapsed session**, DP-43's 12-month ceiling solved at a 2026-09-14 lock and re-solved at `record` if
the lock date moves — decides Q029 too: above it both lock, below it **both go to
`research/questions/DEFERRED.md` on the same measurement**. A second exposure request for an
identical funnel would be a second number for one quantity and is refused.

**What Q029 does route on its own is `m`.** R1b is a **counts-only, outcome-free feasibility**
request: which layers have usable variation, whether the ablation reconstructs the platform's own
arithmetic (Gate 0), whether an ablated slate ever differs from the published one, the GEX pre-v1.5
weight, the near-miss pool, and the DP-50 commit sweep including the v1.7 workstream. It fixes the
EVALUABLE / DEAD / UNEVALUABLE list and therefore `m`, at `record`, from counts, with no outcome in
view. **It is blocking for the lock** — not because it can move the decision date (it cannot) but
because `m`, the BH denominator, cannot be fixed after the numbers exist.

**All eight of the draft's own §11 items go the Registrar's way**, and four of them are tightened
rather than merely accepted. **One item is DEFAULTED** (#9, the prospective-only window start — the
same item and the same shape as Q027 DECISIONS #7; it is where this question spends Haci's waiting).
**Three are ROUTED** to the Data Steward: the borrowed Q027 R1 basis and its gate (#10, blocking for
lock, **already routed under Q027 — no new request**), R1b (#11, counts only, **blocking for `m` and
for the lock**), and R2 (#12, the shared successor freezes, **not** a blocker — DP-23). **Six
corrections** are listed for `apply`; every one of them tightens a clause and none weakens one.

**Rule 14: no exception is requested and none is needed.** Every ranking variable, every replay
input, every weight, every gate, every episode id and every stratum label is a 16:05 ET write on the
pick night; the session t+1 open is used only as a price and only as the entry; §6's table declares
each input. **DP-05 is untouched and DP-41 is not engaged.**

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | E3's MPE — ±5.0 pp or DP-20's doubling clause | DECIDED | **Option A — ±5.0 pp**, and the doubling clause's strictness is **kept as a blocking companion rather than as the MPE**. DP-20's own text licenses a *larger* MPE for "an endpoint with **no control** (a raw arm contrast)"; `ΔE*_{t,j}` has rule 5's distance-matched control inside it by construction (§3 B4), so the licence does not reach it on its face, and the six precedents that used 10.0 pp (Q007 P1, Q008 K1, Q012 P2, Q014 E1, Q022 E1, Q023 E1) each raised it for **independently estimated components or small independent cells** — a premise that fails here, where the two `E_t`'s are computed on the **same night, from slates overlapping on most members, against control sets drawn from the same pool at the same distance**. H-075 is also written with ±5.0 pp. **The tightening, which is where B's strictness goes:** §4.4's **added-minus-dropped decomposition** — the undiluted control-adjusted contrast of the picks the ablation adds against those it drops — becomes a **blocking companion** (a new §8 clause): on layers with **≥ 20 discordant contributing nights** it must carry the **same sign as `E3ⱼ`**, and a contrast beyond 10.0 pp in the **opposite** sign blocks a CONFIRMED. Below 20 discordant nights it prints counts only and §8 clause 9's lead-with-the-`k=0`-share rule already carries the narrowness. | **DP-20** (5.0 pp is the standing number; its larger-MPE clause is scoped to endpoints with no control), **DP-44** (touch-rate endpoints take DP-20), **DP-25** (units and cuts come from H-075 as written), **DP-45** — of the two readings, the strict half of B is kept as a blocker instead of choosing between them (the Q027 DECISIONS #2 / #6 construction); the reason for A is **not** that 10.0 pp would be hard to reach |
| 2 | The GEX addition weight | DECIDED | **Option A — the measured value.** `scoring_weights.gex_alignment` in the **last `sas_runs.config_json` dated before the v1.5 ship of 2026-05-14**, read by **R1b(c)** from the pinned `manifest_v001` freeze (never a live query). If **no** pre-2026-05-14 night in the freeze carries a non-zero value, the addition weight is **12.0** with the reallocation derivation printed verbatim in §2.3 (`+7 +3 +2 = 12`; `24+20+26+5+8+5 = 88`). If R1b returns **several** distinct non-zero values, the **last one dated before 2026-05-14** is registered and the others are printed. The `w ∈ {5, 12, 24}` curve stays a **descriptive companion that never decides** (§4.4), in every branch, including the fallback branch. **Settled at `record` (item 23): the measured value is 12.0** (last population config before the v1.5 ship, 2026-05-08; only 12.0 and 0.0 ever appear in the frozen history) — **the fallback branch did not fire and is struck** (Correction 9). | ground 3 — one defensible answer: the honest counterfactual for "GEX at its nominal weight" is the weight the engine actually gave it, and a measurement beats the registrar's arithmetic; **DP-50(c)** (the value comes from the pinned freeze, never a live query); **DP-26** (a convention fixed at lock, not derived from an outcome) |
| 3 | Ablation scope — weight-only or layer-removed-everywhere | DECIDED | **Option A — weight-only.** The weight vector varies; `cross_layer_bonus`, `conflict_penalty`, every subscore (including the ATR projection cap already baked into `projection_score`) and the **ATR-elite block decision** are held at their stored production values, with the block's cap re-applied exactly where `atr_elite_block_applied` is true. "Layer removed everywhere" stays a **printed sensitivity that never decides** (§4.4). A is the counterfactual a brief could actually ship (`scoring_weights[j] = 0`, §9); B mixes four edits into one number no implementation could act on, and §9's product rules would then rest on a change no one would make. | ground 3 — the counterfactual must be the change that can be implemented; **DP-26**; rule 11 (what ships is a flag-off weight change with a byte-identical checksum, which is exactly A's arithmetic) |
| 4 | The partial IC's status — primary or secondary | DECIDED | **Option A — `E2ⱼ` is a primary; three endpoints per evaluable layer; `m = 3L`.** It is the endpoint §9's demote-or-remove line rests on and the **contribution limb Q028 explicitly defers to this question**, so it is an endpoint that licenses a product change and it carries a q (rule 8). `m = 3L` is also the **larger BH denominator**, i.e. the stricter bar for every other endpoint in the question. | rule 8 (an endpoint that licenses a change is corrected, not exempted); **DP-40 / DP-45** — of two options differing in strictness, the stricter denominator; Q028 §8's own deferral of the contribution limb to H-075 |
| 5 | E3's denominator convention | DECIDED | **Option A — renormalized**, the platform's own arithmetic (`base = Σ score·w / Σ w`, `:1348`, with `completeness` and the weight-dependent missing-data penalty recomputed from `W'` by the identical formulas). The **fixed-denominator** version — `w_j` out of the numerator but not out of `avail_w` — is a **printed sensitivity** beside every E3 (§4.4), so §10 threat 2's "lose `j`" versus "lose `j` and up-weight the rest" stays separable without a second primary. | ground 3 — A is what setting a weight to zero does in production and B measures a state the engine cannot be put into; same ground as item 3; **DP-26** |
| 6 | Evaluability, and how `m` is fixed | DECIDED | **Option A — declared once at `record` from R1b's counts, then closed**, with four clauses that stop A becoming a way to shrink a denominator. **(i)** The declaration rests on **coverage and arithmetic facts only** (§4.3's 70% / 5-value / 50%-of-nights rule, Gate 0's rehearsal, the slate-change rate) and on **no outcome of any kind**. **(ii)** `m` is **fixed in every branch**: an EVALUABLE pair short of its floor at the decision pass still has its p computed and **stays in `m`** — dropping it would lower the bar for the survivors. **(iii)** A pair declared **DEAD or UNEVALUABLE at `record` is never added to `m` later**; if the successor freeze's own coverage counts show a layer that was dead on the sealed freeze carrying usable variation inside the window, it is reported as **`UNREGISTERED_LIVE`** — counts only, no verdict, no q — and named as a successor question. **(iv)** The R1b report is filed **before the lock commit**; a pair whose evaluability R1b cannot determine is **UNEVALUABLE**, not EVALUABLE (DP-45). Under B a single uncomputed layer's undefined statistic would fire DP-13 and then defer the whole question on a bookkeeping artefact. **Executed at `record`: `m` = 16, the register is closed** (item 22); clause (iv) did not fire — R1b determined every one of the 21 pairs. | ground 3 — a BH denominator must be fixed before the numbers exist (rule 8, rule 3); **DP-43** (the EVALUABLE / demotion determination is made at lock from counts, never afterwards); **DP-45** for clause (iv) |
| 7 | E3's night set | DECIDED | **Option A — every E3-contributing night, including the nights where the two slates are identical** (`ΔE = 0`), with the discordant-night decomposition printed beside it (§4.4) and §8 clause 9's requirement that a `k=0` share above 50% **lead the verdict sentence**. The decision-relevant quantity is what the *product's published slate* would have done, not what a treated subset did; B defines its population by the treatment, which is a post-treatment selection, and would need 80 **discordant** nights per layer. A is also the **diluting** choice — including `ΔE = 0` nights pulls every estimate toward zero. | ground 3 — B conditions the population on the treatment; **DP-45** (A is the option less likely to reach CONFIRMED); **DP-21** (the floor is not restructured to make a thinner population reach it) |
| 8 | The two modifiers (cross-layer bonus `:1078`, conflict penalty `:1116`) | DECIDED | **Option A — ablate both, report descriptively: no MPE, no q, no verdict, no §9 rule**, printed in every branch whatever they show (the anti-cherry-pick rule). **H-012 owns the conflict penalty as its own open F2 BACKLOG line**, and registering it here would test it twice and count it once — DP-29's failure mode exactly. A striking modifier split is a reason to **register H-012 as its own primary question**, and §9 already says so. | **DP-29** (an overlapping hypothesis is marked *merged into QNNN* or left to its owner, never double-counted); rule 8 (forking paths — two primaries no hypothesis has argued for); ground 3 — the modifiers are not layers and H-075 is about the seven layers |
| 9 | The window start (prospective-only) | **DEFAULTED** | **Pick nights ≥ 2026-09-15 only** — the first session after the lock commit, deliberately aligned to Q027 so one freeze, one exposure count and one maturity horizon serve both. The sealed stretch (2026-06-01..2026-08-12) is printed **once** as a labelled post-hoc panel, split at 2026-07-06, entering **no** verdict, no CI comparison, no half, no stratum test, no q and no §9 rule. The cost is that Q029 decides on **2027-04-12 instead of now** (written as 2027-03-08 at `decide`; item 10's measured rate moved it out). It is the most defensible default the desk has: the platform's own August layer audit (`docs/SAS_SCORING_RESEARCH_PLAN.md:53-67`) already printed **H-075's own statistic, per layer, with a verdict per layer**, on the sealed cohort, and the registrar read it while drafting. | **DP-43**; not taken: read the sealed nights, decides now, not blind |
| 10 | Exposure basis, the lock-or-DEFER gate, the window end and the decision date | **DEFAULTED (R-3)** — settled at `record`, Q027's R1 received | **LOCK, not DEFERRED.** Q027's measured contributing-night rate under its §2.5 complete definition is **0.6761 per elapsed session (48/71)** ≥ the **0.36** gate (re-solved at the actual lock date 2026-09-14, unchanged) — clear by 88%. **Window: pick nights 2026-09-15..2027-03-05 = 119 elapsed sessions**, adopted from Q027 **whole** (Floor A binds at ceil(80/0.6761) = session 119; Floor B — E3 — binds at the **same** session 119, see item 24; Floor C, DP-24's 30 post-lock nights, lands at session 45 = 2026-11-16 and is non-binding, satisfied by construction). **Decision date: Monday 2027-04-12** (window end + 20 sessions maturity = 2027-04-05, + one calendar week freeze margin, first Monday on or after, not a holiday). **Single DP-13 extension:** window end session 149 = **2027-04-19**, decided **Monday 2027-05-24**; still short there → `research/questions/DEFERRED.md`, no second pass. Every date moved **out** from the provisional 2027-03-08 → **2027-04-12** and 2027-04-19 → **2027-05-24**, because 0.6761 is **slower** than the borrowed 0.9538. The **0.9577 eligible-night proxy is not used for any date** — it extrapolates past the price freeze's own forward-bar horizon and would have pulled the decision in to ~2027-02-22; a faster rate could never have moved a date in. 6.9 / 8.3 months from lock, inside DP-43's 12-month ceiling (2027-09-14). **One freeze, one exposure count, one maturity horizon, one decision date, shared with Q027 — as §2.0 promised.** | **DP-43** (the window that reaches every floor, computed at `record` from the Steward's numbers; +30-session extension; > 12 months → DEFERRED, not engaged), **DP-45** (out only, never the shorter window, never the extrapolated rate), **DP-13**, **DP-21**, **DP-24**; Correction 5's inequality; `STEWARD_Q027_exposure.md` + Q027 `DECISIONS.md` item 8 / `schedule.json`. Not taken: the 0.9577 eligible-night proxy — decides ~2027-02-22 |
| 10a | *(superseded at `record`)* the routed form of item 10 | ROUTED → data-steward — **CLOSED, Q027's R1 delivered 2026-09-14; no second count was run** | waits on **Q027's R1**, read from **`research/reports/STEWARD_Q027_exposure.md`, request R1 item (a)** — the contributing-night rate per elapsed session under Q027 §2.5's complete definition. **No second exposure count is routed and none should be run**: Q029's E1/E2 funnel *is* Q027's funnel (§2.0). Settled at `record` on that one measurement: **≥ 0.36 contributing nights per elapsed session → both questions lock** and §5.5's dates are recomputed on the measured rate, **out only**; **< 0.36 → both go to `research/questions/DEFERRED.md`**, unregistered, on the same number. Three things are fixed now so none is argued with counts in view: the threshold is the **inequality** (DP-43's ceiling solved at the actual lock date, rounded up, re-solved at `record` if the lock date moves); the window end is the **later** of the E1/E2 and E3 floor projections (§5.2), moving **out** only; and a decision date landing on a market holiday moves **out** to the next Monday, never in. | — |
| 11 | `m`, the EVALUABLE / DEAD list, the GEX weight and the suppression list | ROUTED → data-steward — **CLOSED, R1b delivered 2026-09-14** (`research/reports/STEWARD_Q029_feasibility.md`); settled in items **21–26** below, all fixed at `record` and now closed | waits on **R1b** (§5.3), counts only, no outcome of any kind, measured on the pinned `manifest_v001` against `exclusions_v003.json` plus read-only `git log` / `git show` at `fa70688`. **Blocking for the lock**, because `m` is a BH denominator and cannot be fixed once the numbers exist (item 6). It decides `m`, the EVALUABLE / DEAD / UNEVALUABLE list, the REMOVAL / ADDITION split and its floor consequence (item 16), the GEX addition weight (item 2), whether E3 is evaluable at all (item 17) and the sub-cell suppression list (item 13). **It does not decide the lock gate; Q027's R1 does.** | — |
| 12 | Successor freezes | ROUTED → data-steward — **dates fixed at `record` from item 10, and they moved out**: pick nights **2026-09-15..2027-03-05**, daily bars through **2027-04-05** (t+20 of the last pick night) and ≥ 60 prior sessions before 2026-09-15, delivered before **Monday 2027-04-12**; the extension pair **only if** DP-13 fires — pick nights through **2027-04-19**, bars through **2027-05-17**, due before **Monday 2027-05-24**. The add-only successor exclusions file carries **four** criteria, Q027 item 11's fourth (`payload_disabled_runs`) included — adopted with the machinery (§2.0), forward-only, no v003 night removed. Re-issued in full under "Routed requests" | waits on **R2** (§5.4) — **one** pair built for Q027 and Q029 together: `manifest_v00N` (selections, every candidate row published and unpublished, **including `score_details_json` and `missing_data_json`**, plus `sas_runs.config_json` frozen **per night** and `market_regime_daily`) and `manifest_prices_v00N` (daily bars for every candidate symbol on every in-window night, **plus DP-23's hourly bars for published symbols** — Correction 4), with the add-only successor exclusions file. Due before the decision date; **not a blocker for lock** (DP-23). Dates follow item 10 and may move **out, never in**. | — |
| 13 | Demotion, and the sub-cell suppression list | DECIDED | **No primary is demotable after lock.** The EVALUABLE / DEAD / UNEVALUABLE determination and every demotion happen **once, at `record`, from R1b's counts** (item 6); a shortfall measured afterwards is a **floor failure** — the single DP-13 extension, then DEFERRED — **never** a demotion and **never** an INCONCLUSIVE verdict. **Sub-cells: the list is FIXED at lock**, revised **once** at `record` from R1b and Q027's R1 counts, then **closed** — a cell suppressed at lock **stays suppressed even if it clears 20 measured nights** at the decision pass, and a cell cleared at lock still needs ≥ 20 measured contributing nights to print. **Suppression restricts affirmative reporting only**: it never removes a blocker, never by itself makes an endpoint INCONCLUSIVE, and the halves, the monthly blocks, the bull-only version, the "mixed graded long" version, the binary-outcome IC, the 5-session companion, the placebo adjustment and item 1's added-minus-dropped blocker are **not** on the list and block at whatever count they have (item 1's blocker at its own ≥ 20-night floor). **The revision ran at `record` and the list is now closed (item 25):** eight cells suppressed — five `tape_t` cells and the three absent `market_regime` labels — everything else on the affirmative list at ≥ 20 measured nights. **No primary is demoted.** | **DP-43** (demotion decided at lock, never afterwards), **DP-21** (20 per cell, no floor moved in either direction); **Q027 DECISIONS #10 and Correction 2/3**, adopted with the machinery (§2.0); Q023 #9, Q022 #6 |
| 14 | Exclusions inside a window every night of which postdates the freeze | DECIDED | `eval.py` unions **`research/data/exclusions_v003.json`** (the newest file) with the **add-only successor exclusions file** issued with the successor selection freeze — the identical three lists (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs`), built by the identical criteria, covering nights after 2026-09-10. The successor file may only **add** nights; no night is ever removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be. DP-04 applies mechanically on top. Both paths are `eval.py` inputs — no hard-coded file name, no hard-coded date. | **DP-22** read as "one list, one set of criteria" — its "cite the newest file" clause presumes a sealed window and Q029's is entirely post-freeze; **Q027 DECISIONS #11**, Q023 #8, Q018 #4, same construction |
| 15 | A mid-window change to the weight vector or to the publication gates | DECIDED | **As drafted in §5.5, and deliberately wider than Q027's list.** A change to `scoring_weights`, the timeframe multipliers, the enrichment flags, `qualification_threshold`, the ATR-elite caps or the GEX-missingness offset makes `overall_score` and the ablation **two different experiments**: the window is **cut at the ship date**, the **post-ship** segment becomes the question's window with the whole §5.5 schedule recomputed from it — **out, never in**, subject to the same single extension and the same 12-month ceiling measured from the **original** lock — the pre-ship segment becomes a labelled descriptive panel entering no verdict, and if neither segment reaches the floors inside the ceiling Q029 is **DEFERRED**. **`publication_floor`, `bear_publish_threshold`, `max_output_cap` and `min_completeness` are split triggers here although Q027 DECISIONS #12 correctly treats them as non-splits there** — they change *which rows are published*, which is precisely the object `E3ⱼ` measures, as well as `d*_t`'s source cohort. **The window is cut whole, not per endpoint**: Q029 has one window, one freeze and one decision date shared with Q027, and splitting E3 from E1/E2 would give the question two schedules. **DP-50(b) runs the other way too:** any such platform change — **including any promotion of the v1.7 score** (`docs/SAS_SCORING_RESEARCH_PLAN.md` §7, Phase 5) — is **flag-off until 2027-04-12** (2027-05-24 if the extension fires; written as 2027-03-08 / 2027-04-19 at `decide`, moved out with item 10), checked before any fix brief is written; it is **one constraint shared with Q027**, on the same date, not two. **Confirmed at `record` on R1b(g): no split trigger is in view — commit sweep NONE since `fa70688`, v1.7 unshipped and unscheduled, every config change in the freeze more than two months before the window** (item 27). | **DP-06 / DP-50(a)** (a config change splits a column into two features at the ship date), **DP-50(b)** (ship timing checked against in-flight questions, the PI-011 / Q010 pattern), **DP-50(c)**; **DP-45** (a whole-window cut is the stricter of the two readings); Q027 DECISIONS #12, Q018 #9, Q022 #3 |
| 16 | The REMOVAL / ADDITION split — its scope, and what it does to the floors | DECIDED | **The split governs `E3ⱼ` only.** `E1ⱼ` and `E2ⱼ` are rank correlations of a **subscore**, which does not depend on the weight that subscore carries, so they are computed over **all** contributing nights regardless of the layer's effective weight, with the weight split reported as a **descriptive stratum** (Correction 1). For `E3ⱼ`, §2.3's per-night rule stands and the two sides are **never pooled** (the DP-06 pattern on a weight vector) — **but a side that R1b(b) projects below 80 contributing nights inside the window is declared UNEVALUABLE at `record`**, counts only, no verdict, **not in `m`**, exactly as a DEAD pair is, and the other side is that layer's E3 endpoint. Only sides that enter `m` can ever fire DP-13. Without this clause a layer whose nights split 50/50 would register two endpoints neither of which can reach 80, and the **whole question** would be deferred on an artefact of the weight census rather than on a measured shortfall. **Settled at `record` (item 23): no split survives** — six layers are one-sided on 68 of 68 segment nights, and `fundamental_quality`'s single ADDITION night projects to **1.2** contributing nights → **UNEVALUABLE, not in `m`**, its REMOVAL side carrying the layer's E3. | **DP-43** (an arm projected below its floor is demoted at lock from counts, never dropped afterwards); item 6's ground — declared from a coverage fact with no outcome in view; **DP-06** (two features are not pooled); ground 3 — an IC does not depend on the weight of the variable it ranks |
| 17 | What happens if the Gate-0 or slate-replay rehearsal fails before the lock | DECIDED | **Registered now, so it is not decided with counts in view.** If **R1b(d)**'s whole-freeze reconstruction rate is below **95%**, or **R1b(e)(i)**'s replay disagrees with the frozen published set on more than **1%** of slate rows, then **every `E3ⱼ` is UNEVALUABLE at `record`** — counts only, no verdict, not in `m` — and **Q029 locks as an IC-only question**: `m = 2L`, §1 and §9 state that the ablation limb is not measured, **no weight brief, no DECORATIVE / HARMFUL / CARRIES label and no §9 product rule follows**, and the per-layer register prints `E3 UNEVALUABLE` in all seven rows. In that branch a **PI is filed under DP-07** (the platform's own `overall_score` does not reconstruct from the components it stores, or its published slate does not reproduce from its own `_qualify_lane`), and **H-003's own mechanism goes to `research/questions/DEFERRED.md`** with the measured reconstruction rate named. Q029 is **not** deferred wholesale: E1 and E2 answer H-075's IC limb and H-076's contribution limb, and those are worth the wait on their own. Gate 0's thresholds are **never relaxed to make a pass succeed** (§2.4). **Settled at `record`, and the branch did NOT fire (item 21):** reconstruction is **100.00%** on the 2026-06-01..2026-09-10 segment (68/68 nights, each ≥ 99%) and replay disagreement is **0.00%** (0 nights above the 1% gate); the **84.77%** whole-freeze figure is a pre-v1.5 formula-vintage artefact (DP-06), is printed with its mechanism and decides nothing. **No PI is filed, no E3 endpoint is UNEVALUABLE for Gate-0 reasons, H-003's mechanism does not go to DEFERRED**, and no threshold was relaxed to get there. | ground 3 — one defensible answer: an arithmetic the desk cannot reproduce cannot carry a verdict, and a question that still answers two of its three limbs is not deferred; **DP-07** (a platform defect is a PI, not a research finding); **DP-21 / DP-45** (no gate lowered to keep an endpoint alive) |
| 18 | The lane for the slate replay | DECIDED | **Bull lane only**, as drafted: `main = [c for c in scorecards if dominant_direction != 'bearish']` with the night's own threshold, `min_completeness` and `max_output_cap`; **the bear lane is held at its production membership and enters neither slate**, with bearish picks excluded and counted. The two lanes have independent caps, so a bull ablation cannot move a bear slot, and pooling them would put a second, differently-gated population inside one endpoint. It is also forced by rule 6: bear-contributing nights ran at **0.157 per session** (H-062), so a bear E3 endpoint could not reach 80 nights inside DP-43's ceiling in any window. **Binding on the report:** every E3 verdict sentence says *"the published **bull** slate"*, never *"the slate"*. | ground 3 — one defensible answer (independent caps); **DP-28** (the publication predicate); **DP-43 / DP-21** (a bear endpoint cannot reach the floor and is not registered as though it could); H-062's measured rate |
| 19 | Who writes `eval.py`, who runs it, and the conventions fixed at lock | DECIDED | The **Researcher** writes `eval.py` **once** (rule 9) and runs the **2027-04-12** pass and, if it fires, the **2027-05-24** extension pass on the **byte-identical, unmodified** script (dates fixed at `record`, item 10); the **Data Steward** owns R1b, R2, the pins and the cross-freeze comparison. **No interim looks.** Fixed at lock and not reopened at the decision pass: seed **20260914**; **10,000** permutation draws for B1, B2 and the E3 sign-flip; **2,000** draws for B3 and for each of the two bootstraps; the **10-session** expected block length; the 0.05 Gate-0 tolerance, the 99% / 95% / 95% Gate-0 rates and the 1% replay gate; the **0.90** E2 identification threshold; the expanding-window `tape_t` tercile cuts and the `market_regime` v1.2 timestamp test. Seed, draw counts and library versions print in the results header. | rule 9 (no judgment in the inner loop); **DP-26** (registrar conventions fixed before any outcome is seen, none promotable at the decision pass); Q028 DECISIONS' same split of duties |
| 20 | The BH sets — within the question, in F1, and the F2 companion | DECIDED | **Within the question:** BH over **`m` = the EVALUABLE layer-endpoint pairs**, fixed at `record` and **never revised** (item 6). **Across F1:** Q006 (2) + Q024 (6) + Q025 (2, which never shrinks despite Q025's deferral) + Q029 (`m`) = **10 + `m`**, computed at the decision pass over the F1 questions locked by then and **never falling below it** — **settled at `record`: `m` = 16, so F1 = 26 and F2's companion set = 14** (item 26); another F1 question locking before **2027-04-12** joins the set and the q's are recomputed on the larger denominator. **The F2 companion correction on `E1ⱼ` and `E2ⱼ` is required, not optional**: they are computed on Q027's population, distance and clock, and a layer IC and the composite IC are not independent tests, so they must clear **q ≤ 0.10 in F1 and in F2** — F2's set being Q023 (2) + Q027 (2) + these `2L` endpoints — and **the larger of the two q's is the one quoted and the one that decides**. `E3ⱼ` is corrected in F1 only. **H-003 and H-020 are counted once, here** (merged into Q029, DP-29). | rule 8; **DP-29** (family by the primary endpoint's subject — selection → F1 — with overlapping hypotheses merged, not double-counted); the Q015 / Q020 companion-correction pattern; **Q027 DECISIONS #13** — a family set is stated symmetrically and never shrinks |

**Added at `record` (2026-09-14), from R1b — items 21–27. Each settles part of item 11 and is now closed.**

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 21 | Gate 0's scope — the "whole-freeze ≥ 95%" clause, and whether the E3 limb exists | DECIDED | **The segment reading. The E3 limb exists; item 17's trigger did not fire.** The Gate-0 determination is made on the **2026-06-01..2026-09-10 segment**, where reconstruction is **100.00% (68/68 nights, every night ≥ 99%, zero exceptions)**; the whole-freeze **84.77%** is **reported in §2.4 with its full mechanism** and decides nothing. Reason, stated without hedging: **Correction 3 — DECIDED at `decide`, before any count existed — already names Gate 0 among the "coverage and arithmetic facts" it scopes to the segment**, and R1b(d) shows the shortfall is not a residual error but a **different feature under DP-06 / DP-50(a)**: rows before ~2026-05-11 carry an 8-key `score_details_json` with **no `atr_elite_block_applied` and no GEX-missingness offset**, and every non-reconstructing row resolves to a residual of **exactly +5.00** — the `fa70688` formula applied to an engine two ships older. The literal reading is **degenerate on this question's facts**: the prospective window is **post-v1.5 by construction**, so it would kill the limb on rows `eval.py` will never read. Item 17's own reason — an arithmetic the desk cannot reproduce cannot carry a verdict — is **met** on the population that is read. **Nothing is relaxed in exchange:** the in-window gates stand at **≥ 99% per night, ≥ 95% whole-window, 0.05 tolerance**, `eval.py` fails loudly on an in-window night below 99%, the **1% replay gate** stands (measured 0.00% on 68/68 segment nights), and the larger `m` this admits is the **stricter** BH denominator for every endpoint. **No PI** (DP-07 not engaged): the −7.00 residual tail is confined to the same partial-schema era and is an artefact of the desk's own rehearsal of a superseded engine, not a defect in the engine that ran. | **DP-06 / DP-50(a)** (a config ship splits a column into two features at the ship date); **Correction 3**, already decided and already naming Gate 0; ground 3 — one defensible answer once the mechanism is dated; **not** a DP-45 case: DP-45 breaks ties the desk cannot state, it does not license a reading that voids a limb on rows outside the window (and the option taken raises the BH bar rather than lowering it). Not taken: the literal 2026-04-01 reading — `m = 10`, IC-only, no ablation limb |
| 22 | `m`, and the closed EVALUABLE / DEAD / UNEVALUABLE register | DECIDED | **`m` = 16**, fixed at `record` and **never revised** (item 6). **EVALUABLE on all three endpoints (5 layers × 3 = 15):** `flow_strength` (99.88% non-null, 3,986 distinct, variance 100% of nights), `technical_structure` (100.00%, 1,216, 100%), `gex_alignment` (99.00%, 32, 100% — E1/E2 do not depend on the layer's production weight, Correction 1/item 16), `fundamental_quality` (98.71%, 379, 98.5%), `catalyst_event` (100.00%, 8, 100%). **`projection`: E3 only (+1 = 16).** Its subscore is non-null on **62.74%** of segment rows and clears 70% in **no month measured** (49.44% → peak 65.11%, plateauing below the floor from July), so **E1_projection and E2_projection are UNEVALUABLE** — counts only, no verdict, **not in `m`**; **E3_projection is EVALUABLE**, since §4.3's 70% clause binds E1/E2 and ADDITION-E3 only and never REMOVAL-E3. **`smart_money_confirmation`: DEAD on all three** — 0.00% non-null and 0 distinct values on every row of the whole freeze, `enable_smart_money_enrichment` False on all 102 nights, and E3 ≡ 0 by mechanical identity (`:1341` counts a dimension only when `available and weight > 0`). **`fundamental_quality`'s ADDITION side: UNEVALUABLE** (item 23). **E2's control set is the retained set of five** — flow, technical, gex, fundamental, catalyst — so every evaluable E2 controls for **four** other layers, clearing §4.3's "≥ 3 other retained layers"; **`projection` is not among the controls** (Correction 10). The register is **closed**: a pair declared DEAD or UNEVALUABLE here is **never added to `m` later**, and a layer alive in the window that was dead on the freeze is reported as **`UNREGISTERED_LIVE`**, counts only (item 6(iii)). | **item 6** (declared once at `record` from coverage facts, no outcome in view, then closed), **item 16**, **item 21**; §4.3's own three clauses applied to R1b(a)/(b); **DP-43** (the determination is made at lock from counts); **DP-45** for item 6(iv) — R1b determined every pair, so no pair falls to the "undetermined → UNEVALUABLE" branch |
| 23 | The REMOVAL / ADDITION assignment, and the GEX addition weight | DECIDED | **No split survives on the segment; the assignment is per layer, not per night, as measured.** **REMOVAL on 68 of 68 segment nights:** `flow_strength`, `technical_structure`, `projection`, `catalyst_event`. **ADDITION on 68 of 68:** `gex_alignment` (production weight 0.0 on 100% of segment rows) and `smart_money_confirmation` (DEAD, not tested). **`fundamental_quality`: REMOVAL**, 67 of 68 nights — `enable_fundamental_enrichment` measures **True on 67 of the 68 segment nights** (and 81 of 102 population nights), **contrary to the draft's own expectation** that the code's `False` dataclass default (`super_agent_select_models.py:110`) would make it DEAD or ADDITION-only. Its **single ADDITION night, 2026-06-02**, projects to **1.2 contributing nights at 119 sessions** → **UNEVALUABLE at `record`**, counts only, no verdict, **not in `m`** (item 16); that night also carries Q027's `payload_disabled_runs` signature (all 8 published rows `analysis_status = "disabled"`), so under the machinery adopted at §2.0 it would be excluded whole in any case — two independent reasons, one conclusion. **GEX addition weight = 12.0, directly measured, not the fallback:** `scoring_weights.gex_alignment` in the last population config dated before 2026-05-14 is **2026-05-08 → 12.0**, and only **two** distinct values appear anywhere in the frozen history (12.0 through 2026-05-08, 0.0 from 2026-05-18). §2.3's arithmetic-fallback branch (`+7 +3 +2 = 12`) is **struck** — it is not needed and must not read as the registered basis (Correction 9). The `w ∈ {5, 12, 24}` curve stays a **descriptive companion that never decides**. | **item 2** Option A (the measured value, from the pinned freeze — **DP-50(c)**, never a live query); **item 16** (a side projected below 80 is UNEVALUABLE at `record`, counts only); **DP-06** (the two sides are never pooled); **DP-26** (a convention fixed at lock, not derived from an outcome) |
| 24 | E3's contributing-night rate, the near-miss pool, and which floor Correction 2 governs | DECIDED | **Floor B binds where Floor A binds — session 119 — so the window does not move beyond Q027's.** Every limb of §2.6's E3 rule measures at **100% on the segment**: Gate 0 passes on **68/68** nights (item 21); the replay disagrees on **0.00%** of nights, none above the 1% gate; `|S^prod_t| ≥ 1` on every night; and **B4's distance-matched control pool** — that night's eligible rows in **neither** slate — measures **mean 51.8, median 54, min 39** (`STEWARD_Q023_exposure.md` §6), clearing Correction 2's **≥ 10 distinct** floor on every night with a wide margin. **The distinction that decides this, stated explicitly because reading it the other way would defer the question on a bookkeeping artefact: Correction 2's ≥ 10 floor is on B4's control pool, NOT on B3's near-miss pool.** R1b(f) measures the **near-miss** pool (bull-lane, threshold + completeness pass, not selected — B3's placebo draw pool) at **min 0 (3 of 68 nights), median 8, max 26**; applied to that pool the ≥ 10 floor would strike roughly half the nights. **Consequence of the min-0 nights: none, in counts.** `k_{t,j} ≤ |near-miss pool|` **by construction** (the ablated slate is the top-`|S|` of the same passing set, so a swap needs an entrant from that pool), therefore B3's draw of `k_{t,j}` symbols is **always feasible**; an empty pool forces `k_{t,j} = 0`, and **item 7 already counts identical-slate nights (`ΔE = 0`) as contributing** — the diluting choice. **Registered for determinacy, and it costs nothing here:** a night whose near-miss pool holds fewer than **10** distinct names prints a **`DEGENERATE_PLACEBO` flag** with its pool size (the 2,000 B3 draws are then near-exhaustive and the placebo mean is close to determinate); the night **still contributes**, its `ΔE*` is still defined, and **no night is back-filled by widening the pool**. The per-layer `k = 0` share (flow 5.9%, technical 4.4%, gex 1.5%, projection 16.2%, fundamental 11.8%, **catalyst 67.6%**, smart-money 100%) leads each E3 verdict sentence under §8 clause 9 — catalyst's 67.6% is above 50% and will lead its sentence. | **Correction 2** read on its own text (§3 B4's pool, the number B4 actually draws); **item 7** (every E3-contributing night counts, including `ΔE = 0`); **DP-21** (no floor moved in either direction); **DP-43 / DP-45** (the window end is the **later** of the two floor projections and moves **out** only — here they coincide, so it does not move); ground 3 — `k ≤ pool` is mechanical |
| 25 | The sub-cell suppression list — fixed, and now closed | DECIDED | **Q027's measured list, transferred whole, and closed.** The two questions share the funnel, the population, the contributing-night rule **and now the window (119 sessions)**, so Q027's per-cell projections at session 119 are this question's counts; re-measuring the same cells on the same nights would be a second number for one quantity. **SUPPRESSED (8 cells):** `tape_t` `up_low` (16.8 nights projected), `down_high` (13.4), `up_high` (8.4), `down_mid` (6.7), `down_low` (5.0), and the three `market_regime` labels **structurally absent** from the measurement — `bearish`, `neutral`, `risk_off` (0 of 48 nights). **NOT suppressed:** `tape_t` `up_mid` (30.2), `market_regime` `strongly_bullish` (48.6) and `bullish` (23.5), all three `best_timeframe` cells (**E1/E2 only** — for E3 the slate's timeframe composition prints instead), **bull-only and bear-only** (80.4 each on the candidate-level population), published versus unpublished. **`market_regime` `unlabelled` is not a cell** — the pre-2026-06-09 backfill cannot occur in a window starting 2026-09-15 (rule 7). §4.4's drafted expectations — bear-only suppressed, all six `tape_t` cells suppressed — are **struck**: they were rates on the **narrower published** population (PI-010's published-elite counts, H-062's 0.157/session bear rate) and do not transfer to a candidate-level funnel (Correction 13). **Clearing the projection is permission to print, not a guarantee:** every listed cell still needs **≥ 20 measured** contributing nights at the decision pass, and a cell suppressed here **stays suppressed even if it clears 20** (item 13). **Suppression restricts affirmative reporting only** — it never removes a blocker, never by itself makes an endpoint INCONCLUSIVE, and §8's blockers run on **measured** counts for suppressed and unsuppressed cells alike. | **item 13**; **Q027 DECISIONS item 10 and Correction 2/3**, adopted with the machinery (§2.0); **DP-21** (20 per cell, no floor moved); **DP-43** (fixed at lock from counts, never afterwards) |
| 26 | The BH sets, with `m` final | DECIDED | **Within the question: `m` = 16**, the EVALUABLE layer-endpoint pairs of item 22, **fixed in every branch** — an endpoint short of floor at the decision pass still has its p computed and **stays in `m`**; a DEAD or UNEVALUABLE pair was never in it; **no pair is dropped afterwards**. §7's "expected 12–15, bounded above by 21" is replaced by the measured 16 (Correction 8). **Across F1: Q006 (2) + Q024 (6) + Q025 (2, which never shrinks despite Q025's deferral) + Q029 (16) = 26**, computed at the decision pass over the F1 questions locked by then and **never falling below 26**; another F1 question locking before 2027-04-12 joins the set and the q's are recomputed on the larger denominator. **F2 companion, required on E1ⱼ and E2ⱼ: Q023 (2) + Q027 (2) + `2L` = 10 → 14**, where **L = 5** (the IC-evaluable layers; `projection` contributes no IC endpoint and `smart_money` none). **E1ⱼ and E2ⱼ must clear q ≤ 0.10 in both sets and the larger of the two q's is quoted and decides**; **E3ⱼ is corrected in F1 only.** **H-003, H-020 and H-075 are counted once, here.** Threshold q ≤ 0.10 alongside raw p (rule 8). | **item 20** applied to the measured `m`; rule 8; **DP-29**; **Q027 DECISIONS #13** — a family set is stated symmetrically and never shrinks |
| 27 | DP-50's sweep, and the v1.7 split trigger | DECIDED | **No split is in view at lock, and item 15's clause stays load-bearing rather than ceremonial.** R1b(g): the commit sweep since `fa70688` over the four named SAS files returns **NONE**, independently re-verified (ancestry confirmed; `git log fa70688..HEAD` over those paths is empty — the same 4 commits Q027's R1 found, 2 substantive + 2 merges, none touching them). **v1.7 has not shipped and is not scheduled**: `docs/SAS_SCORING_RESEARCH_PLAN.md` at `fa70688` is still headed *"Status: PROPOSAL, not a decision record"*, its own Phase 1 prerequisite (dark-cohort W60 backfill) has not shipped, and the only in-flight related work (PI-001, branch not merged) touches none of the four files. **No repair rewrote a historical row** anywhere in R1b's census, so **no new `DATA_NOTES.md` entry is owed** from this report; the config changes it found (the v1.5 weight reallocation effective 2026-05-18, the ATR-elite caps from 2026-05-18, `publication_floor` from 2026-07-08, `bear_publish_threshold` from 2026-06-29, the enrichment-flag history) are **per-night contemporaneous facts, not mutations**, and every one of them predates the window by more than two months. **Forward consequence, unchanged:** any weights / multiplier / enrichment-flag / `qualification_threshold` / `publication_floor` / `max_output_cap` / `min_completeness` / ATR-elite-cap / GEX-offset change — **including any v1.7 promotion** — is **flag-off until 2027-04-12 (2027-05-24 if the extension fires)**, checked before any fix brief is written, and if one ships inside the window item 15 cuts the window **whole** at the ship date, out and never in. | **DP-50(a)/(b)/(c)**; **item 15**; **DP-06**; R1b(g) |

## Corrections to silent choices

**Six at `decide`, nine added at `record` (7–15).** The Registrar applies them all at `apply` with the rest of this file. Everything else was checked
against the policy and already matches (list at the end of this section).

1. **§7 and §2.3 — `m` "bounded above by 21" contradicts the draft's own split rule, and the split is
   applied to endpoints it cannot govern.** §2.3 says a layer whose nights split between REMOVAL and
   ADDITION "is two different tests and is never pooled … each counted in `m`", which can put `m`
   above 7 × 3 = 21; and it is written as though it governed all three endpoints, when `E1ⱼ` and
   `E2ⱼ` rank a **subscore**, whose ordering information does not depend on the weight the subscore
   carries. **Must read:** §2.3's REMOVAL / ADDITION rule governs **`E3ⱼ` only**; `E1ⱼ` and `E2ⱼ` are
   computed over **all** of the layer's contributing nights regardless of its effective weight, with
   the REMOVAL / ADDITION split reported as a **descriptive stratum** subject to the ≥ 20-night rule;
   and §7's bound reads **`m ≤ 21 + (one further E3 endpoint for each layer whose nights split and
   both of whose sides R1b projects ≥ 80 contributing nights)`**, with item 16's clause — a side
   projected below 80 is **UNEVALUABLE at `record`**, counts only, not in `m` — stated in §4.3 beside
   the DEAD rule.
2. **§2.6(iii) — the E3 control-pool floor is stated at ≥ 3 while §3 B4 matches the 10 nearest.**
   Drawing 10 controls with replacement from a pool of 3 gives a control set of three distinct names
   replicated, and a touch rate built on it is not the distance-matched control rule 5 requires.
   **Must read:** an E3-contributing night needs **≥ 10 distinct same-night control candidates** in
   that night's control pool for **every** pick in `S^prod_t ∪ S^abl_t,j` — the number B4 actually
   draws — and a night below it is **non-contributing and counted, never back-filled by widening the
   match**. The cost is nil in expectation: `STEWARD_Q023_exposure.md` §6 measures a mean of **51.8**
   same-night non-published rows passing the Q006 match screens (median 54, **min 39**).
3. **§4.3 and §5.3(a) — evaluability is measured over a span DP-06 says is two different features.**
   R1b runs over the whole freeze, 2026-04-01..2026-09-10, and §4.3 fixes the EVALUABLE / DEAD list
   from those counts — but the catalyst layer is a different feature before 2026-06-01 (DP-06), and
   an enrichment flag or a weight vector that changed inside April–May would let sealed coverage
   mis-declare a layer that is alive in the prospective window, or alive one that is dead.
   **Must read:** the EVALUABLE / DEAD / UNEVALUABLE determination is made on the
   **2026-06-01..2026-09-10 segment** of the freeze, with the per-month series printed beside it so a
   coverage trend is visible; the April–May counts serve R1b(b)'s flag census and R1b(c)'s GEX weight
   **only** and decide no layer's evaluability. Item 6(iii)'s `UNREGISTERED_LIVE` clause covers the
   residual risk in the direction that cannot inflate a claim.
4. **§5.4 — the successor price freeze drops DP-23's hourly bars.** The draft says "no hourly bar is
   used and no endpoint depends on one" (§2.2, true) and asks the Steward not to build them; **DP-23
   says successor price freezes *always* include all candidate symbols, published and unpublished,
   **plus hourly bars for published symbols***, unconditionally. **Must read:** §5.4's R2 asks for
   DP-23's freeze as written — hourly bars for published symbols included. This changes **no** Q029
   endpoint (DP-27 stays unreachable; no intra-session ordering is needed anywhere) and costs only
   build time; it is an **addition** to the shared Q027/Q029 pair, so Q027's own R2 text — which asks
   for them to be skipped — is not contradicted in anything it relies on. The general question
   ("is DP-23's hourly-bar clause waivable where no endpoint uses one?") is filed under **Standing
   rules proposed**, for Haci, and is not decided by this run.
5. **§5.5 — the session-by-session arithmetic reads as evidence, and it rests on a borrowed number.**
   The 92-session count, the "floor A met at session 84" line and the "8 further sessions" cushion
   all rest on Q027's borrowed **0.9538**/elapsed-session published-pick rate, which is not this
   funnel's rate. **Must read:** §5.5's table and arithmetic are a **drafting projection**,
   superseded at `record` by Q027 R1's **measured** contributing-night rate, from which the window
   end and every date are recomputed **moving out only** (DP-43, DP-45); the 8-session cushion is a
   margin on a borrowed number and is **not evidence** — if the measured rate puts floor A or floor B
   below 80 inside the primary window, the **window end moves out before lock**, because DP-13's
   single extension is the fallback for a **measured** shortfall and never the plan. A measured rate
   **faster** than the borrowed one changes nothing and never could.
6. **§8 — the decision rule has no clause for item 1's blocker, and §4.4 lists the
   added-minus-dropped decomposition as purely descriptive.** **Must read:** §4.4 moves the
   added-minus-dropped decomposition from "purely descriptive" to the **"computed, and blocking"**
   list, and §8 gains a clause (numbered with clauses 6–10): for `E3ⱼ` on a layer with **≥ 20
   discordant contributing nights**, the decomposition must carry the **same sign as `E3ⱼ`**, and a
   decomposition beyond **10.0 pp in the opposite sign** blocks a CONFIRMED; below 20 discordant
   nights it prints counts only and blocks nothing. §8's INCONCLUSIVE list gains the failure of that
   clause.

**Added at `record` (2026-09-14), from R1b and Q027's settled schedule:**

7. **§2.4 and §4.3 — Gate 0's evaluability clause must name the segment, and must print the
   whole-freeze figure beside it.** As drafted, §2.4/§5.3(d) read "whole-freeze", which R1b measures at
   **84.77%** while the segment measures **100.00%**. **Must read:** the Gate-0 **evaluability**
   determination is made on the **2026-06-01..2026-09-10 segment** (item 21, Correction 3's own
   scoping, DP-06); §2.4 prints **both** figures with the mechanism — the 8-key `score_details_json`
   before ~2026-05-11, the exactly **+5.00** residual signature of the v1.5 GEX-missingness offset, and
   the **−7.00** tail confined to the same partial-schema era — so no reader takes 100% as an
   unqualified claim about the whole freeze. The **in-window** gates are unchanged: **≥ 99% per night,
   ≥ 95% whole-window, tolerance 0.05**, `eval.py` failing loudly on any in-window night below 99%.
   §17's IC-only branch is recorded as **not taken, with the measured rates named**, rather than struck.
8. **§7 and §4.3 — "`m` expected 12–15, bounded above by 21" is replaced by the measured `m` = 16.**
   **Must read:** `m` = **16**, itemised per layer (item 22), fixed at `record` and never revised; the
   drafted range and the expectation paragraph in §4.3 ("flow, technical, projection and catalyst
   evaluable on all three; smart-money and fundamental expected DEAD or ADDITION-only") are **struck and
   replaced by the measured register**, with the drafted expectation kept in one struck line so the
   contradiction is visible: **`projection` lost two of its three endpoints** and **`fundamental_quality`
   gained all three on its REMOVAL side**. Correction 1's bound stands and 16 is inside it (no layer has
   both sides clearing 80, so the bound is the plain 21).
9. **§2.3 — the GEX addition weight is the measured 12.0 and the arithmetic-fallback branch must be
   struck.** **Must read:** the addition weight is **12.0**, read from the last population config before
   the v1.5 ship (**2026-05-08**), with the note that only two values ever appear in the frozen history
   (12.0 through 2026-05-08, 0.0 from 2026-05-18); the `+7 +3 +2 = 12` derivation stays as a
   **corroborating remark**, never as the registered basis. §2.3's "if no night carries a non-zero
   value" branch is **struck** — it did not fire.
10. **§4.1 and §4.3 — `E2ⱼ` is partial on the retained set of five, and `projection` is not in it.**
    The retained set under §4.3's coverage rule is **flow, technical, gex, fundamental, catalyst**;
    `projection` fails the 70% floor, so the partial IC controls for **four** other layers and **the
    largest-weighted layer in the engine (29 pts) is not among the controls**. **Must read:** §4.1/§4.3
    name the retained set explicitly, §8's E2 verdict sentence says *"partial on the four other
    **retained** layers, `projection` excluded for coverage"*, and the `R²_{t,j}` panel is printed on
    that set. This is an interpretation constraint on every E2 result and it is not optional.
11. **§4.4 — the tie-structure reference is mandatory beside `gex_alignment` and `catalyst_event`.**
    R1b(a) measures **32** distinct `gex_alignment` values and **8** distinct `catalyst_event` values on
    4,020 segment rows. An IC on a variable with 8 levels against a mostly-tied outcome rank is bounded
    well below 1. **Must read:** the per-night touch base rate, the tied-block size and the **maximum
    attainable `|ρ|`** print **beside every quoted `E1ⱼ` / `E2ⱼ`** and are named in the verdict sentence
    for those two layers; **`IC_t` is never rescaled** by them and **the 0.05 MPE is never adjusted** for
    them — rescaling would silently move the MPE.
12. **§2.6(iii) — the control floor must name B4's pool, not B3's.** As drafted the clause says "control
    pool" without saying which, and Correction 2 raised the number to 10; R1b(f) measures the **near-miss
    (B3) pool** at **min 0, median 8**, so the wrong reading would strike about half the nights.
    **Must read:** §2.6(iii) requires **≥ 10 distinct same-night candidates in that night's §3 B4
    distance-matched control pool** — the night's eligible rows in **neither** slate, measured at mean
    51.8 / min 39 — **and imposes no floor on B3's near-miss pool**. §3 B3 gains: `k_{t,j} ≤ |near-miss
    pool|` by construction, so the draw is always feasible; a night with an **empty** pool has
    `k_{t,j} = 0` and contributes `ΔE* = 0` (item 7); a night whose pool holds **fewer than 10** distinct
    names prints a **`DEGENERATE_PLACEBO`** flag with its pool size and **still contributes**; no night is
    ever back-filled by widening a pool or a match.
13. **§4.4 — the suppression expectations are struck and replaced by the closed list.** The draft states
    *"bear-only is expected to be SUPPRESSED"* and *"the six `tape_t` cells are expected to be
    SUPPRESSED"*. **Must read:** the registered rule is a **measured count**, not an expectation; the list
    is item 25's — **five** `tape_t` cells and the three absent `market_regime` labels suppressed,
    **bear-only, `up_mid`, both live regime labels and all three `best_timeframe` cells on the affirmative
    list** at ≥ 20 measured nights. The published-population rates the draft cited (PI-010, H-062's
    0.157/session) **do not transfer** to a candidate-level funnel, and the sentence saying so is part of
    the correction.
14. **§5.5, §5.4, §5.2 and §9 — every date is replaced by Q027's measured schedule, moving out.**
    **Must read:** window **2026-09-15..2027-03-05 = 119 elapsed sessions**; decision **Monday
    2027-04-12**; single DP-13 extension to window end **2027-04-19** (session 149) decided **Monday
    2027-05-24**, the hard stop, then DEFERRED; R2's freeze pair covers pick nights through **2027-03-05**
    with bars through **2027-04-05**, delivered before **2027-04-12**, the extension pair through
    **2027-04-19** with bars through **2027-05-17** before **2027-05-24**; §9's and item 15's DP-50(b)
    flag-off constraint runs to **2027-04-12 (2027-05-24 if the extension fires)**. §5.5's whole
    session-by-session table, the 0.9538 planning rate, the "floor A met at session 84" line and the
    "8 further sessions" cushion are **struck** and replaced by the measured arithmetic (Correction 5's
    instruction, now executed): **0.6761/session → ceil(80/0.6761) = 119**. Floor B is recorded as binding
    at the **same** session 119 with item 24's three measured limbs named, not as "recomputed at record".
    Holidays used: 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31.
15. **§2.5 — the replay's treatment of a config key that is absent must be registered, not left to the
    dataclass.** R1b(e) found that **56 of 102 nights' `config_json` lack `publication_floor` entirely**
    (all pre-2026-07-08), which is not the same as the key being present and null, and that substituting
    the current dataclass default (80.0) produced **spurious** disagreement. **Must read:** §2.5's replay
    honours **each night's own config literally** — an **absent** key means that gate **did not exist that
    night** (floor 0.0), and the current default is **never** substituted for a historical night; the same
    rule applies to `bear_publish_threshold`, `bear_max_output_cap` and the ATR-elite caps. Inside Q029's
    own window the point is moot (`publication_floor` = 80.0 has been live since 2026-07-08), so this
    governs the sealed descriptive panel and makes `eval.py` deterministic rather than
    version-dependent. §6's prior-art panel notes that the **12 April replay discordances** are the
    pre-2026-07-02 single-lane counter, not a replay failure.

Checked and **not** corrections — each already matches the policy: the machinery adopted from Q027
**as that file stands after its own DECISIONS.md is applied**, which is the only reading under which
"one machinery, two questions" is true (§2.0); the entry the **session t+1 regular-session open** for
every row alike, with **DP-11 correctly not fired** and the `C_t` basis a printed sensitivity that
never decides (**DP-03(b)**, **DP-42**); the **L3 distance on the 20-session clock** with the
40-session companion descriptive (**DP-09**, **DP-42**); the IC MPE at **0.05** stated with Haci's own
H3 source and never lowered at the decision pass, with **no DP entry written by this run**
(**DP-25**, **DP-44**, **DP-40**); floors read as **≥ 80 contributing nights per primary endpoint**
and 20 per reported cell (**DP-21**); **≥ 30 contributing nights after the lock commit**, satisfied by
construction, with **DP-31 correctly not invoked** — PROSPECTIVELY_CONFIRMED is reachable from this
run by design and no successor replication is owed (**DP-24**); one automatic extension then DEFERRED,
fired on `eval.py`'s **measured** counts and never on a projection, a floor shortfall never an
INCONCLUSIVE verdict (**DP-13**); the publication predicate **`qualified IS TRUE AND selected_rank IS
NOT NULL`** with dark-lane rows out of both slates and still in the candidate population
(**DP-28**); **no stop assumed**, adverse excursion and counter-direction touches at `−d*_t` reported
and never used as exits, **DP-30** not engaged and **DP-27** not reachable (**DP-02**); the blocking
companion for `E3ⱼ` stated as **touch-within-5-sessions** and not as a sessions-to-touch difference,
which has no MPE (**DP-44**, Q027 Correction 1 inherited); suppression restricting **affirmative
reporting only** and never removing a blocker (Q027 Correction 2 inherited); the successor freeze
covering **every candidate symbol, published and unpublished** (**DP-23**); the **two CIs per
primary** with the episode at gaps ≤ 10 sessions and the CI-2-includes-zero case INCONCLUSIVE rather
than CONFIRMED (**DP-51**, §8 clause 4); the whole window after the **2026-06-09** point-in-time
boundary, so the `market_regime` backfill hazard cannot reach it (rule 7, FREEZE_v001 §7); counts
taken from the **pinned freeze** and never a live query (**DP-50(c)**); the DP-50(b) flag-off
constraint named in §9 and checked before any fix brief (**DP-50(b)**); **DP-49** binding every brief
this question produces — a weight change is provable from the repo alone; the **August layer audit**
printed **once** as a labelled prior-art panel entering no verdict, no CI comparison, no half, no
stratum and no q, with §6's four binding consequences listed so a reader can check them (rule 3);
every number **NON_QUOTABLE** (rule 12) and nothing subscriber-facing before PROSPECTIVELY_CONFIRMED
(rule 10); and **no rule-14 exception requested or needed** (**DP-05** untouched, **DP-41** respected).

## Defaulted on Haci's behalf

- #9 Window start — chose **prospective-only, pick nights ≥ 2026-09-15**; not taken: read the sealed
  nights, decides now, not blind — DP-43. Overturn = successor question.
- #10 Window end, decision date, extension — chose **2026-09-15..2027-03-05, decided Monday 2027-04-12,
  single extension decided Monday 2027-05-24**, on Q027's measured 0.6761 contributing nights/session;
  not taken: the 0.9577 eligible-night proxy — decides ~2027-02-22 — DP-43, DP-45. Overturn = successor
  question.

Two items at `record`; #9 is the same one Q027 defaulted four hours earlier, for a stronger reason. The
platform's own August layer audit (`docs/SAS_SCORING_RESEARCH_PLAN.md:53-67`) is **H-075's own
statistic**, already computed per layer on the sealed cohort, with a verdict in its own last column —
*"Largest weight, no signal"*, *"Only weighted layer that works"*, *"Mildly anti-predictive"*,
*"Dead — NULL on all 5,868 rows"* — and the registrar read it while drafting. Sealed nights can
produce a description of that table; they cannot produce a test of it. The price is that **Haci waits
until 2027-04-12 for a question whose sealed-period answer is already written down in the platform
repo**, and that is the honest cost of rule 3 here. **Item 10 joined this list at `record`**, as this
file said it would: Q027's measured rate is **slower** than the borrowed one, so the window end and
both dates moved **out** (2027-03-08 → 2027-04-12; 2027-04-19 → 2027-05-24). A faster rate would have
changed nothing and never could (DP-43, DP-45).

Nothing else was defaulted. Items 1–8, 13–20 **and the seven added at `record` (21–27)** each met a DECIDE ground, and none of them is a
question about how Haci trades — the level, the lane, the clock, the entry basis and the target
distance all arrive from Q027's machinery and from DP-09 / DP-42 as already locked in Q002–Q024, and
the one MPE that is not a DP number is **his own**, from H3. **No floor, arm, MPE, gate, denominator
or clause was weakened anywhere in this file:** items 1, 6, 7, 13, 16, 17 and 18 and Corrections 1–3
and 6 each tighten one, and the one place a number moved (Correction 2, the control-pool floor from 3
to 10) moved it up. **The `record` pass kept that true:** `m` rose from an expected 12–15 to **16**,
which **raises** the BH bar for every endpoint in the question; every date moved **out**; no gate,
tolerance or floor was relaxed to admit the E3 limb; the suppression list was taken from measurement
rather than from the draft's expectations; and the one reading that could have been called lenient —
scoping Gate 0 to the segment — is the one that makes the **denominator larger** and leaves the
in-window gates untouched.

## Routed requests

### data-steward — R1 — **already routed under Q027; do not run a second count**

**No request.** Q029's E1/E2 funnel is Q027's funnel (PREREG §2.0), so the exposure basis is read
from **`research/reports/STEWARD_Q027_exposure.md`, request R1, item (a)** — contributing nights per
elapsed session under Q027 §2.5's complete definition — when that report lands. **Please do not build
a second exposure count for Q029**: one funnel, one number, one gate. Q029 locks if and only if Q027
locks on that number (**≥ 0.36 contributing nights per elapsed session**, re-solved at `record` if
the lock date moves) and is **DEFERRED with Q027** below it, on the same measurement. If R1's report
already carries the per-floor projected dates Q027 asked for, they serve Q029 unchanged; §5.5's
window end is then set on the **later** of that projection and the E3 projection built from R1b(d)(e),
moving **out only**.

### data-steward — R1b (counts only, **blocking for `m` and for the lock**) — **CLOSED, delivered 2026-09-14**

**Answered in full** at `research/reports/STEWARD_Q029_feasibility.md`; settled in items 21–27 and
Corrections 7–15. Nothing further is asked of the Steward on R1b. The request text is kept below as
issued, unedited, so what was asked before the counts existed stays legible.

Q029 (which of the seven SAS scoring layers earns its weight — PREREG §5.3 request R1b) needs a
**counts-only feasibility** measurement on the **frozen** data — `research/data/manifest_v001.json`
against `research/data/exclusions_v003.json`, plus read-only `git log` / `git show` in the platform
repo at `fa70688` — and **never a live query** (DP-50(c)). **This is not an exposure count and does
not size the question**: Q029 borrows Q027's R1 for that and no second exposure count should be run.
It is blocking for the lock because it fixes **`m`**, the BH denominator, which cannot be fixed once
outcomes exist. **No outcome of any kind is read**: no touch, no first-touch date, no return, no
excursion, no `outcome_*` column, no `sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`,
and no score-versus-outcome cross-tab of any shape; **no price bar is needed for any part of R1b**
beyond the daily bars already pinned for Q027's R1(c). Population: **every row in `sas_candidates`,
published or not, regardless of `qualified` / `threshold_pass`**, over pick nights
**2026-04-01..2026-09-10** — the whole freeze, because the enrichment flags and the pre-v1.5 GEX
weight change inside it — with `exclusions_v003` and DP-04 nights removed. Please return, **per layer
and per month**, and separately for the **2026-06-01..2026-09-10 segment**, which is the segment that
decides evaluability (DP-06; the April–May counts serve (b) and (c) only): **(a) layer coverage** —
the non-null share of each of the seven subscore columns over all candidate rows, the distinct-value
count, and the share of nights with non-zero within-night variance, scored against the retained-layer
rule Q028 §4.0 registers (≥ 70% non-null, ≥ 5 distinct values, variance on ≥ 50% of nights); **(b) the
production effective-weight census** — from `score_details_json.weighted_dimensions[j].weight`, the
share of rows with weight > 0, the distinct weight values, the **REMOVAL / ADDITION split of nights**
under PREREG §2.3's per-night rule, and the per-night values of `enable_fundamental_enrichment` and
`enable_smart_money_enrichment` from `sas_runs.config_json`; where a layer's nights **split**, please
also give the count of nights on each side and the implied per-side rate per elapsed session, since a
side projecting below 80 contributing nights in a 92-session window is declared UNEVALUABLE at lock
and the other side becomes that layer's endpoint; **(c) the GEX addition weight** — the value of
`scoring_weights.gex_alignment` in **every distinct** `sas_runs.config_json` in the freeze with the
date range of each, and in particular **the last config dated before 2026-05-14**; if no night in the
freeze carries a non-zero value, please say so **explicitly**, since the PREREG then registers 12.0
with its derivation printed; **(d) the Gate-0 reconstruction rehearsal** — the share of rows whose
stored `overall_score` reconstructs to within **0.05** from stored `weighted_dimensions` +
`config_json` + the stored `cross_layer_bonus`, `conflict_penalty`, missing-data flags, GEX-missingness
offset and `atr_elite_block_applied` flag, **per night and whole-freeze**, with the
`weighted_dimensions` parse-coverage per night and the residual distribution — a pure arithmetic check
on frozen columns, and the one that decides whether the ablation limb exists at all (below 95%
whole-freeze, every E3 endpoint is UNEVALUABLE at lock and Q029 registers as an IC-only question);
**(e) the slate-replay check and the per-layer slate-change rate** — replay `_qualify_lane` on the
**bull lane** (`super_agent_select_scoring.py:1509-1548`, `:1642-1649`) with each night's own config,
and report (i) the disagreement rate against the frozen published set (`qualified IS TRUE AND
selected_rank IS NOT NULL`, DP-28), listing every night above 1% and every `qualification_reason` the
replay cannot reproduce, and (ii) **for each of the seven layers, the share of nights on which the
ablated slate differs from the production slate at all, and the distribution of the discordant count
`k_{t,j}`** — a function of 16:05 columns only, which reads no outcome and tells the desk before the
lock which E3 endpoints can move; **(f) the near-miss pool** — per night, the number of bull-lane
candidates passing that night's threshold and completeness gates but **not** selected, with
min / median / max; and **(g) the DP-50(a)/(b) commit sweep** since manifest SHA `fa70688` over
`services/super_agent_select_scoring.py`, `services/super_agent_select_models.py`,
`services/super_agent_select_service.py` and `services/sas_conviction_card.py` — the weights, the
timeframe multipliers, the enrichment flags, `qualification_threshold`, `publication_floor`,
`max_output_cap`, `min_completeness`, the ATR-elite caps, the GEX-missingness offset and the lane-plan
writer — each with SHA and date in ET, with an explicit answer **even when it is "none"**, plus a
dated `research/data/DATA_NOTES.md` entry for any repair that rewrote historical rows; and **please
state separately whether any part of the "v1.7" scoring workstream
(`docs/SAS_SCORING_RESEARCH_PLAN.md` §7, Phase 5: "v1.7 assembled → shadow-parallel nightly (dark)
≥ 4 weeks") has shipped or is scheduled to ship inside pick nights 2026-09-15..2027-03-10**, because a
promotion of a new weight vector is exactly the event that cuts this question's window (DP-50(b): it
is flag-off until 2027-03-08, the same constraint and the same date Q027 carries). **What R1b
decides:** `m`, the EVALUABLE / DEAD / UNEVALUABLE list, the REMOVAL / ADDITION split and its
per-side floor consequence, the GEX addition weight, whether the E3 limb is evaluable at all, and the
sub-cell suppression list — all fixed at `record` and then closed. **It does not decide the lock gate;
Q027's R1 does.** Report to `research/reports/STEWARD_Q029_feasibility.md`.

### data-steward — R2 (successor freezes) — **dates fixed at `record`; they moved out**; due before the decision date, **not** a blocker for lock

**Re-issued 2026-09-14 with final dates (supersedes the provisional text below, which is kept for the
record).** Build **one** pair for Q027 and Q029 together: `manifest_v00N` (selections) and
`manifest_prices_v00N` (daily bars) covering pick nights **2026-09-15 .. 2027-03-05**, with **20
forward sessions** beyond the last included pick night (**daily bars through 2027-04-05**) and **≥ 60
prior sessions** before 2026-09-15, delivered before **Monday 2027-04-12**; and — **only if** the
single DP-13 extension fires — a second pair covering **.. 2027-04-19** with forward bars through
**2027-05-17**, due before **Monday 2027-05-24**, built then and not before. The add-only successor
exclusions file carries **four** criteria — `manual_runs`, `non_session_runs`,
`uncorroborated_publication_runs` and **`payload_disabled_runs`** (Q027 DECISIONS item 11 /
Correction 7: a night on which **every** published row carries
`public_payload_json.analysis_status = "disabled"` or no `lane_plans` object at all is excluded
**whole**) — add-only, applied to nights after 2026-09-10, **no night removed from any v003 list**.
Every scope requirement in the paragraph below stands unchanged, including Q029's **(v)**
`score_details_json` + `missing_data_json`, **(vi)** per-night `config_json`, and **(vii)** DP-23's
hourly bars for published symbols. Please re-confirm every date **session by session from the trading
calendar** when the freeze is built (holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18,
2027-02-15, 2027-03-26, 2027-05-31); a correction may move a date **out, never in**.

*(provisional text as issued at `decide`, superseded above on dates only:)*

Q029 (PREREG §5.4 request R2, DP-23) and **Q027** need the **same** successor freezes — please build
**one** pair and pin it for both. `manifest_v00N` (selections: the same SQL and the same exclusion
criteria as v001, over **`sas_candidates` for every candidate row, published and unpublished**, plus
`sas_runs` and `market_regime_daily`) and `manifest_prices_v00N` (daily bars for **every candidate
symbol on every in-window night, published or not**), covering pick nights
**2026-09-15 .. 2027-01-26** with **20 forward sessions beyond the last included pick night** (daily
bars through **2027-02-24**) and **≥ 60 prior sessions before 2026-09-15**, delivered before
**Monday 2027-03-08**; and — **only if** the single DP-13 extension fires — a second pair covering
**.. 2027-03-10** with forward bars through **2027-04-08**, due before **Monday 2027-04-19**, built
then and not before. **All dates are provisional and are fixed at `record` from Q027's R1 report;
a correction may move a date out, never in.** Q027's four scope requirements apply unchanged — every
candidate symbol published and unpublished, never assumed from v001's symbol list; an **add-only**
successor exclusions file applying the identical three criteria to the post-lock nights, which may
add nights and may never remove one from a v003 list; rows whose bars are missing **excluded and
counted, never back-filled or imputed** — **plus three that are Q029's and are not optional:**
**(v)** `sas_candidates.score_details_json` and `sas_candidates.missing_data_json` are in the frozen
column set — without `weighted_dimensions` there is no ablation; **(vi)** `sas_runs.config_json` is
frozen **per night**, not once, because the replay uses each night's own thresholds, caps, flags and
multipliers; and **(vii)** **hourly bars for published symbols are included, per DP-23** — Q029 uses
none and Q027 uses none, so this is a build requirement from the standing policy rather than an
endpoint requirement, and it should be built rather than skipped (Q027's own R2 text asks for them to
be skipped; DP-23's clause is unconditional and this request supersedes only by addition). **The
DP-50(a) guard is load-bearing here:** where a successor freeze overlaps an earlier one on
`sas_candidates`, the rows are compared and any disagreement in `overall_score`, **any layer
subscore**, `conflict_penalty`, `cross_layer_bonus`, `dominant_direction` or
**`weighted_dimensions[*].weight`** is a **loud failure** — a repair that rewrote a weight would
silently re-run this experiment. Please repeat R1b(g)'s commit sweep for the period **between** the
freezes, with a dated `DATA_NOTES.md` entry for any repair that rewrites historical rows, and report
explicitly — **even when the answer is "none"** — whether any weights, timeframe-multiplier,
enrichment-flag, `qualification_threshold`, `publication_floor`, `max_output_cap`, `min_completeness`,
ATR-elite-cap or GEX-offset change, **including any v1.7 promotion**, shipped **inside** the window;
DECISIONS item 15 cuts Q029's window at such a ship date, out and never in. Please re-confirm every
§5.5 date **session by session from the trading calendar** when the freeze is built; the holiday list
used here is 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26.

## Schedule

**FINAL — filled at `record` 2026-09-14** from `research/reports/STEWARD_Q027_exposure.md` (R1,
borrowed per §5.2) and `research/reports/STEWARD_Q029_feasibility.md` (R1b). Q027's measured rate
**0.6761 contributing nights per elapsed session (48/71)** — not the borrowed 0.9538 and not the
0.9577 eligible-night proxy. Every date moved **out** from the provisional schedule and may only ever
move out again (DP-43, DP-45).

decision_date: **2027-04-12** (Monday) · extension_date: **2027-05-24** (Monday — DP-13's single
automatic extension, window end 2027-04-19 = session 149; then DEFERRED, there is no second pass) ·
hard_stop: **2027-05-24** (still short there → `research/questions/DEFERRED.md`) · rule:
**exposure-driven**

- **window:** pick nights **2026-09-15 .. 2027-03-05** = **119 elapsed sessions**; extended window
  .. **2027-04-19** = 149 sessions · **extended: false** — **Q027's window, adopted whole** (§2.0,
  §5.2): one freeze, one exposure count, one maturity horizon, one decision date.
- **binding floors:** **A** — ≥ 80 contributing nights per E1ⱼ/E2ⱼ endpoint (DP-21) at
  ceil(80/0.6761) = **session 119**. **B** — ≥ 80 contributing nights per E3ⱼ endpoint: binds at the
  **same session 119**, because every additional limb of §2.6's E3 rule measures at 100% on the sealed
  segment (Gate 0 **68/68** nights; replay disagreement **0.00%**, no night above the 1% gate; B4
  control pool mean 51.8 / **min 39** ≥ Correction 2's 10; `|S^prod_t| ≥ 1` on every night), and the
  min-0 **near-miss** nights cost nothing (`k ≤ pool` by construction; `k = 0` nights contribute
  `ΔE* = 0` under item 7) — item 24. **C** — DP-24's ≥ 30 post-lock contributing nights lands at
  session 45 = **2026-11-16**, **non-binding**, satisfied by construction. Window end = **later of A
  and B = session 119**.
- **decision-date arithmetic:** window end 2027-03-05 + **20 sessions maturity** = 2027-04-05, + one
  calendar week freeze margin = 2027-04-12, first Monday on or after = **Monday 2027-04-12**, not a
  market holiday. Extension: session 149 = 2027-04-19, + 20 sessions = 2027-05-17, + one week, first
  Monday on or after = **Monday 2027-05-24**. Holidays used: 2026-11-26, 2026-12-25, 2027-01-01,
  2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31.
- **maturity:** 20 sessions, uniform across every eligible row.
- **gates, all on `eval.py`'s measured counts and none reduced:** ≥ 80 contributing nights per
  **EVALUABLE layer-endpoint pair**; ≥ 30 contributing nights dated after the lock commit; ≥ 30
  eligible rows with non-zero within-night variance in `subscore_j` on every E1/E2 contributing night;
  **Gate 0's ≥ 99% per-night and ≥ 95% whole-window reconstruction** on the in-window nights (tolerance
  0.05) and the **1% replay gate**; **≥ 10 distinct same-night B4 controls per slate member**
  (Correction 2 / Correction 12 — B4's pool, not B3's) on every E3 contributing night; ≥ 20 measured
  contributing nights for any sub-cell on item 25's closed reporting list.
- **ceiling:** DP-43's 12 months from a 2026-09-14 lock = **2027-09-14**. 2027-04-12 is **6.9 months**,
  2027-05-24 is **8.3 months** — both inside. **Not DEFERRED.**
- **lock-or-DEFER gate: CLEARED** — Q027's, on Q027's measurement: **0.6761 ≥ 0.36**, clear by 88%; the
  inequality was re-solved at the actual lock date (2026-09-14) and is unchanged. **Q029 locks with
  Q027, on the same number.**
- **`m`: 16 — fixed and closed** (item 22). EVALUABLE ×3: flow_strength, technical_structure,
  gex_alignment (ADDITION, w = 12.0), fundamental_quality (REMOVAL), catalyst_event; **projection: E3
  only**; **smart_money_confirmation: DEAD ×3**; fundamental's ADDITION side UNEVALUABLE.
  **BH: within-question 16 · F1 = 26 · F2 companion = 14**, larger q decides for E1ⱼ/E2ⱼ.

## Standing rules added

_none._ Nothing here is Haci's word: items 9 **and 10** were **DEFAULTED** under DP-43, which adds no
DP entry (DP-40) — the `record` pass changed nothing about that, and items 1–8 and 13–20 are applications of DP-02, DP-03, DP-06, DP-07, DP-09, DP-13, DP-20,
DP-21, DP-22, DP-23, DP-24, DP-25, DP-26, DP-28, DP-29, DP-42, DP-43, DP-44, DP-45, DP-49, DP-50,
DP-51 and locked precedent. The generalisable ones are listed below as **proposals**, for him to
confirm or drop.

## Standing rules proposed

- **The MPE for any per-night rank-correlation (IC) endpoint is 0.05 in Spearman-ρ units.** Haci's own
  number from H3. **This is the second question to need it** (Q027 proposed it first); H-082's decay
  series is the third. Deciding it three times invites three numbers. The entry should carry the tie
  caveat in the same sentence: an IC against a mostly-tied path-outcome rank is bounded well below 1,
  so the per-night touch base rate, the tied-block size and the **maximum attainable |ρ|** print
  beside any quoted ρ, and `IC_t` is **never rescaled** by them.
- **DP-20's doubling clause applies to the *premise*, not to the arithmetic shape.** A difference of
  two control-adjusted rates keeps **5.0 pp** where the two components are **paired within night over
  largely the same units against a shared control pool**; it doubles to **10.0 pp** where they are
  **independently estimated or rest on small independent cells** (Q007 P1, Q008 K1, Q012 P2, Q014 E1,
  Q022 E1, Q023 E1 — every precedent gave that reason, not the shape). Where the doubling is declined,
  the strict half is kept as a **blocking companion on the undiluted contrast**, not dropped.
- **An endpoint's evaluability is a counts question and is settled at lock.** Where an endpoint can
  fail for a coverage or arithmetic reason that has nothing to do with its effect — a layer the
  platform does not compute, an engine whose score does not reconstruct, a replay that does not
  reproduce the product — the desk routes a **counts-only feasibility request**, declares each
  endpoint EVALUABLE / DEAD / UNEVALUABLE at `record`, fixes `m` there and **never revises it**; an
  endpoint declared dead is never revived into `m`, and one that survives and then falls short of its
  floor stays in `m`.
- **A question that adopts another question's machinery by reference adopts its DECISIONS and its
  gate.** The reference is to the other PREREG **as it stands after its own `apply`**, the exposure
  count is **borrowed and named as borrowed**, no second count is routed for the same funnel, and the
  borrowing question **defers with the lending one** on the lending question's lock gate. Q027 → Q029
  is the first instance; Q028 → Q029's coverage rule is the second half of the same pattern.
- **Is DP-23's hourly-bar clause unconditional?** Two questions now (Q027, Q029) need a successor
  price freeze and use **no** hourly bar anywhere. This run applied DP-23 as written (Correction 4) —
  build them — because a Default is applied, not argued with. If Haci would rather the clause read
  "hourly bars for published symbols **where any endpoint needs intra-session ordering**", the DP-23
  row should be edited in place; until then the Steward builds them on every successor freeze.

**Added at `record` (2026-09-14) — five more, each one a thing R1b taught that will recur:**

- **A gate stated over "the whole freeze" is evaluated on the segment the question's window belongs
  to, whenever a config ship makes the earlier rows a different feature.** Q029's Gate 0 reconstructs
  at 84.77% from 2026-04-01 and 100.00% from 2026-06-01, and the gap is entirely one ship's worth of
  missing JSON fields. The rule that settles it without argument: **an arithmetic-reconstruction or
  coverage gate is measured on the engine vintage the question will actually read**, the whole-freeze
  figure is **printed beside it with the mechanism**, and the two are never quoted interchangeably
  (DP-06 / DP-50(a) extended from columns to formulas). Without it, every question whose window
  postdates a ship can be killed by rows it never touches.
- **A question that borrows another's exposure count borrows its whole schedule, out only.** Q029
  adopts Q027's window, decision date, extension date and hard stop **verbatim** and computes no date
  of its own that could land earlier. The corollary is what keeps "one machinery, two questions" true:
  one freeze, one exposure count, one maturity horizon, one decision date — and a borrowed schedule
  moves out with the lender, never in.
- **A sub-cell suppression list measured for one question transfers whole to a question that shares
  its funnel, population, contributing-night rule and window.** Re-measuring the same cells on the
  same nights produces a second number for one quantity. Q027 → Q029 is the first instance.
- **Name the pool a control floor governs.** Q029 carries two same-night pools — B4's distance-matched
  control pool (min 39) and B3's near-miss placebo pool (min 0, median 8) — and a floor of "≥ 10
  distinct controls" written without naming one of them would have struck half the nights and deferred
  the question on a bookkeeping artefact. Any floor on a draw pool names the pool, and a placebo pool
  smaller than the swap it simulates is impossible by construction (`k ≤ pool`) rather than a missing
  value.
- **A partial-correlation endpoint states which layers it is partial on, in the verdict sentence.**
  `projection` fails Q029's coverage floor, so every E2 controls for four layers and **not** for the
  largest-weighted one; a partial IC quoted without that list reads as controlling for the whole
  engine. The general form: an endpoint defined "given the other retained X" prints the retained set
  and names the exclusions wherever it is quoted or ledgered.
