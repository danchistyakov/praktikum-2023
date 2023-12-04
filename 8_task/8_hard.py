from pymongo import MongoClient
import pandas as pd
from prettytable import PrettyTable

def create_csv_file():
    df = pd.DataFrame(columns=['ID студента', '№ группы', 'ФИО', 'Средний балл успеваемости', '№ зачетной книжки'])
    file_name = "Egor-1point.csv"
    df.to_csv(file_name, index=False)
    print("Файл CSV с заданными столбцами создан.")


def input_student_data():
    while True:
        try:
            student_id = int(input("Введите ID студента: "))
            group_number = int(input("Введите номер группы: "))
            name = input("Введите ФИО студента: ")
            if any(not c.isalpha() and not c.isspace() for c in name):
                raise ValueError
            average_score = float(input("Введите средний балл успеваемости (от 0 до 5): "))
            if not (0 <= average_score <= 5):
                raise ValueError
            record_book_number = int(input("Введите номер зачетной книжки: "))
            break
        except ValueError:
            print("Некорректный ввод, попробуйте снова.")
        finally:
            print("Попытка ввода завершена.")

    return [student_id, group_number, name, average_score, record_book_number]


def enter_student_data():
    df = pd.read_csv("Egor-1point.csv")

    for _ in range(3):
        student_data = input_student_data()
        df.loc[len(df)] = student_data

    df.to_csv("Egor-1point.csv", index=False)

    table = PrettyTable()
    table.field_names = df.columns
    for row in df.itertuples(index=False):
        table.add_row(row)
    print(table)


def save_to_mongodb(collection):
    df = pd.read_csv('Egor-1point.csv')

    collection.delete_many({})
    collection.insert_many(df.to_dict('records'))

    students = collection.find()
    table = PrettyTable()
    table.field_names = df.columns
    for student in students:
        row = [student[column] for column in df.columns]
        table.add_row(row)

    print(table)


def get_from_mongodb(collection):
    students = list(collection.find())
    df = pd.DataFrame(students)
    excel_file = 'students.xlsx'
    df.to_excel(excel_file, index=False)

    df_from_excel = pd.read_excel(excel_file)

    table = PrettyTable()
    table.field_names = df_from_excel.columns
    for _, row in df_from_excel.iterrows():
        table.add_row(row)
    print(table)


def main_menu():
    client = MongoClient('mongodb://user:pass@localhost:27016/?authSource=admin')
    db = client['students_database']
    collection = db['students']
    while True:
        print("1. Создать файл CSV")
        print("2. Внесение данных студентов")
        print("3. Сохранить CSV-файл в MongoDB и вывести на экран")
        print("4. Сохранить данные из MongoDB в Excel и вывести из Excel на экран в виде таблицы")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            create_csv_file()
        elif choice == '2':
            enter_student_data()
        elif choice == '3':
            save_to_mongodb(collection)
        elif choice == '4':
            get_from_mongodb(collection)
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main_menu()
