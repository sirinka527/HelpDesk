from datetime import datetime
from typing import Callable

from ..config import STATUS_OPTIONS
from ..storage.read_request import read_requests
from ..storage.save_request import save_request


def update_status(request_id: int, new_status: str, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> None:
    if new_status not in STATUS_OPTIONS:
        func_error_handler("Invalid status")
        return

    data = read_requests()
    
    request = data.get(str(request_id))
    if not request:
        func_error_handler("Request not found")
        return

    request["status"] = new_status
    request["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    data[str(request_id)] = request

    save_request(data)