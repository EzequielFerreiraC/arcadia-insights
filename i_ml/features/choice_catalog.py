"""
Choice catalog & feature engineering helpers for the ML models.
Shared by the training job and the serving layer so features stay consistent.
"""
from __future__ import annotations

# The final decision that we predict.
FINAL_CHOICE_ID = "ep5_final"

ENDINGS: dict[str, str] = {
    "sacrificar_arcadia_bay": "Sacrifice Arcadia Bay",
    "sacrificar_chloe": "Sacrifice Chloe",
}

# (choice_id, option_a, option_b, readable_label_for_option_a)
# Feature = 1 when the player picked option_a, else 0.
FEATURE_CHOICES: list[tuple[str, str, str, str]] = [
    ("ep1_report_nathan", "reportar", "nao_reportar", "Reportar Nathan"),
    ("ep1_lisa_plant", "regar", "nao_regar", "Regar a planta da Lisa"),
    ("ep1_kate_petition", "assinar", "nao_assinar", "Assinar a petição da Kate"),
    ("ep2_save_kate", "salvar", "nao_salvar", "Salvar Kate"),
    ("ep2_help_alyssa", "ajudar", "ignorar", "Ajudar Alyssa"),
    ("ep3_trust_chloe", "confiar", "nao_confiar", "Confiar em Chloe"),
    ("ep3_blame_pool", "encobrir", "assumir", "Encobrir o desastre da piscina"),
    ("ep4_accuse_nathan", "acusar", "nao_acusar", "Acusar Nathan"),
    ("ep4_comfort_victoria", "confortar", "ignorar", "Confortar Victoria"),
]

FEATURE_IDS = [c[0] for c in FEATURE_CHOICES]
FEATURE_LABELS = {c[0]: c[3] for c in FEATURE_CHOICES}

# Choices whose option_a is the "empathetic / caring" pick — used to name clusters.
EMPATHETIC = {
    "ep1_lisa_plant": "regar",
    "ep1_kate_petition": "assinar",
    "ep2_save_kate": "salvar",
    "ep2_help_alyssa": "ajudar",
    "ep3_trust_chloe": "confiar",
    "ep4_comfort_victoria": "confortar",
}


def build_feature_vector(picks: dict[str, str]) -> list[int]:
    """Turn a player's {choice_id: option} map into the model feature vector."""
    return [1 if picks.get(cid) == opt_a else 0 for cid, opt_a, _opt_b, _label in FEATURE_CHOICES]


def empathy_score(picks: dict[str, str]) -> int:
    """Count how many empathetic options the player picked (0..6)."""
    return sum(1 for cid, opt in EMPATHETIC.items() if picks.get(cid) == opt)


def humanize(option: str) -> str:
    return option.replace("_", " ").replace("nao ", "não ").capitalize()
