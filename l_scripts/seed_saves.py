#!/usr/bin/env python3
"""
Seed script — generates synthetic Life is Strange saves and uploads them to the API.

This populates the database so the analytics endpoints return realistic numbers
(popular vs. rare choices, community percentages, leaderboard, etc.).

Usage:
    python l_scripts/seed_saves.py --count 300 --api http://localhost:8000

Each generated player samples one option per decision point, weighted so the
aggregate popularity matches the canonical Life is Strange community splits.
"""
from __future__ import annotations

import argparse
import io
import json
import random
import sys
import time

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("Este script precisa de 'requests' (pip install requests).")

COUNTRIES = ["BR", "US", "GB", "FR", "DE", "JP", "CA", "AU", "PT", "ES", "MX", "IT"]
PLATFORMS = ["PC", "PlayStation", "Xbox", "Nintendo"]

# choice_id, chapter, choice_text, {option: weight}
CATALOG = [
    (1, 1, "ep1_report_nathan", "Reportar Nathan ao diretor", {"reportar": 0.49, "nao_reportar": 0.51}),
    (1, 2, "ep1_lisa_plant", "Regar a planta da Lisa", {"regar": 0.74, "nao_regar": 0.26}),
    (1, 3, "ep1_kate_petition", "Assinar a petição da Kate", {"assinar": 0.88, "nao_assinar": 0.12}),
    (2, 1, "ep2_save_kate", "Salvar Kate do telhado", {"salvar": 0.82, "nao_salvar": 0.18}),
    (2, 2, "ep2_help_alyssa", "Ajudar Alyssa", {"ajudar": 0.69, "ignorar": 0.31}),
    (3, 1, "ep3_trust_chloe", "Confiar em Chloe", {"confiar": 0.63, "nao_confiar": 0.37}),
    (3, 2, "ep3_blame_pool", "Encobrir o desastre da piscina", {"encobrir": 0.41, "assumir": 0.59}),
    (4, 1, "ep4_accuse_nathan", "Acusar Nathan Prescott", {"acusar": 0.04, "nao_acusar": 0.96}),
    (4, 2, "ep4_comfort_victoria", "Confortar Victoria", {"confortar": 0.55, "ignorar": 0.45}),
    (5, 1, "ep5_final", "Decisão final no farol", {"sacrificar_arcadia_bay": 0.53, "sacrificar_chloe": 0.47}),
]


def weighted_choice(options: dict[str, float]) -> str:
    keys = list(options.keys())
    weights = list(options.values())
    return random.choices(keys, weights=weights, k=1)[0]


def build_save(seed: int) -> dict:
    random.seed(None)  # keep it truly random per player
    choices = []
    base_ts = 500
    for episode, chapter, choice_id, choice_text, options in CATALOG:
        base_ts += random.randint(600, 1400)
        choices.append(
            {
                "episode": episode,
                "chapter": chapter,
                "choice_id": choice_id,
                "choice_text": choice_text,
                "option_selected": weighted_choice(options),
                "timestamp_in_game": base_ts,
            }
        )
    return {
        "player": {
            "country": random.choice(COUNTRIES),
            "platform": random.choice(PLATFORMS),
            "game_version": "1.0",
        },
        "choices": choices,
        # nonce makes each file's checksum unique
        "nonce": f"{seed}-{random.random()}",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=300)
    parser.add_argument("--api", default="http://localhost:8000")
    args = parser.parse_args()

    url = f"{args.api.rstrip('/')}/api/v1/saves/upload"
    ok, dup, err = 0, 0, 0

    print(f"Enviando {args.count} saves para {url} …")
    for i in range(args.count):
        payload = json.dumps(build_save(i)).encode("utf-8")
        files = {"file": (f"seed_{i:04d}.json", io.BytesIO(payload), "application/json")}
        try:
            resp = requests.post(url, files=files, timeout=30)
            if resp.status_code == 201:
                ok += 1
            elif resp.status_code == 409:
                dup += 1
            else:
                err += 1
                if err <= 3:
                    print(f"  [{resp.status_code}] {resp.text[:200]}")
        except requests.RequestException as exc:
            err += 1
            if err <= 3:
                print(f"  erro de rede: {exc}")
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{args.count} (ok={ok}, dup={dup}, err={err})")
        time.sleep(0.005)

    print(f"\nConcluído: {ok} criados, {dup} duplicados, {err} erros.")


if __name__ == "__main__":
    main()
