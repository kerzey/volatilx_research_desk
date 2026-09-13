# Q009 — decisions before lock
Run: 2026-09-13 by decision-maker · Source: PREREG.md "Open decisions before lock", 8 items
(+ items 9–16, registrar-silent choices that a `DP` entry contradicts or that the applied decisions force)

State note: `research/questions/Q009_stop_whipsaw/state.json` does not exist and `PREREG.md` is
uncommitted — the question is pre-lock (PREREG_DRAFT) and these decisions are in scope. The state
file is initialised by the controller (registrar/coordinator), not here. No `results/` directory
exists and none was read.

**Summary:** 13 DECIDED, 3 ROUTED (all to the data-steward; R1 blocks the lock, R2 and R3 do not),
**0 ASK this pass** — every open item is covered by a `DP` entry, a locked precedent or one
defensible technical answer. The one genuinely-Haci item this question carries (R-3: whether P3
stays a primary endpoint under the DP-21 floor, and where the decision date and hard stop land) is
**unanswerable without the Steward's counts** and goes to him with the numbers attached, exactly as
Q007's questions C and E did. See "Questions for Haci".

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Exposure-only stop count (swing-stop coverage, wrong-side stops, TIGHT/MID/WIDE night counts) | ROUTED → data-steward (**R1**, blocks the lock) | Waits on the counts in "Routed requests" R1. What it decides: (a) whether eligible **contributing** nights (DP-21) can project to 80 by the hard stop — if not, the blocker is that the printed stop is not populated, i.e. a data problem, and Q009 goes to `research/questions/DEFERRED.md` instead of being locked; (b) whether **P3 stays a primary endpoint** — it now needs ≥ 80 TIGHT-contributing nights, not 20 (item 10); (c) the decision date and hard stop, set **once** on the matched (B1-valid) definition so they are not moved twice as Q007's were. (a), (b) and the date are R-3 → Haci **with the numbers attached**, never decided here and never by loosening a floor. | DP-21; DP-12 downstream note (Q007 DECISIONS.md); Q007 items 2, 17 |
| 2 | Successor freezes (`manifest_v002`, `manifest_prices_v002`) | DECIDED (+ routed **R2**, not a blocker) | **Lock Q009 now, pinned to `manifest_v001` / `manifest_prices_v001`**; the successors are built and pinned **at the decision date**, with symbol scope = **every candidate on the new nights, published and unpublished** (B1 needs the unpublished symbols' closes and forward bars), plus hourly bars for published symbols (P2/P3 same-session tie-breaks). §5's clause stands: nights whose unpublished-candidate bars are missing are excluded from P1 and counted, never back-filled. Build order is in "Routed requests" R2 and does **not** block the lock. | DP-23; Q006 §5; Q007 item 1 |
| 3 | Stop line | DECIDED | **The printed swing-lane stop, paired with L3** — the printed stop of the lane whose target is the primary endpoint. The pick's own `best_timeframe` lane is **not** used (it would make the stop line vary pick by pick and would break the one-lane pairing with L3); the printed swing **invalidation** line stays a secondary run through the same P1/P2 constructions, descriptive; day lane (day stop ↔ L1) and long lane (long stop ↔ L5) stay secondaries. | DP-30; DP-09 (L3 is the primary level); Q007 item 8 |
| 4 | Stop-distance buckets | DECIDED | **As drafted, on `s_close`: TIGHT `0 < s < 1.0`, MID `1.0 ≤ s < 2.0`, WIDE `s ≥ 2.0` ATR.** A registrar-chosen band stands provided it was not derived from sealed outcomes, and §6's disclosure establishes that the 1-ATR unit is the desk's existing Q004 adverse line, not an EXPLORE_001 figure. §2's sentence "the cut points are a registrar choice and an open decision for Haci" is deleted. Under item 12 the bucket variable and the entry-relative stop distance become the **same quantity**, which is what the bucket name is meant to mean. | DP-26; PREREG §6 disclosure |
| 5 | MPEs | DECIDED | **P1: 5.0 pp** (control-adjusted touch-rate endpoint, the desk's standing number; P1 is a single control adjustment, not a difference of differences, so Q007's raised 10.0 pp does not carry over). **P2: 0.25 ATR per trade. P3: 0.25 ATR per trade.** The draft's 0.20 / 0.30 are placeholders written before Haci set the number; DP-10 fixes every per-trade ATR-denominated endpoint at 0.25 ATR and is **not re-asked**. P3 does not get a larger MPE than P2: DP-10 allows a larger one only with a Registrar reason, and "a wider stop raises risk per share" is an argument about position sizing, not about the per-trade ATR effect the endpoint measures. | DP-10 (Haci 2026-09-12, Q007 question B); DP-20; Q007 item 4b and its Q009 downstream note |
| 6 | Tie rule (unresolved same-session stop/target) | DECIDED | **P2/P3: stop fills first**, as drafted — hourly bars in time order first; if one hourly bar holds both levels, or the symbol has no hourly bars, the stop fills first; the count is printed. **P1 keeps SAME_SESSION = 0** (not a whipsaw) on daily bars for picks and controls alike: that is the same conservative principle in P1's direction (the outcome less favourable to the hypothesis) and it keeps picks and controls graded identically, which hourly-only-for-picks would not. The two rules are not harmonised into one; each is the conservative reading of its own endpoint. | DP-27; PREREG §4, §10.3 |
| 7 | Exclusions file | DECIDED (+ routed **R3** for 2026-06-26) | **Cite `research/data/exclusions_v002.json`** in the header, in §2 and in `eval.py` (`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates`, read from the JSON, no hard-coded dates). The "exclusions_v001 plus the PREREG-cited re-run night 2026-07-02" fallback and the "if Haci issues v002 before lock" conditional are **deleted, not kept** — v002 exists and carries all four KT-audit re-run nights, of which 2026-07-02 is the one inside this window. The **2026-06-26 mixed-state night** (§10 threat 11) and the E9a historical-payload question (§10 threat 6) are a Steward ruling, not a Haci decision: routed as **R3**; if either shows `public_payload_json` was mutated after publication, the Steward issues `exclusions_v003.json` before the batch is locked and the PREREG cites that instead (DP-22's mechanism, no new decision). | DP-22; Q007 item 6 |
| 8 | Family: F4 vs F6 | DECIDED | **F6 — Exits and execution**, and `research/BACKLOG.md` H-032 is **re-filed from F4 to F6** by the Registrar when applying. DP-29 assigns a question by its **primary endpoint's subject**, and §8 is explicit that only **P2 or P3** can license a rule — both are the realized result of using the printed stop as an **exit** (the H-050 shape: exit rule vs no exit rule). §7 is rewritten: F6 holds H-050, H-051, H-052 and H-032; Q009 is the only registered F6 question, so the family correction is over Q009's own primaries today. **Anti-leniency clause (binding):** because P1 *is* a path-after-selection endpoint, the Reporter prints for P1 **two** q-values — BH within F6, and BH as if P1 were an F4 primary alongside the registered F4 primaries (Q007's four) — and **P1's verdict uses the larger (more conservative) q**. The family move must not make any endpoint easier to confirm than it was in the draft. | DP-29; rule 8; PREREG §8 ("a rule requires P2 or P3") |
| 9 | Primary clock: 40 sessions (drafted) vs 20 | DECIDED — **Correction** | **The primary clock is L3 within 20 sessions measured from the stated entry**, for P1, P2 and P3; the 40-session version of each is reported alongside, descriptively, wherever it has matured. DP-09 is Confirmed and was generalised in place on 2026-09-13 precisely so that it attaches to the level and the horizon, not to the entry basis: when L3 is the primary level the clock is 20 sessions, not the platform's 40-session swing-lane window, and **floors and decision dates are computed on the 20-session window**. It is also the conservative direction for this hypothesis — a shorter window gives the "recovered anyway" leg less room, so P1 and P2 both understate a whipsaw rather than overstate it. Nothing is lost: the 40-session numbers are still produced. | DP-09 (Haci 2026-09-12, Q007 question A); Q007 §4 |
| 10 | Sample floors: the floor reading | DECIDED — **Correction** | **≥ 80 contributing nights per primary endpoint, ≥ 20 contributing nights per reported sub-cell.** The draft's "≥ 20 eligible nights per reported cell, ≥ 80 eligible nights total" with "for P3 ≥ 20 TIGHT-cell nights" is exactly the weaker reading DP-21 rules out. **P3 is a primary endpoint, so P3's floor is 80 TIGHT-contributing nights**, not 20. Contributing night: for P1 — a night with ≥ 1 eligible pick **with a valid B1 control set**; for P2 — a night with ≥ 1 eligible pick; for P3 — a night with ≥ 1 eligible **TIGHT** pick. The floor is not loosened to keep P3; if the Steward's count (R1) cannot project 80 TIGHT-contributing nights by the hard stop, P3 drops to descriptive and the within-question BH runs across 2 — and **that drop is R-3, Haci's, with the numbers attached**. | DP-21; Q007 Corrections (same reading), Q008 §5 |
| 11 | Publication predicate | DECIDED — **Correction** | §2's "every published pick (`selected_rank IS NOT NULL`)" becomes **`qualified IS TRUE AND selected_rank IS NOT NULL`**; dark-lane rows are excluded from the treatment rows, and the B1 control pool is the **complement** of that predicate (same-night rows that are not published — qualified-false and dark-lane rows alike). | DP-28; Q007 item 18 / Corrections |
| 12 | Entry basis | DECIDED — **Correction** | **Entry is the pick-night regular-session close `C_t`** (`prices_daily_split`), the DP-03(a) after-hours proxy, **for picks and controls alike** — not the next-session open the draft uses. DP-11 is the standing rule for this batch and the Q007 pass recorded it explicitly ("Q008 and Q009 are drafts about picks that are already held, so their entry basis is `C_t` under DP-11"); a desk pass does not revert a recorded instruction of Haci's ("*measure the movement of the stock from closed price of previous day not opening prices*"). It is also the better geometry for this question in particular: the bucket variable `s_close` becomes the **actual entry-relative stop distance**, so TIGHT means what it says; the "stop at or through the entry" and "target at or through the entry" exclusions vanish (the wrong-side-of-`C_t` checks already cover them), so the picks whose stop was breached overnight — the most stop-relevant picks of all — are **graded instead of dropped**; and no forward bar is needed to decide eligibility, which is what lets R1 be a genuine no-forward-bar count. The **next-open basis is kept as a descriptive sensitivity** on picks and controls, and the real after-hours price `E_AH` (Q004's definition verbatim) as a **picks-only** descriptive sensitivity; neither decides. | DP-11; DP-03(a); Q007 item 12 and its Q009 downstream note; rule 5 (one basis on both sides) |
| 13 | Rule-5 stop-exit exception — its scope | DECIDED | The exception stands but is **written narrowly**: the printed stop is used as an exit **only inside the named execution plan E-STOP, and only in P2/P3**. In P1 and in **every** touch-rate, first-touch, excursion, counter-touch and scale-out figure in the file the stop is a measurement line and no position is ever exited on it; adverse excursion and counter-direction touches are reported, not used as exits. The results header and `REPORT.md` carry one sentence naming the exception and citing rule 5 and DP-02, so the desk's default ("stops are never assumed") is not read as having moved. | DP-02; rule 5 ("unless the PREREG says otherwise"; named execution plans) |
| 14 | Does DP-12 apply (matched control on a path-derived conditioning variable)? | DECIDED | **No.** Q009's conditioning variable is `s_close = dir × (C_t − S) / ATR` — the printed stop and the pick-night close, both **known at publication**; no part of it is a completed piece of the forward price path, so DP-12's matched-conditioning requirement does not fire. The Q007 downstream note ("check at decision time whether Q009's conditioning variable is path-derived") is hereby **closed: it is not**. The rule-5 distance-matched control **B1 stays as drafted** for P1 (it is required by rule 5 regardless of DP-12), and its availability is counted **before** lock in R1 — which is the part of DP-12's downstream note that does bind here, so the decision date is set once. | DP-12 (scope); rule 5; PREREG §2, §3 |
| 15 | Block bootstrap length | DECIDED — follows item 9 | **Expected block length 10 sessions** (20-session forward windows overlap across adjacent nights), 2,000 resamples, date-clustered CI printed alongside. The drafted 20 was Q006's length for a 40-session window; the 40-session descriptive companions are printed with the 20-session block and that is stated. | Q007 §4; Q006 §4; item 9 |
| 16 | PROSPECTIVELY_CONFIRMED clause | DECIDED — **Correction** | "≥ 30 eligible pick nights after this file's lock commit (and, for P3, ≥ 20 TIGHT-cell nights among them)" becomes **"≥ 30 *contributing* nights for the confirming endpoint dated after this file's lock commit"** — TIGHT-contributing for P3 — frozen separately, never inspected earlier, reproducing the sign under the unmodified `eval.py`. The clause does not weaken; if the window cannot supply 30, the decision date moves and that move is R-3. | DP-24; DP-21 |

## Corrections to silent choices

Applied by the Registrar with the rest; each is a `DP` entry the draft contradicts, or an edit the
decisions above force.

- **§8 MPE paragraph — the MPEs are not placeholders.** "**MPE (placeholders — Haci to confirm at
  lock…)**", "**P2: 0.20 ATR per trade**", "**P3: 0.30 ATR per trade**, higher because…" and the
  sentence "The P2/P3 MPEs have **no desk-derived basis** … Haci should set them from how much
  per-trade difference would make him stop honouring a printed stop" are stale: Haci set the number
  on 2026-09-12 (Q007 question B → DP-10). It must read: "**MPE: P1 5.0 pp (DP-20, the standing
  control-adjusted touch-rate number). P2 0.25 ATR per trade and P3 0.25 ATR per trade (Haci
  2026-09-12 → DP-10; the standing number for every per-trade ATR-denominated endpoint, not
  re-asked).**" (DP-10; DP-20; item 5.)
