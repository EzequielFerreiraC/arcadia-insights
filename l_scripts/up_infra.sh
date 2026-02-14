#!/usr/bin/env bash
# Bring up the infrastructure needed for the pipeline.
# Phase 1 (inline mode) only requires Postgres. Kafka/MinIO/ClickHouse are
# started too for later phases but we only block on Postgres being healthy.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! docker ps >/dev/null 2>&1; then
  echo "!! Docker daemon não está rodando."
  echo "   Rode no seu terminal:  sudo service docker start"
  exit 1
fi

echo "== subindo serviços =="
docker-compose up -d postgres redis minio kafka zookeeper clickhouse

echo "== aguardando Postgres ficar pronto =="
for i in $(seq 1 40); do
  if docker exec arcadia-postgres pg_isready -U arcadia >/dev/null 2>&1; then
    echo "Postgres pronto."
    break
  fi
  sleep 2
done

echo "== status =="
docker ps --format "table {{.Names}}\t{{.Status}}"
