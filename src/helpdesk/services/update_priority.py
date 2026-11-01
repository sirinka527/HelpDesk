from datetime import datetime
from typing import Callable

from ..config import PRIORITY_OPTIONS
from ..storage.read_request import read_requests
from ..storage.save_request import save_request


def update_priority(request_id: int, new_priority: str, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> None:
    if new_priority not in PRIORITY_OPTIONS:
        func_error_handler("Invalid priority")
        return

    data = read_requests()

    request = data.get(str(request_id))
    if not request:
        func_error_handler("Request not found")
        return

    request["priority"] = new_priority
    request["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    data[str(request_id)] = request

    save_request(data)
