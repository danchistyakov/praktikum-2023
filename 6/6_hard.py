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

def save_and_display_from_mongodb():
    client = MongoClient("mongodb://user:pass@localhost:27017/?authSource=admin")
    db = client.your_database
    collection = db.your_collection

    data = pd.DataFrame(list(collection.find()))
    data.to_excel("output.xlsx")

    excel_data = pd.read_excel("output.xlsx")
    table = PrettyTable()
    table.field_names = excel_data.columns.tolist()
    for index, row in excel_data.iterrows():
        table.add_row(row)
    print(table)

def main_menu():
    while True:
        print("\n1. Создать файл 'Egor-1point.txt'")
        print("2. Вывести все папки и файлы")
        print("3. Переименовать файл и вывести файлы")
        print("4. Создать папку 'Kirill-3points'")
        print("5. Переместить файл в 'Kirill-3points'")
        print("6. Вывести размер файла 'Egor-2points.txt'")
        print("8. Сохранить данные из MongoDB в Excel и вывести таблицу")
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
        elif choice == "8":
            save_and_display_from_mongodb()
        elif choice == "0":
            break

if name == "__main__":
    main_menu()