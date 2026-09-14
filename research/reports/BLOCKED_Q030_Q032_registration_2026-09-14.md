# Q030 and Q032 cannot be registered: the desk's resumption path is not implemented by its own enforcement

**2026-09-14. INTERNAL.** Every measurement these two questions were waiting for is delivered and
every lock gate reads PASS. Neither question can be registered anyway, because two pieces of
enforcement code — both off-limits to the desk under rule 15 — block the exact path the desk's own
`DEFERRED.md` entries instruct it to take.

Nothing was worked around. No hook was edited, no file untracked, no PREREG shadowed under another
name. This file records the blocker and preserves the finished registrar output so that a re-run
after the fix is a single command.

## What is ready

| artefact | state |
|---|---|
| `research/data/manifest_prices_universe_v001.json` | built, pinned, SHA-256 verified |
| `research/reports/STEWARD_Q030_universe_coverage_probe.md` | delivered — 97.55% vs the 90% gate |
| `research/reports/STEWARD_Q030_counts_dryrun.md` | delivered — R2(iii), `m_t ≥ 1` never binds |
| `research/reports/STEWARD_Q032_spy_history_probe.md` | delivered — 424 SPY bars vs 250 needed |
| `research/reports/STEWARD_Q032_limbs_true_partition.md` | delivered — all three rate limbs PASS |
| Q030 lock-or-DEFER gate | **PASS** on all three limbs |
| Q032 lock-or-DEFER gate | **PASS** on all three rate limbs |

Committed in `b01ff2a`. None of it is blocked; none of it needs redoing.

## The blocker, in two layers

Both questions sit at `state.json` = **`DEFERRED`**, with a **tracked but never-locked** `PREREG.md`
— committed on 2026-09-14 purely as the record of the deferral, exactly as their `DEFERRED.md`
entries say ("Both files are preserved exactly as drafted"). Neither ever reached `PREREG_LOCKED`.

**Layer 1 — `.claude/hooks/guard_write.py:76-85`.** `is_locked_prereg()` decides lock status from
git tracking alone:

```python
def is_locked_prereg(root: str, rel: str) -> bool:
    """A PREREG.md that is already committed is locked; only a new question dir may be written."""
    if not rel.endswith("PREREG.md"):
        return False
    out = subprocess.check_output(["git", "-C", root, "ls-files", "--error-unmatch", rel], ...)
    return bool(out.strip())
```

Tracked ⇒ locked. It never consults `state.json`, and it is an **absolute rule with no `DESK_ADMIN`
escape** (`:101-107`). A committed *deferred draft* is therefore indistinguishable from a locked
pre-registration, and `@registrar apply` is refused on its first edit.

**Layer 2 — `research/lib/controller.py:24`.** `DEFERRED` is in `TERMINAL`:

```python
TERMINAL = {"NULL", "INCONCLUSIVE", "REJECTED", "DEFERRED"}
```

`ORDER` contains no `DEFERRED`, so there is no transition *out* of it. Even with layer 1 fixed, the
question cannot legally walk back to `PREREG_DRAFT` to be applied and then locked.

**The conflict.** Both `DEFERRED.md` entries end with "the question **resumes at
`@registrar apply Q030`** / `apply Q032` when the trigger below is met", and both were written by
the desk under DP-40..48. `research/lib/desk_queue.py` agrees — its `lifted_deferrals()` surfaces
both as `RESUME QNNN` at the head of the work list, and `board.py` §8 prints them. So the queue, the
board and both deferral records all instruct a path that the hook and the controller refuse. The
desk documented a resumption route it never implemented. This is the first time that route has been
exercised: Q030 and Q032 are the first deferrals whose triggers have ever been met.

## What this is not

It is not a reason to renumber. Both entries state that the question number is **consumed and not
reused**, and a successor would discard 13 and 16 settled decision items plus the corrections
already folded into them. It is also not a reason to reach for `git rm --cached`: that dodges an
enforcement hook by a side door rather than fixing it, and rule 15 reserves both files for Haci.

