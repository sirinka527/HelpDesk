import logging
from datetime import datetime
from typing import Callable

from ..domain.constants import STATUS_OPTIONS
from ..storage.read_request import read_requests
from ..storage.save_request import save_request


logger = logging.getLogger(__name__)

def update_status(request_id: int, new_status: str, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> None:
    logger.debug(f"Updating status for request with ID: {request_id}")
    if new_status not in STATUS_OPTIONS:
        logger.debug("Invalid status")
        func_error_handler("Invalid status")
        return

    data = read_requests()
    
    request = data.get(str(request_id))
    if not request:
        logger.debug(f"Request with ID {request_id} not found")
        func_error_handler("Request not found")
        return

    request["status"] = new_status
    request["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    data[str(request_id)] = request

    save_request(data)
    logger.info(f"Status for request with ID {request_id} updated successfully")