import json
from jsonschema import ValidationError, validate
from datetime import datetime
from pathlib import Path
from typing import Callable

schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "status": {"type": "string", "enum": ["open", "in progress", "resolved", "closed"]},
        "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "title", "description", "status", "priority", "created_at", "updated_at"]
}

request_file = Path("request.json")
STATUS_OPTIONS = ["open", "in progress", "resolved", "closed"]
PRIORITY_OPTIONS = ["low", "medium", "high", "critical"]

def save_request(data: dict) -> None:
    with open(request_file, "w") as f:
        json.dump(data, f, indent=4)

def error_handler(message: str) -> None:
    print(f"Error: {message}")

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


def print_request(requests: dict) -> None:
    if not requests:
        print("No requests found.")
        return

    for request in requests.values():
        print(f"ID: {request['id']}")
        print(f"Title: {request['title']}")
        print(f"Description: {request['description']}")
        print(f"Status: {request['status']}")
        print(f"Priority: {request['priority']}")
        print(f"Created At: {request['created_at']}")
        print(f"Updated At: {request['updated_at']}")
        print("-" * 40)

def read_requests() -> dict:
    if not request_file.exists() or request_file.stat().st_size == 0:
        return {}

    with open(request_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from request file")
            return {}

        try:
            for request in data.values():
                validate(instance=request, schema=schema)
        except ValidationError as e:
            print(f"Error: Validation failed for request {request.get('id', 'unknown')}: {e.message}")
            for request_id in list(data.keys()):
                if not validate(instance=data[request_id], schema=schema):
                    del data[request_id]
        
        return data

def read_request_by_id(request_id: int) -> dict:
    data = read_requests()
    
    return data.get(str(request_id), {})

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

def delete_request(request_id: int, func_error_handler: Callable[[str], None] = lambda x: print(f"Error: {x}")) -> None:
    data = read_requests()

    if str(request_id) not in data:
        func_error_handler("Request not found")
        return

    del data[str(request_id)]

    save_request(data)

def search_requests_by_title(title: str) -> dict:
    data = read_requests()

    results = {id: request for id, request in data.items() if title.lower() in request["title"].lower()}
    return results

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

def main():
    if not request_file.is_file():
        request_file.touch()

    while True:
        print("Выберете действие" \
        "\n1. Создать обращение" \
        "\n2.Прочитать обращения" \
        "\n3.Удалить обращение" \
        "\n4.Изменение статуса/приоритета обращения" \
        "\n5.Выход")

        try:
            user_choise = int(input("--> "))
        except ValueError:
            print("Введите целочисленное значение")
            continue

        match user_choise:
            case 1:
                print("Заполните все необходимые данные")

                title = input("Название обращения: ")
                description = input("Подробное описание: ")
                print("---\n" + ", ".join(STATUS_OPTIONS) + "\n---")
                status = input("Статус из вариантов выше: ")
                print("---\n" + ", ".join(PRIORITY_OPTIONS) + "\n---")
                priority = input("Приоритет из вариантов выше: ")

                create_request(title, description, status, priority, error_handler)

            case 2:
                print("Выберете действие" \
                "\n1. Поиск по названию" \
                "\n2. Фильтрация по статусу и приоритету" \
                "\n3. Показать все обращения")

                try:
                    sub_choise = int(input("--> "))
                except ValueError:
                    print("Введите целочисленное значение")
                    continue

                match sub_choise:
                    case 1:
                        title = input("Введите название обращения: ")
                        results = search_requests_by_title(title)
                        print_request(results)

                    case 2:
                        print("---\n" + ", ".join(STATUS_OPTIONS) + "\n---")
                        status = input("Статус из вариантов выше: ")
                        print("---\n" + ", ".join(PRIORITY_OPTIONS) + "\n---")
                        priority = input("Приоритет из вариантов выше: ")
                        results = filtering_by_status_and_priority(status, priority)
                        print_request(results)

                    case 3:
                        requests = read_requests()
                        print_request(requests)

            case 3:
                request_id = int(input("Введите ID обращения для удаления: "))
                delete_request(request_id, error_handler)

            case 4:
                request_id = int(input("Введите ID обращения для изменения: "))
                print("Выберете действие" \
                "\n1. Изменить статус" \
                "\n2. Изменить приоритет")

                try:
                    sub_choise = int(input("--> "))
                except ValueError:
                    print("Введите целочисленное значение")
                    continue
                match sub_choise:
                    case 1:
                        print("---\n" + ", ".join(STATUS_OPTIONS) + "\n---")
                        status = input("Статус из вариантов выше: ")
                        update_status(request_id, status, error_handler)
                    case 2:
                        print("---\n" + ", ".join(PRIORITY_OPTIONS) + "\n---")
                        priority = input("Приоритет из вариантов выше: ")
                        update_priority(request_id, priority, error_handler)

            case 5:
                print("Выход из программы")
                break

if __name__ == "__main__":
    main()
