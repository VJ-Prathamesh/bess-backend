import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "projects.json"


def read_projects():
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf8")
    with open(DATA_FILE, "r", encoding="utf8") as f:
        return json.load(f)


def save_projects(projects):
    with open(DATA_FILE, "w", encoding="utf8") as f:
        json.dump(projects, f, indent=4)
