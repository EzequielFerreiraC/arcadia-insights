"""
Upload Save Use Case
====================
Orchestrates the ingestion of a save file:

  1. checksum + de-duplication
  2. resolve/create the player
  3. persist the Save row (status=uploaded)
  4. store raw bytes in the Bronze bucket (best-effort)
  5. publish `saves.uploaded` (kafka mode) OR extract choices inline (inline mode)
"""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from a_configs.logging_config import get_logger
from a_configs.settings import get_settings
from b_models.save import SaveResponse
from c_api.src.application.services import save_pipeline
from c_api.src.domain.entities.player import Player
from c_api.src.domain.entities.save import Save, SaveStatusEnum
from c_api.src.infrastructure.messaging import event_bus
from c_api.src.infrastructure.storage import object_store

logger = get_logger(__name__)
settings = get_settings()


class DuplicateSaveError(Exception):
    """Raised when a save with the same checksum already exists."""

    def __init__(self, checksum: str):
        self.checksum = checksum
        super().__init__(f"Save com checksum {checksum} já foi enviado.")


class UploadSaveUseCase:
    """Handle a save upload end-to-end."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute(
        self,
        raw: bytes,
        filename: str,
        player_id: Optional[UUID] = None,
    ) -> SaveResponse:
        checksum = save_pipeline.compute_checksum(raw)

        # De-duplication on the unique checksum column.
        existing = await self.session.execute(
            select(Save).where(Save.checksum == checksum)
        )
        if existing.scalar_one_or_none() is not None:
            raise DuplicateSaveError(checksum)

        # Parse up-front so an invalid file is rejected before we persist anything.
        parsed = save_pipeline.parse_save(raw)
        player = await save_pipeline.resolve_player(self.session, player_id, parsed)

        # Best-effort raw storage in Bronze (only when enabled / infra available).
        s3_path = None
        if settings.STORAGE_ENABLED or settings.PIPELINE_MODE == "kafka":
            s3_path = object_store.put_bronze_save(checksum, filename, raw)

        save = Save(
            player_id=player.id,
            filename=filename,
            file_size_bytes=len(raw),
            checksum=checksum,
            status=SaveStatusEnum.UPLOADED,
            s3_path=s3_path,
        )
        self.session.add(save)
        await self.session.flush()

        # Keep the player's save counter in sync.
        player.total_saves = (player.total_saves or 0) + 1

        if settings.PIPELINE_MODE == "kafka":
            # Event-driven path: a worker will extract choices asynchronously.
            save.status = SaveStatusEnum.PROCESSING
            event_bus.publish_save_uploaded(
                save_id=save.id,
                player_id=player.id,
                filename=filename,
                file_size_bytes=len(raw),
                checksum=checksum,
                s3_path=s3_path,
            )
        else:
            # Inline path: extract choices synchronously (works with just Postgres).
            choices = save_pipeline.build_choices(save.id, player.id, parsed)
            count = await save_pipeline.persist_choices(self.session, save, choices)
            if settings.EVENTS_ENABLED:
                event_bus.publish_choices_extracted(
                    save_id=save.id,
                    player_id=player.id,
                    choices=[
                        {
                            "episode": c.episode,
                            "chapter": c.chapter,
                            "choice_id": c.choice_id,
                            "option_selected": c.option_selected,
                        }
                        for c in choices
                    ],
                    total_choices=count,
                )

        await self.session.flush()
        await self.session.refresh(save)
        return SaveResponse.model_validate(save)
