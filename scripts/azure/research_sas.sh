#!/usr/bin/env bash
# Creates the `research` container and prints two scoped SAS tokens.
# Usage: ACCOUNT=volatilxstorage PROD_CONTAINER=volatilx ./scripts/azure/research_sas.sh
set -euo pipefail
: "${ACCOUNT:?set ACCOUNT}"; : "${PROD_CONTAINER:?set PROD_CONTAINER}"
EXPIRY=$(date -u -d '+90 days' +%Y-%m-%dT%H:%MZ 2>/dev/null || date -u -v+90d +%Y-%m-%dT%H:%MZ)

az storage container create --account-name "$ACCOUNT" --name research --auth-mode login >/dev/null

echo "PROD_BLOB_SAS (read+list only, expires $EXPIRY):"
az storage container generate-sas --account-name "$ACCOUNT" --name "$PROD_CONTAINER" \
  --permissions rl --expiry "$EXPIRY" --auth-mode login --as-user -o tsv
echo
echo "RESEARCH_BLOB_SAS (read/write/list/create, expires $EXPIRY):"
az storage container generate-sas --account-name "$ACCOUNT" --name research \
  --permissions rwlc --expiry "$EXPIRY" --auth-mode login --as-user -o tsv
echo
echo "Check: the following upload to prod MUST fail with 403"
echo "  az storage blob upload --account-name $ACCOUNT -c $PROD_CONTAINER -n _probe.txt -f /dev/null --sas-token \"\$PROD_BLOB_SAS\""
