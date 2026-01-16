"""
ML API Routes — Ending Prediction & Player Profiles
"""
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from a_configs.database import get_db
from b_models.ml import PredictionResponse, ProfileCluster
from c_api.src.infrastructure.database import PostgresChoiceRepository
from c_api.src.infrastructure.ml import serving

router = APIRouter(prefix="/ml", tags=["ml"])


@router.get(
    "/prediction/{player_id}",
    response_model=PredictionResponse,
    summary="Predict the player's ending",
)
async def predict(player_id: UUID, db: AsyncSession = Depends(get_db)):
    choices = await PostgresChoiceRepository(db).get_by_player(player_id)
    if not choices:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sem escolhas para o jogador {player_id}.")

    picks = {c.choice_id: c.option_selected for c in choices}
    try:
        return serving.predict_ending(picks)
    except serving.ModelNotTrained as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(exc)) from exc


@router.get("/profiles", response_model=List[ProfileCluster], summary="Player behavioural clusters")
async def profiles():
    try:
        return serving.get_profiles()
    except serving.ModelNotTrained as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(exc)) from exc
