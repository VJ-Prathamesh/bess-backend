from fastapi import APIRouter, Query

from app.modules.pv_sizing import schemas, service

router = APIRouter(tags=["PV Sizing"])


@router.get("/catalog/pv-modules", response_model=list[schemas.PVModuleOut])
def get_pv_modules(
    manufacturer: str | None = None,
    min_power_w: float | None = Query(default=None, ge=0),
):
    return service.list_pv_modules(manufacturer, min_power_w)


@router.put("/projects/{id}/pv-config", response_model=schemas.PVConfigOut)
def set_pv_config(id: int, payload: schemas.PVConfigIn):
    return service.configure_pv(id, payload)
