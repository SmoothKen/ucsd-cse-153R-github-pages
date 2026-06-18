#!/usr/bin/env bash
set -euo pipefail

# Enable GitHub Pages for the current repo.
# Defaults match update_github_repo() in audio_snippets.sh:
#   origin: git@github.com:SmoothKen/$(basename "$PWD")
#   branch: master
#   source path: /
#
# Common use after update_github_repo:
#   scripts/enable_github_pages.sh
#
# Optional forms:
#   scripts/enable_github_pages.sh main
#   scripts/enable_github_pages.sh master /docs
#   scripts/enable_github_pages.sh SmoothKen ucsd-cse-190-github-pages
#   scripts/enable_github_pages.sh SmoothKen ucsd-cse-190-github-pages master /
#   scripts/enable_github_pages.sh git@github.com:SmoothKen/ucsd-cse-190-github-pages master /

usage() {
    cat >&2 <<'USAGE'
Usage:
    scripts/enable_github_pages.sh
    scripts/enable_github_pages.sh [BRANCH]
    scripts/enable_github_pages.sh [BRANCH] [/|/docs]
    scripts/enable_github_pages.sh OWNER REPO [BRANCH] [/|/docs]
    scripts/enable_github_pages.sh OWNER/REPO [BRANCH] [/|/docs]
    scripts/enable_github_pages.sh git@github.com:OWNER/REPO[.git] [BRANCH] [/|/docs]

Defaults:
    OWNER/REPO  inferred from git remote origin, or SmoothKen/$(basename "$PWD")
    BRANCH      master
    PATH        /
USAGE
}

looks_like_repo() {
    case "$1" in
        git@github.com:*|https://github.com/*|http://github.com/*|*/*)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

normalize_repo() {
    local repo="$1"

    repo="${repo#https://github.com/}"
    repo="${repo#http://github.com/}"
    repo="${repo#git@github.com:}"
    repo="${repo%.git}"
    repo="${repo%/}"

    if [[ "$repo" != */* ]]; then
        repo="SmoothKen/$repo"
    fi

    printf '%s\n' "$repo"
}

repo_arg="${PAGES_REPO:-}"
branch="${PAGES_BRANCH:-master}"
source_path="${PAGES_PATH:-/}"

case "$#" in
    0)
        ;;
    1)
        if looks_like_repo "$1"; then
            repo_arg="$1"
        else
            branch="$1"
        fi
        ;;
    2)
        if looks_like_repo "$1"; then
            repo_arg="$1"
            branch="$2"
        elif [[ "$2" == "/" || "$2" == "/docs" ]]; then
            branch="$1"
            source_path="$2"
        else
            repo_arg="$1/$2"
        fi
        ;;
    3)
        if looks_like_repo "$1"; then
            repo_arg="$1"
            branch="$2"
            source_path="$3"
        else
            repo_arg="$1/$2"
            branch="$3"
        fi
        ;;
    4)
        repo_arg="$1/$2"
        branch="$3"
        source_path="$4"
        ;;
    *)
        usage
        exit 1
        ;;
esac

if [[ "$source_path" != "/" && "$source_path" != "/docs" ]]; then
    echo "GitHub Pages source path must be / or /docs; got: $source_path" >&2
    usage
    exit 1
fi

if [[ -z "$repo_arg" ]]; then
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        repo_arg="$(git remote get-url origin 2>/dev/null || true)"
    fi

    if [[ -z "$repo_arg" ]]; then
        repo_arg="SmoothKen/$(basename "$PWD")"
    fi
fi

repo_slug="$(normalize_repo "$repo_arg")"
owner="${repo_slug%%/*}"
repo="${repo_slug#*/}"

if [[ -z "$owner" || -z "$repo" || "$owner" == "$repo" ]]; then
    echo "Could not infer OWNER/REPO from: $repo_arg" >&2
    usage
    exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
    echo "GitHub CLI 'gh' is required. Install it, then run: gh auth login --git-protocol ssh" >&2
    exit 1
fi

if ! gh auth status -h github.com >/dev/null 2>&1; then
    echo "Run this once first: gh auth login --git-protocol ssh" >&2
    exit 1
fi

if ! gh repo view "$owner/$repo" >/dev/null 2>&1; then
    echo "Cannot access $owner/$repo through gh." >&2
    echo "Make sure the GitHub repo exists and update_github_repo has pushed it." >&2
    exit 1
fi

if ! gh api "repos/$owner/$repo/branches/$branch" \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2026-03-10" >/dev/null 2>&1; then
    echo "Remote branch not found: $owner/$repo:$branch" >&2
    echo "Run update_github_repo first, or pass the branch actually pushed." >&2
    exit 1
fi

payload=$(printf '{"build_type":"legacy","source":{"branch":"%s","path":"%s"}}' "$branch" "$source_path")

if gh api "repos/$owner/$repo/pages" \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2026-03-10" >/dev/null 2>&1; then
    gh api --method PUT "repos/$owner/$repo/pages" \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2026-03-10" \
        --input - <<< "$payload" >/dev/null
    action="Updated"
else
    gh api --method POST "repos/$owner/$repo/pages" \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2026-03-10" \
        --input - <<< "$payload" >/dev/null
    action="Created"
fi

site_url="$(gh api "repos/$owner/$repo/pages" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2026-03-10" \
    --jq '.html_url // empty' 2>/dev/null || true)"

printf '%s GitHub Pages for %s/%s from %s:%s\n' "$action" "$owner" "$repo" "$branch" "$source_path"
if [[ -n "$site_url" ]]; then
    printf 'Site: %s\n' "$site_url"
fi
