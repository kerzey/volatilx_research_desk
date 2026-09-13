# Q010 — stop_whipsaw_prospective: does Q009's stop result repeat on nights nobody had seen when it was registered?

**Status:** DRAFT (lock by committing this file **together with Q009's `PREREG.md`, at one commit** — DP-31; DECISIONS.md item 15; see "Decisions before lock" at the end)
**Family:** F6 Exits and execution (hypothesis H-032, the prospective half of Q009 — **not** counted as a second F6 question in the BH correction; §7)
**Type:** **Replication.** Every **definition, filter and exclusion criterion** is inherited from `research/questions/Q009_stop_whipsaw/PREREG.md` **verbatim by reference**; nothing is re-specified here. Q009's **window-specific measured counts are not inherited** — they are Q009 findings and enter only as §10.5's population-drift baseline (§2; DP-26). The only inputs that differ are the pick-night window (§2), the freezes it is pinned to (§5) and the exclusions file passed to the script (§2).
**Parent question:** research/questions/Q009_stop_whipsaw/PREREG.md (registered `HISTORICAL_ONLY`, DP-31)
**Manifest (selections / prices):** the successor freezes named in §5 — built and pinned at this question's decision date (DP-23). **No freeze covering this question's nights exists today, by design:** its nights have not happened yet.
**Exclusions:** research/data/exclusions_v003.json — the newest exclusions file at lock (DP-22). The exclusions file is an **input** to `eval.py`, not a literal inside it, so the run passes the newest exclusions file in force at the decision date; it must be a **superset of v003**, and the **criteria set is closed at lock** (§2).
**Lock mechanics (DP-31; DECISIONS.md item 15):** Q009's `PREREG.md` and this file enter `PREREG_LOCKED` at **one commit**; neither may be committed without the other, and if the controller will not advance one of them, **neither locks** — a Q009 locked without its successor is a DP-31 violation, not a sequencing detail.
**Inheritance pins (§4):** the lock commit's sha, and the sha256 of Q009's `PREREG.md` **and** of Q009's `eval.py` as of that commit, are written into this header by the lock commit itself. Both sha256s are printed in Q010's results header and compared before the run; a mismatch on **either** halts the run (§4).
**Registered by:** registrar · **Approved by:** haci (pending lock) · **Date:** 2026-09-13
**Decisions:** DECISIONS.md (2026-09-13)

---

## 1. Hypothesis (plain English)

**Whatever Q009 found about the printed swing stop on nights up to its decision date, the same thing
happens again — same direction, same size — on pick nights that had not occurred when Q009 was
locked, and indeed had not occurred when Q009 reported.**

That is the whole question. Q010 introduces no new estimand, no new level, no new entry basis, no new
MPE and no new code. It exists because Haci chose a Q009 window that places only ≈ 16 contributing
nights after Q009's lock commit against DP-24's 30 (Q009 §8; DECISIONS.md items 23–24), so Q009 can
reach **HISTORICALLY_CONFIRMED** at best. DP-31 requires the successor replication to be **drafted and
locked at the same commit as its parent**, before any of Q009's numbers are seen — a successor written
after the parent's output would carry every design choice made with those numbers in hand, which is
what rule 3 exists to prevent. **Q010 is the only thing that can fire Q009 §9** (§8).

**Q010 is not a standalone study and never produces a standalone claim.** Its gate is DP-24's 30
contributing nights, not rule 6 / DP-21's 80, because its job is to satisfy Q009 §8's
PROSPECTIVELY_CONFIRMED clause, not to establish the effect from scratch. It is reported only as the
prospective half of Q009's result, never as independent evidence, and on its own it can never carry a
CONFIRMED verdict (§8).

## 2. Population

**What is inherited, and what is not (DP-26; DECISIONS.md item 4).** Inherited **verbatim from
Q009 §2**, with no re-specification: the publication predicate (`qualified IS TRUE AND selected_rank
IS NOT NULL`, DP-28), the swing-lane stop as the stop line (DP-30), the definitions of `C_t`, `ATR`,
`dir`, `S`, `T`, `s_close`, `d_close`, the TIGHT / MID / WIDE buckets on `s_close` (DP-26), every
exclusion **criterion** and the requirement that each be counted and printed (null-ladder, null-stop,
`outcome_target_invalid`, wrong-side stop, wrong-side L3, immaturity at 20 sessions, missing bars,
< 60 daily bars), the unit of inference (the trading night, rule 6) and the three contributing-night
definitions. **Q009's window-specific measured counts are *not* inherited** — its 48 matured nights,
383 published picks, 303 eligible picks, 47 contributing nights, TIGHT 282 / MID 21 / WIDE 0 and
wrong-side-stop 66 of 371 (17.8%) are findings about Q009's window, not conventions, and they enter
this file **only** as the §10.5 population-drift comparison baseline. Q010 measures its own counts and
expects none of Q009's. If the two files ever appear to disagree on a **definition**, **Q009's text
governs**.

Only these three things differ, and each is an input to the script rather than a change to it:

- **Window (stated as a rule, so Q009's DP-13 extension needs no edit here).** Let **D** be Q009's
  decision date as its §5 defines it: **2026-11-09**, or **2026-12-21** if Q009's single automatic
  DP-13 extension fires on measured counts. Q010's population is **pick nights strictly after D** —
  the first trading session after D is the first candidate night — running for **N = 46 trading
  sessions** from that night (DECISIONS.md item 1; the branch table in §5 gives the dated
  illustrations). No night in Q009's registered window can enter Q010, and no night in Q010's window
  was available to Q009: by construction the two populations are disjoint, and every Q010 night
  post-dates Q009's decision date D and hence, a fortiori, both files' lock commit.
  **Why the window starts after Q009's *decision date* and not after its last pick night
  (DECISIONS.md item 11):** it is the only rule under which **no night is ever assigned to a question
  after that night has occurred**. Starting after Q009's last pick night would place
  2026-10-05..2026-11-13 in Q010 if Q009 does not extend and in Q009 if it does — with the branch
  chosen on 2026-11-09, after those nights happened. Under the registered rule the start only ever
  moves **later**, no night is ever moved *into* Q009, and the two populations stay disjoint on both
  branches. The price is that ≈ 26 sessions (2026-10-03..2026-11-09 on Q009's primary branch) fall in
  neither question; that cost is disclosed in §10.9 rather than left to be noticed.
- **Freezes.** The successor selection and price freezes named in §5 (DP-23), pinned at Q010's
  decision date. Q009's own freezes are not re-read.
- **Exclusions file (DECISIONS.md item 5).** The newest `exclusions_vNNN.json` in force at the
  decision date (DP-22), which **must be a superset of `exclusions_v003.json`**, on two registered
  conditions:
  - **The criteria set is closed at lock.** The admissible exclusion criteria are exactly v003's
    blocks (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs`,
    `catalyst_layer_regime_change`, `regime_label_point_in_time_from`) plus DP-04's mechanical
    re-run / non-session test, which the inherited `eval.py` already applies (`finished_at` later
    than the next session's open, or a run dated on a non-session day). A night in Q010's window
    **may not be excluded under a criterion invented after lock** without a Steward ruling made on
    **row timestamps and exposure counts only** — never on outcomes — routed and printed before the
    run. That is the 2026-06-26 pattern (a frozen row set its own run audit does not corroborate):
    reported with its counts, ruled by the Steward, never silently included and never dropped without
    a printed count.
  - **The delta is printed.** The results header prints the difference between `exclusions_v003.json`
    and the file actually passed to `eval.py`, block by block, with **the number of Q010 nights each
    block removes**.

## 3. Baseline(s) — what this must beat

**Inherited verbatim from Q009 §3**: **B1** (the 10 nearest same-night non-published candidates,
matched on `beta60` / `atr_pct` / `runup20`, with the stop and target placed at the same ATR distances
off the control's own pick-night close, graded on the same 20-session window and the same daily-bar
rule — rule 5's distance-matched control); **B2** (the same picks with no stop, plan E-NOSTOP — the
paired "what happens when X did not happen" baseline for P2); **B3** (descriptive, the stop's cost on
the matched controls). Control rows never add to inferential n (rule 6).

**Q010's additional baseline is Q009 itself.** The quantity that decides here is not only "is the
effect there" but "is it the *same* effect": the sign of each endpoint's estimate in Q009, and the
MPE it had to clear. That comparison is made once, at Q010's decision date, on the two files' printed
estimates — never by re-running or re-tuning Q009 (§8).

## 4. Objective metric (rule 5)

**Inherited verbatim from Q009 §4**, and computed by **the byte-identical, unmodified `eval.py` that
Q009 registers** — `research/questions/Q009_stop_whipsaw/eval.py`. Q010 writes **no** evaluation code.
Rule 9 applies in its strictest form: the script was written once, for Q009, and Q010 does not touch
it.

**Two pins, both checked before the run (DECISIONS.md item 3).** Q010's results header prints, and
`eval.py`'s caller compares against the values recorded in this file's header at the lock commit,
**both**:

1. the sha256 of `research/questions/Q009_stop_whipsaw/eval.py`, and
2. the sha256 of `research/questions/Q009_stop_whipsaw/PREREG.md`.

**A mismatch of a single byte on either halts the run** and the question goes to the Red Team, not to
a verdict. A question that inherits five sections by reference must checksum the file it inherits
from, or "verbatim by reference" is unenforceable.

**`eval.py` takes its window and its data paths as inputs (DECISIONS.md item 2; rule 9).** The
byte-identity requirement above is only achievable if the same script can be run on two different
windows without an edit. It is therefore registered here, and binds the Q009 script as written, that
`eval.py` takes **the window start date, the window end date, the selection and price manifest paths,
the exclusions-file path and the output directory as inputs** (config file or CLI), with **no
hard-coded dates, manifest names, exclusion dates or output paths anywhere in the script**. If the
Q009 script hard-codes any of them, that is a **defect to be fixed in the Q009 script before it is
used for either run** — never a post-hoc edit taken as "the script changed" between Q009 and Q010.

Carried over unchanged, and listed here only so no reader has to assume:

- **Entry basis: the pick-night regular-session close `C_t`** (DP-11 / DP-03(a)), for picks and
  controls alike; session index k = 1..20 with k = 1 = session t+1 (DP-09 — L3 within **20** sessions
  is the primary clock, the platform's 40-session lane window is the descriptive companion).
- **P1** — the control-adjusted whipsaw rate (`k_S` exists, `k_T` exists, `k_T > k_S`), unconditional,
  SAME_SESSION scored 0 on daily bars for picks and controls alike; `m1` in percentage points.
- **P2** — plans **E-STOP** and **E-NOSTOP** paired on the same picks, `Δ_p = r_{E-STOP} −
  r_{E-NOSTOP}` in ATR units, night-averaged; `m2` in ATR units, negative = the printed stop costs
  money.
- **P3** — descriptive, does not decide, and its p-value still enters the BH correction (§7).
- The rule-5 stop-exit exception is confined to plan E-STOP in P2 and P3, exactly as Q009 §4 states
  (DP-02); every other figure is graded with no stop, and the same sentence is printed in the results
  header and in `REPORT.md`.
- Tie rule: unresolved same-session stop/target fills **stop-first** in P2/P3 (DP-27); P1 keeps
  SAME_SESSION = 0.
- **Inference:** stationary block bootstrap over the ordered contributing nights, expected block
  length **10 sessions**, 2,000 resamples (the CI decides); date-clustered CI printed alongside;
  paired sign-flip permutation, 10,000 permutations, for p. Every count Q009 prints is printed here.
- **Quotability:** every number is **NON_QUOTABLE** (rule 12), including after a PROSPECTIVELY_CONFIRMED
  verdict, until restated on a W60 basis.

## 5. Sample floors and expected n

- **Gate: ≥ 30 contributing nights per endpoint (DP-24)**, on that endpoint's own contributing-night
  definition (Q009 §2: P1 — nights with ≥ 1 eligible pick carrying a valid B1 control set; P2 —
  nights with ≥ 1 eligible pick), **all of them dated after Q009's decision date D — hence, a
  fortiori, after both files' lock commit** (§2's window rule), measured by `eval.py` from the frozen
  data — never a projection or a run-rate. DP-21's 80-night floor is **not** the gate here and is not
  silently imported: Q010 is a replication satisfying Q009 §8's prospective clause, and DP-24 fixes
  that number at 30. DP-24's 30 is never reduced. Rule 6 / DP-21 is satisfied **by the pair** — Q009's
  ≥ 80 contributing nights plus Q010's ≥ 30 post-lock nights, which is exactly DP-24's standing
  construction — not by Q010 alone (§8).
- **Sub-cells, halves and tape strata (DECISIONS.md item 8).** Sub-cell figures (bucket, tape
  stratum, half, score band, bull/bear, regime) are printed **only** where they clear the **20
  contributing-night** cell floor (DP-21) and **SUPPRESSED with their counts** otherwise. At N = 46
  the two halves are ≈ 21 contributing nights each, so they will usually print; most other strata
  will not. Q009 §8's **both-halves clause and tape-stratum clause are not imported as gates** (§8) —
  they are 80-night clauses and a ≈ 42-night window cannot carry them. They are **printed
  descriptively** wherever the cell clears the 20-night floor, and a **sign disagreement between the
  halves is stated next to the pair verdict** in `REPORT.md`. Not importing them is not a loosening:
  DP-24's prospective clause is sign + MPE + CI, and nothing else in §8 is relaxed to compensate.
- **Expected n (the Steward's measured rate, context only — it gates nothing).** Q009's exposure
  count measures **47 contributing nights over the 51 sessions 2026-06-01..2026-08-12** under
  `exclusions_v003.json` (`research/reports/STEWARD_Q009_exposure.md` §R1(c),(d) and its v003
  addendum) — ≈ 0.92 contributing nights per session, with all three contributing-night definitions
  collapsing to the same count because the B1 control pool never binds (100% of eligible picks have
  ≥ 10 same-night non-published controls; median pool 54, 10th percentile 41). At that rate the
  registered **46-session** window supplies ≈ **42** contributing nights against a floor of 30
  (DECISIONS.md item 1). A fresh exposure-only count on the actual prospective nights is routed to the
  Steward (R5) and the gate fires on `eval.py`'s measured counts regardless.
- **Window length, decision date, extension and DEFERRED fallback (N = 46; DECISIONS.md item 1;
  DP-13).** Stated as rules, so Q009's extension moves Q010's dates without an edit:
  - **The registered rules.** (i) **Window:** the **46** trading sessions beginning with the first
    session strictly after Q009's decision date D (§2). (ii) **Decision date:** the first Monday at
    least five business days after the **20th trading session following the last pick night in the
    window** — the freeze margin the Steward needs to build and pin the successor freezes.
    (iii) **One automatic extension (DP-13):** if either endpoint is short of 30 contributing nights
    at the decision date on measured counts, the window extends **once**, automatically and with no
    new question to Haci, by a further **30 trading sessions**, with the decision date recomputed by
    rule (ii). The extended run uses the same byte-identical `eval.py` and the same gate.
  - **Dated illustrations (DECISIONS.md item 10).** The four branches, so no branch is undated.
    **Every cell below is illustrative — the Steward fixes the exact session-count date against the
    trading calendar when building the freezes (R5). The rules above, not these dates, are what is
    registered**; the rules are deterministic given the calendar, so fixing a date later is
    arithmetic, not a choice made with numbers in view.

    | Q009 branch (D) | Q010 branch | window (illustrative) | decision date (illustrative) |
    |---|---|---|---|
    | primary, D = 2026-11-09 | primary, 46 sessions | 2026-11-10 .. ≈ 2027-01-15 | Monday **2027-02-22** |
    | primary, D = 2026-11-09 | + extension, +30 sessions | 2026-11-10 .. ≈ 2027-03-01 | the Monday rule (ii) gives for a window ending ≈ 2027-03-01 — ≈ early Apr 2027 |
    | extension, D = 2026-12-21 | primary, 46 sessions | 2026-12-22 .. ≈ 2027-03-01 | the **same** Monday as the row above — the rule depends only on the window end |
    | extension, D = 2026-12-21 | + extension, +30 sessions | 2026-12-22 .. ≈ 2027-04-14 | the Monday rule (ii) gives for a window ending ≈ 2027-04-14 — ≈ late May 2027 |

    The two middle rows necessarily resolve to the **same** decision date, because rule (ii) is a
    function of the window end alone and both windows end ≈ 2027-03-01. An earlier draft of this file
    gave them two different dates; that was arithmetic, not two rules, and the table is the correction.
  - **DEFERRED fallback.** If either endpoint is still short after that single extension, Q010 goes
    to **DEFERRED** (`research/questions/DEFERRED.md`, with the measured counts) rather than running
    under-powered, and Q009's verdict stands as `HISTORICAL_ONLY` for good unless a new question is
    registered. There is no second extension.
  - **No interim looks.** `eval.py` is run **once** on Q010's window (twice only if the extension
    fires, on the extended window, with the same script). Waiting on exposure-only counts is not
    optional stopping, because exposure counts carry no outcome.
- **Whether Q010 runs at all.** Q010 runs **if and only if Q009 returns HISTORICALLY_CONFIRMED on at
  least one primary endpoint**. If Q009 returns NULL or INCONCLUSIVE on both, there is nothing to
  replicate: Q010 is closed unrun, the reason is ledgered, and any later prospective test of H-032 is
  a **new** pre-registration, not this one re-opened (rule 3; DP-31 — the successor exists to reach
  the tradeable verdict, not to give a null a second window). **If Q009 goes to DEFERRED** — a gate
  still short after its own single DP-13 extension (Q009 §5) — Q010 is likewise **closed unrun**, for
  the same reason and by the same route: the reason is ledgered and any later prospective test of
  H-032 is a new pre-registration (DECISIONS.md item 7). This is fixed here, before Q009's numbers
  exist, so the choice can never be made with them in view.
- **Freeze discipline (DP-23).** The successor selection freeze (same SQL as `manifest_v001`) and
  price freeze (same Alpaca queries) covering Q010's nights, with the symbol list extended to **every
  candidate on those nights, published and unpublished** (B1 needs the unpublished symbols' pick-night
  closes and forward bars) and **hourly bars for published symbols** (the P2/P3 same-session
  tie-break), carrying **20** forward sessions beyond the last pick night (40 where the descriptive
  companion is to be computed). `eval.py` records every sha256. Nights whose unpublished-candidate bars
  are missing are excluded from P1 and counted, never back-filled. This is a **third** freeze build,
  after Q009's primary and extension builds; it is routed to the Steward as **R5** (DECISIONS.md),
  due at Q010's decision date and **not a blocker for lock**. R5 also carries the exclusions file for
  Q010's nights — a superset of v003 under §2's closed criteria set, with the v003→run-file delta
  printed — and the exposure-only population funnel and contributing-night counts that §10.5's drift
  comparison needs before any estimate is read.

## 6. Test window, split and stratification

- **Test window:** §2's rule — pick nights strictly after Q009's decision date D, for **46** trading
  sessions (§5's branch table for the dated illustrations). **Contamination is structurally impossible
  for the registered definitions**: every
  definition, threshold, MPE, clock and line in this file was fixed at Q009's lock commit, before any
  night in this window occurred and before any of Q009's outputs existed. The one exposure that is
  *not* structural is the human one — at Q010's decision date the desk will know Q009's result — and
  it is contained by the same two devices: **nothing in this file may be edited after lock**, and the
  script is byte-identical.
- **Split:** no in-sample / out-of-sample split inside Q010. Q010 **is** the out-of-sample half;
  Q009's window is the in-sample half, and the pair is what is reported (§8). Halves within Q010
  (≈ 21 contributing nights each at N = 46) are printed descriptively where they clear the 20-night
  cell floor and **decide nothing**; a sign disagreement between them is stated next to the pair
  verdict in `REPORT.md` (§5, §8).
- **Regime / tape stratification (rule 7):** as Q009 §6 — `market_regime_daily` `regime_version`
  'v1.2' (legal point-in-time from 2026-06-09, so legal throughout this window), and the trailing SPY
  tape stratum (sign of the 20-session return × tercile of 20-session realized volatility, terciles
  cut on Q010's own contributing-night set). Cells below 20 contributing nights are SUPPRESSED. The
  report states the tape Q010's window fell in, in words, next to Q009's — **a replication in a
  different tape that reproduces the sign is stronger evidence, and one that fails in a different tape
  is not a refutation of Q009's window** (§8, §10 threat 2).
- **Knowledge time (rule 14):** as Q009 §6's table, unchanged. No session-t+1 quantity enters any
  primary endpoint or any eligibility filter; the entry is `C_t`; **no rule-14 exception is requested
  and none is needed** (DP-05 untouched, no R-1 arises).

## 7. Multiple testing

- **Within the question:** the inherited `eval.py` computes **BH across m = 3** (P1, P2, P3) at
  q ≤ 0.10, exactly as Q009 §7 specifies, and P3's p-value enters the correction while carrying no
  verdict. **m stays at 3 whatever the number of endpoints in Q010's verdict scope** (§8 clause 1 may
  leave only one endpoint eligible for a pair verdict): a narrower verdict scope must not lower the
  BH threshold for the endpoint that *is* in play (DECISIONS.md item 6). Q010's q-values are
  **printed** and reported; the pair's verdict rule in §8 is the one that decides, and it is at least
  as strict (it requires the CI to exclude 0 and `|m| > MPE` on top of the sign).
- **P1's anti-leniency dual q (Q009 §7) carries over**: the Reporter prints P1's q within F6 and as if
  P1 were an F4 primary alongside the registered F4 primaries, and any statement about P1 uses the
  **larger** q.
- **Across the family: Q010 is filed in F6 and is not counted as a second F6 question.** A replication
  of the same endpoints on later nights is not a second test of a different hypothesis; counting it
  would inflate the family and, perversely, loosen the BH thresholds for everything else in F6. Q009
  §7 states the same thing from the other side. H-032 is one hypothesis, registered once, evaluated in
  two windows.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

**MPEs, inherited verbatim from Q009 §8 and not re-asked:** **P1 5.0 pp** (DP-20), **P2 0.25 ATR per
trade** (DP-10), **P3 0.25 ATR per trade** as a reference line beside a descriptive figure (DP-10).
`m1` is in percentage points of control-adjusted whipsaw rate; `m2` and `m3` in ATR units per trade.

The verdict is a **verdict on the pair**, endpoint by endpoint. Let `m_hist` be Q009's printed
estimate for an endpoint and `m_pro` Q010's.

**Verdict scope (DECISIONS.md item 6).** The unmodified script computes **everything** — P1, P2, P3,
every secondary, both clocks — and nothing is switched off; it is byte-identical (§4). But **only an
endpoint on which Q009 returned HISTORICALLY_CONFIRMED can take a pair verdict** (clause 1 below).
Every other endpoint's Q010 figure is printed **descriptive-only** and carries no verdict, in either
direction.

- **PROSPECTIVELY_CONFIRMED (the pair)** — for an endpoint, requires **all** of:
  1. Q009 returned **HISTORICALLY_CONFIRMED** on that endpoint (all seven of its §8 clauses);
  2. Q010 has **≥ 30 contributing nights** for that endpoint, on its own definition, **all dated
     after Q009's decision date D — hence, a fortiori, after both files' lock commit** (§2, §5);
  3. **`sign(m_pro) = sign(m_hist)`**;
  4. **`|m_pro| > MPE`** for that endpoint (5.0 pp for P1, 0.25 ATR for P2);
  5. Q010's block-bootstrap 95% CI for that endpoint **excludes 0**.
  Only P1 and P2 can reach this verdict; P3 is descriptive in both files and reaches no verdict.
  **This is the only route by which Q009 §9 fires** (Q009 §9's opening line; DP-31; rule 10). Even
  then every number is NON_QUOTABLE until restated on a W60 basis (rule 12), and any subscriber-facing
  statement is drafted from the pair, never from Q010 alone.
  **A P1-only pair licenses nothing:** Q009 §8 requires **P2 CONFIRMED** for a guide line or platform
  change, and §9 here is unchanged by this question (DECISIONS.md item 6).
- **NULL (the pair does not replicate):** the gate is met and either `sign(m_pro) ≠ sign(m_hist)`, or
  `|m_pro| < MPE` with Q010's 95% CI including 0. Q009's historical verdict **stands as registered,
  with its `HISTORICAL_ONLY` label**, and is ledgered as "confirmed in-window, did not replicate
  prospectively". Nothing on the platform changes. This is a real finding and is ledgered with the
  same care as a confirmation.
- **INCONCLUSIVE:** anything else — the sign reproduces but `0 < |m_pro| ≤ MPE` with the CI excluding
  0 ("real but below MPE", rule 6), or `|m_pro| ≥ MPE` with the CI including 0. Q009 keeps its
  `HISTORICAL_ONLY` label; §9 does not fire.
- **Gate shortfall is not a verdict.** Fewer than 30 contributing nights on an endpoint at the
  decision date fires the single DP-13 extension (§5), then DEFERRED. It is never read as NULL and
  never as INCONCLUSIVE.
- **What is not required of Q010, said explicitly so no one imports it later:** the 80-contributing-
  night floor (DP-21 governs a primary endpoint establishing an effect; DP-24's 30 governs a
  prospective replication), Q009 §8's both-halves clause, and its tape-stratum clause — a 30-night
  window cannot carry either, and **nothing else is loosened to compensate**: the MPEs, the CI, the
  sign test and the byte-identical script are all unchanged. Both clauses are still **printed
  descriptively** wherever the cell clears 20 contributing nights, and a half-to-half sign
  disagreement is stated next to the pair verdict (§5, §6).
- **Not a precedent (DECISIONS.md item 13).** Rule 6 / DP-21 is met **by the pair** — Q009 at ≥ 80
  contributing nights plus Q010 at ≥ 30 post-lock nights, DP-24's standing construction — never by
  Q010 alone. **A future question may not cite this file as precedent for a 30-night primary
  endpoint; the 30 is DP-24's prospective clause, not a floor.** No CLAUDE.md rule is softened here
  and no `DP` entry is created by this file.
- **Reporting discipline.** Q010's numbers are never presented as independent evidence for H-032. The
  LEDGER entry is written against **Q009** — "PROSPECTIVELY_CONFIRMED (Q009 + Q010)" or "Q009
  HISTORICALLY_CONFIRMED, HISTORICAL_ONLY; Q010 did not replicate" — with Q010 listed as the
  prospective half.

## 9. If CONFIRMED, what changes on the platform

**Nothing changes on the strength of Q010 alone.** What a PROSPECTIVELY_CONFIRMED *pair* licenses is
written once, in **Q009 §9**, and is not restated or extended here: the Manual Trading Guide line about
the printed swing stop, the card relabelling, the flag-off stop-distance field, and the brief for the
*existence* (never the width) of an ATR floor on written stops. Those bullets are dormant until this
question fires them, and they fire only under §8's five clauses.

Two things this question adds, and nothing more:

- **It removes the `HISTORICAL_ONLY` label from the pair's verdict** (Q009 §8 clause 7) — that label,
  not any new finding, is what blocks Q009 §9 today.
- **It sets the shadow clock.** Implementation still follows rule 11: any resulting change ships
  flag-off with a byte-identical checksum on the old path and is shadowed ≥ 20 trading days before a
  flip. Owner: implementer.

If the pair is NULL or INCONCLUSIVE, **nothing changes**: the guide's current stop language stands,
Q009 stays `HISTORICAL_ONLY`, and F6 effort moves on.

## 10. Known threats to validity (registrar's own list)

1. **The desk will know Q009's result when Q010 runs.** That is the unavoidable cost of a sequential
   design, and it is contained by construction: every definition, MPE, gate, clock and decision rule
   in this file is fixed at the same commit as Q009's, before Q009's output exists; the script is
   byte-identical and checksummed at run time; and the file may not be edited after lock. What cannot
   be contained is the *choice to run* — which is why §5 fixes it as a rule (Q010 runs iff Q009
   confirms) rather than leaving it to be decided with the numbers in hand.
2. **A different tape.** On the registered N = 46 Q010's window is Nov 2026–Jan 2027 (Dec 2026–Mar
   2027 if Q009's extension fires; §5's branch table), a different tape from Q009's Jun–Oct window,
   and it spans a holiday season in which the nightly run-rate may be lower than the 0.92
   contributing nights/session measured over Jun–Aug. The run-rate risk is carried by DP-13's single
   automatic extension, not by a lowered gate (§5).
   A sign that reproduces across two tapes is stronger
   than rule 7 normally requires; a sign that fails may be regime, not refutation. §8 does not let
   either reading be improvised: a failure is ledgered as "did not replicate prospectively" and
   licenses nothing, in either direction.
3. **Thirty nights is a small sample.** The CI at ~30–45 contributing nights is wide, so an effect
   real but smaller than Q009's may land as INCONCLUSIVE. That is the intended asymmetry: DP-24's 30
   is a bar for *claiming*, not for *believing*, and "below MPE" is INCONCLUSIVE by rule 6, never a
   quiet pass.
4. **Overlapping 20-session windows** inflate precision, as in Q009; the same 10-session block length
   is used, on a shorter series.
5. **The population may drift.** The stop writer is an LLM and the platform ships changes; if the
   wrong-side-stop share, the null-stop share or the TIGHT/MID/WIDE split in Q010's window differs
   materially from Q009's measured 17.8% / 0% / 93.1%–6.9%–0%, the two windows are not speaking about
   the same object. **This is the one and only place Q009's measured counts enter Q010** (§2): they
   are the drift-comparison baseline, never an expectation and never a filter. `eval.py` prints
   Q010's own figures per month and per score band, and R5 returns them exposure-only before any
   estimate is read; the Reporter compares them side by side and says so before comparing estimates.
   A large drift is a reason to call the replication INCONCLUSIVE on the face of the population, and
   that call is the Red Team's, not a gate.
6. **A platform change could invalidate the inherited definitions mid-window** (an ATR floor on
   written stops, a side guard, a ladder-writer change). The inherited `eval.py` already prints the
   platform commits touching `services/super_agent_select_service.py` and
   `ai_agents/principal_agent.py` inside the window with P2 split at each such date; if any of them
   changes how the stop is written, Q010's window is no longer a replication of Q009's and the pair is
   INCONCLUSIVE. **This is a live risk precisely because a confirmed Q009 argues for such a change** —
   no such change may ship before Q010's decision date without voiding this question (rule 11's
   flag-off discipline is what makes that avoidable). The constraint is carried, in those terms, on
   the `PLATFORM_ISSUES.md` wrong-side-stop entry the Q009 pass filed: *a side/distance guard on the
   written stop must not ship flag-on before Q010's decision date* (DECISIONS.md item 14). Filing and
   maintaining that entry is the coordinator's / Steward's lane; this file states the research
   consequence only.
7. **Prospective data-integrity failures.** New re-run nights are caught mechanically (DP-04);
   a 2026-06-26-shaped failure (a frozen row set its own run audit does not corroborate) is not, and
   is routed to the Steward before the run (§2). The desk's validators did not catch the 2026-06-26
   case on their own — the Red Team did.
8. **Everything Q009 §10 lists still applies** — non-random stop placement, the entry-anchored stop,
   daily bars unable to order a same-session stop and target, gap-through fills, `C_t` as a proxy for
   an after-hours fill, the stock path as a proxy for a spread, thin elite and MID cells — and is not
   re-litigated here.
9. **Sessions that fall in neither question — disclosed, not accidental.** Because Q010's window
   starts after Q009's *decision date* D rather than after Q009's last pick night (§2), ≈ **26**
   trading sessions (2026-10-03..2026-11-09 on Q009's primary branch; the equivalent stretch on the
   extension branch) are studied by neither question. That is the price of the only rule under which
   no night is assigned to a question after that night has occurred, and it is a cost in nights, not
   a bias: the skipped stretch is defined by the calendar and by Q009's registered decision date,
   both fixed before any of it happens, so nothing about those nights' outcomes can influence which
   question they land in. Any later question wanting them must register for them itself.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: **R5 — the successor freezes for
Q010's window (selection + prices, third build), the exact session-count dates for all four branch
cells, the exclusions file in force for those nights, and the exposure-only population and
contributing-night counts at the decision date; due at Q010's decision date by design (§5, DP-23) and
not a blocker for lock.** Nothing is outstanding for Haci: the draft's single unresolved item — the
window length N and therefore the initial decision date — is settled at **N = 46** under DP-13 and
DP-24 (DECISIONS.md item 1), and is his to overturn at lock like any other decision here.

Q010 is locked **together with its parent** `research/questions/Q009_stop_whipsaw/PREREG.md` at the
**same commit** (DP-31; DECISIONS.md item 15). Neither file may be committed without the other; if
the controller will not advance one of them, neither locks.
