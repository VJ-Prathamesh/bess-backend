from enum import Enum
from pydantic import BaseModel, Field


class WeatherSource(str, Enum):
    nsrdb = "NSRDB"
    pvgis = "PVGIS"
    nasa = "NASA POWER"


class LocationWeatherRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class LocationCreate(BaseModel):
    project_id: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    weather_source: WeatherSource = WeatherSource.nsrdb


class LocationResponse(BaseModel):
    location_id: str
    project_id: str
    latitude: float
    longitude: float
    city: str
    state: str
    country: str
    timezone: str
    elevation: float
    avg_solar_radiation: float
    annual_solar_radiation: float
    avg_temperature: float
    weather_source: str
    dataset: str