## What Haci needs to decide

The desk has no legal move here. Two files must change, and both are his:

**(1) `.claude/hooks/guard_write.py`** — make the lock test consult the controller, not git. A
PREREG is locked when its question has actually reached `PREREG_LOCKED`:

```python
def is_locked_prereg(root: str, rel: str) -> bool:
    """A PREREG.md is locked once its question has reached PREREG_LOCKED — tracking is not lock."""
    if not rel.endswith("PREREG.md"):
        return False
    try:
        out = subprocess.check_output(["git", "-C", root, "ls-files", "--error-unmatch", rel],
                                      text=True, stderr=subprocess.DEVNULL)
        if not out.strip():
            return False
    except Exception:
        return False
    try:
        st = json.loads(Path(root, Path(rel).parent, "state.json").read_text())
        seen = {h.get("state") for h in st.get("history", [])} | {st.get("state")}
        return "PREREG_LOCKED" in seen          # deferred drafts are tracked but never locked
    except Exception:
        return True                             # no readable state: fail closed, stay locked
```

This keeps the guarantee that matters — a question that was ever locked can never be edited — and
stops a deferred draft being treated as one. It fails closed when `state.json` is missing or
unreadable.

**(2) `research/lib/controller.py`** — give `DEFERRED` a documented way back. The narrow form: allow
`DEFERRED → PREREG_DRAFT` only, only with `--by desk`, and only when the question's `DEFERRED.md`
entry carries a `TRIGGER MET` line (the condition `desk_queue.lifted_deferrals()` already computes).
That keeps `DEFERRED` terminal for every question whose trigger has not been measured away.

Both are maintenance edits, not research decisions, and neither weakens a lock. If you would rather
not touch enforcement at all, the alternative is to accept that a met trigger cannot revive a
deferred question and to say so in `DEFERRED.md` — but then the resumption sentences in Q030's,
Q032's and Q033's entries, the `RESUME` bucket in `desk_queue.py` and the board line are all wrong
and should come out.

## After the fix, the desk finishes in one pass

Everything the registrar decided for Q030 is settled and is reproduced below verbatim, so `apply`
becomes mechanical. Q032's registrar output is appended when it reports.

### Q030 — settled, ready to paste

**§2.2 ATR smoothing, fixed as Wilder** (the under-specification found while building the dry run):

> **`ATR_{s,t}` = Wilder-smoothed ATR14 on split-adjusted bars dated ≤ t**, fixed at lock (DP-26):
> `TR_u = max(H_u − L_u, |H_u − C_{u−1}|, |L_u − C_{u−1}|)`, smoothed by
> `ATR_u = ATR_{u−1} + (TR_u − ATR_{u−1}) / 14` — `alpha = 1/14`, `adjust=False`, `min_periods=14`,
> byte-for-byte the construction `research/lib/q030_counts_dryrun.py` used for R2(iii). Simple-mean
> ATR14 is not used anywhere in this question. §2.2(a)'s ≥ 60-bar requirement decays the seeding
> transient by `(13/14)^46 ≈ 0.036` before any `T_{s,t}` is set. Never the platform's `atr_pct`
> (corrupted around splits, PI-003).

Reasons recorded: every count this lock rests on was measured under Wilder, so simple mean would
lock a schedule calibrated on a mover level `eval.py` would not compute; the choice is not
outcome-informed, so DP-26 holds; the platform's own ATR helpers are simple means, but §2.2 already
refuses platform ATR outright and 2,405 base symbols have no platform ATR at all.

**Schedule — re-verified session by session from a 2026-09-14 lock; nothing moves.**

