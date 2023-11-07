import mysql.connector
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
    print(list_as_string)
    raw_list = input('Введите список элементов для задачи 2: ')
    str_list = raw_list.split(' ')
    list_as_string = ', '.join(str_list)
    values = (2, list_as_string,)
    cursor.execute(sql, values)
    connection.commit()
    print(list_as_string)


def print_odds_before_stop(cursor, connection):
    stop = 71278
    cursor.execute("SELECT data FROM task_5_table WHERE id = 1")
    raw_list = cursor.fetchone()[0]
    num_list = [int(number) for number in raw_list.split(',')]
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
    str_value = ', '.join(map(str, filtered_list))
    values = (1, str_value)
    cursor.execute(sql, values)
    connection.commit()
    print(filtered_list)


def remove_number(cursor, connection):
    to_remove = 500
    cursor.execute("SELECT data FROM task_5_table WHERE id = 2")
    raw_list = cursor.fetchone()[0]
    num_list = [int(number) for number in raw_list.split(',')]
    filtered_list = [number for number in num_list if number != to_remove]
    sql = """
            INSERT INTO task_5_table (id, data) VALUES (%s, %s) AS new_values (id, data)
            ON DUPLICATE KEY UPDATE data = new_values.data;
            """
    str_value = ', '.join(map(str, filtered_list))
    values = (2, str_value)
    cursor.execute(sql, values)
    connection.commit()
    print(filtered_list)


def generate_unique_list(cursor, connection):
    rn = [x for x in range(1, 76)]
    random.shuffle(rn)
    filtered_list = rn[:20]
    sql = """
                INSERT INTO task_5_table (id, data) VALUES (%s, %s) AS new_values (id, data)
                ON DUPLICATE KEY UPDATE data = new_values.data;
                """
    str_value = ', '.join(map(str, filtered_list))
    values = (3, str_value)
    cursor.execute(sql, values)
    connection.commit()
    print(filtered_list)

def save_to_excel(cursor, connection):
    cursor.execute("SELECT data FROM task_5_table")
    raw_list = cursor.fetchall()
    wb = openpyxl.Workbook()
    ws = wb.active
    for item in raw_list:
        ws.append([item[0]])
        print(item[0])
    wb.save("data.xlsx")
    print("Данные сохранены в Excel.")


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
            generate_unique_list(cursor, connection)
        elif choice == "2":
            print_odds_before_stop(cursor, connection)
            remove_number(cursor, connection)
            generate_unique_list(cursor, connection)
        elif choice == "3":
            save_to_excel(cursor, connection)
        elif choice == "4":
            connection.close()
            break
        else:
            print("Неизвестный выбор!")


if __name__ == "__main__":
    main()
