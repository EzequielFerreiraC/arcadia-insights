"""
Get Player Use Case
"""
from uuid import UUID
from typing import Optional
from c_api.src.domain.repositories.player_repository import IPlayerRepository
from b_models.player import PlayerResponse


class GetPlayerUseCase:
    """Use case for getting a player by ID"""
    
    def __init__(self, player_repository: IPlayerRepository):
        self.player_repository = player_repository
    
    async def execute(self, player_id: UUID) -> Optional[PlayerResponse]:
        """Execute the use case"""
        player = await self.player_repository.get_by_id(player_id)
        
        if not player:
            return None
        
        return PlayerResponse.model_validate(player)