```
decision_date: 2027-04-12 (Monday) · extension_date: 2027-05-24 (Monday; DP-13's single
automatic extension, then DEFERRED) · hard_stop: 2027-05-24 · rule: exposure-driven ·
extended: false · window: pick nights 2026-09-15 .. 2027-03-05 = 119 elapsed sessions
(extended: .. 2027-04-19, 149) · planning rate: 0.6761 contributing nights/elapsed session
(STEWARD_Q027_exposure.md, borrowed lower bound; Q030's own measured 0.9412 deliberately NOT
used — it moves the date in) · maturity: 20 sessions · floors: >= 80 contributing nights
(binds at session 119), >= 30 post-lock (session 45 = 2026-11-16, non-binding), >= 20 per
reported sub-cell · ceiling: 6.9 months (extended 8.3) vs DP-43's 12 = 2027-09-14 ·
interim: none (DP-58 not registered) · lock-or-DEFER gate: PASS on all three limbs
```

Holidays used: 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26 (Good Friday;
Easter 2027 is 03-28). Memorial Day 2027 is 05-31, so 2027-05-24 is a session. Session 119 =
2027-03-05 (Fri); t+20 = 2027-04-05; +1 week → Monday 2027-04-12. Extension session 149 =
2027-04-19; t+20 = 2027-05-17; +1 week → Monday 2027-05-24.

**DP-58 — no interim look is registered.** Q030's primary is out of scope, on three grounds:

1. **The endpoint family is not the one DP-58 names.** DP-58 admits "a touch-rate or per-trade ATR
   contrast". E1 is a dimensionless **ratio of means** with null 1.00 and a **multiplicative** MPE of
   2.00 — the touch sits inside the *definition of the mover set* over 2,405 base symbols, not in the
   rate of a traded target from an entry basis, and there is no trade. DECISIONS item 2 already
   refused to import DP-20's touch-rate unit for this reason: additive touch-rate policy on a 2.4%
   base silently demands a lift above 3 and re-files the hypothesis.
2. **The boundary is undefined for a compound MPE.** §8 clause 3 requires **both** `E1 ≥ 2.00` **and**
   `D ≥ +1.0 pp`. DP-58's boundary names "the MPE", singular. Registering an interim would mean
   deciding at lock whether the two CIs must exclude 2.00, or +1.0 pp, or both, and whether `D`'s own
   CI pair enters the O'Brien–Fleming boundary. **That is writing policy, not applying it**, and
   DP-40 puts it outside an autonomous registrar's reach.
3. Supporting only: the 60th contributing night lands at session 89 ≈ 2027-01-21, interim decision
   ≈ 2027-03-01 — about six weeks early — while DP-58 waives no floor, so clauses 6–11 must come
   clean at 60 nights too and the fixed look pays α 0.05 → 0.048 regardless.

§5.2 and §8 each take one sentence: *"No interim look is registered (DP-58). The primary is a ratio
endpoint, outside DP-58's touch-rate / per-trade-ATR scope, and its compound MPE has no defined
boundary under that entry; `eval.py` is run once, at the decision pass."*

**This is a finding about DP-58, not only about Q030.** The policy filed this morning names its
scope as "touch-rate or per-trade ATR contrast" and has no entry for a ratio endpoint or a compound
MPE. Q030 is the first question to test that edge and it falls outside. If interim looks are wanted
for ratio endpoints, DP-58 needs a second clause — which is Haci's call, not the desk's.

