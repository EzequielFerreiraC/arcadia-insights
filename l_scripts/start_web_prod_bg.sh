#!/usr/bin/env bash
# Start the Next.js PRODUCTION server detached (fast navigation, prefetch).
# Requires `npm run build` to have been run first.
cd "$(dirname "$0")/.."
mkdir -p logs
fuser -k 3000/tcp >/dev/null 2>&1 || true
sleep 1
setsid nohup bash -c 'cd d_web && npm run start' > logs/web.log 2>&1 < /dev/null &
echo "web (produção) iniciado (pid $!), log em logs/web.log"
