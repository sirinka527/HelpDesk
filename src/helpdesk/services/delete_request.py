from typing import Callable

from ..storage.read_request import read_requests
from ..storage.save_request import save_request


def delete_request(request_id: int, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> None:
    data = read_requests()

    if str(request_id) not in data:
        func_error_handler("Request not found")
        return

    del data[str(request_id)]

    save_request(data)