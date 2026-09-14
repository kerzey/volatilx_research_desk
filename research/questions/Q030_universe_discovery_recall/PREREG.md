# Q030 — universe_discovery_recall: does the candidate universe find the big movers before they move?

**Status:** PREREG_DRAFT (lock by committing this file). Open decisions are listed in §11 and are
resolved by `@decision-maker decide Q030`, folded back by `@registrar apply Q030`, before the lock.
**Family:** **F8 System validity** (hypothesis **H-074**, Haci's H4 *Discovery*). DP-29 places it
there without argument: the primary endpoint's subject is neither the path after selection (F4) nor
the score's calibration (F2) — it is whether the step **before** selection, candidate generation,
reaches the names that go on to make large moves. H-074 is counted **once**, here.
**Manifest (R1 counts and the sealed post-hoc panel only):** research/data/manifest_v001.json
(as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e) and
research/data/manifest_prices_v001.json (as_of: 2026-09-10).
**Manifest (the question itself):** the **successor selection freeze** named in §5.3 (DP-23) —
`manifest_v00N` (`sas_candidates` **for every candidate row, published and unpublished**, `sas_runs`,
`market_regime_daily`) — and **`manifest_prices_universe_v001`**, a new price freeze covering **every
symbol in the pinned base universe `B`** (§2.2) plus every in-window candidate symbol and the
benchmarks, with ≥ 60 prior sessions before the first in-window night and 20 forward sessions beyond
the last. **The primary window is entirely prospective: not one night that carries a verdict here
exists in `manifest_v001`.**
**Base-universe artifact (pinned, and it is data, not code):** volatilx `data/sp500_sectors.json`,
key `mapping`, sha256 (LF-normalized) **`c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201`**
— the Q022 / Q024 pin, **one commit ever** (`4171b1a`, 2026-05-17, `_meta.last_synced` 2026-05-17,
source FMP `/profile`), never re-synced. **2,405 entries** (measured:
`research/reports/STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md`, sector-coverage section).
**Correction recorded, not silently applied:** the BACKLOG H-074 entry says *"the 2,252 symbols in
`data/sp500_sectors.json`"*; the file the desk actually holds carries **2,405** mapped symbols. Every
count in §5 uses 2,405, and `eval.py` fails loudly if the pinned blob's entry count or sha256 differs
from the two values printed here.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates` ∪
`non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, DP-22)
**unioned with the add-only successor exclusions file** issued with the successor selection freeze —
identical three lists, identical criteria, covering nights after 2026-09-10, add-only: no night is
ever removed from a v003 list. Both paths are `eval.py` inputs; no hard-coded file name, no
hard-coded date. DP-04 applies mechanically on top.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14

---

## 1. Hypothesis (plain English)

**The ~57 stocks VolatilX puts in front of its scoring engine each night contain the stocks that are
about to make a big move far more often than the same number of names drawn at random from the
investable market would — at least twice as often.**

