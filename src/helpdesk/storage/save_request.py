import json

from ..config import DATA_FILE

def save_request(data: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)