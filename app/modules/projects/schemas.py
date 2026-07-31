from enum import Enum

from pydantic import BaseModel, Field


class ApplicationType(str, Enum):
    residential = "Residential"
    commercial = "Commercial"
    industrial = "Industrial"


class ChargingSource(str, Enum):
    solar_only = "Solar PV Only"
    solar_grid = "Solar PV + Grid Hybrid"
    grid_only = "Grid Only"


class ProjectCreate(BaseModel):
    project_name: str = Field(..., min_length=3)
    location_name: str
    application_type: ApplicationType
    charging_source: ChargingSource


class ProjectResponse(ProjectCreate):
    project_id: str
    current_step: int
