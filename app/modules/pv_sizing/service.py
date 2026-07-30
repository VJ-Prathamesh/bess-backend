from fastapi import HTTPException

from app.modules.projects import repository as projects_repository
from app.modules.pv_sizing import calculation, repository, schemas


def list_pv_modules(manufacturer: str | None = None, min_power_w: float | None = None) -> list[dict]:
    return repository.list_pv_modules(manufacturer, min_power_w)


def configure_pv(project_id: int, payload: schemas.PVConfigIn) -> dict:
    if not projects_repository.get(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    module = repository.get_pv_module(payload.pv_module_id)
    if not module:
        raise HTTPException(status_code=404, detail="PV module not found")
    result = calculation.calculate_pv_configuration(
        module, payload.modules_per_string, payload.number_of_strings,
        payload.inverter.model_dump(), payload.site_conditions.min_temperature_c,
        payload.site_conditions.max_temperature_c, payload.energy_design.daily_energy_kwh,
        payload.energy_design.peak_sun_hours, payload.energy_design.performance_ratio,
        payload.energy_design.safety_margin_pct, payload.scorecard.bess_capacity_kwh,
        payload.scorecard.coupling_type, payload.mounting.mounting_type,
        payload.mounting.modules_per_row, payload.mounting.rows_per_table,
        payload.mounting.total_tables, payload.mounting.module_orientation,
    )
    response = {"project_id": project_id, "pv_module_id": payload.pv_module_id,
                "modules_per_string": payload.modules_per_string,
                "number_of_strings": payload.number_of_strings, **result}
    repository.save_pv_config(project_id, payload.model_dump(), response)
    return response
