# Q014 — decisions before lock
Run: 2026-09-13 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 4 items
**`record` run: 2026-09-13, from `research/reports/STEWARD_Q014_exposure.md` (R1 returned, all four
parts). R1(a) = VERIFIED single application ⇒ item 13's cascade branch (i) fires, the §2.1 three-bucket
reconstruction governs, the conditional registrar route is VOID and Q014 locks. Schedule filled below:
decision_date 2027-04-05, extension_date 2027-05-17, inside DP-43's 2027-09-13 ceiling ⇒ not DEFERRED.
See "## Settled at `record`". R1 is closed; R2 stays open, due at the decision date.**
(+ items 5–21: the two R-3 choices the draft made in §5 without naming them as such, the choices a `DP`
entry or a locked precedent settles, and the DP-compliance confirmations the Registrar needs at `apply`)

**Mode: autonomous (`--autonomous`).** DP-40..48 are in force: **no decision is put to Haci before
lock.** What would have been an ASK is `DEFAULTED` — R-1 → **DP-41**, R-2 → **DP-42**, R-3 →
**DP-43**, R-4 → **DP-44**, R-5 → **DP-45**; otherwise the Registrar's recommendation unless a DECIDE
ground gives another answer (DP-40), and where two options differ only in strictness, the stricter.
Every DEFAULTED item is listed under "Defaulted on Haci's behalf" and on the board; the locked
question stands (rule 3) and Haci overturns any of it by asking for a successor question, never by
editing the locked file.

**Summary: 25 DECIDED (19 at `decide`, 6 more at `record` — items 22–27), 2 DEFAULTED (both R-3 →
DP-43 — E2's status as a primary, and the window/decision date, whose arithmetic is now settled:
2026-06-01..2027-02-25, decide Monday 2027-04-05), 2 ROUTED (**R1 returned and closed**; R2 successor
freezes open, due at the decision date, never blocking), 0 ASK.** All four of the draft's open items are settled here; three of
them by a `DP` entry, a locked precedent or one defensible technical answer, and the fourth (E2) by
DP-43, because "drop a primary endpoint to reach the floor sooner" is exactly the trade DP-43 refuses.

**[Settled 2026-09-13: R1(a) returned VERIFIED; the block below is discharged and Q014 locks — item
22.]** **Q014 cannot lock until R1(a) returns**, on the Q013 precedent and for the same reason: R1(a) decides
whether the conditioning variable is knowledge-time legal at all. The draft's §2.1 reconstruction
(`score_b* = score_b / oi_confirm_mult`) is exact **only if** the OI-confirmation pass multiplied each
row at most once and stored the multiplier it used. If it did not, the persistence count would carry
post-16:05 information, that would need a new rule-14 exception, and the desk grants none (DP-41).
Item 13 pre-commits the whole cascade now, before any outcome exists, so nothing is chosen after the
fact. R1(b)–(d) do not block the lock; they fix the schedule at `record` (item 5).

