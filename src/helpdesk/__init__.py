from helpdesk.config import DATA_FILE, STATUS_OPTIONS, PRIORITY_OPTIONS

from helpdesk.storage.read_request import read_requests

from helpdesk.services.create_request import create_request
from helpdesk.services.read_request_by_id import read_request_by_id
from helpdesk.services.update_priority import update_priority
from helpdesk.services.update_status import update_status
from helpdesk.services.delete_request import delete_request
from helpdesk.services.filtering_by_status_and_priority import filtering_by_status_and_priority
from helpdesk.services.search_requests_by_title import search_requests_by_title


def error_handler(message: str) -> None:
    print(f"Error: {message}")

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

def main():
    if not DATA_FILE.is_file():
        DATA_FILE.touch()

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
                "\n3. Показать все обращения" \
                "\n4. Поиск по id")

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

                    case 4:
                        try:
                            request_id = int(input("Введите id обращения: "))
                        except ValueError:
                            print("Введите целочисленное значение")
                            continue

                        results = read_request_by_id(request_id)
                        print_request(results)

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
