#!/usr/bin/env bash
# Run the FastAPI backend from the repo root using the local venv.
# PIPELINE_MODE=inline (default) extracts choices synchronously — works with
# just Postgres. Set PIPELINE_MODE=kafka to use the event-driven worker path.
set -euo pipefail
cd "$(dirname "$0")/.."

export PYTHONPATH="$PWD"
export PIPELINE_MODE="${PIPELINE_MODE:-inline}"

echo "== API em http://localhost:8000  (PIPELINE_MODE=$PIPELINE_MODE) =="
exec .venv/bin/uvicorn c_api.src.main:app --host 0.0.0.0 --port 8000 --reload
