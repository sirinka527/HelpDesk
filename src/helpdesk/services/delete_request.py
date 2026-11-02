import logging
from typing import Callable

from ..storage.read_request import read_requests
from ..storage.save_request import save_request


logger = logging.getLogger(__name__)

def delete_request(request_id: int, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> None:
    logger.debug(f"Deleting request with ID: {request_id}")

    data = read_requests()

    if str(request_id) not in data:
        logger.debug(f"Request with ID {request_id} not found")
        func_error_handler("Request not found")
        return

    del data[str(request_id)]
    logger.info(f"Request with ID {request_id} deleted successfully")

    save_request(data)