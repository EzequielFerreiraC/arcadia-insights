"""
PostgreSQL Player Repository Implementation
"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from c_api.src.domain.entities.player import Player
from c_api.src.domain.repositories.player_repository import IPlayerRepository


class PostgresPlayerRepository(IPlayerRepository):
    """PostgreSQL implementation of Player Repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, player: Player) -> Player:
        """Create a new player"""
        self.session.add(player)
        await self.session.flush()
        await self.session.refresh(player)
        return player
    
    async def get_by_id(self, player_id: UUID) -> Optional[Player]:
        """Get player by ID"""
        result = await self.session.execute(
            select(Player).where(Player.id == player_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Player]:
        """Get all players with pagination"""
        result = await self.session.execute(
            select(Player).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def update(self, player: Player) -> Player:
        """Update player"""
        await self.session.flush()
        await self.session.refresh(player)
        return player
    
    async def delete(self, player_id: UUID) -> bool:
        """Delete player"""
        player = await self.get_by_id(player_id)
        if player:
            await self.session.delete(player)
            return True
        return False
    
    async def increment_saves(self, player_id: UUID) -> None:
        """Increment total saves count"""
        await self.session.execute(
            update(Player)
            .where(Player.id == player_id)
            .values(total_saves=Player.total_saves + 1)
        )
    
    async def increment_choices(self, player_id: UUID, count: int = 1) -> None:
        """Increment total choices count"""
        await self.session.execute(
            update(Player)
            .where(Player.id == player_id)
            .values(total_choices=Player.total_choices + count)
        )
