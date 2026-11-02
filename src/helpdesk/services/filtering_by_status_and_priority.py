import logging
from typing import Callable

from ..domain.constants import STATUS_OPTIONS, PRIORITY_OPTIONS
from ..storage.read_request import read_requests


logger = logging.getLogger(__name__)

def filtering_by_status_and_priority(status: str | None = None, priority: str | None = None, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> dict:
    logger.debug("Filtering requests by status and priority")
    data = read_requests()

    if status is not None and status not in STATUS_OPTIONS:
        logger.debug("Invalid status")
        func_error_handler("Invalid status")
        return {}

    if priority is not None and priority not in PRIORITY_OPTIONS:
        logger.debug("Invalid priority")
        func_error_handler("Invalid priority")
        return {}

    if status is not None and status in STATUS_OPTIONS:
        data = {id: request for id, request in data.items() if status == request["status"]}

    if priority is not None and priority in PRIORITY_OPTIONS:
        data = {id: request for id, request in data.items() if priority == request["priority"]}

    logger.info("Filtered requests")
    return data