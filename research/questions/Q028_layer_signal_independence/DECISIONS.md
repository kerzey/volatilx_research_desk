# Q028 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 5 items + 4 raised here (Gate 0 enforceability, script authorship and the standing re-run's owner, determinism/seed, the DP-50 sweep at lock) = 9

State read: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14T05:49:45Z) — in scope. No `results/` directory exists, no `eval.py` exists, and **no parquet, weekly, daily or results file was read to write this file**: every number below is a row count, a night count, a date or a policy id taken from the draft, from `research/data/exclusions_v003.json` (102 = 34 + 68 nights, 11 excluded, verified), from `research/BACKLOG.md` H-076 / the F8 header, and from locked precedent. **No item in this file is pending.** `## Schedule` is written here and is **final**; `record Q028` is not required.

## The headline

**All nine items are DECIDED. There is no DEFAULTED item, no ASK-class item and no routed request.**
None of R-1..R-4 is engaged: **no rule-14 exception is requested or needed** (every column is written with
the candidate at 16:05 on its own `trading_date`, DP-05 untouched, **DP-41 not engaged**); nothing encodes
how Haci trades — there is no entry basis, no lane, no ladder target, no "elite" cut and no position of any
kind (**DP-42 inapplicable**); nothing trades waiting against sample — the population is a **closed census
on a freeze taken 2026-09-10**, four days before the lock, with **zero accrual** (**DP-43 has no input**,
`rule: fixed`); and there is **no MPE in any unit** (**DP-10 / DP-20 / DP-44 inapplicable**, as §4 already
says — the one number that is not a Registrar convention, H-076's **0.80**, is Haci's own, taken as written
under **DP-25**, exactly as Q027 took his 0.05). **R-5 did not fire**: each item below has a DECIDE ground,
and where two options differed only in strictness the stricter was taken (**DP-45**).

