from typing import Callable

from ..config import PRIORITY_OPTIONS, STATUS_OPTIONS
from ..storage.read_request import read_requests


def filtering_by_status_and_priority(status: str | None = None, priority: str | None = None, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> dict:
    data = read_requests()

    if status is not None and status not in STATUS_OPTIONS:
        func_error_handler("Invalid status")
        return {}

    if priority is not None and priority not in PRIORITY_OPTIONS:
        func_error_handler("Invalid priority")
        return {}

    if status is not None and status in STATUS_OPTIONS:
        data = {id: request for id, request in data.items() if status == request["status"]}

    if priority is not None and priority in PRIORITY_OPTIONS:
        data = {id: request for id, request in data.items() if priority == request["priority"]}

    return data