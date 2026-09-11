#!/usr/bin/env bash
# OS-level containment for the research desk. Hooks are policy; this is enforcement.
# Creates a dedicated Unix user that can READ the repo but WRITE only under research/ and .claude/ caches.
# Run once as root/sudo on the machine that runs Claude Code for research. Re-run after `git pull`
# if new top-level directories appear.
#
# Usage: sudo REPO=/path/to/volatilx ./scripts/setup_sandbox.sh
# Then run the desk as:  sudo -u vxresearch -i bash -c 'cd $REPO && claude'
set -euo pipefail
: "${REPO:?set REPO}"
USER_NAME=vxresearch
GROUP_NAME=vxresearch

id -u "$USER_NAME" &>/dev/null || useradd -m -s /bin/bash "$USER_NAME"
getent group "$GROUP_NAME" >/dev/null || groupadd "$GROUP_NAME"

# Whole repo: owner keeps rw; research user read-only via ACL.
setfacl -R -m u:$USER_NAME:rX "$REPO"
setfacl -R -d -m u:$USER_NAME:rX "$REPO"

# Writable islands. research/lib and research/data are read-only even here (steward writes data via a
# separate freeze invocation run by you, or grant research/data explicitly below).
for d in research/questions research/reports research/BACKLOG.md research/LEDGER.md docs/research; do
  mkdir -p "$(dirname "$REPO/$d")"; [ -e "$REPO/$d" ] || { [[ "$d" == *.md ]] && touch "$REPO/$d" || mkdir -p "$REPO/$d"; }
  setfacl -R -m u:$USER_NAME:rwX "$REPO/$d"
  setfacl -R -d -m u:$USER_NAME:rwX "$REPO/$d" 2>/dev/null || true
done
# Data freeze: allow writes only to parquet/manifests dir (steward), not to lib code.
setfacl -R -m u:$USER_NAME:rwX "$REPO/research/data"
setfacl -R -d -m u:$USER_NAME:rwX "$REPO/research/data"

# Explicitly deny writes to enforcement code and to the app.
for d in .claude research/lib services scripts tests app.py; do
  [ -e "$REPO/$d" ] && setfacl -R -m u:$USER_NAME:rX "$REPO/$d" || true
done

# .git: read for status/log; block direct object writes. Commits by the desk happen via a
# separate committer step you run (or grant .git rw to a second 'vximplementer' user only).
setfacl -R -m u:$USER_NAME:rX "$REPO/.git"

# Secrets never readable by the desk.
[ -f "$REPO/.env" ] && setfacl -m u:$USER_NAME:--- "$REPO/.env" || true
# The desk gets its own env with only the research credentials:
install -m 600 -o $USER_NAME -g $GROUP_NAME /dev/null /home/$USER_NAME/.research.env
echo "# fill: RESEARCH_DB_URL, PROD_SAS_TOKEN, RESEARCH_SAS_TOKEN, OPENAI_API_KEY" > /home/$USER_NAME/.research.env

echo "sandbox user $USER_NAME configured. Verify:"
echo "  sudo -u $USER_NAME touch $REPO/services/_probe   # must fail"
echo "  sudo -u $USER_NAME touch $REPO/research/questions/_probe && rm $REPO/research/questions/_probe   # must succeed"
echo "Alternative: run the desk in a container with services/ scripts/ .claude/ mounted :ro and research/ mounted rw."