All five drafted items go the Registrar's way on the option; **four of them are tightened** — the
tightenings are in the Choice column and in `## Corrections`, and **none of them weakens a floor, a
threshold, a gate or a CI clause**. The four items raised here are the ones the draft settles silently in a
way a DP entry or a CLAUDE.md rule does not permit to stay silent: three Gate 0 targets with no number and
no failure branch (the Q026 item-2 lesson), an unnamed RNG seed under rule 9, an ambiguous script owner, and
the DP-50 sweep the desk now records at every lock.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Which column carries the "agent-level fields" H-076 names | DECIDED | Option **A** — Tier 2 reads **`sas_candidates.score_details_json`** (`_serialize_score_details`, volatilx `services/super_agent_select_service.py:306-336`). **`market_regime_daily.component_scores_json` is not read anywhere in this question**, and §2.5's recorded correction stands as written. The register prints, once, the sentence that it is a **night-level, market-wide** object with four regime components (`models.py:1912`; `services/market_regime/scorer.py:506`) so the BACKLOG's wording cannot be re-borrowed by H-083, which cites the same phrase | ground 3 — one defensible answer: a night-level, one-row-per-night object **cannot enter a within-night cross-section of candidates**, so option B is not a stricter or looser test, it is not a computable one; **DP-25 is not offended** — the hypothesis's units, population and cuts are unchanged, the correction is a mis-named column, not a re-unit (Q026 item 1's "the list in the PREREG is authoritative and the script transcribes it"); Tier 2 **never decides** (§4.5), so this cannot move a verdict in either direction |
| 2 | Missingness handling for the matrices | DECIDED | Option **A** — **complete-case rows on the retained layer set** are primary, pairwise-complete printed as a sensitivity — **with the sensitivity made binding rather than decorative:** where the pairwise-complete matrix is positive semi-definite and its §8 criterion crossing **disagrees** with the complete-case primary on the same criterion in the same cell, **that criterion's line is INCONCLUSIVE (MIXED)**, never the favourable half. Where it is **not** PSD, that fact and the smallest eigenvalue are printed and the sensitivity is reported as uncomputable for S1/S2 (the arithmetic reason A is primary). The missingness-indicator matrix and per-night complete-case retention print beside the score matrix, always (§4.0, §10.2) | ground 3 — S1 and N_eff **are** eigenvalues, and a pairwise matrix can be non-PSD, so under B the two headline statistics are not interpretable; **DP-45** for the binding-disagreement clause — the pair differ only in strictness once B is a sensitivity, and the stricter reading is that a disagreement cannot be resolved in the verdict's favour; **Q027 DECISIONS #2 / #6** (keep the rejected option as a **binding companion**, not a footnote) |
| 3 | A layer that is null, constant or without within-night variance | DECIDED | Option **A** — **dropped from the matrix, named, counted, and read as *not an independent signal*** (REDUNDANT criterion (d)) — with three tightenings, all in §8: **(i) the dead-layer route is labelled.** A REDUNDANT verdict names its route — `REDUNDANT (correlation route)` via (a)/(b)/(c), `REDUNDANT (dead-layer route)` via (d), both routes named where both fire; both map to HISTORICALLY_CONFIRMED / `HISTORICAL_ONLY` and neither changes §9. **(ii) a criterion that turns on `K` must survive the coverage floor that works against it.** Criterion **(d)** requires `K ≤ 4` at the **70%** floor **and** at the **50%** floor; DISTINCT's `K ≥ 5` requires `K ≥ 5` at the **70%** floor **and** at the **90%** floor. Otherwise that line is **MIXED**. (Criteria (a)–(c) keep the two CIs of §4.6 as their guard and print the 50% / 90% sensitivities beside them — stated so the asymmetry is deliberate, not an omission.) **(iii) a dead-layer finding must print its cause.** The verdict sentence names each dropped layer with its null share, its distinct-value count, **its cause at `fa70688`** (`enable_smart_money_enrichment` / `enable_fundamental_enrichment` default `False`, `services/super_agent_select_models.py:110-111`; `gex_alignment` base weight `0.0`, `:9-17`; or absent context) and **the summed effective weight the dropped layers carry** | ground 3 — option B is **not computable without fabricating data**: a layer with zero within-night variance has no defined Spearman correlation and would have to be handed a unit eigenvalue that no variation in the data supports, which would inflate `N_eff` toward 7 by construction; **DP-45** for (ii), the floor working against each criterion, and threat §10.6 which says criterion (d) turns on the floor; **rule 10 / DP-31 / §9** for (i) and (iii) — a `K ≤ 4` verdict is a true statement about *this freeze's configuration*, and naming the route, the cause and the weight is what stops it being read as an architecture indictment that §9 already forbids acting on |
| 4 | Ledger the structure verdict alone, or hold it for H-075 | DECIDED | Option **A** — **ledgered on its own**, with the label fixed here and used verbatim wherever the verdict is restated: **"structure limb only — contribution untested (H-075)"**, alongside `HISTORICAL_ONLY` (DP-31) and `NON_QUOTABLE` (rule 12). §8's closing paragraph and the LEDGER entry both carry it; the joint H6 answer is assembled by the **Reporter** from ledgered verdicts only (the H-077 pattern), and **no architecture change follows from this question in either branch** (§9) | ground 2 — **Q026 precedent**: a diagnostic that reads no outcome is ledgered on its own with its label; ground 3 — H-083's setup rule and H-075's estimability scoping both take this register as an input (§9.1, §9.2), so holding it blocks two questions and buys nothing; **DP-29** (Q028 carries no primary and joins no correction set, so nothing downstream depends on the timing of its q); the hold option's only benefit — preventing a misreading — is delivered instead by the label and by §9's opening clause |
| 5 | The 11 `exclusions_v003` nights | DECIDED | Option **A** — **excluded from every verdict-carrying cell**, all-113-night version printed as a labelled sensitivity that **never decides, never promotes and never demotes** a verdict line. `eval.py` derives the exclusion set **from `research/data/exclusions_v003.json` at run time** (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs`, 11 nights → **102**: 34 in-sample, 68 sealed), never hard-coded, and `manual_runs.late_but_clean` nights are **kept**. A disagreement between the 102-night verdict and the 113-night sensitivity is reported as evidence **about the excluded nights**, not about the architecture | **DP-22** (the newest file, and v003 is the newest — v001/v002/v003 only exist); **DP-04**; ground 3 — on a re-run night the frozen row is a re-run's output 19–51 h after 16:05 (`sas_candidates_availability_note_correction`) and on 2026-06-26 the frozen row set contradicts the night's own run audit, so those cross-sections are **not the 16:05 cross-section this question is about**; **Q005 / Q026** precedent; **DP-45** direction |
| 6 | Gate 0's targets, made enforceable *(raised here)* | DECIDED | §4.1 items **(b), (c), (d), (e) are restated as pre-stated, binary, row-level conditions** — each keeps its gate status and none is relaxed. **(b)** B3(i) and B3(ii) are computed on **every included row, with no domain carve-out**; the registered arithmetic is the full chain §3 B3 names (effective weights `:682-722`, `cross_layer_bonus` `:1078`, `conflict_penalty` `:1116`, missing penalty `:1364-1368`, the +5 GEX-missingness offset and clamp `:1379-1399`, the ATR-elite block `:1401-1423`); a row class the script cannot reconstruct is **named, counted and left in the denominator**, and the target stays **R² ≥ 0.90**. **(c)** and **(d)** become **identities against that night's own `sas_runs.config_json` and the code at `fa70688`**, checked **row by row at relative tolerance 1e-6**: on every night whose config has `enable_smart_money_enrichment` false (or lacks the key — the code default at `services/super_agent_select_models.py:111` governs, and those nights are counted), the re-implemented `_effective_dimension_weights` gives `smart_money_confirmation` an effective weight of **exactly 0** on every row; and `gex_alignment`'s base weight parsed from every night's config is **exactly 0.0**. The **distributional shares those items currently gesture at** — null share, constant share, distinct-value counts — are **printed, not gated**. **(e)** becomes a **script-correctness gate**: Gate 0 fails if the catalyst layer is pooled across **2026-06-01** anywhere in a verdict-carrying cell (DP-06 is mandatory whether or not a difference is visible); the per-month catalyst panel either side of that date is **printed**, not gated. The two-pass bound and the **2026-10-12** hard stop are unchanged, and **no Gate 0 target is ever relaxed to make a pass succeed** | **Q026 DECISIONS #2**, in the same words: *"'arithmetically verified' without a tolerance is not a pre-registered rule"* — as drafted, (c) "consistent with PI-008", (d) "null share is material" and (e) "distribution differs" have **no number and no failure branch**, so they would be judged with the frozen rows in view, which **rule 9** forbids; ground 3 — a config-implied identity is checkable **without a magnitude guess**, and inventing a share threshold at draft would be a number with no source (**DP-25**, **DP-26**); **DP-45** for (b)'s no-carve-out reading — "rows where the registered arithmetic applies" is a domain chosen at run time, and the stricter reading keeps every row in |
| 7 | Who writes `eval.py`, and who owns the standing re-run *(raised here)* | DECIDED | The **Researcher** writes `eval.py` **once** from §4 as amended by these decisions (rule 9) **and runs the 2026-09-28 pass** — this is an ordinary question pass on a pinned parquet, not a Steward census, so Q026's split does not carry over and is not precedent here. **§9's standing re-run is the Data Steward's**: the **byte-identical** script, re-run at **every subsequent freeze** and **additionally whenever `sas_runs.config_json`'s hash changes**, published as `research/reports/LAYER_STRUCTURE_vNNN.md`. The header must name both roles so the ambiguity between the header ("Researcher writes and runs") and §9 ("registered here as a Steward step") is closed at lock | **rule 9** (the Researcher writes a deterministic `eval.py` once), which is not a preference the draft may re-open; ground 3 — the standing artefact is a freeze-triggered publication and the Steward owns freezes (**Q026 #3**, the KT register's shape); **DP-50(a)** — a successor freeze can disagree with its predecessor about the past, which is *why* the re-run is byte-identical and Steward-owned |
| 8 | Determinism: seed, draw counts, environment *(raised here)* | DECIDED | The PREREG names a **fixed RNG seed, `20260914`** (the lock date, the Q027 convention), used for **both** the B2 permutation reference (2,000 draws) and **both** bootstraps of §4.6 (2,000 resamples each), and `eval.py` **prints the seed, the draw counts and its library versions** in the register's header. A re-run under the bounded Gate 0 loop **reuses the same seed**; a pass that changes the seed is a new pass and is recorded as one with its diff and date | **rule 9** — "deterministic `eval.py`": 3 × 2,000 draws with an unnamed seed is not reproducible, and a register whose numbers cannot be re-derived cannot be a standing per-freeze artefact (item 7, §9); **DP-26** (a convention fixed at draft, derived from no outcome); **Q027 DECISIONS** (seed 20260914, same convention, same date) |
| 9 | DP-50(a)/(b) at lock, and which SHA the code is read at *(raised here)* | DECIDED | **Immaterial to the population by construction, and said so in the file rather than passed over:** Q028 reads a parquet frozen **2026-09-10** and pinned by sha256 (`sas_candidates` `af40ad8a…aaa2f2`, plus `sas_runs`), so no repair shipping after it reaches a single row — including **`2d5776c`** (PI-001), which touches `uoa_symbol_daily.fwd_return_*`, **a table this question does not read at all** (§2.4). It is **not** immaterial to the definitions: every code reference is read at **`fa70688bc252d14f8d67e371afafc194731c324e`** via `git show fa70688:<path>`, **never at HEAD**, and the register prints the SHA it read at beside the manifest SHA. **DP-50(b) runs forward, not backward, here**: a weights, multiplier, flag or scoring change shipped after this lock does **not** constrain any brief, because Q028's verdict is about the engine **at `fa70688` on 2026-04-01..2026-09-10**; it instead **fires §9's standing re-run** (item 7), and any repair rewriting historical `sas_candidates` rows still gets its dated `DATA_NOTES.md` entry as usual | **DP-50(a)/(b)/(c)**, **rule 4**; **§10 threats 5 and 11**; **Q026 DECISIONS #8** and **Q024 DECISIONS #17** are the precedent for running the sweep at lock and recording it **even when the answer is "none"** |

## Corrections to silent choices

**Seven.** The Registrar applies them at `apply` with the rest of this file. Every one tightens a clause;
none weakens a floor, a threshold, a gate, a CI requirement or a cell.

1. **§4.1 Gate 0 (b), (c), (d), (e) — three targets have no number and one has a run-time domain.**
   *(item 6)* **(b)** must read: B3(i) and B3(ii) are computed on **every included row, no domain
   carve-out**, target **R² ≥ 0.90**, with any unreconstructible row class **named, counted and kept in
   the denominator** — the draft's *"on rows where the registered arithmetic applies"* is a domain chosen
   while looking. **(c)** must read as a row-by-row identity at **relative tolerance 1e-6**: on every night
   whose `config_json` has `enable_smart_money_enrichment` false, or lacks the key (code default `False`,
   `services/super_agent_select_models.py:111`; those nights counted), the re-implemented
   `_effective_dimension_weights` gives `smart_money_confirmation` effective weight **exactly 0** on every
   row. **(d)** must read: `gex_alignment`'s base weight parsed from **every** night's `config_json` is
   **exactly 0.0**. **(e)** must read as a **script-correctness gate**: Gate 0 fails if the catalyst layer
   is pooled across **2026-06-01** in any verdict-carrying cell. The null shares, constant shares,
   distinct-value counts and the per-month catalyst panel are **printed, not gated**.
2. **§4.6 and §4.3 — no RNG seed is named anywhere.** *(item 8)* Add: **seed `20260914`**, fixed at lock,
   used for the B2 permutation reference (2,000 draws) and for both bootstraps (2,000 resamples each);
   `eval.py` prints the seed, the draw counts and its library versions in the register header; a Gate 0
   re-run pass reuses the same seed.
3. **Header, "Script" line, and §9 — the owner is ambiguous.** *(item 7)* The header must read:
   **"Script by: Researcher (rule 9, written once from §4) · First pass run by: Researcher, 2026-09-28, on
   the pinned parquet (DP-50(c)) · Standing per-freeze re-run: Data Steward, byte-identical script,
   published as `LAYER_STRUCTURE_vNNN.md`"**, and §9's "registered here as a Steward step" must name the
   Steward as the owner of the **re-run only**.
4. **§4.0 / §4.3 / §8 — the pairwise-complete sensitivity is printed but binds nothing.** *(item 2)* Add
   to §8: where the pairwise-complete matrix is PSD and its criterion crossing **disagrees** with the
   complete-case primary in the same cell, **that criterion's line is INCONCLUSIVE (MIXED)**; where it is
   not PSD, the smallest eigenvalue is printed and S1/S2 are reported uncomputable on it.
5. **§8 criterion (d) and the DISTINCT `K ≥ 5` clause — both turn on a Registrar convention (§10.6) and
   are tested at one floor only.** *(item 3)* Add: **(d)** requires `K ≤ 4` at the **70%** floor **and** at
   the **50%** floor; **DISTINCT** requires `K ≥ 5` at the **70%** floor **and** at the **90%** floor;
   otherwise that line is **MIXED**. Add the route labels `REDUNDANT (correlation route)` /
   `REDUNDANT (dead-layer route)`, and require the verdict sentence to name each dropped layer with its
   null share, distinct-value count, **cause at `fa70688`** and the **summed effective weight** the dropped
   layers carry.
6. **§8 closing paragraph and the LEDGER entry — the qualifier is described but not fixed as a label.**
   *(item 4)* The verdict is restated everywhere with the label **"structure limb only — contribution
   untested (H-075)"**, beside `HISTORICAL_ONLY` (DP-31) and `NON_QUOTABLE` (rule 12).
7. **§2.3 and §5.4 / §11.** *(items 5, and the standing Registrar step)* §2.3's all-113-night sensitivity
   must say it **never promotes and never demotes** a verdict line. §5.4 is replaced by `## Schedule`
   below, which is identical to it in every date and adds the gate and ceiling lines. §11 is replaced in
   full by a pointer to this file.

Checked and **not** corrections — each already matches the policy: **rule 5's price-path objective
correctly inapplicable**, with DP-01, DP-03, DP-08, DP-09, DP-11 and DP-12 cited as considered and no
entry basis, ladder target, touch, control cohort or fixed-horizon return anywhere; **no stop and no
excursion read** (DP-02, DP-27, DP-30 not reachable); **no MPE in any unit** and DP-10 / DP-20 / DP-44
named inapplicable, with the thresholds serving the MPE's role and fixed at draft (**DP-25** for H-076's
own 0.80, **DP-26** for the 70% coverage floor, the Spearman choice, the within-night standardisation,
the 90% Tier 2 parse floor and the ≤ 10-session episode gap); **DP-21** read in its strictest form —
102 / 34 / 68 nights, ≥ 20 contributing nights **and** a median ≥ 10 complete-case rows per night for any
verdict-carrying cell, with a short cell **demoted to descriptive at lock and printed, never dropped**
(**DP-43**'s demote-not-drop, applied although DP-43's schedule half has no input); **DP-24 unreachable by
design** with the projection printed as **0 contributing nights, exactly**, and **DP-31** applied on its
own terms — no outcome column, no price bar, nothing unsealable — with its successor clause resolving,
**for a diagnostic only**, to §9's standing re-run, and that reasoning written so it cannot be borrowed by
a question that reads an outcome (the Q026 wording); **DP-13 and DP-23 inapplicable** (nothing accrues, no
successor freeze, no price manifest at all); **DP-06** and rule 7 satisfied by the single 2026-06-01 cut
with "holds in one period only is not a result" made binding in §8; **rule 7's regime stratification**
correctly limited to nights ≥ **2026-06-09** and descriptive, with `market_regime_snapshot` kept distinct
as the whole-sample point-in-time descriptor (the Q005 §6 distinction); **DP-28** considered and applied
**only as a descriptive stratum**, correctly, since there is no published arm; **DP-51 applied as a gate,
not a footnote** — both CIs on every statistic in every cell, and a crossing that holds on the
night-clustered CI and not on the episode-clustered one is INCONCLUSIVE (and note this is the opposite
call from Q026, where DP-51 was stated as **not** applying because there was no CI to cluster — the
difference is that Q028 bootstraps); **rule 8** satisfied — F8's correction set stays **H-074 / H-081 /
H-083** and Q028 joins none, per the family header; **rule 12** — every number `NON_QUOTABLE`; **rule 9** —
one pass, no interim look, script written before the numbers; **DP-07 / DP-48 / DP-49** correctly governing
§9.3's PI route and any brief that follows; and **no rule-14 exception requested or needed** (**DP-05**
untouched, **DP-41** respected).

