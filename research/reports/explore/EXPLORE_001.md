# EXPLORE_001 — Path, entry timing and volatility, seen the way Haci trades SAS

**Requested by:** Haci · **Agent:** Explorer · **Date:** 2026-09-10
**Data:** manifest_v001 (in-sample split only, trading_date ≤ 2026-05-29) + manifest_prices_v001
(forward paths of in-sample rows only, ≤ 60 sessions). No sealed-period pick was loaded.
**Platform SHA:** fa70688bc252d14f8d67e371afafc194731c324e
**Scripts:** `research/reports/explore/scripts/` (run `run_all.sh` from the desk root; logs land in
`research/reports/explore/work/logs/`).

> Every number below is **in-sample, exploratory — not a finding.** April–May 2026 was a strong,
> mostly one-way tape. The sample is 41 nights, and the analysis sample is 35. Treat every
> pattern as possibly specific to that tape. No p-values are reported, by design.

---

## Decision paragraph for Haci

The six targets are mostly a ruler, not a forecast. L1 and L2 sit a median 0.3 and 0.55 ATR from
the pick-night close, inside one normal day's range, so random same-night stocks touch targets at
the same distance almost as often. SAS's real edge in-sample was **modest (about 5 points of
touch rate), concentrated in the deep targets (L4–L6) and in speed**: picks reach L3/L4 in
noticeably fewer sessions than a matched control (median 3 vs 5 at L3, 7 vs 11 at L4). For your style, five ideas are worth
registering:

1. **Close a spread leg when the stock first touches the short strike; don't hold to expiry.** L3
   was touched within 20 sessions for about 3 in 4 picks, but about 4 in 10 of those were back
   below L3 by session 20.
2. **Move strike and target choice to ATR distances and stop trusting L1/L2 as evidence.** They
   are hit about as often as a random same-night stock.
3. **Skip or size down first-time picks** (not published in the prior 10 sessions). In-sample they
   did not beat the control; names on a 3+ streak did clearly. This is existing backlog H-052,
   sharpened.
4. **Judge L1/L2 on an entry you can actually get.** L1 was already passed at the next open for
   about 1 pick in 5, and by 10:00 ET for about half. Your after-hours partial fill on elite
   nights captures that overnight move. Buying the day-1 dip does not help: limit orders filled on
   the weaker picks.
5. **Pick option expiry from the target's ATR distance.** Targets within 1 ATR took a median of 1–2
   sessions to touch; 2–3 ATR, about 8; 3–5 ATR, about 17.

What was *not* supported: high-beta or volatile names were **not** more two-sided in ATR terms.
They trended further in one direction.

**Testing constraint.** The sealed period has only 71 nights, below the 80-night total floor
(rule 6). As of 2026-09-10 it has only 51 nights with a matured 20-session window, 31 with a
40-session window and 11 with a 60-session window. None of these ideas can clear the floor on the
sealed period alone today. Short-window versions (≤ 20 sessions) can clear it around late
October 2026 once prospective nights accrue.

**Data problems you should know about before anyone trusts a number:**
- 4 in-sample nights (05-11 to 05-14) were computed after one or more later sessions had
  already traded. Those picks were never actionable, and their spot prices are mixed-date.
- The platform's earnings date was wrong for every candidate in-sample.
- The platform's ATR is corrupted around stock splits.

Details are in §9.

---

## Ranked top 5

Scoring: (i) mechanism, (ii) sealed-period testability against the rule-6 floors,
(iii) money impact for Haci's style, (iv) what the platform could change.

