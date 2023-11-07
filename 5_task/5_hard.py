import mysql.connector
from mysql.connector import Error
import random
import openpyxl

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '3306',
    'raise_on_warnings': True
}


def set_lists(cursor, connection):
    raw_list = input('Введите список элементов для задачи 1: ')
    str_list = raw_list.split(' ')
    list_as_string = ', '.join(str_list)
    sql = """
    INSERT INTO task_5_table (id, data) VALUES (%s, %s) AS new_values (id, data)
    ON DUPLICATE KEY UPDATE data = new_values.data;
    """
    values = (1, list_as_string,)
    cursor.execute(sql, values)
    raw_list = input('Введите список элементов для задачи 1: ')
    str_list = raw_list.split(' ')
    list_as_string = ', '.join(str_list)
    values = (2, list_as_string,)
    cursor.execute(sql, values)
    connection.commit()
    cursor.execute("SELECT data FROM task_5_table")
    result = cursor.fetchall()
    for item in result:
        print(item)


def print_odds_before_stop(cursor, connection):
    stop = 71278
    cursor.execute("SELECT data FROM task_5_table WHERE id = 1")
    raw_list = cursor.fetchone()[0]
    print(raw_list)
    num_list = [int(number) for number in raw_list.split(',')]
    print(num_list)
    filtered_list = []
    for item in num_list:
        if item == stop:
            break
        if item % 2 == 1:
            filtered_list.append(item)
    sql = """
        INSERT INTO task_5_table (id, data) VALUES (%s, %s) AS new_values (id, data)
        ON DUPLICATE KEY UPDATE data = new_values.data;
        """
    str_value = ', '.join(filtered_list)
    values = (1, str_value)
    cursor.execute(sql, values)
    connection.commit()
    cursor.execute("SELECT data FROM task_5_table WHERE id = 1")
    result = cursor.fetchone()
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
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_5")
    except:
        print("")
    cursor.execute("USE task_5")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS task_5_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data VARCHAR(255)
    );
    """
    try:
        cursor.execute(create_table_query)
    except:
        print("")

    while True:
        print("""
        1. Ввод/генерация списков, сохранение и вывод из MySQL.
        2. Выполнение всех операций из базового варианта, сохранение результатов и вывод из MySQL (тоже в виде таблицы).
        3. Сохранить данные из MySQL в Excel и вывести на экран..
        4. Выход.
        """)
        choice = input("Выберите действие: ")
        if choice == "1":
            set_lists(cursor, connection)
        elif choice == "2":
            print_odds_before_stop(cursor, connection)
            remove_number(cursor, connection)
        elif choice == "3":
            generate_unique_list()
        elif choice == "4":
            connection.close()
            break
        else:
            print("Неизвестный выбор!")


if __name__ == "__main__":
    main()