**State note:** `research/questions/Q014_uoa_persistence/state.json` reads `PREREG_DRAFT` (registrar,
2026-09-13T21:05Z) at both the `decide` and the `record` run; the Decision-maker did not touch it.
**R1(a) has returned**, so `@registrar apply Q014` runs now, and the controller advances Q014 to
`PREREG_LOCKED --by desk`, writing `schedule.json` from the `## Schedule` block in the same step
(DP-46). No `results/` directory exists and none was read; no parquet, no weekly and no daily report
was opened; `PREREG.md` was not edited.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Handling of the OI-confirmation rewrite of `score_swing` / `score_long` in the persistence count (draft item 1) | DECIDED | **Option A — reconstruct the 16:05 value as `score_b* = score_b / oi_confirm_mult` where the multiplier is non-null, `score_b` otherwise, across all three buckets**, with `label_b` used as frozen (written once at 16:05 from the pre-multiplier score, `uoa_screener.py:1728-1734`). **Option C is unavailable**: taking the mutated values at face value puts post-16:05 information into a feature and would need a new rule-14 exception the desk does not grant. **Option B silently narrows H-040's three-bucket definition** and is kept where the draft already puts it — the §10 threat-1 sensitivity, printed every run — *and* as the pre-committed fallback of item 13, not as the primary. Three bookkeeping requirements travel with A, all decided now and none tunable later: `eval.py` prints (i) the count and share of lookback rows carrying a non-null `oi_confirm_mult` and its value distribution, (ii) the number of `strong` flags and the number of **arm assignments** the reconstruction changes versus the frozen values, and (iii) the count of reconstructed scores landing within ±0.5 of the 70 cut (a rounding band), with both readings of that band printed as a named sensitivity. **`oi_confirm_mult` is used only to invert a known mutation and never as a feature** — the reconstructed quantity *is* the 16:05 value, which is why no exception is requested (DP-05 untouched). | rule 14; DP-41 (option C needs an exception; none granted); DP-25 (the hypothesis's own three-bucket seed definition); DP-26 (the ≥ 70 cut and the direction-matched label are conventions from the seed, not findings); PREREG §2.1, §10 threat 1; PI-013 |
| 2 | Entry basis (draft item 2) | DECIDED | **Option A — the session t+1 official regular-session open `O_1` (DP-03(b))**, identically for picks, Pool-A controls and Pool-B controls, each from its **own** t+1 open. **DP-11 does not fire:** nothing here is a position already held when the signal appears — the persistence count is read at 16:05 ET on the pick night and the trade is opened afterwards. Pool-B controls are drawn from the UOA screener universe and have neither after-hours prices nor, in general, hourly bars, and rule 5 requires **one** basis on both sides. The pick-night-close basis (DP-03(a) / DP-11's `C_t` proxy) is the descriptive sensitivity the draft already names and **never decides**. | DP-03(b); DP-11 (scope — does not fire); DP-42 (entry basis by DP-03/DP-11); rule 5; Q006 §4 (locked: t+1 open for picks and controls alike); Q013 item 7 |
| 3 | Does the repeat-selection stratum gate E1's verdict or only stratify it? (draft item 3) | DECIDED | **Option A — it gates.** §8 clause 7 stands as drafted: where the `prior_pub10 = 0` cell clears 20 contributing nights it must share the pooled sign **and** reach at least half of E1's MPE; where it is SUPPRESSED for want of nights, E1 is **INCONCLUSIVE, not CONFIRMED**. The two options differ only in strictness, so the stricter is taken without further argument, and there is an independent reason: Q003 (H-052) already owns the re-selection continuation finding, and an ungated E1 could confirm the same effect a second time under a different name — which §7 forbids and §9 refuses to act on. With item 6, "half the MPE" is **5.0 pp**. | DP-45 (stricter of two readings); DP-29 (an overlapping hypothesis is not counted twice); rule 8; PREREG §7 (Q003 overlap), §8 clause 7, §10 threat 2 |
| 4 | Is E2 a primary endpoint or a descriptive baseline? (draft item 4; **R-3** — "dropping a primary endpoint") | **DEFAULTED** | **Option A — E1 and E2 are both primary, each gated on its own ≥ 80 contributing nights and its own ≥ 30 post-lock nights, BH across m = 2.** H-040 names both baselines ("3+ UOA not selected" and "selected with 0 UOA") and dropping E2 leaves untested the one result that would stop a subscriber-facing claim — that the persistently-flagged names SAS *passed over* did just as well. The stated advantage of option B does not even exist: on the draft's own projection **E1 binds** (≈ 0.65 contributing nights/session against E2's ≈ 0.88), so demoting E2 would not move the decision date by a day; and a later date would not be a reason in any case. | DP-43 (a primary is never dropped to reach a floor sooner); DP-25 (the test stays the one that was proposed); rule 8; **not taken:** E2 descriptive, notionally reaching the floor sooner |
| 5 | Window, decision date, DP-13 extension and DEFERRED fallback (PREREG §5; **R-3**) | **DEFAULTED** | **DP-43's recipe, with the drafted dates as a floor and the arithmetic settled at `record` from R1(b).** Window: pick nights **2026-06-01** (DP-06) through the earliest end at which **both** primaries project ≥ 80 contributing nights (DP-21) **and** ≥ 30 contributing nights dated after the lock commit (DP-24), on **E1's** measured rate, since E1 binds. Decision date = window end + **20** sessions maturity (DP-09's clock) + one week of freeze margin, first Monday on or after. **Drafted values — window end 2026-11-30, decision Monday 2027-01-11, single automatic DP-13 extension to pick nights ..2027-01-15 with decision Monday 2027-02-22 — stand as a floor: R1(b)'s measured rate may push every date out, never pull one in.** The exact session-count dates are fixed from the trading calendar by the Steward when the successor freezes are built. One automatic extension (+30 sessions, DP-13/DP-43), then **DEFERRED** — no second extension, no gate reduced, no under-powered run, and a gate shortfall is **never** INCONCLUSIVE. Gates fire on **`eval.py`'s measured counts** at the decision pass, never on the projection, the arm-split assumption or R1. **12-month ceiling: if R1(b) puts the initial decision date after 2027-09-13, Q014 is not locked** — it goes to `research/questions/DEFERRED.md` with the date and the measured rate named (the H-062 precedent). No interim looks; `eval.py` is written once (rule 9) and run once. | DP-43; DP-13; DP-21; DP-24; DP-45; Q011 item 8 (a projection pushes a date out, never in); H-062 DEFERRED precedent; **not taken:** a shorter, sealed-only window reporting sooner but HISTORICAL_ONLY (DP-31) |
| 6 | MPE per primary endpoint | DECIDED | **E1 = 10.0 pp. E2 = 5.0 pp.** Both two-sided; the verdict carries its sign. E2 is a single-arm control-adjusted touch-rate excess — **exactly DP-20's shape**, so DP-20's 5.0 pp applies unchanged. **E1 is a difference of differences across two arms with small per-night cells** (≈ 2.5 PERSIST and ≈ 1.4 NONE eligible picks per night on the draft's own projection), which is the precise shape for which the locked Q007 §8 raised DP-20's floor to **10.0 pp**, on the Q003 §8 precedent. Consistency across questions decides this, not local optimality: the same estimator shape carries the same bar. The draft's single "+5.0 pp for both" is corrected accordingly, and §8 clause 7's "half the MPE" reads **5.0 pp** for E1. No money-unit MPE is invented anywhere (DP-44); the sessions-to-first-touch forms stay descriptive with no MPE (DP-44). | DP-20 (5.0 pp floor; a larger MPE is allowed with a reason, a smaller one is not); DP-44; DP-45; **Q007 §8 / DECISIONS.md item 4a** (DiD with small cells → 10.0 pp); Q003 §8; Q011 item 10 (which declined the uplift for a *paired same-pick* contrast — a different shape) |
| 7 | Where each control's synthetic target is anchored (silent in §2.3; contradicts the construction it cites) | DECIDED | **Anchor on the pick's close-basis distance, exactly as Q006 §3 step 3 writes it: `d_close,p = dir_p × (L3_p − C_{t,p}) / ATR_p` and `L3_c = C_c × (1 + dir_p × d_close,p × atr_pct_c)`, for Pool A and Pool B alike**, graded from each control's **own** t+1 open over the same 20 sessions, with the same "at or through the entry is not a hit" rule. The draft anchors at the control's close `C_c` but sizes the distance with **`d_open,p`**, the pick's distance measured *after* the pick's own overnight gap — which is not the same ATR distance on both sides: the pick's distance from entry is `d_open,p`, while the control's becomes `d_open,p − gap_c`, so the control gets its own gap subtracted a second time. Rule 5 requires the same ATR distance; the locked Q006 / Q007 / Q009 / Q015 construction achieves it by measuring the distance from the close on both sides and entering at the open on both sides. `d_open,p` stays in the file where it belongs — as the printed gap-through diagnostic (`d_open ≤ 0`) and in the ATR-distance-tercile cell. **Every pick has `d_close,p > 0` by §2.4's own wrong-side-L3 exclusion**, so the construction is always defined. | rule 5 ("targets placed at the same ATR distance"); **Q006 §3 step 3** (locked, verbatim); Q007 B3; Q009 §3; Q015 §3; DP-26 |
| 8 | The `completeness_score ≥ 35` screen on the control pool (silent in §2.3) | DECIDED | **The screen stands, and the file stops calling Pool A "the Q006 §3 / Q011 §3 construction" without qualification.** It is a 16:05-legal, outcome-independent convention applied identically to both arms, so DP-26 keeps it; but no locked question's control pool carries it, and Pool A is therefore **that construction plus a completeness screen**. `eval.py` prints the number of same-night non-published candidates removed by the screen and the per-pick pool size before and after it, so the deviation is visible and any Q006 / Q011 cross-reference is read with it in view. The **same screen applies to the Pool-B sub-pool of non-published SAS candidates** ("SAS saw it and passed"); it cannot apply to Pool B proper, whose symbols come from the UOA universe and have no `completeness_score`, and that asymmetry is disclosed in §2.3 rather than patched. | DP-26 (registrar-chosen conventions stand, not derived from sealed outcomes); Q006 §3; consistency bookkeeping |
| 9 | Which exclusions file | DECIDED | **`research/data/exclusions_v003.json`** — the newest file on disk (v001, v002, v003; no v004 exists at this run), read by `eval.py` as `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, with **no date hard-coded** in the PREREG or in `eval.py`. In-window that removes 2026-06-26, 2026-07-02 and 2026-07-06; the printed figure is the one `eval.py` derives. `catalyst_layer_regime_change.fixed_from = 2026-06-01` and `regime_label_point_in_time_from = 2026-06-09` are read from the same file, not restated as literals. If the Steward issues `exclusions_v004.json` before Q014 locks, the draft cites that file instead — the cited version is always the newest at lock. | DP-22; Q011 item 11; Q013 item 5 |
| 10 | Publication predicate | DECIDED | **`qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28)**, as drafted. Dark-lane rows (`qualified IS TRUE`, `selected_rank IS NULL`) are **not** treatment rows, are counted, and remain available to Pool A and to the Pool-B sub-pool. Q002/Q004/Q006's looser `selected_rank`-only predicate is **flagged to the Red Team for those questions' reviews, not fixed here** and not copied. | DP-28; PREREG §2.2 |
| 11 | Family, within-question and within-family correction | DECIDED | **F5 Cross-engine interaction**, as drafted: the primary endpoints' *subject* is whether a second engine's prior-session signal adds information to SAS selection, which is F5's definition; the endpoint is a path metric because rule 5 requires that of every question, and that does not move it to F4 (DP-29). **BH across m = 2 within the question** (E1, E2) at **q ≤ 0.10**; every secondary prints raw p marked "descriptive, does not decide". **Across the family: verified — F5 holds H-040 and H-041, and Q014 is the only registered F5 question**, so F5 carries **2** primaries (checked against every `**Family:**` header in `research/questions/` and against `research/BACKLOG.md` §F5). The Q003 (F6), Q006 (F1) and Q002 (F7) overlaps are non-independence hazards: cross-referenced, **never counted as two confirmations**, exactly as §7 drafts them. | DP-29; rule 8; BACKLOG §F5; PREREG §7 |
| 12 | Primary level, lane and clock | DECIDED | **L3 = `public_payload_json.lane_plans.swing_trading.targets[0]`, first touch within 20 sessions from the stated entry**, on the swing lane. H-040 names no level, so DP-42's default for a swing-lane question applies, on DP-09's clock; the platform's 40-session swing window is reported alongside, descriptively, wherever it has matured. L1, L2 and L4 stay descriptive. **Sample floors, maturity and every date in §5 are computed on the 20-session window.** | DP-42; DP-09; Q007 §5; Q011 §2; Q013 item 8 |
| 13 | Knowledge time — is a rule-14 exception needed, and what happens if the reconstruction cannot be verified | DECIDED | **None is requested and none is granted; DP-05 is untouched.** DP-05(b)'s later classification clock is Q008's and **does not travel**. `eval.py` must compute the eligible set, both control pools, `uoa5`, the arm labels and every stratum label into a frozen per-pick table **before any session-t+1 or later bar is loaded**, and fail loudly if a t+1-or-later field is referenced in eligibility, matching, arm assignment or stratification. The banned-input list of §6 stands verbatim (`uoa_symbol_daily.fwd_return_*` — PI-001; every `oi_*` column **as a feature**; `sas_selection_excursion` / `outcome_*` / `level_hit_*`; the platform's `atr_pct` and `spot_close`). **Pre-committed cascade, decided now and deterministic, so nothing is chosen after the fact:** (i) if R1(a) confirms the multiplier was applied **at most once per row and stored whenever applied**, the §2.1 three-bucket reconstruction governs (item 1); (ii) if it does not — rows exist that the OI pass touched with a null or non-recoverable `oi_confirm_mult` — the conditioning variable falls back **automatically** to **`score_day` only**, the one bucket `uoa_screener.py:2236-2239` does not rewrite, with every other definition unchanged; (iii) if `score_day` is itself shown not to be point-in-time, Q014 needs a new rule-14 exception, the desk grants none, and it goes to `research/questions/DEFERRED.md` instead of locking. **R1(a) is blocking for exactly that reason.** | rule 14; DP-41; DP-05 (scope); manifest_v001 `availability.uoa_symbol` (`oi_confirm_*` = lag 1 session, "next-morning understates how late some historical rows were finalized"); Q013 item 11 (blocking KT check precedent) |
| 14 | Does DP-12 fire (matched control on a path-derived conditioning variable)? | DECIDED | **No.** DP-12 governs conditioning variables that are themselves part of the forward price path — an overnight gap (Q007), a fast start (Q008). Q014's `uoa5` count is built entirely from sessions `t−5..t−1` and is fixed at 16:05 ET on the pick night, before any post-decision bar exists. Pool A therefore stays **unmatched on `uoa5`** — matching on it would strip out the variable under test, and E1's whole content is the difference between two `uoa5` arms. Pool B *is* matched on `uoa5 ≥ 3`, but by H-040's own design of the second baseline, not by DP-12 compulsion. | DP-12 (scope — does not fire); Q013 item 9; PREREG §2.1, §3 |
| 15 | Picks whose L3 is at or through the entry `O_1` (`d_open ≤ 0`) | DECIDED | **Not a hit, kept in the denominator, counted and printed per arm**, with the identical rule applied to every control against its own synthetic target from its own `O_1`. Excluding them would filter the denominator on a session-t+1 price (rule 14) and would remove exactly the picks that gapped to target — plausibly more of them in the PERSIST arm, which is the effect the printed share exists to expose. The both-arms removal sensitivity is printed and **never decides**. | rule 5 ("a target already passed at that entry is not a hit"); DP-26; DP-41; Q011 item 7; Q013 item 13 |
| 16 | Same-session ties, and the use of hourly bars | DECIDED | **Counter-first (DP-27), on daily bars, for picks and controls alike; hourly bars are used by no endpoint.** Pool-B symbols have no hourly coverage and rule 5 requires one basis on both sides, so the asymmetry is structural and is **disclosed, not patched**. The count of ambiguous sessions is printed separately and **TIE is never a third category in a printed share**. | DP-27; rule 5; Q011 item 15 / Q013 item 15 (same treatment, same disclosure) |
| 17 | Whether any arm or cell is demoted to descriptive at lock (DP-43's demotion clause) | DECIDED | **Nothing among the primaries is demotable, and the clause is discharged at lock.** An E1-contributing night requires **≥ 1 eligible PERSIST pick and ≥ 1 eligible NONE pick** (§2.4), so the two arms are jointly the unit rather than separate floors: a thin arm shows up as *fewer contributing nights* and is handled by item 5's machinery (date moves out → single extension → DEFERRED), never by demoting an arm the estimator cannot do without. The `MID` arm is descriptive **by design** (§3 B4), not by demotion. Sub-cells — bear (expected SUPPRESSED, H-062 measures 0.157 bear-carrying nights/session in this window), the 90+ band, regime and tape cells — are governed by the standing rule: **below 20 contributing nights ⇒ SUPPRESSED, counts only, no point estimate**, and a SUPPRESSED sub-cell does **not by itself** make an endpoint INCONCLUSIVE (§8 clause 1 as drafted). **No demotion after lock, in either direction.** | DP-43 (demotion decided at lock, never afterwards); DP-21; Q013 item 16; Q011 item 9 form; PREREG §2.4, §5 |
| 18 | Window start and the in-sample contamination rule | DECIDED | **Pick nights ≥ 2026-06-01, and the April–May nights are not used at all — not even as a descriptive panel**, as drafted. EXPLORE_001 §G ran H-040's own persistence construction on those nights and reported the arm shares *and* the pooled matched-control excess by arm (−0.09 / +0.05 / +0.13) into the backlog, so they are contaminated for this question in the strongest sense. The window also sits entirely after the 2026-06-01 catalyst-layer fix (DP-06). The registrar's sealed-period contamination check (§6) stands as recorded: no desk output has read the 0 / 1–2 / 3+ contrast on nights ≥ 2026-06-01, and the ≥ 70 cut, the direction-matched label and the 5-session lookback all come from the in-sample seed. | DP-06; rule 3; DP-45 (the stricter reading — excluded outright rather than shown descriptively); PREREG §6 |
| 19 | Successor freezes, and what blocks the lock | DECIDED | **Lock pinned to `manifest_v001` / `manifest_prices_v001`; the successor pair is built and pinned at the decision date (routed R2).** Scope as the draft writes it, and the wider Pool-B scope is deliberate and must not be quietly narrowed: **(i)** `uoa_symbol` covering every session from **5 sessions before the window start** through the window end, including `oi_confirm_mult`; **(ii)** daily bars for **every candidate on every new night, published and unpublished** (Pool A); **(iii)** daily bars for **every symbol appearing in `uoa_symbol` with a directional label and a reconstructed `score_b* ≥ 70`** in the window (Pool B — wider than DP-23's default candidate-symbol scope, ≈ 500 symbols). Forward coverage 20 sessions beyond the last included pick night, 40 where the descriptive companion is computed. **Hourly bars are not required by any endpoint** (item 16). A second pair only if the DP-13 extension fires. Symbols without bars are dropped from their pool and **counted, never back-filled**; a materially truncated Pool B is a **Red Team flag, not a silent redefinition** (§10 threat 9). `eval.py` takes window start/end, manifest paths, exclusions path and output directory as arguments — no hard-coded dates, names or paths — records every sha256 and prints pre-lock and post-lock night counts separately, so one byte-identical script serves both runs. **R2 does not block the lock; R1(a) does** (item 13). | DP-23; DP-46; Q006 §5; Q011 item 14; Q013 item 12; PREREG §5 R2 |
| 20 | The `score_swing` / `score_long` rewrite as a platform defect (§10 threat 1) | DECIDED | **Already filed — it is `PI-013` (med, OPEN): "`uoa_symbol_daily.score_swing` / `score_long` overwritten in place by the next-morning OI-confirmation pass; no point-in-time copy."** §10 threat 1 cites PI-013 by id rather than saying the defect "belongs in `PLATFORM_ISSUES.md`", and keeps the sentence that **Q014 does not depend on it being fixed** — item 1's reconstruction and item 13's fallback both work on the data as it stands. No new PI entry is opened and no brief follows from this question. | DP-07; DP-48; `research/PLATFORM_ISSUES.md` PI-013 |
| 21 | Inference conventions (block length, resamples, seed, quotability) | DECIDED | **Stand as drafted.** Stationary block bootstrap over the ordered contributing nights, expected block length **10 sessions** (fixed here, not chosen after seeing results; the same length Q004/Q007/Q009/Q011 use for 20-session forward windows), 2,000 resamples, date-clustered CI printed alongside; permutation p with 10,000 draws, **seed 20260913**, the arm label permuted **within night** (E1) and the published/Pool-B label permuted within the night's persistent set (E2). Control rows never add to inferential n. Every number here rests on a 20- or 40-session basis ⇒ **NON_QUOTABLE** (rule 12). | DP-26; rule 6; rule 12; Q009 §4 / Q011 §4 (same block length and construction) |

## Settled at `record` (2026-09-13, R1 returned)

Source: `research/reports/STEWARD_Q014_exposure.md`, parts (a)–(d), counts only — no `results/`
directory exists for Q014, none was read, and no outcome number entered any decision below. These
items close the two ROUTED entries' blocking half and the two DEFAULTED entries' arithmetic. Nothing
here re-opens a settled item: items 1–21 stand exactly as decided, and every gate still fires on
`eval.py`'s measured counts at the decision pass, never on R1 or on the projection below.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 22 | R1(a) — is the persistence variable knowledge-time legal, and which branch of item 13's cascade fires? | DECIDED (ROUTED item 13 / R1(a) returned) | **Branch (i) fires: the §2.1 three-bucket reconstruction `score_b* = score_b / oi_confirm_mult` governs, and Q014 locks in its drafted form.** The Steward's verdict is **VERIFIED single application** on four independent readings, all on the full population rather than a sample: 1,190 non-null multipliers confined entirely to {0.90, 1.00, 1.05, 1.10} with **0** values outside it; **0** rows in any month where the OI pass ran (`oi_confirm_score` / `oi_confirm_ratio` / `oi_confirmed_contracts` non-null) but `oi_confirm_mult` is null — the unrecoverable population the PREREG feared **does not exist in this window**; **0 of 13,646** flow-setup-labelled rows with `score_day < 35`, i.e. `score_day` shows the same zero-inconsistency signature as a bucket never rewritten; **0 of 16,264** reconstructed `score_swing*` and **0 of 9,720** `score_long*` below the label's own 35 floor, including the single raw `score_long` borderline case, which resolves cleanly under **one** division. The reconstruction moves **3 of 369** arm assignments (0.8%, all MID→PERSIST by one step: APH 2026-06-05, APH 2026-06-08, MO 2026-07-24). **Branches (ii) and (iii) are void**, and with them **the conditional `registrar` route below** — no `DEFERRED.md` entry is written for H-040. `oi_confirm_mult` remains an inversion of a known mutation, never a feature; **no rule-14 exception is requested or granted and DP-05 is untouched** (DP-41). | item 13's pre-committed cascade (i); rule 14; DP-41; DP-05 (scope, untouched); STEWARD_Q014_exposure.md §(a) |
| 23 | The residual limitation R1(a) could not close — no OI-confirm run-history table | DECIDED | **Disclosed, not resolved, and it does not block.** The Steward reports that `uoa_screener.py:1996-2024` guards its own re-execution unless a force flag is passed, that the frozen data carries **no run-history table** for that pass (the same absence as PI-004 / PI-012's `super_agent_select_runs`), and that a **forced** manual re-run therefore cannot be positively excluded from the data alone; nothing in the data shows one. §10 threat 1 records this in those terms, cites **PI-013** by id (item 20) and states the bound the evidence does put on it: a second application would have to have produced a compound multiplier outside the four documented values (**0 observed**) *and* left every one of the 25,984 reconstructed label/score pairs consistent. The `updated_at − created_at` gap (median 143.3h with a multiplier vs 120.5h without) is recorded as **not usable as a signature** — `updated_at` is bumped by other backfills — and is cited neither as evidence for nor against. **No new PI entry**; no brief follows. | DP-07; DP-48; rule 14 (a disclosed bound, not a silent assumption); PI-013; PI-004 / PI-012 precedent |
| 24 | Does item 13's cascade stay live for the **post-lock** nights, which R1(a) could not cover? | DECIDED | **Yes — pre-committed now, deterministic, and evaluated before any outcome exists.** R1(a) verified sessions 2026-05-22..2026-08-12 only; the successor freeze (R2) brings nights the verification has not seen. `eval.py` therefore re-runs R1(a)'s checks (i) and (ii) — the multiplier value distribution, and the count of rows where the OI pass ran with a null multiplier — over **every** lookback session in the full registered window, pre-lock and post-lock, **inside the frozen pre-outcome table item 13 already requires it to build before the first session-t+1 bar is loaded**, and prints them per month. If any night in the window carries a multiplier outside {0.90, 1.00, 1.05, 1.10} or a single "ran but null" row, the conditioning variable falls back **automatically and for the whole window** to **`score_day` only** (branch (ii)), every other definition unchanged; if `score_day` itself fails its label-consistency check, the run is not made and Q014 goes to `research/questions/DEFERRED.md` (branch (iii), DP-41). The stricter of the two readings is taken without further argument, and the branch is fixed **now**, before any outcome exists, so nothing is chosen after the fact (rule 9). | item 13 (cascade, extended in scope not in substance); rule 9; rule 14; DP-41; DP-45 (the stricter reading) |
| 25 | The run-rate the schedule is projected on | DECIDED | **The pooled measured E1 rate, 22 / 51 = 0.4314 contributing nights per session**, over the whole sealed window. **No sub-window rate is substituted**: unlike Q015, where the rate was measured *declining* month over month and DP-45 forced the slowest, Q014's monthly E1 rate **rises** (June 8/21 = 0.381, July 9/22 = 0.409, August partial 5/8 = 0.625). The fastest month is **not** used — that would pull the date in, which DP-43 forbids — and the slowest single month (0.381, 21 sessions, which would set Monday **2027-05-03**) is not used either, because there is no measured decline to justify treating three months of noise as a trend, and because the case it guards against is exactly what **DP-13's single automatic extension** exists for: the extension date (**2027-05-17**) already sits *later* than the slowest-month projection. **E1 binds**, as the PREREG assumed but at 0.4314 rather than the drafted 0.65 — E2's 46 / 51 = 0.9020 clears both of its own floors months earlier. | DP-43 (the measured run-rate); DP-45 (never the rate that reaches a date sooner); DP-13; Q015 record precedent (slowest rate *when a decline is measured*); STEWARD_Q014_exposure.md §(c) |
| 26 | DP-43's demotion clause, discharged on measured numbers (item 17 confirmed) | DECIDED | **No arm is demoted; the clause is discharged at lock and does not reopen.** E1's contributing-night definition requires **≥ 1 eligible PERSIST *and* ≥ 1 eligible NONE pick on the same night** (§2.4), so at the 80-contributing-night floor both arms carry 80 nights by construction — a thin arm can only show up as a *later date*, which is exactly what happened (0.4314 vs the drafted 0.65, because the measured NONE arm is **8.4%**, less than half the 18% the EXPLORE_001 in-sample seed assumed, and 25 of 47 nights carry **zero** eligible NONE picks). E2's PERSIST arm contributes on **46 of 47** nights and is nowhere near the 20-night line. `MID` stays descriptive **by design** (§3 B4), not by demotion. Sub-cells — bear, the 90+ band, regime, tape and item 3's `prior_pub10 = 0` cell — remain governed by the standing rule (**< 20 contributing nights ⇒ SUPPRESSED, counts only, no point estimate**) on `eval.py`'s measured counts, and the window is **not** lengthened to rescue a stratum: DP-43 sizes the window on the two primary gates only. Item 3 already fixes the consequence if the `prior_pub10 = 0` cell is SUPPRESSED — **E1 is INCONCLUSIVE, not CONFIRMED** — which is the conservative direction and needs no further decision. | DP-43 (demotion decided at lock, never afterwards); DP-21; items 3 and 17; PREREG §2.4, §8 clause 1 |
| 27 | Pool A, Pool B and universe coverage — do any of the draft's construction risks bind? | DECIDED | **None binds in the sealed window; every diagnostic still prints, because the post-lock nights are unmeasured.** (a) The `completeness_score ≥ 35` screen (item 8) removes **0 of 2,354** same-night non-published candidates — the minimum observed is 65.4 — so Pool A is in practice the locked Q006 §3 construction here; the before/after pool-size print item 8 requires **stays**, since the screen is untested on post-lock nights. Per-pick Pool A size min 16 / median 26 / max 30, **0 of 369 picks** below the 3-neighbour minimum. (b) Pool B is thick: min 21 / median 56 / max 93 per PERSIST pick, **0 of 164** below the minimum, 46 of 47 nights contributing — **§10 threat 9 does not fire**, and E2 can carry a verdict. (c) The Pool-B price-coverage gap is real and is **counted, never back-filled**: **71 of 502** UOA symbols (14.1%) have no daily bars in `manifest_prices_v001`, costing **56 qualifying-but-dropped instances** across the 164 PERSIST picks (mean 0.34, max 2 per pick). §10 threat 9 records those figures, and **R2(iii)'s widened symbol scope is what closes the gap prospectively — it must not be narrowed** (item 19). (d) UOA universe coverage: 56 sessions, min 489 rows, **0 sessions below the 200-row floor**; median 1 symbol entering / 0 leaving per session. **0 picks** are lost to lookback coverage. | item 8; item 19; DP-23; PREREG §2.3, §10 threat 9; STEWARD_Q014_exposure.md §(c), §(d) |

**The `## Schedule` block below is the whole of DP-43's answer to items 4 and 5.** Both DEFAULTED
items stand as defaulted — E2 remains primary (item 4) and the window follows DP-43's recipe
(item 5); only the arithmetic was pending, and R1(b)+(c) have now supplied it.

## Corrections to silent choices

Applied by the Registrar with the rest (`@registrar apply Q014`). **R1(a) has returned (VERIFIED,
item 22), so `apply` is unblocked and runs now**; the record-time corrections are appended at the end
of this list.

- **§8 opening and §8 clause 7 — one MPE per endpoint, not one for both (item 6).** "**MPE for both:
  +5.0 pp**" is replaced by: **E1's MPE is 10.0 pp** — DP-20's 5.0 pp floor raised, with the one-line
  reason DP-20 requires, because E1 is a *difference of differences across two arms with small
  per-night cells*, the shape for which locked Q007 §8 set 10.0 pp on the Q003 §8 precedent — and
  **E2's MPE is 5.0 pp**, DP-20 unchanged, because E2 is a single-arm control-adjusted excess. Both
  two-sided. §8 clause 7's "**half the MPE (2.5 pp)**" becomes "**half the MPE (5.0 pp)**". Every other
  appearance of "5.0 pp" in §8's decision rules is re-read per endpoint. (DP-20; DP-44; DP-45;
  Q007 §8.)
- **§2.3 and §4 — the control's synthetic target is sized from the close-basis distance (item 7).**
  Replace `L3_c = C_c × (1 + dir_p × d_open,p × atr_pct_c)` with `d_close,p = dir_p × (L3_p − C_{t,p})
  / ATR_p` and `L3_c = C_c × (1 + dir_p × d_close,p × atr_pct_c)`, for **Pool A and Pool B alike**,
  graded from each control's own t+1 open over the same 20 sessions under the same
  "at-or-through-entry is not a hit" rule — the locked Q006 §3 step 3 construction verbatim. `d_open`
  survives only as the gap-through diagnostic and in the ATR-distance tercile. Add the one-line reason
  so the choice is not re-argued: sizing the control's target with the pick's *post-gap* distance while
  grading it from the control's *own* open subtracts each control's gap a second time, which is not
  "the same ATR distance" on both sides. (rule 5; Q006 §3.)
- **§2.3 — Pool A is the Q006 construction *plus* a completeness screen, and says so (item 8).** The
  phrase "the Q006 §3 / Q011 §3 construction" is qualified: no locked question's control pool carries
  a `completeness_score ≥ 35` filter. The screen stands (DP-26) and `eval.py` prints the candidates it
  removes and the per-pick pool size before and after it; the same screen is stated for the Pool-B
  **sub-pool** of non-published SAS candidates, and the note that Pool B proper cannot carry it is
  added rather than the asymmetry being left implicit.
- **§5 — the decision date, the extension and the DEFERRED fallback are DP-43 output, not a drafted
  projection (item 5).** The three dates stay in the file as a **floor**, with the sentence that
  R1(b)'s measured E1 contributing-night rate may push every one of them **out** and never pull one
  **in** (Q011 item 8), that the Steward fixes the exact session counts from the trading calendar when
  the successor freezes are built, and that the **12-month ceiling** applies: a projected initial
  decision date after **2027-09-13** means Q014 is **not locked** and goes to
  `research/questions/DEFERRED.md` with the date and the measured rate named. Keep verbatim: gates fire
  on `eval.py`'s measured counts, never on the projection or the run-rate; no interim looks.
- **§5 — the arm-split projection is labelled as an assumption, not a measurement.** The 32 % PERSIST
  / 18 % NONE split comes from **EXPLORE_001 §G's in-sample April–May read**, on nights this question
  excludes; §5 already names it, and must keep that label when R1(b)'s measured sealed-window `uoa5`
  distribution replaces it at `record`. The population funnel borrowed from
  `research/reports/STEWARD_Q011_exposure.md` (0.9216 contributing nights/session, ≈ 7.85 eligible
  picks/night) is a **measured** input and keeps its citation.
- **§2.1, §6 and §10 threat 1 — the reconstruction carries a pre-committed fallback (item 13).** Add
  the deterministic cascade: verified single application ⇒ three-bucket reconstruction; unverifiable ⇒
  **`score_day` only**, automatically, every other definition unchanged; `score_day` itself not
  point-in-time ⇒ **DEFERRED** (DP-41). Add the three diagnostics item 1 requires (non-null multiplier
  share and distribution; arm assignments changed by the reconstruction; reconstructed scores inside a
  ±0.5 rounding band of the 70 cut, with both readings printed).
- **§10 threat 1 — cite `PI-013` by id** instead of "belongs in `PLATFORM_ISSUES.md`" (item 20).
- **§11 "Open decisions before lock" — delete the section entirely** once the above are applied;
  nothing may read as open at lock. After applying, `grep` the file for `open decision`,
  `Recommendation:`, `MPE for both`, `d_open,p × atr_pct_c` and `belongs in` — every hit must be gone
  or deliberate.
- **Status line and `state.json` — bookkeeping.** The Status line drops "DRAFT … open decisions in
  §11" and records the lock; the controller advances Q014 to `PREREG_LOCKED --by desk` and writes
  `schedule.json` from `## Schedule` in the same step (DP-46). The Decision-maker edits neither file.

### Added at `record` (R1 returned) — apply with the rest

- **§5 — every projected date is replaced by the `## Schedule` block below, verbatim.** Window end
  **2027-02-25**, decision Monday **2027-04-05**, single DP-13 extension to pick nights ..**2027-04-09**
  with decision Monday **2027-05-17**. The drafted floor (end 2026-11-30 / Monday 2027-01-11 /
  2027-02-22) is **superseded, moved out by 12 weeks, never in** (Q011 item 8, DP-45). Keep verbatim:
  gates fire on `eval.py`'s measured counts, never on this projection or on a run-rate; no interim looks.
- **§5 — the arm split and the contributing-night rate are now measured, and are labelled as such.**
  Replace EXPLORE_001 §G's in-sample **32% PERSIST / 18% NONE** assumption and the drafted **0.65
  contributing nights/session** with the sealed-window measured values, citing
  `research/reports/STEWARD_Q014_exposure.md` §(b)/§(c) and stating that they are **counts only, no
  outcome of any kind was computed** (rule 3 is intact): 369 eligible picks over 47 nights,
  **PERSIST 164 (44.4%) / MID 174 (47.2%) / NONE 31 (8.4%)**; **E1 22/51 = 0.4314** and **E2 46/51 =
  0.9020** contributing nights per session; the funnel 383 → 369 (8 no-L3, 4 `outcome_target_invalid`,
  2 wrong-side L3, 0 lost to lookback coverage or forward maturity); one night with zero eligible picks
  (2026-06-02, all 8 picks lack a swing lane, the same night Q009/Q011 lose). The in-sample seed keeps
  its label as an **assumption that the measurement contradicted** — NONE is less than half as thick as
  assumed, and that is why the date moved out. (Item 25; item 26.)
- **§2.1, §6 and §10 threat 1 — the cascade is discharged for the sealed window and stays live for the
  post-lock nights.** State the R1(a) result in the four numbers that carry it (0 multiplier values
  outside {0.90, 1.00, 1.05, 1.10} of 1,190; 0 "ran but null" rows in any month; 0 of 13,646 `score_day`
  and 0 of 25,984 reconstructed `score_swing*`/`score_long*` label inconsistencies; 3 of 369 arm
  assignments moved), record that **branch (i) governs**, and keep the cascade text as a **standing,
  pre-committed branch over the whole registered window** with `eval.py` re-running checks (i) and (ii)
  per month inside the pre-outcome frozen table (item 24). Add the residual limitation in the Steward's
  own terms — no OI-confirm run-history table, so a **forced** re-run cannot be excluded from the data
  alone; none is visible; `updated_at − created_at` is **not** a usable signature — and cite **PI-013**
  by id. (Items 22, 23, 24.)
- **§2.3 and §10 threat 9 — the pool diagnostics are now measured, and the print requirements stand
  anyway.** Record: the `completeness_score ≥ 35` screen removes **0 of 2,354** candidates in the sealed
  window (minimum observed 65.4), Pool A per-pick size min 16 / median 26 / max 30 with **0 of 369**
  picks below the 3-neighbour minimum, Pool B min 21 / median 56 / max 93 with **0 of 164** PERSIST
  picks below it, and **71 of 502 UOA symbols (14.1%) without daily bars in the pinned price freeze,
  costing 56 qualifying-but-dropped instances**. §10 threat 9 states that it **did not fire in the
  sealed window** and that R2(iii)'s widened symbol scope is what keeps it from firing after the lock.
  Every diagnostic item 8 and item 19 require is still printed — the post-lock nights are unmeasured.
  (Item 27.)
- **§2.4 — no arm is demoted.** Add the one line DP-43's demotion clause needs at lock: PERSIST and
  NONE are jointly the E1 contributing-night unit and carry 80 nights each at the floor by
  construction; E2's PERSIST arm contributes on 46 of 47 nights; `MID` is descriptive by design; the
  window is **not** lengthened to rescue a stratum, and a SUPPRESSED `prior_pub10 = 0` cell makes E1
  **INCONCLUSIVE** under item 3. No demotion after lock, in either direction. (Item 26.)

**Conflicts with already-locked questions (for the Red Team; the locked files stand, nothing is
edited):** none new. Two standing ones are repeated only so Q014's construction is read with them in
view — (a) Q006/Q007 include pick night **2026-06-26**, which `exclusions_v003.json` now excludes
(already flagged in Q009's, Q011's and Q013's DECISIONS.md; Q014 uses v003); (b) Q004 §2's looser
publication predicate (`selected_rank` only) versus DP-28, which Q014 follows. **Not a conflict:**
Q007 §8's 10.0 pp and Q011's 5.0 pp are the *same* rule applied to two different estimator shapes, and
item 6 places Q014's two endpoints on the correct side of it.

## Defaulted on Haci's behalf

- #4 E2's status — chose both E1 and E2 primary, BH across m = 2, each with its own 80-night gate;
  not taken: E2 descriptive, floor reached sooner — DP-43. Overturn = successor question.
- #5 window and decision date — chose DP-43's recipe from 2026-06-01; **settled at `record` on the
  Steward's measured E1 rate: window 2026-06-01..2027-02-25, decide Monday 2027-04-05, one automatic
  extension to ..2027-04-09 / Monday 2027-05-17, then DEFERRED** — 12 weeks later than the drafted
  floor, pushed out and never pulled in; not taken: a shorter sealed-only window, HISTORICAL_ONLY —
  DP-43. Overturn = successor question.
- #5b rate used — chose the pooled measured 0.4314 E1 nights/session; not taken: the fastest month
  (0.625, forbidden) and the slowest (0.381, no measured decline) — DP-43/DP-45. Overturn = successor
  question.

## Routed requests

### data-steward

**R1 — RETURNED AND CLOSED, 2026-09-13** → `research/reports/STEWARD_Q014_exposure.md`, all four
parts, protocol observed (counts only; no touch, no return, no MAE, no picks-minus-control
difference). (a) **VERIFIED single application** ⇒ item 13 branch (i), Q014 locks in its drafted form
(item 22), with one disclosed limitation (item 23). (b)+(c) fix the `## Schedule` below (items 25–27).
**Nothing further is asked of the Steward for the lock.** The original request is kept verbatim below
for the audit trail; do not re-send it.

**R1 — parts (b)–(d) are the exposure count; part (a) is BLOCKING for the lock. Counts only, no
outcome of any kind.** Paste-ready:

**R1 — knowledge-time verification and exposure count for Q014 (UOA persistence × SAS selection,
H-040). Part (a) is blocking: Q014 cannot lock without it.** On the frozen data only
(`research/data/manifest_v001.json` → `v001_uoa_symbol.parquet` and `v001_sas_candidates.parquet`, plus
`research/data/manifest_prices_v001.json`), pick nights **2026-06-01** through the last night with a
matured 20-session forward window, non-excluded per `research/data/exclusions_v003.json`
(`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪
`uncorroborated_publication_runs.trading_dates`), published picks under the DP-28 predicate
(`qualified IS TRUE AND selected_rank IS NOT NULL`) carrying a
`public_payload_json.lane_plans.swing_trading.targets[0]` (L3):
**(a) Knowledge-time verification of the persistence variable — blocking.** Q014 reconstructs the
16:05 ET bucket score as `score_b* = score_b / oi_confirm_mult` (non-null multiplier) or `score_b`
(null), because the next-morning OI-confirmation pass overwrites `score_swing` and `score_long` in
place (volatilx `services/uoa_screener.py:2236-2239`, multiplier stored in `oi_confirm_mult`,
`:2223-2232`; `label_*` written once at 16:05 from the pre-multiplier score, `:1728-1734`). Please
establish, on `uoa_symbol` rows for every session in the lookback range (window start **minus 5
sessions**) through the window end: **(i)** the count and share of rows with a non-null
`oi_confirm_mult` and the distribution of its values — is it confined to {0.90, 1.00, 1.05, 1.10}, and
are there values outside that set (which would indicate more than one application)? **(ii)** the count
of rows that show evidence the OI pass **ran** — any non-null `oi_confirm_score`, `oi_confirm_ratio`
or `oi_confirmed_contracts` — while `oi_confirm_mult` is **null**, i.e. rows whose 16:05 score is not
recoverable, by month and as a share; **(iii)** whether `score_day` shows any sign of the same
rewrite (`created_at` / `updated_at` pattern, or `score_day` values inconsistent with `label_day`'s
16:05 derivation); **(iv)** for a sample of rows, whether the reconstructed `score_b*` is consistent
with the frozen `label_b` (a `BULLISH_FLOW_SETUP` / `BEARISH_FLOW_SETUP` label whose own 16:05 score
would have to be below the label's threshold is evidence the multiplier was applied more than once).
**(b) The `uoa5` distribution, on both candidate definitions.** For every eligible pick, the count of
sessions among the 5 strictly before the pick night on which `strong(symbol, u, dir) = 1` —
`strong` = any bucket `b ∈ {day, swing, long}` with `score_b* ≥ 70` **and** `label_b` matching the
pick's `dominant_direction` — reported as the full `uoa5 = 0..5` histogram and as the three arms
`PERSIST` (≥ 3) / `MID` (1–2) / `NONE` (0); and **the same histogram computed on `score_day` only**,
so the schedule can be derived under whichever definition item 13's cascade selects. Also: how many
arm assignments differ between the reconstructed and the frozen (unreconstructed) values.
**(c) Contributing-night counts and pool sizes.** On Q014 §2.4's definitions — **E1**: matured
non-excluded nights carrying **≥ 1 eligible PERSIST pick with ≥ 3 Pool-A controls** *and* **≥ 1
eligible NONE pick with ≥ 3 Pool-A controls**; **E2**: nights carrying **≥ 1 eligible PERSIST pick
with ≥ 3 Pool-B controls** — with the eligibility funnel printed in full (published/matured →
null-ladder → `outcome_target_invalid` → wrong-side L3 (`dir × (L3 − C_t) ≤ 0`) → < 60 daily bars →
lookback coverage → missing t+1 bar → **eligible picks**), the counts **per month** and the measured
**contributing nights per session** for each endpoint separately. Pool A = the 10 nearest same-night
non-published `sas_candidates` rows of the same direction with `completeness_score ≥ 35` on
`beta60` / `atr_pct` / `runup20` from `prices_daily_split` bars ≤ t, night-median/MAD standardized,
Euclidean; Pool B = the 10 nearest same-night non-published **UOA-universe** symbols that themselves
carry `uoa5 ≥ 3` in the pick's direction, same features, same standardization. Report the **per-pick
pool-size distribution for both pools**, the **share of picks below the 3-neighbour minimum** for
each, the number of Pool-B symbols dropped for want of daily bars in the pinned price freeze, and the
size of the Pool-B **sub-pool** restricted to same-night non-published SAS candidates.
**(d) UOA universe coverage.** Per-session `uoa_symbol` row counts across the window and the five
sessions before it, flagging any session below **200** rows (Q014 excludes picks whose lookback
touches such a session), plus universe turnover (symbols entering/leaving between adjacent sessions).
**Protocol (binding): counts only.** Session t+1's official open may be read for pool construction and
for the `d_open ≤ 0` count; for sessions ≥ 2 only the **existence** of bars (maturity/coverage) may be
checked, never their values. **No touch of any level, no return, no MAE, no P&L, no
picks-minus-control difference and no outcome of any kind may be computed or reported** — the same
discipline as `STEWARD_Q011_exposure.md` and `STEWARD_Q009_exposure.md` §R1. Definitions: `C_t` = the
actual pick-night regular-session close from `prices_daily_split` (never `spot_close`); ATR14 from
`prices_daily_split` bars ≤ t (never the platform's `atr_pct`, PI-003); `dir` = +1 bullish / −1
bearish from `dominant_direction`.
**What it decides.** (a) **Whether Q014 exists in its drafted form:** a verified single application
keeps the three-bucket definition; unrecoverable rows switch it automatically to `score_day` only; a
`score_day` that is itself not point-in-time means a new rule-14 exception, which the desk does not
grant (DP-41), and Q014 goes to `research/questions/DEFERRED.md` (exception named: `uoa_symbol`,
`score_swing` / `score_long` / `score_day`, 16:05 ET on each lookback session) instead of locking.
(b)+(c) **the whole §5 schedule** (DECISIONS.md item 5, DP-43): the measured **E1** contributing-night
rate — E1 binds — fixes the window end, the decision date (window end + 20 sessions + one week, first
Monday on or after, never earlier than the drafted **Monday 2027-01-11**) and the single DP-13
extension (+30 sessions); **if 80 contributing nights per primary and 30 post-lock contributing nights
cannot be projected by 2027-09-13, Q014 is DEFERRED with that date and the measured rate named, on the
H-062 precedent, rather than locked.** (c) also settles whether the drafted 0.65 contributing
nights/session survives contact with a measured arm split, and whether Pool B is thick enough for E2
to carry a verdict at all (§10 threat 9).

**R2 — OPEN, not a blocker for lock. Dates now fixed by R1: due at `decision_date` = Monday
**2027-04-05**, covering pick nights through the registered window end **2027-02-25**; a second pair
only if the DP-13 extension fires, in which case it covers through **2027-04-09** and is due Monday
**2027-05-17**.** Paste-ready (re-issued at `record` with the concrete dates; supersedes the wording
below it, which is otherwise unchanged):

**R2 — successor freezes for Q014 (DP-23, with a widened symbol scope).** Build and pin the successor
selection freeze `manifest_v002` (same SQL, same exclusion criterion as v001) and the successor price
freeze `manifest_prices_v002` (same Alpaca queries) covering pick nights after **2026-09-10** through
Q014's registered window end **2027-02-25** (lookback begins 5 sessions before the window start,
2026-05-22), with **(i)** `uoa_symbol` covering every session from **5 sessions
before the window start** through the window end, **including `oi_confirm_mult`, `oi_confirm_score`,
`oi_confirm_ratio` and every `label_*` / `score_*` column** (the reconstruction and its audit need
them; none is used as a feature); **(ii)** daily bars for **every candidate on every new night,
published and unpublished** (Pool A needs their pick-night closes, prior bars for
beta60/atr_pct/runup20, t+1 opens and forward bars); and **(iii)** daily bars for **every symbol
appearing in `uoa_symbol` with a directional label and a reconstructed `score_b* ≥ 70`** anywhere in
the window — this is wider than DP-23's default candidate-symbol scope and is what Pool B is made of
(≈ 500 symbols). Forward coverage **20** sessions beyond the last included pick night, **40** where
the descriptive 40-session companion is computed. **Hourly bars are not required by any Q014
endpoint.** The decision and extension dates are **already fixed** at `record` (2027-04-05 /
2027-05-17, computed on the NYSE session calendar — see `## Schedule`); please re-verify them against
the exchange calendar published for 2027 when the freeze is built and report any **later** date, never
an earlier one. Symbols without bars are dropped from their pool and **counted, never
back-filled**; a materially truncated Pool B is flagged to the Red Team rather than absorbed silently.
**Standing from R1: 71 of 502 UOA symbols (14.1%) had no daily bars in `manifest_prices_v001`, costing
56 qualifying-but-dropped Pool-B instances — closing that gap is what scope (iii) is for.**

### registrar (conditional, fires only on an R1(a) total failure) — **VOID, does not fire**

**R1(a) returned VERIFIED (item 22): branch (i) governs, no `DEFERRED.md` entry is written for H-040,
and nothing is routed to the Registrar here. The conditional is kept for the audit trail only.**

**If R1(a) shows that neither the three-bucket reconstruction nor `score_day` alone is point-in-time:**
write the `research/questions/DEFERRED.md` entry for **H-040**, naming the exception the question
would need — table `uoa_symbol`, columns `score_swing` / `score_long` / `score_day` (and the
`label_*` companions), time 16:05 ET on each of the five lookback sessions — the evidence from R1(a),
the link to `PI-013`, and what would move it back into the backlog (a point-in-time score column the
OI pass cannot overwrite, or an append-only audit row). Q014 is **not** locked in that branch
(DP-41, DP-43). If only the *swing/long* buckets fail, nothing is routed here: item 13's cascade
switches the definition to `score_day` and Q014 locks.

## Schedule

**Filled at `record` (2026-09-13) from `research/reports/STEWARD_Q014_exposure.md` §(c) by DP-43's
recipe, on the pooled measured **E1** contributing-night rate (E1 binds; E2's 0.9020/session clears
both of its own floors months earlier). Written verbatim to
`research/questions/Q014_uoa_persistence/schedule.json` by the Registrar at `apply` / lock (DP-46).**

decision_date: **2027-04-05** (Monday) · extension_date: **2027-05-17** (Monday) · hard_stop: **none**
(DP-13's single automatic extension, then DEFERRED, replaces it) · rule: **fixed** · window: pick
nights **2026-06-01 .. 2027-02-25** (after `exclusions_v003.json`; in-window that removes 2026-06-26,
2026-07-02, 2026-07-06, and whatever later nights the file names at the decision pass — no date is
hard-coded, item 9) · extended: **false** · gates: **per primary endpoint** — ≥ 80 contributing nights
(DP-21, on §2.4's own per-endpoint definitions: E1 needs ≥ 1 eligible PERSIST **and** ≥ 1 eligible NONE
pick with ≥ 3 Pool-A controls on the same night; E2 needs ≥ 1 eligible PERSIST pick with ≥ 3 Pool-B
controls) **and** ≥ 30 contributing nights dated after the lock commit (DP-24), both on `eval.py`'s
measured counts at the decision pass; a shortfall on one endpoint is never covered by the other's
count, and a gate shortfall is **never** INCONCLUSIVE · ceiling: **cleared** — 2027-04-05 is
**5.4 months** inside DP-43's 2027-09-13 date, so Q014 is **locked, not DEFERRED**.

- **Rate used: 0.4314 E1-contributing nights per session** (22 of 51 elapsed sessions,
  2026-06-01..2026-08-12), the pooled measured rate. The monthly series **rises** (June 8/21 = 0.381,
  July 9/22 = 0.409, August partial 5/8 = 0.625), so unlike Q015 there is no measured decline to force
  a sub-window rate; the fastest month is not used (DP-43 forbids pulling a date in) and the slowest
  (0.381 → Monday 2027-05-03) is not used either, because the case it guards is what DP-13's automatic
  extension covers, and the extension date is **later** than it. E2's 0.9020/session is not binding.
  (Item 25.)
- **decision_date arithmetic, on the exact NYSE session calendar.** 58 further E1-contributing nights
  are needed beyond the 22 measured; 58 / 0.4314 = 134.5 → **135 sessions** (a fractional session
  rounds **up**). Counting real NYSE sessions from 2026-08-13 — Aug 13, Sep 21 (Labor Day 09-07 shut),
  Oct 22, Nov 20 (Thanksgiving 11-26), Dec 22 (Christmas 12-25), Jan 19 (New Year 01-01, MLK 01-18),
  Feb 18 to the 25th (Presidents' Day 02-15) — the 135th session, and so the projected 80th
  contributing night and the **window end**, is **2027-02-25**. + **20** sessions maturity (DP-09) =
  **2027-03-25** (Good Friday 2027-03-26 falls after it and does not bite); + one week freeze margin =
  2027-04-01; **first Monday on or after = 2027-04-05**.
  **This is 5 calendar days later than the Steward's 2027-03-29**, and the difference is deliberate:
  §(c)'s projection uses a plain business-day calendar, which ignores the **six** market holidays in
  that span. The exchange-calendar date is the correct one and it moves the date **out**; a projection
  may push a drafted date out, never pull one in (DP-43, DP-45; Q011 item 8). Against the drafted floor
  of Monday 2027-01-11 it is **out by 12 weeks**, because the measured NONE arm (8.4%) is less than
  half the in-sample seed's assumed 18%.
- **extension_date arithmetic (DP-13, +30 sessions, fires automatically on `eval.py`'s measured counts
  with the byte-identical `eval.py`, no new question to Haci):** window +30 NYSE sessions from
  2027-02-25 → pick nights **2026-06-01 .. 2027-04-09** (Good Friday 2027-03-26 shut); 2027-04-09 + 20
  sessions = **2027-05-07**; + one week = 2027-05-14; **first Monday on or after = 2027-05-17**. If a
  gate is still short there the answer is **DEFERRED** — never a second extension, never a reduced
  gate, never an under-powered run, and never INCONCLUSIVE.
- **DP-24 is not binding and this is not HISTORICAL_ONLY.** 114 of the 135 projected sessions fall
  after the lock commit (21 elapse between 2026-08-13 and the 2026-09-13 lock), projecting ≈ 49 E1
  post-lock contributing nights against the 30 required; E1's 30-post-lock floor alone would decide on
  **2027-02-01** and E2's earlier still. PROSPECTIVELY_CONFIRMED is reachable from this run by design,
  **DP-31 does not apply**, and no successor replication question is drafted.
- **Demotions, settled at lock and final:** none. PERSIST and NONE are jointly E1's contributing-night
  unit and carry 80 nights each at the floor; E2's PERSIST arm contributes on 46 of 47 nights; `MID` is
  descriptive by design. Sub-cells stay under the standing < 20-night SUPPRESSED rule on measured
  counts, and the window is not lengthened to rescue one. (Item 26.)
- **note:** _PREREG §5 / DP-43 / DP-13 / DP-21 / DP-24 / DP-45. Every gate is evaluated on `eval.py`'s
  measured counts from the frozen data at the decision pass, never on R1, on this projection or on a
  run-rate; `eval.py` runs **once** and there are no interim looks (rule 9). Routed **R2** (successor
  freezes through 2027-02-25, widened Pool-B symbol scope, 20 forward sessions — 40 for the descriptive
  companion) is due at `decision_date`; a second pair only if the extension fires. **R1 is returned and
  closed.**_

## Standing rules added

_none._ **The `record` step adds none either:** the schedule is DP-43 arithmetic on the Steward's
measured numbers, and items 22–27 are applications of items 13, 17 and 19 to a returned routed
request. Every item here is settled by an existing `DP` entry, a locked precedent or one defensible
technical answer, and the two DEFAULTED items are applications of DP-43. **No `DP` entry is created
from a DEFAULTED item** — a default is the desk acting on Haci's behalf, not an answer from him
(DP-40); only an answer of his becomes a Confirmed row.

## Standing rules proposed

Written down because they would generalise, **not added** to `research/DECISION_POLICY.md`. Each needs
Haci's word (or a later `--ask` cycle) before it becomes a `DP` row.

- **P-5 (would sharpen DP-20): the MPE follows the estimator's shape, not the question.** A
  single-arm control-adjusted touch-rate excess takes DP-20's **5.0 pp**; a **difference of
  differences** across two arms with small per-night cells takes **10.0 pp**; a paired contrast of two
  plans on the *same* picks takes 5.0 pp. Rationale: Q007 §8 raised it, Q011 item 10 declined it and
  Q014 item 6 needed both readings in one question — stating the rule once stops it being re-argued
  per draft.
- **P-6 (would extend rule 5's control requirement): a control's synthetic target is sized from the
  same basis the pick's distance is measured on, and both are graded from their own entry.** Where the
  entry is the t+1 open, the distance is still measured close-to-target on both sides (Q006 §3 step 3)
  — mixing a post-gap pick distance with a close-anchored control target subtracts the control's gap
  twice. Rationale: Q014 item 7; the same error is easy to reintroduce in any question whose entry is
  not the close.
- **P-7 (would extend DP-41): a question whose conditioning variable is stored in a column the
  platform overwrites carries a pre-committed fallback definition, decided at lock.** Verified exact
  reconstruction ⇒ the full definition; unverifiable ⇒ the narrower definition built only from columns
  nothing rewrites; that column contaminated too ⇒ DEFERRED. **The verification is re-run by `eval.py`
  over the whole registered window inside the pre-outcome table, because a Steward check made at lock
  can only cover the sealed nights.** Rationale: Q014 items 13 and 24; it converts an
  R-1 that would otherwise stall the queue into a deterministic branch fixed before any outcome exists.
- **P-8 (would sharpen DP-43): a projected floor date is computed on the exchange's session calendar,
  not on a business-day calendar, and a business-day projection is treated as a floor.** Run-rates are
  measured per NYSE session, so a forward projection in business days silently gains a day per market
  holiday and always errs *early* — the one direction DP-43 forbids. Rationale: Q014's `record` — the
  Steward's business-day projection gave Monday 2027-03-29 and the session-calendar computation gives
  Monday 2027-04-05, six holidays' worth; Q015 hit the same conversion and happened to land on the same
  Monday either way. Stating it once stops the arithmetic being re-derived, and re-derived differently,
  per question.
