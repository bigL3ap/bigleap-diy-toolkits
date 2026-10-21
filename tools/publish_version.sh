#!/usr/bin/env bash
# Publish a branch into a folder of the GitHub Pages site, so it can be compared with the original
# using the "Original / Updated / Final" switch at the top of every page (assets/version-switch.js).
#
#   main                                 -> /          Original (what's live today)
#   feature/diy-optimization-buildout    -> /preview/  Updated, in review
#   final                                -> /final/    Final, approved
#
# Run from a clone, with main checked out and up to date:
#   tools/publish_version.sh feature/diy-optimization-buildout preview
#   tools/publish_version.sh final final
#   git push origin main
#
# It replaces the folder with the branch's site files (no tests, tools, docs or skills), lists the version
# in versions.json at the site root (which the switch reads), then commits.
set -euo pipefail
branch="${1:?branch name}"; folder="${2:?folder: preview or final}"
case "$folder" in preview|final) ;; *) echo "The folder must be preview or final." >&2; exit 1 ;; esac
[ "$(git rev-parse --abbrev-ref HEAD)" = "main" ] || { echo "Check out main first." >&2; exit 1; }
git fetch origin "$branch"
rev=$(git rev-parse FETCH_HEAD)          # works in single-branch and shallow clones too
rm -rf "$folder"; mkdir "$folder"
git archive "$rev" | tar -x -C "$folder" \
  --exclude='.claude' --exclude='tests' --exclude='tools' --exclude='docs' --exclude='.github' \
  --exclude='preview' --exclude='final' --exclude='*.md'
# list the version in versions.json at the site root, so the switch offers it
id=$([ "$folder" = preview ] && echo updated || echo final)
python3 - "$id" <<'PY'
import json, sys
p = 'versions.json'
try: d = json.load(open(p))
except Exception: d = {"published": ["original"]}
pub = d.setdefault("published", ["original"])
if "original" not in pub: pub.insert(0, "original")
if sys.argv[1] not in pub: pub.append(sys.argv[1])
d["published"] = [v for v in ["original", "updated", "final"] if v in pub]
json.dump(d, open(p, "w"), indent=2); open(p, "a").write("\n")
PY
git add -A "$folder" versions.json
git commit -m "Publish $branch to /$folder/ (${rev:0:7})" || echo "Nothing changed."
echo "Done. Push with: git push origin main"