BACKLOG **H-074** (Haci's H4, *Discovery*) reads: *"can VolatilX find major opportunities before they
move — PASS candidate-universe recall materially exceeds random / base-universe expectation, ideally
≥ 2× lift; FAIL the best future movers rarely enter the universe → candidate generation is the
bottleneck, not ranking."* It names the universe, the base universe, a mover definition, a recall
statistic and a lift threshold, and leaves the entry reference, the touch construction, the
random-draw denominator, the contributing-night rule and the decision rule open. This PREREG fixes
all of them.

**This is the step before every other selection question.** Q006 draws its controls from the night's
own candidate pool; Q024 draws its sector-matched random arm from the same pool; Q027 ranks inside
it. **None of them can see what the pool never contained.** Q030 is the only registered question
whose population is the market outside the pool.

**One primary** (§4), night-level, two-sided:

- **E1 — the discovery lift.** The share of that night's *movers* (base-universe symbols that go on
  to travel **+3 of their own ATRs within 20 sessions**) that were in the candidate universe, divided
  by the share a same-size random draw from the base universe would have captured. **MPE: lift ≥ 2.00**
  (Haci's own number; §4.2 states its source and §11 item 2 routes the unit question), with the
  two-sided mirror at **lift ≤ 0.50**.

**Secondaries, none of which decides anything** (§4.3): the same statistic for **bear** movers at
−3 ATR; **recall by source feed** (which of the seven source tags finds the movers); the
**sector-matched** and **liquidity-matched** random universes; the **tradeable-B** restriction; the
2-ATR and 4-ATR thresholds; and the **precision** form.

**Why the window starts after the lock.** The desk's weekly snapshots have repeatedly printed sealed
forward returns and 20-session touch rates for published picks (BACKLOG H-010, H-011, H-013 snapshot
lines; CLAUDE.md's standing findings). Those reads bear on the numerator of this statistic — how
often names that reached the universe go on to make large moves — even though nothing anywhere has
ever computed the denominator over the base universe. Under DP-45 that partial read is enough: the
window is **prospective-only, pick nights ≥ 2026-09-15** (§6), and the sealed stretch is printed once
as a labelled post-hoc panel that enters no verdict, no half, no stratum test, no CI comparison and
no q. This is the Q023 / Q024 / Q027 pattern, applied for the same reason. A second, independent
reason stands on its own: the candidate universe's **composition changed inside the sealed period**
(bear projection v1 rejoined the universe on 2026-07-02, commit `5b716a2`, volatilx
`services/candidate_universe_builder.py:120-148`), so the sealed stretch is not one feature.

**Direction of the claim.** H-074 predicts lift > 1 and Haci's PASS line asks for ≥ 2. The endpoint
is registered **two-sided**: a confirmed lift *below* 1 — the universe systematically avoiding the
names that move — would be the most consequential result this desk could produce about candidate
generation, and §9 says what it licenses.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Symbol rows are reduced to one statistic per
  night first; nights are the observations. Random-draw control symbols never add to n.
- **Source tables (successor selection freeze, §5.3):**
  `sas_candidates` — **every row, published or not, scored or not**: `trading_date`, `symbol`,
  `source_membership_json`, `overall_score`, `qualified`, `selected_rank`, `dominant_direction`,
  `best_timeframe` (the last five for sub-cells only, never for eligibility);
  `sas_runs` — `finished_at` (DP-04), `stats_json` (`universe_count`, `source_counts`,
  `sources_present` — the corroboration gate, §2.6), `config_json` (the universe-config audit,
  §5.2's split rule);
  `market_regime_daily` — `trading_date`, `regime_version`, `market_regime`, `created_at` (rule-7
  stratum only; never a filter, never an arm).
- **Source tables (`manifest_prices_universe_v001`, §5.3):** `prices_daily_split` (pick-night close,
  ATR14, 20-session dollar volume, forward bars to t+20, SPY tape) for **every base-universe symbol
  and every in-window candidate symbol**; `prices_daily_raw` (split-factor snapping only).
  **No hourly bar is used and no primary or secondary depends on one.**
- **Pinned artifact:** `data/sp500_sectors.json` `mapping` (2,405 symbols → sector ETF), sha256 above.
- **No outcome column is ever an input.** `outcome_*`, `sas_selection_excursion.*`, `level_hit_*`,
  `uoa_symbol_daily.fwd_return_*` are never joined; the last is banned outright (FREEZE_v001 §5).
  Every outcome in this question — for candidates and non-candidates alike — is computed from pinned
  bars, which is the only way a statistic over 2,405 symbols could be computed at all: the platform
  grades nothing outside its own published picks (FREEZE_v001 §4: 0 of 5,572 non-qualified rows
  sealed).

### 2.1 The candidate universe `U_t` — exact filter

**The two dates below are illustrative of values `eval.py` receives as inputs.** §5.3 R3 requires the
script to take the window start, the window end, the manifest paths, the exclusions-file paths, the
pinned-blob path and the output directory as arguments, with **no hard-coded date, manifest name or
path**, so the byte-identical script serves the primary run, the single DP-13 extension run and the
sealed panel alike.

```sql
SELECT DISTINCT c.symbol
FROM   sas_candidates c
JOIN   sas_runs run ON run.trading_date = c.trading_date
WHERE  c.trading_date >= DATE '2026-09-15'        -- §6 window start   (input, illustrative)
  AND  c.trading_date <= DATE '2027-01-26'        -- §5.2 window end   (input, illustrative)
  AND  c.trading_date NOT IN (<exclusions_v003 ∪ the add-only successor file:
                               manual_runs ∪ non_session_runs
                               ∪ uncorroborated_publication_runs, read from the JSONs>)
```

**No score filter, no qualification filter, no publication filter, no direction filter.** The
hypothesis is about the *universe*, not the slate: a symbol that entered `build_candidate_universe`
(volatilx `services/candidate_universe_builder.py:71`) and was scored has been "found", whatever
score it got, whether or not it published, and whichever direction the scorer settled on. The
qualification threshold (70.0, `services/super_agent_select_models.py:85`), the publication floor
(80.0, `:91`) and DP-28's publication predicate govern questions with a published arm; **Q030 has
none**, and `qualified` / `selected_rank` appear here only as descriptive sub-cells (§4.3).

**Why `sas_candidates` is `U_t`.** Every entry the universe builder returns is scored
(`services/super_agent_select_service.py:665-668`) and every ranked scorecard is persisted as a
candidate row (`:735-746`), so the candidate table is the universe, not a filtered survivor set.
`sas_runs.stats_json.universe_count` is written as `len(scorecards)` (`:445`) and is the independent
corroboration of that claim — §2.6 makes it a gate rather than a footnote.

**`U_t^B` = `U_t ∩ B_t`** (§2.2) is the set the primary uses. `|U_t|` — the whole universe, including
the ETFs and the non-`B` names — is carried as the as-filed companion denominator (§4.3, §11 item 1).

### 2.2 The base universe `B_t`, and the mover set `M_t`

- **`B`** = the 2,405 symbols in the `mapping` key of the pinned blob (S&P 500 ∪ Russell 2000 as of
  2026-05-17). **`B` is fixed for the whole question and is never re-synced mid-window**; a re-sync
  would make the denominator a different population (§10 threat 1).
- **`B_t`, the gradeable base universe on night t** = symbols of `B` with
  (a) ≥ 60 split-adjusted daily bars dated ≤ t (ATR14, `mom20`, `adv20` defined), and
  (b) a daily bar on the pick night t itself.
  Symbols failing either are **excluded and counted, per night, by reason** — never imputed.
- **`C_{s,t}`** = symbol s's regular-session close on night t from `prices_daily_split`.
  **`ATR_{s,t}`** = ATR14 from `prices_daily_split` bars dated ≤ t (never the platform's `atr_pct`,
  corrupted around splits — DATA_NOTES / PI-003).
- **The mover level**, bulls: `T_{s,t} = C_{s,t} + 3 × ATR_{s,t}`. Bears (secondary):
  `T^-_{s,t} = C_{s,t} − 3 × ATR_{s,t}`. **3 ATR is H-074's own distance and is registered as filed**
  (DP-25, DP-42 — the hypothesis names the level; the platform's L1–L6 ladder cannot be used here
  because 2,348-odd non-candidate symbols have no ladder, and that asymmetry is precisely what a
  recall statistic must avoid). The 2-ATR and 4-ATR versions are printed as a fixed sensitivity band
  (§4.3, DP-26) and decide nothing.
- **`M_t` (bull movers)** = symbols `s ∈ B_t` whose **regular-session high touches `T_{s,t}` on some
  session in t+1..t+20**. A gap through `T_{s,t}` at a session open is a touch.
  **This is a path definition, not a fixed-horizon one** (rule 5, DP-01): a symbol that travels 3 ATR
  by t+6 and gives it all back by t+20 *was* the opportunity, and a t+20 close-to-close test would
  miss it. The t+20 close-to-close version is printed and **decides nothing**.
- **Right-censoring is never graded as a non-move.** A symbol whose forward bars stop at t+k (k < 20)
  through halt, delisting or acquisition is a **mover** if it touched by t+k, and is **excluded and
  counted as ungradeable** if it did not. This is the clause that keeps takeover pops — which delist
  — inside `M_t` instead of silently deleting the most discoverable movers there are.
- **Every symbol is asked to travel the same number of its own ATRs, in the same direction, on the
  same clock.** That is where rule 5's distance-matched control lives in this question: the
  comparison is not picks against an outside cohort, it is the universe against the rest of the
  market with an identical, self-scaled distance on both sides. A recall number from this question is
  never quoted without that sentence attached (§8's language clause).

### 2.3 The night statistic

For a contributing night t (§2.5), with `n_t = |U_t^B|`, `m_t = |M_t|`, `b_t = |B_t|`:

| quantity | definition |
|---|---|
| **`recall_t`** | `|M_t ∩ U_t^B| / m_t` — the share of the night's movers the universe had already found at 16:05 ET |
| **`e_t`** | `n_t / b_t` — the recall a uniform random draw of `n_t` symbols from `B_t` captures in expectation (exact, hypergeometric) |
| **`precision_t`** | `|M_t ∩ U_t^B| / n_t` — the share of the universe that turned out to be movers |
| **`base_t`** | `m_t / b_t` — the night's market-wide mover rate |
| **identity** | `recall_t / e_t ≡ precision_t / base_t`. The lift is symmetric in the two readings, and both are printed. |

**The entry reference is the pick-night close `C_t`** and the measurement window is t+1..t+20, for
every symbol alike. This is the **discovery** framing, not a trade: a name that gaps +3 ATR at the
t+1 open is exactly the "major opportunity" H4 asks whether the platform found *before* it moved, so
it counts. Rule 5's *"a target already passed at entry is not a hit"* governs a pick's tradeable
target and is honoured in the **tradeable companion** (§4.3): the same statistic from the session
t+1 open with gap-throughs excluded, printed always, deciding nothing, and §9 forbids reading the
primary as a tradeable claim.

### 2.4 Exclusions — each counted, printed in the results header, never silently dropped

Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, the
pinned blob, or a measurement failure. None can move a symbol between `U_t` and its complement.

- **Nights** in the union of `exclusions_v003.json` and the add-only successor file; any night whose
  `finished_at` is later than the next session's open, or dated on a non-session day (DP-04); any
  night with no SAS run.
- **Base symbols failing §2.2's (a) or (b)** → excluded from `B_t` and counted by reason. A symbol
  excluded from `B_t` is excluded from `M_t`, from `U_t^B` and from `b_t` **simultaneously** — it
  never sits in one term and not another.
- **Ungradeable base symbols** (no touch and forward bars truncated before t+20) → excluded and
  counted (§2.2). A night is **non-contributing** if more than **10%** of `B_t` is ungradeable.
- **Candidate symbols outside `B`** (ETFs, ADRs, post-May-2026 listings) → not in `U_t^B`, counted
  every night with their symbols listed, and carried in the as-filed `|U_t|` companion (§4.3).
- **Nights whose `stats_json` corroboration fails** (§2.6) → excluded and counted.
- **Immature nights** — session t+20 after the last trading date of `manifest_prices_universe_v001` →
  excluded and counted. Maturity comes from the trading calendar, never from whether a price exists.
- **Nights with `m_t = 0` or `n_t = 0`** → `recall_t` or `e_t` undefined → **non-contributing**
  (§2.5), counted, not an exclusion.

### 2.5 Contributing night, and the episode (DP-51)

- **Contributing night (the floor unit, DP-21):** a non-excluded, matured night in the window with
  `m_t ≥ 1`, `n_t ≥ 1`, `B_t` covering **≥ 90%** of the pinned blob's 2,405 symbols, ungradeable share
  ≤ 10%, and the §2.6 corroboration passing. **No minimum `m_t` beyond 1 is imposed**, deliberately:
  a floor on the mover count would select nights by the tape's own breadth, in a direction the desk
  cannot sign. The `m_t` distribution is printed, and the `m_t ≥ 10` restriction is a mandatory
  sensitivity (§4.3).
- **Episode (DP-51, the H-070 unit):** one **symbol's** run of appearances in the eligible analysis
  population — membership in `B_t` for base symbols, appearance in `U_t` for candidates — with gaps
  of **≤ 10 sessions** between successive appearances; a gap of 11 or more starts a new episode
  (the TI-003 / Q003 / Q027 §2.5 window). For a continuously listed base symbol this is one episode
  spanning the window, so CI 2 (§4.4) is in effect a **symbol-clustered** bootstrap — which is the
  conservative reading, and it is meant to be.
  *Why it bites here specifically:* `M_t` is defined by a forward 20-session window on every night, so
  **one 3-ATR run makes the same symbol a mover on up to 20 consecutive nights**, and the same ~57
  names recur in `U_t` night after night. A night-clustered CI treats one symbol's single move as up
  to twenty independent observations of "the universe found a mover". The night cluster absorbs
  same-night correlation; the episode cluster absorbs the other axis.

### 2.6 The universe-corroboration gate

`U_t` is read from `sas_candidates`, but the run's own `stats_json` independently records
`universe_count`, `source_counts` and `sources_present`
(`services/super_agent_select_service.py:445`, `:457-458`). `eval.py` compares the two per night and
**fails loudly** when the distinct-symbol count of `sas_candidates` differs from
`stats_json.universe_count` by more than **2%** of `universe_count` on any night, and marks that
night excluded (§2.4). This is the Q026 Channel-C construction, and it is the only defence against
the one failure mode that would silently deflate recall: a universe entry that was built, was never
persisted as a candidate row, and would therefore be scored as "the platform never found it".

## 3. Baselines — what this must beat

- **B1 (primary, the null): a uniform random draw of `n_t` symbols from `B_t`, on every night.**
  Its expected recall is `e_t = n_t / b_t` exactly, so the point estimate needs no simulation; the
  simulation supplies the null's dispersion. **10,000 randomization draws, seed 20260914**: on each
  draw, replace `U_t^B` by a uniform `n_t`-subset of `B_t` on every night, recompute the whole
  endpoint, and read the two-sided p off the resulting distribution, which is centred on lift = 1 by
  construction. Monte Carlo; **adds no n** (rule 6).
- **B2 (secondary, H-074's own second baseline; blocking only in one direction): a sector-matched
  random universe of the same size.** Draw `n_t` symbols from `B_t` matching the sector-ETF
  composition of `U_t^B` exactly (the pinned blob's 11 ETFs; a sector short of names draws the
  remainder unconstrained and the shortfall is counted, the Q024 SECRAND convention). This is
  H-072's lesson applied to discovery: a universe that is simply always long semis would show a lift
  without finding anything.
- **B3 (secondary, blocking only in one direction): a liquidity-matched random universe.** Draw `n_t`
  symbols from `B_t` matched on the decile of trailing 20-session dollar volume (`adv20`, from bars
  ≤ t) of `U_t^B`. Options flow lives in liquid names, and a lift that is entirely "liquid names move
  3 ATR more (or less) often" is not discovery.
- **B4 (descriptive): the universe's own persistence.** `U_{t−1}^B` used in place of `U_t^B` on night
  t — the lift a one-day-stale universe achieves. It measures how much of any lift is same-night
  information rather than a standing list of usual suspects. Descriptive, never decides.

**Blocking clause on B2 and B3 (§8 clause 6):** a question-level CONFIRMED is blocked if **either**
matched lift's point estimate is **below 1.00 with its own 95% night-clustered CI excluding 1.00** —
i.e. if the universe *loses* to a sector- or liquidity-matched random draw. No magnitude is invented
for them beyond "must not lose": they carry no MPE and cannot confirm anything.

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Nothing in this question is decided by a fixed-horizon return.** The t+20 close-to-close version of
the mover set, and the mean forward return of `U_t^B` against `B_t`, are printed and are
**descriptive by rule 5 and DP-01**.

### 4.1 Per night

`recall_t`, `e_t`, `precision_t`, `base_t` as defined in §2.3, over §2.5's contributing nights.

### 4.2 The primary endpoint

- **E1 = (mean over contributing nights of `recall_t`) / (mean over contributing nights of `e_t`)** —
  a dimensionless lift, null value **1.00**.
  The ratio-of-means form is registered rather than the mean of per-night lifts because `m_t` is a
  small count on a quiet night and `recall_t / e_t` is then violently right-skewed (a single mover
  found on a night with `e_t = 0.02` reads as a lift of 50). Both means are night-level statistics,
  the bootstrap resamples nights and recomputes the whole ratio, so the night remains the unit of
  inference (rule 6). **The mean of per-night lifts is printed beside it, descriptively.**
- **MPE: `E1 ≥ 2.00`**, mirror `E1 ≤ 0.50`.
- **Materiality floor (registered alongside the MPE, §8 clause 3b):**
  `D = mean_t(recall_t − e_t) ≥ +1.0 pp` (mirror ≤ −1.0 pp), printed with its own two CIs.

**On the MPE.** `≥ 2× lift` is **Haci's own number**, from the Master Hypothesis Program's H4 PASS
line (`research/reports/INBOX_2026-09-14_master_hypothesis_program.md` §1, H4: *"Candidate-universe
recall materially exceeds random/base-universe expectation, ideally ≥2× lift"*). It is applied as
registered, with "ideally" read as the threshold rather than as an aspiration (DP-45: the stricter
reading). **DP-20 is considered and not applied**: it governs a **touch-rate** endpoint whose base
rate sits at 40–70%, where +5.0 pp is a proportionate bar; here the null base rate is
`e_t ≈ 57 / 2,405 ≈ 2.4%`, and +5.0 pp on that base would demand a lift above 3 — a different and
unfiled hypothesis. **DP-44 carries no MPE unit for a ratio endpoint** and an autonomous run writes
no DP entry from a DEFAULTED item, so **§11 item 2 puts "lift MPE unit" to the Decision-maker as a
standing rule**. The materiality floor exists because a ratio alone can be large over nothing: a lift
of 2 over a base rate of 0.4% would mean the universe captures under 1% of the market's movers, which
no one could call discovery. **Neither the MPE nor the floor is lowered at the decision pass in any
branch** (rule 6).

### 4.3 Secondary, sensitivity and descriptive output

Everything here prints raw p only and is labelled *"descriptive, does not decide"* — **except the
named blockers** (§8 clauses 6–9), which carry no verdict of their own but block a CONFIRMED verdict
when they run the other way. Suppression restricts affirmative reporting only: it never removes a
blocker.

**Computed, and blocking:**

- the **as-filed denominator** companion — E1 recomputed with `n_t = |U_t|`, the whole universe
  including symbols outside `B` (§11 item 1). It is the arithmetically looser construction's mirror
  image: a larger `n_t` raises `e_t` and lowers the lift, so requiring it to clear 2.00 as well makes
  the pair strictly the stricter test (clause 7);
- **B2 sector-matched** and **B3 liquidity-matched** lifts (§3, clause 6);
- the **tradeable-B** restriction — `B_t` further restricted to `C_{s,t} ≥ $5` and `adv20 ≥ $5M`,
  which changes `b_t`, `m_t`, `n_t` and `e_t` together — must not sit below lift 1.00 with its CI
  excluding 1.00 (clause 8). It is the version a subscriber-facing claim would have to rest on, and
  §9 says so;
- **Half A / Half B** (§6) — the stability clause, blocking at whatever count it has, not a reported
  stratum and not on the suppression list (clause 10);
- the **monthly-block stability panel**: E1 within calendar month for months with ≥ 10 contributing
  nights; the ≥ 60% same-sign-as-full-sample share is clause 11.

**Computed, mandatory, purely descriptive — the list closes at lock (rule 8's forking-path rule):**

- the **bear secondary**: the identical statistic at −3 ATR over bear movers, with both CIs, raw p,
  and a second variant restricting `U_t^B` to rows with `dominant_direction = 'bearish'` or a bear
  source tag. **No verdict rests on it and §9 says a striking bear result licenses a successor
  PREREG and nothing else** (the Q027 / H-012 convention);
- **recall by source feed**: `U_t^B` restricted to each of the seven source tags
  (`uoa_day`, `uoa_swing`, `uoa_long`, `whale_watch`, `projection_bullish`, `projection_bearish`,
  `projection_bearish_v2` — `services/candidate_universe_builder.py:91-148`), each with its own
  `n_t` and therefore its own `e_t`, so the feeds are compared at equal draw size. Seven forking
  paths; raw p only; this is the table that names which feed to widen if the verdict is NULL (§9);
- the **2-ATR and 4-ATR** mover thresholds (fixed at lock, DP-26);
- the **`m_t ≥ 10`** restriction (§2.5);
- the **tradeable companion** — the whole endpoint from the session t+1 open with gap-throughs
  excluded (§2.3);
- the **t+20 close-to-close** mover definition — rule 5's descriptive twin, printed to show how much
  of `M_t` is path rather than endpoint;
- **B4**, the stale-universe lift;
- **precision and base rate** per night, and the `recall_t` / `e_t` / `m_t` / `n_t` / `b_t` series in
  full;
- **sessions-to-first-touch** among movers, universe versus non-universe — the speed read (DP-08):
  if the universe finds movers *late*, it shows here;
- **overlap counts**: `|U_t ∩ B|`, `|U_t \ B|` with symbols listed, and the distinct-symbol and
  **episode** counts with the episode-length distribution;
- the **mover-characteristics table**: `adv20` decile, price level, sector, `ATR%` and `mom20` of
  `M_t ∩ U_t^B` versus `M_t \ U_t^B` — what the universe systematically misses, which is the
  operational half of a NULL;
- the **published-slate footnote**: `|M_t ∩ (published picks)| / m_t`, printed for context only. It
  is **not** a selection-edge statistic and §7 forbids reading it as one.

**Sub-cells — the list is FIXED at lock** (revised once at `record` from R1's measured counts, then
closed). Reported only at ≥ 20 contributing nights; below that, SUPPRESSED (counts only):
`market_regime_daily.market_regime` (rule 7, §6); the SPY `tape_t` stratum (§6); terciles of `m_t`
(market breadth); terciles of `n_t`; bull and bear; sector of the mover. **All six `tape_t` cells are
expected to be SUPPRESSED** (≈ 15 nights each at the registered window length) and are printed as
counts; no suppression removes a blocker.

**Quotability:** 20-session basis, W20 research window → **every number in this question is
`NON_QUOTABLE`** (rule 12). **No 40-session companion is computed**: it would add 20 sessions of
maturity to the schedule for a number that decides nothing.

### 4.4 Inference — two CIs for the primary (DP-51)

Night-level throughout. Random-draw control symbols never add to n (rule 6).

- **CI 1 — date-clustered (the registered bootstrap):** resample **contributing nights** with
  replacement, 2,000 resamples, recomputing `mean(recall_t) / mean(e_t)`. A **stationary block
  bootstrap** over the ordered nights (expected block length **10 sessions** — the Q004 / Q007 /
  Q009 / Q011 / Q015 / Q023 / Q027 value, fixed at lock, not chosen after seeing anything) is printed
  beside it.
- **CI 2 — episode-clustered (DP-51):** resample **symbol-episodes** (§2.5) with replacement **and**
  nights with replacement, jointly: draw a bootstrap set of episodes and a bootstrap set of nights,
  keep the symbol-nights in the intersection, recompute each retained night's `recall_t` and `e_t`
  from the surviving symbols (`B_t`, `U_t^B` and `M_t` all restricted to survivors; a night is
  retained only if `m_t ≥ 1` and `n_t ≥ 1` among survivors), and recompute the ratio of means. 2,000
  resamples, same seed.
- **DP-51's rule is a decision rule here, not a footnote: a primary that clears MPE with CI 1
  excluding 1.00 but CI 2 including 1.00 is INCONCLUSIVE, never CONFIRMED** (§8 clause 5).
- **p-value (decides, feeds BH):** B1's randomization null, 10,000 draws, seed 20260914, two-sided.
- **Every estimate prints:** contributing nights; `b_t`, `n_t`, `m_t` (min / median / max); distinct
  symbols and **episodes** with the episode-length distribution; contributing nights dated after the
  lock commit; symbols excluded by reason, per night; the `|U_t \ B|` list; the corroboration-gate
  residuals; and the §4.3 mover-characteristics table.

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights for the primary endpoint** and
  ≥ **20 contributing nights per reported sub-cell**. The weaker "80 eligible with ≥ 20 contributing"
  reading is not used. **No floor is ever lowered to reach a date.**
- **DP-24:** ≥ 30 contributing nights dated after the lock commit. **Every** contributing night here
  is post-lock by construction (§6), so DP-24 binds at 30 of the 80 and is not the gate.
  **PROSPECTIVELY_CONFIRMED is reachable from this run by design; DP-31 does not apply and no
  successor replication question is needed.**
- **Binding maturity: 20 sessions**, uniform across every symbol (§2.2).
- **The primary is not demotable.** A night shortfall is a floor failure — the single DP-13
  extension, then DEFERRED — never a demotion to descriptive (DP-43).

### 5.1 Exposure basis — and why no second Steward count is routed

**The candidate-side contributing-night rate is taken from the Steward's Q027 exposure report**
(`research/reports/STEWARD_Q027_exposure.md`, in preparation at this lock, measured counts-only on
`manifest_v001` + `manifest_prices_v001` over pick nights 2026-06-01..2026-09-10 against
`exclusions_v003.json`), **rather than routing a second count for the same nights.** That report
measures the all-candidates funnel — Q027 §2.5's contributing night, a non-excluded matured night
carrying ≥ 30 eligible candidate rows — which is **strictly narrower** than Q030's night rule: Q030
needs only a valid non-excluded matured run with `n_t ≥ 1` and `m_t ≥ 1`, and imposes **no per-row
screen on candidates at all** (it needs bars for base-universe symbols, not for candidates). Q027's
measured rate is therefore a **lower bound** on Q030's, and using it is conservative in the only
direction that matters (DP-43: dates move out, never in).

What the desk already holds, all counts-only and all from pinned freezes:

| quantity | measured | source |
|---|---|---|
| contributing nights per elapsed session, published-pick funnel | **0.9538** (62/65) | `STEWARD_Q023_exposure.md` §5 |
| eligible nights per elapsed session before the freeze-horizon maturity cut | **0.9783** (45/46) | `STEWARD_Q024_…` (a) |
| candidate rows per night with ≥ 60 prior daily bars | min **56**, median **63**, max **68** | `STEWARD_Q024_…` (b) |
| base-universe entries in the pinned blob | **2,405** | `STEWARD_Q024_…`, sector coverage |
| all-candidates funnel rate | **to be measured** | `STEWARD_Q027_exposure.md` (R1a) |

**Planning rate used in §5.2: 0.9538 contributing nights per elapsed session**, stated as **borrowed**
rather than dressed up with an invented haircut (the Q023 §5.1 finding: *"a haircut on a borrowed
number is not a haircut"*), with an 8-session cushion carried in the window instead. R1 replaces it
with the measured Q027 rate at `record`, and a measured rate can only move the dates **out**
(DP-43, DP-45).

**What has never been measured, and is R2's job:** anything at all about `B`. No desk report has
computed a single quantity over the 2,405-symbol base universe — not bar coverage, not a mover rate,
not `|U_t ∩ B|`. That is why R2 is blocking for the lock (§5.3) and why §8's floors are stated on
nights rather than on movers.

### 5.2 Window, decision date, extension, DEFERRED fallback (DP-43, DP-13; no outcome is looked at)

**Window: pick nights 2026-09-15 .. 2027-01-26 inclusive = 92 elapsed sessions.**
**Decision date: Monday 2027-03-08.** Single DP-13 extension to pick nights **.. 2027-03-10**
(122 sessions), decided **Monday 2027-04-19**, which is also the **hard stop**: still short there,
Q030 goes to DEFERRED.

| floor | planning rate | sessions needed | projected at 92 sessions |
|---|---|---|---|
| **A:** ≥ 80 contributing nights (DP-21) | 0.9538/session | 84 (2027-01-13) | **87.7 nights** |
| **B:** ≥ 30 contributing nights dated after the lock commit (DP-24) | 0.9538/session | 32 (2026-10-29) | **87.7** (all post-lock by construction) |
| **C:** ≥ 20 contributing nights per *reported* sub-cell | — | — | decided cell by cell at the decision pass; suppression list §4.3 |

**Arithmetic, session by session** (holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18,
2027-02-15, 2027-03-26): 2026-09-15 is session 1; Sep 12 + Oct 22 + Nov 20 + Dec 22 = 76 at
2026-12-31; Jan 4–8, 11–15, 19–22, 25, 26 = **92 at 2027-01-26** (Tuesday). Floor A alone is met at
session 84 = 2027-01-13; the window carries **8 further sessions** so the floor is met inside the
primary window rather than only if the extension fires. **Decision date:** 2027-01-26 **+ 20
sessions** maturity = **2027-02-24**; **+ one calendar week** freeze margin = 2027-03-03; first
Monday on or after = **Monday 2027-03-08** — **5.8 months from the lock**, well inside DP-43's
12-month ceiling. `eval.py` is written once (rule 9) and run **once**, then. **No interim looks.**

**This is deliberately the identical window, maturity and schedule as Q027**, so that one successor
selection freeze and one price fetch can serve both: `manifest_prices_universe_v001` is a strict
superset of Q027's R2 price freeze (it covers `B` ∪ every in-window candidate symbol), and the
add-only successor exclusions file is the same file. The alignment is an efficiency for the Steward,
not a statistical link — §7 states that the two questions share no endpoint and may not be read as
confirming each other.

- **Extension (DP-13; DP-43's +30 sessions).** If a floor is short at 2027-03-08 on `eval.py`'s
  **own measured counts** (never on a projection or a run-rate), the window extends **once**,
  automatically and with no new question, to pick nights **2026-09-15 .. 2027-03-10** (session 122),
  decision **Monday 2027-04-19** (2027-03-10 + 20 sessions = 2027-04-08; + one week = 2027-04-15;
  first Monday on or after). The extended run uses the **byte-identical, unmodified `eval.py`** and
  the same floors. 7.2 months from lock, inside the ceiling.
- **DEFERRED fallback (the hard stop).** If a floor is still short after that single extension, Q030
  goes to `research/questions/DEFERRED.md` with the measured counts rather than running
  under-powered. **No second extension, no reduced floor, and a floor shortfall is never an
  INCONCLUSIVE verdict** (§8).
- **Fixed at lock and not reopened at the decision pass:** the MPE and the materiality floor (§4.2,
  §8); the 3-ATR level and the 2/4-ATR sensitivity band; the 20-session clock; the 90% `B_t` coverage
  and 10% ungradeable rules; the 2% corroboration tolerance; the 10-session block length; `m = 1`
  (§7); the sub-cell suppression list (§4.3, revised once at `record` from R1 and then closed); the
  §4.3 descriptive list, which closes at lock.
- **If the universe's composition changes mid-window**, `U_t` is **two different features** and the
  window is **cut at the ship date**: the post-ship segment becomes the question's window with this
  whole schedule recomputed from it — **out, never in**, subject to the same single extension and the
  same 12-month ceiling measured from the original lock — the pre-ship segment becomes a labelled
  descriptive panel entering no verdict, and if neither segment reaches the floor inside the ceiling
  the question is **DEFERRED** (DP-06's pattern, DP-50(a)). A "composition change" is, exactly: any
  commit touching `services/candidate_universe_builder.py`; any change to `uoa_screener.max_symbols`
  (today 40, `services/uoa_screener.py:351`), to the UOA bulletin's day/swing/long list sizes, to the
  insider-watch parameters (`insider_limit`, `insider_min_otm_pct`, `insider_min_dte`,
  `insider_max_dte`, `insider_history_days`, `insider_min_premium_max`, `insider_min_spike_mult`), or
  to which projection tables feed the universe; and any `sas_runs.config_json` change to those keys.
  **A change to the scoring weights, the thresholds or the publication floor is *not* such a split for
  this question** — the universe is built upstream of scoring — and that narrower split rule is one of
  the few advantages Q030 has over every other question in flight.

### 5.3 Routed requests

- **R1 → data-steward (counts only; blocking for the schedule, not for the lock).** No new work:
  **take (a) from `research/reports/STEWARD_Q027_exposure.md`** as delivered — the all-candidates
  contributing-night rate per elapsed session over 2026-06-01..2026-09-10, denominators in elapsed
  sessions with exclusions not pre-removed (the Q019 / Q022 / Q023 convention) — and add only:
  (b) the distinct-symbol count of `sas_candidates` per night **against `sas_runs.stats_json.universe_count`**,
  with the count of nights exceeding the 2% tolerance (§2.6) and the per-night `source_counts`;
  (c) the share of each night's candidate symbols present in the pinned blob's `mapping`, and the
  distinct list of candidate symbols **absent** from it over the sealed window (the ETF / non-`B`
  residue of §2.4);
  (d) the **DP-50(a)/(b) commit sweep** since manifest SHA `fa70688` over
  `services/candidate_universe_builder.py`, `services/uoa_screener.py` and the projection-pick
  writers — with an explicit answer **even when it is "none"** — and a dated `DATA_NOTES.md` entry
  for any repair that rewrote historical rows.
  No outcome of any kind is read; no live query (DP-50(c)).
- **R2 → data-steward (BLOCKING FOR THE LOCK — the universe price freeze).** Build
  **`manifest_prices_universe_v001`**: daily bars, `adjustment=split` and `adjustment=raw`,
  `feed=sip`, from the Alpaca market-data host, for **every one of the 2,405 symbols in the pinned
  blob's `mapping`**, plus every in-window candidate symbol and the existing benchmarks, covering
  **≥ 60 sessions before 2026-09-15** through **2027-02-24** (20 sessions beyond the last in-window
  pick night), delivered before **Monday 2027-03-08**; a second cut **only if** the DP-13 extension
  fires, through 2027-04-08, delivered before **Monday 2027-04-19**, built then and not before.
  The existing tool takes its symbol list from a base manifest (`research/lib/freeze_prices.py`,
  `BATCH = 50`, `:46`); extending it to take an explicit symbol list is a change under `research/`
  and is **not** an enforcement file under rule 15. **No hourly bars are required.** Symbols with no
  bars are **excluded and counted, never back-filled or imputed**.
  **Three things R2 must report before the freeze is pinned, and they decide whether Q030 locks:**
  **(i) feasibility** — whether `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` are present in the Steward's
  environment and the 2,405-symbol pull completes (the Q024 R1(d) failure is the known hazard: that
  check *could not be run* for one benchmark symbol because no credentials were present);
  **(ii) coverage** — the share of the 2,405 symbols returning ≥ 60 bars in a trailing 60-session
  probe, which must be **≥ 90%** (§2.5's `B_t` rule applied to the freeze itself);
  **(iii) a counts-only dry run on the sealed period** — `b_t`, `n_t`, `m_t` and nothing else (no
  `recall_t`, no lift, no intersection count) for pick nights 2026-06-01..2026-08-12, so the desk
  knows whether `m_t ≥ 1` is ever binding before it commits to a schedule.
  **The lock-or-DEFER gate R2 decides:** feasibility **and** coverage ≥ 90% **and** an
  all-candidates contributing-night rate (R1a) **≥ 0.36 per elapsed session** — the DP-43 ceiling
  solved at this lock leaves ≈ 225 admissible elapsed sessions, so 80 nights requires 0.356 — → Q030
  locks and §5.2's dates are recomputed on the measured rate, **moving out only**. Any limb failing →
  Q030 goes to `research/questions/DEFERRED.md` with the measured numbers and the blocker named
  (credential, coverage or rate), unregistered. Every neighbouring night-rate measurement sits
  between 0.95 and 0.98, so the rate limb is a clear expected pass; **the credential limb is the real
  risk and is the reason R2 blocks the lock rather than merely the decision date.**
- **R3 → data-steward (due before the decision date; not a blocker for lock; DP-23).** The successor
  **selection** freeze `manifest_v00N` (same SQL, same exclusion criteria) covering pick nights
  2026-09-15..2027-01-26 (and ..2027-03-10 if the extension fires), with the **add-only successor
  exclusions file** — the identical file Q027's R2 requires, built once. Where a successor freeze
  overlaps an earlier one on `sas_candidates`, the rows are compared and `eval.py` **fails loudly** on
  any disagreement in the symbol set of a night (a repair that changed which symbols were candidates
  would silently re-run this experiment — DP-50(a)). R1(d)'s commit sweep is **repeated for the
  period between the freezes**. Every §5.2 date is re-confirmed session by session from the trading
  calendar when the freeze is built; a correction may move a date **out, never in**.
- **R4 → data-steward (optional, droppable, and it decides nothing): the sealed-period universe
  price freeze.** The same B-wide bars for pick nights 2026-06-01..2026-08-12 with forward bars to
  2026-09-10, so the same byte-identical `eval.py` can print §6's labelled post-hoc panel **at the
  decision pass, never before**. If R2's fetch proves expensive or rate-limited, **R4 is the first
  thing dropped** and the panel is simply not printed; no verdict, no clause and no date depends on
  it.

## 6. Test window, split and stratification

- **Test window: prospective only — pick nights 2026-09-15 .. 2027-01-26**, opening on the first
  session after the lock commit dated 2026-09-14 (the window starts on 09-15 rather than 09-14 so
  that no night whose 16:05 ET run may precede the lock commit can enter), through §5.2's end.
  *Justification.* Two reasons, either sufficient: (a) the sealed period has been read against the
  numerator's ingredients — the weeklies have printed sealed forward returns and 20-session touch
  rates for published picks, and CLAUDE.md carries standing findings drawn from them, so how often
  names that reached the universe go on to travel a multiple of their ATR is not blind on those
  nights (DP-45); (b) the universe's **composition changed inside the sealed period** — bear
  projection v1 rejoined the candidate universe on 2026-07-02 (`5b716a2`,
  `services/candidate_universe_builder.py:120-148`) — so `U_t` is not one feature across it.
- **The sealed post-hoc panel** (R4; `manifest_v001` + the sealed universe bars, pick nights
  **2026-06-01 .. 2026-08-12** — after the DP-06 boundary and at the 20-session maturity cutoff of
  the sealed price horizon) prints every §4 endpoint **once**, labelled, and enters **no verdict, no
  CI comparison, no half, no stratum test, no q and no §9 rule**. It is split at **2026-07-02** into
  sub-panels **A = 2026-06-01..2026-07-01** and **B = 2026-07-03..2026-08-12** and the halves are
  never blended (the bear-v1 rejoin above). Each sub-panel is SUPPRESSED below 20 contributing
  nights. It is computed by the same byte-identical `eval.py` **at the decision pass**, so it cannot
  inform any choice made here.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date (re-derived from the final window at the decision pass); Half B = after.
  The primary must carry the same side of 1.00 in both halves (§8 clause 10). The halves are a
  **stability clause, not a reported stratum**, and block at whatever count they have.
- **Monthly blocks:** calendar months of the window with ≥ 10 contributing nights; the share with the
  same side of 1.00 as the full-sample estimate is §8 clause 11. At the registered length that is
  four to five blocks, so the clause reads as "at least 3 of 4" or "at least 3 of 5" — stated
  numerically at the decision pass from the measured block count, with the rule (≥ 60%, rounded up)
  fixed here.
- **Regime stratification (rule 7).** Two stratifiers, both reported, both subject to §4.3's
  ≥ 20-night rule, both constructed exactly as in Q027 §6:
  - `market_regime_daily.market_regime`, **v1.2 only**, the row with `trading_date = t`, legal only
    where `created_at` falls on that `trading_date` **and at or before that night's own
    `sas_runs.finished_at`** (the Q023 §2.2 timestamp test). A night with no legal label keeps its
    place in the primary — the label is a **stratifier here, not a filter and not an arm** — and is
    reported in an `unlabelled` cell. The window starts long after the 2026-06-09 point-in-time
    boundary (FREEZE_v001 §7), so the backfill hazard cannot reach it.
  - **`tape_t`**, the SPY proxy, trailing and legal at 16:05 ET: sign of SPY's trailing 20-session
    return × tercile of its trailing 20-session realized volatility, from `prices_daily_split` bars
    dated ≤ t, with **expanding-window** tercile cut points, so no later night's data sets an earlier
    night's stratum. All six cells are expected to be SUPPRESSED and are printed as counts.
- **Knowledge time (rule 14) — every input declared. Q030 needs no rule-14 exception and requests
  none** (DP-05 untouched, DP-41 respected).

  | input | source | available | use |
  |---|---|---|---|
  | `symbol` set of the night's candidates, `source_membership_json` | `sas_candidates` (all rows) | pick night, 16:05 ET | `U_t`, source secondary |
  | `universe_count`, `source_counts`, `finished_at`, `config_json` | `sas_runs` | publication time on the pick night | corroboration gate, DP-04, §5.2 split audit |
  | `overall_score`, `qualified`, `selected_rank`, `dominant_direction` | `sas_candidates` | pick night, 16:05 ET | descriptive sub-cells only |
  | base-universe membership and sector | `volatilx:data/sp500_sectors.json`, sha256 `c4d12610…0201` | 2026-05-17, four months before the first in-window night; never re-synced | `B`, B2 |
  | `C_{s,t}`, ATR14, `adv20`, `mom20`, SPY tape | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | mover levels, `B_t`, B3, `tape_t` |
  | `market_regime` (v1.2, `trading_date = t`) | `market_regime_daily` | declared 16:05 ET / lag 0, enforced per night by the timestamp test | rule-7 stratum only |
  | daily bars t+1..t+20 for every `B_t` symbol | `prices_daily_split` | after the pick night | **outcome measurement only** |

  **What `eval.py` must enforce:** `B_t`, `U_t`, `U_t^B`, every mover level `T_{s,t}`, every episode id
  and every stratum label are computed and written to a frozen per-symbol-night table **before any
  post-pick-night bar is loaded**. The run fails if any t+1-or-later field is referenced in
  eligibility, in universe membership, in the mover level, or in stratification.

## 7. Multiple testing

- **Within the question: m = 1** — E1 — so BH within the question is degenerate and the raw p is the
  q. **`m = 1` is fixed at lock**: the bear statistic, the seven source feeds, the matched baselines
  and every sensitivity print raw p only, marked *"descriptive, does not decide"*, and **no secondary
  is promoted to a primary at the decision pass**. That is the whole protection against this
  question's forking-path risk, which is large (seven feeds × two directions × three ATR thresholds),
  and the §4.3 list closes at lock for the same reason.
- **Across the family: F8 System validity.** F8's BH correction runs across the members carrying
  primaries — **H-074 (this question), H-081 and H-083**; H-069 (Q026), H-070 (DP-51), H-076 (Q028),
  H-077 and H-084 are diagnostics or syntheses with no primary and enter no correction set. At this
  lock the F8 set is **Q030 (1)** and it **never shrinks below 1**; if H-081 or H-083 locks before
  2027-03-08 its primaries join the set and the q's are recomputed on the larger m at the decision
  pass. Threshold **q ≤ 0.10**, alongside raw p (rule 8).
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q006 (F1)** contrasts published picks against distance-matched unpublished controls *inside*
    the universe. Q030 asks whether the universe contains the movers at all. A confirmed Q030 says
    nothing about whether SAS picks well **within** the pool, and a confirmed Q006 says nothing about
    what the pool missed. Neither may be quoted as support for the other.
  - **Q024 (F1)** benchmarks the published slate against SPY, equal-weight, a **sector-matched random
    draw from the same-night candidate pool**, and momentum ranks. Q030's B2 draws from **`B`**, not
    from the pool — the two random arms are drawn from different populations and answer different
    questions. A Q024 confirmation does not imply discovery, and a Q030 confirmation does not imply
    the slate beats SPY.
  - **Q027 (F2)** ranks candidates inside `U_t` by score. Q030's population is `B`. The two questions
    share the successor freeze and the schedule and **no endpoint**: the universe could contain every
    mover and rank them backwards, or contain few and rank those few perfectly.
  - **Q022 (F4)** uses the same pinned sector blob for a same-night concentration arm; the shared
    artifact is not a shared test.
  - **Q028 (F8)** decomposes the layer subscores' structure and reads no price bar; it cannot
    contaminate this question and is not in the correction set.
  - **H-081 and H-083 (F8, unregistered)** are the other two F8 members carrying primaries; their
    primaries join this correction set when they lock, and neither is tested here.
  - **EN-016** (a larger candidate universe) is the enhancement this question's NULL branch would
    prioritize. It is not evidence and it is not a test.

## 8. Decision rule (numeric, written before unsealing)

`E1` is a **dimensionless lift**, the ratio of the mean nightly recall of +3-ATR movers within 20
sessions to the mean nightly recall a same-size uniform random draw from the gradeable base universe
would achieve, over §2.5's contributing nights. Null value **1.00**. Two-sided. H-074 predicts
`E1 > 1` and Haci's PASS line asks for `E1 ≥ 2`.

**MPE — `E1 ≥ 2.00`** (Haci's number, Master Hypothesis Program H4; §4.2 states the source and §11
item 2 routes the unit question), **mirror `E1 ≤ 0.50`**. **Materiality floor — `D ≥ +1.0 pp`**
(mirror `≤ −1.0 pp`). **Neither is lowered at the decision pass in any branch**, including one where
the CI excludes 1.00 and the point estimate sits at 1.9. That is what an MPE is for (rule 6).

**HISTORICALLY_CONFIRMED** requires **all** of:

1. **contributing nights ≥ 80** and **≥ 30 dated after the lock commit** (DP-21, DP-24), with ≥ 20
   for any sub-cell that is *reported*. A sub-cell below 20 is **SUPPRESSED** (counts only) and does
   not by itself make the endpoint INCONCLUSIVE; suppression restricts affirmative reporting only and
   never removes clauses 6–11's blockers;
2. **`B_t` covering ≥ 90% of the 2,405 pinned symbols, ungradeable share ≤ 10%, and the §2.6
   corroboration gate passing, on every contributing night** — mechanical gates on the statistic's
   meaning, checked per night, with violating nights non-contributing;
3. (a) `E1 ≥ 2.00` (or `≤ 0.50` on the mirror) **and** (b) `D ≥ +1.0 pp` (or `≤ −1.0 pp`);
4. the **date-clustered bootstrap 95% CI excludes 1.00**, and B1's randomization p supports it;
5. **the episode-clustered 95% CI (DP-51, §4.4) also excludes 1.00.** A primary that clears MPE on
   the date-clustered CI and not on the episode-clustered one is **INCONCLUSIVE, never CONFIRMED**;
6. **neither matched baseline runs the other way**: neither the B2 sector-matched nor the B3
   liquidity-matched lift sits **below 1.00 with its own 95% CI excluding 1.00** (§3);
7. the **as-filed `|U_t|` denominator** version of E1 also clears 2.00 (§4.3, §11 item 1);
8. the **tradeable-B** version does not sit below 1.00 with its CI excluding 1.00 (§4.3);
9. the **2-ATR and 4-ATR** versions do not sit beyond the mirror MPE in the opposite direction — a
   lift above 2 at 3 ATR while the universe *avoids* 2-ATR and 4-ATR movers is a threshold artefact,
   not discovery;
10. the point estimate sits on the **same side of 1.00 in both halves** (§6), with neither half beyond
    the mirror MPE in the opposite direction;
11. the **monthly-block stability clause** (§6): the share of qualifying monthly blocks on the same
    side of 1.00 as the full-sample estimate is **≥ 60%** (rounded up on the measured block count);
12. **BH `q ≤ 0.10`** within F8 (§7).

- **NULL:** floors and clause 2 met, **both** CIs include 1.00, **and** `E1` between 0.50 and 2.00.
  *"The candidate universe finds the market's big movers no more often than a random list of the same
  length"* is a **real finding with a direct product consequence** (§9) — it is H-074's own FAIL
  branch, Haci's *"candidate generation is the bottleneck, not ranking"* — and it is ledgered with the
  same care as a positive.
- **INCONCLUSIVE:** anything else — a date-clustered CI excluding 1.00 while the episode-clustered one
  does not (clause 5), halves on opposite sides of 1.00, a blocking companion running the other way,
  fewer than 60% of monthly blocks agreeing, `1.00 < E1 < 2.00` with a CI excluding 1.00 ("real but
  below MPE", rule 6), `D` below the materiality floor with a large-looking lift, or a CI including
  1.00 with `E1 ≥ 2.00`. **A floor shortfall is never INCONCLUSIVE** — it fires the single DP-13
  extension, then DEFERRED (§5.2).
- **What a confirmed E1 does and does not mean (binding on the report).** A CONFIRMED-positive E1
  means *"on an average night, the share of the market's +3-ATR movers already sitting in the
  candidate universe was L times the share a same-size random list would have held"*. It does **not**
  mean the picks made money; it does **not** mean the published slate beats anything (Q006, Q024); it
  does **not** mean the score ranks those movers correctly (Q027); and it does **not** mean the moves
  were **tradeable** — the tradeable companion (§4.3) is the only number that speaks to that, and it
  must be printed beside any quoted lift, together with the base rate `base_t`, the mover count `m_t`
  and the identical-3-ATR construction.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5) — it requires ≥ 30 contributing
  nights dated after this file's lock commit (DP-24, DP-21), which every contributing night here is,
  frozen in the successor manifests and never inspected earlier, reproducing the sign under the
  unmodified `eval.py`. The clause does not weaken. No subscriber-facing statement before that
  (rule 10); even then the basis is `NON_QUOTABLE` until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the candidate universe is assembled from six feeds and a hard cap — the UOA day / swing / long
bulletins, the whale-watch insider list and the bullish and two bearish projection lists
(`services/candidate_universe_builder.py:91-148`), with the screener's own `max_symbols = 40`
(`services/uoa_screener.py:351`) one reason the pool sits near 57 names. **Nothing on the platform
measures whether that pool reaches the market's movers**, and this question is the measurement. Rules
below fire **only** where §8 licenses them, and nothing subscriber-facing ships before
PROSPECTIVELY_CONFIRMED (rule 10):

- **CONFIRMED positive (lift ≥ 2, every clause clean):** (a) a Manual Trading Guide line stating the
  measured lift, with the base rate, the mover count and the tradeable-B number printed beside it;
  (b) **EN-016 (a larger candidate universe) is de-prioritized** on `research/ENHANCEMENTS.md` with
  this question's number as the reason, and the desk's effort moves to ranking and selection
  (Q027 / H-073, H-075) — that reallocation is the main consequence and it is an internal one;
  (c) an `INTERNAL_TOOL`, flag-off nightly panel reporting the running recall lift, so decay is
  caught (the H-082 pattern) rather than discovered a year later. **No subscriber-facing claim of the
  form "we find the movers"** may be made on a W20 basis (rule 12), and none at all before the W60
  restatement.
- **NULL (lift ≈ 1):** this is H-074's own FAIL branch and it is the more actionable of the two.
  **Candidate generation is the bottleneck.** (a) **EN-016 is promoted** to the top of the
  enhancement list with the measured numbers attached; (b) a brief is filed under DP-48 proposing a
  wider universe — raising `uoa_screener.max_symbols`, adding a price- and volume-screened base feed,
  or both — **with the §4.3 recall-by-source table naming which feed to widen and the
  mover-characteristics table naming what kind of name is being missed**; (c) every downstream
  selection question is reported with the sentence *"measured inside a pool with no demonstrated
  discovery advantage"*, because a ranking edge inside a pool that is not itself special is a smaller
  claim than it looks. Shipped flag-off with a byte-identical checksum on the old path and shadowed
  ≥ 20 trading days before any flip (rule 11).
- **CONFIRMED negative (lift ≤ 0.50):** the universe systematically avoids the names that move. This
  is filed to `PLATFORM_ISSUES.md` as a defect in candidate generation (DP-07) with the
  mover-characteristics table attached, the internal presentation of the universe as an
  "opportunity funnel" is suspended immediately, and a brief is written to examine the feeds'
  screens. The measurement stays here; the defect half goes to Haci.
- **A blocking companion running the other way (clauses 6–9), whatever E1 does:** the failing
  companion is reported in the verdict sentence, no guide line is written, and the specific failure
  routes — a B3 failure to EN-016's liquidity screen, a threshold artefact (clause 9) to a successor
  question on the mover definition.
- **The bear secondary, the seven source feeds and every suppressed cell license nothing on their
  own** (§4.3, §7). A striking bear result is a reason to register a bear-discovery question with its
  own primary, not a finding.
- **Nothing here licenses a claim about the picks.** Discovery is not selection (Q006), not ranking
  (Q027) and not benchmark-beating (Q024). Any restatement of this verdict that drops the word
  "universe" is wrong.
- **Q030 is in flight from this lock until its decision date, and DP-50(b) applies to the platform in
  the meantime.** There is one database, and a change to universe construction rewrites what this
  question reads. Any platform change to `services/candidate_universe_builder.py`, to
  `uoa_screener.max_symbols`, to the bulletin list sizes, to the insider-watch parameters or to which
  projection tables feed the universe is **flag-off until Q030's decision date, 2027-03-08**
  (2027-04-19 if the single DP-13 extension fires) — the PI-011 / Q010 pattern, checked before any
  fix brief is written. If such a change ships anyway it takes a dated `DATA_NOTES.md` entry naming
  the file, the date range and the ship SHA, and §5.2's window split applies (DP-06, DP-50(a)).
  **A scoring-side change does not trigger this clause** (§5.2).
- **DP-49 binds every brief this question produces:** each check handed to the **coding agent** must
  be satisfiable from the platform repo alone — the test suite, a pure-function import,
  `git show --stat`, a file diff. Anything that reads or writes a table belongs in the brief's
  verification section, addressed to the Data Steward on `$RESEARCH_DB_URL`, or to Haci where a write
  is required. Where a frozen manifest covers the affected table, the brief names that parquet as the
  before-snapshot (DP-50(c)).
- Owner: implementer. Shadow period before any flip: ≥ 20 trading days.

## 10. Known threats to validity (registrar's own list)

1. **The base universe is a stale snapshot, and the staleness only grows.** `sp500_sectors.json` was
   synced once, on 2026-05-17, and the window runs to 2027-01-26 — eight months of index additions,
   IPOs and delistings missing. The bias is **one-directional and structural**: names that listed or
   joined the indices after May 2026 are absent from `B` entirely, and those are disproportionately
   the high-momentum names a flow-led universe would find. They are excluded from `M_t` **and** from
   `U_t^B` **and** from `b_t` simultaneously (§2.4), which keeps the arithmetic coherent but removes a
   slice of the market where the engine plausibly does well. Mitigations, all disclosure rather than
   repair: the `|U_t \ B|` symbol list is printed every night; the as-filed `|U_t|` companion (clause
   7) shows what a larger draw denominator does; and §9 forbids any claim about "the market" as
   opposed to "the 2,405 names in the pinned list". **Re-syncing the blob mid-window is forbidden** —
   it would change the denominator under the experiment.
2. **The mover set overlaps itself across nights.** One 3-ATR run makes the same symbol a mover on up
   to twenty consecutive nights, and the same ~57 names recur in `U_t`. A night-clustered CI would
   treat one move as up to twenty observations. DP-51's episode-clustered CI is the answer and it is a
   **decision** clause (§8 clause 5), not a footnote; because most base symbols are continuously
   listed it is effectively a symbol-clustered bootstrap, and it is expected to be materially wider
   than CI 1. If it is not, that itself is worth reporting.
3. **ATR normalization is the match, and it is also the mechanism.** Every symbol is asked for 3 of
   its own ATRs, which is what makes candidates and non-candidates comparable — but ATR14 is
   backward-looking, so a name whose volatility is compressed at t has a mechanically nearer target.
   If the universe over-samples compressed-volatility names, part of any lift is that, not foresight.
   This is not removable without changing the hypothesis; it is disclosed, and the
   mover-characteristics table prints `ATR%` for found and missed movers so the reader can see it.
4. **A penny-and-microcap tail inflates the denominator.** `B` includes Russell 2000 names where a
   3-ATR move is routine and which no subscriber would trade; they enlarge `m_t`, depress `recall_t`,
   and make the primary conservative in a way nobody chose. The tradeable-B companion (clause 8) and
   B3's liquidity match are the two reads on it, and §9 requires the tradeable number beside any
   quoted lift.
5. **`sas_candidates` may not be exactly the universe.** A universe entry whose context build fails
   can drop out before persistence (`services/super_agent_select_service.py:735-746` guards on
   `candidates_by_symbol` and `contexts_by_symbol` membership), and such a drop would be scored as
   "the platform never found it". §2.6's `stats_json` corroboration gate at 2% is the defence; if it
   fires often, the question has a measurement problem and the gate will say so loudly rather than
   quietly deflating recall.
6. **Right-censoring is exactly where the best movers are.** Acquisitions pop and then delist. §2.2's
   rule — touched-by-t+k is a mover, not-touched-and-truncated is ungradeable — is what keeps them in
   the numerator; the count of ungradeable symbols per night is printed, and a night above 10% is
   non-contributing.
7. **Recall says nothing about ranking, sizing or tradeability.** A universe of 57 names containing
   all the movers is worthless if the score puts them last (Q027) or if the moves are ungettable
   (clause 8). §8's language clause and §9's last bullet are written to stop the leap, and this is the
   threat most likely to be committed by a reader rather than by the analysis.
8. **The forking-path surface is unusually large.** Seven source feeds × two directions × three ATR
   thresholds × two denominators is ninety-odd numbers, and only one decides. `m = 1`, a §4.3 list
   that closes at lock, and a suppression list fixed at lock are the three protections; the report is
   required to print the whole source table whatever its shape, so no feed can be selected after the
   fact.
9. **Universe-composition drift inside the window.** The universe builder, the screener cap, the
   bulletin sizes and the insider parameters are all live code. R1(d) sweeps to the lock, R3 sweeps
   between freezes, and §5.2's split rule fires on any such ship, moving the window out, never in.
10. **One database (DP-50).** A platform repair between freezes can rewrite which symbols were
    candidates on a past night. Rule 4's pinned manifests are what stands between that and a locked
    question, and R3's loud symbol-set comparison is what detects it.
11. **The prospective window may not be representative.** Ninety-two sessions is one stretch of tape,
    and rule 7's cells are expected to be thin (all six `tape_t` cells suppressed). Discovery is
    plausibly regime-dependent — a narrow tape has few movers and they are news-driven, which is
    where flow should shine — so a lift measured over one stretch is a real but narrow finding, and
    §9's language keeps it that way.
12. **A NULL here is consequential and will be argued with.** "The universe is no better than a random
    list" is a statement about the product's first stage, and the temptation at the decision pass will
    be to find a feed, a threshold or a regime cell where it isn't. The suppression list, the closed
    §4.3 list, `m = 1` and the blocking half and monthly-block clauses exist precisely so that a null
    cannot be rescued by a cell chosen afterwards.

---

## Open decisions before lock

1. **The random-draw denominator** — Options: A `n_t = |U_t ∩ B_t|`, the candidates that are actually
   in the base universe, with the as-filed `|U_t|` version as a **blocking** companion (§8 clause 7) /
   B `n_t = |U_t|` as the BACKLOG filed it. Recommendation: **A**, because a candidate outside `B`
   can never appear in `M_t`, so counting it in the draw size compares the engine against a random
   list it never drew — and requiring the as-filed version to clear 2.00 as well keeps A strictly the
   stricter test rather than the looser one. Changes: §2.1, §2.3, §4.3, §8 clause 7.
2. **"Lift MPE unit" as a standing rule** — Options: A apply `≥ 2.00` here from Haci's H4 line plus
   the `+1.0 pp` materiality floor, and route the *general* rule ("the MPE for a ratio/lift endpoint
   is a lift of 2.0 together with a stated absolute floor") to the Decision-maker as a proposed
   standing entry, since DP-44 has no ratio unit and this run writes no DP from a DEFAULTED item /
   B apply DP-20's +5.0 pp to the difference `D` and derive the lift from it. Recommendation: **A**,
   because DP-20 was set for touch rates on 40–70% bases and +5.0 pp on a 2.4% base silently demands
   a lift above 3 — a different hypothesis from the one filed. Changes: §4.2, §8 clause 3, and a
   proposed DP entry (written by the Decision-maker, not by the Registrar).
3. **The materiality floor on `D`** — Options: A require `D ≥ +1.0 pp` alongside the lift (§8 clause
   3b) / B lift only. Recommendation: **A**, because a lift of 2 over a base rate of 0.4% would mean
   the universe captures under 1% of the market's movers, and no reading of "finds major opportunities"
   survives that. Changes: §4.2, §8 clause 3.
4. **The mover's reference price and gap-throughs** — Options: A level from the pick-night close
   `C_t`, any touch in t+1..t+20 counting **including a gap through at the t+1 open**, with the
   tradeable-from-t+1-open version printed / B the tradeable framing as the primary. Recommendation:
   **A**, because H4 asks whether the platform found the name **before it moved** and a name that
   gaps overnight is the archetype of that, while §8's language clause and §9 forbid reading A as a
   tradeable claim. Changes: §2.3, §4.3, §8, §9.
5. **The base universe for the primary** — Options: A all of `B` as filed, with the tradeable-B
   version ($5 price, $5M `adv20`) printed and **blocking at lift ≥ 1.00** (§8 clause 8) / B
   tradeable-B as the primary. Recommendation: **A**, because DP-25 registers the hypothesis as
   filed and the tradeable restriction changes `b_t`, `m_t` and `e_t` together in a direction the
   desk cannot sign in advance; the blocking clause is what stops A being the looser choice.
   Changes: §2.2, §4.3, §8 clause 8.
6. **The bear direction** — Options: A bull recall is the single primary and the −3 ATR statistic is
   a fully computed secondary that decides nothing / B bull and bear as co-primaries, `m = 2`.
   Recommendation: **A**, because H-074 names one primary and files bears as "separately"; the bear
   statistic is computed identically and §9 routes a striking bear result to its own PREREG rather
   than letting it be harvested here (the Q027 / H-012 convention). Changes: §4.3, §7, §9.
7. **The sealed post-hoc panel** — Options: A request the sealed-period universe bars as **R4**, a
   droppable routed item, and print the panel once at the decision pass from the same byte-identical
   `eval.py` / B no sealed panel at all. Recommendation: **A**, because the panel is computed after
   the primary run is fixed and cannot inform any choice, and it is the only read the desk will ever
   have on whether the universe held the April–August movers — while remaining the first thing
   dropped if R2's fetch is expensive. Changes: §5.3 R4, §6.
