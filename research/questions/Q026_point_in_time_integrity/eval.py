#!/usr/bin/env python3
"""Q026 point_in_time_integrity -- the leakage register, written once from PREREG.md sec 4.

PREREG    research/questions/Q026_point_in_time_integrity/PREREG.md
          commit 32566fae37ce932812af9fa63e7eb5b30561c2e1
          sha256 c857dad682d004b6550db9760dd2e7bd3e4374cfe59fd88cca7b9a6848487933
DECISIONS research/questions/Q026_point_in_time_integrity/DECISIONS.md (8 items, all DECIDED)
Data      research/data/manifest_v001.json        (11 selection tables, 107,185 rows)
          research/data/manifest_prices_v001.json (Channel D only, 584,231 rows)
          exclusions_v001 / v002 / v003 -- each question's own cited file (sec 2.3, DP-22)
Attribution  the read-only platform repo at the FROZEN SHA
          fa70688bc252d14f8d67e371afafc194731c324e, read with `git show fa70688:<path>`,
          never HEAD (sec 4.3, sec 10.6, decision 8). The SHA read is printed in the register.
Type      DIAGNOSTIC / census. PASS / FAIL. No MPE, no BH, no CI, no p-value (sec 4.7).
          Every number is NON_QUOTABLE (rule 12) and carries the label HISTORICAL_ONLY (sec 9).

NO LIVE QUERY OF ANY KIND (rule 4, DP-50(c), decision 4). This module imports no database
driver and no desk db helper; it reads sha256-pinned parquet, pinned JSON, the pinned PREREG
texts, and the platform repo at one frozen SHA. Nothing else.

Written by:  Researcher, 2026-09-14, from sec 4 only, before seeing a single frozen row
             (decision 5, sec 10.10). Run by: the Data Steward, once, on 2026-09-21 (sec 5.4).
Run:         see RUNBOOK.md.  Default output: research/reports/KT_REGISTER_manifest_v001.md
             plus research/questions/Q026_point_in_time_integrity/results/*.
Re-runs at every subsequent freeze with a BYTE-IDENTICAL script (sec 9, decision 3): every
path is an argument, nothing about v001 is hard-coded in the logic.

AMENDMENT GATE -- RESOLVED 2026-09-14.  sec 4.0 left the decision-time boundary for
same-evening batch writes unresolved (AMENDMENTS.md 2026-09-14, A1).  The decision-maker
settled it by dated amendment (autonomous, DP-40): DECISION_TIME_RULE = "R2_SAME_EVENING",
boundary(N) = 23:59:59.999999 ET on N.  The Researcher transcribed the settled constant and
added the A1r reporting on 2026-09-14; the Researcher did not choose the rule and the Steward
does not choose it at run time (rule 9; sec 10.10 -- a gap in sec 4 is fixed by a dated
amendment BEFORE the run, never during it).  The preflight gate stays in place: an unset rule,
an unknown rule id, or a rule without its amendment citation still aborts before Gate 0.

A1r (AMENDMENTS.md 2026-09-14) adds reporting only, and changes no threshold, filter, exit
rule or decision rule: Channel A carries n_W_gt_R1/R2/R3, the two band columns and n_L_gt_U
under all three rules, totalled per table / month / overall; the register carries a
`Boundary sensitivity` section (M, MM, U, questions_touched, both STOP-THE-DESK limbs under
each rule) headed DESCRIPTIVE -- DOES NOT DECIDE; the header, summary.json and the verdict
sentence name the rule, its amendment and A12's R3 fallback count.  sec 8 is computed under
R2_SAME_EVENING alone.  The sensitivity block may never select a rule after looking (rule 9).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, date, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

QDIR = Path(__file__).resolve().parent
ROOT = QDIR.parents[2]
ET = ZoneInfo("America/New_York")
UTC = timezone.utc

# --------------------------------------------------------------------------------------------
# sec 4.0 -- the decision-time boundary.  RESOLVED by dated amendment (AMENDMENTS.md A1,
# 2026-09-14; DECISIONS.md "Amendments after lock"), decision-maker, autonomous, DP-40.
#
#   R1_1605_LITERAL  boundary(N) = 16:05 ET on N                      -- sec 4.0 as written
#   R2_SAME_EVENING  boundary(N) = 23:59:59.999999 ET on N            -- FREEZE_v001 sec 7's
#                    "created_at/updated_at cluster same trading_date evening" reading   <-- IN FORCE
#   R3_NEXT_OPEN     boundary(N) = 09:30 ET on the next NYSE session  -- DP-04 / the criterion
#                    exclusions_v001..v003 and Gate 0(a) already use
#
# The three readings give different verdicts (see AMENDMENTS.md A1).  The registrar /
# decision-maker set this constant by a dated amendment before the run; neither the Researcher
# nor the Steward chooses it, and it is never changed after the register exists (rule 9: a
# different boundary after the fact is a look, and is a successor question).
DECISION_TIME_RULE = "R2_SAME_EVENING"
DECISION_TIME_RULE_AMENDMENT = ("AMENDMENTS.md 2026-09-14 A1 RESOLVED: R2_SAME_EVENING "
    "(decision-maker, autonomous, DP-40; boundary(N) = 23:59:59.999999 ET on N)")

RULE_IDS = ("R1_1605_LITERAL", "R2_SAME_EVENING", "R3_NEXT_OPEN")
RULE_SHORT = {"R1_1605_LITERAL": "R1", "R2_SAME_EVENING": "R2", "R3_NEXT_OPEN": "R3"}
RULE_BOUNDARY_TEXT = {
    "R1_1605_LITERAL": "boundary(N) = 16:05 ET on N (sec 4.0 as written)",
    "R2_SAME_EVENING": "boundary(N) = 23:59:59.999999 ET on N (a write is late when it lands "
                       "on a later ET calendar day)",
    "R3_NEXT_OPEN": "boundary(N) = 09:30 ET on the next NYSE session after N",
}
# A1r: the verbatim heading the sensitivity block must carry.
SENSITIVITY_HEADING = ("DESCRIPTIVE -- DOES NOT DECIDE. The verdict is computed under "
                       "R2_SAME_EVENING only (AMENDMENTS.md 2026-09-14, A1).")
# A1r / R2 blind spot: the tables sec 10.2 records as having no independent count, i.e. no
# Channel C corroboration.  For these the 16:05..23:59:59 ET band rests on attribution alone.
NO_INDEPENDENT_COUNT_TABLES = ("uoa_symbol", "gex_symbol", "projection_bull",
                               "projection_bear_v2", "conviction_monitor", "market_regime")

# --------------------------------------------------------------------------------------------
# Pins.  Every one of these is checked before anything is read (sec 2.2, decision 8).
PREREG_SHA256 = "c857dad682d004b6550db9760dd2e7bd3e4374cfe59fd88cca7b9a6848487933"
PREREG_COMMIT = "32566fae37ce932812af9fa63e7eb5b30561c2e1"
PLATFORM_SHA = "fa70688bc252d14f8d67e371afafc194731c324e"
PLATFORM_SHA_SHORT = "fa70688"

# sec 2.2 -- THE AUTHORITATIVE QUESTION LIST, TRANSCRIBED.  21 ids.  The script fails loudly,
# with the diff, and produces no register, if this transcription does not match PREREG sec 2.2.
QUESTION_IDS_IN = (
    "Q002", "Q003", "Q004", "Q006", "Q007", "Q008", "Q009", "Q010", "Q011", "Q012",
    "Q013", "Q014", "Q015", "Q016", "Q018", "Q019", "Q021", "Q022", "Q023", "Q024",
    "Q005",
)
QUESTION_IDS_OUT = ("Q001", "Q017", "Q020", "Q025")
# sec 2.2 decision 1 -- the four prospective-window questions whose out-of-window nights
# produce ADVISORY rows.  ADVISORY enters neither M nor U nor either STOP-THE-DESK limb.
ADVISORY_QUESTIONS = ("Q010", "Q022", "Q023", "Q024")

# sec 8 -- the five core selection columns (STOP-THE-DESK limb (a)).
CORE_SELECTION_COLUMNS = ("overall_score", "qualified", "selected_rank",
                          "dominant_direction", "best_timeframe")
# sec 4.4 -- the publication predicate columns a Channel C disagreement makes MATERIAL.
PUBLICATION_PREDICATE_COLUMNS = ("qualified", "selected_rank")

# sec 6 -- the three registered boundaries and the in-sample cut.
BOUNDARIES = {"catalyst_layer_2026-06-01": date(2026, 6, 1),
              "regime_point_in_time_2026-06-09": date(2026, 6, 9),
              "uoa_fwd_return_resumption_2026-07-06": date(2026, 7, 6)}
LOW_N_FLOOR = 20   # sec 5.1 -- any per-night/per-month cell below this is labelled, no trend read

# sec 4.1 / sec 3 -- Gate 0 targets.  Fixed in sec 3 BEFORE the run; never relaxed (sec 8).
# The derivations below use no hard-coded date list; these are the targets the derived sets
# are checked against.
GATE0_RERUN_NIGHTS = ("2026-04-02", "2026-04-24", "2026-05-15", "2026-07-02")
GATE0_MANUAL_RUN_NIGHTS = ("2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14", "2026-07-06")
GATE0_REGIME_LATE_NIGHT = "2026-07-06"
GATE0_REGIME_BACKFILL_BEFORE = date(2026, 6, 9)
GATE0_LATE_BLOCK_TABLES = ("uoa_symbol", "gex_symbol", "projection_bull")
GATE0_LATE_BLOCK_RANGE = (date(2026, 1, 7), date(2026, 3, 20))
GATE0_LATE_BLOCK_MIN_NIGHTS = 20          # AMENDMENTS.md A5 (KT_AUDIT sec 3 measures 42-45)
GATE0_GEX_APPEND_NIGHTS = ("2026-05-13", "2026-05-14", "2026-05-15")
GATE0_STATS_JSON_NIGHT = "2026-06-26"
GATE0_HOURS_RERUN = 12.0                  # sec 4.1(a), given: benign nights top out at 6.8h
GATE0_HOURS_LATE_BLOCK = 12.0             # AMENDMENTS.md A5
GATE0_HOURS_SPREAD = 12.0                 # AMENDMENTS.md A5 (KT_AUDIT sec 2: 21-51h)
GATE0_TABLES_EXPECTED = 11                # sec 3 B2 -- FREEZE_v001 sec 7's 11-row table

# sec 4.3 -- the documented reconstruction (Q014 sec 2.1) and its verification (decision 2).
OI_MULT_SET = (0.90, 1.00, 1.05, 1.10)    # uoa_screener.py:2223-2232 at fa70688
RECONSTRUCTION_RTOL = 1e-6                # decision 2, fixed here

# AMENDMENTS.md 2026-09-14, A6 RIDER.  The closed divisor set above is a transcription of the
# code at fa70688.  It is verified at run time, literal by literal, at the cited line range.
# If ANY of the four is not there the check cannot be evaluated: by decision 2's own failure
# branch the reconstruction tuple is MATERIAL (not mitigated, not skipped), and the withdrawal
# is printed in the register with A9's withdrawals (sec 10.6).
OI_MULT_SET_CITATION = dict(path="services/uoa_screener.py", lines=(2223, 2232),
                            literals=tuple("oi_mult = %.2f" % m for m in OI_MULT_SET),
                            key_prefix="A6_OI_MULT_SET")

# --------------------------------------------------------------------------------------------
# sec 4.3 -- ATTRIBUTED LATE-WRITE PATHS.  A (table, column) whose late-write path is
# attributable from the platform repo at fa70688 or from a manifest/exclusions correction is
# MATERIAL on the nights the predicate names, whatever the row timestamps say.
# Every repo-sourced entry carries the exact line range and the literal the script must find at
# that range in `git show fa70688:<path>`; if the literal is not there the entry is WITHDRAWN,
# the tuple is not attributed, and the withdrawal is printed in the register (sec 10.6).
ATTRIBUTION = [
    dict(id="A_REGIME_BACKFILL", table="market_regime", columns=["*"],
         nights="trading_date <= 2026-06-08", source="manifest_v001.availability.market_regime",
         repo=None,
         note="wholesale missing-then-backfilled history, written 2026-06-02/06-08 (PI-005); "
              "no point-in-time row exists for any night before 2026-06-09"),
    dict(id="A_UOA_OI_LAG1", table="uoa_symbol",
         columns=["oi_confirm_ratio", "oi_confirm_mult", "oi_confirm_score",
                  "oi_confirmed_contracts", "oi_confirm_total_contracts"],
         nights="*", source="manifest_v001.availability.uoa_symbol (declared lag 1)",
         repo=dict(path="services/uoa_screener.py", lines=(2231, 2235),
                   literal="sym_row.oi_confirm_ratio = float(oi_ratio)"),
         note="next-morning OI confirmation pass; declared lag_sessions 1 for any *_oi_* column"),
    dict(id="A_UOA_SCORE_MUT", table="uoa_symbol", columns=["score_swing", "score_long"],
         nights="*", source="PI-013",
         repo=dict(path="services/uoa_screener.py", lines=(2236, 2239),
                   literal="sym_row.score_swing = float(sym_row.score_swing) * oi_mult"),
         note="mutated in place by the next-morning OI pass; the frozen cell is not the 16:05 "
              "value.  Q014 reads it through the sec 4.3 reconstruction (MATERIAL_MITIGATED)"),
    dict(id="A_UOA_FWD", table="uoa_symbol",
         columns=["fwd_return_1d_pct", "fwd_return_3d_pct", "fwd_return_5d_pct",
                  "fwd_return_7d_pct", "fwd_return_14d_pct", "fwd_return_30d_pct",
                  "fwd_mfe_1d_pct", "fwd_mae_1d_pct"],
         nights="*", source="PI-001 / FREEZE_v001 sec 5",
         repo=dict(path="services/uoa_screener.py", lines=(151, 160),
                   literal="_ALL_OUTCOME_COLUMNS = ("),
         note="forward-outcome backfill; outcome columns, banned as features by every PREREG"),
]

# sec 4.3 INDETERMINATE resolution step.  A table resolves only where the code at fa70688 names
# a CLOSED set of columns the later pass writes.  Closure is a transcription with its evidence;
# the script verifies each cited literal at fa70688 and withdraws the closure if it is absent.
# Every table without an entry here leaves its INDETERMINATE tuples CONTAMINATION_UNRESOLVED,
# which is U > 0, which is INCONCLUSIVE by sec 8 -- never PASS (DP-45).
LATER_WRITE_SETS = {
    "uoa_symbol": dict(
        columns=["oi_confirm_ratio", "oi_confirm_mult", "oi_confirm_score",
                 "oi_confirmed_contracts", "oi_confirm_total_contracts",
                 "score_swing", "score_long",
                 "fwd_return_1d_pct", "fwd_return_3d_pct", "fwd_return_5d_pct",
                 "fwd_return_7d_pct", "fwd_return_14d_pct", "fwd_return_30d_pct",
                 "fwd_mfe_1d_pct", "fwd_mae_1d_pct"],
        evidence=[dict(path="services/uoa_screener.py", lines=(2231, 2239),
                       literal="sym_row.oi_confirm_mult = float(oi_mult)"),
                  dict(path="services/uoa_screener.py", lines=(151, 160),
                       literal="_ALL_OUTCOME_COLUMNS = ("),
                  dict(path="services/uoa_screener.py", lines=(415, 421),
                       literal="setattr(row, k, float(v))")],
        basis="Two later-write paths exist for uoa_symbol_daily at fa70688: the OI confirmation "
              "pass (uoa_screener.py:1925, writing :2231-2239) and the forward-outcome backfill "
              "(uoa_screener.py:346 and :484, writing the _ALL_OUTCOME_COLUMNS tuple of "
              ":151-160 through the setattr at :420).  No other function assigns to a "
              "UoaSymbolDaily row after the nightly create at uoa_screener.py:1210.  CLOSED."),
}

# --------------------------------------------------------------------------------------------
# sec 2.2 / sec 4.0 -- PER-QUESTION TRANSCRIPTION (the Researcher's extraction, sec 10.5).
# One entry per listed question: its registered window, the exclusions file IT cites and the
# blocks IT names (DP-22, sec 2.3), and every frozen column it reads, with a citation.
# `as_feature=False` marks a read its own PREREG scopes to an audit / exclusion-ledger use;
# such a column is listed in the register but is IMMATERIAL by sec 4.3's own definition.
# `lookback_sessions` extends the in-window night range backwards for that table only.
# columns=["*"] means every column of that table (used where the PREREG names the table but not
# its columns; the wider reading, DP-45).
# The extraction is pinned: each question's PREREG.md sha256 is checked before the run, so the
# transcription can never drift from the text it was made from (sec 10.5, sec 10.9).
QUESTIONS = [
 dict(id="Q002", dir="Q002_speed_to_target",
      sha="c66a64e35337d054a60874a08ae982d45e285f9bbb49e5d1a1054f699d56bc87",
      window=("2026-06-01", None), excl=("research/data/exclusions_v001.json", ("manual_runs",)),
      reads=[dict(table="sas_candidates", columns=["public_payload_json", "selected_rank",
                  "overall_score", "dominant_direction", "context_json"]),
             dict(table="sas_runs", columns=["finished_at", "config_json"])],
      level_predicate="ranked", level_columns=["public_payload_json"],
      cite="Q002 sec 2 Source tables (manifest_v001) bullet; sec 6 test window >= 2026-06-01"),
 dict(id="Q003", dir="Q003_repeat_selection",
      sha="8000feaf74a994dbdbbce67588c5f3fa9fcd3ce449fb6b9926159c6f81443fd9",
      window=("2026-06-01", None), excl=("research/data/exclusions_v001.json", ("manual_runs",)),
      reads=[dict(table="sas_candidates", columns=["public_payload_json", "selected_rank",
                  "overall_score", "dominant_direction"]),
             dict(table="sas_runs", columns=["finished_at", "config_json"])],
      level_predicate="ranked", level_columns=["public_payload_json"],
      cite="Q003 sec 2 source tables and streak definition; sec 6 test window >= 2026-06-01"),
 dict(id="Q004", dir="Q004_entry_basis",
      sha="2e27bd2318b51cc1ccaef01fbe54b71fbfd6717f1c7e3c1204cd18512e7b1fc2",
      window=("2026-06-01", None), excl=("research/data/exclusions_v001.json", ("manual_runs",)),
      reads=[dict(table="sas_candidates", columns=["public_payload_json", "selected_rank",
                  "overall_score", "dominant_direction", "context_json"]),
             dict(table="sas_runs", columns=["finished_at"])],
      level_predicate="ranked", level_columns=["public_payload_json"],
      cite="Q004 sec 2 source tables, where sas_runs.finished_at is load-bearing (the E_AH "
           "entry clock); sec 6 test window >= 2026-06-01"),
 dict(id="Q005", dir="Q005_elite_thinning",
      sha="8347b49881bb5bec1e25be586bd42406cc6a274dbca26e55c91df4ed558cd7bc",
      window=("2026-04-01", "2026-09-10"),
      excl=("research/data/exclusions_v001.json", ("manual_runs",)),
      reads=[dict(table="sas_candidates", columns=[
                  "overall_score", "completeness_score", "qualified", "threshold_pass",
                  "qualification_reason", "selected_rank", "dominant_direction",
                  "best_timeframe", "confidence_level", "flow_strength_score",
                  "technical_structure_score", "gex_alignment_score", "projection_score",
                  "fundamental_quality_score", "catalyst_event_score",
                  "smart_money_confirmation_score", "cross_layer_bonus", "conflict_penalty",
                  "missing_data_penalty", "source_membership_json", "score_details_json",
                  "missing_data_json", "context_json", "industry", "market_regime_snapshot"]),
             dict(table="sas_runs", columns=["config_json", "stats_json"])],
      level_predicate=None, level_columns=[],
      cite="Q005 sec 2 Source tables, plus sec 6 which adds market_regime_snapshot as a "
           "Channel 3a descriptor; window 2026-04-01..2026-09-10, all non-excluded nights"),
 dict(id="Q006", dir="Q006_control_cohort_path",
      sha="4f6cd76aaefe35ca3d9035fdc05d53033dedbdd31256c08f39ba6329e5a3e633",
      window=("2026-04-01", "2026-09-10"),
      excl=("research/data/exclusions_v001.json", ("manual_runs",)),
      reads=[dict(table="sas_candidates", columns=["public_payload_json", "selected_rank",
                  "overall_score", "dominant_direction", "best_timeframe", "context_json"]),
             dict(table="sas_runs", columns=["finished_at", "config_json"])],
      level_predicate="ranked", level_columns=["public_payload_json"],
      cite="Q006 sec 2 source tables; sec 6 all 108 non-excluded nights 2026-04-01..2026-09-10"),
 dict(id="Q007", dir="Q007_gap_at_open",
      sha="6968e7ca6b3295f45f9a6f0494b9ffadb7969be64f799c9c034186079bd143e2",
      window=("2026-06-01", None),
      excl=("research/data/exclusions_v002.json", ("manual_runs", "non_session_runs")),
      reads=[dict(table="sas_candidates", columns=["selected_rank", "qualified", "overall_score",
                  "dominant_direction", "best_timeframe", "public_payload_json",
                  "days_to_earnings_corrected"]),
             dict(table="sas_runs", columns=["finished_at"])],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q007 sec 2 source tables; header cites exclusions_v002.json; sec 6 window >= 06-01"),
 dict(id="Q008", dir="Q008_fast_start_l4",
      sha="3ec46ec4c7cfc910139010e38de341e255ae882d51237041461676e09287d081",
      window=("2026-06-01", "2026-10-23"),
      excl=("research/data/exclusions_v002.json", ("manual_runs", "non_session_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank",
                  "qualification_reason", "overall_score", "dominant_direction",
                  "best_timeframe", "public_payload_json"]),
             dict(table="sas_runs", columns=["finished_at"])],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q008 sec 2 source tables; sec 6 pick nights 2026-06-01..2026-10-23"),
 dict(id="Q009", dir="Q009_stop_whipsaw",
      sha="6c0f8f0460a04f6bf9ee51b079dfdf6b440c709804a9530b8753df7e2918b064",
      window=("2026-06-01", None),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe", "public_payload_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q009 sec 2)"),
             dict(table="sas_runs", columns=["finished_at"]),
             dict(table="sas_runs", columns=["stats_json"], as_feature=False,
                  note="exclusion audit only (Q009 sec 2)")],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q009 sec 2 source tables and the printed-swing-stop definition; sec 6 window"),
 dict(id="Q010", dir="Q010_stop_whipsaw_prospective",
      sha="1d6e6cdc122151b24311a0365cfe2b55bc99760bfe860a22a4043559f8776051",
      window=("2026-11-10", None),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe", "public_payload_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="inherited exclusion audit (Q009 sec 2 verbatim by reference)"),
             dict(table="sas_runs", columns=["finished_at"])],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q010 sec 2 Window: pick nights strictly after Q009 decision date D = 2026-11-09 "
           "(2026-12-21 if the DP-13 extension fires), for 46 sessions; every column inherited "
           "from Q009 sec 2 verbatim. The earlier branch is transcribed, the wider ADVISORY "
           "surface (DP-45)."),
 dict(id="Q011", dir="Q011_day1_dip_limit",
      sha="e95ef79740e0b7beb3f020ca3d0ae285b60d13dd259a9557b58c623656cf1125",
      window=("2026-06-01", None),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe", "public_payload_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q011 sec 2)"),
             dict(table="sas_runs", columns=["finished_at"])],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q011 sec 2 source tables; sec 6 test window >= 2026-06-01"),
 dict(id="Q012", dir="Q012_capital_recycling",
      sha="b1af050d259677a197f82bb2fffdcb14b76bb28f63a1d33803b4cc5e7dc49ada",
      window=("2026-06-01", None),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe", "public_payload_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q012 sec 2)"),
             dict(table="sas_runs", columns=["finished_at"])],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q012 sec 2 source tables; sec 6 slot-start nights >= 2026-06-01"),
 dict(id="Q013", dir="Q013_earnings_proximity",
      sha="1eeb9f705b46f5fc5347b96ac4e4bdebf0734df7efa35f935a1f8b1a1af1c7d0",
      window=("2026-06-01", None),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank",
                  "qualification_reason", "overall_score", "dominant_direction",
                  "best_timeframe", "public_payload_json", "days_to_earnings_corrected",
                  "days_since_earnings_corrected", "earnings_phase", "earnings_phase_subtag",
                  "earnings_event_risk_corrected"]),
             dict(table="sas_runs", columns=["finished_at"])],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q013 sec 2 Source tables, sas_candidates bullet, including the five point-in-time "
           "earnings fields; sec 6 pick nights from 2026-06-01"),
 dict(id="Q014", dir="Q014_uoa_persistence",
      sha="e58bb6914fc00671d22654d2b4f61c2a7a2d9dd7d932922582d1cfcadf08c9f6",
      window=("2026-06-01", None),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe", "completeness_score",
                  "public_payload_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q014 sec 2)"),
             dict(table="sas_runs", columns=["finished_at"]),
             dict(table="uoa_symbol", columns=["score_day", "score_swing", "score_long",
                  "label_day", "label_swing", "label_long", "oi_confirm_mult"],
                  lookback_sessions=5,
                  note="Q014 sec 2.1: uoa5 counts the 5 trading sessions strictly before the "
                       "pick night, so the in-window night range extends 5 sessions back")],
      level_predicate="dp28", level_columns=["public_payload_json"],
      reconstruction=dict(table="uoa_symbol", columns=["score_swing", "score_long"],
                          divisor="oi_confirm_mult",
                          cite="Q014 sec 2.1: score_b* = score_b / oi_confirm_mult where the "
                               "multiplier is non-null, score_b otherwise "
                               "(uoa_screener.py:2236-2239)"),
      cite="Q014 sec 2 Source tables plus sec 2.1 reconstruction; sec 6 test window"),
 dict(id="Q015", dir="Q015_band_85_90_updown",
      sha="d7c41ad6d423c49bab325a433c8cccb9ea0c367bbc051a6f197efefdc0b344e3",
      window=("2026-06-01", None),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe", "public_payload_json",
                  "score_details_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q015 sec 2)"),
             dict(table="sas_runs", columns=["finished_at"])],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q015 sec 2 source tables. score_details_json re-derives each band (sec 10 threat "
           "12), so it is read as a feature, not as an audit column; sec 6 window"),
 dict(id="Q016", dir="Q016_two_sided_beta_atr",
      sha="1e4699c59f90f613e89f5c33ac0750d82361575371c5d01547737564febc017c",
      window=("2026-06-01", "2026-11-13"),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe", "trading_date", "symbol",
                  "public_payload_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q016 sec 2)"),
             dict(table="sas_runs", columns=["finished_at"]),
             dict(table="market_regime", columns=["*"], night_from="2026-06-09",
                  note="Q016 sec 2: market_regime_daily, stratum only, nights >= 2026-06-09")],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q016 sec 2 source tables; Pick nights 2026-06-01 through 2026-11-13 inclusive"),
 dict(id="Q018", dir="Q018_lane_choice_by_band",
      sha="da1eb4060ae86641bc6ee4b4806c2f240117dc61dd70eff5de9cb3387d5cb1aa",
      window=("2026-09-14", None),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe", "public_payload_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q018 sec 2)"),
             dict(table="sas_runs", columns=["finished_at"])],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q018 sec 2 source tables; sec 6 prospective only, pick nights >= 2026-09-14. "
           "Q018 is NOT one of sec 2.2 four ADVISORY questions, so its out-of-window nights "
           "are IMMATERIAL and not ADVISORY -- sec 2.2 is transcribed literally."),
 dict(id="Q019", dir="Q019_conviction_monitor_exit",
      sha="140ce0edfe366fa2eaf38574cc346c3ea009cb492e6d8409f91163f76e2b1d3b",
      window=("2026-06-01", "2027-05-03"),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="audit only (Q019 sec 2)"),
             dict(table="sas_runs", columns=["finished_at"]),
             dict(table="conviction_monitor", columns=["trading_date", "original_pick_date",
                  "symbol", "days_since_qualified", "overall_tier", "age_adjusted_severity",
                  "polarity_tier", "technical_overall_tier", "reason_codes_json",
                  "polarity_details_json", "technical_signal_count_json", "created_at",
                  "updated_at"],
                  note="Q019 sec 2: monitor rows carry trading_date s in t+1..t+5, later than "
                       "the pick night t, so the night range needs no backward extension")],
      level_predicate=None, level_columns=[],
      cite="Q019 sec 2 source tables; sec 6 pick nights 2026-06-01 .. 2027-05-03"),
 dict(id="Q021", dir="Q021_pin_risk_two_sided",
      sha="3c658dfa28eb848948f12e1170d16d98bf7b8918441093ff47069149f38cf7d0",
      window=("2026-06-01", "2027-04-30"),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["qualified", "selected_rank", "overall_score",
                  "dominant_direction", "best_timeframe", "trading_date", "symbol",
                  "context_json", "public_payload_json"]),
             dict(table="sas_runs", columns=["finished_at"]),
             dict(table="market_regime", columns=["*"], night_from="2026-06-09",
                  note="Q021 sec 2: market_regime_daily, stratum only, nights >= 2026-06-09"),
             dict(table="gex_symbol", columns=["*"], as_feature=False,
                  note="Q021 sec 2: gex_symbol_daily is used ONLY for the disagreement audit "
                       "in sec 6, never as the feature. The feature is "
                       "sas_candidates.context_json -> gex_context")],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q021 sec 2 source tables; Pick nights 2026-06-01 through 2027-04-30 inclusive"),
 dict(id="Q022", dir="Q022_sector_cluster_nights",
      sha="dd08406ad982366d07fa3572fecf6c833e12b7c75b723acaadbce0739d2a576c",
      window=("2026-07-08", "2027-01-13"),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["trading_date", "symbol", "qualified",
                  "selected_rank", "overall_score", "dominant_direction", "best_timeframe",
                  "public_payload_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q022 sec 2.1)"),
             dict(table="sas_runs", columns=["finished_at"]),
             dict(table="market_regime", columns=["*"], night_from="2026-06-09",
                  note="Q022 sec 2.1: market_regime_daily, stratum only, nights >= 2026-06-09")],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q022 sec 2.1 Sources; sec 2.2 Pick nights 2026-07-08 through 2027-01-13 inclusive"),
 dict(id="Q023", dir="Q023_band_80_90_strongly_bullish",
      sha="43709c6da58bcf8f834e2b802e209e6f4d01889183b7b7952dd3f773065e490f",
      window=("2026-09-14", "2027-02-25"),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["trading_date", "qualified", "selected_rank",
                  "overall_score", "dominant_direction", "best_timeframe", "confidence_level",
                  "public_payload_json", "score_details_json", "context_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q023 sec 2)"),
             dict(table="sas_runs", columns=["finished_at", "config_json"]),
             dict(table="market_regime", columns=["trading_date", "regime_version",
                  "market_regime", "raw_parent_regime", "score_band", "regime_phase",
                  "regime_confidence", "data_quality", "asof_close_date",
                  "effective_for_trading_date", "secular_risk_score", "created_at"]),
             dict(table="projection_bull", columns=["*"],
                  note="Q023 sec 2: projection_pick_bullish_daily, the B3 panel only (sec 3), "
                       "never a primary. No column list is given there, so every column is "
                       "taken -- the wider reading, DP-45")],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q023 sec 2 source tables; sec 6 pick nights 2026-09-14 .. 2027-02-25"),
 dict(id="Q024", dir="Q024_sas_vs_simple_benchmarks",
      sha="d29193bcb4cec9789e346f43c02089f82a8a03cd802645dadbe5efae41ebe257",
      window=("2026-09-14", "2027-04-07"),
      excl=("research/data/exclusions_v003.json",
            ("manual_runs", "non_session_runs", "uncorroborated_publication_runs")),
      reads=[dict(table="sas_candidates", columns=["trading_date", "symbol", "qualified",
                  "selected_rank", "overall_score", "dominant_direction", "best_timeframe",
                  "confidence_level", "technical_structure_score", "public_payload_json"]),
             dict(table="sas_candidates", columns=["outcome_target_invalid"], as_feature=False,
                  note="exclusion audit only (Q024 sec 2.1)"),
             dict(table="sas_runs", columns=["finished_at"]),
             dict(table="market_regime", columns=["*"], night_from="2026-06-09",
                  note="Q024 sec 2.1: market_regime_daily, stratum only, regime_version v1.2, "
                       "same-evening writes only")],
      level_predicate="dp28", level_columns=["public_payload_json"],
      cite="Q024 sec 2.1 Sources; sec 2.2 Pick nights 2026-09-14 through 2027-04-07 inclusive"),
]

# sec 4.6 -- Channel E column classification.  Deterministic, name-based, printed in full so a
# misclassification is visible rather than silent (sec 10.9).
OUTCOME_TABLES = ("sas_excursion", "whale_ledger")
EVIDENCE_TABLES = ("outcome_corrections",)      # read as evidence about restatement, sec 4.5
OUTCOME_PREFIXES = ("outcome_", "fwd_return_", "fwd_mfe_", "fwd_mae_", "level_hit_",
                    "mae_", "mfe_", "realized_")
OUTCOME_SUBSTRINGS = ("_hit_", "hit_by_", "days_to_hit", "recovered_to", "pierced_",
                      "reselect", "_at_touch", "touch_date", "breach", "window_sealed",
                      "was_sealed")
METADATA_NAMES = ("id", "run_id", "created_at", "updated_at", "computed_at", "audit_path",
                  "public_output_path", "analysis_report_path", "analysis_schema_version",
                  "analysis_status", "status", "computation_version", "library_version",
                  "config_hash", "source_market_intelligence_run_id", "row_id", "authorization",
                  "correction_date", "cause", "bar_source", "table_name", "field",
                  "old_value", "new_value", "alert_id", "closed_at", "synthesis_status")


# =============================================================================================
# Helpers -- pure, deterministic, no I/O beyond the pinned files and the frozen platform SHA.
# =============================================================================================

class Abort(Exception):
    """Loud failure.  The register is not written and no number is produced (sec 2.2)."""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_path(p: str) -> Path:
    return ROOT / str(p).replace("\\", "/")


def to_date(x) -> date | None:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    if isinstance(x, date) and not isinstance(x, datetime):
        return x
    ts = pd.Timestamp(x)
    if pd.isna(ts):
        return None
    return ts.date()


def et_dt(d: date, hh: int, mm: int, ss: int = 0, us: int = 0) -> datetime:
    """A wall-clock ET moment on date d, DST-aware, returned in UTC (sec 4.0)."""
    return datetime(d.year, d.month, d.day, hh, mm, ss, us, tzinfo=ET).astimezone(UTC)


def decision_time(d: date) -> datetime:
    """D(N) = 16:05 ET on N (sec 4.0).  Used for reporting in every rule."""
    return et_dt(d, 16, 5)


class Calendar:
    """NYSE session list, derived from the pinned files only (AMENDMENTS.md A4).

    sessions = the dates SPY trades in prices_daily_split, unioned with every trading_date in
    the frozen selection tables (the price freeze starts 2026-01-31, while the frozen selection
    SQL carries rows back to 2026-01-02).  No exchange calendar package, no network, no query.
    """

    def __init__(self, sessions: list[date], source_note: str):
        self.sessions = sorted(set(sessions))
        self.index = {d: i for i, d in enumerate(self.sessions)}
        self.source_note = source_note

    def shift(self, d: date, k: int) -> date | None:
        i = self.index.get(d)
        if i is None:                      # d is not itself a session (e.g. 2026-04-03)
            j = np.searchsorted(np.array(self.sessions, dtype="O"), d, side="right")
            i = int(j) - 1
            if i < 0:
                return None
        j = i + k
        if j < 0 or j >= len(self.sessions):
            return None
        return self.sessions[j]

    def next_session(self, d: date) -> date | None:
        return self.shift(d, 1)

    def next_open(self, d: date) -> datetime | None:
        n = self.next_session(d)
        return None if n is None else et_dt(n, 9, 30)


def boundary_for(d: date, cal: Calendar, rule: str) -> datetime | None:
    """The decision-time boundary on night d under the amended sec 4.0 rule (AMENDMENTS A1)."""
    if rule == "R1_1605_LITERAL":
        return decision_time(d)
    if rule == "R2_SAME_EVENING":
        return et_dt(d, 23, 59, 59, 999999)
    if rule == "R3_NEXT_OPEN":
        nxt = cal.next_open(d)
        # At the last session of the freeze there is no next open.  Fall back to the
        # same-evening boundary, which is EARLIER and therefore flags more, never less
        # (DP-45: the reading less likely to clear).  Recorded in the register.
        return nxt if nxt is not None else et_dt(d, 23, 59, 59, 999999)
    raise Abort("unknown DECISION_TIME_RULE: %r" % (rule,))


def r3_fallback_fired(d: date, cal: Calendar) -> bool:
    """AMENDMENTS.md A12, as narrowed by A1: the last session of a freeze has no next open, so
    R3 falls back to the same-evening boundary.  With R2 in force this affects the **R3
    sensitivity column only**; the count of nights on which it fired is printed (A1r item 3)."""
    return cal.next_open(d) is None


def use_time(d: date, lag: int, cal: Calendar, rule: str) -> datetime | None:
    """U(T, N) = boundary(N + lag_sessions) -- the earliest decision a row dated N may inform."""
    nd = cal.shift(d, int(lag or 0))
    return None if nd is None else boundary_for(nd, cal, rule)


def declared_time(d: date, available_time_et: str) -> datetime | None:
    """A(T, N).  None where the declaration is not a clock (post-hoc) -- AMENDMENTS.md A2."""
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", str(available_time_et or "").strip())
    if not m:
        return None
    return et_dt(d, int(m.group(1)), int(m.group(2)))


def git_show(codebase: Path, path: str, sha: str = PLATFORM_SHA_SHORT) -> list[str]:
    """Read a file from the read-only platform repo at the FROZEN SHA.  Never HEAD (sec 10.6)."""
    out = subprocess.run(["git", "-C", str(codebase), "show", "%s:%s" % (sha, path)],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise Abort("git show %s:%s failed in %s -- %s" % (sha, path, codebase, out.stderr.strip()))
    return out.stdout.splitlines()


def verify_repo_literal(codebase: Path, path: str, lines: tuple, literal: str) -> dict:
    """Confirm a transcribed path:line citation still says what it is cited as saying."""
    try:
        text = git_show(codebase, path)
    except Abort as exc:
        return dict(path=path, lines=list(lines), literal=literal, ok=False, reason=str(exc))
    lo, hi = int(lines[0]), int(lines[1])
    window = "\n".join(text[max(lo - 1, 0):hi])
    ok = literal in window
    return dict(path=path, lines=[lo, hi], literal=literal, ok=bool(ok),
                reason="" if ok else "literal not found at %s:%d-%d at %s" % (path, lo, hi,
                                                                             PLATFORM_SHA_SHORT))


# =============================================================================================
# Preflight -- every pin checked before a single frozen row is read (sec 2.2, decisions 1, 8).
# =============================================================================================

def parse_prereg_question_list(prereg_text: str) -> tuple[list[str], list[str]]:
    """Extract sec 2.2's IN and OUT question ids from the PREREG text itself.

    The bullet is `- **Questions:** ...`.  Q001 opens the out-sentence and appears nowhere else
    in the bullet, so the ids before the first `Q001` are the IN list, and the ids between
    `Q001` and the `are **out**` marker that closes the same sentence are the OUT list.  (The
    text after that marker is prose and is not scanned: it names Q024 as a drafting precedent,
    which is not a membership statement.)  Any deviation aborts the run rather than guessing.
    """
    m = re.search(r"^- \*\*Questions:\*\*(.*?)(?=^- \*\*)", prereg_text, re.S | re.M)
    if not m:
        raise Abort("PREREG sec 2.2: the '- **Questions:**' bullet was not found")
    bullet = " ".join(m.group(1).split())
    if "21 registered questions" not in bullet:
        raise Abort("PREREG sec 2.2 no longer says '21 registered questions': %r" % bullet[:200])
    cut = bullet.find("Q001")
    if cut < 0:
        raise Abort("PREREG sec 2.2: the out-list marker Q001 was not found in the bullet")
    end = bullet.find("are **out**", cut)
    if end < 0:
        raise Abort("PREREG sec 2.2: the 'are **out**' marker was not found after Q001")
    ids_in, ids_out = [], []
    for tok in re.findall(r"Q\d{3}", bullet[:cut]):
        if tok not in ids_in:
            ids_in.append(tok)
    for tok in re.findall(r"Q\d{3}", bullet[cut:end]):
        if tok not in ids_out:
            ids_out.append(tok)
    return ids_in, ids_out


def check_question_transcription(prereg_text: str) -> dict:
    ids_in, ids_out = parse_prereg_question_list(prereg_text)
    mine_in, mine_out = set(QUESTION_IDS_IN), set(QUESTION_IDS_OUT)
    diff = dict(
        missing_from_script=sorted(set(ids_in) - mine_in),
        extra_in_script=sorted(mine_in - set(ids_in)),
        out_missing_from_script=sorted(set(ids_out) - mine_out),
        out_extra_in_script=sorted(mine_out - set(ids_out)),
        overlap=sorted(mine_in & mine_out),
    )
    if any(diff.values()) or len(mine_in) != 21 or len(ids_in) != 21:
        raise Abort("sec 2.2 TRANSCRIPTION MISMATCH -- no register is produced.\n"
                    "  PREREG in  (%d): %s\n  script in  (%d): %s\n"
                    "  PREREG out (%d): %s\n  script out (%d): %s\n  diff: %s"
                    % (len(ids_in), ids_in, len(mine_in), sorted(mine_in),
                       len(ids_out), ids_out, len(mine_out), sorted(mine_out),
                       json.dumps(diff)))
    return dict(prereg_in=ids_in, prereg_out=ids_out, matched=True)


def preflight(args) -> dict:
    ev = {}

    # (0) the amendment gate -- sec 4.0 / AMENDMENTS.md A1.
    if DECISION_TIME_RULE is None:
        raise Abort(
            "DECISION_TIME_RULE is unresolved.  PREREG sec 4.0 defines D(N) = 16:05 ET while "
            "its own B1/B2 sources (manifest availability, FREEZE_v001 sec 7, "
            "KT_AUDIT sec 1) treat the same-evening batch write as compliant; the two readings "
            "give different verdicts.  sec 10.10 requires the gap to be fixed by a dated "
            "amendment BEFORE the run, never during it.  See AMENDMENTS.md A1 (2026-09-14).  "
            "The Researcher does not choose it and the Steward does not choose it at run time.")
    if DECISION_TIME_RULE not in RULE_IDS:
        raise Abort("DECISION_TIME_RULE %r is not one of %s" % (DECISION_TIME_RULE, RULE_IDS))
    if not DECISION_TIME_RULE_AMENDMENT:
        raise Abort("DECISION_TIME_RULE is set but DECISION_TIME_RULE_AMENDMENT names no "
                    "dated amendment.  A rule without its amendment citation is not registered.")
    ev["decision_time_rule"] = DECISION_TIME_RULE
    ev["decision_time_rule_amendment"] = DECISION_TIME_RULE_AMENDMENT

    # (1) this PREREG, unchanged since the lock commit.
    prereg = QDIR / "PREREG.md"
    prereg_text = prereg.read_text(encoding="utf-8")
    got = sha256_file(prereg)
    if got != PREREG_SHA256:
        raise Abort("Q026 PREREG.md sha256 %s != pinned %s -- the locked text has changed; "
                    "stop (rule 3)" % (got, PREREG_SHA256))
    ev["prereg_sha256"] = got
    ev["prereg_commit"] = PREREG_COMMIT

    # (2) sec 2.2's question list, transcribed, with a loud failure on mismatch (decision 1).
    ev["question_list"] = check_question_transcription(prereg_text)
    ev["question_list"]["script_in"] = list(QUESTION_IDS_IN)
    ev["question_list"]["script_out"] = list(QUESTION_IDS_OUT)

    # (3) every listed question's own PREREG, unchanged since the extraction was made from it.
    qsha = {}
    for q in QUESTIONS:
        p = ROOT / "research" / "questions" / q["dir"] / "PREREG.md"
        if not p.exists():
            raise Abort("%s PREREG.md not found at %s" % (q["id"], p))
        h = sha256_file(p)
        if h != q["sha"]:
            raise Abort("%s PREREG.md sha256 %s != the sha256 the sec 4.3 column extraction was "
                        "made from (%s).  The transcription may be stale; stop (sec 10.5)."
                        % (q["id"], h, q["sha"]))
        qsha[q["id"]] = h
    if sorted(qsha) != sorted(QUESTION_IDS_IN):
        raise Abort("the QUESTIONS table does not cover exactly the 21 ids of sec 2.2: %s"
                    % sorted(set(QUESTION_IDS_IN) ^ set(qsha)))
    ev["question_prereg_sha256"] = qsha

    # (4) the manifests and every pinned parquet, by sha256 and by row count (rule 4, DP-50).
    man = json.loads(norm_path(args.manifest).read_text())
    manp = json.loads(norm_path(args.manifest_prices).read_text())
    ev["manifest"] = dict(path=args.manifest, version=man.get("version"),
                          as_of=man.get("as_of"), frozen_at=man.get("frozen_at"),
                          sha256=sha256_file(norm_path(args.manifest)),
                          platform_git_sha=man.get("platform_git_sha"))
    ev["manifest_prices"] = dict(path=args.manifest_prices, version=manp.get("version"),
                                 as_of=manp.get("as_of"), frozen_at=manp.get("frozen_at"),
                                 sha256=sha256_file(norm_path(args.manifest_prices)),
                                 platform_git_sha=manp.get("platform_git_sha"))
    if man.get("platform_git_sha") != PLATFORM_SHA:
        raise Abort("manifest platform_git_sha %s != the pinned attribution SHA %s"
                    % (man.get("platform_git_sha"), PLATFORM_SHA))
    files = []
    for mm in (man, manp):
        for t in mm["tables"]:
            f = norm_path(t["file"])
            if not f.exists():
                raise Abort("pinned parquet missing: %s" % f)
            h = sha256_file(f)
            if t.get("sha256") and h != t["sha256"]:
                raise Abort("%s sha256 %s != manifest %s -- the freeze is not the pinned one"
                            % (t["name"], h, t["sha256"]))
            files.append(dict(table=t["name"], file=str(f.relative_to(ROOT)).replace("\\", "/"),
                              rows_declared=t.get("rows"), sha256=h))
    ev["files"] = files

    # (5) the read-only platform repo at the frozen SHA (sec 4.3, sec 10.6, decision 8).
    codebase = Path(args.codebase).resolve()
    out = subprocess.run(["git", "-C", str(codebase), "rev-parse", PLATFORM_SHA_SHORT],
                         capture_output=True, text=True)
    if out.returncode != 0 or out.stdout.strip() != PLATFORM_SHA:
        raise Abort("the platform repo at %s does not resolve %s to %s (got %r)"
                    % (codebase, PLATFORM_SHA_SHORT, PLATFORM_SHA, out.stdout.strip()))
    ev["platform_sha_read"] = PLATFORM_SHA
    ev["codebase"] = str(codebase)

    # (6) every exclusions file each question cites (sec 2.3, DP-22).
    excl = {}
    for q in QUESTIONS:
        path, blocks = q["excl"]
        p = norm_path(path)
        if not p.exists():
            raise Abort("%s cites %s, which does not exist" % (q["id"], path))
        d = json.loads(p.read_text())
        for b in blocks:
            if b not in d:
                raise Abort("%s cites block %s of %s, which the file does not carry"
                            % (q["id"], b, path))
        excl[path] = dict(sha256=sha256_file(p), version=d.get("version", "001"),
                          declared_on=d.get("declared_on"),
                          blocks_present=[b for b in d if b.endswith("_runs")])
    ev["exclusions_files"] = excl
    ev["no_live_query"] = ("This module opens no database connection.  It imports argparse, "
                           "hashlib, json, os, re, subprocess, sys, collections, datetime, "
                           "pathlib, zoneinfo, numpy, pandas -- and nothing else (rule 4, "
                           "DP-50(c), decision 4).")
    return ev, man, manp


def excluded_nights(path: str, blocks: tuple) -> set:
    d = json.loads(norm_path(path).read_text())
    out = set()
    for b in blocks:
        for s in d.get(b, {}).get("trading_dates", []):
            out.add(date.fromisoformat(s))
    return out


# =============================================================================================
# Loading.  Every row of every table in both manifests (sec 2.2 -- this is a census).
# =============================================================================================

WRITE_TS = {          # (W_row, L_row) per table.  AMENDMENTS.md A3 for sas_excursion.
    "sas_candidates": ("created_at", "updated_at"),
    "sas_runs": ("created_at", "updated_at"),
    "sas_excursion": ("computed_at", "computed_at"),
    "conviction_monitor": ("created_at", "updated_at"),
    "market_regime": ("created_at", "updated_at"),
    "uoa_symbol": ("created_at", "updated_at"),
    "gex_symbol": ("created_at", "updated_at"),
    "whale_ledger": ("created_at", "updated_at"),
    "projection_bull": ("created_at", "updated_at"),
    "projection_bear_v2": ("created_at", "updated_at"),
    "outcome_corrections": ("created_at", "updated_at"),
}


def load_tables(man: dict) -> dict:
    out = {}
    for t in man["tables"]:
        df = pd.read_parquet(norm_path(t["file"]))
        out[t["name"]] = df
    return out


def write_times(df: pd.DataFrame, table: str) -> pd.DataFrame:
    """W_row and L_row per row (sec 4.0).  updated_at null or == created_at resolves to W."""
    wcol, lcol = WRITE_TS[table]
    n = len(df)
    if n == 0:
        return pd.DataFrame(dict(night=[], W=[], L=[]))
    night = pd.Series([to_date(x) for x in df["trading_date"]], index=df.index)
    W = pd.to_datetime(df[wcol], utc=True, errors="coerce") if wcol in df.columns else pd.Series(
        pd.NaT, index=df.index, dtype="datetime64[ns, UTC]")
    L = pd.to_datetime(df[lcol], utc=True, errors="coerce") if lcol in df.columns else pd.Series(
        pd.NaT, index=df.index, dtype="datetime64[ns, UTC]")
    L = L.where(L.notna() & (L >= W), W)
    return pd.DataFrame(dict(night=night, W=W, L=L), index=df.index)


# =============================================================================================
# Channel A -- the write-time census (sec 4.2).  Every row, every table, every night.
# =============================================================================================

# A1r item 1 -- the per-(table, night) boundary columns, in a fixed order.
BAND_COLUMNS = ("n_W_gt_R1", "n_W_gt_R2", "n_W_gt_R3", "n_W_band_R1_R2", "n_W_band_R2_R3",
                "n_L_gt_U_R1", "n_L_gt_U_R2", "n_L_gt_U_R3")


def _boundary_triple(sub: pd.DataFrame, night: date, lag: int, cal: Calendar) -> dict:
    """n_W_gt_* and n_L_gt_U_* under each of R1 / R2 / R3, plus the two bands (A1r item 1).

    DESCRIPTIVE ONLY.  The columns that decide are n_W_gt_B / n_L_gt_U, computed under the
    in-force rule alone.  R1 is contained in R2 is contained in R3 in permissiveness, so both
    bands are non-negative by construction: n_W_band_R1_R2 is the same-evening batch band
    (16:05..23:59:59 ET on N) and n_W_band_R2_R3 is the overnight-before-next-open band.
    """
    out = {}
    for rid in RULE_IDS:
        sh = RULE_SHORT[rid]
        b = boundary_for(night, cal, rid)
        u = use_time(night, lag, cal, rid)
        out["n_W_gt_%s" % sh] = 0 if b is None else int((sub["W"] > pd.Timestamp(b)).sum())
        out["n_L_gt_U_%s" % sh] = 0 if u is None else int((sub["L"] > pd.Timestamp(u)).sum())
    out["n_W_band_R1_R2"] = int(out["n_W_gt_R1"] - out["n_W_gt_R2"])
    out["n_W_band_R2_R3"] = int(out["n_W_gt_R2"] - out["n_W_gt_R3"])
    return out


def channel_a(tables: dict, man: dict, cal: Calendar, rule: str) -> pd.DataFrame:
    avail = man.get("availability", {})
    rows = []
    for t in man["tables"]:
        name = t["name"]
        df = tables[name]
        dec = avail.get(name, {})
        at_et, lag = dec.get("available_time_et"), int(dec.get("lag_sessions") or 0)
        if len(df) == 0:
            rows.append(dict(table=name, night=None, month=None, n_rows=0, declared_time=at_et,
                             lag_sessions=lag, n_W_gt_A="n/a", n_W_gt_B=0, n_L_gt_U=0,
                             **{c: 0 for c in BAND_COLUMNS},
                             r3_fallback=False,
                             median_lateness_h=None, max_lateness_h=None, spread_h=None,
                             W_heterogeneous=False,
                             note="table is empty in the freeze -- nothing to census"))
            continue
        wt = write_times(df, name)
        for night, idx in wt.groupby("night").groups.items():
            sub = wt.loc[idx]
            if night is None:
                continue
            b = boundary_for(night, cal, rule)
            a = declared_time(night, at_et)
            u = use_time(night, lag, cal, rule)
            lateness = (sub["W"] - pd.Timestamp(decision_time(night))).dt.total_seconds() / 3600.0
            n_gt_a = "n/a" if a is None else int((sub["W"] > pd.Timestamp(a)).sum())
            n_gt_b = 0 if b is None else int((sub["W"] > pd.Timestamp(b)).sum())
            n_l_gt_u = 0 if u is None else int((sub["L"] > pd.Timestamp(u)).sum())
            spread = (sub["W"].max() - sub["W"].min()).total_seconds() / 3600.0 if sub["W"].notna().any() else None
            rows.append(dict(
                table=name, night=night.isoformat(), month=night.isoformat()[:7],
                n_rows=int(len(sub)), declared_time=at_et,
                lag_sessions=lag, n_W_gt_A=n_gt_a, n_W_gt_B=n_gt_b, n_L_gt_U=n_l_gt_u,
                **_boundary_triple(sub, night, lag, cal),
                r3_fallback=bool(r3_fallback_fired(night, cal)),
                median_lateness_h=None if lateness.isna().all() else round(float(lateness.median()), 4),
                max_lateness_h=None if lateness.isna().all() else round(float(lateness.max()), 4),
                spread_h=None if spread is None else round(float(spread), 4),
                W_heterogeneous=bool(n_gt_b not in (0, int(len(sub)))),
                note=""))
    out = pd.DataFrame(rows).sort_values(["table", "night"], na_position="first")
    return out.reset_index(drop=True)


def boundary_band_totals(chan_a: pd.DataFrame) -> dict:
    """A1r item 1 -- the same triple totalled per table, per month and overall."""
    cols = list(BAND_COLUMNS)
    out = {}
    if not len(chan_a):
        empty = pd.DataFrame(columns=["n_rows"] + cols)
        return dict(by_table=empty, by_month=empty, overall=empty)
    d = chan_a.copy()
    for c in cols + ["n_rows"]:
        d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0).astype(int)
    out["by_table"] = d.groupby("table")[["n_rows"] + cols].sum().reset_index()
    dm = d[d["month"].notna()]
    out["by_month"] = (dm.groupby("month")[["n_rows"] + cols].sum().reset_index()
                       if len(dm) else pd.DataFrame(columns=["month", "n_rows"] + cols))
    tot = d[["n_rows"] + cols].sum()
    out["overall"] = pd.DataFrame([dict(scope="overall",
                                        **{k: int(v) for k, v in tot.items()})])
    return out


# =============================================================================================
# Channel C -- internal corroboration (sec 4.4).  The only channel that sees a traceless
# mutation.  Independent of every timestamp.
# =============================================================================================

STATS_ANALOGUES = {           # AMENDMENTS.md A8: fixed here, never inferred at run time
    "qualified_count": ("n_qualified", "n_published"),
    "published_count": ("n_published",),
    "selected_count": ("n_published",),
    "candidate_count": ("n_rows",),
    "candidates_count": ("n_rows",),
    "total_candidates": ("n_rows",),
    "scored_count": ("n_rows",),
    "universe_count": ("n_rows",),
}


def _json_load(x):
    if isinstance(x, dict):
        return x
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return {}
    try:
        return json.loads(x)
    except Exception:
        return {}


def channel_c(tables: dict) -> pd.DataFrame:
    runs, cand = tables["sas_runs"], tables["sas_candidates"]
    cand = cand.assign(_night=[to_date(x) for x in cand["trading_date"]])
    rows = []
    for _, r in runs.iterrows():
        night = to_date(r["trading_date"])
        sub = cand[cand["_night"] == night]
        qual = sub["qualified"].fillna(False).astype(bool) if "qualified" in sub else pd.Series(
            False, index=sub.index)
        ranked = sub["selected_rank"].notna() if "selected_rank" in sub else pd.Series(
            False, index=sub.index)
        pub = qual & ranked
        derived = dict(n_rows=int(len(sub)), n_qualified=int(qual.sum()),
                       n_published=int(pub.sum()), n_ranked=int(ranked.sum()))
        stats = _json_load(r.get("stats_json"))
        disagreements, uncompared = [], []
        for k, v in stats.items():
            kl = str(k).lower()
            if kl == "direction_counts" and isinstance(v, dict):
                obs_pub = Counter(str(s).lower() for s in sub.loc[pub, "dominant_direction"])
                obs_q = Counter(str(s).lower() for s in sub.loc[qual, "dominant_direction"])
                want = {str(a).lower(): int(b) for a, b in v.items() if isinstance(b, (int, float))}
                if want and want != {k2: v2 for k2, v2 in obs_pub.items() if v2} and \
                   want != {k2: v2 for k2, v2 in obs_q.items() if v2}:
                    disagreements.append("direction_counts=%s vs published=%s qualified=%s"
                                         % (want, dict(obs_pub), dict(obs_q)))
                continue
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                continue
            if kl in STATS_ANALOGUES:
                cands = [derived[a] for a in STATS_ANALOGUES[kl]]
                if int(v) not in cands:
                    disagreements.append("%s=%s vs %s" % (k, v, dict(
                        zip(STATS_ANALOGUES[kl], cands))))
            elif "count" in kl or kl.startswith("n_"):
                uncompared.append("%s=%s" % (k, v))
        ranks = sorted(int(x) for x in sub.loc[pub, "selected_rank"].dropna()) if len(sub) else []
        dup = [k for k, c in Counter(ranks).items() if c > 1]
        gap = bool(ranks) and (ranks != list(range(min(ranks), min(ranks) + len(ranks))))
        if dup:
            disagreements.append("duplicate selected_rank %s" % dup)
        if gap:
            disagreements.append("gap-ranked selected_rank %s" % ranks)
        payload_formed = int(sub.loc[pub, "public_payload_json"].map(
            lambda x: bool(_json_load(x))).sum()) if "public_payload_json" in sub else 0
        rows.append(dict(night=night.isoformat(), n_rows=derived["n_rows"],
                         n_qualified=derived["n_qualified"], n_published=derived["n_published"],
                         n_ranked=derived["n_ranked"],
                         stats_qualified_count=stats.get("qualified_count"),
                         stats_fields=";".join(sorted(str(k) for k in stats)),
                         payload_formed_published=payload_formed,
                         uncompared_count_fields=";".join(sorted(uncompared)),
                         disagreement=bool(disagreements),
                         disagreement_detail=" | ".join(disagreements)))
    return pd.DataFrame(rows).sort_values("night").reset_index(drop=True)


# =============================================================================================
# Gate 0 -- the positive control (sec 4.1).  Run first, read first.  Targets fixed in sec 3;
# derivations use no hard-coded date list.  No target is ever relaxed (sec 8).
# =============================================================================================

def gate0(tables: dict, man: dict, cal: Calendar, rule: str, chan_a: pd.DataFrame,
          chan_c: pd.DataFrame) -> dict:
    runs = tables["sas_runs"].copy()
    runs["_night"] = [to_date(x) for x in runs["trading_date"]]
    for c in ("created_at", "started_at", "finished_at"):
        runs[c] = pd.to_datetime(runs[c], utc=True, errors="coerce")

    # (a) DP-04: finished_at later than the next session's open; plus the 12h corroboration.
    dp04, gap12, gaps = [], [], {}
    for _, r in runs.iterrows():
        nxt = cal.next_open(r["_night"])
        if nxt is not None and pd.notna(r["finished_at"]) and r["finished_at"] > pd.Timestamp(nxt):
            dp04.append(r["_night"].isoformat())
        if pd.notna(r["started_at"]) and pd.notna(r["created_at"]):
            h = (r["started_at"] - r["created_at"]).total_seconds() / 3600.0
            gaps[r["_night"].isoformat()] = round(float(h), 3)
            if h >= GATE0_HOURS_RERUN:
                gap12.append(r["_night"].isoformat())
    rerun_set = sorted(set(dp04) | set(gap12))

    # (b) per-night candidate created_at spread, and equality with the run's finished_at.
    cand = tables["sas_candidates"].copy()
    cand["_night"] = [to_date(x) for x in cand["trading_date"]]
    cand["created_at"] = pd.to_datetime(cand["created_at"], utc=True, errors="coerce")
    fin = {r["_night"]: r["finished_at"] for _, r in runs.iterrows()}
    spread_rows, eq_nights = [], []
    for night, sub in cand.groupby("_night"):
        sp = (sub["created_at"].max() - sub["created_at"].min()).total_seconds() / 3600.0
        eq = bool(pd.notna(fin.get(night)) and (sub["created_at"] == fin[night]).all())
        spread_rows.append(dict(night=night.isoformat(), n_rows=int(len(sub)),
                                spread_h=round(float(sp), 6), equals_run_finished_at=eq))
        if eq:
            eq_nights.append(night.isoformat())

    # (c) market_regime rows created more than one session after their trading_date, and the
    #     multi-regime_version structure before 2026-06-09.
    mr = tables["market_regime"].copy()
    mr["_night"] = [to_date(x) for x in mr["trading_date"]]
    mr["created_at"] = pd.to_datetime(mr["created_at"], utc=True, errors="coerce")
    late_regime, versions_pre = [], defaultdict(set)
    for _, r in mr.iterrows():
        nxt = cal.shift(r["_night"], 1)
        bound = None if nxt is None else et_dt(nxt, 23, 59, 59, 999999)
        if bound is not None and pd.notna(r["created_at"]) and r["created_at"] > pd.Timestamp(bound):
            late_regime.append(r["_night"].isoformat())
        if r["_night"] < GATE0_REGIME_BACKFILL_BEFORE:
            versions_pre[r["_night"].isoformat()].add(str(r.get("regime_version")))
    late_regime = sorted(set(late_regime))
    multi_version_nights = sorted(k for k, v in versions_pre.items() if len(v) > 1)
    backfilled_pre = sorted(set(k for k in versions_pre))

    # (d) per-night median write lateness by table across 2026-01..2026-03.
    lo, hi = GATE0_LATE_BLOCK_RANGE
    late_block = {}
    for tname in GATE0_LATE_BLOCK_TABLES:
        sub = chan_a[(chan_a["table"] == tname) & chan_a["night"].notna()].copy()
        sub["_d"] = sub["night"].map(date.fromisoformat)
        win = sub[(sub["_d"] >= lo) & (sub["_d"] <= hi)]
        hits = win[win["median_lateness_h"].fillna(-1) > GATE0_HOURS_LATE_BLOCK]
        late_block[tname] = dict(n_nights_in_range=int(len(win)), n_late=int(len(hits)),
                                 nights=sorted(hits["night"].tolist()))

    # (e) gex_symbol within-night append: spread > 12h.
    gx = chan_a[(chan_a["table"] == "gex_symbol") & chan_a["night"].notna()]
    gex_append = sorted(gx[gx["spread_h"].fillna(0) > GATE0_HOURS_SPREAD]["night"].tolist())

    # (f) Channel C disagreement nights.
    stats_nights = sorted(chan_c[chan_c["disagreement"]]["night"].tolist())

    checks = []

    def chk(cid, target, got, ok, detail=""):
        checks.append(dict(id=cid, target=target, found=got, passed=bool(ok), detail=detail))

    chk("B2.1_eleven_tables", "%d tables censused" % GATE0_TABLES_EXPECTED,
        int(chan_a["table"].nunique()),
        chan_a["table"].nunique() == GATE0_TABLES_EXPECTED,
        "FREEZE_v001 sec 7's 11-row sampled table is superseded by a counted one")
    chk("B2.2_rerun_nights", list(GATE0_RERUN_NIGHTS), rerun_set,
        set(GATE0_RERUN_NIGHTS).issubset(rerun_set),
        "DP-04 set %s ; started-created >= %sh set %s" % (dp04, GATE0_HOURS_RERUN, gap12))
    chk("B2.2b_manual_runs", list(GATE0_MANUAL_RUN_NIGHTS), rerun_set,
        set(GATE0_MANUAL_RUN_NIGHTS).issubset(rerun_set), "exclusions_v001 manual_runs")
    chk("B2.2c_candidates_equal_finished", "the re-run nights carry candidate created_at == "
        "the run's finished_at", eq_nights,
        set(GATE0_RERUN_NIGHTS).issubset(set(eq_nights)), "KT_AUDIT sec 1")
    chk("B2.3_regime_late_2026-07-06", GATE0_REGIME_LATE_NIGHT, late_regime,
        GATE0_REGIME_LATE_NIGHT in late_regime, "manifest availability.market_regime note")
    chk("B2.4_regime_backfill_pre_0609", "every market_regime night < 2026-06-09 backfilled, "
        "multiple regime_version rows", dict(n_nights=len(backfilled_pre),
                                             n_multi_version=len(multi_version_nights)),
        len(multi_version_nights) > 0 and len(backfilled_pre) > 0,
        "PI-005; manifest universe_membership_note")
    ok_block = all(v["n_late"] >= GATE0_LATE_BLOCK_MIN_NIGHTS for v in late_block.values())
    chk("B2.5_late_block_jan_mar", "%d+ late nights in %s..%s for each of %s"
        % (GATE0_LATE_BLOCK_MIN_NIGHTS, lo, hi, list(GATE0_LATE_BLOCK_TABLES)),
        {k: v["n_late"] for k, v in late_block.items()}, ok_block, "KT_AUDIT sec 3")
    chk("B2.6_gex_within_night_append", list(GATE0_GEX_APPEND_NIGHTS), gex_append,
        set(GATE0_GEX_APPEND_NIGHTS).issubset(set(gex_append)), "KT_AUDIT sec 2")
    chk("B2.7_stats_json_2026-06-26", GATE0_STATS_JSON_NIGHT, stats_nights,
        GATE0_STATS_JSON_NIGHT in stats_nights,
        "exclusions_v003 uncorroborated_publication_runs / STEWARD_Q009_exposure sec R3")

    passed = all(c["passed"] for c in checks)
    return dict(passed=bool(passed), checks=checks,
                derived=dict(dp04_nights=dp04, gap12_nights=gap12, rerun_set=rerun_set,
                             run_started_minus_created_h=gaps,
                             candidate_night_spread=spread_rows,
                             market_regime_late_nights=late_regime,
                             market_regime_multi_version_nights=multi_version_nights,
                             late_block=late_block, gex_append_nights=gex_append,
                             stats_json_disagreement_nights=stats_nights))


# =============================================================================================
# Channel D -- restatement anachronism in the pinned price freeze (sec 4.5).
# Channel D reads the price manifest and nothing else from it: no forward bar is read as an
# outcome, no return, no touch, no excursion (sec 2.4).
# =============================================================================================

def split_factor_changes(manp: dict) -> tuple[pd.DataFrame, date]:
    raw = pd.read_parquet(norm_path(
        next(t["file"] for t in manp["tables"] if t["name"] == "prices_daily_raw")))
    spl = pd.read_parquet(norm_path(
        next(t["file"] for t in manp["tables"] if t["name"] == "prices_daily_split")))
    raw = raw[["symbol", "date", "c"]].rename(columns={"c": "c_raw"})
    spl = spl[["symbol", "date", "c"]].rename(columns={"c": "c_split"})
    m = raw.merge(spl, on=["symbol", "date"], how="inner")
    m["date"] = pd.to_datetime(m["date"]).dt.date
    m = m[(m["c_split"].notna()) & (m["c_split"] != 0)]
    m["factor"] = m["c_raw"] / m["c_split"]
    m = m.sort_values(["symbol", "date"])
    prev = m.groupby("symbol")["factor"].shift(1)
    rel = (m["factor"] / prev - 1.0).abs()
    ch = m[(prev.notna()) & (rel > 1e-6)]
    changes = ch[["symbol", "date", "factor"]].rename(
        columns={"date": "factor_change_date", "factor": "factor_after"})
    changes = changes.assign(factor_before=prev[ch.index].values)
    last_date = max(m["date"]) if len(m) else None
    return changes.reset_index(drop=True), last_date


def row_predicate_mask(df: pd.DataFrame, predicate: str | None) -> pd.Series:
    if predicate is None:
        return pd.Series(False, index=df.index)
    ranked = df["selected_rank"].notna() if "selected_rank" in df else pd.Series(False, index=df.index)
    if predicate == "ranked":
        return ranked
    if predicate == "dp28":
        qual = df["qualified"].fillna(False).astype(bool) if "qualified" in df else pd.Series(
            False, index=df.index)
        return qual & ranked
    if predicate == "all":
        return pd.Series(True, index=df.index)
    raise Abort("unknown row predicate %r" % predicate)


def channel_d(tables: dict, manp: dict, qwin: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    changes, last_date = split_factor_changes(manp)
    by_symbol = defaultdict(list)
    for _, r in changes.iterrows():
        by_symbol[r["symbol"]].append(r["factor_change_date"])
    cand = tables["sas_candidates"].copy()
    cand["_night"] = [to_date(x) for x in cand["trading_date"]]
    rows = []
    for q in QUESTIONS:
        if not q.get("level_predicate"):
            continue
        mask = row_predicate_mask(cand, q["level_predicate"])
        sub = cand[mask]
        for _, r in sub.iterrows():
            night = r["_night"]
            if night not in qwin[q["id"]]["in_window_nights"]:
                continue
            for d in by_symbol.get(r.get("symbol"), []):
                if night < d <= last_date:
                    rows.append(dict(question=q["id"], table="sas_candidates",
                                     column=";".join(q["level_columns"]),
                                     night=night.isoformat(), symbol=r.get("symbol"),
                                     factor_change_date=d.isoformat(),
                                     predicate=q["level_predicate"],
                                     reason="stored price level compared against "
                                            "prices_daily_split bars that were restated by a "
                                            "corporate action after the pick night"))
    material = pd.DataFrame(rows)
    # Value-correction appendix (sec 4.5, DP-50(a)): evidence only, produces no material row.
    oc = tables["outcome_corrections"].copy()
    if len(oc):
        app = (oc.groupby(["table_name", "field", "was_sealed", "correction_date"], dropna=False)
                 .size().reset_index(name="n"))
        app["correction_date"] = app["correction_date"].astype(str)
    else:
        app = pd.DataFrame(columns=["table_name", "field", "was_sealed", "correction_date", "n"])
    return material, changes, app


# =============================================================================================
# Channel E -- declaration coverage (sec 4.6).  Reported, never material on its own.
# =============================================================================================

def classify_column(table: str, col: str) -> str:
    c = col.lower()
    if c in METADATA_NAMES:
        return "metadata"
    if table in OUTCOME_TABLES:
        return "metadata" if c in ("trading_date", "symbol", "id") else "outcome"
    if table in EVIDENCE_TABLES:
        return "metadata"
    if any(c.startswith(p) for p in OUTCOME_PREFIXES) or any(s in c for s in OUTCOME_SUBSTRINGS):
        return "outcome"
    return "feature_eligible"


def channel_e(man: dict, chan_a: pd.DataFrame, read_index: dict) -> tuple[pd.DataFrame, dict]:
    avail = man.get("availability", {})
    het_tables = set(chan_a[chan_a["W_heterogeneous"] == True]["table"])   # noqa: E712
    rows, proposal = [], {}
    for t in man["tables"]:
        name = t["name"]
        dec = avail.get(name, {})
        note = str(dec.get("note") or "")
        cols = {}
        for col in t["columns"]:
            klass = classify_column(name, col)
            flags = []
            if klass == "feature_eligible":
                if col in note or re.search(re.escape(col), note):
                    flags.append("GAP_DECLARED_IN_NOTE_ONLY")
                for pat in re.findall(r"[a-z][a-z0-9_]*\*|\*_[a-z0-9_]+\*?", note):
                    rx = "^" + pat.replace("*", ".*") + "$"
                    if re.match(rx, col):
                        flags.append("GAP_NOTE_PATTERN:%s" % pat)
                if name in het_tables:
                    flags.append("GAP_ROW_HETEROGENEITY")
                for a in ATTRIBUTION:
                    if a["table"] == name and (col in a["columns"] or a["columns"] == ["*"]):
                        flags.append("GAP_ATTRIBUTED_LATE_PATH:%s" % a["id"])
            flags = sorted(set(flags))
            readers = sorted(read_index.get((name, col), set()))
            rows.append(dict(table=name, column=col, klass=klass,
                             declared_available_time_et=dec.get("available_time_et"),
                             declared_lag_sessions=dec.get("lag_sessions"),
                             declaration_gap=bool(flags), gap_flags=";".join(flags),
                             read_by=";".join(readers)))
            if flags:
                cols[col] = dict(gap_flags=flags,
                                 available_time_et="TODO_STEWARD",
                                 lag_sessions="TODO_STEWARD",
                                 evidence="Q026 Channel E, register %s" % man.get("version"))
        proposal[name] = dict(available_time_et=dec.get("available_time_et"),
                              lag_sessions=dec.get("lag_sessions"),
                              note=dec.get("note"), columns=cols)
    return pd.DataFrame(rows), proposal


# =============================================================================================
# sec 4.3 -- the MATERIAL_MITIGATED reconstruction check (decision 2, strict).
# Row by row on every in-window row, never a sample, relative tolerance 1e-6.  A null or zero
# divisor, a missing multiplier column, or a mismatch outside tolerance makes the whole TUPLE
# MATERIAL.  The divisor set is the closed set the code names at fa70688 (AMENDMENTS.md A6).
# =============================================================================================

def check_reconstruction(df: pd.DataFrame, nights: set, rec: dict,
                         mult_set_ok: bool = True, mult_set_detail: str = "") -> dict:
    div = rec["divisor"]
    out = dict(divisor=div, rtol=RECONSTRUCTION_RTOL, columns={}, verified=True,
               n_rows_in_window=0, failures=[],
               documented_divisor_set=list(OI_MULT_SET),
               divisor_set_citation="%s:%s:%d-%d" % (PLATFORM_SHA_SHORT,
                                                     OI_MULT_SET_CITATION["path"],
                                                     OI_MULT_SET_CITATION["lines"][0],
                                                     OI_MULT_SET_CITATION["lines"][1]),
               divisor_set_verified_at_sha=bool(mult_set_ok),
               divisor_set_withdrawal=("" if mult_set_ok else mult_set_detail))
    # AMENDMENTS.md 2026-09-14, A6 RIDER.  The closed divisor set is the whole content of the
    # A6 check; if it is not at its cited line range at the frozen SHA the check cannot be
    # evaluated, and decision 2's own failure branch makes the TUPLE MATERIAL -- not mitigated,
    # not skipped.  The withdrawal is printed with A9's withdrawals (sec 10.6).
    if not mult_set_ok:
        out["verified"] = False
        out["failures"].append(
            "A6 RIDER (AMENDMENTS.md 2026-09-14): the documented divisor set %s is NOT at "
            "%s:%s:%d-%d at run time -- the reconstruction check cannot be evaluated and the "
            "tuple is MATERIAL (decision 2 failure branch).  %s"
            % (list(OI_MULT_SET), PLATFORM_SHA_SHORT, OI_MULT_SET_CITATION["path"],
               OI_MULT_SET_CITATION["lines"][0], OI_MULT_SET_CITATION["lines"][1],
               mult_set_detail))
        for col in rec["columns"]:
            out["columns"][col] = dict(ok=False, reason="A6 rider: divisor-set citation "
                                                        "withdrawn at %s" % PLATFORM_SHA_SHORT)
        return out
    if len(df) == 0:
        out["verified"] = False
        out["failures"].append("no rows to verify")
        return out
    d = df.copy()
    d["_night"] = [to_date(x) for x in d["trading_date"]]
    d = d[d["_night"].isin(nights)]
    out["n_rows_in_window"] = int(len(d))
    if div not in d.columns:
        out["verified"] = False
        out["failures"].append("missing multiplier column %s -- tuple is MATERIAL" % div)
        return out
    m = pd.to_numeric(d[div], errors="coerce")
    n_null = int(m.isna().sum())
    n_zero = int((m == 0).sum())
    bad_set = sorted(set(round(float(x), 6) for x in m.dropna().unique()) - set(OI_MULT_SET))
    for col in rec["columns"]:
        if col not in d.columns:
            out["columns"][col] = dict(ok=False, reason="column absent from the freeze")
            out["verified"] = False
            continue
        v = pd.to_numeric(d[col], errors="coerce")
        rec16 = v / m
        back = rec16 * m
        with np.errstate(invalid="ignore", divide="ignore"):
            rel = (back - v).abs() / v.abs().where(v.abs() > 0, 1.0)
        n_out = int((rel > RECONSTRUCTION_RTOL).fillna(True).sum() - v.isna().sum())
        n_out = max(n_out, 0)
        ok = (n_null == 0 and n_zero == 0 and not bad_set and n_out == 0)
        out["columns"][col] = dict(ok=bool(ok), n_rows=int(len(d)), n_null_divisor=n_null,
                                   n_zero_divisor=n_zero, n_out_of_tolerance=n_out,
                                   divisors_outside_documented_set=bad_set)
        if not ok:
            out["verified"] = False
            out["failures"].append(
                "%s: null_divisor=%d zero_divisor=%d out_of_tolerance=%d "
                "divisors_outside_%s=%s" % (col, n_null, n_zero, n_out,
                                            list(OI_MULT_SET), bad_set))
    return out


# =============================================================================================
# Windows and per-night statistics.
# =============================================================================================

def night_stats(tables: dict, man: dict, cal: Calendar, rule: str) -> dict:
    """(table, night) -> the four counts Channel B classifies on (sec 4.2, sec 4.3)."""
    avail = man.get("availability", {})
    st = {}
    for t in man["tables"]:
        name = t["name"]
        df = tables[name]
        if len(df) == 0:
            continue
        lag = int((avail.get(name, {}) or {}).get("lag_sessions") or 0)
        wt = write_times(df, name)
        for night, idx in wt.groupby("night").groups.items():
            if night is None:
                continue
            sub = wt.loc[idx]
            b = boundary_for(night, cal, rule)
            u = use_time(night, lag, cal, rule)
            w_gt = 0 if b is None else int((sub["W"] > pd.Timestamp(b)).sum())
            l_gt = 0 if b is None else int(((sub["W"] <= pd.Timestamp(b)) &
                                           (sub["L"] > pd.Timestamp(b))).sum())
            l_gt_u = 0 if u is None else int((sub["L"] > pd.Timestamp(u)).sum())
            st[(name, night)] = dict(n_rows=int(len(sub)), n_W_gt_B=w_gt, n_indet=l_gt,
                                     n_L_gt_U=l_gt_u)
    return st


def question_windows(cal: Calendar, census_nights: dict) -> dict:
    out = {}
    for q in QUESTIONS:
        ws = date.fromisoformat(q["window"][0])
        we = date.fromisoformat(q["window"][1]) if q["window"][1] else None
        ex = excluded_nights(*q["excl"])
        per_read = {}
        for r in q["reads"]:
            tws = ws
            if r.get("lookback_sessions"):
                shifted = cal.shift(ws, -int(r["lookback_sessions"]))
                tws = shifted or ws
            if r.get("night_from"):
                nf = date.fromisoformat(r["night_from"])
                tws = max(tws, nf)
            twe = we
            if r.get("night_to"):
                nt = date.fromisoformat(r["night_to"])
                twe = nt if twe is None else min(twe, nt)
            nights = set()
            for n in census_nights.get(r["table"], ()):  # census nights of that table only
                if n < tws or (twe is not None and n > twe) or n in ex:
                    continue
                nights.add(n)
            per_read[(r["table"], tuple(r["columns"]))] = nights
        base = set()
        for n in census_nights.get("sas_candidates", ()):
            if n >= ws and (we is None or n <= we) and n not in ex:
                base.add(n)
        out[q["id"]] = dict(window_start=ws, window_end=we, excluded=ex,
                            in_window_nights=base, per_read=per_read)
    return out


# =============================================================================================
# Channel B -- column-level materiality (sec 4.3).  The section that decides.
# =============================================================================================

CLASSES = ("MATERIAL", "MATERIAL_MITIGATED", "CONTAMINATION_UNRESOLVED", "ADVISORY",
           "IMMATERIAL")


def attribution_hits(table: str, column: str, night: date, verified: dict) -> list:
    hits = []
    for a in ATTRIBUTION:
        if a["table"] != table:
            continue
        if a["columns"] != ["*"] and column not in a["columns"]:
            continue
        if a.get("repo") and not verified.get(a["id"], {}).get("ok", False):
            continue                      # withdrawn: the cited literal is not at that line
        cond = a["nights"]
        if cond != "*":
            m = re.fullmatch(r"trading_date <= (\d{4}-\d{2}-\d{2})", cond)
            if not m or night > date.fromisoformat(m.group(1)):
                continue
        hits.append(a["id"])
    return hits


def channel_b(tables: dict, man: dict, cal: Calendar, rule: str, stats: dict, qwin: dict,
              chan_c: pd.DataFrame, chan_d: pd.DataFrame, verified: dict,
              recon: dict, census_nights: dict) -> tuple[pd.DataFrame, dict]:
    cols_of = {t["name"]: list(t["columns"]) for t in man["tables"]}
    disagree_nights = set(date.fromisoformat(d) for d in
                          chan_c[chan_c["disagreement"]]["night"].tolist())
    # candidate nights whose rows carry a DP-04-flagged run's finished_at (sec 4.3 MATERIAL)
    runs = tables["sas_runs"].copy()
    runs["_night"] = [to_date(x) for x in runs["trading_date"]]
    runs["finished_at"] = pd.to_datetime(runs["finished_at"], utc=True, errors="coerce")
    flagged = set()
    for _, r in runs.iterrows():
        nxt = cal.next_open(r["_night"])
        started = pd.to_datetime(r.get("started_at"), utc=True, errors="coerce")
        created = pd.to_datetime(r.get("created_at"), utc=True, errors="coerce")
        late = nxt is not None and pd.notna(r["finished_at"]) and r["finished_at"] > pd.Timestamp(nxt)
        gap = pd.notna(started) and pd.notna(created) and \
            (started - created).total_seconds() / 3600.0 >= GATE0_HOURS_RERUN
        if late or gap:
            flagged.add(r["_night"])
    cand = tables["sas_candidates"].copy()
    cand["_night"] = [to_date(x) for x in cand["trading_date"]]
    cand["created_at"] = pd.to_datetime(cand["created_at"], utc=True, errors="coerce")
    eq_flagged_nights = set()
    fin = {r["_night"]: r["finished_at"] for _, r in runs.iterrows()}
    for night, sub in cand.groupby("_night"):
        if night in flagged and pd.notna(fin.get(night)) and (sub["created_at"] == fin[night]).any():
            eq_flagged_nights.add(night)
    d_pairs = set()
    if len(chan_d):
        for _, r in chan_d.iterrows():
            d_pairs.add((r["question"], date.fromisoformat(r["night"])))

    rows = []
    for q in QUESTIONS:
        advisory_q = q["id"] in ADVISORY_QUESTIONS
        w = qwin[q["id"]]
        for r in q["reads"]:
            table = r["table"]
            as_feature = r.get("as_feature", True)
            # AMENDMENTS.md 2026-09-14, A7 RIDER.  Convention (i) narrows the surface, so it is
            # never silent: an as_feature=False column carries the sub-label
            # IMMATERIAL_BY_SCOPE and the PREREG sentence that scopes it, and keeps its row in
            # the class-count table (sec 4.3: no column may be omitted).  The sub-label is
            # print-only -- the class stays IMMATERIAL and the sec 8 verdict is untouched.
            scope_class = "" if as_feature else "IMMATERIAL_BY_SCOPE"
            scope_note = "" if as_feature else r.get("note", "")
            cols = cols_of[table] if r["columns"] == ["*"] else r["columns"]
            cols = [c for c in cols if c in cols_of[table]]
            in_nights = w["per_read"][(table, tuple(r["columns"]))]
            rec = q.get("reconstruction")
            for col in cols:
                for night in sorted(census_nights.get(table, ())):
                    s = stats.get((table, night))
                    if s is None:
                        continue
                    attr = attribution_hits(table, col, night, verified)
                    late_pattern = bool(s["n_W_gt_B"] or s["n_indet"] or attr)
                    if (night not in in_nights) or (not as_feature):
                        if advisory_q and late_pattern and as_feature:
                            klass, why = "ADVISORY", ("late-write pattern on a column this "
                                                      "prospective-window question will read, "
                                                      "on a night outside its in-window range")
                        else:
                            klass = "IMMATERIAL"
                            why = ("out of window" if night not in in_nights
                                   else "not read as a feature by this question")
                        rows.append(dict(question=q["id"], table=table, column=col,
                                         night=night.isoformat(), klass=klass, reason=why,
                                         n_rows=s["n_rows"], n_W_gt_B=s["n_W_gt_B"],
                                         n_indeterminate=s["n_indet"],
                                         attribution=";".join(attr), as_feature=as_feature,
                                         scope_class=scope_class, scope_note=scope_note,
                                         in_window=bool(night in in_nights)))
                        continue

                    reasons = []
                    if s["n_W_gt_B"] > 0:
                        reasons.append("W_row > boundary on %d of %d rows"
                                       % (s["n_W_gt_B"], s["n_rows"]))
                    if attr:
                        reasons.append("attributed late-write path: %s" % ";".join(attr))
                    if table == "sas_candidates" and night in eq_flagged_nights:
                        reasons.append("candidate W_row equals a DP-04-flagged run finished_at")
                    if (table == "sas_candidates" and night in disagree_nights
                            and col in PUBLICATION_PREDICATE_COLUMNS):
                        reasons.append("Channel C: the night's stats_json does not corroborate "
                                       "the frozen row set (publication predicate column)")
                    if (q["id"], night) in d_pairs and col in (q.get("level_columns") or []):
                        reasons.append("Channel D: stored price level restated by a split "
                                       "after the pick night")

                    if reasons:
                        mitigable = (rec is not None and rec["table"] == table
                                     and col in rec["columns"]
                                     and len(reasons) == 1 and reasons[0].startswith("attributed")
                                     and set(attr) <= {"A_UOA_SCORE_MUT"})
                        if mitigable:
                            rr = recon.get(q["id"], {})
                            cinfo = (rr.get("columns") or {}).get(col, {})
                            if rr.get("verified") and cinfo.get("ok"):
                                klass = "MATERIAL_MITIGATED"
                                why = ("read through the reconstruction its own PREREG states; "
                                       "verified row by row at rtol %g" % RECONSTRUCTION_RTOL)
                            else:
                                klass = "MATERIAL"
                                why = ("reconstruction failed the sec 4.3 check (decision 2): %s"
                                       % "; ".join(rr.get("failures", ["not evaluated"])))
                        else:
                            klass, why = "MATERIAL", "; ".join(reasons)
                    elif s["n_indet"] > 0:
                        lw = LATER_WRITE_SETS.get(table)
                        closed = bool(lw) and all(
                            verified.get("%s:%s:%s" % (table, e["path"], e["lines"]), {}).get("ok")
                            for e in lw["evidence"])
                        if closed:
                            if col in lw["columns"]:
                                klass = "MATERIAL"
                                why = ("row rewritten after the boundary and the code at %s "
                                       "names this column in the later pass" % PLATFORM_SHA_SHORT)
                            else:
                                klass = "IMMATERIAL"
                                why = ("row rewritten after the boundary but the closed later-"
                                       "write set at %s does not contain this column"
                                       % PLATFORM_SHA_SHORT)
                        else:
                            klass = "CONTAMINATION_UNRESOLVED"
                            why = ("W_row <= boundary < L_row on %d rows; the code at %s does "
                                   "not close the set of columns the later pass writes for %s. "
                                   "Resolved by: a per-column write timestamp (EN-015), an "
                                   "append-only run history (EN-001), a point-in-time score "
                                   "column (PI-013)." % (s["n_indet"], PLATFORM_SHA_SHORT, table))
                    else:
                        klass, why = "IMMATERIAL", "no detectable post-boundary write"
                    rows.append(dict(question=q["id"], table=table, column=col,
                                     night=night.isoformat(), klass=klass, reason=why,
                                     n_rows=s["n_rows"], n_W_gt_B=s["n_W_gt_B"],
                                     n_indeterminate=s["n_indet"],
                                     attribution=";".join(attr), as_feature=as_feature,
                                     scope_class=scope_class, scope_note=scope_note,
                                     in_window=True))
    tuples = pd.DataFrame(rows)

    # class counts for EVERY column of EVERY table, always (sec 4.3).  No column is omitted.
    counts = []
    seen = set()
    if len(tuples):
        g = tuples.groupby(["table", "column", "klass"]).size().unstack(fill_value=0)
        # A7 rider: the IMMATERIAL_BY_SCOPE sub-count, so a scoped-out column is visible as
        # scoped out rather than indistinguishable from an out-of-window IMMATERIAL row.
        scoped = tuples[tuples["scope_class"] == "IMMATERIAL_BY_SCOPE"]
        scoped_n = scoped.groupby(["table", "column"]).size().to_dict()
        scoped_q = {k: ";".join(sorted(set(v["question"])))
                    for k, v in scoped.groupby(["table", "column"])}
        scoped_why = {}
        for k, v in scoped.groupby(["table", "column"]):
            notes = sorted({n for n in v["scope_note"] if n})
            scoped_why[k] = " | ".join(notes)
        for (table, column), row in g.iterrows():
            seen.add((table, column))
            readers = sorted(set(tuples[(tuples["table"] == table) &
                                        (tuples["column"] == column) &
                                        (tuples["klass"] != "IMMATERIAL")]["question"]))
            counts.append(dict(table=table, column=column,
                               **{c: int(row.get(c, 0)) for c in CLASSES},
                               IMMATERIAL_BY_SCOPE=int(scoped_n.get((table, column), 0)),
                               questions_non_immaterial=";".join(readers),
                               questions_immaterial_by_scope=scoped_q.get((table, column), ""),
                               scope_sentences=scoped_why.get((table, column), "")))
    for t in man["tables"]:
        for col in t["columns"]:
            if (t["name"], col) in seen:
                continue
            counts.append(dict(table=t["name"], column=col,
                               **{c: 0 for c in CLASSES},
                               IMMATERIAL_BY_SCOPE=0,
                               questions_non_immaterial="",
                               questions_immaterial_by_scope="",
                               scope_sentences="",
                               ))
    cc = pd.DataFrame(counts).fillna(0)
    cc["read_by_any_listed_question"] = cc.apply(
        lambda r: bool(r["questions_non_immaterial"]) or
        ((r["table"], r["column"]) in seen), axis=1)
    return tuples, cc.sort_values(["table", "column"]).reset_index(drop=True)


# =============================================================================================
# sec 8 -- the decision rule, numeric, written before unsealing.
# =============================================================================================

def boundary_phrase(rule: str | None = None) -> str:
    """A1r item 4 -- the boundary, named, for every verdict sentence."""
    r = rule or DECISION_TIME_RULE
    return ("`%s`: %s -- %s" % (r, RULE_BOUNDARY_TEXT.get(r, "boundary undefined"),
                                DECISION_TIME_RULE_AMENDMENT))


def verdict(gate: dict, tuples: pd.DataFrame, qwin: dict, chan_d: pd.DataFrame,
            rule: str | None = None) -> dict:
    rule = rule or DECISION_TIME_RULE
    bphrase = boundary_phrase(rule)
    if not gate["passed"]:
        return dict(verdict="INCONCLUSIVE", controller_verdict="INCONCLUSIVE",
                    label="HISTORICAL_ONLY", gate0_passed=False, M=None, MM_failed=None,
                    MM_verified=None, U=None, advisory=None, stop_the_desk=False,
                    stop_limbs=[], decision_time_rule=rule, questions_touched=None,
                    channel_d_material_rows=int(len(chan_d)), per_question={},
                    statement=(
                        "Gate 0 did not re-find every B2 item under the decision-time boundary "
                        "%s.  The rest of the register is "
                        "not interpreted (sec 8).  At most two fix-and-re-run passes, all "
                        "inside the hard stop 2026-10-05 (decision 7)." % bphrase))
    mat = tuples[tuples["klass"] == "MATERIAL"]
    mm = tuples[tuples["klass"] == "MATERIAL_MITIGATED"]
    unres = tuples[tuples["klass"] == "CONTAMINATION_UNRESOLVED"]
    adv = tuples[tuples["klass"] == "ADVISORY"]
    M, U = int(len(mat)), int(len(unres))
    mm_failed = int(mat["reason"].str.startswith("reconstruction failed").sum()) if M else 0
    limbs, detail = [], {}
    for q in QUESTIONS:
        qid = q["id"]
        nights_in = len(qwin[qid]["in_window_nights"])
        core = mat[(mat["question"] == qid) & (mat["column"].isin(CORE_SELECTION_COLUMNS))]
        # a Channel D row never enters limb (a): a stored price level is not a core column
        n_core_nights = core["night"].nunique()
        share = (n_core_nights / nights_in) if nights_in else 0.0
        detail[qid] = dict(in_window_nights=nights_in, core_material_nights=int(n_core_nights),
                           share=round(float(share), 4),
                           any_material=bool((mat["question"] == qid).any()))
        if nights_in and share >= 0.20:
            limbs.append("(a) %s: material rows on a core selection column cover %.1f%% of its "
                         "%d in-window nights" % (qid, 100 * share, nights_in))
    n_q_touched = int(mat["question"].nunique()) if M else 0
    if n_q_touched >= 5:
        limbs.append("(b) material rows touch %d of the 21 listed questions" % n_q_touched)
    if M >= 1:
        v, cv = "FAIL", "HISTORICALLY_CONFIRMED"
        st = ("FAIL: M = %d material (question, table, column, night) tuples across %d of the "
              "21 listed questions -- each one a feature column a listed question reads whose "
              "row was written after the end of the ET calendar day on which the decision was "
              "made (%s).  The failure is per-row and scoped (sec 8); the sec 9 "
              "remedy attaches to the affected tuples, not to the desk."
              % (M, n_q_touched, bphrase))
    elif U > 0:
        v, cv = "INCONCLUSIVE", "INCONCLUSIVE"
        st = ("INCONCLUSIVE: M = 0 but U = %d unresolved tuples under %s -- the timestamps "
              "cannot exclude contamination and the code at %s could not close the column "
              "set.  U > 0 is never PASS (DP-45)." % (U, bphrase, PLATFORM_SHA_SHORT))
    else:
        v, cv = "PASS", "NULL"
        st = ("PASS: no feature column any registered question reads was written after that "
              "question's decision-time boundary (%s), on any night inside its window, on this "
              "freeze." % bphrase)
    return dict(verdict=v, controller_verdict=cv, label="HISTORICAL_ONLY", gate0_passed=True,
                M=M, MM_failed=mm_failed, MM_verified=int(len(mm)), U=U,
                advisory=int(len(adv)), questions_touched=n_q_touched,
                stop_the_desk=bool(limbs), stop_limbs=limbs, per_question=detail,
                channel_d_material_rows=int(len(chan_d)), decision_time_rule=rule,
                statement=st)


# =============================================================================================
# A1r item 2 -- BOUNDARY SENSITIVITY.  DESCRIPTIVE ONLY; IT DECIDES NOTHING.
#
# The sec 8 verdict is computed under the in-force rule alone (AMENDMENTS.md 2026-09-14, A1).
# This block re-runs Channel B and the sec 8 arithmetic under each of the three enumerated
# readings so a reader can see what any other boundary would have produced WITHOUT the verdict
# depending on it.  Gate 0, Channel C, Channel D, the windows and the reconstruction check are
# rule-independent and are computed once, under the in-force rule, and reused unchanged.
#
# RULE 9.  The block may never be used to select a rule after looking.  A different boundary
# after this register exists is a look, and is a successor question, never a re-run of this one.
# =============================================================================================

def boundary_sensitivity(tables: dict, man: dict, cal: Calendar, gate: dict, qwin: dict,
                         chan_c: pd.DataFrame, chan_d: pd.DataFrame, verified: dict,
                         recon: dict, census_nights: dict, in_force_rule: str,
                         in_force_tuples: pd.DataFrame, in_force_ver: dict) -> pd.DataFrame:
    clock_tables = sorted(t["name"] for t in man["tables"]
                          if declared_time(date(2026, 1, 2),
                                           (man.get("availability", {}).get(t["name"], {}) or {})
                                           .get("available_time_et")) is not None)
    rows = []
    for rid in RULE_IDS:
        if rid == in_force_rule:
            tp, ver = in_force_tuples, in_force_ver
        else:
            st_r = night_stats(tables, man, cal, rid)
            tp, _cc = channel_b(tables, man, cal, rid, st_r, qwin, chan_c, chan_d, verified,
                                recon, census_nights)
            ver = verdict(gate, tp, qwin, chan_d, rid)
        limb_a = [x for x in (ver.get("stop_limbs") or []) if x.startswith("(a)")]
        limb_b = [x for x in (ver.get("stop_limbs") or []) if x.startswith("(b)")]
        note = ""
        if rid == "R1_1605_LITERAL":
            bound = int(len(tp[(tp["in_window"] == True) & (tp["as_feature"] == True) &   # noqa: E712
                               (tp["table"].isin(clock_tables))])) if len(tp) else 0
            note = ("BY CONSTRUCTION, NOT A MEASUREMENT: under R1 every row of a same-evening "
                    "batch table breaches the boundary, so M is bounded below by the %d "
                    "in-window feature tuples on the clock-declared tables (%s).  M = 0 and "
                    "PASS are unreachable under R1 before any data is read."
                    % (bound, ", ".join(clock_tables)))
        elif rid == "R3_NEXT_OPEN":
            note = ("A12 (as narrowed by A1) governs this column only: at the last session of "
                    "the freeze there is no next open and the same-evening boundary is used "
                    "instead.  See a12_r3_fallback_nights in the header.")
        elif rid == in_force_rule:
            note = "IN FORCE -- this is the row the sec 8 verdict was computed from."
        rows.append(dict(
            rule=rid, in_force=bool(rid == in_force_rule),
            boundary=RULE_BOUNDARY_TEXT[rid],
            M=ver["M"], MM_verified=ver["MM_verified"], MM_failed=ver["MM_failed"],
            U=ver["U"], ADVISORY=ver["advisory"],
            questions_touched=ver["questions_touched"],
            stop_limb_a_fired=bool(limb_a), stop_limb_a_questions=len(limb_a),
            stop_limb_b_fired=bool(limb_b),
            stop_the_desk=ver["stop_the_desk"],
            verdict_if_this_rule_had_been_chosen=ver["verdict"],
            note=note))
    return pd.DataFrame(rows)


# =============================================================================================
# sec 6 -- splits, and the per-night reporting unit (rule 6).
# =============================================================================================

def nightly_frame(tuples: pd.DataFrame, chan_a: pd.DataFrame, census_nights: dict,
                  qwin: dict) -> pd.DataFrame:
    all_nights = sorted(set().union(*[set(v) for v in census_nights.values()]) if census_nights
                        else set())
    excl_any = {n for n in all_nights
                if all(n in qwin[q["id"]]["excluded"] or
                       n not in qwin[q["id"]]["in_window_nights"] for q in QUESTIONS)}
    rows = []
    tby = tuples.groupby(["night", "klass"]).size().unstack(fill_value=0) if len(tuples) else None
    aby = chan_a[chan_a["night"].notna()].groupby("night")[
        ["n_rows", "n_W_gt_B", "n_L_gt_U"] + list(BAND_COLUMNS)].sum() if len(chan_a) else None
    for n in all_nights:
        key = n.isoformat()
        rec = dict(night=key, month=key[:7],
                   in_sample=bool(n <= date(2026, 5, 29)),
                   before_catalyst_fix=bool(n < BOUNDARIES["catalyst_layer_2026-06-01"]),
                   before_regime_pit=bool(n < BOUNDARIES["regime_point_in_time_2026-06-09"]),
                   before_uoa_resumption=bool(
                       n < BOUNDARIES["uoa_fwd_return_resumption_2026-07-06"]),
                   out_of_every_window_or_excluded=bool(n in excl_any))
        for c in CLASSES:
            rec[c] = int(tby.loc[key, c]) if (tby is not None and key in tby.index
                                              and c in tby.columns) else 0
        if aby is not None and key in aby.index:
            rec["rows_censused"] = int(aby.loc[key, "n_rows"])
            rec["rows_W_after_boundary"] = int(aby.loc[key, "n_W_gt_B"])
            rec["rows_L_after_use_time"] = int(aby.loc[key, "n_L_gt_U"])
            # A1r item 1 -- the same night, under all three boundaries.  Descriptive.
            for c in BAND_COLUMNS:
                rec[c] = int(aby.loc[key, c])
        else:
            rec["rows_censused"] = rec["rows_W_after_boundary"] = rec["rows_L_after_use_time"] = 0
            for c in BAND_COLUMNS:
                rec[c] = 0
        rows.append(rec)
    return pd.DataFrame(rows)


def split_tables(nightly: pd.DataFrame) -> dict:
    out = {}
    if not len(nightly):
        return out
    for key, col in (("month", "month"), ("in_sample", "in_sample"),
                     ("before_catalyst_fix_2026-06-01", "before_catalyst_fix"),
                     ("before_regime_pit_2026-06-09", "before_regime_pit"),
                     ("before_uoa_resumption_2026-07-06", "before_uoa_resumption")):
        g = nightly.groupby(col).agg(
            n_nights=("night", "count"),
            MATERIAL=("MATERIAL", "sum"), MATERIAL_MITIGATED=("MATERIAL_MITIGATED", "sum"),
            CONTAMINATION_UNRESOLVED=("CONTAMINATION_UNRESOLVED", "sum"),
            ADVISORY=("ADVISORY", "sum"), IMMATERIAL=("IMMATERIAL", "sum"),
            rows_censused=("rows_censused", "sum")).reset_index()
        g["LOW_N"] = g["n_nights"] < LOW_N_FLOOR
        out[key] = g
    return out


# =============================================================================================
# Output.
# =============================================================================================

def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if df is None or not len(df):
        return "_(none)_\n"
    d = df if max_rows is None else df.head(max_rows)
    head = "| " + " | ".join(str(c) for c in d.columns) + " |"
    sep = "|" + "|".join("---" for _ in d.columns) + "|"
    body = ["| " + " | ".join("" if pd.isna(v) else str(v) for v in r) + " |"
            for r in d.itertuples(index=False)]
    tail = "" if (max_rows is None or len(df) <= max_rows) else \
        "\n_... %d further rows in the CSV_\n" % (len(df) - max_rows)
    return "\n".join([head, sep] + body) + "\n" + tail


def write_register(path: Path, ev: dict, gate: dict, chan_a: pd.DataFrame,
                   tuples: pd.DataFrame, class_counts: pd.DataFrame, chan_c: pd.DataFrame,
                   chan_d: pd.DataFrame, changes: pd.DataFrame, appendix: pd.DataFrame,
                   chan_e: pd.DataFrame, proposal: dict, nightly: pd.DataFrame,
                   splits: dict, ver: dict, recon: dict, verified: dict, cal: Calendar,
                   res_rel: str, bands: dict | None = None,
                   sens: pd.DataFrame | None = None, a12: dict | None = None,
                   scoped_reads: pd.DataFrame | None = None) -> None:
    L = []
    A = L.append
    A("# Knowledge-time register -- %s\n" % ev["manifest"]["path"])
    A("**NON_QUOTABLE (rule 12). Label: HISTORICAL_ONLY (Q026 sec 9). No subscriber claim "
      "follows from any number here.**\n")
    A("- Question: Q026 point_in_time_integrity, PREREG commit `%s`, sha256 `%s`"
      % (ev["prereg_commit"], ev["prereg_sha256"]))
    A("- Script: `research/questions/Q026_point_in_time_integrity/eval.py` (Researcher, "
      "written once from sec 4; decision 5). Run by the Data Steward.")
    A("- Run at (UTC): %s" % datetime.now(UTC).isoformat())
    A("- Selection manifest: `%s` v%s, as_of %s, frozen_at %s, sha256 `%s`"
      % (ev["manifest"]["path"], ev["manifest"]["version"], ev["manifest"]["as_of"],
         ev["manifest"]["frozen_at"], ev["manifest"]["sha256"]))
    A("- Price manifest: `%s` v%s, sha256 `%s` (Channel D only)"
      % (ev["manifest_prices"]["path"], ev["manifest_prices"]["version"],
         ev["manifest_prices"]["sha256"]))
    A("- **Attribution SHA read: `%s`** (`git show %s:<path>`), never HEAD (sec 10.6, "
      "decision 8)." % (ev["platform_sha_read"], PLATFORM_SHA_SHORT))
    A("- Decision-time rule in force: **%s** -- %s.  Amendment: %s"
      % (ev["decision_time_rule"],
         RULE_BOUNDARY_TEXT.get(ev["decision_time_rule"], "boundary undefined"),
         ev["decision_time_rule_amendment"]))
    A("- A12 fallback (R3 sensitivity column only, AMENDMENTS.md 2026-09-14): fired on **%s** "
      "night(s)%s" % ((a12 or {}).get("n_nights", "n/a"),
                      (" -- %s" % ", ".join((a12 or {}).get("nights", [])))
                      if (a12 or {}).get("nights") else ""))
    A("- Session calendar: %s" % cal.source_note)
    A("- %s" % ev["no_live_query"])
    A("- Every table file was checked by sha256 against its manifest entry before it was read.")
    A("")
    A("## 0. Verdict (sec 8)\n")
    A("**%s** -- controller verdict `%s`, label `%s`.\n" % (ver["verdict"],
                                                            ver["controller_verdict"],
                                                            ver["label"]))
    A(ver["statement"] + "\n")
    A("- M (MATERIAL tuples) = %s" % ver["M"])
    A("- MM verified (MATERIAL_MITIGATED) = %s ; MM failed (counted inside M) = %s"
      % (ver["MM_verified"], ver["MM_failed"]))
    A("- U (CONTAMINATION_UNRESOLVED tuples) = %s" % ver["U"])
    A("- ADVISORY rows = %s (in neither M nor U nor either STOP-THE-DESK limb)" % ver["advisory"])
    A("- STOP-THE-DESK: %s" % ("YES -- " + " ; ".join(ver["stop_limbs"]) if ver["stop_the_desk"]
                               else "no"))
    A("")
    A("## 1. Gate 0 -- positive control (sec 4.1, read first)\n")
    A("Gate 0 %s.\n" % ("PASSED" if gate["passed"] else "FAILED -- nothing below is interpreted"))
    A(md_table(pd.DataFrame([{k: (json.dumps(v) if isinstance(v, (list, dict)) else v)
                              for k, v in c.items()} for c in gate["checks"]])))
    if not gate["passed"]:
        A("\n**Gate 0 failed. Per sec 8 and decision 7 the register is filed incomplete, the "
          "script defect goes to the Researcher, at most two fix-and-re-run passes are "
          "permitted and all of them sit inside the hard stop 2026-10-05. No Gate 0 target is "
          "ever relaxed to make a pass succeed. No other section of this register was "
          "computed.**\n")
        path.write_text("\n".join(L), encoding="utf-8")
        return
    A("## 2. What was read, and what was not (sec 2.2, sec 2.4)\n")
    A(md_table(pd.DataFrame(ev["files"])))
    A("\n`prices_hourly_raw` and `prices_daily_raw` carry no write timestamps and are not "
      "subject to Channel A; that is stated here rather than passed over (sec 4.5).\n")
    A("No outcome column of any table is read as an outcome anywhere in this question; no "
      "price bar is read as a return, a touch or an excursion (sec 2.4).\n")
    A("### 2.1 The 21 listed questions, and the columns extracted for each (sec 10.5)\n")
    qrows = []
    for q in QUESTIONS:
        for r in q["reads"]:
            qrows.append(dict(question=q["id"], table=r["table"],
                              columns=",".join(r["columns"]),
                              as_feature=r.get("as_feature", True),
                              window="%s..%s" % (q["window"][0], q["window"][1] or "open"),
                              exclusions="%s [%s]" % (q["excl"][0].split("/")[-1],
                                                      ",".join(q["excl"][1])),
                              lookback_sessions=r.get("lookback_sessions", 0),
                              note=r.get("note", ""), citation=q["cite"]))
    A(md_table(pd.DataFrame(qrows)))
    A("\nExtraction backstop (sec 10.5, sec 10.9): see `%s/extraction_review.csv` for every "
      "backticked token in each listed PREREG that names a frozen column and is NOT in the "
      "transcription above.\n" % res_rel)
    A("#### 2.1.1 Columns scoped out of the feature surface (`as_feature=False`) -- "
      "AMENDMENTS.md 2026-09-14, A7 rider\n")
    A("A7 convention (i) NARROWS the feature surface, so every use of it is itemised here with "
      "the PREREG sentence that scopes it, and each such column keeps a row in the class-count "
      "table below under `IMMATERIAL_BY_SCOPE` rather than being absent (sec 4.3: no column may "
      "be omitted). These columns are IMMATERIAL by sec 4.3's own wording, not by a judgment "
      "made at run time. `sas_runs.finished_at` is a feature everywhere and is NOT in this "
      "table.\n")
    A(md_table(scoped_reads if scoped_reads is not None else pd.DataFrame()))
    A("\nFull list: `%s/as_feature_false_scoped.csv`.\n" % res_rel)
    A("## 3. Channel A -- write-time census (sec 4.2)\n")
    A("One row per (table, night), all nights including the pre-April rows, no table omitted "
      "and no night summarised away. Full table in `%s/channel_a.csv`.\n" % res_rel)
    A(md_table(chan_a.groupby("table").agg(
        nights=("night", "count"), rows=("n_rows", "sum"),
        rows_W_after_boundary=("n_W_gt_B", "sum"), rows_L_after_use_time=("n_L_gt_U", "sum"),
        max_lateness_h=("max_lateness_h", "max"),
        max_within_night_spread_h=("spread_h", "max")).reset_index()))
    A("\n`n_W_gt_A` is `n/a` where the declaration is not a clock (`post-hoc`): "
      "AMENDMENTS.md A2.\n")
    A("\n**The columns that decide are `n_W_gt_B` and `n_L_gt_U`, both computed under the "
      "in-force rule `%s` alone.**\n" % ev["decision_time_rule"])
    A("### 3.1 The same census under all three boundaries (A1r item 1) -- DESCRIPTIVE\n")
    A("Per `(table, night)` in `%s/channel_a.csv`: `n_W_gt_R1`, `n_W_gt_R2`, `n_W_gt_R3`, the "
      "band columns `n_W_band_R1_R2` (the same-evening batch band, 16:05..23:59:59 ET on N) and "
      "`n_W_band_R2_R3` (the overnight-before-next-open band), and `n_L_gt_U` under each of the "
      "three rules. R1 is contained in R2 is contained in R3, so both bands are non-negative by "
      "construction. Totals follow.\n" % res_rel)
    bands = bands or {}
    A("**Per table**\n")
    A(md_table(bands.get("by_table")))
    A("\n**Per month**\n")
    A(md_table(bands.get("by_month")))
    A("\n**Overall**\n")
    A(md_table(bands.get("overall")))
    A("\nCSVs: `%s/boundary_bands_by_table.csv`, `%s/boundary_bands_by_month.csv`, "
      "`%s/boundary_bands_overall.csv`.\n" % (res_rel, res_rel, res_rel))
    A("## 4. Channel B -- column-level materiality (sec 4.3)\n")
    A("### 4.1 Class counts for every column of every table (no column omitted)\n")
    A(md_table(class_counts, max_rows=400))
    A("\n`IMMATERIAL_BY_SCOPE` (AMENDMENTS.md 2026-09-14, A7 rider) is a **sub-count of "
      "`IMMATERIAL`**, not a sixth class: it is the number of tuples that are IMMATERIAL "
      "because the reading question's own PREREG scopes that column to an audit / "
      "exclusion-ledger use (`as_feature=False`, section 2.1.1 above), rather than because the "
      "night is out of window. It enters no total and moves no verdict.\n")
    A("\nFull table: `%s/channel_b_class_counts.csv`.\n" % res_rel)
    for klass, fname in (("MATERIAL", "material"), ("MATERIAL_MITIGATED", "material_mitigated"),
                         ("CONTAMINATION_UNRESOLVED", "contamination_unresolved"),
                         ("ADVISORY", "advisory")):
        sub = tuples[tuples["klass"] == klass]
        A("### 4.2 %s -- itemised in full (%d tuples)\n" % (klass, len(sub)))
        A(md_table(sub[["question", "table", "column", "night", "n_rows", "n_W_gt_B",
                        "n_indeterminate", "attribution", "reason"]], max_rows=200))
        A("\nFull list: `%s/channel_b_%s.csv`.\n" % (res_rel, fname))
    A("IMMATERIAL tuples are counted and summarised, never itemised (sec 4.3): %d.\n"
      % int((tuples["klass"] == "IMMATERIAL").sum()))
    A("### 4.3 The reconstruction check (sec 4.3, decision 2: every in-window row, rtol 1e-6)\n")
    A("```\n%s\n```\n" % json.dumps(recon, indent=1, default=str))
    A("### 4.4 Attribution literals verified at `%s`\n" % PLATFORM_SHA_SHORT)
    vdf = pd.DataFrame([dict(key=k, **v) for k, v in verified.items()]) if verified \
        else pd.DataFrame()
    A(md_table(vdf))
    A("\n#### 4.4.1 Withdrawals (sec 10.6; AMENDMENTS.md A9, and A6 by its 2026-09-14 rider)\n")
    wdf = vdf[vdf["ok"] == False] if len(vdf) and "ok" in vdf.columns else pd.DataFrame()  # noqa: E712
    if not len(wdf):
        A("_(none -- every cited literal was found at its cited line range at `%s`)_\n"
          % PLATFORM_SHA_SHORT)
    else:
        A("**A cited literal was not at its cited line range. The entry is WITHDRAWN: the "
          "attribution is not applied, or -- for `%s*` -- the A6 divisor-set check cannot be "
          "evaluated and the reconstruction tuple is MATERIAL by decision 2's own failure "
          "branch.**\n" % OI_MULT_SET_CITATION["key_prefix"])
        A(md_table(wdf))
    A("## 5. Channel C -- internal corroboration (sec 4.4)\n")
    A("Per night: the run's own `stats_json` count fields against the frozen candidate row "
      "set, the publication predicate against the run audit, duplicate or gap-ranked "
      "`selected_rank`, and fully-formed payloads on uncorroborated nights. Full table in "
      "`%s/channel_c.csv`.\n" % res_rel)
    A(md_table(chan_c[chan_c["disagreement"]]))
    A("\n**Tables with no internal corroboration at all -- `uoa_symbol`, `gex_symbol`, "
      "`projection_bull`, `projection_bear_v2`, `conviction_monitor`, `market_regime` -- have "
      "no defence against a traceless mutation (sec 10 threat 2). A clean Channel A count for "
      "those tables is not evidence that none occurred.**\n")
    A("## 6. Channel D -- restatement anachronism in the price freeze (sec 4.5)\n")
    A("Split-factor change dates detected as `p001_daily_raw.c / p001_daily_split.c` moving by "
      "more than 1e-6 between adjacent bars (%d changes). The register reports the factor "
      "change and its date and does not name the corporate action (sec 10 threat 7).\n"
      % len(changes))
    A(md_table(changes, max_rows=100))
    A("\n### 6.1 MATERIAL restatement rows (counted in M, limb (b) only -- decision 6)\n")
    A(md_table(chan_d, max_rows=200))
    A("\n### 6.2 Value-correction appendix (evidence only, produces no material row)\n")
    A(md_table(appendix, max_rows=200))
    A("## 7. Channel E -- declaration coverage (sec 4.6)\n")
    A(md_table(chan_e[chan_e["declaration_gap"]], max_rows=200))
    A("\nFull classification of every column: `%s/channel_e.csv`. Proposed column-level "
      "availability block for the next freeze config: `%s/proposed_availability_block.json` "
      "(a Steward artifact; Q026 edits nothing).\n" % (res_rel, res_rel))
    A("## 8. Splits (sec 6)\n")
    for k, g in splits.items():
        A("### %s\n" % k)
        A(md_table(g))
    A("\nAny cell below %d nights is flagged `LOW_N` and no trend is read from it (sec 5.1).\n"
      % LOW_N_FLOOR)
    A("## 9. Boundary sensitivity (A1r item 2)\n")
    A("**%s**\n" % SENSITIVITY_HEADING)
    A("`M`, `MM`, `U`, `questions_touched` and both STOP-THE-DESK limbs, recomputed under each "
      "of the three enumerated readings of sec 4.0. Gate 0, Channel C, Channel D, the question "
      "windows and the reconstruction check are boundary-independent and were computed once, "
      "under the in-force rule, and reused unchanged.\n")
    A(md_table(sens if sens is not None else pd.DataFrame()))
    A("\n**Rule 9.** This block may never be used to select a rule after looking. A different "
      "boundary after this register exists is a look, and is a successor question, never a "
      "re-run of this one. The sec 8 verdict above was computed under `%s` alone.\n"
      % ev["decision_time_rule"])
    A("\nCSV: `%s/boundary_sensitivity.csv`.\n" % res_rel)
    A("## 10. What this register does not say (sec 10)\n")
    A("1. A timestamp is not a per-cell write time; a PASS means no *detectable* post-boundary "
      "write on a read column, not a proof that none occurred.\n"
      "2. A traceless mutation is invisible to Channel A; Channel C only works where an "
      "independent count exists.\n"
      "3. `sas_runs` is updated in place: a re-run night's original 16:05 output is "
      "unrecoverable (EN-001).\n"
      "4. The question list is frozen at the 2026-09-14 lock; a question locked later is not "
      "in this register (sec 9's standing per-freeze re-run closes that gap).\n"
      "5. Materiality depends on each PREREG's own sec 2 being read correctly; section 2.1 "
      "above lists exactly what was extracted so a miss is visible rather than silent.\n"
      "6. Reading the platform repo to attribute a write path is an interpretation; the SHA "
      "read is printed above and every cited literal was verified at it.\n")
    if ev["decision_time_rule"] == "R2_SAME_EVENING":
        A("\n### 10.1 The residual blind spot of the rule in force, per table "
          "(AMENDMENTS.md 2026-09-14, A1)\n")
        A("Under `R2_SAME_EVENING` a write between **16:05 and 23:59:59.999999 ET on night N** "
          "is NOT flagged by the timestamp limb. That band is `n_W_band_R1_R2` in section 3.1 "
          "and is covered -- where it is covered at all -- by three other defences: sec 4.3's "
          "attribution limb (a documented late-write path), Channel C's internal corroboration "
          "(the only channel that sees a traceless mutation, sec 10.2), and sec 4.2's "
          "within-night `W_row` spread. The table below states, per table, which of the three "
          "apply. **Where a table has no independent count, this band rests on attribution "
          "alone for that table.**\n")
        brows = []
        attr_tables = {a["table"] for a in ATTRIBUTION}
        for t in man_tables_of(ev):
            sub = chan_a[(chan_a["table"] == t) & (chan_a["night"].notna())]
            band = int(pd.to_numeric(sub["n_W_band_R1_R2"], errors="coerce").fillna(0).sum()) \
                if len(sub) and "n_W_band_R1_R2" in sub.columns else 0
            has_count = t not in NO_INDEPENDENT_COUNT_TABLES
            brows.append(dict(
                table=t,
                rows_in_band_16_05_to_23_59=band,
                channel_c_independent_count=has_count,
                attributed_late_write_path=(t in attr_tables),
                within_night_W_spread_reported=True,
                band_coverage=("attribution, Channel C and the within-night spread"
                               if has_count else
                               "ATTRIBUTION ALONE -- no independent count exists for this "
                               "table (sec 10.2); a clean Channel A count is not evidence that "
                               "no 16:05..23:59 write occurred")))
        A(md_table(pd.DataFrame(brows)))
        A("\nThis is a limitation of the amended rule. It changes nothing in sec 10 of the "
          "PREREG, which is not edited.\n")
    path.write_text("\n".join(L), encoding="utf-8")


def man_tables_of(ev: dict) -> list:
    """Table names, in manifest order, taken from the preflight evidence (no re-read)."""
    seen, out = set(), []
    for f in ev.get("files", []):
        t = f.get("table")
        if t and t not in seen and t in WRITE_TS:
            seen.add(t)
            out.append(t)
    return out


def extraction_backstop(man: dict) -> pd.DataFrame:
    """sec 10.5 / sec 10.9 backstop: every backticked token in a listed PREREG that names a
    frozen column and is not in that question's transcription is listed for review.  It never
    changes a classification -- it makes a miss visible."""
    cols_by_table = {t["name"]: set(t["columns"]) for t in man["tables"]}
    every_col = set().union(*cols_by_table.values())
    rows = []
    for q in QUESTIONS:
        text = (ROOT / "research" / "questions" / q["dir"] / "PREREG.md").read_text(
            encoding="utf-8")
        toks = set()
        for m in re.findall(r"`([^`]+)`", text):
            for t in re.split(r"[^A-Za-z0-9_]+", m):
                if t in every_col:
                    toks.add(t)
        taken = set()
        for r in q["reads"]:
            cols = cols_by_table[r["table"]] if r["columns"] == ["*"] else set(r["columns"])
            taken |= cols
        for t in sorted(toks - taken):
            rows.append(dict(question=q["id"], token=t,
                             tables=";".join(sorted(k for k, v in cols_by_table.items()
                                                    if t in v)),
                             status="EXTRACTION_REVIEW -- named in the PREREG text, not in the "
                                    "transcription"))
    return pd.DataFrame(rows)


# =============================================================================================
# main
# =============================================================================================

def build_calendar(tables: dict, manp: dict) -> Calendar:
    spl_file = next(t["file"] for t in manp["tables"] if t["name"] == "prices_daily_split")
    spl = pd.read_parquet(norm_path(spl_file), columns=["symbol", "date"])
    spy = spl[spl["symbol"] == "SPY"]["date"]
    src = "SPY bars in prices_daily_split"
    if not len(spy):
        spy = spl["date"]
        src = "all symbols in prices_daily_split (no SPY rows in the freeze)"
    sessions = {pd.Timestamp(x).date() for x in spy}
    n_price = len(sessions)
    for name, df in tables.items():
        if "trading_date" in df.columns and len(df):
            sessions |= {d for d in (to_date(x) for x in df["trading_date"]) if d is not None}
    note = ("%s (%d dates) unioned with every trading_date in the frozen selection tables "
            "(total %d sessions, %s..%s) -- AMENDMENTS.md A4; no exchange calendar package, no "
            "network, no query" % (src, n_price, len(sessions), min(sessions), max(sessions)))
    return Calendar(sorted(sessions), note)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Q026 knowledge-time register (sec 4).")
    ap.add_argument("--manifest", default="research/data/manifest_v001.json")
    ap.add_argument("--manifest-prices", default="research/data/manifest_prices_v001.json")
    ap.add_argument("--codebase", default=os.environ.get(
        "CODEBASE_DIR", r"C:/Users/sahin/Projects/volatilx"))
    ap.add_argument("--register", default=None,
                    help="default research/reports/KT_REGISTER_<manifest stem>.md (sec 9)")
    ap.add_argument("--results", default=None,
                    help="default <question dir>/results")
    args = ap.parse_args(argv)

    res = Path(args.results) if args.results else (QDIR / "results")
    res.mkdir(parents=True, exist_ok=True)
    res_rel = str(res.relative_to(ROOT)).replace("\\", "/") if str(res).startswith(str(ROOT)) \
        else str(res)

    try:
        ev, man, manp = preflight(args)
    except Abort as exc:
        block = dict(question="Q026", verdict="ABORTED", controller_verdict=None,
                     label="HISTORICAL_ONLY", reason=str(exc))
        print(json.dumps(block, indent=2))
        return 2

    reg_path = Path(args.register) if args.register else (
        ROOT / "research" / "reports" / ("KT_REGISTER_%s.md" % Path(args.manifest).stem))
    reg_path.parent.mkdir(parents=True, exist_ok=True)

    rule = DECISION_TIME_RULE
    tables = load_tables(man)
    for t in man["tables"]:                    # census completeness (sec 2.2)
        if t.get("rows") is not None and len(tables[t["name"]]) != int(t["rows"]):
            raise Abort("%s has %d rows, manifest declares %d"
                        % (t["name"], len(tables[t["name"]]), t["rows"]))
    cal = build_calendar(tables, manp)
    census_nights = {name: sorted({d for d in (to_date(x) for x in df["trading_date"])
                                   if d is not None}) if len(df) else []
                     for name, df in tables.items()}

    chan_a = channel_a(tables, man, cal, rule)
    chan_c = channel_c(tables)
    gate = gate0(tables, man, cal, rule, chan_a, chan_c)

    # ---- A1r item 1 / item 3: the boundary bands and A12's R3 fallback count.  Both are
    # descriptive and are produced whether or not Gate 0 passes.
    bands = boundary_band_totals(chan_a)
    all_census_nights = sorted(set().union(*[set(v) for v in census_nights.values()])
                               if census_nights else set())
    a12_nights = [n.isoformat() for n in all_census_nights if r3_fallback_fired(n, cal)]
    a12 = dict(n_nights=len(a12_nights), nights=a12_nights,
               scope=("R3 sensitivity column only -- AMENDMENTS.md 2026-09-14, A12 as narrowed "
                      "by A1's resolution; it cannot touch the sec 8 verdict under R2"))

    # ---- Gate 0 first, read first (sec 4.1).  On failure nothing else is computed (sec 8).
    if not gate["passed"]:
        ver = verdict(gate, pd.DataFrame(columns=["klass", "question", "column", "night",
                                                  "reason"]), {}, pd.DataFrame())
        (res / "gate0.json").write_text(json.dumps(gate, indent=1, default=str), encoding="utf-8")
        chan_a.to_csv(res / "channel_a.csv", index=False)
        for k, g in bands.items():
            g.to_csv(res / ("boundary_bands_%s.csv" % k), index=False)
        write_register(reg_path, ev, gate, chan_a, pd.DataFrame(), pd.DataFrame(), chan_c,
                       pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {},
                       pd.DataFrame(), {}, ver, {}, {}, cal, res_rel,
                       bands=bands, sens=None, a12=a12, scoped_reads=None)
        summary = dict(question="Q026", n_nights=len(census_nights.get("sas_runs", [])),
                       n_nights_excluded=0, mean_oos=None, ci=None, p_perm=None, mpe=None,
                       verdict=ver["verdict"], controller_verdict=ver["controller_verdict"],
                       label="HISTORICAL_ONLY", gate0_passed=False,
                       gate0_failed_checks=[c["id"] for c in gate["checks"]
                                            if not c["passed"]],
                       decision_time_rule=rule,
                       decision_time_rule_amendment=DECISION_TIME_RULE_AMENDMENT,
                       a12_r3_fallback_nights=a12["n_nights"],
                       register=str(reg_path.relative_to(ROOT)).replace("\\", "/"),
                       statement=ver["statement"],
                       note="sec 4.7: no estimate, no CI, no p-value, no MPE. Every number is "
                            "NON_QUOTABLE.")
        (res / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(json.dumps(summary, indent=2))
        return 0

    # ---- attribution literals, verified at the frozen SHA (sec 4.3, sec 10.6).
    codebase = Path(args.codebase).resolve()
    verified = {}
    for a in ATTRIBUTION:
        if a.get("repo"):
            verified[a["id"]] = verify_repo_literal(codebase, a["repo"]["path"],
                                                    a["repo"]["lines"], a["repo"]["literal"])
    for table, lw in LATER_WRITE_SETS.items():
        for e in lw["evidence"]:
            verified["%s:%s:%s" % (table, e["path"], e["lines"])] = verify_repo_literal(
                codebase, e["path"], e["lines"], e["literal"])
    # AMENDMENTS.md 2026-09-14, A6 RIDER -- the closed divisor set, literal by literal, at its
    # cited line range at the frozen SHA.  If any one is absent the A6 check cannot be
    # evaluated, the reconstruction tuple is MATERIAL (decision 2's failure branch) and the
    # withdrawal is printed with A9's (sec 10.6).
    _cit = OI_MULT_SET_CITATION
    for lit in _cit["literals"]:
        verified["%s:%s" % (_cit["key_prefix"], lit)] = verify_repo_literal(
            codebase, _cit["path"], _cit["lines"], lit)
    mult_set_ok = all(verified["%s:%s" % (_cit["key_prefix"], lit)]["ok"]
                      for lit in _cit["literals"])
    mult_set_detail = "; ".join(
        "%s: %s" % (lit, "found" if verified["%s:%s" % (_cit["key_prefix"], lit)]["ok"]
                    else "NOT FOUND")
        for lit in _cit["literals"])

    qwin = question_windows(cal, census_nights)
    stats = night_stats(tables, man, cal, rule)

    recon = {}
    for q in QUESTIONS:
        if q.get("reconstruction"):
            rec = q["reconstruction"]
            nights = qwin[q["id"]]["per_read"][
                (rec["table"], tuple(next(r["columns"] for r in q["reads"]
                                          if r["table"] == rec["table"])))]
            recon[q["id"]] = check_reconstruction(tables[rec["table"]], nights, rec,
                                                  mult_set_ok=mult_set_ok,
                                                  mult_set_detail=mult_set_detail)
            recon[q["id"]]["cite"] = rec["cite"]

    chan_d, changes, appendix = channel_d(tables, manp, qwin)
    tuples, class_counts = channel_b(tables, man, cal, rule, stats, qwin, chan_c, chan_d,
                                     verified, recon, census_nights)
    read_index = defaultdict(set)
    for _, r in tuples[tuples["as_feature"] == True].iterrows():    # noqa: E712
        read_index[(r["table"], r["column"])].add(r["question"])
    chan_e, proposal = channel_e(man, chan_a, read_index)
    nightly = nightly_frame(tuples, chan_a, census_nights, qwin)
    splits = split_tables(nightly)
    ver = verdict(gate, tuples, qwin, chan_d, rule)
    review = extraction_backstop(man)

    # ---- A1r item 2 -- DESCRIPTIVE boundary sensitivity.  Computed after the verdict above,
    # which is fixed under the in-force rule and is not revisited (rule 9).
    sens = boundary_sensitivity(tables, man, cal, gate, qwin, chan_c, chan_d, verified, recon,
                                census_nights, rule, tuples, ver)

    # ---- A7 rider -- every as_feature=False column, itemised with its scoping PREREG sentence.
    _cols_of = {t["name"]: list(t["columns"]) for t in man["tables"]}
    scoped_rows = []
    for q in QUESTIONS:
        for r in q["reads"]:
            if r.get("as_feature", True):
                continue
            cols = _cols_of[r["table"]] if r["columns"] == ["*"] else r["columns"]
            for c in cols:
                scoped_rows.append(dict(
                    question=q["id"], table=r["table"], column=c,
                    as_feature=False, class_count_label="IMMATERIAL_BY_SCOPE",
                    scoping_prereg_sentence=r.get("note", ""),
                    columns_declared=",".join(r["columns"]), citation=q["cite"]))
    scoped_reads = pd.DataFrame(scoped_rows)

    # ---- outputs
    (res / "gate0.json").write_text(json.dumps(gate, indent=1, default=str), encoding="utf-8")
    chan_a.to_csv(res / "channel_a.csv", index=False)
    chan_c.to_csv(res / "channel_c.csv", index=False)
    chan_e.to_csv(res / "channel_e.csv", index=False)
    class_counts.to_csv(res / "channel_b_class_counts.csv", index=False)
    tuples.to_csv(res / "channel_b_tuples.csv", index=False)
    for klass, fname in (("MATERIAL", "material"), ("MATERIAL_MITIGATED", "material_mitigated"),
                         ("CONTAMINATION_UNRESOLVED", "contamination_unresolved"),
                         ("ADVISORY", "advisory")):
        tuples[tuples["klass"] == klass].to_csv(res / ("channel_b_%s.csv" % fname), index=False)
    chan_d.to_csv(res / "channel_d_material.csv", index=False)
    changes.to_csv(res / "channel_d_split_factor_changes.csv", index=False)
    appendix.to_csv(res / "channel_d_correction_appendix.csv", index=False)
    nightly.to_csv(res / "nightly.csv", index=False)
    review.to_csv(res / "extraction_review.csv", index=False)
    for k, g in bands.items():                       # A1r item 1
        g.to_csv(res / ("boundary_bands_%s.csv" % k), index=False)
    sens.to_csv(res / "boundary_sensitivity.csv", index=False)          # A1r item 2
    scoped_reads.to_csv(res / "as_feature_false_scoped.csv", index=False)   # A7 rider
    (res / "a12_r3_fallback.json").write_text(json.dumps(a12, indent=1), encoding="utf-8")
    for k, g in splits.items():
        g.to_csv(res / ("split_%s.csv" % re.sub(r"[^A-Za-z0-9_.-]", "_", k)), index=False)
    (res / "proposed_availability_block.json").write_text(
        json.dumps(proposal, indent=1, default=str), encoding="utf-8")
    (res / "preflight.json").write_text(json.dumps(ev, indent=1, default=str), encoding="utf-8")
    (res / "reconstruction.json").write_text(json.dumps(recon, indent=1, default=str),
                                             encoding="utf-8")

    write_register(reg_path, ev, gate, chan_a, tuples, class_counts, chan_c, chan_d, changes,
                   appendix, chan_e, proposal, nightly, splits, ver, recon, verified, cal,
                   res_rel, bands=bands, sens=sens, a12=a12, scoped_reads=scoped_reads)

    n_nights = len(census_nights.get("sas_runs", []))
    n_excl_all = int(nightly["out_of_every_window_or_excluded"].sum()) if len(nightly) else 0
    summary = dict(
        question="Q026", type="DIAGNOSTIC_CENSUS",
        n_nights=n_nights,
        n_nights_excluded=n_excl_all,
        mean_oos=None, ci=None, p_perm=None, mpe=None,
        verdict=ver["verdict"], controller_verdict=ver["controller_verdict"],
        label="HISTORICAL_ONLY", quotable=False,
        gate0_passed=True,
        M=ver["M"], MM_verified=ver["MM_verified"], MM_failed=ver["MM_failed"], U=ver["U"],
        advisory=ver["advisory"], questions_touched=ver["questions_touched"],
        stop_the_desk=ver["stop_the_desk"], stop_limbs=ver["stop_limbs"],
        channel_d_material_rows=ver["channel_d_material_rows"],
        decision_time_rule=rule, decision_time_rule_amendment=DECISION_TIME_RULE_AMENDMENT,
        decision_time_boundary=RULE_BOUNDARY_TEXT[rule],
        a12_r3_fallback_nights=a12["n_nights"], a12_scope=a12["scope"],
        oi_mult_set_verified_at_sha=bool(mult_set_ok),
        boundary_sensitivity_heading=SENSITIVITY_HEADING,
        boundary_sensitivity=json.loads(sens.to_json(orient="records")),
        platform_sha_read=PLATFORM_SHA,
        register=str(reg_path.relative_to(ROOT)).replace("\\", "/"),
        statement=ver["statement"],
        note=("sec 4.7: no estimate, no standard error, no bootstrap, no permutation, no "
              "p-value, no BH, no CI, no MPE, no episode clustering (DP-51 inapplicable). "
              "Every number is NON_QUOTABLE (rule 12) and HISTORICAL_ONLY (sec 9)."))
    (res / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    sm = ["# Q026 -- run summary (NON_QUOTABLE, HISTORICAL_ONLY)\n",
          "Verdict per the PREREG sec 8 decision rule: **%s** (controller `%s`).\n"
          % (ver["verdict"], ver["controller_verdict"]),
          ver["statement"] + "\n",
          "- Gate 0: PASSED (sec 4.1, read first).",
          "- n per cell: see `nightly.csv` and `split_*.csv`; cells below %d nights are "
          "flagged LOW_N and no trend is read from them." % LOW_N_FLOOR,
          "- Metric: a count of rows in a sha256-pinned file. **No CI, no raw p, no BH q** -- "
          "sec 4.7 and sec 7: this question has no primary endpoint and enters no BH set.",
          "- M = %s, MM verified = %s, MM failed = %s, U = %s, ADVISORY = %s."
          % (ver["M"], ver["MM_verified"], ver["MM_failed"], ver["U"], ver["advisory"]),
          "- STOP-THE-DESK: %s" % ("YES -- " + " ; ".join(ver["stop_limbs"])
                                   if ver["stop_the_desk"] else "no"),
          "- Decision-time boundary: **%s** -- %s. Amendment: %s."
          % (rule, RULE_BOUNDARY_TEXT[rule], DECISION_TIME_RULE_AMENDMENT),
          "- A12 R3 fallback fired on %d night(s); %s." % (a12["n_nights"], a12["scope"]),
          "- Boundary sensitivity (%s): see `boundary_sensitivity.csv` and register section 9. "
          "The band counts under all three rules are in `channel_a.csv`, "
          "`boundary_bands_by_table.csv`, `boundary_bands_by_month.csv` and "
          "`boundary_bands_overall.csv`." % SENSITIVITY_HEADING,
          "- Register: `%s`" % summary["register"],
          "- Regime breakdown: sec 6 forbids stratifying by `market_regime_daily` before "
          "2026-06-09 (it is one of the objects under audit); the calendar panel, the three "
          "registered boundaries and the in-sample/out-of-sample cut are in `split_*.csv`.",
          "- No cell is suppressed for an n floor: the census reads every night and every row "
          "(sec 5.1)."]
    (res / "SUMMARY.md").write_text("\n".join(sm) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Abort as exc:
        print(json.dumps(dict(question="Q026", verdict="ABORTED", reason=str(exc)), indent=2))
        sys.exit(2)
