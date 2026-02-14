#!/usr/bin/env python3
"""
Gold Aggregation Job
====================
Reads the Silver-equivalent OLTP data (Postgres `choices`/`players`/`saves`) and
writes curated Gold aggregates to ClickHouse (OLAP):

  - arcadia.choice_popularity   (per option, global popularity %)
  - arcadia.player_stats        (per player rollups)
  - arcadia.episode_stats       (per episode rollups)

This is what the Spark gold job would compute; done here in SQL + Python so it
runs end-to-end without a Spark cluster.

Run:
    PYTHONPATH=. .venv/bin/python l_scripts/run_gold.py
    (or: bash l_scripts/run_gold.sh)
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from sqlalchemy import text  # noqa: E402

from a_configs.database import AsyncSessionLocal  # noqa: E402
from a_configs.logging_config import get_logger, setup_logging  # noqa: E402
from c_api.src.infrastructure.olap import clickhouse as ch  # noqa: E402

logger = get_logger("gold_job")


def _jsonl(rows: list[dict]) -> str:
    return "\n".join(json.dumps(r, default=str) for r in rows)


async def build_choice_popularity(session) -> list[dict]:
    result = await session.execute(
        text(
            """
            WITH per_choice AS (
                SELECT choice_id, COUNT(DISTINCT player_id) AS total
                FROM choices GROUP BY choice_id
            ),
            per_opt AS (
                SELECT choice_id, choice_text, episode, chapter, option_selected,
                       COUNT(DISTINCT player_id) AS players
                FROM choices
                GROUP BY choice_id, choice_text, episode, chapter, option_selected
            )
            SELECT o.choice_id, o.choice_text, o.episode, o.chapter, o.option_selected,
                   o.players AS total_players,
                   ROUND(o.players * 100.0 / NULLIF(c.total, 0), 2) AS percentage
            FROM per_opt o JOIN per_choice c ON c.choice_id = o.choice_id
            """
        )
    )
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return [
        {
            "choice_id": r["choice_id"],
            "choice_text": r["choice_text"],
            "episode": int(r["episode"]),
            "chapter": int(r["chapter"]),
            "option_selected": r["option_selected"],
            "total_players": int(r["total_players"]),
            "percentage": float(r["percentage"] or 0),
            "last_updated": now,
        }
        for r in result.mappings().all()
    ]


async def build_player_stats(session) -> list[dict]:
    result = await session.execute(
        text(
            """
            SELECT p.id::text AS player_id, p.country, p.platform,
                   p.total_saves, p.total_choices,
                   (SELECT COUNT(DISTINCT episode) FROM choices c WHERE c.player_id = p.id) AS unique_episodes,
                   COALESCE((SELECT MAX(uploaded_at) FROM saves s WHERE s.player_id = p.id), NOW()) AS last_save_date
            FROM players p
            """
        )
    )
    rows = []
    for r in result.mappings().all():
        ue = int(r["unique_episodes"] or 0)
        rows.append(
            {
                "player_id": r["player_id"],
                "country": (r["country"] or "??")[:2],
                "platform": r["platform"] or "PC",
                "total_saves": int(r["total_saves"] or 0),
                "total_choices": int(r["total_choices"] or 0),
                "unique_episodes": ue,
                "last_save_date": r["last_save_date"].strftime("%Y-%m-%d %H:%M:%S"),
                "playtime_hours": 0.0,
                "completion_percentage": round(ue * 100.0 / 5, 1),
            }
        )
    return rows


async def build_episode_stats(session) -> list[dict]:
    result = await session.execute(
        text(
            """
            SELECT episode,
                   COUNT(DISTINCT player_id) AS total_players,
                   ROUND(COUNT(*)::numeric / NULLIF(COUNT(DISTINCT player_id), 0), 2) AS avg_choices
            FROM choices GROUP BY episode ORDER BY episode
            """
        )
    )
    today = datetime.utcnow().strftime("%Y-%m-%d")
    return [
        {
            "episode": int(r["episode"]),
            "total_players": int(r["total_players"]),
            "avg_choices_per_player": float(r["avg_choices"] or 0),
            "avg_playtime_hours": 0.0,
            "completion_rate": 0.0,
            "date": today,
        }
        for r in result.mappings().all()
    ]


async def main() -> None:
    setup_logging(level="INFO")
    logger.info("Iniciando agregação Gold (Postgres → ClickHouse)")

    async with AsyncSessionLocal() as session:
        popularity = await build_choice_popularity(session)
        players = await build_player_stats(session)
        episodes = await build_episode_stats(session)

    tables = {
        "choice_popularity": popularity,
        "player_stats": players,
        "episode_stats": episodes,
    }

    for name, rows in tables.items():
        await ch.execute(f"TRUNCATE TABLE IF EXISTS arcadia.{name}")
        if rows:
            await ch.execute(f"INSERT INTO arcadia.{name} FORMAT JSONEachRow", body=_jsonl(rows))
        logger.info(f"Gold arcadia.{name}: {len(rows)} linhas escritas.")

    logger.info("Agregação Gold concluída.")


if __name__ == "__main__":
    asyncio.run(main())
