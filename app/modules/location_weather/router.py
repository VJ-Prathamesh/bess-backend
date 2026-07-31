from fastapi import APIRouter

from .schemas import LocationWeatherRequest
from .service import save_weather_location, get_weather_locations

router = APIRouter(
    prefix="/location",
    tags=["Location"]
)


@router.post("/weather")
def create_weather_location(location: LocationWeatherRequest):

    return save_weather_location(
        latitude=location.latitude,
        longitude=location.longitude,
    )


@router.get("/weather")
def read_weather_locations():

    return get_weather_locations()