"""EXPLORE_001 step 0: inspect in-sample tables (in-sample split only)."""
import json, sys
import pandas as pd
sys.path.insert(0, "research/lib")
import eval_utils as eu
M = "research/data/manifest_v001.json"
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 80)
cand = eu.load_split(M, "in_sample", name="sas_candidates")
print("cand", cand.shape, cand.trading_date.min(), cand.trading_date.max())
pub = cand[cand.qualification_reason == "selected"]
print("published", len(pub), "nights", pub.trading_date.nunique(), "elite", (pub.overall_score >= 90).sum())
print(cand.qualification_reason.value_counts().head(20))
print(pub[["overall_score","dominant_direction","best_timeframe","selected_rank"]].describe(include="all"))
print(pub.dominant_direction.value_counts(), pub.best_timeframe.value_counts())
print("candidates per night", cand.groupby("trading_date").size().describe())
r = pub.iloc[0]
pp = json.loads(r.public_payload_json) if isinstance(r.public_payload_json, str) else r.public_payload_json
print(json.dumps(pp, indent=1, default=str)[:3000])
sp = json.loads(r.source_payloads_json) if isinstance(r.source_payloads_json, str) else r.source_payloads_json
print("SOURCE keys", list(sp.keys()) if isinstance(sp, dict) else type(sp))
print(json.dumps(sp, indent=1, default=str)[:5000])
ex = eu.load_split(M, "in_sample", name="sas_excursion")
print("excursion", ex.shape, ex.computation_version.value_counts())
print(ex.columns.tolist())
