#!/bin/bash
# Refresh all currently and future public PAL Actors, without paid runs or Store edits.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK="$ROOT/.catalog-update.lock"
mkdir "$LOCK" 2>/dev/null || { echo "CATALOG_UPDATE_ALREADY_RUNNING"; exit 0; }
trap 'rmdir "$LOCK" 2>/dev/null || :' EXIT
cd "$ROOT"
if ! /usr/bin/git diff --quiet -- catalog.html example-tasks.html examples-directory-public-manifest.json scripts/generate_catalog.py scripts/generate_public_example_tasks.py; then
  echo "CATALOG_LOCAL_CHANGES_NEED_REVIEW"; exit 1
fi
/usr/bin/git fetch --quiet origin main
if ! /usr/bin/git merge-base --is-ancestor HEAD origin/main; then
  echo "CATALOG_REMOTE_CONFLICT_NEEDS_REVIEW"; exit 1
fi
/usr/bin/git merge --ff-only origin/main
/usr/bin/python3 scripts/generate_public_example_tasks.py
/usr/bin/python3 scripts/generate_catalog.py
if /usr/bin/git diff --quiet -- catalog.html example-tasks.html examples-directory-public-manifest.json; then
  echo "CATALOG_UNCHANGED"; exit 0
fi
/usr/bin/git add -- catalog.html example-tasks.html examples-directory-public-manifest.json
/usr/bin/git -c user.name="Practical AI Lab" -c user.email="319231112+jojoagogog-beep@users.noreply.github.com" commit -m "Refresh published PAL Actors and public example tasks" -- catalog.html example-tasks.html examples-directory-public-manifest.json
/usr/bin/git push https://github.com/jojoagogog-beep/ecommerce-jsonld-qa-checklist.git HEAD:main
echo "CATALOG_UPDATED_AND_PUSHED"
