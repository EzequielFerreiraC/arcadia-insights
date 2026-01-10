"""
Save API Routes
"""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from a_configs.database import get_db
from b_models.choice import ChoiceResponse
from b_models.save import SaveResponse
from c_api.src.application.services.save_pipeline import SaveParseError
from c_api.src.application.use_cases.upload_save import DuplicateSaveError, UploadSaveUseCase
from c_api.src.domain.entities.player import Player
from c_api.src.infrastructure.database import PostgresChoiceRepository, PostgresSaveRepository

router = APIRouter(prefix="/saves", tags=["saves"])

MAX_SAVE_BYTES = 25 * 1024 * 1024  # 25 MB


@router.post(
    "/upload",
    response_model=SaveResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a save file",
)
async def upload_save(
    file: UploadFile = File(...),
    player_id: Optional[UUID] = Form(default=None),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a Life is Strange save (JSON). The file is stored in the Bronze layer,
    a `saves.uploaded` event is emitted and its choices are extracted.

    - **file**: the save file (.json / .sav)
    - **player_id**: optional; if omitted, a player is created from the save's `player` block
    """
    raw = await file.read()
    if not raw:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Arquivo vazio.")
    if len(raw) > MAX_SAVE_BYTES:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Arquivo maior que 25 MB.")

    use_case = UploadSaveUseCase(db)
    try:
        return await use_case.execute(raw=raw, filename=file.filename or "save.json", player_id=player_id)
    except DuplicateSaveError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except SaveParseError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.get("/", response_model=List[SaveResponse], summary="List saves")
async def list_saves(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    limit = min(limit, 100)
    repository = PostgresSaveRepository(db)
    saves = await repository.get_all(skip=skip, limit=limit)
    return [SaveResponse.model_validate(s) for s in saves]


@router.get("/{save_id}", response_model=SaveResponse, summary="Get save by ID")
async def get_save(save_id: UUID, db: AsyncSession = Depends(get_db)):
    repository = PostgresSaveRepository(db)
    save = await repository.get_by_id(save_id)
    if save is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Save {save_id} não encontrado.")
    return SaveResponse.model_validate(save)


@router.get("/{save_id}/choices", response_model=List[ChoiceResponse], summary="Get choices of a save")
async def get_save_choices(save_id: UUID, db: AsyncSession = Depends(get_db)):
    repository = PostgresChoiceRepository(db)
    choices = await repository.get_by_save(save_id)
    return [ChoiceResponse.model_validate(c) for c in choices]


@router.delete("/{save_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a save")
async def delete_save(save_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a save and its extracted choices, keeping player counters in sync."""
    save_repo = PostgresSaveRepository(db)
    save = await save_repo.get_by_id(save_id)
    if save is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Save {save_id} não encontrado.")

    choice_repo = PostgresChoiceRepository(db)
    removed_choices = await choice_repo.delete_by_save(save_id)

    player = await db.get(Player, save.player_id)
    if player is not None:
        player.total_saves = max(0, (player.total_saves or 0) - 1)
        player.total_choices = max(0, (player.total_choices or 0) - removed_choices)

    await save_repo.delete(save)
    return None
