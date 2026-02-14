#!/usr/bin/env bash
# Run the event-driven save processing worker (Kafka consumer).
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD"
echo "== worker: consumindo saves.uploaded =="
exec .venv/bin/python l_scripts/run_worker.py
