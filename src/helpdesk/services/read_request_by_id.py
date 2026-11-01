from ..storage.read_request import read_requests


def read_request_by_id(request_id: int) -> dict:
    data = read_requests()

    if str(request_id) not in data:
        return {}
    
    return {request_id: data[str(request_id)]}