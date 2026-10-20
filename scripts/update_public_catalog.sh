#!/bin/bash
# Public store catalog refresh: safe weekly, no Actor runs or paid actions.
set -euo pipefail
ROOT="$HOME/Projects/pal-ecommerce-schema-guide"
LOCK="$ROOT/.catalog-update.lock"
mkdir "$LOCK" 2>/dev/null || { echo "CATALOG_UPDATE_ALREADY_RUNNING"; exit 0; }
trap 'rmdir "$LOCK" 2>/dev/null || :' EXIT
cd "$ROOT"
/usr/bin/python3 scripts/generate_catalog.py
if /usr/bin/git diff --quiet -- catalog.html; then
  echo "CATALOG_UNCHANGED"
  exit 0
fi
/usr/bin/git add -- catalog.html
/usr/bin/git -c user.name="Practical AI Lab" -c user.email="319231112+jojoagogog-beep@users.noreply.github.com" commit -m "Refresh published PAL Apify Actors catalog" -- catalog.html
/usr/bin/git push origin main
echo "CATALOG_UPDATED_AND_PUSHED"
