import json
from datetime import datetime
from pathlib import Path

petition_file = Path("petition.json")
STATUS_OPTIONS = ["open", "in progress", "resolved", "closed"]
PRIORITY_OPTIONS = ["low", "medium", "high", "critical"]

def error_handler(message: str) -> None:
    print(f"Error: {message}")

def create_petition(title: str, description: str, status: str, priority: str, func_error_handler: callable = lambda x: print(f"Error: {x}")) -> None:

    if not title or not description:
        func_error_handler("Title and description cannot be empty")
        return

    if status not in STATUS_OPTIONS:
        func_error_handler("Invalid status")
        return

    if priority not in PRIORITY_OPTIONS:
        func_error_handler("Invalid priority")
        return

    data = read_petitions()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    next_id = max((int(id) for id in data), default=0) + 1

    petition = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "created_at": now,
        "updated_at": now
    }

    data[str(next_id)] = petition

    with open(petition_file, "w") as f:
        json.dump(data, f, indent=4)

def print_petitions(petitions: dict) -> None:
    if not petitions:
        print("No petitions found.")
        return
    
    for petition in petitions.values():
        print(f"ID: {petition['id']}")
        print(f"Title: {petition['title']}")
        print(f"Description: {petition['description']}")
        print(f"Status: {petition['status']}")
        print(f"Priority: {petition['priority']}")
        print(f"Created At: {petition['created_at']}")
        print(f"Updated At: {petition['updated_at']}")
        print("-" * 40)

def read_petitions() -> dict:
    if not petition_file.exists() or petition_file.stat().st_size == 0:
        return {}

    with open(petition_file, "r") as f:
        data = json.load(f)
        return data

def read_petition_by_id(petition_id: int) -> dict:
    data = read_petitions()
    
    return data.get(str(petition_id), {})

def update_status(petition_id: int, new_status: str, func_error_handler: callable = lambda x: print(f"Error: {x}")) -> None:
    if new_status not in STATUS_OPTIONS:
        func_error_handler("Invalid status")
        return

    data = read_petitions()
    
    petition = data.get(str(petition_id))
    if not petition:
        func_error_handler("Petition not found")
        return

    petition["status"] = new_status
    petition["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(petition_file, "w") as f:
        json.dump(data, f, indent=4)

def update_priority(petition_id: int, new_priority: str, func_error_handler: callable = lambda x: print(f"Error: {x}")) -> None:
    if new_priority not in PRIORITY_OPTIONS:
        func_error_handler("Invalid priority")
        return

    data = read_petitions()

    petition = data.get(str(petition_id))
    if not petition:
        func_error_handler("Petition not found")
        return

    petition["priority"] = new_priority
    petition["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(petition_file, "w") as f:
        json.dump(data, f, indent=4)

def delete_petition(petition_id: int, func_error_handler: callable = lambda x: print(f"Error: {x}")) -> None:
    data = read_petitions()

    if str(petition_id) not in data:
        func_error_handler("Petition not found")
        return

    del data[str(petition_id)]

    with open(petition_file, "w") as f:
        json.dump(data, f, indent=4)

def search_petitions_by_title(title: str) -> dict:
    data = read_petitions()

    results = {id: petition for id, petition in data.items() if title.lower() in petition["title"].lower()}
    return results

def filtering_by_status_and_priotiry(status: str | None = None, priority: str | None = None, func_error_handler: callable = lambda x: print(f"Error: {x}")) -> dict:
    data = read_petitions()

    if status is not None and status not in STATUS_OPTIONS:
        func_error_handler("Invalid status")
        return {}

    if priority is not None and priority not in PRIORITY_OPTIONS:
        func_error_handler("Invalid priority")
        return {}

    if status is not None and status in STATUS_OPTIONS:
        data = {id: pertition for id, pertition in data.items() if status == pertition["status"]}

    if priority is not None and priority in PRIORITY_OPTIONS:
        data = {id: pertition for id, pertition in data.items() if priority == pertition["priority"]}

    return data

def main():
    if not petition_file.is_file():
        petition_file.touch()

    while True:
        print("Выберете действие" \
        "\n1. Создать обращение" \
        "\n2.Прочитать обращения" \
        "\n3.Удалить обращение" \
        "\n4.Изменение статуса/приоритета обращения" \
        "\n5.Выход")

        try:
            user_choise = int(input("--> "))
        except TypeError:
            print("Введите целочисленное значение")

        match user_choise:
            case 1:
                print("Заполните все необходимые данные")

                title = input("Название обращения: ")
                description = input("Подробное описание: ")
                print("---\n" + ", ".join(STATUS_OPTIONS) + "\n---")
                status = input("Статус из вариантов выше: ")
                print("---\n" + ", ".join(PRIORITY_OPTIONS) + "\n---")
                priority = input("Приоритет из вариантов выше: ")

                create_petition(title, description, status, priority, error_handler)

            case 2:
                print("Выберете действие" \
                "\n1. Поиск по названию" \
                "\n2. Фильтрация по статусу и приоритету" \
                "\n3. Показать все обращения")

                try:
                    sub_choise = int(input("--> "))
                except TypeError:
                    print("Введите целочисленное значение")

                match sub_choise:
                    case 1:
                        title = input("Введите название обращения: ")
                        results = search_petitions_by_title(title)
                        print_petitions(results)

                    case 2:
                        print("---\n" + ", ".join(STATUS_OPTIONS) + "\n---")
                        status = input("Статус из вариантов выше: ")
                        print("---\n" + ", ".join(PRIORITY_OPTIONS) + "\n---")
                        priority = input("Приоритет из вариантов выше: ")
                        results = filtering_by_status_and_priotiry(status, priority)
                        print_petitions(results)

                    case 3:
                        petitions = read_petitions()
                        print_petitions(petitions)

            case 3:
                petition_id = int(input("Введите ID обращения для удаления: "))
                delete_petition(petition_id, error_handler)

            case 4:
                petition_id = int(input("Введите ID обращения для изменения: "))
                print("Выберете действие" \
                "\n1. Изменить статус" \
                "\n2. Изменить приоритет")

                try:
                    sub_choise = int(input("--> "))
                except TypeError:
                    print("Введите целочисленное значение")

                match sub_choise:
                    case 1:
                        print("---\n" + ", ".join(STATUS_OPTIONS) + "\n---")
                        status = input("Статус из вариантов выше: ")
                        update_status(petition_id, status, error_handler)
                    case 2:
                        print("---\n" + ", ".join(PRIORITY_OPTIONS) + "\n---")
                        priority = input("Приоритет из вариантов выше: ")
                        update_priority(petition_id, priority, error_handler)

            case 5:
                print("Выход из программы")
                break

if __name__ == "__main__":
    main()
