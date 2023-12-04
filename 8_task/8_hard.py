from pymongo import MongoClient
from prettytable import PrettyTable
import csv

client = MongoClient("localhost", 27016)  # измените, если необходимо
db = client["student_database"]
collection = db["students"]

def create_csv_file():
    filename = "Egor-1point.csv"
    headers = ["ID студента", "№ группы", "ФИО", "Средний балл успеваемости", "№ зачетной книжки"]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Запись заголовков

    print("Файл CSV с заданными столбцами создан.")

def enter_student_data(filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for _ in range(15):
            while True:
                try:
                    student_id = int(input("Введите ID студента: "))
                    group_number = int(input("Введите номер группы: "))
                    name = input("Введите ФИО студента: ")
                    average_score = float(input("Введите средний балл успеваемости (от 0 до 5): "))
                    if not (0 <= average_score <= 5):
                        raise ValueError("Средний балл должен быть от 0 до 5.")
                    record_book_number = input("Введите номер зачетной книжки: ")

                    # Запись данных студента в файл
                    writer.writerow([student_id, group_number, name, average_score, record_book_number])
                    break
                except ValueError as e:
                    return print(f"Ошибка ввода: {e}. Попробуйте еще раз.")
            print("Данные студентов внесены в файл.")

def read_csv_file():
    # Сюда добавьте код для чтения данных из файла CSV

def save_to_mongodb():
    # Сюда добавьте код для сохранения данных в MongoDB

def read_from_mongodb():
    # Сюда добавьте код для чтения данных из MongoDB

def save_to_excel():
    # Сюда добавьте код для сохранения данных в Excel

def main_menu():
    while True:
        print("1. Создать файл CSV")
        print("2. Внесение данных студентов")
        print("3. Прочитать данные из CSV")
        print("4. Сохранить данные в MongoDB")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            create_csv_file()
        elif choice == '2':
            enter_student_data()
        elif choice == '3':
            read_csv_file()
        elif choice == '4':
            save_to_mongodb()
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
