"""
List Players Use Case
"""
from typing import List
from c_api.src.domain.repositories.player_repository import IPlayerRepository
from b_models.player import PlayerResponse


class ListPlayersUseCase:
    """Use case for listing all players"""
    
    def __init__(self, player_repository: IPlayerRepository):
        self.player_repository = player_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[PlayerResponse]:
        """Execute the use case"""
        players = await self.player_repository.get_all(skip=skip, limit=limit)
        
        return [PlayerResponse.model_validate(player) for player in players]
