from datetime import datetime
from typing import Callable

from ..config import STATUS_OPTIONS, PRIORITY_OPTIONS
from ..storage.read_request import read_requests
from ..storage.save_request import save_request


def create_request(title: str, description: str, status: str, priority: str, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> None:

    if not title.strip() or not description.strip():
        func_error_handler("Title and description cannot be empty")
        return

    if status not in STATUS_OPTIONS:
        func_error_handler("Invalid status")
        return

    if priority not in PRIORITY_OPTIONS:
        func_error_handler("Invalid priority")
        return

    data = read_requests()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    try:
        next_id = max((int(id) for id in data), default=0) + 1
    except ValueError:
        print("Error: Invalid data in request file")
        return

    request = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "created_at": now,
        "updated_at": now
    }

    data[str(next_id)] = request

    save_request(data)