- **Header, §2 exclusions bullet — exclusions file.** Cite `research/data/exclusions_v002.json`;
  delete "exclusions_v001.json … plus the confirmed re-run night 2026-07-02" and the conditional
  "If Haci issues `exclusions_v002.json` before lock, `eval.py` reads it instead and this bullet
  becomes a pointer" — v002 exists, so the bullet **is** the pointer. `eval.py` reads
  `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` from the JSON; no hard-coded dates.
  (DP-22; item 7.)
- **§2 treatment rows — publication predicate.** "every published pick (`selected_rank IS NOT NULL`)"
  → **`qualified IS TRUE AND selected_rank IS NOT NULL`**; §3 B1's "same-night unpublished
  `sas_candidates` rows" → "same-night rows that are **not published** under that predicate
  (qualified-false and dark-lane rows alike)". (DP-28; item 11.)
- **§4, §2, §5, §7, §8, §10 — the primary clock is 20 sessions, not 40.** Every primary-endpoint
  definition (P1's `k_S`/`k_T`, P2's E-STOP/E-NOSTOP terminal exit, P3) runs on **k = 1..20** with
  the terminal exit at the **session-20 close**; the 40-session version of each is produced and
  labelled "descriptive, does not decide". §2's closing line ("Levels and windows are the platform's
  own: L3 lane window 40 trading sessions") keeps the platform citation but reads that the **primary
  clock is 20 sessions from the stated entry (DP-09), with the platform's 40-session lane window
  reported alongside**. §5's maturity arithmetic ("Binding maturity: 40 sessions", the "≈ 28 nights"
  and "80th eligible night ≈ 2026-09-25 → matures ≈ 2026-11-20" lines) is **recomputed on a
  20-session maturity** from the Steward's R1 counts, not re-estimated by hand. §10 threat 8 reads
  "overlapping **20-session** windows … block length fixed here (10 sessions)". Day-lane (L1/20) and
  long-lane (L5/60) secondaries are unchanged. (DP-09; item 9.)
