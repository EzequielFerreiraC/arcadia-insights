"""
Platform (Data Catalog & Observability) Schemas
"""
from __future__ import annotations

from pydantic import BaseModel


class CatalogTable(BaseModel):
    name: str
    layer: str  # Bronze | Silver | Gold
    rows: int
    format: str
    partitions: int
    updated: str | None = None


class PipelineHealth(BaseModel):
    name: str
    status: str  # healthy | degraded | down
    detail: str
    metric: str


class CatalogMetrics(BaseModel):
    total_records: int
    events_processed_24h: int
    avg_pipeline_latency_ms: int
    data_lake_partitions: int


class CatalogResponse(BaseModel):
    metrics: CatalogMetrics
    tables: list[CatalogTable]
    pipelines: list[PipelineHealth]


class ObservabilityMetrics(BaseModel):
    throughput_per_min: int
    events_last_hour: int
    jobs_executed_24h: int
    failures_24h: int
    success_rate: float
