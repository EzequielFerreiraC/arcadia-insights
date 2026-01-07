"""
ML Serving
==========
Loads the trained artifacts (RandomForest ending predictor + K-Means profiles)
and exposes prediction helpers. Artifacts are cached in memory. If a model is
missing, ModelNotTrained is raised so the API can respond gracefully.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any

import i_ml
from i_ml.features.choice_catalog import build_feature_vector

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(i_ml.__file__)), "trained_models")
_ENDING_PATH = os.path.join(MODELS_DIR, "ending_predictor.joblib")
_PROFILES_PATH = os.path.join(MODELS_DIR, "profiles.json")

_WEIGHTS = ["alto", "médio", "baixo"]


class ModelNotTrained(Exception):
    """Raised when a required model artifact is not available."""


@lru_cache(maxsize=1)
def _ending_bundle() -> dict[str, Any]:
    if not os.path.exists(_ENDING_PATH):
        raise ModelNotTrained("Modelo de predição de final não treinado.")
    import joblib

    return joblib.load(_ENDING_PATH)


@lru_cache(maxsize=1)
def _profiles() -> list[dict[str, Any]]:
    if not os.path.exists(_PROFILES_PATH):
        raise ModelNotTrained("Perfis (clustering) não treinados.")
    with open(_PROFILES_PATH, encoding="utf-8") as f:
        return json.load(f)


def predict_ending(picks: dict[str, str]) -> dict[str, Any]:
    """Predict ending probabilities for a player's choice map."""
    bundle = _ending_bundle()
    model = bundle["model"]
    classes = bundle["classes"]
    endings = bundle["endings"]

    vec = build_feature_vector(picks)
    proba = model.predict_proba([vec])[0]

    predictions = sorted(
        (
            {"ending": endings.get(cls, cls), "probability": round(float(p) * 100, 1)}
            for cls, p in zip(classes, proba)
        ),
        key=lambda d: d["probability"],
        reverse=True,
    )

    direction = predictions[0]["ending"] if predictions else "—"
    factors = [
        {"factor": imp["label"], "weight": _WEIGHTS[min(i, len(_WEIGHTS) - 1)], "direction": direction}
        for i, imp in enumerate(bundle["importances"][:4])
    ]
    return {"predictions": predictions, "factors": factors}


def get_profiles() -> list[dict[str, Any]]:
    return _profiles()