- **§4 Inference — block length.** "expected block length **20 sessions** (40-session forward windows
  overlap …; Q006's length for a 40-session window)" → "**expected block length 10 sessions**
  (20-session forward windows overlap across adjacent nights; Q007 §4)". (item 15.)
- **§4, §2, §3 — entry basis.** "**Entry basis: next-day open** (`X = O_{t+1}`…)" → "**Entry basis:
  pick-night regular-session close `C_t`** (`prices_daily_split`), the DP-03(a) after-hours proxy,
  for picks and controls alike (DP-11; DECISIONS.md item 12)". Consequential edits, all mechanical:
  - §2 definitions: delete `X = O_{t+1}`, `s_open`, `d_open`; keep `s_close = dir × (C_t − S)/ATR`
    as **both** the bucket variable and the grading stop distance, and add
    `d_close = dir × (T − C_t)/ATR` as the target distance.
  - §2 exclusions: delete the "stop at or through the entry (`s_open ≤ 0`)" and "L3 at or through the
    entry (`d_open ≤ 0`)" bullet — the wrong-side-of-`C_t` bullets for the stop (`s_close ≤ 0`) and
    for L3 already cover it on this basis, and nothing is dropped for a level breached overnight.
    Keep every other exclusion, each counted and printed, per bucket.
  - §3 B1: place the control's levels off the **control's own close**,
    `S_c = C_c × (1 − dir_p × s_close,p × atr_pct_c)`, `T_c = C_c × (1 + dir_p × d_close,p × atr_pct_c)`,
    graded from the control's own close, same direction, same 20-session window, same daily-bar rule
    (the Q007 B3 anchoring pattern, moved from the open to the close).
  - §4 plans: session index k = 1..20 with **k = 1 = session t+1, entered at `C_t`**; the
    "opens through … (k ≥ 2)" gap-through clauses become **k ≥ 1**, so a session-t+1 open through the
    stop fills at that open and an open through L3 fills there too. Rule 5's "a target already passed
    at entry is not a hit" is carried by the wrong-side-of-`C_t` exclusion.
  - §4 secondaries: add the **next-open entry basis** (picks and controls) and keep `E_AH` as a
    **picks-only** sensitivity — both "descriptive, does not decide".
  - §6 knowledge-time table: the `X = O_{t+1}` row moves to the secondaries (sensitivity only), so no
    session-t+1 quantity enters any primary or any eligibility filter; note explicitly that Q009
    needs **no** rule-14 exception (DP-05 is untouched, no R-1 arises).
  - §10 threat 2 ("the stop is anchored to the lane entry, not the close or the open") keeps its
    wrong-side headline counts, now per bucket on the close basis. Add one clause to §10 threat 4:
    the close is not a tradable price (SAS publishes after the close), so `C_t` is a proxy for an
    after-hours fill, and the `E_AH` sensitivity shows the picks-only difference (DP-11).
  (DP-11; DP-03(a); item 12.)
