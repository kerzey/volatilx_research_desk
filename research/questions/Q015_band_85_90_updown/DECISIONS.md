# Q015 — decisions before lock
Run: 2026-09-13 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 3 items
Recorded: 2026-09-13 by decision-maker (autonomous) · Source: `research/reports/STEWARD_Q015_exposure.md` (R1, returned) — schedule settled, no item left open
(+ items 4–21: the DP-compliance confirmations the Registrar needs when it applies, and the choices
the draft made silently that a `DP` entry or a locked precedent settles)

**Mode: autonomous (`--autonomous`).** DP-40..48 are in force: **no decision is put to Haci before
lock.** What would have been an ASK is `DEFAULTED` — R-1 → **DP-41**, R-2 → **DP-42**, R-3 →
**DP-43**, R-4 → **DP-44**, R-5 → **DP-45**; otherwise the Registrar's recommendation unless a DECIDE
ground gives another answer (DP-40), and where two options differ only in strictness, the stricter.
Every DEFAULTED item is listed under "Defaulted on Haci's behalf" and on the board; the locked
question stands (rule 3) and Haci overturns any of it by asking for a successor question, never by
editing the locked file.

**Summary: 19 DECIDED, 2 DEFAULTED (both R-3 → DP-43), 1 ROUTED open (R2 successor freezes — due at
the decision date, not blocking), 0 ASK.** Two of the draft's three open items are settled by a locked
precedent or by one defensible technical answer; the third (H-060's missing baselines) and the
schedule are R-3 and are defaulted under DP-43.

**R1 has returned (`research/reports/STEWARD_Q015_exposure.md`, 2026-09-13) and Q015 is clear to
lock.** R1 was counts-only and decided two things and nothing else: (i) whether 80 paired contributing
nights and 30 post-lock paired contributing nights are projectable inside DP-43's 12-month ceiling —
**they are, under all three measured rates including the most pessimistic**, so Q015 is **locked, not
DEFERRED**; and (ii) the §5 window end, decision date and extension date, now computed below at
`record` from the measured rate. Every date moved **out** from the drafted floor and none moved **in**
(DP-43, DP-45; Q011 item 8): decision date **Monday 2027-01-18 → Monday 2027-08-30**, extension
**Monday 2027-03-01 → Monday 2027-10-11**. Everything else in this file was already final. **Nothing
in R1 is an outcome** — the report is a funnel, band counts, contributing nights, coverage and pool
sizes; no touch, no UPDOWN, no revisit, no plan result, no band difference. No `results/` directory
exists and none was read.

**State note:** `research/questions/Q015_band_85_90_updown/state.json` reads `PREREG_DRAFT`
(registrar, 2026-09-13T21:05Z) and was not touched at `record`. R1 has returned; when
`@registrar apply Q015` runs, the controller advances Q015 to `PREREG_LOCKED --by desk`, writing `schedule.json` from the `## Schedule` block in
the same step (DP-46). No `results/` directory exists and none was read; no parquet, no weekly and no
daily report was opened; `PREREG.md` was not edited.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | H-060's named baselines (`<80`, `90+`) cannot be tested; what replaces them (draft item 1) | **DEFAULTED** | **Option A — the primary comparator is band B = 80–85, paired within night; bands E (90+) and U (<80) are descriptive from lock and SUPPRESSED below 20 contributing nights.** The `<80` baseline is closed by configuration, not by thinness (`publication_floor = 80.0`, 2026-07-07, volatilx `services/super_agent_select_models.py:86-91`; DP-28 excludes the dark rows it becomes), so no window recovers it; `90+` as a *primary* comparator needs 80 paired contributing nights on a cell measured at 18 nights per 50 and shrinking, which lands the decision date past **DP-43's 12-month ceiling** — a ceiling that sends a question to DEFERRED rather than being stretched to fit. The registrable contrast is the adjacent traded band, which is also the **stricter** of the three (one score step, same night, same publication process; §10 threat 7 states the false-NULL direction of error plainly). H-060 is **not** deferred, because the contrast it is really about — 85–90 versus the band below it — is testable now at full floors. A properly powered 85–90 vs 90+ contrast is a **separate future question**, registrable on the H-062 trigger pattern (§3 B1′). **R1 confirms the premise on measured counts:** band E carries **15 eligible picks on 14 of 48 matured nights** (10 in June, 4 in July, **0** in the matured part of August) and band U **1 pick on 1 night** — both below the 20-contributing-night floor, both **SUPPRESSED**, and band E is shrinking exactly as drafted. | DP-43 (12-month ceiling; arms below 20 contributing nights demoted to descriptive **at lock**, never dropped afterwards); DP-21; DP-28; DP-45; H-062 DEFERRED precedent; **not taken:** DEFER H-060 until elite exposure recovers |
| 2 | Which line is "the swing counter level" (draft item 2) | DECIDED | **Option A — `S` = the printed swing-lane stop, `public_payload_json.lane_plans.swing_trading.stop`**, in the signal-date split basis, used **only as a measured line and never as an exit** (rule 5, DP-02). Option B (`sell_setup.targets[0]` / `swing_c1` from the analysis-report blob) is **not in any freeze** — `analysis_report_path` is a path, not content — so B is not a choice between two available lines but a request for a new freeze of unknown coverage; the platform itself falls back to the printed stop in exactly that case (volatilx `services/sas_excursion.py:303-328`). This is the same line Q009 and Q010 use (`S = lane_plans.swing_trading.stop`) and the same line Q008 §4 uses for its counter level, on overlapping nights — consistency across the three questions that read this line matters more than the platform's preferred label. The **−1.0 ATR** version stays printed beside every primary (§4 secondaries), and any §9 line must say the level is the printed stop (§10 threat 3). | Q009 §2/§4 and Q010 (locked, same line); Q008 §4; DP-02; DP-23 (freeze scope); one defensible technical answer — B's data does not exist in the frozen set |
| 3 | Entry basis (draft item 3) | DECIDED | **Option A — `X = C_t`, the pick-night regular-session close** from `prices_daily_split` (never `spot_close`), the DP-03(a) after-hours proxy in **DP-11's** construction, applied identically to picks and to B2's distance-matched controls. Rule 5 requires one basis on both sides and **only the close exists on the control side**; that, not a preference, settles it. Q009 — the nearest question on the desk, the same two lines in the opposite order — was moved to `C_t` for the same reason, and Q007 uses it. The **next-session-open basis (DP-03(b)) is computed and printed for every endpoint as a named sensitivity**, with the not-takeable count; a pick whose L3 is already through at that basis is not a hit there (rule 5). `C_t` is also the ATR, `d_L3`, `d_S`, beta60 and runup20 reference. | DP-11; DP-03(a); DP-42 (entry basis by DP-03/DP-11); rule 5 (one basis for picks and controls); Q009 DECISIONS §"entry basis"; Q007 §4 |
| 4 | Window, decision date, single extension, DEFERRED fallback (**R-3**) | **DEFAULTED** | **DP-43's fixed recipe, arithmetic computed at `record` from R1's measured paired-night rate.** Window: pick nights **2026-06-01** (DP-06; the in-sample Apr–May nights EXPLORE_001 read are excluded outright, §6) through the session at which the measured rate projects **≥ 80 contributing nights per primary endpoint on its own definition** (DP-21 — P1/P2 on the paired A-and-B night, P3 on the band-A night) **and ≥ 30 contributing nights dated after the lock commit** (DP-24). **Decision date** = window end + **20** sessions maturity (DP-09) + one-week freeze margin, first Monday on or after — and **never earlier than the drafted Monday 2027-01-18** with its window end 2026-12-04: R1 pushes the date **out**, never **in** (Q011 item 8). **One automatic DP-13 extension**: window +30 sessions, maturity and margin recomputed, first Monday on or after (drafted floor: window end 2027-01-20, decision **Monday 2027-03-01**). **Then DEFERRED** — no second extension, no reduced floor, no under-powered run, and a gate shortfall is **never** INCONCLUSIVE. Gates fire on **`eval.py`'s measured counts** at the decision pass, never on R1 or a run-rate. **12-month ceiling: if the projected initial decision date lands after 2027-09-13, Q015 is not locked** — it goes to `research/questions/DEFERRED.md` with that date and the measured rate named (H-062 precedent). No interim looks; `eval.py` is written once (rule 9) and run once. **SETTLED at `record` from R1, on the slowest measured rate (0.2500 paired-contributing nights per session — the partial-August rate): window = pick nights 2026-06-01..2027-07-20; decision date Monday 2027-08-30; the single DP-13 extension runs the window to 2027-08-31 with decision Monday 2027-10-11; then DEFERRED. The 12-month ceiling is cleared (2027-08-30 ≤ 2027-09-13, 14 days of margin), so Q015 locks.** See `## Schedule`. | DP-43; DP-13; DP-21; DP-24; DP-45; Q011 item 8; Q013 item 3; **not taken:** a shorter window reaching a 2026 date on the projected rate |
| 5 | MPEs for the three primaries | DECIDED | **P1 = +5.0 pp** (DP-20 exactly — a within-night paired touch-rate contrast, the Q011 structure; **no uplift proposed and none warranted**). **P2 = P3 = 0.25 ATR** (DP-10 via DP-44 — the standing per-trade ATR number), measured **per published pick in the band, never rescaled to a per-toucher basis** (rescaling divides a diluted mean by a smaller denominator and lowers the bar). All three **two-sided**; a result beyond MPE with the opposite sign is a confirmed finding with that sign. **No money-unit MPE is invented** anywhere (DP-44). | DP-20; DP-10; DP-44; Q013 item 4; Q011 item 10; PREREG §8 as drafted (confirmed, not changed) |
| 6 | Which exclusions file | DECIDED | **`research/data/exclusions_v003.json`** — the newest file on disk (v001, v002, v003; no v004 exists at this run), read by `eval.py` as `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, with **no date hard-coded** in the PREREG or in `eval.py`. `catalyst_layer_regime_change.fixed_from = 2026-06-01` and `regime_label_point_in_time_from = 2026-06-09` are read from the same file, not restated as literals. If the Steward issues `exclusions_v004.json` before Q015 locks, the draft cites that file instead. | DP-22; Q013 item 5; Q011 item 11 |
| 7 | Publication predicate | DECIDED | **`qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28)**, as drafted, for every arm including the descriptive bands E and U. Dark-lane rows are never treatment rows, are counted, and stay in the B2 control pool. Q002/Q004/Q006's looser `selected_rank`-only predicate is **flagged to the Red Team for those questions' reviews, not fixed here** and not copied. | DP-28; Q013 item 6; PREREG §2 |
| 8 | Primary level, lane and clock | DECIDED | **L3 = `lane_plans.swing_trading.targets[0]`, first touch within 20 sessions from `C_t`** — the level and lane H-060 names, on DP-09's clock. The platform's 40-session swing window is the descriptive companion, matured nights only. **Every floor, every maturity calculation and every date in §5 is computed on the 20-session window.** | DP-09; DP-42 (the level the hypothesis names; swing lane); Q007 §5; Q011 §2; Q013 item 8 |
| 9 | Same-session ordering of the L3 touch and the counter touch | DECIDED | **DP-27 governs: an unorderable same-session pair counts counter-first**, i.e. it does **not** score UPDOWN — here the reading less favourable to the hypothesis. Applied identically in band A, band B and B2 (controls have no hourly bars at all, so the asymmetry is structural, disclosed, not patched). The count resolved by this rule is printed per band and the opposite reading is printed as a named sensitivity that **never decides**. | DP-27; Q008 item 14; Q013 item 15; Q011 item 3 |
| 10 | P1's form: unconditional joint event vs the conditional "gave it back given it touched" | DECIDED | **P1 stays the unconditional joint event over every eligible pick** (touched L3, then revisited `S`, inside 20 sessions). The conditional form conditions the denominator on a **post-entry path event** — survivor-biased and outside rule 14's discipline for anything that decides — so it is computed, printed with its own CI and labelled *"conditions on a post-entry path event; descriptive, does not decide"*. The decomposition `P1 = P(touch L3) × P(revisit S | touched)` and the bare L3-touch rate per band are **mandatory** beside every P1 figure, and §8's binding paragraph on what a confirmed P1 may be said to mean stands verbatim. | rule 14; rule 6; DP-45; BACKLOG H-056's own "pre-register an unconditional version"; PREREG §1, §4, §8, §10 threat 2 |
| 11 | Family, within-question correction, and the two family-correction sets | DECIDED | **Q015 stays in F7** (where BACKLOG files H-060), counted **once**, with the **F6 companion correction** for P2 and P3 — **q ≤ 0.10 required in both families**, the larger q quoted. This is the stricter reading of DP-29's genuine ambiguity (P1's subject is the path after selection, P2/P3's subject is an exit plan) and it matches how Q012 handles the mirror case. **BH across m = 3 within the question** at q ≤ 0.10. Correction sets, computed at the decision pass on the questions locked by then: **F7** = Q002 (3) + Q004 (2) + Q011 (4) + **Q015 (3)** + **Q012's 3 F7-companion primaries** = 15 if Q012 locks; **F6 companion for P2/P3** = Q009 (2) + Q012 (3) + **these 2** = 7 (Q010 is the same hypothesis's prospective replication and is **not** a second F6 question). Companion-corrected primaries count in **both** directions — that is the arithmetic Q012 already commits to and it is the stricter one. | DP-29; rule 8; Q012 §7 (mirror case, locked-cycle draft); Q009 re-filing precedent; Q013 item 10 |
| 12 | The Q012 overlap clause — may a Q015 primary be dropped later? | DECIDED | **No. `m = 3` is fixed at lock.** Q012 and Q015 were drafted in the same autonomous cycle and **no endpoint is identical** (different level — L1/L2 vs L3; different clock — 5-session cap vs 20 sessions; different alternative — committed scale-out vs hold-to-t+20), so the draft's conditional "that primary is dropped here rather than run twice" is **discharged at lock** and must not survive as a live clause: dropping a primary after lock would lower the BH bar for the survivors, which no rule permits. The overlap is handled exactly as §7 drafts it otherwise — cross-referenced, **never presented or counted as two confirmations** of "exit lower-conviction picks earlier". | rule 8; DP-43 (no arm or endpoint demoted after lock); Q009 precedent (an endpoint short of floor still has its p computed, so m never falls); PREREG §7 |
| 13 | Knowledge time — is a rule-14 exception needed? | DECIDED | **None is requested and none is granted; DP-05 is untouched** (DP-41 respected). Band, direction, L3, `S`, ATR, both plans, both strata and the B2 matching inputs are fully specified at 16:05 ET on the pick night; every eligible pick is in its band's denominator from the close; **no post-entry quantity classifies, filters, matches or stratifies any pick**. DP-05(b)'s later classification clock is Q008's and **does not travel**. `eval.py` must write the frozen per-pick table (eligibility, band, `X`, `L3`, `S`, `ATR`, direction, every stratum label, the matched control set) **before any session-t+1 or later bar is loaded**, and **fail loudly** if a t+1-or-later field is referenced in eligibility, band assignment, matching or stratification. `sas_selection_excursion` / `outcome_*` / `level_hit_*` are never inputs; `uoa_symbol_daily.fwd_return_*` is banned (FREEZE_v001 §5, PI-001); the regime label is used only for nights ≥ 2026-06-09, `regime_version = 'v1.2'`, same-evening writes only. | rule 14; DP-41; DP-05 (scope); PREREG §6 table; Q013 item 11 |
| 14 | Successor freezes, symbol scope, and what blocks the lock | DECIDED | **Lock pinned to `manifest_v001` / `manifest_prices_v001`;** successor selection and price freezes are built and pinned **at the decision date** (routed R2), symbol scope = **every candidate on every new night, published and unpublished** (B2 needs the unpublished symbols' closes, prior bars for beta60 / atr_pct / runup20, and forward bars) **plus hourly bars for published symbols** (ordering rule 1), carrying **20** forward sessions beyond the last included pick night (**40** where the descriptive companion is computed). A second pair is built **only if** the DP-13 extension fires. `eval.py` takes window start, window end, manifest paths, exclusions path and output directory as **inputs — no hard-coded dates, manifest names or paths** — so one byte-identical script serves both runs, records every sha256 and prints pre-lock and post-lock night counts separately. **R2 does not block the lock; R1 does** (item 4). | DP-23; DP-46; Q006 §5; Q011 item 14; Q013 item 12 |
| 15 | Demotion at lock, and what happens to a thin cell at the decision pass | DECIDED | **Bands E (90+) and U (<80) are descriptive from lock** — measured, not guessed, and settled before any outcome is seen (item 1) — printed with their counts where they clear **20 contributing nights** and **SUPPRESSED** below it. **No arm is demoted after lock, in either direction.** A thin cell at the decision pass is handled where it belongs: as a SUPPRESSED sub-cell (§8 clause 1), **never** by moving a primary to descriptive and never by promoting a descriptive arm that R1 happens to measure above 20. Bands A and B are jointly the P1/P2 unit (a night needs ≥ 1 eligible pick in each), so a thin band A shows up as *fewer contributing nights* and is handled by item 4's date machinery — it is not a demotable arm. | DP-43 (demotion decided at lock); DP-21; Q013 item 16; PREREG §2 contributing-night definition, §5 |
| 16 | Floors, SUPPRESSION, and the INCONCLUSIVE boundary | DECIDED | **≥ 80 contributing nights per primary endpoint on its own definition** (DP-21's stricter reading; the "80 eligible with ≥ 20 contributing" reading is not used) **and ≥ 30 contributing nights dated after the lock commit** (DP-24), **and ≥ 20 contributing nights for any sub-cell that is reported**. A sub-cell below 20 is **SUPPRESSED** — counts only, no point estimate, not even "small n, directionally" — and does **not by itself** make its endpoint INCONCLUSIVE; the rule-7 protection lives in §8 clauses 5–7 (both halves same sign; no ≥ 20-night tape stratum beyond MPE in the opposite sign; the control-adjusted clause). **A gate shortfall is not INCONCLUSIVE either** — it fires the single DP-13 extension, then DEFERRED. **No floor is ever lowered to hit a date.** | DP-21; DP-24; DP-13; Q007 §8 clause 1; Q011 correction 2; Q013 item 3 |
| 17 | Scope of the B2 control-adjusted clause (§8 clause 7) | DECIDED | **Clause 7 binds P1 and P2 only, as drafted, and it is mandatory for those two.** P1 and P2 are **band contrasts**, and the distance confound (§10 threat 1: ladder prices and stops are LLM-written with no ATR scaling) can manufacture a band difference; the control-adjusted version strips both distances, so a control-adjusted result beyond MPE in the **opposite** sign makes the endpoint INCONCLUSIVE. P3 is a **within-pick two-plan difference in band A** with no band contrast to confound, and the opposite-sign clause does not transfer with a sensible meaning; its control version is printed as a descriptive panel and **never decides**. The −1.0 ATR counter-level version (distance-matched by construction) is printed beside all three. | rule 5 (distance-matched control); PREREG §3 B2, §8 clause 7, §10 threats 1 and 14; one defensible technical answer |
| 18 | Band assignment and score integrity | DECIDED | **Half-open intervals on the published `overall_score`, no rounding: A = [85, 90), B = [80, 85), E = [90, ∞), U = (−∞, 80)** — H-060's own cut, not re-united (DP-25); "elite" = `overall_score ≥ 90` as DP-42 defines it, and band E is exactly that set. Sub-bands **85–88 / 88–90** are the platform's own (`scripts/generate_sas_trading_guide.py:78-84`), printed where they clear 20 contributing nights. `eval.py` **re-derives** each pick's band from `score_details_json` where the layer subscores are present and **fails loudly** on a disagreement with `overall_score` beyond 0.05 rather than silently trusting a column that has been rewritten before (§10 threat 12). | DP-25; DP-42 ("elite" = ≥ 90); DP-26 (registrar-chosen bands stand); PREREG §2, §10 threat 12 |
| 19 | The exclusion ladder, and the ungradeable-night rule | DECIDED | **As drafted, each reason counted per band and printed in the results header, never silently dropped:** exclusions_v003 nights; DP-04 re-run nights; null lane plan / no swing lane / no `targets[0]` / no `stop`; `d_L3 ≤ 0` or `d_S ≤ 0` (an invalid plan at publication — decided at the close, before any forward bar, identically in both bands) or non-null `outcome_target_invalid`; missing forward bars in t+1..t+20 (a **measurement failure, never a classifier** — it never moves a pick between bands); < 60 daily bars ≤ t; immature nights by the **trading calendar**, never by whether a price exists (right-censoring is never graded as a non-touch). **A night is dropped if > 25% of its eligible picks are ungradeable**, and a matured night on which no row survives is a **non-contributing night, not an exclusion** — the 8 no-lane-plan rows all fall on 2026-06-02, which is therefore non-contributing. | DP-04; DP-22; DP-26 (registrar-chosen thresholds stand, not derived from sealed outcomes); rule 5; PREREG §2, §10 threat 10 |
| 20 | Execution plans, secondaries and what may never decide | DECIDED | **Plan T and Plan H both enter at `X` and neither uses a stop** (rule 5, DP-02) — the counter level is a measured line only. The **committed scale-out** (`BAND_EXITS`, 85–88 / 88–90 / 80–85) is run from `X` and reported beside Plan T and Plan H, truncated at t+20 and labelled, because rule 5 requires the named execution plan's realized result. **Descriptive, raw p only, never decides:** the conditional revisit factor, the next-open basis, the −1 ATR counter level, the 40-session companion, B2 and the control-adjusted versions (except clause 7's use), the band-matched sensitivity, sub-cells, MFE/MAE, **sessions-to-touch (no MPE — DP-44; Q002 owns speed)** and close-to-close return at T+5/T+20 (**secondary and descriptive by rule 5**). | rule 5; DP-02; DP-44 (sessions-to-touch descriptive); PREREG §4, §7 |
| 21 | Quotability | DECIDED | **Every number in this question is `NON_QUOTABLE`** (20- and 40-session bases; rule 12), including anything a CONFIRMED verdict produces, until it is restated on a W60 basis. Nothing subscriber-facing follows before PROSPECTIVELY_CONFIRMED (rule 10), and the demoted 90+/<80 cells license nothing at any stage (§9). | rule 12; rule 10; PREREG §4, §9 |

## Corrections to silent choices

Applied by the Registrar with the rest (`@registrar apply Q015`). **R1 has returned; every bullet
below is now concrete and nothing waits.**

- **§7 F7 roster — the hypothesis count is stale.** "F7 holds H-053…H-060, H-065, H-066 (10
  hypotheses)" reads **9**: **H-066 was re-filed to F6** under DP-29 with Q012 (BACKLOG F7 entry;
  Q012 §-header: "F7 therefore holds 9 hypotheses and H-066 is **not** counted in both"). Note in the
  same bullet that **H-053 is merged into Q006** and **H-055 is DEFERRED**, so neither contributes a
  primary to F7's correction. (DP-29; item 11.)
