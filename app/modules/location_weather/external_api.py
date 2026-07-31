import json
import os
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

NSRDB_API_KEY = os.getenv("NSRDB_API_KEY", "AnzJhrz72E2QUH90ahk4XD05oa9gGRgoLSQVBUIe")


def _get_timezone_label(longitude: float) -> str:
    offset_hours = int(round(longitude / 15.0))
    offset_hours = max(-12, min(14, offset_hours))
    sign = "+" if offset_hours >= 0 else "-"
    return f"UTC {sign}{abs(offset_hours)}"


def _reverse_geocode(latitude: float, longitude: float) -> Dict[str, Any]:
    endpoint = (
        "https://nominatim.openstreetmap.org/reverse"
        f"?format=jsonv2&lat={latitude}&lon={longitude}&zoom=10"
    )

    try:
        request = urllib.request.Request(
            endpoint,
            headers={"User-Agent": "bess-backend/1.0"},
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = json.load(response)
    except Exception:
        return {"city": "Unknown", "state": "", "country": "Unknown"}

    address = payload.get("address", {})
    return {
        "city": address.get("city") or address.get("town") or address.get("village") or address.get("hamlet") or "Unknown",
        "state": address.get("state") or address.get("region") or "",
        "country": address.get("country") or "Unknown",
    }


def _fetch_solar_resource(latitude: float, longitude: float) -> Dict[str, Any]:
    params = {
        "api_key": NSRDB_API_KEY,
        "lat": latitude,
        "lon": longitude,
    }
    endpoint = "https://developer.nrel.gov/api/solar/solar_resource/v1.json?" + urllib.parse.urlencode(params)

    try:
        request = urllib.request.Request(endpoint, headers={"User-Agent": "bess-backend/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except Exception:
        return {}

    outputs = payload.get("outputs", {})
    avg_ghi = outputs.get("avg_ghi")
    annual_ghi = outputs.get("annual_ghi")

    if avg_ghi is None:
        avg_ghi = 0.0

    if annual_ghi is None:
        annual_ghi = float(avg_ghi) * 365.0

    elevation = payload.get("inputs", {}).get("site", {}).get("elevation")
    if elevation is None:
        elevation = 0.0

    return {
        "avg_solar_radiation": float(avg_ghi),
        "annual_solar_radiation": float(annual_ghi),
        "elevation": float(elevation),
    }


def _fetch_temperature(latitude: float, longitude: float) -> Optional[float]:
    endpoint = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current=temperature_2m&timezone=auto"
    )

    try:
        request = urllib.request.Request(endpoint, headers={"User-Agent": "bess-backend/1.0"})
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = json.load(response)
    except Exception:
        return None

    current = payload.get("current", {})
    temperature = current.get("temperature_2m")
    return float(temperature) if temperature is not None else None


def build_weather_payload(
    latitude: float,
    longitude: float,
    location_id: str,
    project_id: str,
    weather_source: str = "NSRDB",
) -> Dict[str, Any]:
    geocode = _reverse_geocode(latitude, longitude)
    solar_resource = _fetch_solar_resource(latitude, longitude)
    avg_temperature = _fetch_temperature(latitude, longitude)

    if avg_temperature is None:
        avg_temperature = 0.0

    return {
        "location_id": location_id,
        "project_id": project_id,
        "latitude": round(float(latitude), 6),
        "longitude": round(float(longitude), 6),
        "city": geocode.get("city", "Unknown"),
        "state": geocode.get("state", ""),
        "country": geocode.get("country", "Unknown"),
        "timezone": _get_timezone_label(longitude),
        "elevation": round(float(solar_resource.get("elevation", 0.0)), 6),
        "avg_solar_radiation": round(float(solar_resource.get("avg_solar_radiation", 0.0)), 2),
        "annual_solar_radiation": round(float(solar_resource.get("annual_solar_radiation", 0.0)), 2),
        "avg_temperature": round(float(avg_temperature), 2),
        "weather_source": weather_source,
        "dataset": f"{weather_source.lower()}-{location_id}",
    }


def fetch_weather_payload(latitude: float, longitude: float, location_id: str, project_id: str, weather_source: str = "NSRDB") -> Dict[str, Any]:
    return build_weather_payload(latitude, longitude, location_id, project_id, weather_source)