**What `apply` would fold** (all settled, none on disk): header gate line and manifest reference;
items 2–3 into §1/§4.2/§8 cl.3 (compound MPE, DP-20 considered and not applied); item 1 into
§2.1/§2.3/§4.3/§8 cl.7 (`n_t = |U_t ∩ B_t|`, as-filed `|U_t|` blocking); items 4–5 and the Wilder
clause into §2.2; Correction 6 into §2.4/§4.3 (`payload_disabled_runs` retained, flagged, counted);
Correction 7 + item 11 into §4.3 (suppression revised once from R2(iii), then closed; later R1(b)/(c)
may only add); Correction 1 into §5.1 (0.6761 as a borrowed lower bound, the 8-session cushion
struck, Q030's own 0.9412 recorded as measured-not-used, and the "nothing about `B` has ever been
measured" paragraph replaced by `b_t` 2342/2355/2375, `n_t` 45/61/68, `m_t` 332/886/1328, `m_t = 0`
on 0 of 51 nights, coverage 97.80–98.54%, ungradeable ≤ 0.76%); the schedule block into §5.2 with
2027-01-26 → 2027-03-05 and 2027-03-08 → 2027-04-12 and 2027-04-19 → 2027-05-24 propagated through
§6, §7, §9 (including Correction 4's DP-50(b) flag-off dates) and §10 (threat 1's window, threat 11's
"ninety-two sessions" → 119); Correction 2 + 3 and the R2 status into §5.3, recording R2 as
**delivered in part** — `manifest_prices_universe_v001` covers **history only and carries no
registered forward night**, and R2's forward cut is still owed through 2027-04-05, delivered before
Monday 2027-04-12, extension cut through 2027-05-17 before Monday 2027-05-24; §11 → `## Decisions
before lock`; and BACKLOG flipping H-074 from deferred to registered as Q030.

### Q032 — settled, ready to paste

**Schedule, built from scratch by item 14's method. Floor D binds, and the extension does not fit.**

| floor | rate (measured, t+40 basis) | sessions | first reached |
|---|---|---:|---|
| **A** 80 contributing nights | 0.5536 | 145 | 2027-04-13 |
| **B** 20 rarer-arm nights | 0.2589 | 78 | 2027-01-05 |
| **C** 30 post-lock nights (DP-24) | 0.5536 | 55 | 2026-12-01 |
| **D** ≥ 5 gate-counting tape-episodes per arm | 0.0268 | **187** | **2027-06-11 — BINDS** |

```
Window:        pick nights 2026-09-15 .. 2027-06-11 inclusive = 187 elapsed sessions
Binding floor: D (5 gate-counting tape-episodes in the rarer arm) at 0.0268/session
               - a change from the proxy reading, where floor A bound
Maturity:      + 40 sessions        -> 2027-08-10 (Tue)
Freeze margin: + one calendar week  -> 2027-08-17 (Tue)
Decision date: first Monday on or after -> Monday 2027-08-23   (11.3 months from lock)
Extension:     NONE ADMISSIBLE
Hard stop:     Monday 2027-08-23
rule:          exposure-driven
```

**Q032 would lock without a rescue, and this is the most important thing on this page.** Item 14
fixes DP-13's extension at +30 sessions. Session 217 = 2027-07-27; +40 maturity = 2027-09-22; +one
week = 2027-09-29; first Monday = **2027-10-04 — past DP-43's 12-month ceiling of 2027-09-14**. Item
14's own clause then fires: over 12 months from the lock → DEFERRED. So **any gate short at
2027-08-23 ends the question outright, with no second run.** Floor D is exactly the limb most likely
to be short: it is measured at 3 absolute episodes on the historical panel and needs 5. A rarer arm
that arrives at 4 episodes kills Q032 with no recourse.

The registrar did **not** trim floor D and did **not** stretch the window to the ceiling to
manufacture headroom. Both were available and both are wrong — item 14 derives the window end from
the floors, not from the ceiling, and DP-53 says a later date is not more valid for being later.
Whether a DP-13 extension *truncated* at the ceiling (session 206, decision Monday 2027-09-13) is
admissible where item 14's fixed +30 is not, is a new question DECISIONS.md does not cover. It is
drafted on the stricter reading (no extension) and **routed to the Decision-maker**.

Two holidays are missing from DECISIONS' calendar list, both inside the maturity run and both used
above: **2027-07-05** and **2027-09-06**.

**Ceiling re-solve (Correction 3, from the actual 2026-09-14 lock, not inherited).** Latest
admissible decision Monday 2027-09-13 → −1 week = 2027-09-06 (Labor Day) → last session ≤ that is
2027-09-03 → −40 sessions = 2027-07-12 = session 206. Inequalities = floors ÷ 206 = **0.39 / 0.10 /
0.025**; the as-filed 0.40 / 0.10 / 0.025 is stricter and governs (DP-45). Measured **0.5536 /
0.2589 / 0.0268** — all three PASS on both readings. Floor D's window ends at session 187 of an
admissible 206: **19 sessions of margin, 9%**.

