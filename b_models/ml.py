"""
ML Response Schemas
"""
from __future__ import annotations

from pydantic import BaseModel


class EndingPrediction(BaseModel):
    ending: str
    probability: float


class PredictionFactor(BaseModel):
    factor: str
    weight: str
    direction: str


class PredictionResponse(BaseModel):
    predictions: list[EndingPrediction]
    factors: list[PredictionFactor]


class ProfileCluster(BaseModel):
    name: str
    description: str
    players: int
    occurrence: float
    typical_choices: list[str]
