import os
import shutil

def main_menu():
    while True:
        print("\n1. Создать файл 'Egor-1point.txt' и внести туда 55 строк.")
        print("2. Вывести все папки и файлы проекта.")
        print("3. Переименовать файл 'Egor-1point.txt' в 'Egor-2points.txt'.")
        print("4. Создать папку 'Kirill-3points'.")
        print("5. Переместить 'Egor-2points.txt' в 'Kirill-3points'.")
        print("6. Вывести размер файла 'Egor-2points.txt'.")
        print("0. Выход")

        choice = input("\nВыберите действие: ")

        if choice == '1':
            create_file()
        elif choice == '2':
            list_files_folders()
        elif choice == '3':
            rename_file()
        elif choice == '4':
            create_folder()
        elif choice == '5':
            move_file()
        elif choice == '6':
            show_file_size()
        elif choice == '0':
            break

def create_file():
    # Создание файла и запись в него 55 строк
    with open("Egor-1point.txt", "w") as file:
        for i in range(1, 56):
            file.write(f"Строка {i}\n")
    print("Файл 'Egor-1point.txt' создан и заполнен.")

def list_files_folders():
    # Вывод всех файлов и папок в текущей директории
    for item in os.listdir():
        print(item)

def rename_file():
    # Переименование файла
    if os.path.exists("Egor-1point.txt"):
        os.rename("Egor-1point.txt", "Egor-2points.txt")
        print("Файл переименован в 'Egor-2points.txt'.")
    else:
        print("Файл 'Egor-1point.txt' не найден.")

def create_folder():
    # Создание папки
    if not os.path.exists("Kirill-3points"):
        os.mkdir("Kirill-3points")
        print("Папка 'Kirill-3points' создана.")
    else:
        print("Папка 'Kirill-3points' уже существует.")

def move_file():
    # Перемещение файла
    if os.path.exists("Egor-2points.txt"):
        shutil.move("Egor-2points.txt", "Kirill-3points/Egor-2points.txt")
        print("Файл перемещен в папку 'Kirill-3points'.")
    else:
        print("Файл 'Egor-2points.txt' не найден.")

def show_file_size():
    # Вывод размера файла
    path = "Kirill-3points/Egor-2points.txt"
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"Размер файла 'Egor-2points.txt': {size} байт.")
    else:
        print("Файл 'Egor-2points.txt' не найден.")

if __name__ == "__main__":
    main_menu()
