"""
Choice Models - Pydantic Schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, UUID4


class ChoiceCreate(BaseModel):
    """Schema for creating a new choice"""
    player_id: UUID4
    save_id: UUID4
    episode: int = Field(..., ge=1, le=5, description="Episode number (1-5)")
    chapter: int = Field(..., ge=1, description="Chapter number")
    choice_id: str = Field(..., description="Unique choice identifier from game")
    choice_text: str = Field(..., min_length=1, max_length=500)
    option_selected: str = Field(..., min_length=1, max_length=200)
    timestamp_in_game: int = Field(..., description="Timestamp in game (seconds)")


class ChoiceResponse(BaseModel):
    """Schema for choice response"""
    id: UUID4
    player_id: UUID4
    save_id: UUID4
    episode: int
    chapter: int
    choice_id: str
    choice_text: str
    option_selected: str
    timestamp_in_game: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChoiceStatistics(BaseModel):
    """Schema for choice statistics (global)"""
    choice_id: str
    choice_text: str
    episode: int
    chapter: int
    total_players: int
    options: dict[str, int]  # {option: count}
    most_popular: str
    popularity_percentage: float
