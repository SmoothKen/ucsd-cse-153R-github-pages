#!/bin/bash
set -e
cd "$(dirname "$0")/.."
scripts/rebuild_site.sh

if type update_github_repo >/dev/null 2>&1
then
    update_github_repo
else
    echo "Built site. Now run: update_github_repo"
fi
