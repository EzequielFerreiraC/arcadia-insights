"""
Analytics API Routes
"""
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from a_configs.database import get_db
from b_models.analytics import (
    CompareRow,
    EpisodeDistribution,
    GlobalStats,
    LeaderboardEntry,
    NarrativePath,
    PlayerSummary,
    RankedChoice,
    TimelineRow,
)
from b_models.choice import ChoiceResponse
from c_api.src.infrastructure.database import AnalyticsRepository, PostgresChoiceRepository

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Candidate narrative paths: (choice A, option A, choice B, option B, label, verb A, verb B)
_PATH_CANDIDATES = [
    ("ep2_save_kate", "salvar", "ep3_trust_chloe", "confiar", "Salvar Kate → Confiar em Chloe", "salvaram Kate", "confiaram em Chloe"),
    ("ep1_lisa_plant", "regar", "ep1_kate_petition", "assinar", "Regar a planta → Assinar petição", "regaram a planta", "assinaram a petição"),
    ("ep3_trust_chloe", "confiar", "ep5_final", "sacrificar_arcadia_bay", "Confiar em Chloe → Salvar Chloe", "confiaram em Chloe", "sacrificaram Arcadia Bay"),
    ("ep4_accuse_nathan", "acusar", "ep5_final", "sacrificar_chloe", "Acusar Nathan → Sacrificar Chloe", "acusaram Nathan", "sacrificaram Chloe"),
    ("ep2_save_kate", "nao_salvar", "ep3_trust_chloe", "nao_confiar", "Não salvar Kate → Não confiar em Chloe", "não salvaram Kate", "não confiaram em Chloe"),
]


@router.get("/global", response_model=GlobalStats, summary="Quick global statistics")
async def global_stats(db: AsyncSession = Depends(get_db)):
    return await AnalyticsRepository(db).global_stats()


@router.get("/choices/popular", response_model=List[RankedChoice], summary="Most popular choices")
async def popular_choices(limit: int = 5, db: AsyncSession = Depends(get_db)):
    return await AnalyticsRepository(db).most_popular(min(limit, 20))


@router.get("/choices/rare", response_model=List[RankedChoice], summary="Least popular choices")
async def rare_choices(limit: int = 5, db: AsyncSession = Depends(get_db)):
    return await AnalyticsRepository(db).least_popular(min(limit, 20))


@router.get("/episodes", response_model=List[EpisodeDistribution], summary="Choices per episode")
async def episode_distribution(db: AsyncSession = Depends(get_db)):
    return await AnalyticsRepository(db).episode_distribution()


@router.get("/timeline", response_model=List[TimelineRow], summary="Majority option per decision point")
async def timeline(db: AsyncSession = Depends(get_db)):
    return await AnalyticsRepository(db).timeline()


@router.get("/paths", response_model=List[NarrativePath], summary="Narrative co-occurrence paths")
async def paths(db: AsyncSession = Depends(get_db)):
    repo = AnalyticsRepository(db)
    results: list[NarrativePath] = []
    for a_id, a_opt, b_id, b_opt, label, verb_a, verb_b in _PATH_CANDIDATES:
        freq = await repo.path_frequency(a_id, a_opt, b_id, b_opt)
        results.append(
            NarrativePath(
                label=label,
                detail=f"{freq:.0f}% dos jogadores que {verb_a} também {verb_b}.",
                frequency=freq,
            )
        )
    results.sort(key=lambda p: p.frequency, reverse=True)
    return results


@router.get("/leaderboard", response_model=List[LeaderboardEntry], summary="Rare-choice leaderboard")
async def leaderboard(limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await AnalyticsRepository(db).leaderboard(min(limit, 50))


@router.get(
    "/players/{player_id}/choices",
    response_model=List[ChoiceResponse],
    summary="Choices of a player",
)
async def player_choices(player_id: UUID, db: AsyncSession = Depends(get_db)):
    choices = await PostgresChoiceRepository(db).get_by_player(player_id)
    return [ChoiceResponse.model_validate(c) for c in choices]


@router.get(
    "/players/{player_id}/compare",
    response_model=List[CompareRow],
    summary="Player choices vs. community",
)
async def player_compare(player_id: UUID, db: AsyncSession = Depends(get_db)):
    return await AnalyticsRepository(db).player_compare(player_id)


@router.get(
    "/players/{player_id}/summary",
    response_model=PlayerSummary,
    summary="Player dashboard summary",
)
async def player_summary(player_id: UUID, db: AsyncSession = Depends(get_db)):
    summary = await AnalyticsRepository(db).player_summary(player_id)
    if summary is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Nenhuma escolha encontrada para o jogador {player_id}.",
        )
    return summary