## Defaulted on Haci's behalf

**None.** No item in this question reached the ASK class. There is no rule-14 exception (**R-1**); nothing
that encodes how he trades — no level, lane, clock, entry basis, option structure or "elite" cut appears
anywhere in the file (**R-2**); no trade-off between waiting and sample, because the population closed on
2026-09-10 and the post-lock projection is **0 contributing nights, exactly** (**R-3**); and no MPE in
money, ATR or percentage points (**R-4**). Every item resolved to a DP entry, a CLAUDE.md rule, locked
precedent, or the stricter of two options that differ only in strictness; **R-5 did not fire**. The
Registrar's recommended option was taken in all five drafted items — four of them tightened, never
loosened — and the four items raised here exist because a silent choice in the draft was not compatible
with rule 9 or with the Q026 tolerance lesson.

## Routed requests

**No routed request.** Nothing here waits on another agent's number or artefact. **No Steward exposure
count is needed and none is a lock condition** (§5.2, the Q026 reading): the population is 102 of 113
already-frozen nights on a freeze taken four days before the lock, nothing accrues, so there is no
run-rate to measure, no projection to make, no arm to demote on a projection and no input for DP-43's
exposure-driven schedule. **No successor freeze is needed** (DP-23 inapplicable — the population is
complete at v001) and **no price manifest is needed at all**. The two handoffs in `## Schedule` are
ordinary work, not decisions: the Researcher writes and runs `eval.py`; the Steward owns the standing
per-freeze re-run afterwards (item 7).

