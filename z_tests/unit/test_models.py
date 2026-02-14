"""
Unit tests for Pydantic Models
"""
import pytest
from pydantic import ValidationError

from b_models.player import PlayerCreate, PlayerResponse, Platform
from b_models.choice import ChoiceCreate, ChoiceResponse
from b_models.save import SaveUpload, SaveResponse, SaveStatus


def test_player_create_valid():
    """Test valid player creation"""
    player = PlayerCreate(
        country="BR",
        platform=Platform.PC,
        game_version="1.0.0"
    )
    
    assert player.country == "BR"
    assert player.platform == Platform.PC
    assert player.game_version == "1.0.0"


def test_player_create_invalid_country():
    """Test player creation with invalid country code"""
    with pytest.raises(ValidationError) as exc_info:
        PlayerCreate(
            country="BRA",  # Must be 2 characters
            platform=Platform.PC,
            game_version="1.0.0"
        )
    
    assert "String should have at most 2 characters" in str(exc_info.value)


def test_choice_create_valid():
    """Test valid choice creation"""
    choice = ChoiceCreate(
        episode=1,
        chapter=1,
        choice_id="sacrifice_chloe",
        choice_text="Sacrifice Chloe?",
        option_selected="yes",
        timestamp_in_game=3600
    )
    
    assert choice.episode == 1
    assert choice.chapter == 1
    assert choice.choice_id == "sacrifice_chloe"


def test_choice_create_invalid_episode():
    """Test choice creation with invalid episode number"""
    with pytest.raises(ValidationError) as exc_info:
        ChoiceCreate(
            episode=6,  # Max is 5
            chapter=1,
            choice_id="test",
            choice_text="Test",
            option_selected="yes",
            timestamp_in_game=0
        )
    
    assert "less than or equal to 5" in str(exc_info.value)


def test_save_upload_valid():
    """Test valid save upload"""
    save = SaveUpload(
        filename="save_episode1.sav",
        file_size_bytes=1024,
        checksum="abc123def456"
    )
    
    assert save.filename == "save_episode1.sav"
    assert save.file_size_bytes == 1024
    assert save.checksum == "abc123def456"


def test_save_status_enum():
    """Test save status enum values"""
    assert SaveStatus.UPLOADED == "uploaded"
    assert SaveStatus.PROCESSING == "processing"
    assert SaveStatus.PROCESSED == "processed"
    assert SaveStatus.FAILED == "failed"


def test_platform_enum():
    """Test platform enum values"""
    assert Platform.PC == "PC"
    assert Platform.PLAYSTATION == "PlayStation"
    assert Platform.XBOX == "Xbox"
    assert Platform.NINTENDO == "Nintendo Switch"
