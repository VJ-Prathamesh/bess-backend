import json
import os
from typing import Final


SCORE_DB_FILE = "app/db_store/pv_config.json"


# Temporary deterministic catalog. It can be replaced by the component catalog
# without changing the API contract.
PV_MODULES: Final[list[dict]] = [
    {
        "id": 1, "manufacturer": "JA Solar", "model_name": "JAM66-D45-630-LB",
        "max_power_w": 630.0, "efficiency_pct": 23.32, "vmp_v": 40.7,
        "imp_a": 15.48, "voc_v": 48.9, "isc_a": 16.18,
        "length_mm": 2382.0, "width_mm": 1134.0, "weight_kg": 32.5, "frame_type": "Aluminium",
        "temp_coeff_voc_pct_per_c": -0.275, "temp_coeff_pmax_pct_per_c": -0.29,
        "temp_coeff_vmp_pct_per_c": -0.29, "max_system_voltage_v": 1500.0,
    },
    {
        "id": 2, "manufacturer": "LONGi", "model_name": "Hi-MO 6 LR5-72HTH-585M",
        "max_power_w": 585.0, "efficiency_pct": 22.6, "vmp_v": 44.1,
        "imp_a": 13.27, "voc_v": 52.4, "isc_a": 14.15,
        "length_mm": 2278.0, "width_mm": 1134.0, "weight_kg": 27.5, "frame_type": "Aluminium",
        "temp_coeff_voc_pct_per_c": -0.265, "temp_coeff_pmax_pct_per_c": -0.29,
        "temp_coeff_vmp_pct_per_c": -0.29, "max_system_voltage_v": 1500.0,
    },
    {
        "id": 3, "manufacturer": "Jinkosolar 2023", "model_name": "JKM630N-78HL4-BDV",
        "max_power_w": 630.0, "efficiency_pct": 22.54, "vmp_v": 47.7,
        "imp_a": 13.21, "voc_v": 57.08, "isc_a": 13.86,
        "length_mm": 2465.0, "width_mm": 1134.0, "weight_kg": 32.4, "frame_type": "Aluminium",
        "temp_coeff_voc_pct_per_c": -0.25, "temp_coeff_pmax_pct_per_c": -0.30,
        "temp_coeff_vmp_pct_per_c": -0.30, "max_system_voltage_v": 1500.0,
    },
]


def list_pv_modules(manufacturer: str | None = None, min_power_w: float | None = None) -> list[dict]:
    modules = PV_MODULES
    if manufacturer:
        needle = manufacturer.casefold()
        modules = [module for module in modules if needle in module["manufacturer"].casefold()]
    if min_power_w is not None:
        modules = [module for module in modules if module["max_power_w"] >= min_power_w]
    return list(modules)


def get_pv_module(module_id: int) -> dict | None:
    return next((module for module in PV_MODULES if module["id"] == module_id), None)


def _load_scores() -> dict:
    if not os.path.exists(SCORE_DB_FILE):
        return {}
    with open(SCORE_DB_FILE, encoding="utf-8") as file:
        return json.load(file)


def save_pv_config(project_id: int, request_payload: dict, calculation_result: dict) -> None:
    """Persist the latest raw input and calculated PV result for each project."""
    scores = _load_scores()
    scores[str(project_id)] = {"input": request_payload, "result": calculation_result}
    os.makedirs(os.path.dirname(SCORE_DB_FILE), exist_ok=True)
    with open(SCORE_DB_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=2)
