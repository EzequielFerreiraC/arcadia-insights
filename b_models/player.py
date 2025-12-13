"""
Player Models - Pydantic Schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, UUID4
from enum import Enum


class Platform(str, Enum):
    """Gaming platform"""
    PC = "PC"
    PLAYSTATION = "PlayStation"
    XBOX = "Xbox"
    NINTENDO = "Nintendo"


class PlayerCreate(BaseModel):
    """Schema for creating a new player"""
    country: str = Field(..., min_length=2, max_length=2, description="ISO country code")
    platform: Platform
    game_version: str = Field(..., description="Game version string")


class PlayerResponse(BaseModel):
    """Schema for player response"""
    id: UUID4
    country: str
    platform: Platform
    game_version: str
    created_at: datetime
    updated_at: datetime
    total_saves: int = 0
    total_choices: int = 0
    
    class Config:
        from_attributes = True


class PlayerStats(BaseModel):
    """Schema for player statistics"""
    player_id: UUID4
    total_saves: int
    total_choices: int
    unique_episodes: int
    last_save_date: Optional[datetime]
    playtime_hours: float = 0.0
    completion_percentage: float = 0.0