- **§7 family-correction sets — state both, with the companion primaries counted in both
  directions.** F7's set at the decision pass = Q002 (3) + Q004 (2) + Q011 (4) + Q015 (3) **+ Q012's
  3 F7-companion primaries where Q012 has locked** = 15; the F6 companion set for P2/P3 = Q009 (2) +
  Q012 (3) + Q015's 2 = 7, with **Q010 excluded as the same hypothesis's prospective replication**.
  The draft's "12 primaries in the family correction" is the pre-Q012 number. The larger q is the one
  quoted, and CONFIRMED needs q ≤ 0.10 in both. (rule 8; DP-29; item 11.)
- **§7 Q012 overlap bullet — delete the live conditional.** "If Q012 locks first with an endpoint
  identical to a Q015 primary, that primary is dropped here rather than run twice (it is not, as
  drafted)" is replaced by: *no endpoint is identical (L1/L2 with a 5-session cap against the
  committed scale-out, versus L3 within 20 sessions against hold-to-t+20), so `m = 3` is fixed at
  lock and no primary is dropped afterwards; the two questions are adjacent readings of one idea and
  are never counted as two confirmations.* (item 12; rule 8.)
- **Header line and §5 exposure paragraph — print R1's measured counts (they now exist).**
  "**Measured exposure:** none yet for this population" and the §5 "Projection until R1 returns"
  paragraph are replaced by `research/reports/STEWARD_Q015_exposure.md`'s measured numbers, cited to
  that file: **48 matured pick nights 2026-06-01..2026-08-12; 383 published picks → 303 eligible**
  after the §2 funnel (8 no swing lane — all on 2026-06-02; 4 `outcome_target_invalid`; 2 wrong-side
  L3; **66 wrong-side stop**, the binding exclusion in every band; 0 null-L3, 0 null-stop, 0 missing
  `C_t`, 0 ungradeable); **band A 38 picks / 21 nights, band B 249 / 47, band E 15 / 14, band U 1 / 1**;
  **P1/P2 paired nights = 21 and P3 band-A nights = 21 — the identical set**, because `nights_A ⊂
  nights_B` in this window (26 nights carry band B only; 2026-06-02 carries no eligible pick in any
  band and is **non-contributing, not an exclusion**); sub-bands **85–88 = 26 picks / 18 nights** and
  **88–90 = 12 / 9**; measured rate **21/51 = 0.4118 paired nights per session, declining month over
  month** (June 0.476, July 0.409, partial August 0.250). Also print, in §4/§10 where each belongs:
  **hourly-bar coverage on t+1..t+20 is 100.0%** for all 303 eligible picks in every band and month
  (no DP-27 fallback is forced on the picks side by a missing bar), while **206 of 428 unpublished
  candidate symbols (48.1%) have no hourly bars anywhere in the freeze**, so a B2 control drawn from
  them falls to DP-27's counter-first reading **by construction, not by a thin sample** — the §10
  threat-14 asymmetry is now a measured number, disclosed, not patched (item 9); and the **B2 pool is
  never thin** — median 54, p10 42, minimum 37 rows on any contributing night, **0.0%** of eligible
  picks in any band with < 3 or < 10 valid same-night controls. The weekly 2026-09-12 band counts and
  the `STEWARD_Q011_exposure.md` rate stay in the file **only** with their existing label — a
  mechanical projection that **gates nothing** — and the EXPLORE_001 April–May figures stay labelled
  in-sample, outside the window, **not a projection**. (DP-43; item 4; R1.)
