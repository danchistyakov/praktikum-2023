import csv
from pymongo import MongoClient
from prettytable import PrettyTable

# Функция для подключения к MongoDB
def connect_to_mongodb():
    client = MongoClient('mongodb://user:pass@localhost:27017/?authSource=admin')
    db = client['students_database']
    return db

# Функция для создания файла Egor-1point.csv
def create_csv_file():
    file_name = 'Egor-1point.csv'
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['ID студента', '№ группы', 'ФИО', 'Средний балл', '№ зачетной книжки']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
    return file_name

# Функция для добавления студентов в файл CSV
def add_students_to_csv():
    file_name = create_csv_file()
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['ID студента', '№ группы', 'ФИО', 'Средний балл', '№ зачетной книжки']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        print("Введите данные студентов. Для прекращения ввода введите 'СТОП'.")

        for _ in range(15):
            student_id = input('Введите ID студента: ')
            if student_id.upper() == 'СТОП':
                break

            group_number = input('Введите № группы: ')
            if group_number.upper() == 'СТОП':
                break

            full_name = input('Введите ФИО студента: ')
            if full_name.upper() == 'СТОП':
                break

            while True:
                try:
                    average_grade = float(input('Введите средний балл успеваемости (от 0 до 5): '))
                    if not 0 <= average_grade <= 5:
                        raise ValueError("Некорректный формат балла")
                    break
                except ValueError as e:
                    print(e)
                    continue

            record_book_number = input('Введите № зачетной книжки: ')
            if record_book_number.upper() == 'СТОП':
                break

            writer.writerow({
                'ID студента': student_id,
                '№ группы': group_number,
                'ФИО': full_name,
                'Средний балл': average_grade,
                '№ зачетной книжки': record_book_number
            })
        print("Ввод данных завершен.")
        return file_name

# Функция для сохранения данных из CSV в MongoDB
def save_to_mongodb_from_csv(file_name):
    db = connect_to_mongodb()
    collection = db['students_collection']

    with open(file_name, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        students = [student for student in reader]

    collection.insert_many(students)

# Функция для вывода данных из MongoDB в виде таблицы
def display_from_mongodb():
    db = connect_to_mongodb()
    collection = db['students_collection']

    table = PrettyTable()
    table.field_names = ['ID студента', '№ группы', 'ФИО', 'Средний балл', '№ зачетной книжки']

    for student in collection.find():
        table.add_row([
            student['ID студента'],
            student['№ группы'],
            student['ФИО'],
            student['Средний балл'],
            student['№ зачетной книжки']
        ])

    print(table)

def main():
    while True:
        print("Меню:")
        print("1. Создать файл и структуру таблицы")
        print("2. Внести студентов в файл")
        print("3. Сохранить данные в MongoDB и вывести на экран")
        print("4. Сохранить данные из MongoDB в Excel и вывести на экран")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            create_csv_file()  # Создать файл и структуру таблицы
        elif choice == '2':
            add_students_to_csv()  # Добавление студентов в файл
            continue  # Возврат к главному меню после добавления студентов
        elif choice == '3':
            file_name = 'Egor-1point.csv'
            save_to_mongodb_from_csv(file_name)  # Сохранение данных из CSV в MongoDB
            display_from_mongodb()  # Вывод данных из MongoDB
        elif choice == '4':
            # Здесь будет код для сохранения данных из MongoDB в Excel и вывода на экран
            pass
        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Пожалуйста, выберите существующий вариант.")

if __name__ == "__main__":
    main()
