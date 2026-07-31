import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "location_data.json"


def read_locations():

    if not DATA_FILE.exists():

        with open(DATA_FILE, "w") as file:
            json.dump([], file)

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def write_locations(locations):

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(locations, file, indent=4)