- **§5 dates — replace the drafted floor dates with the settled ones; they moved out, not in.**
  The window end **2026-12-04**, decision date **Monday 2027-01-18** and extension decision date
  **Monday 2027-03-01** were a floor; R1's measured rate pushes all three **out**. §5 now reads:
  **primary window = pick nights 2026-06-01..2027-07-20** inclusive, after exclusions; **decision date
  Monday 2027-08-30**; **one automatic DP-13 extension** to pick nights **2026-06-01..2027-08-31**
  (+30 sessions) with decision date **Monday 2027-10-11**; **then DEFERRED**, no second extension, no
  reduced floor. The arithmetic, printed in §5 so it can be checked: 59 more contributing nights are
  needed beyond the 21 measured; at the **slowest measured rate, 0.2500/session** (partial August),
  that is 236 sessions → the 80th contributing night lands **2027-07-20**; + **20** sessions maturity
  (DP-09) = 2027-08-17 on the trading calendar (2027-08-18 on the Steward's mechanical 365/252
  conversion — the two agree to one session and to the same Monday); + one-week freeze margin =
  2027-08-24; first Monday on or after = **2027-08-30**. Extension: 2027-07-20 + 30 sessions =
  **2027-08-31**; + 20 sessions = **2027-09-29** (2027-09-06 Labor Day closed); + one week =
  2027-10-06; first Monday on or after = **2027-10-11**. Keep DP-43's **12-month ceiling** in the text
  and record that it is **cleared**: 2027-08-30 is 14 days inside 2027-09-13, so Q015 is locked and
  the conditional DEFERRED branch does not fire. State plainly that **the extension decision date
  (2027-10-11) falls after the ceiling date** — DP-43's ceiling tests the **initial** decision date,
  and DP-13's single extension is agreed at lock, so it stands; if a gate is still short there the
  answer is **DEFERRED**, never an under-powered run. Keep "gates fire on `eval.py`'s measured counts,
  never on a projection or a run-rate" and "no interim looks". (DP-43; DP-13; DP-45; item 4.)
