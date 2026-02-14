#!/usr/bin/env python3
"""
Save Processing Worker (event-driven)
=====================================
Consumes `saves.uploaded` from Kafka, downloads the raw save from the Bronze
bucket (MinIO), extracts the choices into Postgres, and publishes
`choices.extracted`. This is the asynchronous path used when the API runs in
PIPELINE_MODE=kafka.

Run:
    PYTHONPATH=. .venv/bin/python l_scripts/run_worker.py
    (or: bash l_scripts/run_worker.sh)
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from uuid import UUID

# Ensure the repo root is importable.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from kafka import KafkaConsumer  # noqa: E402

from a_configs.logging_config import get_logger, setup_logging  # noqa: E402
from a_configs.settings import get_settings  # noqa: E402
from a_configs.database import AsyncSessionLocal  # noqa: E402
from c_api.src.application.services import save_pipeline  # noqa: E402
from c_api.src.infrastructure.database import PostgresChoiceRepository  # noqa: E402
from c_api.src.infrastructure.messaging import event_bus  # noqa: E402
from c_api.src.infrastructure.storage import object_store  # noqa: E402

settings = get_settings()
logger = get_logger("save_worker")


async def handle_event(event: dict) -> None:
    """Process a single saves.uploaded event."""
    save_id = event.get("save_id")
    player_id = event.get("player_id")
    s3_path = event.get("s3_path")

    if not save_id:
        logger.warning(f"Evento sem save_id: {event}")
        return

    logger.info(f"Processando save {save_id} (s3_path={s3_path})")

    raw = object_store.get_bronze_object(s3_path) if s3_path else None

    async with AsyncSessionLocal() as session:
        try:
            if raw is None:
                raise save_pipeline.SaveParseError(
                    "Conteúdo bruto indisponível no Bronze (MinIO)."
                )
            count = await save_pipeline.extract_for_save(session, UUID(save_id), raw)
            choices = await PostgresChoiceRepository(session).get_by_save(UUID(save_id))
            await session.commit()
            logger.info(f"Save {save_id}: {count} escolhas extraídas.")
        except Exception as exc:  # noqa: BLE001
            await session.rollback()
            async with AsyncSessionLocal() as err_session:
                await save_pipeline.mark_save_failed(err_session, UUID(save_id), str(exc))
                await err_session.commit()
            logger.error(f"Falha ao processar save {save_id}: {exc}")
            return

    # Emit the downstream event.
    event_bus.publish_choices_extracted(
        save_id=UUID(save_id),
        player_id=UUID(player_id) if player_id else UUID(save_id),
        choices=[
            {
                "episode": c.episode,
                "chapter": c.chapter,
                "choice_id": c.choice_id,
                "option_selected": c.option_selected,
            }
            for c in choices
        ],
        total_choices=len(choices),
    )


def main() -> None:
    setup_logging(level="INFO")
    topic = settings.KAFKA_TOPIC_SAVES_UPLOADED
    logger.info(f"Worker iniciado. Consumindo '{topic}' em {settings.KAFKA_BOOTSTRAP_SERVERS}")

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="save-processing-worker",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        for message in consumer:
            try:
                loop.run_until_complete(handle_event(message.value))
            except Exception as exc:  # noqa: BLE001
                logger.error(f"Erro inesperado no worker: {exc}")
    except KeyboardInterrupt:
        logger.info("Worker encerrado.")
    finally:
        consumer.close()
        loop.close()


if __name__ == "__main__":
    main()
