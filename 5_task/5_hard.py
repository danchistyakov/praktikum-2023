import mysql.connector
from mysql.connector import Error
import random
import openpyxl

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
    'port':'3306',
  'raise_on_warnings': True
}

def print_odds_before_stop(cursor):
    stop = 71278
    raw_list = input('Введите список элементов: ')
    str_list = raw_list.split(' ')
    num_list = list(map(int, str_list))
    print(num_list)
    result = []
    for item in num_list:
        if item == stop:
            break
        if item % 2 == 1:
            result.append(item)
    cursor.execute("INSERT INTO task_5_table (data) VALUES (result)")
    return result

def remove_number():
    to_remove = 500
    raw_list = input('Введите список элементов: ')
    str_list = raw_list.split(' ')
    num_list = list(map(int, str_list))
    return [number for number in num_list if number != to_remove]

def generate_unique_list():
    rn = [x for x in range(1, 76)]
    random.shuffle(rn)
    return print(rn[:20])

def main():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_5")
    cursor.execute("USE task_5")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS your_table_name (
        id INT AUTO_INCREMENT PRIMARY KEY,
        column1 VARCHAR(255),
        column2 INT,
        column3 DATE
    );
    """
    cursor.execute(create_table_query   )


    while True:
        print("""
        1. Ввод списка, фильтрация по нечётным значениям, сохранение и вывод из MySQL.
        2. Ввод списка, удаление значения 500, сохранение и вывод из MySQL.
        3. Генерация списка из случайных значений, сохранение и вывод из MySQL.
        4. Выход.
        """)
        choice = input("Выберите действие: ")
        if choice == "1":
            print_odds_before_stop(cursor)
        elif choice == "2":
            remove_number()
        elif choice == "3":
            generate_unique_list()
        elif choice == "4":
            connection.close()
            break
        else:
            print("Неизвестный выбор!")


if __name__ == "__main__":
    main()
