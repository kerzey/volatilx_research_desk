# Q008 — decisions before lock
Run: 2026-09-13 by decision-maker · Source: PREREG.md "Open decisions before lock", 9 items
(+ 5 silent choices added as items 10–14, + item 15 from Haci's answer) · State: `PREREG_DRAFT`
(state.json confirms), PREREG uncommitted — these decisions are in scope.
**Recorded 2026-09-13:** question A answered by Haci (item 1; item 15 is how it is written up).

Question A is **answered** (the rule-14 exception, R-1, granted Q008-only). One route is out to the Data Steward
(R1, the DP-12 matched-control expected-n count); the R-3 it raises — night set and decision date —
goes to Haci **once**, with the Steward's numbers attached, exactly as Q007's R5 was handled
(DP-12 downstream note, Q007 DECISIONS.md). Nothing else is his.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Knowledge time: 16:00 ET on session t+2 for the F/S classification | ASK (question A) → **ANSWERED, Haci 2026-09-13** | **Yes, for Q008 only.** Bars through **16:00 ET on session t+2** may be used to label a pick fast-start / not — **for that classification and nothing else**. Every other input stays at **16:05 ET on the pick night**, and every outcome is measured **strictly after the classification moment** (sessions 3..40 for L4; `r` from `Cl_2`). He explicitly did **not** take the standing-rule option, so the exception is **question-scoped** and no other question inherits it. | R-1; DP-05 (amended in place 2026-09-13 to record this scope); Haci 2026-09-13 |
| 2 | Successor freezes and their symbol scope | DECIDED | Lock **now**, pinned to `manifest_v001` / `manifest_prices_v001`; `manifest_v002` (selections, nights after 2026-09-10) and `manifest_prices_v002` are built and pinned **at the decision date**, symbol scope = **every candidate on every night in the window, published and unpublished**, plus hourly bars for published symbols (the §4 counter-level tie-break needs them). §5's clause stands: if a successor price freeze omits unpublished-candidate symbols for a night, that night is excluded from K2 and counted, never back-filled. Build request is routed (R2) but does **not** block the lock. The *timing* half of this item is item 3. | DP-23; Q007 DECISIONS item 1; Q006 §5 |
| 3 | Night set vs speed (06-01..10-23 / decision 2026-12-28, vs 06-01..09-25 / decision ≈2026-11-30) | ROUTED → data-steward (R1) | waits on the matched-control contributing-night count and its run-rate. The choice is a waiting-vs-sample trade-off = **R-3**; it goes to Haci **once**, with the numbers attached, not now and not twice. The floor is never lowered to hit a date (DP-21, DP-12). | R-3; DP-12 downstream note (Q007 DECISIONS.md); Q007 items 2/17 pattern |
| 4 | Floor reading | DECIDED | **≥ 80 contributing nights per primary endpoint**, ≥ 20 contributing nights per reported sub-cell (cells below 20 SUPPRESSED) — the draft's reading, which is the stricter one. Per endpoint: K1/K3 = nights with ≥ 1 eligible F pick **and** ≥ 1 eligible S pick; **K2 = nights with ≥ 1 eligible F pick that has a non-empty control-F set** (the Q007 item-18 definition: the matched-control validity is part of "contributing"). | DP-21; Q007 DECISIONS item 18 + Corrections |
| 5 | MPEs (draft calls them placeholders) | DECIDED — **not placeholders, not re-asked** | **K1 = +10.0 pp** (DP-20's 5.0 pp is a floor that is never reduced; raised here for the Registrar's stated reason — a fast starter is mechanically closer to L4 at the clock — on the Q003 §8 / Q007 item 4a precedent for an endpoint carrying a known mechanical component). **K2 = +5.0 pp** (DP-20 exactly: a control-adjusted touch rate). **K3 = 0.25 ATR per trade** (DP-10, the standing number for every per-trade ATR-denominated endpoint; Haci set it 2026-09-12 and it is **not** re-asked). | DP-20; DP-10; Q003 §8; Q007 items 4a/4b |
| 6 | Fast-start clock, and whether a gap through L1 counts | DECIDED | **2 sessions** (H-031's "2 days"), as drafted; 1-session and 3-session variants stay clock-sensitivity secondaries. The **G0 exclusion is deleted** — not because the alternative was chosen, but as a consequence of item 10: with the entry at `C_t`, the overnight move is part of the path of a position that is already held, so an L1 touch at or through the t+1 open **is** a session-1 touch, and rule 5's "a target already passed at entry is not a hit" now bites at `C_t`, i.e. it is exactly the existing void rule `d1 ≤ 0` / `d4 ≤ 0`. Nothing is graded as a hit that was already passed at the entry price. | DP-25; DP-26; DP-11 (via item 10); rule 5 |
| 7 | Publication predicate | DECIDED | **`qualified IS TRUE AND selected_rank IS NOT NULL`** as drafted; dark-lane rows excluded from the treatment set and counted. **But the control pool is the complement of that predicate** — every same-night `sas_candidates` row that is not published, **including dark-lane rows** (see Corrections): rule 5 says "unpublished candidates from the same night", dark rows are unpublished candidates, this is the Q007 item-18 / R5 construction, and it is the stricter side (a control pool containing SAS's own strong-but-dark names raises the bar rather than lowering it). Q002/Q004/Q006's looser predicate is a Red Team matter for those questions, never an edit to a locked file. | DP-28; rule 5; Q007 DECISIONS item 18 and its Red Team list |
| 8 | 2026-07-02 / exclusions file | DECIDED | **Cite `research/data/exclusions_v002.json`** — header, §2 exclusions bullet and `eval.py` (`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates`, read from the JSON, no hard-coded dates). The v001 + "PREREG-cited 2026-07-02" fallback wording is deleted, not kept. Only 2026-07-02 falls inside the ≥ 2026-06-01 window, so the population is unchanged; the sealed-night count becomes **69**. | DP-22; Q007 DECISIONS item 6; DATA_NOTES |
| 9 | "New nights" clause in §8 clause 1 | DECIDED | The clause stays and is re-anchored: **≥ 25 contributing nights for that endpoint dated after the lock commit** (not "on or after 2026-09-11" — the lock commit is the blindness criterion, and it is the stricter anchor). DP-24's 30 is **not** imported here: it governs the PROSPECTIVELY_CONFIRMED clause, which is corrected separately (Corrections), and must not be double-counted into the historical track. If the Steward's R1 run-rate shows 25 post-lock contributing nights are unreachable inside the window Haci picks in item 3, **the date moves — the clause does not weaken**, and that move is part of item 3's single R-3. | DP-24 (scope); DP-21; DP-26; Q007 §10.13 blindness anchor |
| 10 | **Entry basis** (silent choice: the draft uses the next-session open `O_1`) | DECIDED — correction | **Pick-night regular-session close `C_t`**, for picks and distance-matched controls alike, as the proxy for the DP-03(a) after-hours fill. DP-11 is Confirmed and names this draft: *"Q008 and Q009 are drafts about picks that are already held, so their entry basis is `C_t` under DP-11 and is settled when their own open decisions are decided"* (Q007 DECISIONS, "Downstream effect of DP-11"). The fast start is a completed part of the path of a **held** position, which is DP-11's scope exactly. The real after-hours price `E_AH` (Q004's definition verbatim) is a **picks-only descriptive sensitivity** on the void / passed-at-entry filter and never decides. Not re-asked: Haci decided it on 2026-09-12. | **DP-11**; DP-03(a); Q007 DECISIONS items 12 and "Downstream effect of DP-11" |
| 11 | DP-12 status of K1 / K2 / K3 (silent: the draft gives all three equal licensing weight in §8) | DECIDED | **K2 is the DP-12 primary** — the only endpoint that can license a SAS-facing claim, a card flag or any §9 platform change, because it is the only contrast matched on the conditioning variable (control-F at the same ATR distances). K1 is the unmatched F-vs-S contrast: it stays a primary endpoint (it is H-031 as written, and it stays in the BH set of 3) but **licenses no rule on its own**. K3 is measured strictly after the clock, so the conditioning move is not inside it and no displacement offset is available or needed (unlike Q007 item 16); it is still an unmatched F-vs-S contrast and licenses no rule on its own. **One carve-out, stated so it is not read as a loophole:** a `playbook/` line that says *stop holding* (flatten at the session-2 close) may rest on K3's **absolute** F-hold gate — `mean_t mean_{p∈F,t}(r_p)` with its 95% CI entirely below 0 — because that is a statement about whether a trade Haci already makes pays, not a hit-rate claim (rule 5) and not a claim of a SAS edge. The §4 difference-in-differences stays a secondary. K2 as drafted (F pick minus its control-F mean) satisfies DP-12; it is not promoted to a double difference. | **DP-12**; rule 5; Q007 DECISIONS items 13/18/19 |
| 12 | Primary level and outcome clock (not listed as open; confirmed) | DECIDED | **L4 = `swing_trading.targets[1]`** stays the primary level (H-031 as written), on the **platform's own 40-session swing window**, outcome = first touch in sessions 3..40. **DP-09 is not extended to L4**: it is scoped to L3 as the primary level, and Q008's clock does not differ from the platform's lane window, so no R-2 arises. L4 within sessions 3..20 stays a NON_QUOTABLE secondary; 3..60 where matured. | DP-09 (scope); DP-26; PREREG §2, §4 |
| 13 | §10 threat 11 — are daily `o`/`h`/`l` regular-session values? | DECIDED | **Marked verified**, citing `research/reports/STEWARD_Q007_exposure.md` §R3 Part 1: **PASS 40/40** on the hourly cross-check, with the stated hourly-granularity caveat. `eval.py` must derive the 09:30/16:00 ET boundary **per date with `zoneinfo`**, never a fixed UTC offset (a fixed offset mis-flagged 2 of 40 pre-DST dates). No new route; the shared verification already exists. | Q007 DECISIONS item 11; R3 report |
| 14 | Same-session tie between a swing counter level and L4 (descriptive race) | DECIDED | **DP-27 governs, for picks and controls alike: an unorderable same-session tie counts counter-level-first** — the outcome less favourable to the hypothesis. The draft's "recorded as TIE" for controls (no hourly bars) is not a third category in any printed rate; the TIE count is printed separately *and* counted counter-first wherever a share is computed. | DP-27 |
| 15 | How the granted rule-14 exception is written into the PREREG | DECIDED | **§6 gains a "Rule 14 exception — human decision record" subsection in the Q007 §6.1 form**, with the same five parts: (i) **decided by** Haci, **2026-09-13**, relayed by the coordinator; his words: *"Yes, for Q008 only"*; (ii) **scope — fast-start classification only**: bars from sessions t+1 and t+2, up to **16:00 ET on session t+2**, may be used for exactly one purpose — assigning the **F / S** label (and setting aside **E4**) against levels anchored at `C_t`, for picks and B2 distance-matched controls alike; (iii) **not covered** — every other input (pick membership, direction, score/band, ladder levels, the entry price `C_t`, ATR, beta60, runup20, the control pool and its matching, regime label, calendar stratum) must have available_time **≤ 16:05 ET on the pick night**; the session-1/2 bars are **never** an entry price, **never** a level or synthetic-target anchor, and **never** a matching, filtering or stratifying input; (iv) **outcome use is not input use** — every outcome is measured **strictly after** the classification moment: L4 first touch in sessions **3..40**, `r` from `Cl_2` (the session-2 close), the counter-level race from session 3 on; (v) **what `eval.py` must enforce** — F/S/E4 and `rem` are computed and written to a frozen per-pick and per-control table **before any bar dated after session t+2 is loaded**; the run **fails** if the classification step references any field dated after session t+2's 16:00 ET close, or if a session-1/2 bar is referenced anywhere outside classification. §6's knowledge-time table row for **F / S / E4 / `Cl_2` / `rem`** reads available **16:00 ET, session t+2 — Rule 14 exception, Haci 2026-09-13 (§6.1), classification only**. **§10 carries the matching threat note**: the residual risk is leakage around the exception (a session-1/2 quantity silently entering matching, filtering, stratification, or an outcome window that starts too early), with the `eval.py` guard above as its stated mitigation, and the note says plainly that the exception is **Q008-scoped** (DP-05 as amended 2026-09-13) so no other question inherits it. | Item 1 (Haci 2026-09-13); Q007 §6.1 form; DP-05 |

## Corrections to silent choices

- **Header + §2 exclusions bullet — exclusions file.** "exclusions_v001.json … plus the confirmed
  re-run night 2026-07-02" → **`research/data/exclusions_v002.json`**, the fallback wording deleted;
  `eval.py` reads the JSON. §5's "70 per exclusions_v001, minus 07-02" becomes "**69 sealed nights
  per exclusions_v002**". (DP-22; item 8.)
- **§2, §4, §6 table, §10 threats 3 and 11, §4 secondaries — entry basis.** Every occurrence of
  "entry basis: next-session open `O_1`" becomes **pick-night close `C_t`** (DP-11; item 10). Concretely:
  - §2 "Path classification at entry": **X4 and G0 are deleted as separate cells.** "Passed at entry"
    is the existing void rule at `C_t` (`d1 ≤ 0` or `d4 ≤ 0`), already an exclusion, already counted.
  - §2 **F** becomes: L1 touched (`H_s ≥ L1` bullish / `L_s ≤ L1` bearish) for some s ∈ {1, 2}, with no
    G0 carve-out — a gap through L1 at the t+1 open is a session-1 touch of a position held since `C_t`.
    **S** is the complement. **E4** is unchanged (L4 touched by the clock → excluded from the primaries,
    counted, share of F printed).
  - §3 B2 step 2 is unchanged (synthetic levels were already built from the control's own close) and
    step 3 drops its X4/G0 branch.
  - §4 first paragraph and the "Close-to-close return from `O_1` at T+10 and T+40" secondary → from `C_t`.
  - §6 knowledge-time table: the `O_1` row is no longer an entry price; the t+1 open is just a bar
    inside sessions 1–2 and is covered by the **F / S / E4 / `Cl_2` / `rem`** row (16:00 ET, session t+2).
  - §10 threat 3 ("G0 removes the strongest starters") is **rewritten**: under the `C_t` entry there is
    no G0 removal, so the threat disappears and is replaced by its converse, disclosed — the fast-start
    group now contains picks whose L1 touch was an overnight gap, which is mechanically closer to L4 at
    the clock; that is the K1 confound of threat 1, handled by K2 (DP-12), the `rem` terciles and the
    difference-in-differences. The "gapped through L1" cell stays as a printed descriptive split of F.
  - §1 and §7 wording that says "after you buy it at the open" / "L1 within 2 sessions from the open"
    → "from the pick-night close". **§7's Q002 overlap paragraph must be re-stated**: Q002's S1 is
    measured from the **next-session open with `passed_at_entry` excluded**, so Q008's conditioning
    event is a different event on a different denominator; the two remain non-independent (same picks,
    overlapping nights) and are never presented as two confirmations, but they are not the same statistic.
  - §10 threat 13's "E-HOLD4 is an equity hold" sentence stands unchanged; `E_AH` is added as the
    picks-only descriptive sensitivity DP-11 requires.
- **§2 control pool — dark-lane rows.** "every `sas_candidates` row on night t with `selected_rank IS
  NULL`" and "Dark-lane rows are excluded from both the treatment set and the control pool" must read:
  the control pool is the **complement of the publication predicate** — every same-night row that is
  **not** (`qualified IS TRUE AND selected_rank IS NOT NULL`), i.e. `qualified = FALSE` rows and
  dark-lane rows alike; dark rows are excluded from the **treatment set only**, and their count is
  printed. (DP-28; rule 5's "unpublished candidates"; Q007 item 18 and its §R5 construction.)
- **§5 — "no coverage figure … and none may be requested".** Deleted. The DP-12 downstream note
  (Q007 DECISIONS.md) requires Q008's matched-control expected-n to be counted **before lock**, as
  Q007's R5 was, so the decision date is set once rather than extended twice. The request (R1 below)
  is scoped so that it reads **nothing about L4 and nothing beyond session 2** — Q008's own outcome
  stays sealed — and so that it never computes a picks-minus-control L1 difference, which is Q002's
  S1. §5's expected-n arithmetic is then **replaced by the Steward's returned figures**, cited to the
  report, in the Q007 §5 pattern; the "≈ 100 eligible nights" estimate stays only as the calendar
  arithmetic it is, labelled as such.
- **§8 MPE paragraph — not placeholders.** "MPE (placeholders; Haci to confirm at lock…)" must read:
  "**MPE: K1 +10.0 pp (DECISIONS.md item 5; DP-20 is the 5.0 pp floor, raised here because K1 carries
  a known mechanical proximity component — Q003 §8 / Q007 item 4a precedent). K2 +5.0 pp (DP-20).
  K3 0.25 ATR per trade (Haci 2026-09-12 → DP-10; the standing number for every per-trade
  ATR-denominated endpoint, not re-asked).**" (Item 5.)
- **§8 clause 1 — anchor.** "≥ 25 of them dated on or after 2026-09-11" → "**≥ 25 contributing nights
  for that endpoint dated after this file's lock commit**". The justification sentence is rewritten to
  say that the clause does not weaken if the count is short — the decision date moves instead (item 3's
  R-3). (Item 9.)
- **§8 PROSPECTIVELY_CONFIRMED clause.** "≥ 30 eligible pick nights on or after 2026-10-26 … with each
  contributing-night count ≥ 20" must read "**≥ 30 *contributing* nights for that endpoint**, dated on
  or after 2026-10-26 (which is after the lock commit), frozen separately and never inspected earlier,
  reproducing the sign of every confirmed endpoint under the unmodified `eval.py`". The "≥ 20" sub-clause
  goes (30 > 20); the clause does not weaken — if the window cannot supply 30, the date moves and that
  move is R-3. (DP-24; DP-21.)
- **§8 question-level table and §9 — DP-12 licensing (item 11).**
  - Row 2 (`K1 CONF+`, `K2 NULL/INCONCL.`, `K3 CONF+`): its licence "a `playbook/` line for Haci only"
    becomes "**descriptive; ledgered. No playbook line and no SAS claim** — an unmatched contrast
    licenses no rule (DP-12). A playbook line becomes available only under the row-4 absolute-gate
    carve-out, or if K2 is later CONFIRMED."
  - Row 4 (`K3 CONF −` → "fast start = take profit"): the playbook exit line is licensed **only when
    K3's absolute F-hold gate `mean_t mean_{p∈F,t}(r_p)` has its 95% CI entirely below 0**; the F−S
    difference alone does not license it.
  - Row 1 is unchanged (it already requires K2), and §9's "SAS continuation after a fast start" bullet
    keeps its K2 requirement explicitly: no `BAND_EXITS` variant and no card flag without K2 CONFIRMED
    in the same sign.
  - §4's K2 paragraph gains one line: "**K2 is the DP-12 primary: the conditioning variable is part of
    the price path, so only a contrast matched on it can license a rule; K1 and K3 are unmatched
    contrasts and are read under §8's table.**"
- **§7 family bookkeeping — H-063.** F4's enumeration must mark **H-063 as "merged into Q007"**
  (Q007 DECISIONS item 7; DP-29), so the family's BH set is Q007's primaries plus Q008's three, and
  H-063 is not counted as a further registered F4 question.
- **§4 counter-level race — tie rule.** "For controls, which have no hourly bars, it is recorded as
  TIE" must read "**counted counter-level-first (DP-27), with the TIE count printed separately**";
  the same rule applies to any pick tie hourly bars cannot order.
- **§10 threat 11 — mark verified**, citing `research/reports/STEWARD_Q007_exposure.md` §R3 Part 1
  (PASS 40/40, hourly-granularity caveat) and adding the `zoneinfo`/DST requirement on `eval.py`
  (item 13).
- **"Open decisions before lock" section — delete it entirely at apply**, once question A is answered.
  Nothing may be left in the file that reads as open at lock.

**Conflicts with already-locked questions (for the Red Team; the locked files stand, nothing is edited):**
- `Q002 §2`, `Q004 §2`, `Q006 §2` — publication predicate `selected_rank IS NOT NULL` only, looser than
  DP-28, and their control pools correspondingly mis-scoped from 2026-07-02 onward (dark-lane rows).
  Already on Q007's list; repeated here because Q008's §10 threat 5 raises it independently.
- `Q006` — `DATASET_PINNED` citing `exclusions_v001.json`, so its registered population includes the
  four KT-audit re-run nights (DP-22: the file it cites stands; flagged, not edited).

## Questions for Haci

### A. Q008 asks what happens after a pick reaches its first target fast. Nobody can know that on the pick night — it is only visible two sessions later, at the 4pm close on day 2. May the desk use that moment as the decision time for this one label?
Why yours: it is a new knowledge-time exception, and knowledge time is the rule that keeps every
result honest — only you widen it (R-1; DP-05).
- (Recommended) **Yes, for Q008 only** — bars through 16:00 ET on session t+2 may be used to label a
  pick "fast start / not", and for nothing else; every other input stays at 16:05 ET on the pick night
  and every outcome is measured strictly after that moment. Consequence: the question can be registered
  as a hold-or-flatten decision at the day-2 close — which is when the platform's conviction monitor
  already runs (16:02 ET) — and no other question inherits the exception.
- **Yes, as a standing rule** — any question whose subject is a hold-or-exit decision at a
  pre-specified later clock may use bars up to that clock **for classification only**, never for the
  outcome. Consequence: Q009 and future exit questions never ask again; the cost is that the principle
  is then applied without a fresh look each time.
- **No** — Q008 cannot be registered. A fast start is unknowable at 16:05 ET on the pick night, so
  there is no version of H-031 that fits the current rule; the hypothesis is withdrawn from the
  backlog and the F4 effort moves to H-032/H-033/H-064.
Answer: **Haci, 2026-09-13 — option 1, "Yes, for Q008 only."** Bars through 16:00 ET on session t+2
may be used to label a pick fast-start / not, for that classification and nothing else; every other
input stays at 16:05 ET on the pick night and every outcome is measured strictly after the
classification moment. He explicitly did **not** take the standing-rule option, so the exception does
not generalise: it is recorded as a scoped grant inside **DP-05** (edited in place 2026-09-13), with
no new `DP` id, and no other question inherits it. Applied by items 1 and 15.

**One more question will come, once and only once.** The Steward is counting how often the matched
comparison actually exists (R1 below). If it shows the question cannot reach its sample floor inside
the drafted window, the waiting-vs-sample trade-off — how long Q008 stays open — comes back to you as
a single R-3 question with the numbers attached (the Q007 pattern). It is not being asked now,
precisely so the date is set once.

## Routed requests

### data-steward

**R1 — Q008 matched-control expected-n, counts only, before lock.**
On frozen data only (`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`), please report **counts only** for Q008's fast-start classification and its matched control, on the **pick-night close** basis (DP-11, not the next-session open). Population: published picks under `qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28), non-excluded nights per `research/data/exclusions_v002.json`, pick nights ≥ 2026-06-01 whose **2-session classification window** has matured in the price freeze (i.e. through roughly 2026-09-08) — deliberately **not** the 40-session maturity filter, which is a pure calendar shift and would leave only ~28 nights; apply the PREREG §2 eligibility filters that need no bar beyond session 2 (has a lane-plan ladder with an L1 and an L4, `d1 > 0` and `d4 > 0` measured from `C_t`, `d4 > d1`, bars present). `C_t` = actual pick-night close from `prices_daily_split`, `dir` from `dominant_direction`, `ATR_p` = mean of the last 14 true ranges ending at t. A pick is **F** if L1 is touched (`H_s ≥ L1` bullish / `L_s ≤ L1` bearish) in session 1 or 2 — a gap through L1 at the t+1 open counts, because the position is held from `C_t` — and **S** otherwise; a pick whose L4 is touched in sessions 1–2 (**E4**) is set aside and counted. The control pool for night t is every same-night `sas_candidates` row that is **not** published under that predicate (including `qualified = FALSE` and dark-lane rows), symbol with ≥ 60 daily bars dated ≤ t; match as PREREG §3 B2 (standardized `beta60`, `atr_pct`, `runup20` by the night's median/MAD, nearest 10 by Euclidean distance, ties by symbol ascending), give each control synthetic levels at the pick's own ATR distances from the control's own close, and classify each control F/S/E4 from **its own** bars by the same rule. Please report: **(a)** the number of nights with ≥ 1 eligible F pick **and** ≥ 1 eligible S pick (the K1/K3 contributing-night definition); **(b)** the number of nights with ≥ 1 eligible F pick whose **control-F set is non-empty** (the K2 contributing-night definition), and the number with ≥ 1 such F pick **and** ≥ 1 eligible S pick; **(c)** the per-F-pick distribution of control-F set size (median, 10th percentile, minimum, share with ≥ 1), and the count and share of F picks with an **empty** control-F set — that number is a headline for §10 threat 2; **(d)** the monthly run-rate of (a) and (b), the projected date each reaches **80** contributing nights, and the projected number of contributing nights falling between 2026-09-16 and each of 2026-10-23 and 2026-11-30 (that is what §8 clause 1's "≥ 25 after the lock commit" is tested against); **(e)** the population funnel — picks removed by each of the no-ladder, void-at-`C_t`, non-monotone (`d4 ≤ d1`), missing-bar and E4 filters, plus the dark-lane row count. **Disclosure limits, please observe them literally:** read nothing about L4 touches or any level beyond what sessions 1 and 2 require, nothing beyond session 2 at all, no return, no adverse excursion, and **never** compute or report a picks-minus-controls difference on the L1 event or any L1 touch *rate* comparison between picks and controls — that difference is Q002's primary endpoint S1 and Q002 is `DATASET_PINNED` and unevaluated. Raw per-arm pick counts are fine and are not S1 (Q002 measures from the next-session open and excludes `passed_at_entry` picks; this measures from the close and does not), but please state that distinction in the report so no reader conflates them. What it decides: **only the night set and the decision date**, nothing about Q008's design, which is fixed before this returns — if the floor of 80 contributing nights per primary cannot be reached inside the drafted window 2026-06-01..2026-10-23 (decision 2026-12-28), that is a waiting-vs-sample trade-off (R-3) and goes to Haci with your numbers attached, never resolved by loosening the floor (DP-21) and never by falling back to the unmatched contrast (DP-12).

**R2 — successor freezes — due at the decision date, not a blocker for lock.**
When Q008 reaches its decision date (2026-12-28 as drafted, or whatever date item 3's R-3 settles on), build `manifest_v002` (selections, same SQL as v001, covering pick nights after 2026-09-10 through the end of the window, frozen after the window closes) and `manifest_prices_v002` (same Alpaca queries, `end` ≥ the 40th session after the last pick night — 2026-12-21 for a 2026-10-23 window end), with the symbol list covering **every candidate on every night in the window, published and unpublished** — the unpublished symbols' closes and forward bars are what the B2 distance-matched control is made of — plus hourly bars for published symbols for the counter-level tie-break. Scope is fixed by DP-23 and needs no further confirmation. `eval.py` records each sha256 and prints sealed (≤ 2026-09-10) and new (≥ 2026-09-11) night counts separately, and pre-lock vs post-lock counts for §8 clause 1.

## Standing rules added

**No new `DP` id was created.** Haci answered question A with the question-scoped option ("Yes, for
Q008 only") and explicitly declined the standing-rule option, so the answer does not generalise
beyond Q008 and a Confirmed entry of its own would misstate its reach.

Instead, **DP-05 was edited in place on 2026-09-13** so that the single rule-14 entry now records
**both** granted exceptions and their scopes — the Q007 §6.1 gap-group exception (session t+1 official
open, gap-group assignment only, Haci 2026-09-12) and this Q008 exception (bars through 16:00 ET on
session t+2, fast-start F/S classification only, Haci 2026-09-13) — and keeps its closing sentence
unchanged: **every *new* rule-14 exception is asked (R-1)**. Source cited for the addition:
`Haci 2026-09-13, Q008`. This is an addition to an existing Confirmed entry, not an overturn: nothing
in DP-05 was weakened and neither scope touches the other.

**Q009** needs nothing here: its decision pass already concluded that after its item 12 the question
reads no session-t+1-or-later quantity in any primary or eligibility filter, so it raises **no**
rule-14 exception and DP-05 is untouched by it (Q009 DECISIONS.md, item 12 correction and the "R-1"
line).
