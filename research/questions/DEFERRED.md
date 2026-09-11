# Deferred questions — registered as un-answerable with the data the desk holds

A question lands here when its **objective cannot be measured** from the frozen manifests, not when
it merely lacks sample size. Sample-size problems get a PREREG with a floor date (see Q002/Q003/Q004);
data problems get this file. Each entry names the exact data that would move it back into the
backlog. Nothing here may be reported, briefed or quoted in any form until that data exists.

**Opened 2026-09-10 by the registrar, registration round R1.**

## H-055 — "Leg out at the first touch of the short strike (L3) instead of holding to expiry" — and H-056's DTE recommendation

Both of these are **option-structure** questions wearing stock-path clothing, and the desk holds
**no option price history at all**. `manifest_prices_v001` contains Alpaca daily raw and
split-adjusted equity bars plus hourly equity bars including pre/post-market; there is no options
chain, no per-contract OHLC, no bid/ask, no implied volatility, no open interest history. The
platform tables do not fill the gap either: `whale_watch_ledger` is empty (0 rows, verified in
manifest_v001), `uoa_symbol_daily` carries aggregate premium and score columns but no contract-level
marks, and its `fwd_return_*` columns are degraded and banned as outcomes (DATA_NOTES; FREEZE_v001
§5). H-055's claim is that closing a vertical at the first L3 touch beats holding it to the
session-20 close; the stock path can say how often price touched L3 and how often it was back below
L3 at session 20, but it **cannot** say what the spread was worth at either moment — that depends on
time to expiry, the IV path, the strike width and the skew, and the whole point of the claim is a
comparison of two option P&Ls. H-056's second half has the same defect: mapping a target's ATR
distance to a DTE band is a recommendation about **which contract to buy**, and it cannot be
validated on a metric that contains no theta. Running either on the stock proxy alone would produce
a number that looks like a finding and is not one, which is exactly the failure mode this desk
exists to prevent. **Q002 therefore tests only the equity-path half of H-056 (unconditional speed to
target), and Q006 reports touch-then-settle at L3 as a descriptive statistic — neither may be
presented as evidence about spreads or expiry choice.** To move these back into the backlog the desk
needs, for every published pick's symbol and for the matched-control symbols, a frozen options
history covering the pick night through 60 sessions forward: per-contract daily OHLC or end-of-day
marks with bid/ask, open interest and implied volatility, for at least the strikes spanning L1–L6
and the 7–60 DTE range, from a source the Data Steward can pin with a sha256 (a paid EOD options
feed, or Alpaca's options endpoints if the subscription is extended to historical chains). With that
in hand, H-055 becomes a clean paired comparison — same spread, two exit rules — and H-056's DTE
recommendation becomes testable as realized option P&L per DTE band. Until then both stay here.
**Revisit when an options price freeze exists; no decision date can be set, because the blocker is
procurement, not time.**
