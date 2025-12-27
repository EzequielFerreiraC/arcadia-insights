"""PostgreSQL Save Repository"""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from c_api.src.domain.entities.save import Save


class PostgresSaveRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, save_id: UUID) -> Optional[Save]:
        result = await self.session.execute(select(Save).where(Save.id == save_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Save]:
        result = await self.session.execute(
            select(Save).order_by(Save.uploaded_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_player(self, player_id: UUID, skip: int = 0, limit: int = 100) -> list[Save]:
        result = await self.session.execute(
            select(Save)
            .where(Save.player_id == player_id)
            .order_by(Save.uploaded_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def delete(self, save: Save) -> None:
        await self.session.delete(save)
        await self.session.flush()
