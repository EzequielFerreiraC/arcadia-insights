"""PostgreSQL Choice Repository"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from c_api.src.domain.entities.choice import Choice


class PostgresChoiceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_player(self, player_id: UUID, skip: int = 0, limit: int = 200) -> list[Choice]:
        result = await self.session.execute(
            select(Choice)
            .where(Choice.player_id == player_id)
            .order_by(Choice.episode, Choice.chapter, Choice.timestamp_in_game)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_save(self, save_id: UUID) -> list[Choice]:
        result = await self.session.execute(
            select(Choice).where(Choice.save_id == save_id).order_by(Choice.episode, Choice.chapter)
        )
        return list(result.scalars().all())

    async def delete_by_save(self, save_id: UUID) -> int:
        """Delete all choices for a save. Returns the number removed."""
        count = await self.count_by_save(save_id)
        await self.session.execute(sa_delete(Choice).where(Choice.save_id == save_id))
        await self.session.flush()
        return count

    async def count_by_save(self, save_id: UUID) -> int:
        from sqlalchemy import func

        result = await self.session.execute(
            select(func.count()).select_from(Choice).where(Choice.save_id == save_id)
        )
        return int(result.scalar_one() or 0)
