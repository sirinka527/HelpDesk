from ..storage.read_request import read_requests


def search_requests_by_title(title: str) -> dict:
    data = read_requests()

    results = {id: request for id, request in data.items() if title.lower() in request["title"].lower()}
    return results