- **§5 — say which rate was used and why.** The three rates R1 measured project the binding Floor-1
  decision date at **2027-04-19** (flat 0.4118), **2027-05-10** (Jul+Aug 0.3667) and **2027-08-30**
  (partial August 0.2500). §5 states that the desk took the **slowest** of the three because the rate
  is **measured to be declining month over month, not flat**, and because DP-43/DP-45 forbid choosing
  the rate that reaches a date sooner: the cost of the slow rate is waiting, the cost of the fast one
  is a short window, a fired extension and a DEFERRED question. The window is never shortened to reach
  a date. (DP-43; DP-45; item 4.)
- **§5 — Floor 3 is not binding and is met with margin.** At the same 0.2500/session rate, 30
  contributing nights dated after the lock commit are reached by **2027-04-12** (Floor-3 projection),
  about 4½ months before the decision date, and Floor 1 is later than Floor 3 under all three rates.
  §5 says so, and adds that both gates are nevertheless evaluated on `eval.py`'s **measured** counts at
  the decision pass, never on this projection. (DP-21; DP-24; item 16.)
- **§5 DP-31 sentence — restate against measured numbers (now discharged).** "PROSPECTIVELY_CONFIRMED
  stays reachable from this run (DP-24 met with margin; DP-31 does not apply)" was an assertion without
  an exposure count; it now carries one. The 21 measured contributing nights are **pre-lock**
  (2026-06-01..2026-08-12, lock 2026-09-13); DP-24's **30 post-lock** contributing nights are counted
  from nights after the lock commit and are projected clear at **2027-04-12** at the slowest measured
  rate — about 4½ months before the decision date, and earlier than Floor 1 under all three rates, so
  Floor 1 is the binding gate and Floor 3 arrives with margin. **DP-24 is not reduced and DP-31 is
  not invoked** — H-060 is not a question about the sealed period, and the verdict is **not**
  `HISTORICAL_ONLY`; no successor replication question is needed. (DP-24; DP-31 scope; DP-43.)
