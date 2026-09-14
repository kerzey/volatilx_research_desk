# STEWARD — Q032 / Q033-P2 limb (g): SPY history feasibility probe (2026-09-14)

Limb **(g)** of the Q032 / H-079 gate in `research/questions/DEFERRED.md`, shared verbatim by the
Q033 / H-081 P2 entry. The limb asks one thing: can the desk retrieve the SPY history §2.2's tape
arm is built from? It could not be attempted on 2026-09-14 because the session held no Alpaca
credentials. It has now been attempted and it succeeds.

Counts and bar dates only. **No outcome of any kind was read, no freeze was built, no manifest was
pinned, and no live database query was made** (DP-50(c)). Nothing here is a verdict on Q032.

## Credentials

Both `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` are **present** in the desk session, asserted by a
direct presence test, never assumed (the Q024 R1(d) precedent). They come from `.env.research`,
loaded by `research/lib/desk_env.py`, which returns variable **names** and never values. These are
the two credentials CLAUDE.md rule 1 already names the desk as holding; no other was sought.

## The probe

`https://data.alpaca.markets/v2/stocks/bars`, symbol `SPY`, `timeframe=1Day`, `feed=sip`,
requested `2025-01-02..2026-09-12`.

| adjustment | bars | first | last |
|---|---|---|---|
| `split` | **424** | 2025-01-02 | 2026-09-11 |
| `raw` | **424** | 2025-01-02 | 2026-09-11 |

## Against what §2.2 needs

`vol_t` is an expanding-window tercile of SPY's 20-session realised volatility over every SPY
session ≤ t and **requires ≥ 250 such sessions**, below which the night is excluded. `trend_t`
needs SPY's 200-session mean.

| requirement | needed | measured at a 2026-09-15 window start | verdict |
|---|---|---|---|
| SPY sessions strictly before the window start | ≥ 250 | **424** | **PASS** |
| sessions for the 200-session mean | ≥ 200 | **424** | **PASS** |
| split-adjusted daily bars retrievable | yes | yes | **PASS** |

The same holds at a 2026-09-21 window start (424 prior sessions). The arm is assignable from the
first session of the window, so the "first session with ≥ 250 prior SPY sessions is **never**"
finding that drove the deferral is superseded: it was a statement about `manifest_prices_v001`,
which holds 153 SPY bars from 2026-02-02, not about what the vendor can supply.

**Limb (g): PASS.** It was the only failing limb; (a)–(f) were measured and cleared on 2026-09-14
and are not re-measured here.

## One defect found while probing

`ALPACA_DATA_FEED` in `.env.research` holds a **malformed feed name** — four alphabetic characters
beginning `sip`, so a typo of `sip`. Alpaca answers it with **HTTP 400** on every request. The value
itself is not reproduced here.

It matters because `research/lib/freeze_prices.py:104` defaults `--feed` to that variable, so the
next price freeze run without an explicit `--feed` fails outright. `manifest_prices_v001` records
`feed=sip`, so the variable was either correct when that freeze ran or the flag was passed by hand.
Every probe in this report passed `--feed sip` explicitly. Filed in `research/data/DATA_NOTES.md`;
the fix is a one-character edit Haci makes in the file the desk may not read.
