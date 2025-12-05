import csv

def load_csv_file(file_path):
   file = open(file_path, 'r')

   reader = csv.DictReader(file)
   data = list(reader)
   file.close()
   return data

def parse_data(rows):
    pars_data = []
    for row in rows:
        row['age'] = int(row['age'])
        row['bill'] = int(row['bill'])
        if row['region'] == '-':
            row['region'] = 'не указан'

        pars_data.append(row)
    return pars_data


def format_user_description(user_data):
    name = user_data['name']
    device_type = user_data['device_type']
    browser = user_data['browser']
    gender = user_data['sex']
    age = user_data['age']
    bill = user_data['bill']
    region = user_data['region']

    description = (f"ФИО: {name}\n"
                   f"Пол: {gender}\n"
                   f"Возраст: {age} лет\n"
                   f"Устройство, с которого выполнялась покупка: {device_type}\n"
                   f"Браузер: {browser}\n"
                   f"Сумма чека: {bill}y.e.\n"
                   f"Регион покупки: {region}\n")

    return description

def create_users_descript(user_data):
     users_descript = []
     for user in user_data:
         description = format_user_description(user)
         users_descript.append(description)

     return users_descript

def save_text_file(users_descript, output_file):
    file = open(output_file, 'w')

    for user_descript in users_descript:
        file.write(f"{user_descript}")
    file.close()
    print(f"Файл успешно сохранен: {output_file}")

def process_csv_descriptions(input_file, output_file):
    print(f"Загрузка данных из файла: {input_file}")
    raw_data = load_csv_file(input_file)
    parsed_data = parse_data(raw_data)
    users_descript = create_users_descript(parsed_data)
    save_text_file(users_descript, output_file)

def examination():
    print("\nПРОВЕРКА ФАЙЛА:")
    with open(output_txt, 'r') as f:
        for i in range(14):
            line = f.readline()
            print(line, end='')

    print("-" * 50)
    print("Файл создан успешно!")


if __name__ == '__main__':
    input_csv = "web_clients_correct.csv"
    output_txt = "users_descriptions.txt"

    process_csv_descriptions(input_csv, output_txt)
    examination()