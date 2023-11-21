import os
import shutil
import pandas as pd
import mysql.connector
from prettytable import PrettyTable


# другие необходимые импорты

def main_menu():
    # Тело функции аналогично предыдущему примеру
    pass


def create_file():
    # Создание файла и запись в него 55 строк
    pass


def list_files_folders():
    # Вывод всех файлов и папок в текущей директории
    pass


def rename_file():
    # Переименование файла
    pass


def create_folder():
    # Создание папки
    pass


def move_file():
    # Перемещение файла
    pass


def show_file_size():
    # Вывод размера файла
    pass


def save_mysql_to_excel():
    # Подключение к MySQL
    conn = mysql.connector.connect(host='localhost', user='root', password='root', database='mydb')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute("SELECT * FROM your_table")  # Замените 'your_table' на имя вашей таблицы
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]

    # Создание DataFrame и сохранение в Excel
    df = pd.DataFrame(rows, columns=columns)
    df.to_excel('output.xlsx', index=False)

    # Вывод данных из Excel
    print_excel_data('output.xlsx')

    cursor.close()
    conn.close()


def print_excel_data(file_path):
    # Чтение данных из Excel
    df = pd.read_excel(file_path)

    # Вывод данных через PrettyTable или Pandas
    print(df.to_string(index=False))  # Используется Pandas для вывода в формате таблицы


if __name__ == "__main__":
    main_menu()
