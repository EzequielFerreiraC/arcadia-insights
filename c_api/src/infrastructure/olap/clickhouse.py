"""
ClickHouse OLAP client (HTTP)
=============================
Minimal async client over the ClickHouse HTTP interface (port 8123). Avoids an
extra native driver dependency — uses httpx. Fail-safe query helper returns an
empty result if ClickHouse is unavailable so pages degrade gracefully.
"""
from __future__ import annotations

from typing import Any

import httpx

from a_configs.logging_config import get_logger
from a_configs.settings import get_settings

logger = get_logger(__name__)
settings = get_settings()


def _base_url() -> str:
    return f"http://{settings.CLICKHOUSE_HOST}:{settings.CLICKHOUSE_PORT}/"


def _auth() -> tuple[str, str]:
    return (settings.CLICKHOUSE_USER, settings.CLICKHOUSE_PASSWORD)


async def execute(sql: str, body: str | None = None) -> None:
    """Run a statement (DDL/INSERT). `body` is appended after the SQL (for FORMAT ...)."""
    payload = sql if body is None else f"{sql}\n{body}"
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(_base_url(), params={"database": settings.CLICKHOUSE_DB}, content=payload.encode("utf-8"), auth=_auth())
        resp.raise_for_status()


async def query_json(sql: str) -> list[dict[str, Any]]:
    """Run a SELECT and return rows as dicts. Returns [] on failure."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                _base_url(),
                params={"database": settings.CLICKHOUSE_DB, "default_format": "JSONEachRow"},
                content=sql.encode("utf-8"),
                auth=_auth(),
            )
            resp.raise_for_status()
            text = resp.text.strip()
            if not text:
                return []
            import json

            return [json.loads(line) for line in text.splitlines() if line]
    except Exception as exc:  # noqa: BLE001 - degrade gracefully
        logger.warning(f"ClickHouse indisponível: {exc}")
        return []


async def scalar(sql: str, default: Any = 0) -> Any:
    """Run a SELECT returning a single value."""
    rows = await query_json(sql)
    if not rows:
        return default
    return next(iter(rows[0].values()), default)