| # | Idea (H-number) | (i) Mechanism | (ii) Sealed testability | (iii) Money impact | (iv) Platform change if it holds |
|---|---|---|---|---|---|
| 1 | Leg out at first touch of the short strike (L3) vs hold to session-20 close — **H-055** | Good: targets sit at extension/resistance levels; after a touch, price often mean-reverts | Every pick qualifies, so cells are fine. 20-session window: 51 matured sealed nights now, 80 around late Oct 2026. Needs option prices for the real P&L; the stock-path proxy is testable now | High: this is exactly how Haci runs spreads | Exit guidance in the options context ("close at first L3 touch"); re-derive the committed scale-out on this basis |
| 2 | Ladder touches are mostly distance; excess concentrated at L4–L6 — **H-053** | Strong: ladder prices are written by the principal-agent LLM with no ATR scaling (volatilx `ai_agents/principal_agent.py:530-575`; fallback 0.5%/1% steps at `:897-911`) | L1/L2 (20 sessions) testable around late Oct; L4–L6 need 40/60-session windows (31/11 matured nights now), so around Nov–Dec | Medium-high: decides which targets are worth selling strikes against | ATR-scaled ladder (e.g., L1 ≥ ~0.75 ATR); performance card shows hit rate next to the distance-matched control |
| 3 | First-time picks don't beat the control; streaks do — **H-052 (existing, sharpened)** | Good: continuation after re-qualification is a known finding | New picks are ~40% of the book, so both cells clear 20 nights | High: a simple skip/size rule | Streak flag on the card; lower default size for first-time picks |
| 4 | L1/L2 already passed at an actionable entry; after-hours vs open entry — **H-054, H-057** | Mechanical: L1 is closer than the usual overnight gap plus first-hour range | Day-1 metrics mature fast: 66 sealed nights now, 80 around 30 Sep. The elite part (H-057) fails the 20-night cell floor for a long time | Medium: stops Haci "counting" targets he could not have traded; supports the AH partial fill on elite nights | Publish hit rates on the next-open basis as well as the close basis; entry-timing note ("L1 may be gone by the open") |
| 5 | Speed: picks reach L3/L4 faster than matched controls, so pick DTE from target distance — **H-056** | Moderate: flow-led, breakout selection front-loads the move | All picks qualify; 40-session windows need until ~mid-Nov for 80 nights (a ≤ 20-session cap version: late Oct) | High for options: theta, and DTE choice | Options context maps each target's ATR distance to a DTE band instead of today's flat 21–35 DTE |

Runners-up: earnings within 0–3 sessions of the pick (H-064; strong mechanism, but the sealed
period may have few such picks now that the catalyst fix shipped), gap-against opens as a spread
skip rule (H-063), bear picks under-running their control (H-062), and prior-5-session UOA
persistence (existing H-040, which the path lens supports).

---

## Samples used

| Sample | Picks | Nights | Elite 90+ |
|---|---:|---:|---:|
| Published in-sample | 328 | 41 | 21 (17 nights, 12 symbols) |
| With a lane-plan ladder | 312 | 39 | 19 |
| **Analysis sample** (ladder, retro nights 05-11..05-14 excluded) | **280** | **35** | **15 (13 nights, 9 symbols)** |
| All candidates with price paths (control pool) | 2,282 (2,076 non-retro) | 41 (37) | — |

Elite picks are heavily repeated memory/semis names: SNDK ×4, WDC ×2, MU ×2, QCOM ×2, plus AMD,
INTC, STX, NXPI, DDOG. Treat "elite" in-sample as "the April–May semis rally".

Conventions used throughout:
- The reference price is the **actual** pick-night close, not the platform's `spot_close`. It is
  stale on 05-13/14 (§9).
- ATR is ATR14 from split-adjusted bars up to the pick night. The platform's `atr_pct` is
  corrupted around splits (§9); otherwise the two agree closely, Spearman 0.97.
- Touches are regular-session daily high/low, in the signal-date price basis, with split factors
  snapped. Ladder windows are 20/40/60 sessions per volatilx `services/sas_conviction_card.py:190`.
- "Matched control" means the 10 nearest same-night unpublished candidates on beta60, ATR% and
  prior-20-session return, graded on their own price path with a synthetic target at the same
  ATR distance and in the pick's direction.

---

## A. Skill or distance?

**What I did.** For every published ladder level, I measured its distance from the close in ATR
multiples. I graded it within its lane window and compared it with two controls: (1) all
same-night unpublished candidates, and (2) the beta/ATR/run-up-matched control above.
Scripts: `20_theme_A_distance.py`, `21_theme_A_matched.py`. n = 280 picks / 35 nights /
1,660 level rows.

**Where the ladder sits (median distance from the close).**

| | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---|---|---|---|---|---|
| ATR multiples | 0.31 | 0.55 | 0.99 | 2.59 | 3.08 | 5.67 |
| Percent | 1.4% | 2.5% | 4.5% | 11.5% | 13.9% | 26.4% |

