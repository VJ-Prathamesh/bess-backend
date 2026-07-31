import uuid

from .external_api import fetch_weather_payload
from .repository import read_locations, write_locations


def save_location(location):
    location_data = location.model_dump()
    return save_weather_location(
        latitude=location_data['latitude'],
        longitude=location_data['longitude'],
        project_id=location_data.get('project_id', 'default'),
    )


def save_weather_location(latitude, longitude, project_id='default'):
    locations = read_locations()
    location_id = str(uuid.uuid4())

    location_dict = fetch_weather_payload(
        latitude=latitude,
        longitude=longitude,
        location_id=location_id,
        project_id=project_id,
        weather_source='NSRDB',
    )

    locations.append(location_dict)
    write_locations(locations)

    return location_dict


def get_locations():
    return read_locations()


def get_weather_locations():
    return read_locations()


def get_location(location_id):
    locations = read_locations()

    for location in locations:
        if location['location_id'] == location_id:
            return location

    return None


def update_location(location_id, data):
    locations = read_locations()

    for location in locations:
        if location['location_id'] == location_id:
            location.update(data)
            write_locations(locations)
            return location

    return None
