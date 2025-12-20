"""
Create Player Use Case
"""
from uuid import UUID
from c_api.src.domain.entities.player import Player, PlatformEnum
from c_api.src.domain.repositories.player_repository import IPlayerRepository
from b_models.player import PlayerCreate, PlayerResponse


class CreatePlayerUseCase:
    """Use case for creating a new player"""
    
    def __init__(self, player_repository: IPlayerRepository):
        self.player_repository = player_repository
    
    async def execute(self, data: PlayerCreate) -> PlayerResponse:
        """Execute the use case"""
        # Create domain entity
        player = Player(
            country=data.country,
            platform=PlatformEnum(data.platform.value),
            game_version=data.game_version,
        )
        
        # Save to repository
        created_player = await self.player_repository.create(player)
        
        # Return response DTO
        return PlayerResponse.model_validate(created_player)
