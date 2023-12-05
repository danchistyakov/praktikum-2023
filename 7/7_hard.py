'''
Сложный вариант. *
2. Файлы. Реализовать программу с интерактивным консольным меню, (т.е. вывод списка действий
по цифрам. При этом при нажатии на цифру у нас должно выполняться определенное действие).
Задания полностью идентичны заданию №1 базовому варианту. При этом в программе к сложному
варианту дополняется еще один пункт (помимо тех, которые есть в среднем):
1. Создать файл с названием и расширением «Egor-1point.csv», в котором программно создать 5 столбцов:
ID студента, № группы, ФИО, средний балл успеваемости (от 0 до 5), № зачетной книжки.
2. Внести 15 отдельных студентов с клавиатуры (input) через цикл while или for в данный файл и вывести
содержимое файла в виде таблицы через форматированный вывод или библиотеку PrettyTable.
3. Сохранить содержимое файла «Egor-1point.csv» в MySQL и вывести из MySQL на экран в виде
таблички (форматированный вывод или PrettyTable).
4. Сохранить данные из MySQL в Excel и вывести из Excel на экран в виде таблички (форматированный
вывод или PrettyTable).
'''

import csv
from pymongo import MongoClient
from prettytable import PrettyTable

# Создание пустого файла 'Egor-1point.csv'
with open('Egor-1point.csv', 'w', newline='', encoding='utf-8') as file:
    # Создание объекта DictWriter для записи заголовков столбцов
    fieldnames = ['ID студента', '№ группы', 'ФИО', 'Средний балл', '№ зачетной книжки']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

# Функция для подключения к MongoDB
def connect_to_mongodb():
    client = MongoClient('mongodb://user:pass@localhost:27017/?authSource=admin')
    db = client['students_database']
    return db



# Функция для добавления студентов в файл CSV
def add_students_to_csv():
    file_name = 'Egor-1point.csv'
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['ID студента', '№ группы', 'ФИО', 'Средний балл', '№ зачетной книжки']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        print("Введите данные студентов. Для прекращения ввода введите 'СТОП'.")

        while True:
            student_id = input('Введите ID студента: ')
            if student_id.upper() == 'СТОП':
                break

            group_number = input('Введите № группы: ')
            if group_number.upper() == 'СТОП':
                break

            full_name = input('Введите ФИО студента: ')
            if full_name.upper() == 'СТОП':
                break

            try:
                average_grade = float(input('Введите средний балл успеваемости (от 0 до 5): '))
                if average_grade == 'СТОП':
                    break
            except ValueError:
                print("Некорректный формат балла. Попробуйте еще раз.")
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
        return  # Возвращаемся в основную функцию


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
            # Здесь будет код для создания файла и структуры таблицы
            pass
        elif choice == '2':
            add_students_to_csv()  # Добавление студентов в файл
            continue  # Возврат к главному меню после добавления студентов
        elif choice == '3':
            save_to_mongodb_from_csv()  # Сохранение данных из CSV в MongoDB
            display_from_mongodb()  # Вывод данных из MongoDB
        elif choice == '4':
            # Здесь будет код для сохранения данных из MongoDB в Excel и вывода на экран
            pass
        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Пожалуйста, выберите существующий вариант.")

# Функция для сохранения данных студентов из CSV в MongoDB
def save_to_mongodb_from_csv():
    db = connect_to_mongodb()
    collection = db['students_collection']

    with open('Egor-1point.csv', 'w', newline='', encoding='utf-8') as file:
        # Создание объекта DictWriter для записи заголовков столбцов
        fieldnames = ['ID студента', '№ группы', 'ФИО', 'Средний балл', '№ зачетной книжки']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()


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



if __name__ == "__main__":
    # Здесь вызовите функции в соответствии с вашими потребностями, например:
    save_to_mongodb_from_csv()  # Сохранение данных в MongoDB из CSV
    display_from_mongodb()  # Вывод данных из MongoDB