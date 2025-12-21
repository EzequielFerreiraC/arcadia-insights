"""
Save Pipeline Service
=====================
Shared logic for turning an uploaded save file into persisted choices.

Used by BOTH:
  - the API (inline mode) — extracts choices synchronously on upload;
  - the Kafka worker (kafka mode) — extracts choices asynchronously.

The save format is a simple JSON document (a real Life is Strange save is not
publicly parseable), which keeps the pipeline end-to-end demonstrable:

    {
      "player": { "country": "BR", "platform": "PC", "game_version": "1.0" },
      "choices": [
        {
          "episode": 1, "chapter": 1,
          "choice_id": "ep1_report_nathan",
          "choice_text": "Reportar Nathan ao diretor",
          "option_selected": "nao_reportar",
          "timestamp_in_game": 620
        }
      ]
    }
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from c_api.src.domain.entities.choice import Choice
from c_api.src.domain.entities.player import Player, PlatformEnum
from c_api.src.domain.entities.save import Save, SaveStatusEnum


class SaveParseError(ValueError):
    """Raised when a save file cannot be parsed into the expected structure."""


def compute_checksum(raw: bytes) -> str:
    """MD5 hex digest — matches the 32-char `checksum` column (unique)."""
    return hashlib.md5(raw).hexdigest()


def parse_save(raw: bytes) -> dict[str, Any]:
    """Parse and validate raw save bytes into a dict."""
    try:
        data = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise SaveParseError(f"JSON inválido: {exc}") from exc

    if not isinstance(data, dict):
        raise SaveParseError("O save deve ser um objeto JSON.")

    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        raise SaveParseError("O save não contém uma lista 'choices' válida.")

    for i, c in enumerate(choices):
        missing = [k for k in ("episode", "choice_id", "choice_text", "option_selected") if k not in c]
        if missing:
            raise SaveParseError(f"Escolha #{i} sem campos obrigatórios: {', '.join(missing)}")

    return data


def build_choices(save_id: UUID, player_id: UUID, parsed: dict[str, Any]) -> list[Choice]:
    """Turn the parsed 'choices' array into ORM Choice rows."""
    rows: list[Choice] = []
    for c in parsed["choices"]:
        rows.append(
            Choice(
                player_id=player_id,
                save_id=save_id,
                episode=int(c["episode"]),
                chapter=int(c.get("chapter", 1)),
                choice_id=str(c["choice_id"]),
                choice_text=str(c["choice_text"])[:500],
                option_selected=str(c["option_selected"])[:200],
                timestamp_in_game=int(c.get("timestamp_in_game", 0)),
            )
        )
    return rows


async def resolve_player(
    session: AsyncSession,
    player_id: Optional[UUID],
    parsed: dict[str, Any],
) -> Player:
    """Return an existing player by id, or create one from the save's 'player' block."""
    if player_id is not None:
        existing = await session.get(Player, player_id)
        if existing is None:
            raise SaveParseError(f"Jogador {player_id} não encontrado.")
        return existing

    block = parsed.get("player") or {}
    platform_value = str(block.get("platform", "PC"))
    try:
        platform = PlatformEnum(platform_value)
    except ValueError:
        platform = PlatformEnum.PC

    player = Player(
        country=str(block.get("country", "BR"))[:2].upper(),
        platform=platform,
        game_version=str(block.get("game_version", "1.0"))[:50],
    )
    session.add(player)
    await session.flush()
    return player


async def persist_choices(session: AsyncSession, save: Save, choices: list[Choice]) -> int:
    """Persist extracted choices and mark the save as processed."""
    session.add_all(choices)
    save.status = SaveStatusEnum.PROCESSED
    save.choices_extracted = len(choices)
    save.processed_at = datetime.utcnow()

    # Keep the denormalised counters on the player up to date.
    player = await session.get(Player, save.player_id)
    if player is not None:
        player.total_choices = (player.total_choices or 0) + len(choices)

    await session.flush()
    return len(choices)


async def extract_for_save(session: AsyncSession, save_id: UUID, raw: bytes) -> int:
    """Full extraction path used by the Kafka worker: parse raw → persist choices."""
    save = await session.get(Save, save_id)
    if save is None:
        raise SaveParseError(f"Save {save_id} não encontrado.")

    save.status = SaveStatusEnum.PROCESSING
    await session.flush()

    parsed = parse_save(raw)
    choices = build_choices(save.id, save.player_id, parsed)
    return await persist_choices(session, save, choices)


async def mark_save_failed(session: AsyncSession, save_id: UUID, message: str) -> None:
    """Flag a save as failed with an error message (used by the worker)."""
    save = await session.get(Save, save_id)
    if save is not None:
        save.status = SaveStatusEnum.FAILED
        save.error_message = message[:1000]
        await session.flush()
