"""
Analytics Response Schemas
"""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class MostCommonChoice(BaseModel):
    label: str
    pct: float


class GlobalStats(BaseModel):
    total_players: int
    total_choices: int
    total_saves: int
    most_common_choice: MostCommonChoice


class RankedChoice(BaseModel):
    choice_id: str
    choice_text: str
    episode: int
    option_selected: str
    players: int
    pct: float


class EpisodeDistribution(BaseModel):
    episode: str
    choices: int


class LeaderboardEntry(BaseModel):
    player_id: UUID
    country: str
    avg_rarity: float
    rare_count: int


class CompareRow(BaseModel):
    choice_id: str
    choice_text: str
    episode: int
    option_selected: str
    community_pct: float


class PlayerRankedChoice(BaseModel):
    label: str
    episode: int
    pct: float


class PlayerSummary(BaseModel):
    total_choices: int
    completed_episodes: int
    compatibility: int
    ending: str
    rare_choices: list[PlayerRankedChoice]
    popular_choices: list[PlayerRankedChoice]


class TimelineRow(BaseModel):
    episode: int
    chapter: int
    choice_id: str
    choice_text: str
    option_selected: str
    community_pct: float


class NarrativePath(BaseModel):
    label: str
    detail: str
    frequency: float
