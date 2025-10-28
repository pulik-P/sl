documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

# Владелец по номеру дока
def get_owner_by_document_number(doc_number):
    for doc in documents:
        if doc['number'] == doc_number:
            return doc['name']
    return None

# Полка по номеру дока
def get_shelf_by_document_number(doc_number):
    for shelf, docs in directories.items():
        if doc_number in docs:
            return shelf
    return None

# Если ввести р
def process_command_p():
    doc_number = input("Введите номер документа: ")
    owner = get_owner_by_document_number(doc_number)

    if owner:
        print(f"Владелец документа: {owner}")
    else:
        print("Документ с таким номером не найден.")

# Если ввести s
def process_command_s():
    doc_number = input("Введите номер документа: ")
    shelf = get_shelf_by_document_number(doc_number)

    if shelf:
        print(f"Документ хранится на полке: {shelf}")
    else:
        print("Документ с таким номером не найден.")

# Выводит какие есть команды
def show_available_commands():
    print("Программа для автоматизации работы секретаря")
    print("\nДоступные команды:")
    print("p - найти владельца документа")
    print("s - найти полку документа")
    print("q - выход из программы")

# Работа всей программы в целом
def main():
    show_available_commands()

    while True:
        command = input("\nВведите команду: ").strip().lower() #strip()- если случайно поставят пробел при вводе эта команда уберет! lower()- Если ввести с большой буквы, приведет в нижний регистр!

        if command == 'q':
            print("Программа завершена.")
            break
        elif command == 'p':
            process_command_p()
        elif command == 's':
            process_command_s()
        else:
            print("Неизвестная команда. Попробуйте снова.")
            show_available_commands()

if __name__ == "__main__":
    main()