The counter levels mirror this: day_c1 sits 0.32 ATR on the adverse side, swing_c1 0.98,
long_c1 2.52. L4 and L5 are almost the same distance.

**Hit rates against the controls** (in-sample, exploratory — not a finding):

| Level | Pick hit (own window) | All same-night control | Matched control | Pick minus matched (night-avg) | Nights where pick > matched |
|---|---:|---:|---:|---:|---:|
| L1 | 0.93 | 0.89 | 0.89 | +0.04 | 60% |
| L2 | 0.86 | 0.80 | 0.81 | +0.05 | 66% |
| L3 | 0.82 | 0.79 | 0.81 | +0.02 | 49% |
| L4 | 0.68 | 0.60 | 0.63 | +0.06 | 57% |
| L5 | 0.72 | 0.65 | 0.67 | +0.05 | 63% |
| L6 | 0.52 | 0.42 | 0.44 | +0.08 | 74% |

- **Direction.** Picks beat the controls a little at every level. The gap is widest at L6 and
  smallest at L3. Matching on beta and run-up removes about a quarter of the raw excess. Picks are
  much higher-beta (median 1.62 vs 0.97) and have already run (+15% vs +2% over 20 sessions).
- **Bear picks** (25 picks / 14 nights) were hit *less* often than same-night stocks' downside at
  the same distance. That is plausibly just the up-tape.
- **"Different stocks don't move the same amount" — Haci is right, even in ATR units.** Across
  all candidates, the chance of touching +3 ATR within 20 sessions was 0.30 for the low-beta
  tercile and 0.57 for the high-beta tercile. So ATR alone is not a sufficient ruler in a trending
  tape; beta (market drift × exposure) matters too. That is why the matched control includes beta.
- **The ladder is not ATR-consistent.** In percent terms the LLM places high-ATR names' targets
  further out, but less than proportionally. In ATR units, high-ATR picks get *closer* targets
  (L4: 2.0 ATR in the top tercile vs 3.5 in the bottom). Volatile names get easier ladders.
- **Elite** (15 picks / 13 nights): every level L1–L5 was hit except one L4. Excess over the
  matched control is +0.07 to +0.24, but n is tiny and the elite names are concentrated.
- **Caveats.** Three matching features may not capture everything the selection sees. Nights
  overlap in their forward windows. The whole sample is one tape.

## B. Entry timing, as Haci actually enters

**What I did.** I defined five entries (`30_theme_B_entry.py`, `80_extras.py`):
- **Pick-night close:** reference only, not actionable.
- **After-hours at publication:** the close of the hourly bar in which that night's SAS run
  finished. Publication time varies (§9), so this is not a fixed 21:00 UTC.
- **Next open.**
- **Next day 10:00 ET and 11:00 ET:** closes of the 13:00 and 14:00 UTC hourly bars.

n = 280 picks / 35 nights; 211 picks / 31 nights have an actionable AH price. Elite: 15 picks,
12 of them with an AH price (11 nights).

**Price drift before each entry, direction-adjusted** (in-sample, exploratory — not a finding):
- AH at publication: median 0.00 ATR. There is no drift between the close and publication.
- Next open: median +0.06 ATR. It is further in the pick's favour than the AH price 59% of the
  time, so the AH fill was usually the cheaper one.
- Open to 10:00 ET: flat (median 0.00).
- Elite picks gapped more (median +0.31 ATR vs +0.05 for the rest).

**Ladder levels already passed at the entry** (these targets are gone for that buyer):

| Entry | L1 | L2 | L3 | L4 |
|---|---:|---:|---:|---:|
| Pick-night close | 3% | 3% | 0% | 0% |
| After-hours at publication | 1% | 1% | 1% | 0% |
| Next open | 21% | 9% | 5% | 1% |
| 10:00 ET | 52% | 28% | 14% | 3% |
| 11:00 ET | 54% | 31% | 15% | 4% |

Elite at the open: L1 passed 33%, L2 20%, L3 20% (n=15).

