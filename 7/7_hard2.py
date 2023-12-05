import csv
import pymongo
import mysql.connector
import openpyxl
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

def save_to_mongodb():
    file_name = 'Egor-1point.csv'
    client = pymongo.MongoClient('mongodb://user:pass@localhost:27017/')
    db = client['mydatabase']
    collection = db['students']

    with open(file_name, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            collection.insert_one(row)

    print("Содержимое коллекции в MongoDB:")
    for student in collection.find():
        print(student)

def save_to_mysql():
    file_name = 'Egor-1point.csv'
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="pass",
        database="testdb"
    )
    mycursor = mydb.cursor()

    mycursor.execute("CREATE TABLE IF NOT EXISTS students (ID INT AUTO_INCREMENT PRIMARY KEY, student_id VARCHAR(255), group_number VARCHAR(255), full_name VARCHAR(255), average_grade FLOAT, record_book_number VARCHAR(255))")

    with open(file_name, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sql = "INSERT INTO students (student_id, group_number, full_name, average_grade, record_book_number) VALUES (%s, %s, %s, %s, %s)"
            values = (row['ID студента'], row['№ группы'], row['ФИО'], row['Средний балл'], row['№ зачетной книжки'])
            mycursor.execute(sql, values)
            mydb.commit()

    print("Содержимое таблицы в MySQL:")
    mycursor.execute("SELECT * FROM students")
    for student in mycursor.fetchall():
        print(student)

def save_to_excel():
    file_name = 'Egor-1point.csv'
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    with open(file_name, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            sheet.append(row)

    excel_file = 'students.xlsx'
    workbook.save(excel_file)
    print(f"Данные сохранены в Excel файл: {excel_file}")

def main():
    while True:
        print("Меню:")
        print("1. Создать файл и структуру таблицы")
        print("2. Внести студентов в файл")
        print("3. Сохранить данные в MongoDB")
        print("4. Сохранить данные в MySQL")
        print("5. Сохранить данные в Excel")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            create_csv_file()
        elif choice == '2':
            add_students_to_csv()
        elif choice == '3':
            save_to_mongodb()
        elif choice == '4':
            save_to_mysql()
        elif choice == '5':
            save_to_excel()
        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Пожалуйста, выберите существующий вариант.")

if __name__ == "__main__":
    main()
