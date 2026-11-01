from jsonschema import ValidationError, validate
import json

from ..config import DATA_FILE, SCHEMA

def read_requests() -> dict:
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return {}

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from request file")
            return {}

        try:
            for request in data.values():
                validate(instance=request, schema=SCHEMA)
        except ValidationError as e:
            print(f"Error: Validation failed for request {request.get('id', 'unknown')}: {e.message}")
            for request_id in list(data.keys()):
                if not validate(instance=data[request_id], schema=SCHEMA):
                    del data[request_id]
        
        return data