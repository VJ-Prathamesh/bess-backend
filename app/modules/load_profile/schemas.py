from pydantic import BaseModel
from typing import List



class LoadProfileRequest(BaseModel):

    hourly_loads: List[float]

    battery_autonomy_days: int



class LoadProfileResponse(BaseModel):

    total_daily_energy_kwh: float

    peak_load_kw: float

    average_load_kw: float

    load_factor_percent: float

    battery_autonomy_days: int

    required_backup_energy_kwh: float