- **§5 floors, §8 clause 1 — the floor reading.** "≥ **20 eligible nights per reported cell**, ≥ **80
  eligible nights total** … For P3 the cell is nights with ≥ 1 eligible TIGHT pick" must read
  **"≥ 80 contributing nights per primary endpoint — P1: nights with ≥ 1 eligible pick carrying a
  valid B1 control set; P2: nights with ≥ 1 eligible pick; P3: nights with ≥ 1 eligible TIGHT pick —
  and ≥ 20 contributing nights per reported sub-cell (bucket, tape stratum, half, band, bull/bear,
  regime)"**. §8 clause 1 becomes "contributing nights ≥ 80 for that endpoint". §5's pre-lock P3
  clause changes accordingly: "**If TIGHT-contributing nights project below 80 by the hard stop, P3
  is removed from the primaries before lock**" — the number 20 in that clause is wrong. (DP-21;
  item 10.)
- **§8 PROSPECTIVELY_CONFIRMED.** "≥ 30 eligible pick nights occurring after this file's lock commit
  (and, for P3, ≥ 20 TIGHT-cell nights among them)" → "**≥ 30 contributing nights for the confirming
  endpoint dated after this file's lock commit**" (TIGHT-contributing for P3). (DP-24; DP-21;
  item 16.)
