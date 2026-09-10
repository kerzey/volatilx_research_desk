#!/usr/bin/env python3
"""Independent second-opinion review of a research run using the OpenAI API.

The Red Team calls this so the critique comes from a different model family than the
one that wrote eval.py. The model sees PREREG.md, eval.py and results/SUMMARY.md only.

Usage: python scripts/second_opinion.py --question Q001
Env:   OPENAI_API_KEY, OPENAI_REVIEW_MODEL (default set below; change to the current
       strongest reasoning model available to your account).
"""
import argparse
import os
import sys
from pathlib import Path

from openai import OpenAI

MODEL = os.environ.get("OPENAI_REVIEW_MODEL", "gpt-6-astra")

PROMPT = """You are an adversarial reviewer for a quantitative trading research study.
You will receive a pre-registration document, the evaluation script, and the results summary.
Your job is to find reasons the CONFIRMED/NULL verdict could be wrong. Be specific and cite
line numbers from eval.py. Cover: look-ahead bias, denominator/survivorship problems,
baseline mismatch, regime confounding, multiple-testing inflation, effect size vs slippage,
and whether the exit rule is executable by a retail trader. End with one line:
SECOND OPINION: AGREE | DISAGREE | CANNOT TELL, and one sentence why."""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    a = ap.parse_args()
    qdir = next(Path("research/questions").glob(f"{a.question}_*"), None)
    if not qdir:
        sys.exit(f"no question dir for {a.question}")
    parts = []
    for rel in ("PREREG.md", "eval.py", "results/SUMMARY.md"):
        p = qdir / rel
        parts.append(f"\n\n===== {rel} =====\n" + (p.read_text() if p.exists() else "(missing)"))
    client = OpenAI()
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": PROMPT},
                  {"role": "user", "content": "".join(parts)}],
    )
    text = resp.choices[0].message.content
    out = qdir / "results" / "SECOND_OPINION.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"# Second opinion ({MODEL})\n\n{text}\n")
    print(text)


if __name__ == "__main__":
    main()
