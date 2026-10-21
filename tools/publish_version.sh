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
# It replaces the folder with the branch's site files (no tests, tools, docs or skills), then commits.
set -euo pipefail
branch="${1:?branch name}"; folder="${2:?folder: preview or final}"
case "$folder" in preview|final) ;; *) echo "The folder must be preview or final." >&2; exit 1 ;; esac
[ "$(git rev-parse --abbrev-ref HEAD)" = "main" ] || { echo "Check out main first." >&2; exit 1; }
git fetch origin "$branch"
rm -rf "$folder"; mkdir "$folder"
git archive "origin/$branch" | tar -x -C "$folder" \
  --exclude='.claude' --exclude='tests' --exclude='tools' --exclude='docs' --exclude='.github' \
  --exclude='preview' --exclude='final' --exclude='*.md'
git add -A "$folder"
git commit -m "Publish $branch to /$folder/ ($(git rev-parse --short "origin/$branch"))" || echo "Nothing changed."
echo "Done. Push with: git push origin main"
