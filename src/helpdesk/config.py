from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "request.json"

STATUS_OPTIONS = ["open", "in progress", "resolved", "closed"]
PRIORITY_OPTIONS = ["low", "medium", "high", "critical"]

SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "status": {"type": "string", "enum": ["open", "in progress", "resolved", "closed"]},
        "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "title", "description", "status", "priority", "created_at", "updated_at"]
}