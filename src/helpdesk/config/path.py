from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "request.json"

LOG_DIR = BASE_DIR / "log"
LOG_FILE = LOG_DIR / "helpdesk.log"