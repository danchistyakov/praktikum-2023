import os
import shutil
import pandas as pd
from pymongo import MongoClient
from prettytable import PrettyTable

def create_file():
    try:
        with open("Egor-1point.txt", "w") as file:
            for i in range(55):
                line = input(f"Введите строку {i + 1}: ")
                file.write(f"Строка {i + 1}: {line}\n")
        print('Файл создан.')
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")

def list_files_folders():
    try:
        return os.listdir()
    except Exception as e:
        print(f"Ошибка при выводе списка файлов: {e}")
        return []

def rename_file():
    if os.path.exists("Egor-1point.txt"):
        os.rename("Egor-1point.txt", "Egor-2points.txt")
    else:
        print("Файл 'Egor-1point.txt' не найден.")

def create_folder():
    if not os.path.exists("Kirill-3points"):
        os.mkdir("Kirill-3points")
        print('Папка "Kirill-3points" создана.')
    else:
        print("Папка 'Kirill-3points' уже существует.")

def move_file():
    if os.path.exists("Egor-2points.txt"):
        shutil.move("Egor-2points.txt", "Kirill-3points/Egor-2points.txt")
        print('Файл «Egor-2points.txt» перемещен в папку «Kirill-3points')
    else:
        print("Файл 'Egor-2points.txt' не найден.")

def file_size():
    try:
        return os.path.getsize("Kirill-3points/Egor-2points.txt")
    except FileNotFoundError:
        print("Файл 'Kirill-3points/Egor-2points.txt' не найден.")
        return 0


def save_data_to_mongodb(collection):
    file_name = './Kirill-3points/Egor-2points.txt'
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            data_dict = [{'line': line.strip()} for line in lines]

        collection.delete_many({})  # Очистка коллекции перед вставкой новых данных
        collection.insert_many(data_dict)
        print(f"Данные из файла '{file_name}' успешно сохранены в MongoDB.")
    except FileNotFoundError:
        print(f"Файл '{file_name}' не найден.")
    except Exception as e:
        print(f"Ошибка при сохранении данных в MongoDB: {e}")


def export_mongodb_to_excel(collection):
    try:
        data = pd.DataFrame(list(collection.find()))
        data.to_excel('output.xlsx', index=False)  # Эта операция перезаписывает файл 'output.xlsx'
        print(f"Данные успешно сохранены в файл 'output.xlsx'.")
    except Exception as e:
        print(f"Ошибка при экспорте данных из MongoDB в Excel: {e}")

file_xlsl_name = 'output.xlsx'
def display_excel_data_with_prettytable(file_xlsl_name):
    try:
        data = pd.read_excel(file_xlsl_name)
        table = PrettyTable()
        table.field_names = data.columns.tolist()  # Установка заголовков столбцов

        for _, row in data.iterrows():
            table.add_row(row)  # Добавление строк в таблицу

        print(table)  # Вывод таблицы
    except Exception as e:
        print(f"Ошибка при чтении данных из Excel: {e}")



def main_menu():
    client = MongoClient('mongodb://user:pass@localhost:27017/?authSource=admin')
    db = client['points_database']
    collection = db['point']

    while True:
        print("\n1. Создать файл 'Egor-1point.txt' и внести туда 55 разных строк с клавиатуры")
        print("2. Вывести все папки и файлы, которые находятся в данном проекте")
        print("3. Переименовать файл «Egor-1point.txt» в «Egor-2points.txt» и вывести все файлы текущей директории")
        print("4. Создать папку 'Kirill-3points'")
        print("5. Переместить файл «Egor-2points.txt» в папку «Kirill-3points")
        print("6. Вывести размер файла 'Egor-2points.txt'")
        print("7. Сохранить данные из MongoDB в Excel и вывести таблицу")
        print("0. Выход")

        choice = input("\nВведите номер действия: ")

        if choice == "1":
            create_file()
        elif choice == "2":
            print(list_files_folders())
        elif choice == "3":
            rename_file()
            print(list_files_folders())
        elif choice == "4":
            create_folder()
            print(list_files_folders())
        elif choice == "5":
            move_file()
        elif choice == "6":
            print(f"Размер файла: {file_size()} байт")
        elif choice == "7":
            save_data_to_mongodb(collection)
            export_mongodb_to_excel(collection)
            display_excel_data_with_prettytable(file_xlsl_name)
        elif choice == "0":
            break

if __name__ == "__main__":
    main_menu()