- **§5 exposure-count paragraph — what the Steward may read.** "**no bar after night t is read** (not
  even `O_{t+1}`)" is **kept and now consistent**, because item 12 removes the open from every
  eligibility filter. Add that the count is also run on the **B1-valid** definition (same-night
  non-published candidates with ≥ 60 daily bars dated ≤ t) so the decision date is set once, and that
  it reports the null-stop share **by month and by score band** (§10 threat 10 cannot be read
  otherwise). (item 1; DP-12 downstream note.)
- **§5 decision date and hard stop — recomputed, not re-estimated.** The drafted "first Monday on or
  after **2026-11-23** … hard stop **2027-01-25**" was derived from a 40-session maturity and a
  20-night P3 floor, both now wrong in opposite directions. The **rule** stays in form — the first
  Monday on which every retained endpoint shows ≥ 80 contributing nights (DP-21), evaluation runs
  regardless on the hard stop, any endpoint below floor is INCONCLUSIVE (SUPPRESSED) — and the two
  **dates** are set from R1's counts and projections, in one pass. If the projection puts an endpoint
  past the hard stop, that is R-3 and goes to Haci with the numbers; it is never met by lowering a
  floor. (DP-21; DP-24; Q007 items 10 and 20 — the Registrar should note that Q007 moved its stop
  twice for exactly this reason and set Q009's once.)
- **§2 / §1 — the bucket sentence.** "the cut points are a registrar choice and an open decision for
  Haci" → "the cut points are fixed here (DP-26; DECISIONS.md item 4)". (DP-26; item 4.)
- **§4 — the rule-5 stop exception, narrowed.** "**Stops are assumed in this question, and only here**
  … In P1 it is a measurement line. Everywhere else stops are not assumed." is kept and extended by
  one sentence: "**The exception is confined to plan E-STOP in P2 and P3. Every other figure in this
  file — P1, every touch rate, first-touch session, adverse excursion, counter-direction touch and
  the committed L1–L6 scale-out — is graded with no stop, and the same sentence is printed in the
  results header and in `REPORT.md` (rule 5; DP-02).**" (DP-02; item 13.)
- **§7 — family.** "**Family:** F4 Price behaviour after selection (hypothesis H-032)" in the header
  and §7's "Across the family: F4 …" become **F6 Exits and execution** (H-050, H-051, H-052, H-032);
  Q009 is the only registered F6 question, BH runs across its own 3 primaries (2 if P3 is dropped),
  and the F4 paragraph naming Q007's primaries is replaced by the **dual-q clause for P1**: the
  Reporter prints P1's q both within F6 and as if P1 were an F4 primary alongside the registered F4
  primaries, and **P1's verdict uses the larger q**. `research/BACKLOG.md` H-032 is re-filed from F4
  to F6 with the note "registered as Q009"; the F4 list drops to 6 hypotheses and §7's overlap
  paragraph (H-033, H-058, H-060, Q004, Q007) is kept unchanged — none is merged. (DP-29; rule 8;
  item 8.)
- **§10 threats 6 and 11 — routed, not left as "the Steward should".** Both now read that the ruling
  is requested before lock as DECISIONS.md R3, and that if `public_payload_json` was mutated after
  publication on 2026-06-26 (or on the E9a-affected historical rows) the Steward issues
  `exclusions_v003.json` and the PREREG cites it under DP-22. (DP-22; item 7.)
- **"Open decisions before lock" section — delete it entirely** once the above are applied. All eight
  items are decided here or routed; nothing may be left in the file that reads as open at lock. After
  applying, `grep` the file for `0.20 ATR`, `0.30 ATR`, `placeholder`, `O_{t+1}`, `40 trading
  sessions`, `2027-01-25`, `2026-11-23`, `exclusions_v001`, `open decision` — every hit must be gone
  or deliberate (the 40-session descriptive companions and the day/long-lane secondaries are the only
  legitimate survivors of the window greps).

**Conflicts with already-locked questions (for the Red Team; the locked files stand, nothing is edited):**
- `Q006 §4 E1` — primary endpoint is **L3 within 40 sessions**, with floors and the floor date
  computed on that window. DP-09 (Confirmed 2026-09-12, generalised in place 2026-09-13) makes the
  primary clock for an L3 endpoint **20 sessions from the stated entry**, with 40 descriptive. Q006
  locked before DP-09 existed and is not edited; flagged for Q006's Red Team review so the two
  questions' L3 numbers are never read side by side as if they were on one clock.
- `Q004 §2`, `Q006 §2` — publication predicate is `selected_rank not null` only, looser than DP-28.
  (Already flagged in Q007's DECISIONS.md; repeated here only so the flag is not lost.)

## Questions for Haci

**None this pass.** Every open item in the draft is settled by a `DP` entry (DP-09, DP-10, DP-11,
DP-20, DP-21, DP-22, DP-23, DP-24, DP-26, DP-27, DP-28, DP-29, DP-30), by a locked precedent, or by
one defensible technical answer, and no item on the Reserved list is answerable today:

- **R-4 (MPEs)** — already set: DP-10's 0.25 ATR governs P2 **and** P3; DP-20's 5.0 pp governs P1.
  Asking again would be the second time for the same number.
- **R-2 (horizon, level, lane)** — already set: DP-09 (L3 within 20 sessions) and DP-30 (the swing
  lane's printed stop, the lane whose target is the primary endpoint).
- **R-1 (knowledge time)** — none arises: after item 12 the question reads no session-t+1 quantity in
  any primary or eligibility filter, so DP-05 is untouched.
- **R-3 (waiting vs sample size)** — this is the one question Q009 owes Haci, and it **cannot be put
  to him yet**. P3 now needs 80 TIGHT-contributing nights rather than 20 (DP-21), swing-stop
  coverage has never been counted, and the 20-session clock moves the maturity arithmetic. The
  Steward's R1 count decides whether P3 stays primary, where the decision date and hard stop land,
  and whether the question is lockable at all or is a data problem for `DEFERRED.md`. It goes to Haci
  **with those numbers attached**, in one pass, the way Q007's questions C and E did — and the desk
  will not answer it by loosening a floor or by moving the stop twice.

## Routed requests

### data-steward

**R1 — exposure-only stop count (blocks the lock).**

On the frozen data only (`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`),
for published picks (`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28) on non-excluded nights
(`research/data/exclusions_v002.json`, `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates`),
pick nights ≥ 2026-06-01, whose **20-session** forward window has matured against the trading calendar
implied by `prices_daily_split` (the DP-09 clock, not 40 sessions), please report **counts only**.
Inputs are the pick-night close `C_t` from `prices_daily_split`, ATR14 from `prices_daily_split` through
night t, and `public_payload_json.lane_plans.swing_trading` — **no bar dated after night t is read, not
even the session t+1 open**; no high, low or close after t, no touch, no return, no target outcome, no
`sas_selection_excursion` column, nothing from `results/`. Definitions: `dir` = +1 bullish / −1 bearish
from `dominant_direction`; `S` = `lane_plans.swing_trading.stop`; `T` = L3 = `lane_plans.swing_trading.targets[0]`
(confirmed as the swing lane's first target, `services/sas_conviction_card.py:183-186`);
`s_close = dir × (C_t − S) / ATR`; `d_close = dir × (T − C_t) / ATR`.
Please give: **(a)** the population funnel — published picks and nights in window and matured, then rows
removed at each step: no lane-plan ladder at all; swing lane present but **no L3**; swing lane and L3
present but **`stop` null** (the null-stop denominator — this is the headline unknown); non-bullish/bearish
direction; no `C_t` or no ATR; `outcome_target_invalid` non-null; **wrong-side stop** (`s_close ≤ 0`);
**wrong-side L3** (`d_close ≤ 0`); symbol with fewer than 60 daily bars dated ≤ t. **(b)** eligible picks
(all filters passed) split by bucket on `s_close`: **TIGHT** `0 < s_close < 1.0`, **MID** `1.0 ≤ s_close < 2.0`,
**WIDE** `s_close ≥ 2.0`. **(c)** contributing nights on three definitions: **P2** — nights with ≥ 1
eligible pick; **P3** — nights with ≥ 1 eligible **TIGHT** pick; **P1 (B1-valid)** — nights with ≥ 1
eligible pick that has a usable distance-matched control set, i.e. ≥ 10 same-night **non-published**
`sas_candidates` rows (the complement of the publication predicate, including qualified-false and
dark-lane rows) whose symbol has ≥ 60 daily bars dated ≤ t; please also report the share of eligible
picks with ≥ 10 and with ≥ 3 such rows and the median and 10th percentile of that count, so the Registrar
can see whether the nearest-10 pool ever binds. **(d)** the monthly run-rate of each of the three
contributing-night counts, and the projected date each reaches **80** contributing nights, by the method
you used in `research/reports/STEWARD_Q007_exposure.md` R2 (rate = contributing nights ÷ elapsed sessions
between the first and last matured night, projected forward at that constant rate, sessions converted at
365/252). **(e)** the null-stop share and the TIGHT/MID/WIDE split **by month and by score band**
(< 80 / 80–85 / 85–90 / 90+), counts only — §10 threat 10 cannot be read without it. **(f)** the count and
share of **fallback-pattern stops** (stop exactly 0.5% from the lane `entry` with targets at +0.5% / +1%,
`ai_agents/principal_agent.py:897-911`), by month.
**What it decides:** with the floor read as ≥ 80 contributing nights per primary endpoint (DP-21), (c) and
(d) decide whether **P3 stays a primary endpoint** (it needs 80 **TIGHT**-contributing nights, not 20 —
if it cannot project them by the hard stop it drops to descriptive and the within-question BH runs across
2), whether **P1's B1-valid count** rather than the raw pick count is the binding one, and whether Q009 can
be **locked at all** — if eligible contributing nights cannot project to 80, the blocker is that the printed
stop is not populated, which is a data problem and sends the question to `research/questions/DEFERRED.md`
rather than to a later date. Every one of those is a waiting-vs-sample trade-off (R-3): it goes to Haci with
your numbers attached, is not decided by the desk, and is never met by loosening a floor. Your counts also
set Q009's **decision date and hard stop in one pass** — Q007 moved its stop twice because the matched
design was counted after the first date was set; please treat (c)'s B1-valid and TIGHT definitions as the
ones the dates are computed on.

**R2 — successor freezes (at the decision date; not a blocker for lock).**

When Q009 reaches its decision date, build `manifest_v002` (selections, same SQL as v001) and
`manifest_prices_v002` (same Alpaca queries) covering pick nights after 2026-09-10, with the symbol list
extended to **every candidate on those nights, published and unpublished** — the unpublished symbols'
pick-night closes and forward bars are what the B1 distance-matched control is made of — plus **hourly bars
for published symbols**, needed for P2/P3's same-session stop-vs-target ordering. Scope is fixed by DP-23
and needs no further confirmation; `eval.py` records each sha256 and prints pre-lock and post-lock night
counts separately. If a successor price freeze omits unpublished-candidate symbols for some nights, those
nights are excluded from P1 and counted, never back-filled. Note that under DECISIONS.md item 9 the maturity
window is **20 sessions**, so the freeze must carry 20 forward sessions (40 where the descriptive companion
is to be computed) beyond the last included pick night.

**R3 — two pre-lock rulings on whether the frozen payload is the 16:05 ET output (blocks the lock only if
either comes back positive).**

Two nights/rows in Q009's window could carry a `public_payload_json` that is not what was published at
16:05 ET, which would mean the **printed stop the question studies is not the printed stop traders saw**.
First: **2026-06-26**, the mixed-state night the red team flagged separately and the KT audit explicitly
placed out of its scope (`research/reports/KT_AUDIT_manifest_v001_rerun_nights.md`, closing paragraph) —
partial row mutation, not a re-run. Please rule on whether that mutation touched `public_payload_json` (or
the lane-plan fields inside it) on that night's `sas_candidates` rows. Second: **§10 threat 6** — the
wrong-side-target guard and the E9a reclassification (`services/super_agent_select_service.py:810-839`,
ruling E9-2026-07-05) and the cross-lane monotonic re-sort (`:195-257`, "historical rows untouched"):
please compare `created_at` / `updated_at` on the affected rows inside 2026-06-01..2026-09-10 and state
whether any historical row's payload was rewritten after publication, and if so on which trading dates.
Row timestamps, counts and a pass/fail only — no price, no touch, no outcome. **What it decides:** if either
comes back positive, the affected nights are not knowledge-time-legal for this question, and under DP-22 you
issue `research/data/exclusions_v003.json` before this batch is locked and the PREREG cites it (the locked
files that cite v001/v002 are not edited); if both come back negative, §10 threats 6 and 11 are marked
verified with your report cited and nothing else changes. This needs no decision from Haci either way.

## Standing rules added

_none yet_ — no ASK was put this pass, so no new `DP` id is taken. Two notes for the desk, not rules:
(i) DP-12's Q009 downstream check is **closed negative** (item 14) — Q009's conditioning variable is known
at publication; (ii) DP-09's re-worded form has now been applied to a question that never had a
next-open spread entry (item 9), which is what the 2026-09-13 in-place edit was for.
