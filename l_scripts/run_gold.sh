#!/usr/bin/env bash
# Run the Gold aggregation job (Postgres → ClickHouse).
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD"
exec .venv/bin/python l_scripts/run_gold.py
