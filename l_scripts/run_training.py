#!/usr/bin/env python3
"""
ML Training Pipeline
====================
Reads player choices from Postgres, engineers per-player features and trains:

  - Ending predictor (RandomForest): predicts the final choice from earlier ones.
  - Player clustering (K-Means): groups players into behavioural archetypes.

Artifacts are written to i_ml/trained_models/:
  - ending_predictor.joblib   (model + classes + feature importances)
  - profiles.json             (cluster summaries for the Profiles page)

Run:
    PYTHONPATH=. .venv/bin/python l_scripts/run_training.py
    (or: bash l_scripts/run_training.sh)
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import joblib  # noqa: E402
import numpy as np  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.ensemble import RandomForestClassifier  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402
from sqlalchemy import text  # noqa: E402

from a_configs.database import AsyncSessionLocal  # noqa: E402
from a_configs.logging_config import get_logger, setup_logging  # noqa: E402
from i_ml.features.choice_catalog import (  # noqa: E402
    ENDINGS,
    FEATURE_CHOICES,
    FEATURE_IDS,
    FEATURE_LABELS,
    FINAL_CHOICE_ID,
    build_feature_vector,
    empathy_score,
    humanize,
)

logger = get_logger("ml_training")
MODELS_DIR = os.path.join(ROOT, "i_ml", "trained_models")

CLUSTER_NAMES = ["Empático", "Diplomático", "Impulsivo", "Utilitarista"]
CLUSTER_DESCRIPTIONS = {
    "Empático": "Prioriza pessoas e relações acima do resultado prático.",
    "Diplomático": "Evita conflito e negocia para manter o equilíbrio.",
    "Impulsivo": "Decide rápido, guiado por emoção e instinto do momento.",
    "Utilitarista": "Busca o maior benefício coletivo, mesmo com custo pessoal.",
}


async def load_players() -> dict[str, dict[str, str]]:
    """Return {player_id: {choice_id: option_selected}}."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT player_id::text AS pid, choice_id, option_selected FROM choices")
        )
        players: dict[str, dict[str, str]] = {}
        for row in result.mappings().all():
            players.setdefault(row["pid"], {})[row["choice_id"]] = row["option_selected"]
    return players


def train_ending_predictor(players: dict[str, dict[str, str]]) -> dict:
    X, y = [], []
    for picks in players.values():
        if FINAL_CHOICE_ID in picks:
            X.append(build_feature_vector(picks))
            y.append(picks[FINAL_CHOICE_ID])
    X = np.array(X)
    y = np.array(y)

    model = RandomForestClassifier(n_estimators=120, max_depth=8, random_state=42)
    model.fit(X, y)
    acc = model.score(X, y)

    importances = sorted(
        ({"feature": cid, "label": FEATURE_LABELS[cid], "importance": float(imp)}
         for cid, imp in zip(FEATURE_IDS, model.feature_importances_)),
        key=lambda d: d["importance"],
        reverse=True,
    )
    logger.info(f"Ending predictor treinado com {len(X)} jogadores (train acc={acc:.2f}).")
    return {"model": model, "classes": list(model.classes_), "importances": importances}


def train_clustering(players: dict[str, dict[str, str]]) -> list[dict]:
    ids = list(players.keys())
    X = np.array([build_feature_vector(players[pid]) for pid in ids])
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)

    k = min(4, len(ids)) or 1
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = kmeans.fit_predict(Xs)

    total = len(ids)
    # Rank clusters by mean empathy → map to archetype names.
    cluster_ids = sorted(set(labels))
    empathy_by_cluster = {
        c: float(np.mean([empathy_score(players[ids[i]]) for i in range(total) if labels[i] == c]))
        for c in cluster_ids
    }
    ranked = sorted(cluster_ids, key=lambda c: empathy_by_cluster[c], reverse=True)
    name_for = {c: CLUSTER_NAMES[rank] if rank < len(CLUSTER_NAMES) else f"Perfil {c}"
                for rank, c in enumerate(ranked)}

    profiles = []
    for c in cluster_ids:
        members = [i for i in range(total) if labels[i] == c]
        size = len(members)
        # Fraction of members who picked option_a for each feature.
        typical = []
        fracs = []
        for j, (cid, opt_a, opt_b, label) in enumerate(FEATURE_CHOICES):
            frac = float(np.mean([X[i][j] for i in members])) if members else 0.0
            fracs.append((abs(frac - 0.5), frac, label, opt_b))
        for _dev, frac, label, opt_b in sorted(fracs, key=lambda t: t[0], reverse=True)[:3]:
            typical.append(label if frac >= 0.5 else humanize(opt_b))

        name = name_for[c]
        profiles.append({
            "name": name,
            "description": CLUSTER_DESCRIPTIONS.get(name, ""),
            "players": size,
            "occurrence": round(size * 100.0 / total, 1),
            "typical_choices": typical,
        })

    profiles.sort(key=lambda p: p["players"], reverse=True)
    logger.info(f"Clustering treinado: {k} clusters sobre {total} jogadores.")
    return profiles


async def main() -> None:
    setup_logging(level="INFO")
    os.makedirs(MODELS_DIR, exist_ok=True)
    logger.info("Carregando jogadores do Postgres…")
    players = await load_players()
    if not players:
        logger.warning("Sem jogadores para treinar. Rode o seed primeiro.")
        return

    ending = train_ending_predictor(players)
    joblib.dump(
        {"model": ending["model"], "classes": ending["classes"],
         "importances": ending["importances"], "feature_ids": FEATURE_IDS, "endings": ENDINGS},
        os.path.join(MODELS_DIR, "ending_predictor.joblib"),
    )

    profiles = train_clustering(players)
    with open(os.path.join(MODELS_DIR, "profiles.json"), "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

    logger.info("Treino concluído. Artefatos em i_ml/trained_models/.")


if __name__ == "__main__":
    asyncio.run(main())
