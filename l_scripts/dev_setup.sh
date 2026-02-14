#!/usr/bin/env bash
# Dev setup for the API: create a venv, install the minimal runtime deps,
# then run the import smoke test. Safe to re-run.
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT="$(pwd)"
echo "== repo: $ROOT =="

if [ ! -x .venv/bin/python ]; then
  echo "== creating .venv =="
  python3 -m venv .venv
fi

echo "== installing minimal API deps =="
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet \
  fastapi "uvicorn[standard]" "sqlalchemy[asyncio]" asyncpg \
  "pydantic>=2" pydantic-settings python-multipart \
  minio kafka-python redis requests httpx

echo "INSTALL_DONE"

echo "== import smoke test =="
PYTHONPATH="$ROOT" .venv/bin/python l_scripts/smoke_import.py
