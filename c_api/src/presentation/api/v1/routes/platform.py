"""
Platform API Routes — Data Catalog & Observability
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from a_configs.database import get_db
from b_models.platform import (
    CatalogMetrics,
    CatalogResponse,
    CatalogTable,
    ObservabilityMetrics,
    PipelineHealth,
)
from c_api.src.infrastructure.database.platform_repository import PlatformRepository
from c_api.src.infrastructure.olap import clickhouse as ch

router = APIRouter(prefix="/platform", tags=["platform"])


def _iso(value) -> str | None:
    return value.isoformat() if value is not None else None


@router.get("/catalog", response_model=CatalogResponse, summary="Data lake catalog & pipeline health")
async def catalog(db: AsyncSession = Depends(get_db)):
    repo = PlatformRepository(db)
    counts = await repo.counts()
    pm = await repo.pipeline_metrics()

    # Gold layer row counts from ClickHouse.
    gold_pop = int(await ch.scalar("SELECT count() FROM arcadia.choice_popularity") or 0)
    gold_players = int(await ch.scalar("SELECT count() FROM arcadia.player_stats") or 0)
    gold_eps = int(await ch.scalar("SELECT count() FROM arcadia.episode_stats") or 0)
    gold_updated = await ch.scalar("SELECT max(last_updated) FROM arcadia.choice_popularity", default=None)
    gold_online = gold_pop > 0

    tables = [
        CatalogTable(name="bronze.saves_raw", layer="Bronze", rows=counts.get("saves", 0),
                     format="JSON", partitions=counts.get("save_partitions", 0), updated=_iso(counts.get("saves_updated"))),
        CatalogTable(name="silver.choices", layer="Silver", rows=counts.get("choices", 0),
                     format="Parquet", partitions=5, updated=_iso(counts.get("choices_updated"))),
        CatalogTable(name="silver.players", layer="Silver", rows=counts.get("players", 0),
                     format="Parquet", partitions=counts.get("player_partitions", 0), updated=_iso(counts.get("players_updated"))),
        CatalogTable(name="gold.choice_popularity", layer="Gold", rows=gold_pop,
                     format="ClickHouse", partitions=5, updated=str(gold_updated) if gold_updated else None),
        CatalogTable(name="gold.player_stats", layer="Gold", rows=gold_players,
                     format="ClickHouse", partitions=1, updated=str(gold_updated) if gold_updated else None),
        CatalogTable(name="gold.episode_stats", layer="Gold", rows=gold_eps,
                     format="ClickHouse", partitions=1, updated=str(gold_updated) if gold_updated else None),
    ]

    processing = pm.get("processing", 0)
    failed = pm.get("failed", 0)
    pipelines = [
        PipelineHealth(name="Postgres", status="healthy", detail="OLTP · players/saves/choices",
                       metric=f"{counts.get('choices', 0)} escolhas"),
        PipelineHealth(name="Kafka", status="healthy" if pm.get("processed", 0) > 0 else "degraded",
                       detail="saves.uploaded · choices.extracted",
                       metric=f"{pm.get('processed', 0)} processados · {processing} na fila"),
        PipelineHealth(name="Worker", status="degraded" if failed > 0 else "healthy",
                       detail="extração event-driven",
                       metric=f"{failed} falhas" if failed else "sem falhas"),
        PipelineHealth(name="ClickHouse", status="healthy" if gold_online else "down",
                       detail="camada Gold (OLAP)",
                       metric=f"{int(gold_pop or 0)} agregados" if gold_online else "sem dados Gold"),
    ]

    metrics = CatalogMetrics(
        total_records=counts.get("players", 0) + counts.get("saves", 0) + counts.get("choices", 0),
        events_processed_24h=pm.get("events_24h", 0),
        avg_pipeline_latency_ms=int(pm.get("avg_latency_ms", 0) or 0),
        data_lake_partitions=counts.get("save_partitions", 0) + 5 + counts.get("player_partitions", 0),
    )

    return CatalogResponse(metrics=metrics, tables=tables, pipelines=pipelines)


@router.get("/observability", response_model=ObservabilityMetrics, summary="System observability metrics")
async def observability(db: AsyncSession = Depends(get_db)):
    pm = await PlatformRepository(db).pipeline_metrics()
    processed = pm.get("processed", 0)
    failed = pm.get("failed", 0)
    total = processed + failed
    success = round(processed * 100.0 / total, 1) if total else 100.0
    events_1h = pm.get("events_1h", 0)

    return ObservabilityMetrics(
        throughput_per_min=round(events_1h / 60) if events_1h else 0,
        events_last_hour=events_1h,
        jobs_executed_24h=pm.get("jobs_24h", 0),
        failures_24h=pm.get("failed_24h", 0),
        success_rate=success,
    )
