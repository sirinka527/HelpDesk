import logging

from ..storage.read_request import read_requests


logger = logging.getLogger(__name__)

def search_requests_by_title(title: str) -> dict:
    logger.debug(f"Searching requests with title containing: {title}")
    data = read_requests()

    results = {id: request for id, request in data.items() if title.lower() in request["title"].lower()}
    logger.info(f"Found {len(results)} requests with title containing: {title}")
    return results