- **§2 / §5 — the 2026-06-01..2026-08-12 nights are inside the window and inside the freeze; the
  window is not re-based on them.** R1 measured them to fix a rate, not to seed a result: they enter
  `eval.py` on the same footing as every later night, and the pre-lock / post-lock night counts are
  printed **separately** in the results header (item 14) so DP-24's clause can be checked rather than
  asserted. (DP-24; item 14; rule 3.)
- **§3 / §8 — the demotions are now settled on measured counts, at lock, and are final.** Band **E
  (90+)** at **14 contributing nights** and band **U (<80)** at **1** are below the 20-night floor:
  **descriptive from lock and SUPPRESSED — counts only, no point estimate, not "small n,
  directionally"** (items 1, 15, 16). **No arm is demoted or promoted after lock in either
  direction**, whatever the decision-pass counts turn out to be. Bands **A and B are jointly the
  contributing-night unit** and neither is separately demotable — band A's thinness (21 paired nights
  in 51 sessions) is precisely what pushed the decision date from 2027-01-18 to 2027-08-30, which is
  the date machinery doing its job (item 15). The **85–88 (18 nights) and 88–90 (9 nights)** splits are
  **sub-cells, not arms**: they are governed by item 16 at the decision pass (< 20 contributing nights
  ⇒ SUPPRESSED), and at the registered window's slowest rate both project comfortably above 20, so
  nothing about them changes at lock. (DP-21; DP-43; items 1, 15, 16.)
