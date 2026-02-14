#!/usr/bin/env bash
# Start the save worker detached, logging to logs/worker.log.
cd "$(dirname "$0")/.."
mkdir -p logs
setsid nohup bash l_scripts/run_worker.sh > logs/worker.log 2>&1 < /dev/null &
echo "worker iniciado (pid $!), log em logs/worker.log"
