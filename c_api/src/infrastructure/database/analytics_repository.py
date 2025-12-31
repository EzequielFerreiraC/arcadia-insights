"""
Analytics Repository
====================
Read-only aggregations over the OLTP `choices` table (Postgres). These power
the analytics endpoints consumed by the front-end. Popularity of an option is
measured as the share of players (who reached that decision point) that picked
the option; rarity is its complement.
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# Common CTEs reused across queries: per-option popularity as a percentage.
_OPTION_PCT_CTE = """
WITH per_choice AS (
    SELECT choice_id, COUNT(DISTINCT player_id) AS total
    FROM choices GROUP BY choice_id
),
per_option AS (
    SELECT choice_id, choice_text, episode, option_selected,
           COUNT(DISTINCT player_id) AS players
    FROM choices
    GROUP BY choice_id, choice_text, episode, option_selected
),
opt_pct AS (
    SELECT o.choice_id, o.choice_text, o.episode, o.option_selected,
           o.players,
           ROUND(o.players * 100.0 / NULLIF(c.total, 0), 1) AS pct
    FROM per_option o
    JOIN per_choice c ON c.choice_id = o.choice_id
)
"""


class AnalyticsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def global_stats(self) -> dict[str, Any]:
        totals = (
            await self.session.execute(
                text(
                    """
                    SELECT
                        (SELECT COUNT(*) FROM players) AS total_players,
                        (SELECT COUNT(*) FROM choices) AS total_choices,
                        (SELECT COUNT(*) FROM saves)   AS total_saves
                    """
                )
            )
        ).mappings().one()

        top = (
            await self.session.execute(
                text(
                    _OPTION_PCT_CTE
                    + "SELECT choice_text, pct FROM opt_pct ORDER BY players DESC, pct DESC LIMIT 1"
                )
            )
        ).mappings().first()

        return {
            "total_players": totals["total_players"],
            "total_choices": totals["total_choices"],
            "total_saves": totals["total_saves"],
            "most_common_choice": {
                "label": top["choice_text"] if top else "—",
                "pct": float(top["pct"]) if top else 0.0,
            },
        }

    async def _ranked(self, order: str, limit: int) -> list[dict[str, Any]]:
        rows = (
            await self.session.execute(
                text(
                    _OPTION_PCT_CTE
                    + f"""
                    SELECT choice_id, choice_text, episode, option_selected, players, pct
                    FROM opt_pct
                    ORDER BY pct {order}, players DESC
                    LIMIT :limit
                    """
                ),
                {"limit": limit},
            )
        ).mappings().all()
        return [dict(r) for r in rows]

    async def most_popular(self, limit: int = 5) -> list[dict[str, Any]]:
        return await self._ranked("DESC", limit)

    async def least_popular(self, limit: int = 5) -> list[dict[str, Any]]:
        return await self._ranked("ASC", limit)

    async def episode_distribution(self) -> list[dict[str, Any]]:
        rows = (
            await self.session.execute(
                text(
                    """
                    SELECT episode, COUNT(*) AS choices
                    FROM choices GROUP BY episode ORDER BY episode
                    """
                )
            )
        ).mappings().all()
        return [{"episode": f"Ep {r['episode']}", "choices": r["choices"]} for r in rows]

    async def leaderboard(self, limit: int = 10) -> list[dict[str, Any]]:
        rows = (
            await self.session.execute(
                text(
                    _OPTION_PCT_CTE
                    + """
                    SELECT ch.player_id,
                           pl.country,
                           ROUND(AVG(100 - op.pct), 1) AS avg_rarity,
                           SUM(CASE WHEN op.pct < 20 THEN 1 ELSE 0 END) AS rare_count
                    FROM choices ch
                    JOIN opt_pct op
                      ON op.choice_id = ch.choice_id
                     AND op.option_selected = ch.option_selected
                    JOIN players pl ON pl.id = ch.player_id
                    GROUP BY ch.player_id, pl.country
                    ORDER BY avg_rarity DESC
                    LIMIT :limit
                    """
                ),
                {"limit": limit},
            )
        ).mappings().all()
        return [dict(r) for r in rows]

    async def player_compare(self, player_id: UUID) -> list[dict[str, Any]]:
        rows = (
            await self.session.execute(
                text(
                    _OPTION_PCT_CTE
                    + """
                    SELECT DISTINCT ch.choice_id, ch.choice_text, ch.episode,
                           ch.option_selected, op.pct AS community_pct
                    FROM choices ch
                    JOIN opt_pct op
                      ON op.choice_id = ch.choice_id
                     AND op.option_selected = ch.option_selected
                    WHERE ch.player_id = :pid
                    ORDER BY ch.episode
                    """
                ),
                {"pid": str(player_id)},
            )
        ).mappings().all()
        return [dict(r) for r in rows]

    async def player_summary(self, player_id: UUID) -> dict[str, Any] | None:
        base = (
            await self.session.execute(
                text(
                    _OPTION_PCT_CTE
                    + """
                    SELECT
                        COUNT(*) AS total_choices,
                        COUNT(DISTINCT ch.episode) AS completed_episodes,
                        ROUND(AVG(op.pct), 0) AS compatibility
                    FROM choices ch
                    JOIN opt_pct op
                      ON op.choice_id = ch.choice_id
                     AND op.option_selected = ch.option_selected
                    WHERE ch.player_id = :pid
                    """
                ),
                {"pid": str(player_id)},
            )
        ).mappings().first()

        if not base or base["total_choices"] == 0:
            return None

        rare = await self._player_ranked(player_id, "ASC", 3)
        popular = await self._player_ranked(player_id, "DESC", 3)

        ending = (
            await self.session.execute(
                text(
                    """
                    SELECT choice_text, option_selected
                    FROM choices
                    WHERE player_id = :pid
                    ORDER BY episode DESC, chapter DESC, timestamp_in_game DESC
                    LIMIT 1
                    """
                ),
                {"pid": str(player_id)},
            )
        ).mappings().first()

        return {
            "total_choices": base["total_choices"],
            "completed_episodes": base["completed_episodes"],
            "compatibility": int(base["compatibility"] or 0),
            "ending": ending["choice_text"] if ending else "—",
            "rare_choices": rare,
            "popular_choices": popular,
        }

    async def _player_ranked(self, player_id: UUID, order: str, limit: int) -> list[dict[str, Any]]:
        rows = (
            await self.session.execute(
                text(
                    _OPTION_PCT_CTE
                    + f"""
                    SELECT DISTINCT ch.choice_text AS label, ch.episode, op.pct
                    FROM choices ch
                    JOIN opt_pct op
                      ON op.choice_id = ch.choice_id
                     AND op.option_selected = ch.option_selected
                    WHERE ch.player_id = :pid
                    ORDER BY op.pct {order}
                    LIMIT :limit
                    """
                ),
                {"pid": str(player_id), "limit": limit},
            )
        ).mappings().all()
        return [{"label": r["label"], "episode": r["episode"], "pct": float(r["pct"])} for r in rows]

    async def timeline(self) -> list[dict[str, Any]]:
        """Per decision point: the majority option and its community share."""
        rows = (
            await self.session.execute(
                text(
                    """
                    WITH per_choice AS (
                        SELECT choice_id, COUNT(DISTINCT player_id) AS total
                        FROM choices GROUP BY choice_id
                    ),
                    per_opt AS (
                        SELECT choice_id, choice_text, episode, chapter, option_selected,
                               COUNT(DISTINCT player_id) AS players,
                               ROW_NUMBER() OVER (
                                   PARTITION BY choice_id ORDER BY COUNT(DISTINCT player_id) DESC
                               ) AS rn
                        FROM choices
                        GROUP BY choice_id, choice_text, episode, chapter, option_selected
                    )
                    SELECT o.episode, o.chapter, o.choice_id, o.choice_text, o.option_selected,
                           ROUND(o.players * 100.0 / NULLIF(c.total, 0), 1) AS community_pct
                    FROM per_opt o
                    JOIN per_choice c ON c.choice_id = o.choice_id
                    WHERE o.rn = 1
                    ORDER BY o.episode, o.chapter, o.choice_id
                    """
                )
            )
        ).mappings().all()
        return [dict(r) for r in rows]

    async def path_frequency(self, a_id: str, a_opt: str, b_id: str, b_opt: str) -> float:
        """P(picked b_opt for b_id | picked a_opt for a_id), as a percentage."""
        row = (
            await self.session.execute(
                text(
                    """
                    WITH base AS (
                        SELECT DISTINCT player_id FROM choices
                        WHERE choice_id = :a AND option_selected = :aopt
                    )
                    SELECT
                        (SELECT COUNT(*) FROM base) AS base_n,
                        (SELECT COUNT(DISTINCT ch.player_id) FROM choices ch
                         JOIN base b ON b.player_id = ch.player_id
                         WHERE ch.choice_id = :b AND ch.option_selected = :bopt) AS both_n
                    """
                ),
                {"a": a_id, "aopt": a_opt, "b": b_id, "bopt": b_opt},
            )
        ).mappings().one()
        base_n = row["base_n"] or 0
        both_n = row["both_n"] or 0
        return round(both_n * 100.0 / base_n, 1) if base_n else 0.0