**The rarer-arm flip — the registered fix is to stop naming the rarer arm at all.** Sixteen places
presume HOSTILE is rarer. §5.1's header parenthesis "rarer-arm (expected: HOSTILE)" is struck rather
than re-pointed at BENIGN. Both floors are already symmetric (§5 "≥ 20 per arm", §8 clause 2 "≥ 5
episodes per arm"), so no decision rule changes; only *scheduling* needs a rate, and it takes the
slower of the two measured arms (BENIGN 0.2589 < HOSTILE 0.2946), with an explicit line that the
historical identification of BENIGN as rarer is a scheduling input on a panel that is not the
registered window, never a registered expectation about 2026-09..2027-06. §5.1's entire one-sided-
bound apparatus is struck: the true partition is measured and no bound is left to run in a
direction. Item 12's bound direction was *right* — SMA50-only HOSTILE was a lower bound, true
HOSTILE grew 22 → 33 and overtook BENIGN — and that is recorded as a closed prediction, not carried
forward as machinery. §3 B1, §8 clause 8 and §9 are unaffected: the pooled arm is HOSTILE by
construction (8 non-BENIGN cells against BENIGN's 2), so the composition guard stays on HOSTILE
whichever arm is rarer.

**§8 clause 8 — the composition guard is likely to fire, and §10 must say so.** On the matured
panel **UP × HIGH carries 30 of 33 HOSTILE nights = 90.9%** against clause 8's 80% threshold, and
only 4 of 9 cells are observed (MIXED/HIGH 3, UP/HIGH 30, UP/LOW 16, UP/MID 13). The panel is not
the registered window so the guard does not fire, but a CONFIRMED `G` would then be restated as a
finding about **high realised volatility inside an uptrend**, not about hostile tape: on this
history DOWN never occurs and MIXED barely does, so the partition collapses to a volatility split
within a single trend state. Every §9 sentence would have to name UP × HIGH, and the
`WORKS_IN_BENIGN` lane rule would read "calm-to-normal vol in an uptrend beats high vol in an
uptrend" — materially narrower than H-079 filed. That belongs in §10 as its own numbered threat.
BENIGN's own split (UP/LOW 16, UP/MID 13 — 55/45) shows BENIGN is *not* one cell in disguise.
Item 7's single permitted revision is exercised now and closed: add the five never-observed cells
(DOWN×{LOW,MID,HIGH}, MIXED×{LOW,MID}) and MIXED/HIGH to §4.3's SUPPRESSED list. Nothing comes off.

**Limb (f) is still owed — the last unmeasured limb of the lock gate.** The DP-50(a)/(b) commit
sweep and the v1.7 promotion check have not been re-run; owed by the **Data Steward** before the
lock commit. Scope: any change since manifest SHA `fa70688` / platform HEAD `d19c9a9` to the SAS
weights, timeframe multipliers, `qualification_threshold`, `publication_floor`,
`bear_publish_threshold`, `max_output_cap`, `min_completeness`, the ATR-elite caps, the GEX offset,
the scoring enable-flags, the lane-plan writer, or `services/market_regime/scorer.py` (C1 only) —
**with an explicit answer even when it is "none"** — plus whether v1.7 is scheduled to ship inside
**2026-09-15..2027-08-23**. That is now the tightest DP-50(b) flag-off window on the board, ahead of
Q031's 2027-06-07. The 2026-09-14 "NONE" was an absence of a schedule at a different HEAD, not a
clearance.

**DP-58 — declined, and the declination is itself registered.** `G` **is** in scope: a
BENIGN−HOSTILE contrast of control-adjusted L3-touch excess with MPE ±10.0 pp is a touch-rate
contrast. The reason to decline is arithmetic:

- 60 contributing nights at 0.5536/session arrives at **session 109 = 2027-02-19**.
- At session 109 the rarer arm projects `0.0268 × 109 =` **2.9 gate-counting tape-episodes**,
  against §8 clause 2's gate of **≥ 5 per arm**. DP-58 waives no floor and no gate.
- So **the interim can never declare CONFIRMED** — clause 2 fails by construction at 60 nights, and
  since DP-58 forbids stopping for futility, "continue" is the only outcome it can ever produce.
- It would still cost the fixed look α 0.050 → 0.048, for a zero-probability chance of stopping.
- Reinforcing: DP-58 requires the DP-51 episode-clustered CI to exclude the MPE, and resampling ~3
  episodes in one arm is degenerate, not conservative.

§5.2 and §8 each take one sentence: *"DP-58 is in scope and is deliberately not registered; at 60
contributing nights the rarer arm projects 2.9 gate-counting tape-episodes against clause 2's 5, so
the interim could return only 'continue' while spending α on the fixed look. No interim looks."*

**Sections folded once writable:** header manifests + `**Decisions:** DECISIONS.md`; §1/§2.1 window
dates; §2.2 rarer-arm neutrality + guard forecast; §2.5 the 250-session exclusion now provably 0;
§4.2 unchanged; §4.3 suppression revision (6 cells added, closed) + Correction 4's matured-night
counts; §5 floors + the DP-58 declination; §5.1 rebuilt on measured rates (**item 3's 0.6620 cap does
not bind — 0.5536 is slower, so the measured rate is used unmodified**); §5.2 rebuilt whole; §5.3 R1
CLOSED / R2 revived with the SPY-from-2025-01-02 and t+40 riders; §6 halves re-cut by the registered
session-index rule to **Half A 1–94, Half B 95–187**; §7 F2 → 17 and F1 → 28 as `G` rejoins; §8
clauses 1–2 (no extension behind the gate), 8, + the DP-58 line; §9 DP-50(b) flag-off to 2027-08-23
and the UP×HIGH naming consequence; §10 threats 1, 3 and 11 rewritten plus a new composition threat;
§11 replaced by a `## Decisions before lock` block naming R1(f), R2 and the truncated-extension
question routed to the Decision-maker.

**Owed elsewhere, flagged and not touched:** `research/BACKLOG.md` H-079 still reads "DEFERRAL
LIFTED; awaiting re-registration"; `research/questions/DEFERRED.md` still carries the Q032 entry;
`state.json` is still `DEFERRED`; and **Q033's §7 correction-set counts**, cut to F1 28 / F2 17 while
Q032 was deferred, go back to **F1 29 / F2 18** when `G` rejoins. Q033 is unlocked, so that is a live
edit someone owes.

## DP-58 did not apply to either of the first two questions that tested it

This is a finding about the policy filed this morning, not about these two questions.

- **Q030** falls outside its scope: the primary is a dimensionless **ratio of means** (null 1.00,
  multiplicative MPE 2.00) with a **compound** MPE (`E1 ≥ 2.00` **and** `D ≥ +1.0 pp`). DP-58 names
  "touch-rate or per-trade ATR contrast" and speaks of "the MPE", singular.
- **Q032** is inside its scope and is still inert there: the binding constraint is **how many times
  the tape changes state**, not how many nights accumulate, so an interim triggered on a night count
  is blind to the gate that actually binds and can only ever return "continue".

The general lesson is that **a night-count trigger is only meaningful when nights are the binding
floor.** Where an episode, cell or arm floor binds later than the night floor, a 60-night interim
spends α and can return nothing. If DP-58 is to earn its place it likely needs a scope clause for
ratio and compound-MPE endpoints, and a clause placing the interim where **every** registered gate
is reachable rather than at a fixed 60 nights. That is Haci's call; the desk should not widen a
policy on its own to make its own questions fit.

## Re-run after the fix

```
@registrar apply Q030      # then decision-maker record, then controller PREREG_LOCKED --by desk
@registrar apply Q032
```

Both Steward deliveries and the freeze stand; nothing above needs re-measuring.
