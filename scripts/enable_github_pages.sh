#!/usr/bin/env bash
set -euo pipefail

OWNER="${1:?Usage: scripts/enable_github_pages.sh OWNER REPO [BRANCH]}"
REPO="${2:?Usage: scripts/enable_github_pages.sh OWNER REPO [BRANCH]}"
BRANCH="${3:-main}"

if ! command -v gh >/dev/null 2>&1; then
    echo "GitHub CLI 'gh' is required: https://cli.github.com/" >&2
    exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
    echo "Run 'gh auth login' first." >&2
    exit 1
fi

payload=$(printf '{"build_type":"legacy","source":{"branch":"%s","path":"/"}}' "$BRANCH")

if gh api --method POST "repos/$OWNER/$REPO/pages" \
        -H "Accept: application/vnd.github+json" \
        --input - <<< "$payload" >/dev/null; then
    echo "Created GitHub Pages site for $OWNER/$REPO from $BRANCH:/"
else
    gh api --method PUT "repos/$OWNER/$REPO/pages" \
        -H "Accept: application/vnd.github+json" \
        --input - <<< "$payload" >/dev/null
    echo "Updated GitHub Pages site for $OWNER/$REPO to $BRANCH:/"
fi
