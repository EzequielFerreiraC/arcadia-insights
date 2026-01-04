"""
Event Bus (best-effort)
=======================
Thin, fail-safe wrappers around the Kafka producers. Publishing must never
break an HTTP request: if the broker is unavailable the failure is logged and
the pipeline continues (inline mode still persists the data).
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from a_configs.logging_config import get_logger

logger = get_logger(__name__)


def publish_save_uploaded(
    save_id: UUID,
    player_id: UUID,
    filename: str,
    file_size_bytes: int,
    checksum: str,
    s3_path: str | None,
) -> bool:
    """Publish a `saves.uploaded` event. Returns True on success, False otherwise."""
    try:
        from e_kafka.producers.save_upload_producer import get_save_upload_producer

        producer = get_save_upload_producer()
        return producer.send_save_uploaded_event(
            save_id=str(save_id),
            player_id=str(player_id),
            filename=filename,
            file_size_bytes=file_size_bytes,
            checksum=checksum,
            s3_path=s3_path or "",
        )
    except Exception as exc:  # noqa: BLE001 - best-effort by design
        logger.warning(f"Kafka indisponível (save.uploaded não publicado): {exc}")
        return False


def publish_choices_extracted(
    save_id: UUID,
    player_id: UUID,
    choices: list[dict[str, Any]],
    total_choices: int,
) -> bool:
    """Publish a `choices.extracted` event. Returns True on success, False otherwise."""
    try:
        from e_kafka.producers.choice_extracted_producer import get_choice_extracted_producer

        producer = get_choice_extracted_producer()
        return producer.send_choices_extracted_event(
            save_id=str(save_id),
            player_id=str(player_id),
            choices=choices,
            total_choices=total_choices,
        )
    except Exception as exc:  # noqa: BLE001 - best-effort by design
        logger.warning(f"Kafka indisponível (choices.extracted não publicado): {exc}")
        return False
