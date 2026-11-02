import logging
from datetime import datetime
from typing import Callable

from ..domain.constants import PRIORITY_OPTIONS
from ..storage.read_request import read_requests
from ..storage.save_request import save_request


logger = logging.getLogger(__name__)

def update_priority(request_id: int, new_priority: str, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> None:
    logger.debug(f"Updating priority for request with ID: {request_id}")
    if new_priority not in PRIORITY_OPTIONS:
        logger.debug("Invalid priority")
        func_error_handler("Invalid priority")
        return

    data = read_requests()

    request = data.get(str(request_id))
    if not request:
        logger.debug(f"Request with ID {request_id} not found")
        func_error_handler("Request not found")
        return

    request["priority"] = new_priority
    request["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    data[str(request_id)] = request

    save_request(data)
    logger.info(f"Priority for request with ID {request_id} updated successfully")