## Schedule

**FINAL — written at `decide`, 2026-09-14; `record Q028` is not required and no item is pending.**

decision_date: **2026-09-28** (Monday) · extension_date: **none** — DP-13 is inapplicable: it answers "the
floors came up short at the decision date", and no floor can come up short on a census of already-mature,
already-frozen data (§5.1, §5.4) · hard_stop: **2026-10-12** (Monday) — the outer bound on §4.1's bounded
**two-pass** Gate 0 fix-and-re-run loop, each pass recorded with its diff and its date; Gate 0 still
failing there ⇒ **INCONCLUSIVE**, ledgered as such, register filed incomplete, script defect to the
Researcher · rule: **fixed** (not exposure-driven; the population closed 2026-09-10 and the measured
post-lock projection is **0 contributing nights, exactly**)

- **2026-09-14/15** — lock (`--by desk`, DP-46) once the Registrar has applied this file. Population pinned
  at `manifest_v001`; **no price manifest**; no freeze work is required for the lock.
- **by Friday 2026-09-25** — the **Researcher** commits `eval.py`, written once from §4 as amended by the
  Corrections above, with the exclusion set derived from `exclusions_v003.json` at run time (item 5) and
  the seed, draw counts and library versions printed in the register header (item 8).
- **Monday 2026-09-28** — the **Researcher** runs it on the pinned parquet, **Gate 0 first and read first**
  (§4.1, as restated by item 6). One pass, no interim look (rule 9). Output:
  `research/reports/LAYER_STRUCTURE_manifest_v001.md`.