**Did the AH partial fill hurt?** (211 picks / 31 nights)
- Day 1 traded at least 0.25 ATR below the AH price in 59% of picks (elite 4 of 12).
- The day-1 close was better than the AH price in 58% (elite 10 of 12).
- So "sometimes it hurts" is accurate for non-elite picks, and it was rarer for elite picks
  (tiny n).

**Waiting for a dip is worse.** A resting limit 0.25 ATR below the close filled on day 1 for 54%
of picks, and 0.5 ATR below filled for 35%. Once filled, the pick reached L3 before a further
−1 ATR only 54% and 51% of the time. That compares with 57% for a market entry at the open and
64% for the AH entry. On the same 211-pick subset: AH 64% vs open 59% vs limit 56%. The AH and
open entries hit the −1 ATR level first equally often (35%). The AH advantage is purely the moves
that happen overnight. **Mechanism:** limit orders fill on the picks that are going wrong.

**Day-1 gap vs path from the open** (extends existing H-030 to path metrics):
- Gap against the pick (≥0.25 ATR): 39 picks / 19 nights. L3 touched within 20 sessions of the
  open 56%, vs 74% for flat opens (152 / 34). Median 20-session drawdown from the open −1.6 ATR.
- Big gap in favour (≥0.75 ATR): 15 picks / 11 nights. L3 was already passed at the open for
  about half of them, and the drawdown after the open was deeper (median −2.2 ATR).

**Close-to-close, from each entry (secondary):** close +0.5% on T+1, open +0.2%. The overnight
gap is a large share of day-1 return. By T+20 the entries converge.

## C. Path shape, both directions

**What I did.** Order of first touches at three scales: day L1 vs day_c1 within 20 sessions,
swing L3 vs swing_c1 within 40, long L5 vs long_c1 within 60. Same-day ties are broken with
hourly bars. I also used a model-free symmetric version: ±1.5 ATR within 20 sessions and ±2 ATR
within 60. Script: `40_theme_C_shape.py`. n = 280 / 35.

| Scale (median distances) | up-only | up→down | down→up | down-only | same hour / neither |
|---|---:|---:|---:|---:|---:|
| Day (0.31 / 0.31 ATR) | 21% | 35% | 26% | 10% | 8% |
| Swing (1.01 / 0.97 ATR) | 32% | 25% | 25% | 18% | 1% |
| Long (3.09 / 2.50 ATR) | 44% | 21% | 8% | 22% | 6% |
| Symmetric ±1.5 ATR / 20 | 47% | 19% | 9% | 24% | 0% |
| Symmetric ±2 ATR / 60 | 39% | 31% | 10% | 20% | 0% |

- **Day-scale "two-sided" is automatic.** Both levels are 0.3 ATR away, so any normal day
  touches both. Use the swing scale or the symmetric ATR version to talk about real two-way
  moves.
- **By feature (swing-scale up→down share and symmetric ±2 ATR/60 two-sided share).** No 16:05
  feature separated them strongly:
  - ATR tercile: flat to U-shaped.
  - Beta tercile: mid-beta highest.
  - Score band: up→down 16% for <80 (100 picks), 26% for 80–85 (121), 39% for 85–90
    (44 / 28 nights), 33% for 90+ (15).
  - Lane: long-timeframe picks were most two-sided (18 picks).
  - GEX pin risk: 65% two-sided vs 44% without (26 picks / 16 nights). GEX context is missing for
    137 of 280 picks.
- **Drawdown before the first L1 touch:** median −0.35 ATR. 41% of picks went worse than
  −0.5 ATR, and 20% worse than −1 ATR, before L1.
- **L1 to L3:** median 1 session among picks that hit both (230 picks). 60% of picks touched L1
  on day 1 itself.
- **Recovery:** after touching swing_c1 (190 picks), 67% later reached L3 and 53% reached L5.
  With no stops, most dips came back in this tape.
- **Time-to-L1 as a predictor** (existing H-031):
  - L1 on day 1: 168 picks, L6 later hit 61%.
  - L1 in sessions 2–3: 53 picks, 58%.
  - Sessions 4–10: 28 picks, 32%.
  - After session 10: 20 picks, 10%.

  The direction supports H-031 and suggests a "no L1 by session 3, stop adding" rule. The cells
  are small.
