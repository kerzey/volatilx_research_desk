"""EXPLORE_001 step 1: payload structure — lane_plans, atr14 location, context_json keys."""
import json, sys, re, collections
import pandas as pd
sys.path.insert(0, "research/lib")
import eval_utils as eu
M = "research/data/manifest_v001.json"
cand = eu.load_split(M, "in_sample", name="sas_candidates")
pub = cand[cand.qualification_reason == "selected"]
def J(x):
    if x is None: return None
    return json.loads(x) if isinstance(x, str) else x
r = pub.iloc[0]
pp = J(r.public_payload_json)
print(json.dumps(pp.get("lane_plans"), indent=1))
print("PP keys", list(pp.keys()))
# find atr in source payloads
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o[:3]):
            yield from walk(v, path + f"[{i}]")
    else:
        yield path, o
cnt = collections.Counter()
for _, row in cand.sample(300, random_state=1).iterrows():
    sp = J(row.source_payloads_json) or {}
    for p, v in walk(sp):
        p2 = re.sub(r"\[\d+\]", "[]", p)
        if re.search(r"atr|spot|close|beta|earn|gex|regime|pin|sector|premium|iv", p2, re.I):
            cnt[p2] += 1
for k, v in cnt.most_common(80): print(v, k)
print("source membership keys:", collections.Counter(k for x in cand.source_payloads_json for k in (J(x) or {}).keys()))
ctx = J(pub.iloc[0].context_json)
print("CONTEXT keys", list(ctx.keys()))
for k, v in ctx.items():
    print(k, json.dumps(v, default=str)[:600])
sd = J(pub.iloc[0].score_details_json)
print("SCORE DETAILS", json.dumps(sd, default=str)[:3000])
