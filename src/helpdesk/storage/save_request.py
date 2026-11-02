import json
import logging

from helpdesk.config.path import DATA_FILE


logger = logging.getLogger(__name__)

def save_request(data: dict) -> None:
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
            
        logger.debug("Request saved successfully.")
    except Exception as e:
        logger.error(f"Error: Failed to save request", exc_info=True)