- **Comparison with the platform table.** For the same picks, sas_excursion v2 reports
  ran_then_dipped 0.32, dipped_before_l1 0.32, recovered_to_l3 0.68 and recovered_to_l5 0.54.
  Those use calendar windows (see §9), so they are on a different basis.

## D. Volatility harvest

**What I did.** I compared realized 20/60-session range against ATR at selection, and ±ATR
two-sidedness, for all 2,076 non-retro candidates (37 nights) and for the 296 non-retro published
picks. The picks were compared per night with unpublished candidates and with the matched
control. Scripts: `50_theme_D_vol.py`, `70_seeds.py`.

- **Picks realize more range than their ATR implies.** Median 20-session range is 5.6 ATR for
  picks vs 4.7 for same-night unpublished candidates (higher on 81% of nights). Against the
  matched control the excess is +0.8 ATR (62% of nights).
- **But the extra range is one-directional.** Picks reached +1.5 ATR within 20 sessions 76% of
  the time vs 61% for non-picks. Two-sidedness barely differed: ±1.5 ATR/20 was +4 points vs the
  matched control, and ±2 ATR/60 was −2 points. Forward/backward realized-vol ratio is ≈ 0.97
  for both, so there was no vol expansion close-to-close.
- **Haci's high-beta two-sided belief: not supported in ATR units in-sample.** The high-beta pick
  tercile had the widest range (6.1 ATR). Its two-sided rate was only slightly above low-beta
  and below mid-beta (±2 ATR/60: 0.42 vs 0.32 and 0.44). Low-ATR picks
  were the *most* two-sided in ATR terms (0.54 vs 0.39 for high-ATR, n=50 vs 165). In percent
  terms volatile names obviously swing more. The sealed Jun–Aug tape is the natural test: in a
  choppy tape the answer may flip (H-059).
- **Other candidate predictors: none clean.**
  - GEX regime: nothing.
  - UOA premium tercile: widens range but not two-sidedness.
  - Earnings inside 20 sessions: confounded with April vs May; see §G.
  - Pin risk: the best lead, with tiny n (above).
  - Sector: industry is populated for only 12% of picks.

## E. Legging out spreads (stock-path proxy)

**What I did.** Long leg at the entry (next open, or 10:00 ET) and short leg at L2, L3 or L4.
I recorded the touch within N sessions, days to touch, the session-15/20/25 close relative to the
strike, and the race against a −1 ATR move or the swing counter level. Scripts:
`60_theme_E_spreads.py`, `80_extras.py`, `81_speed.py`. n = 280 / 35.

Next-open entry (in-sample, exploratory — not a finding):

| Short strike | Passed at open | Median distance | Touch ≤5 | ≤10 | ≤20 | ≤40 | Median days (p75) | Close through strike at S20 | Strike before −1 ATR |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| L2 | 9% | 0.60 ATR | 0.69 | 0.78 | 0.86 | 0.89 | 2 (6) | 0.53 | 0.68 |
| L3 | 5% | 1.05 ATR | 0.54 | 0.67 | 0.75 | 0.82 | 4 (9) | 0.47 | 0.60 |
| L4 | 1% | 2.52 ATR | 0.29 | 0.44 | 0.56 | 0.68 | 8 (20) | 0.34 | 0.46 |

- **Touch vs settle.** Of picks that touched L3 by session 20, only 62% still closed through L3
  at session 20. That gap is the case for closing a leg at the touch (H-055). The real option P&L
  needs option prices.
- **Speed vs distance** (all strikes pooled, measured from the open):

  | Strike distance | Median days to touch | p75 |
  |---|---:|---:|
  | ≤ 0.5 ATR | 1 | 3 |
  | 0.5–1 ATR | 2 | 6 |
  | 1–2 ATR | 5 | 11 |
  | 2–3 ATR | 8 | 13 |
  | 3–5 ATR | 17 | 36 |

  The platform's flat 21–35 DTE suggestion (`options_context`) is long for L2/L3 strikes and
  short for L5/L6.
- **Speed vs matched control:** L3 median 3 sessions vs 5, L4 7 vs 11, L2 2 vs 2. Touch rates
  within 40 are similar at L3 (0.82 vs 0.81). The edge shows up as *speed* (H-056).
