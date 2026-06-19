#!/bin/bash
set -e
cd "$(dirname "$0")/.."
python -m pip show Jinja2 >/dev/null 2>&1 || python -m pip install --user -r requirements.txt
python scripts/build_site.py
