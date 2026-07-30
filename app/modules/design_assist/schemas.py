from pydantic import BaseModel
from typing import List



class DesignAssistRequest(BaseModel):

    hourly_loads: List[float]

    solar_irradiation: float



class DesignAssistResponse(BaseModel):

    daytime_energy_kwh: float

    nighttime_energy_kwh: float

    total_daily_energy_kwh: float

    peak_load_kw: float

    peak_daytime_load_kw: float

    peak_nighttime_load_kw: float

    solar_irradiation: float