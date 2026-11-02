import logging

from ..storage.read_request import read_requests


logger = logging.getLogger(__name__)

def read_request_by_id(request_id: int) -> dict:
    logger.debug(f"Reading request with ID: {request_id}")
    data = read_requests()

    if str(request_id) not in data:
        logger.debug(f"Request with ID {request_id} not found")
        return {}
    
    logger.info(f"Request with ID {request_id} found")
    return {request_id: data[str(request_id)]}