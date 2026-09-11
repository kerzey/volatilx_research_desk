#!/usr/bin/env bash
# Reproduce EXPLORE_001 end to end (in-sample only). Run from the research-desk root.
set -euo pipefail
S=research/reports/explore/scripts
L=research/reports/explore/work/logs
mkdir -p "$L"
for f in 00_inspect 01_inspect_payloads 02_inspect_prices 03_build_core 04_sanity 05_spot_check 05b_spot_check \
         06_run_lateness 10_paths 20_theme_A_distance 21_theme_A_matched 30_theme_B_entry 40_theme_C_shape \
         41_earnings_check 50_theme_D_vol 60_theme_E_spreads 69_inspect_aux 70_seeds 71_uoa_labels 80_extras 81_speed; do
  echo "== $f"; python "$S/$f.py" > "$L/$f.log" 2>&1
done
