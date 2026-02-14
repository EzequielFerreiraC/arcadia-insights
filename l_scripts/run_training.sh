#!/usr/bin/env bash
# Train the ML models (RandomForest ending predictor + K-Means profiles).
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD"
export API_ENV="${API_ENV:-production}"
exec .venv/bin/python l_scripts/run_training.py