- **§11 "Open decisions before lock" — delete the section entirely** once the above are applied;
  nothing may read as open at lock. After applying, `grep` the file for `open decision`,
  `Recommendation:`, `Options:`, `routed as R1`, `none yet` and `12 primaries` — every hit must be
  gone or deliberate.
- **Status line and `state.json` — bookkeeping.** The Status line drops "DRAFT … three items are open
  … settled by `@decision-maker decide Q015`" and records the lock; the controller advances Q015 to
  `PREREG_LOCKED --by desk` and writes `schedule.json` from `## Schedule` in the same step (DP-46).
  The Decision-maker edits neither file.

**Conflicts with already-locked questions (for the Red Team; the locked files stand, nothing is
edited):** none new. Two standing ones are repeated only so Q015's arithmetic is read with them in
view — (a) Q006/Q007 include pick night **2026-06-26**, which `exclusions_v003.json` now excludes
(already flagged in Q009's, Q011's and Q013's DECISIONS.md; Q015 uses v003); (b) Q004 §2's looser
publication predicate (`selected_rank` only) versus DP-28, which Q015 follows. **Not a conflict:**
Q007 §5 keeps its locked rolling exposure-driven decision rule while Q015 takes DP-43's fixed form —
DP-43 is dated after Q007's lock and governs new questions only; Q007 is not edited.

## Defaulted on Haci's behalf

- #1 H-060's missing baselines — chose the adjacent traded band **80–85** as the primary comparator,
  with 90+ and <80 descriptive at lock and SUPPRESSED below 20 nights; not taken: DEFER H-060 until
  elite exposure recovers — DP-43. Overturn = successor question.
- #4 window, decision date and extension — chose, on the Steward's measured numbers, the **slowest**
  of the three rates (0.2500 paired nights/session, partial August): window pick nights
  **2026-06-01..2027-07-20**, decision date **Monday 2027-08-30**, one automatic +30-session extension
  to **Monday 2027-10-11**, then DEFERRED; not taken: the flat-rate date **2027-04-19** (a shorter
  window, four months sooner) — DP-43, DP-45. Overturn = successor question.

## Routed requests

### data-steward

**R1 — RETURNED 2026-09-13, `research/reports/STEWARD_Q015_exposure.md`. No longer blocking; nothing
further is asked of the Steward for the lock.** All nine parts were answered on frozen data
(`manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`), counts only, protocol
observed. What it settled: (a) the ceiling test — **cleared under all three measured rates**, so Q015
locks rather than deferring; (b) the §5 schedule — see `## Schedule`; (c) bands E and U —
**SUPPRESSED** at 14 and 1 contributing nights. Two cross-question consistency checks came with it
(the 383/48/2026-08-12 matured base and the 303 eligible count both reproduce Q009's and Q011's
figures on a different filter order). The request is kept below verbatim for the record.

**R1 (as sent) — BLOCKING for the lock. Counts only, no outcome of any kind.** Paste-ready:

**R1 — band-composition exposure count for Q015 (up-then-down in the 85–90 band, H-060). Blocking:
Q015 cannot lock without it.** On the frozen data only (`research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json`), pick nights **2026-06-01** through the last night with a
matured **20**-session forward window, non-excluded per `research/data/exclusions_v003.json`
(`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪
`uncorroborated_publication_runs.trading_dates`), published picks under the DP-28 predicate
(`qualified IS TRUE AND selected_rank IS NOT NULL`), each carrying a
`public_payload_json.lane_plans.swing_trading` plan with `targets[0]` (L3) **and** `stop` (S), please
return: **(1)** the §2 funnel in order (published rows → no lane plan / no swing lane / no
`targets[0]` / no `stop` → non-null `outcome_target_invalid` → wrong-side L3 (`dir × (L3 − C_t) ≤ 0`)
→ wrong-side stop (`dir × (C_t − S) ≤ 0`) → missing `C_t` or < 60 daily bars ≤ t → immature < 20
forward sessions → **eligible picks**), each step counted **by band**; **(2)** eligible picks and
contributing nights **by band A = [85, 90), B = [80, 85), E = [90, ∞), U = (−∞, 80)** on the published
`overall_score`, half-open, no rounding; **(3)** **paired nights carrying ≥ 1 eligible pick in band A
and ≥ 1 in band B** (the P1/P2 contributing-night definition) and, separately, **nights carrying ≥ 1
eligible band-A pick** (the P3 definition); **(4)** nights carrying ≥ 1 eligible band-E pick, and the
same for band U; **(5)** the **85–88 and 88–90** splits of band A (eligible picks and nights); **(6)**
the null-ladder, null-stop, wrong-side-L3 and wrong-side-stop counts by band, already inside (1) but
please also give them as a standalone table; **(7)** **hourly-bar coverage** (`prices_hourly_raw`) on
sessions t+1..t+20 for the published pick symbols — share of symbol-sessions with at least one bar,
by month and by band — and the same for the unpublished B2 pool if any hourly bars exist for it;
**(8)** the **B2 control-set size distribution** (10 nearest same-night non-published
`sas_candidates` rows on beta60 / atr_pct / runup20 from `prices_daily_split` bars ≤ t) and the share
of eligible picks with **< 3 valid controls**, by band; **(9)** **contributing nights per month and
the paired-night rate per session**, for both the P1/P2 and the P3 definitions, so the seasonal
clustering is visible rather than averaged away. **Protocol (binding): counts only.** For sessions
t+1..t+20 only the **existence** of bars may be checked (maturity and coverage), never their values;
`C_t` and bars dated ≤ t may be read for eligibility, distances and matching. **No touch of any level,
no UPDOWN, no revisit, no return, no plan result, no band difference and no outcome of any kind may
be computed or reported** — the same discipline as `STEWARD_Q011_exposure.md` and
`STEWARD_Q009_exposure.md` §R1. Definitions: `C_t` = the actual pick-night regular-session close from
`prices_daily_split` (never `spot_close`); ATR14 from `prices_daily_split` bars ≤ t (never the
platform's `atr_pct`, PI-003); `dir` = +1 bullish / −1 bearish from `dominant_direction`; `L3` =
`lane_plans.swing_trading.targets[0]`; `S` = `lane_plans.swing_trading.stop`. **What it decides.**
(a) **Whether Q015 locks at all:** if the measured paired-night rate cannot project **80 paired
contributing nights (P1/P2) and 80 band-A nights (P3), each with ≥ 30 dated after the lock commit**,
by **2027-09-13**, Q015 goes to `research/questions/DEFERRED.md` with that date and the measured rate
named (DP-43's 12-month ceiling, the H-062 precedent) instead of being locked. (b) **The whole §5
schedule** (DECISIONS.md item 4): the measured rate fixes the window end, the decision date (first
Monday on or after window end + 20 sessions + one week, **never earlier than Monday 2027-01-18**) and
the single DP-13 extension (+30 sessions, floor Monday 2027-03-01) — R1 may push these dates **out**,
never **in**. (c) **Whether the descriptive band-E and band-U cells are printed or SUPPRESSED** at the
decision pass (< 20 contributing nights ⇒ SUPPRESSED, counts only); it does **not** change their
demotion, which is settled at lock either way (DECISIONS.md item 15).

**R2 — OPEN, not a blocker for lock. Due at the decision date now fixed: Monday 2027-08-30 (a second
pair only if the DP-13 extension fires, for the decision pass of Monday 2027-10-11). The successor
freezes must cover pick nights after 2026-09-10 through the registered window end 2027-07-20 —
2027-08-31 if the extension fires.** Paste-ready:

**R2 — successor freezes for Q015 (DP-23).** Build and pin the successor selection freeze (same SQL,
same exclusion criterion as v001) and the successor price freeze (same Alpaca queries) covering pick
nights after **2026-09-10** through Q015's registered window end **2027-07-20** (**2027-08-31** if the
DP-13 extension fires), with the daily symbol list extended
to **every candidate on every new night, published and unpublished** — B2 needs the unpublished
symbols' pick-night closes, prior bars for beta60 / atr_pct / runup20, and forward bars — **plus
hourly bars for published symbols** (the §4 same-session ordering of the L3 touch against the counter
touch), carrying **20** forward sessions beyond the last included pick night (**40** where the
descriptive 40-session companion is to be computed), and please fix the exact session-count decision
date from the trading calendar at the same time. Nights whose unpublished-candidate bars are missing
lose their controls, are excluded from the primaries and are **counted, never back-filled**; pairs
that hourly bars cannot order fall to DP-27 (counter-first) and are counted.

### registrar (conditional) — STOOD DOWN, did not fire

The conditional DEFERRED branch ("if R1's measured rate cannot project 80 contributing nights per
primary endpoint with 30 post-lock by 2027-09-13, write the `research/questions/DEFERRED.md` entry for
H-060 instead of locking") **does not fire**: the slowest measured rate projects the binding Floor-1
decision date at **2027-08-30**, inside the **2027-09-13** ceiling by 14 days. **No `DEFERRED.md`
entry is written for H-060.** The registrar's remaining job is `@registrar apply Q015` — fold the
table and the corrections into `PREREG.md`, then lock `PREREG_LOCKED --by desk` and write
`schedule.json` from `## Schedule` below (DP-46).

**One thing for the record, not a conditional:** the margin under the rate the desk chose is **two
weeks**, and the underlying rate is measured to be **declining**. That is not a reason to pick a
faster rate (DP-45) and it changes no gate — gates fire on `eval.py`'s measured counts. If the
extension fires on 2027-10-11 and a gate is still short, the answer is **DEFERRED**, and the
`DEFERRED.md` entry is written then, on measured counts rather than on a projection.

## Schedule

**Filled at `record` (2026-09-13) from `research/reports/STEWARD_Q015_exposure.md` by DP-43's recipe,
on the slowest of the three measured rates.** Written verbatim to
`research/questions/Q015_band_85_90_updown/schedule.json` by the Registrar at `apply` / lock (DP-46).

decision_date: **2027-08-30** (Monday) · extension_date: **2027-10-11** (Monday) · hard_stop: **none**
(DP-13's single automatic extension, then DEFERRED, replaces it) · rule: **fixed** · window: pick
nights **2026-06-01..2027-07-20** (after `exclusions_v003.json`; in-window that removes 2026-06-26,
2026-07-02, 2026-07-06) · extended: **false** · gates: per primary endpoint, **≥ 80 contributing
nights** (DP-21 — P1/P2 on the paired A-and-B night, P3 on the band-A night) **and ≥ 30 contributing
nights dated after the lock commit** (DP-24), both on `eval.py`'s measured counts at the decision
pass · ceiling: **cleared** (2027-08-30 ≤ 2027-09-13, 14 days).

- **Rate used: 0.2500 paired-contributing nights per session** — the partial-August rate, the
  **slowest** of the three R1 measured (flat overall 0.4118, Jul+Aug 0.3667, Aug partial 0.2500).
  Chosen because the rate is measured to be **declining month over month, not flat** (June 0.476, July
  0.409, August 0.250), and because DP-43/DP-45 forbid the rate that reaches a date sooner. The flat
  rate would have set 2027-04-19 and the Jul+Aug rate 2027-05-10; both were rejected as the shorter
  window.
- **decision_date arithmetic:** 59 contributing nights are still needed beyond the 21 measured
  (2026-06-01..2026-08-12); 59 / 0.2500 = **236 sessions** → the 80th contributing night projects to
  **2027-07-20**, the window end; + **20** sessions maturity (DP-09) = 2027-08-17 on the trading
  calendar (2027-08-18 on the Steward's 365/252 mechanical conversion — same Monday either way); + one
  week freeze margin = 2027-08-24; **first Monday on or after = 2027-08-30**. This is **11.5 months
  from the 2026-09-13 lock** — out from the drafted floor of Monday 2027-01-18 by 7½ months, and
  **never pulled in** (DP-43, DP-45; Q011 item 8).
- **extension_date arithmetic (DP-13, fires automatically on `eval.py`'s measured counts only, with
  the byte-identical `eval.py`):** window +30 sessions → pick nights **2026-06-01..2027-08-31**;
  2027-08-31 + 20 sessions = **2027-09-29** (2027-09-06 Labor Day closed); + one week = 2027-10-06;
  **first Monday on or after = 2027-10-11**. It falls **after** the 12-month ceiling date —
  DP-43's ceiling tests the **initial** decision date, and the single extension is agreed at lock, so
  it stands; a gate still short there means **DEFERRED**, never an under-powered run and never
  INCONCLUSIVE.
- **Floor 3 is not binding:** 30 post-lock contributing nights project clear at **2027-04-12** at the
  same rate, about 4½ months before the decision date; Floor 1 (80 total) is later under all three
  rates. **Not HISTORICAL_ONLY** — PROSPECTIVELY_CONFIRMED is reachable from this run by design and
  DP-31 does not apply, so no successor replication question is drafted.
- **Demotions, settled at lock and final:** band **E (90+)** at 14 contributing nights and band **U
  (<80)** at 1 are **descriptive and SUPPRESSED** (items 1, 15, 16). No arm is demoted or promoted
  after lock. Bands A and B are jointly the contributing-night unit and are not separately demotable;
  the 85–88 / 88–90 splits are sub-cells under item 16, not arms.
- **note:** _PREREG §5 / DP-43 / DP-13 / DP-21 / DP-24 / DP-45. Every gate is evaluated on `eval.py`'s
  measured counts from the frozen data at the decision pass, never on R1, this projection or a
  run-rate. `eval.py` runs **once**; no interim looks. Routed **R2** (successor freezes through
  2027-07-20, all candidate symbols published and unpublished plus hourly bars for published symbols,
  20 forward sessions — 40 for the descriptive companion) is due at `decision_date`; a second pair only
  if the extension fires. **R1 is returned and closed.**_

## Standing rules added

_none._ Every item here is settled by an existing `DP` entry, a locked precedent or one defensible
technical answer, and both DEFAULTED items are applications of DP-43. **No `DP` entry is created from
a DEFAULTED item** — a default is the desk acting on Haci's behalf, not an answer from him (DP-40);
only an answer of his becomes a Confirmed row. **The `record` step adds none either:** the schedule is
arithmetic on DP-43's recipe, not a new rule. `research/DECISION_POLICY.md` was not edited.

## Standing rules proposed

Written down because they would generalise, **not added** to `research/DECISION_POLICY.md`. Each needs
Haci's word (or a later `--ask` cycle) before it becomes a `DP` row.

- **P-5 (would extend DP-43): when a hypothesis names a baseline that is closed by platform
  configuration or unreachable inside the 12-month ceiling, the desk registers the nearest **stricter**
  available contrast rather than deferring the whole hypothesis**, demotes the named baselines to
  descriptive at lock, and records the properly powered version as a separate future question with an
  exposure trigger. Rationale: Q015 item 1; without it, every hypothesis written against the pre-July
  publication floor dies rather than being tested one band over.
- **P-6 (would extend DP-29): a question whose primaries split across two families is filed where the
  BACKLOG files it and carries a companion correction in the other family, with q ≤ 0.10 required in
  both and the companion primaries counted in both directions.** Rationale: Q015 item 11 and Q012's
  mirror case; the two questions currently reach the same place by two different routes.
- **P-7 (would sharpen DP-43, added at `record`): when the Steward measures a contributing-night rate
  that is declining month over month, the projection uses the most recent (slowest) measured rate, not
  the flat average over the exposure window.** DP-43 says "the measured run-rate" without saying which
  one when there are three; a flat average is an average over a tape that has already changed.
  Rationale: Q015 `record` — the flat rate would have set the decision date at 2027-04-19 and the
  slowest measured rate set it at 2027-08-30, a four-month difference on the same data; taking the
  faster one risks a short window, a fired extension and a DEFERRED question, and DP-45 already
  forbids picking the sooner date. Cost, stated plainly: the slow rate over-waits if the tape
  recovers, and the question then runs with more nights than its floor needs — the error the desk
  should prefer.
