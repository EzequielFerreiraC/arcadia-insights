"""
Player API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from a_configs.database import get_db
from b_models.player import PlayerCreate, PlayerResponse
from c_api.src.infrastructure.database import PostgresPlayerRepository
from c_api.src.application.use_cases import (
    CreatePlayerUseCase,
    GetPlayerUseCase,
    ListPlayersUseCase,
)

router = APIRouter(prefix="/players", tags=["players"])


@router.post(
    "/",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new player",
)
async def create_player(
    data: PlayerCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new player.
    
    - **country**: ISO 3166-1 alpha-2 country code (e.g., 'BR', 'US')
    - **platform**: Gaming platform (PC, PlayStation, Xbox, Nintendo)
    - **game_version**: Game version string
    """
    repository = PostgresPlayerRepository(db)
    use_case = CreatePlayerUseCase(repository)
    
    return await use_case.execute(data)


@router.get(
    "/{player_id}",
    response_model=PlayerResponse,
    summary="Get player by ID",
)
async def get_player(
    player_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific player by ID.
    """
    repository = PostgresPlayerRepository(db)
    use_case = GetPlayerUseCase(repository)
    
    player = await use_case.execute(player_id)
    
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found",
        )
    
    return player


@router.get(
    "/",
    response_model=List[PlayerResponse],
    summary="List all players",
)
async def list_players(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    List all players with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 100)
    """
    if limit > 100:
        limit = 100
    
    repository = PostgresPlayerRepository(db)
    use_case = ListPlayersUseCase(repository)
    
    return await use_case.execute(skip=skip, limit=limit)
