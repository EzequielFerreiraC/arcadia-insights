"""
Player Repository Interface - Abstract Repository
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from c_api.src.domain.entities.player import Player


class IPlayerRepository(ABC):
    """Player repository interface"""
    
    @abstractmethod
    async def create(self, player: Player) -> Player:
        """Create a new player"""
        pass
    
    @abstractmethod
    async def get_by_id(self, player_id: UUID) -> Optional[Player]:
        """Get player by ID"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Player]:
        """Get all players with pagination"""
        pass
    
    @abstractmethod
    async def update(self, player: Player) -> Player:
        """Update player"""
        pass
    
    @abstractmethod
    async def delete(self, player_id: UUID) -> bool:
        """Delete player"""
        pass
    
    @abstractmethod
    async def increment_saves(self, player_id: UUID) -> None:
        """Increment total saves count"""
        pass
    
    @abstractmethod
    async def increment_choices(self, player_id: UUID, count: int = 1) -> None:
        """Increment total choices count"""
        pass
