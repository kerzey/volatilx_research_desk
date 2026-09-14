# STEWARD — Q030 universe coverage probe (2026-09-14)

Limb 2 of the Q030 / H-074 re-entry trigger in `research/questions/DEFERRED.md`: a
trailing-session probe over every symbol in the pinned blob's `mapping` key. Counts only —
no outcome, no freeze, no manifest, no live database query (DP-50(c)).

- Blob: `4171b1a:data/sp500_sectors.json`, sha256 `c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201`, **pin match: True**, entries **2405**
  (hashed from the committed bytes via `git show`; the Windows working-tree copy is CRLF and hashes differently)
- Window `2026-06-01..2026-09-11`, daily bars, `adjustment=split`, `feed=sip`; max bars returned for any symbol: **72**
- Credentials: both present in the desk session (`research/lib/desk_env.py`)

| measure | value |
|---|---|
| symbols probed | 2405 |
| with ≥ 60 daily bars | **2346** |
| share | **97.55%** |
| gate | ≥ 90% |
| **limb 2 verdict** | **PASS** |
| zero bars | 18 |
| 1..59 bars | 41 |
| fetch errors | 0 |

### Symbols returning zero bars

```
AMWD, BK, CSGS, CTRA, CVGW, DAY, EHAB, HOLX, KFS, MCW, MMC, MPX, SBT, SLNO, THR, THRD, TSEOF, VRE
```

### Symbols returning fewer than the floor

```
ATLN:22, AVB:53, AVNS:38, BBBY:53, CCRN:34, CPRX:30, CWAN:17, EA:45, EEX:29, EQR:54, ESPR:28, FDP:19, FFIC:1, GAMB:36, GOCO:11, GTLS:31, KALV:8, KW:11, LC:14, LPRO:41, MDV:50, NFBK:34, NUVL:30, OLPX:24, PRA:18, RMAX:59, SATS:16, SCVL:9, SEM:21, SILA:21, SKYT:43, SNBR:15, STEL:21, TALK:53, TBRG:26, TMHC:37, TOI:44, TWO:59, VSCO:1, WSR:29, XOMA:29
```

Excluded symbols are **counted and named, never back-filled or imputed** (Q030 DECISIONS.md). A symbol absent here is absent from the freeze R2(iii) builds.
