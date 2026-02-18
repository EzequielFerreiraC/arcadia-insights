"""
Unit tests for Player Use Cases
"""
import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from c_api.src.application.use_cases.create_player import CreatePlayerUseCase
from c_api.src.application.use_cases.get_player import GetPlayerUseCase
from c_api.src.application.use_cases.list_players import ListPlayersUseCase
from c_api.src.domain.repositories.player_repository import IPlayerRepository
from c_api.src.domain.entities.player import Player, PlatformEnum
from b_models.player import PlayerCreate, PlayerResponse, Platform


@pytest.fixture
def mock_repository():
    """Mock player repository"""
    return Mock(spec=IPlayerRepository)


@pytest.mark.asyncio
async def test_create_player_success(mock_repository):
    """Test successful player creation"""
    # Arrange
    player_data = PlayerCreate(
        country="BR",
        platform=Platform.PC,
        game_version="1.0.0"
    )
    
    player_id = uuid4()
    mock_player = Player(
        id=player_id,
        country="BR",
        platform=PlatformEnum.PC,
        game_version="1.0.0"
    )
    
    mock_repository.create = AsyncMock(return_value=mock_player)
    use_case = CreatePlayerUseCase(mock_repository)
    
    # Act
    result = await use_case.execute(player_data)
    
    # Assert
    assert isinstance(result, PlayerResponse)
    assert result.country == "BR"
    assert result.platform == Platform.PC
    assert result.game_version == "1.0.0"
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_player_found(mock_repository):
    """Test getting existing player"""
    # Arrange
    player_id = uuid4()
    mock_player = Player(
        id=player_id,
        country="US",
        platform=PlatformEnum.PLAYSTATION,
        game_version="1.1.0"
    )
    
    mock_repository.get_by_id = AsyncMock(return_value=mock_player)
    use_case = GetPlayerUseCase(mock_repository)
    
    # Act
    result = await use_case.execute(player_id)
    
    # Assert
    assert result is not None
    assert result.country == "US"
    assert result.platform == Platform.PLAYSTATION
    mock_repository.get_by_id.assert_called_once_with(player_id)


@pytest.mark.asyncio
async def test_get_player_not_found(mock_repository):
    """Test getting non-existent player"""
    # Arrange
    player_id = uuid4()
    mock_repository.get_by_id = AsyncMock(return_value=None)
    use_case = GetPlayerUseCase(mock_repository)
    
    # Act
    result = await use_case.execute(player_id)
    
    # Assert
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(player_id)


@pytest.mark.asyncio
async def test_list_players_success(mock_repository):
    """Test listing players with pagination"""
    # Arrange
    mock_players = [
        Player(
            id=uuid4(),
            country="BR",
            platform=PlatformEnum.PC,
            game_version="1.0.0"
        ),
        Player(
            id=uuid4(),
            country="US",
            platform=PlatformEnum.XBOX,
            game_version="1.1.0"
        )
    ]
    
    mock_repository.get_all = AsyncMock(return_value=mock_players)
    use_case = ListPlayersUseCase(mock_repository)
    
    # Act
    result = await use_case.execute(skip=0, limit=10)
    
    # Assert
    assert len(result) == 2
    assert all(isinstance(p, PlayerResponse) for p in result)
    mock_repository.get_all.assert_called_once_with(skip=0, limit=10)


@pytest.mark.asyncio
async def test_list_players_empty(mock_repository):
    """Test listing players when database is empty"""
    # Arrange
    mock_repository.get_all = AsyncMock(return_value=[])
    use_case = ListPlayersUseCase(mock_repository)
    
    # Act
    result = await use_case.execute(skip=0, limit=10)
    
    # Assert
    assert result == []
    mock_repository.get_all.assert_called_once_with(skip=0, limit=10)