- **A gap against at the open is the worst spread entry:** L3 touched within 20 sessions 56% vs
  74% for flat opens, and −1 ATR came first 54% of the time (39 picks / 19 nights).
- **Low-ATR picks** have their L3 further away in ATR terms (1.38), with median 6 days to touch
  and p75 of 21. High-ATR picks: L3 at 0.72 ATR, median 3 days.

## F. Elite 90+ (n = 15 picks / 13 nights in the analysis sample; 21 / 17 overall)

All numbers are in-sample, exploratory, tiny n, and dominated by memory/semis names.
- Every elite pick touched L1 by session 2, and 14 of 15 on day 1.
- L2, L3 and L5 were hit by all 15; L4 by 13; L6 by 12.
- Swing-scale shape: 10 up-only, 5 up→down, none down-first.
- Next open: gapped a median +0.31 ATR in favour. L1 was already passed for 5 of 15 and L3 for
  3 of 15.
- AH entry (12 picks): day-1 close better than the AH price for 10 of 12. Day 1 traded ≥0.25 ATR
  below it for 4 of 12.
- Limit 0.25 ATR below the close filled for only 4 of 15; 0.5 ATR below filled for 0.
- Short strike at L3: touched within 5 sessions for 14 of 15 (median 2 sessions). Still through
  L3 at session 20: 11 of 15.