- **after the verdict, standing** — the **Data Steward** re-runs the byte-identical script at every
  subsequent freeze **and** whenever `sas_runs.config_json`'s hash changes, publishing
  `LAYER_STRUCTURE_vNNN.md` (item 7; DP-50(a)).
- **gates:** none of the rule 6 effect-size form — there is no primary endpoint. The floors that do bind
  are applied in their strictest reading and **none is waived**: ≥ 20 contributing nights **and** a median
  ≥ 10 complete-case rows per contributing night for every verdict-carrying cell, met by the pooled
  (**102**), P0 (**34**) and P1 (**68**) cells; a `best_timeframe` stratum or a month below either is
  **demoted to descriptive at lock and printed, never dropped**. **DP-24 is unreachable by design and §8
  says so** (DP-31); **`HISTORICAL_ONLY`** labels the verdict in every branch, beside "structure limb only
  — contribution untested (H-075)" (item 4).
- **ceiling:** DP-43's 12 months is not engaged — the decision date is 14 days after the lock.

## Standing rules added

_none._ Nothing in this file is Haci's word: every item is an application of DP-04, DP-06, DP-21, DP-22,
DP-25, DP-26, DP-28, DP-29, DP-31, DP-41, DP-43, DP-45, DP-46, DP-48, DP-49, DP-50, DP-51, CLAUDE.md rules
4, 6, 7, 8, 9, 10, 12 and 14, and locked precedent (Q005, Q026, Q027). **No DP entry is added from a
DEFAULTED item** — and there is no DEFAULTED item here either. The generalisable ones are listed below as
proposals.

