'''
Базовый вариант.
1. Файлы. Реализовать программу с интерактивным консольным меню, (т.е. вывод списка действий
по цифрам. При этом при нажатии на цифру у нас должно выполняться определенное действие). При
этом в программе данные пункты должны называться следующим образом:
1. Создать файл с названием и расширением «Egor-1point.csv», в котором программно создать 5 столбцов:
ID студента, № группы, ФИО, средний балл успеваемости (от 0 до 5), № зачетной книжки.
2. Внести 15 отдельных студентов с клавиатуры (input) через цикл while или for в данный файл и вывести
содержимое файла в виде таблицы через форматированный вывод или библиотеку PrettyTable.
'''

import csv
from prettytable import PrettyTable

def create_csv_file():
    file_name = 'Egor-1point.csv'
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['ID студента', '№ группы', 'ФИО', 'Средний балл', '№ зачетной книжки']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()


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


def display_csv_contents():
    file_name = 'Egor-1point.csv'
    with open(file_name, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        table = PrettyTable()
        table.field_names = ['ID студента', '№ группы', 'ФИО', 'Средний балл', '№ зачетной книжки']

        for row in reader:
            table.add_row(
                [row['ID студента'], row['№ группы'], row['ФИО'], row['Средний балл'], row['№ зачетной книжки']])
        print(table)

def main():
    while True:
        print("Меню:")
        print("1. Создать файл и структуру таблицы")
        print("2. Внести студентов в файл")
        print("3. Вывести содержимое файла")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            create_csv_file()
        elif choice == '2':
            add_students_to_csv()
        elif choice == '3':
            display_csv_contents()
        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Пожалуйста, выберите существующий вариант.")

if __name__ == "__main__":
    main()

