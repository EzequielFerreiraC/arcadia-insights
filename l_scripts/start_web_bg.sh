#!/usr/bin/env bash
# Start the Next.js dev server detached, logging to logs/web.log.
cd "$(dirname "$0")/.."
mkdir -p logs
setsid nohup bash -c 'cd d_web && npm run dev' > logs/web.log 2>&1 < /dev/null &
echo "web dev iniciado (pid $!), log em logs/web.log"
