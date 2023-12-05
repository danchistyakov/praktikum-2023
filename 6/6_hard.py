import os
import shutil
import pandas as pd
from pymongo import MongoClient
from prettytable import PrettyTable

def create_file():
    with open("Egor-1point.txt", "w") as file:
        i = 0
        while i < 55:
            file.write(f"Строка {i + 1}\n")
            i += 1

def list_files_folders():
    return os.listdir()

def rename_file():
    os.rename("Egor-1point.txt", "Egor-2points.txt")

def create_folder():
    os.mkdir("Kirill-3points")

def move_file():
    shutil.move("Egor-2points.txt", "Kirill-3points/Egor-2points.txt")

def file_size():
    return os.path.getsize("Kirill-3points/Egor-2points.txt")

# Импорты и другие функции остаются без изменений

def save_data_to_mongodb(collection):
    file_name = './Kirill-3points/Egor-2points.txt'
    try:
        # Чтение данных из текстового файла
        with open(file_name, 'r') as file:
            lines = file.readlines()
            data_dict = [{'line': line.strip()} for line in lines]
        collection.insert_many(data_dict)
        print(f"Данные из файла '{file_name}' успешно сохранены в MongoDB.")
    except FileNotFoundError:
        print(f"Файл '{file_name}' не найден.")
    except Exception as e:
        print(f"Ошибка при сохранении данных в MongoDB: {e}")


def export_mongodb_to_excel(collection):
    try:
        data = pd.DataFrame(list(collection.find()))
        data.to_excel('output.xlsx', index=False)
        print(f"Данные успешно сохранены в файл {'output.xlsx'}.")
    except Exception as e:
        print(f"Ошибка при экспорте данных из MongoDB в Excel: {e}")


def main_menu():
    client = MongoClient('mongodb://user:pass@localhost:27017/?authSource=admin')
    db = client['points_database']
    collection = db['point']

    while True:
        print("\n1. Создать файл 'Egor-1point.txt'")
        print("2. Вывести все папки и файлы")
        print("3. Переименовать файл и вывести файлы")
        print("4. Создать папку 'Kirill-3points'")
        print("5. Переместить файл в 'Kirill-3points'")
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
        elif choice == "0":
            break

if __name__ == "__main__":
    main_menu()