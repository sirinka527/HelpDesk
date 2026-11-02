import json
import logging
from jsonschema import ValidationError, validate

from helpdesk.config.path import DATA_FILE
from helpdesk.schemas.request_schema import SCHEMA
from helpdesk.storage.save_request import save_request

logger = logging.getLogger(__name__)

def read_requests() -> dict:
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        logger.warning("No existing requests found.")
        return {}

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            logger.error("Error: Failed to decode JSON from request file")
            return {}

        data_copy = data.copy() 
        count_deleted = 0

        for request_id, request in data_copy.items():
            try:
                validate(instance=request, schema=SCHEMA)
            except ValidationError as e:
                logger.warning(
                    "Validation failed for request %s: %s",
                    request_id,
                    e.message,
                )
                del data[request_id]
                count_deleted += 1

        if count_deleted > 0:
            save_request(data)
            logger.warning("Requests read successfully. Deleted %d invalid requests.", count_deleted)
        else:
            logger.info("Requests read successfully. No invalid requests found.")
        return data