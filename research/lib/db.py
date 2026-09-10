#!/usr/bin/env python
"""Read-only query helper (replaces psql on machines without it).
Usage: python research/lib/db.py "SELECT count(*) FROM super_agent_select_runs"
       python research/lib/db.py --describe super_agent_select_candidates_daily
Uses RESEARCH_DB_URL only; opens the session read-only regardless of the role's grants."""
import os, sys
import pandas as pd
import psycopg

url = os.environ.get("RESEARCH_DB_URL") or sys.exit("RESEARCH_DB_URL not set")
args = sys.argv[1:]
if not args: sys.exit(__doc__)
if args[0] == "--describe":
    sql = f"""SELECT column_name, data_type, is_nullable FROM information_schema.columns
              WHERE table_name = '{args[1]}' ORDER BY ordinal_position"""
else:
    sql = " ".join(args)
    if not sql.lstrip().lower().startswith(("select", "with", "explain", "show", "\\d")):
        sys.exit("read-only helper: query must start with SELECT/WITH/EXPLAIN")
with psycopg.connect(url, options="-c default_transaction_read_only=on") as conn:
    df = pd.read_sql(sql, conn)
pd.set_option("display.width", 200); pd.set_option("display.max_columns", 60)
print(df.to_string(index=False) if len(df) <= 200 else df.head(200).to_string(index=False) + f"\n... {len(df)} rows")