## Standing rules proposed (for Haci to confirm later)

- **A Gate 0 item states a number and a failure branch, or it is not a gate.** Where the expected fact is
  distributional and no number can be pre-stated without looking, the gate is written as an **identity**
  against the point-in-time config and the code at the frozen SHA (row by row, relative tolerance 1e-6),
  and the distribution is **printed, not gated**. (Item 6; second question in a row — Q026 item 2 was the
  first — and every future diagnostic will meet it.)
- **A printed sensitivity that contradicts the primary on the same criterion makes that criterion
  INCONCLUSIVE.** A sensitivity exists to be capable of changing something; where it is registered as
  descriptive only, the PREREG says which outcome it can and cannot move. (Items 2 and 5; the Q027 #2 /
  #6 "binding companion" shape, stated once.)
- **A verdict criterion that turns on a Registrar convention must hold at the convention and at the
  sensitivity value that works against it.** Here: the 70% coverage floor decides `K`, so criterion (d)
  is checked at 50% too and `K ≥ 5` at 90%. (Item 3; generalises to every band cut, clock and floor a
  Registrar fixes under DP-26 that a §8 criterion depends on.)
- **A deterministic script names its seed at lock.** Draw counts without a seed are not reproducible, and
  a register that is re-run at every freeze must be re-derivable to the digit. (Item 8.)
- **A diagnostic's verdict carries its scope in its own label.** "Structure limb only — contribution
  untested" travels with every restatement, the way `HISTORICAL_ONLY` does, so a half-answer is never
  quoted as the whole one. (Item 4; H-076/H-075, and the same shape will recur for H-077 and H-084.)
