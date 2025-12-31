"""
Platform Metrics Repository
===========================
Real operational metrics derived from the OLTP database — powers the Data
Catalog and Observability pages.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class PlatformRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _one(self, sql: str) -> dict[str, Any]:
        result = await self.session.execute(text(sql))
        row = result.mappings().first()
        return dict(row) if row else {}

    async def counts(self) -> dict[str, Any]:
        return await self._one(
            """
            SELECT
                (SELECT COUNT(*) FROM players) AS players,
                (SELECT COUNT(*) FROM saves) AS saves,
                (SELECT COUNT(*) FROM choices) AS choices,
                (SELECT COUNT(DISTINCT DATE(uploaded_at)) FROM saves) AS save_partitions,
                (SELECT COUNT(DISTINCT country) FROM players) AS player_partitions,
                (SELECT MAX(uploaded_at) FROM saves) AS saves_updated,
                (SELECT MAX(created_at) FROM choices) AS choices_updated,
                (SELECT MAX(updated_at) FROM players) AS players_updated
            """
        )

    async def pipeline_metrics(self) -> dict[str, Any]:
        return await self._one(
            """
            SELECT
                (SELECT COUNT(*) FROM choices WHERE created_at > NOW() - INTERVAL '24 hours') AS events_24h,
                (SELECT COUNT(*) FROM choices WHERE created_at > NOW() - INTERVAL '1 hour') AS events_1h,
                (SELECT COUNT(*) FROM saves WHERE uploaded_at > NOW() - INTERVAL '24 hours') AS jobs_24h,
                (SELECT COUNT(*) FROM saves WHERE UPPER(status) = 'PROCESSED') AS processed,
                (SELECT COUNT(*) FROM saves WHERE UPPER(status) = 'FAILED') AS failed,
                (SELECT COUNT(*) FROM saves WHERE UPPER(status) = 'FAILED' AND uploaded_at > NOW() - INTERVAL '24 hours') AS failed_24h,
                (SELECT COUNT(*) FROM saves WHERE UPPER(status) = 'PROCESSING') AS processing,
                (SELECT COALESCE(ROUND(AVG(EXTRACT(EPOCH FROM (processed_at - uploaded_at)) * 1000)), 0)
                 FROM saves WHERE processed_at IS NOT NULL) AS avg_latency_ms
            """
        )