- Sealed period has 25 elite picks. That is unlikely to reach 20 nights per cell, so any
  elite-only hypothesis (e.g., H-057's elite leg) is INCONCLUSIVE by construction for a while.

## G. Charter seeds on the path lens

Existing hypotheses are reported here with evidence only; nothing is duplicated in the backlog.

- **Re-qualification streak (H-052).** Picks published 0 / 1–2 / 3+ times in the prior 10
  sessions; only picks with a full 10-session history (208 picks / 25 nights).

  | Streak | Picks / nights | Pooled excess vs matched control |
  |---|---|---:|
  | New (0) | 85 / 24 | −0.03 |
  | 1–2 | 71 / 26 | +0.08 |
  | 3+ | 52 / 24 | +0.20 |

  The pattern holds with elite picks removed. At L6 the excess runs from −0.07 for new picks to
  +0.27 for 3+. This is the strongest selection pattern in the pond.
- **UOA persistence (H-040).** Strong same-direction UOA days (bucket score ≥ 70 with a
  directional label) in the prior 5 sessions: 0 days for 50 picks, 1–2 days for 140, 3+ days
  for 90. Excess vs matched control is −0.09 / +0.05 / +0.13. Non-NOISE labels alone cover about
  half the universe every day, so they are useless as a flag.
- **Earnings inside the window (seed; new H-064).** Using corrected report dates:

  | Next report | Picks / nights | L3 hit | Median 20-session drawdown from the open | Median absolute gap |
  |---|---|---:|---:|---:|
  | 0–3 sessions out | 30 / 18 | 0.70 | −2.3 ATR | 0.41 ATR |
  | 4–10 sessions out | 53 / 16 | 0.87 | −1.2 ATR | 0.21 ATR |

  `catalyst_event_score` was a flat 80 in every bin: the layer could not see the report date
  (§9).
- **GEX alignment (H-020).** Only 143 of 280 picks have GEX context. For L1/L2, excess rises with
  alignment tercile (+0.02 / +0.05 / +0.10). For L3/L4 it falls (+0.06 / +0.04 / +0.01). A mixed
  signal on thin data.
- **Near-miss 65–70 (H-002).** Own-direction net excursion at 20 sessions (favorable minus
  adverse, ATR), unpublished candidates:

  | Band | Candidates / nights | Net 20-session excursion |
  |---|---|---:|
  | 65–70 | 311 / 37 | +0.02 ATR |
  | 70–75 | 375 / 37 | +0.81 ATR |

  There is a visible step at the 70 threshold. It is confounded with the bull share (0.70 vs
  0.89) in an up-tape. Also, 75–80 *published* picks (+0.61) did no better than 75–80 capped,
  unpublished ones (+0.94). That is relevant to Q001's control cohort.
- **Sector cluster nights (H-034):** not testable from this freeze (industry 12% populated).
- **Conviction-monitor exits (H-050):** the table starts 2026-05-12, leaving 13 in-sample nights.
  Not testable in-sample.

---

## 9. Things that surprised me or look broken

1. **Retro-computed nights (knowledge-time hazard).** `sas_runs.finished_at` shows 11 of 42
   in-sample runs finished more than 3 hours after 21:00 UTC. Four nights were computed after
   later sessions had traded:

   | Pick night | Run finished |
   |---|---|
   | 05-11 | 05-16 |
   | 05-12 | 05-16 |
   | 05-13 | 05-14 20:11 UTC (after the next close) |
   | 05-14 | 05-16 |

   On 05-13/14, context `spot_close` differs from the actual close for 88 candidates (14
   published), by up to −8.7% (COIN). This contradicts FREEZE_v001 §7's "created_at clusters same
   trading_date evening". 4 elite picks sit on these nights (MRNA ×2, ALB, SMCI). I excluded them;
   the Data Steward should add an actionability flag, and the sealed period needs the same audit
   (`06_run_lateness.py`).
2. **Publication time is not 21:0x UTC in-sample.**
   - 04-01 and 04-06 finished after midnight UTC, so they were actionable only pre-market or at
     the open. 04-02, 04-24 and 05-15 finished over the weekend (actionable at the next open).
   - 04-07 to 04-30: about 23:10 UTC (19:10 ET).
   - 05-06 to 05-08: about 20:42 UTC.
   - From 05-18: about 21:0x UTC.

   An after-hours entry rule must key off `finished_at`. At 23:xx UTC, after-hours liquidity is
   thin: 37 actionable picks had no AH print after publication.
3. **Earnings blind spot.** Context `catalyst_context.next_earnings_date` is ≥ 38 calendar days
   out for **every** in-sample candidate. This is the "bogus market-wide resolver" described in
   volatilx `scripts/rescore_sas_earnings_corrected.py:1-24`, fixed in 69ef05f on 2026-06-01. In
   the corrected dates, 26 published picks were within 0–3 days of a report. The `*_corrected`
   columns are a later backfill from a file ending 2026-05-30, so late-May picks show no July
   report. The catalyst layer (10% weight) therefore changes regime at the in-sample/sealed
   boundary.
4. **Platform `atr_pct` is corrupted around splits.** BKNG shows 0.36–0.49 and CVNA 0.51–0.55
   (true ≈ 0.04–0.06), which looks like an ATR computed across the raw split cliff. Any ATR-based
   sizing or projection for those nights is wrong.
5. **16 published picks have no lane plans** (all on 04-01 and 05-01, including elite WDC 04-01
   and INTC 05-01). This is the null-ladder denominator. Another 9 analysis-sample picks (27 of
   312 ladders overall) have L1 on the wrong side of the actual pick-night close, i.e. "hit" at
   publication.
6. **`sas_excursion` is on a different basis.** It uses calendar windows (60 calendar days),
   narrower than the 20/40/60-session ladder (volatilx `services/sas_excursion.py:8-18`, which
   flags this itself). Its hit dates must not be joined to the ladder as equivalent. The v1/v2
   dedupe is confirmed: in-sample has 328 v1 + 328 v2 rows, and v2 is unique per (date, symbol).
7. **Counter levels ≈ ladder mirror.** The LLM's opposite-direction setup (day_c1 at 0.3 ATR)
   means "hit a bull target then a bear level" happens for most picks in the first days. Any
   two-sided claim should use ATR-symmetric levels or swing/long-scale counters.
8. **The sealed period is below the 80-night floor** (71 nights), and deep-level windows are
   immature (60-session: 11 nights). The Registrar needs a prospective-accrual plan, or a PREREG
   that caps windows at 20 sessions.
9. **Minor.** `industry` is populated for only 12% of picks. `conviction_monitor` starts
   2026-05-12. Elite in-sample means 9 unique symbols in the analysis sample, mostly
   memory/semis.

## Reproducibility

`research/reports/explore/scripts/run_all.sh` regenerates everything. Derived parquet and logs are
in `research/reports/explore/work/` (regenerable; Haci may want to gitignore that folder).
`explore_lib.py` holds the conventions: basis conversion, windows, and in-sample loaders.
