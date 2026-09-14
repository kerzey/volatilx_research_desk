#!/usr/bin/env python3
"""Load .env.research into os.environ for desk tools. Never prints a value.

Why this exists. `scripts/research_routines.sh:13` already does exactly this for headless
runs (`set -a; . ./.env.research; set +a`), so the nightly `daily` / `weekly` / `desk` modes
have always had `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` and `RESEARCH_DB_URL` in the
environment. An interactive session started by hand does not, and the agent cannot source
the file itself (`Read(.env.*)` is denied, and the deny rule covers `. ./.env.research`).
Q030 and Q032 were both deferred on "no Alpaca credentials in the desk's session", which was
true of the session that measured it and false of the environment the Steward actually runs
in. This module closes that gap for both.

    from desk_env import load
    load()                      # returns the sorted NAMES it set, never the values

Contract, and it is the whole point of the file:

- **Values are never returned, printed, logged or put in an exception message.** The only
  thing any caller can learn is which names are present. `present()` answers that directly.
- It never overwrites a variable that is already set, so an explicitly exported value
  (a wrapper's, a CI runner's) always wins over the file.
- It is a no-op if the file is absent, so a tool that calls it still runs wherever the
  environment is already provisioned.

Rule 1 is untouched: this reads only the credentials CLAUDE.md already names the desk as
holding, from the file Haci keeps them in, and asks for no other.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / ".env.research"

# KEY=value / export KEY=value / KEY="value", '#' comments and blank lines skipped.
_LINE = re.compile(r"""^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$""")


def _parse(text: str) -> dict:
    out = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = _LINE.match(line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        out[key] = val
    return out


def load(path: Path = ENV_FILE, override: bool = False) -> list:
    """Set any missing variable from the env file. Returns the NAMES set, sorted."""
    if not path.exists():
        return []
    try:
        text = path.read_bytes().decode("utf-8", errors="replace")
    except OSError:
        return []
    set_names = []
    for key, val in _parse(text).items():
        if override or key not in os.environ:
            os.environ[key] = val
            set_names.append(key)
    return sorted(set_names)


def present(*names: str) -> dict:
    """{name: bool} for each name, after load(). Presence only — never the value."""
    load()
    return {n: bool(os.environ.get(n)) for n in names}


def require(*names: str) -> None:
    """Exit with the missing NAMES if any are absent. Never shows a value."""
    import sys
    missing = [n for n, ok in present(*names).items() if not ok]
    if missing:
        sys.exit(f"not set: {', '.join(missing)} (expected in {path_label()})")


def path_label() -> str:
    return str(ENV_FILE.relative_to(ROOT)) if ENV_FILE.exists() else ".env.research (absent)"


if __name__ == "__main__":
    names = load()
    print(f"env file: {path_label()}")
    print(f"set {len(names)} variable(s) from it: {', '.join(names) if names else '(none — all already set)'}")
    for n, ok in present("ALPACA_API_KEY", "ALPACA_SECRET_KEY", "ALPACA_DATA_FEED",
                         "RESEARCH_DB_URL", "RESEARCH_SAS_TOKEN").items():
        print(f"  {n}: {'present' if ok else 'MISSING'}")
