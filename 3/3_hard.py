import mysql.connector
import openpyxl

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'task_3',
    'raise_on_warnings': False
}


def connect_to_mysql(config):
    connection = mysql.connector.connect(**config)
    print("Подключение к MySQL успешно установлено.")
    return connection


def create_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS list_dictionary (
        id INT PRIMARY KEY,
        keys_text VARCHAR(255),
        values_text VARCHAR(255)
    );
    """
    cursor.execute(create_table_query)
    print("Таблица успешно создана или уже существует.")


def input_lists():
    while True:
        raw_list1 = input('Введите элементы первого списка, разделенные пробелом: ')
        raw_list2 = input('Введите элементы второго списка, разделенные пробелом: ')
        list1 = raw_list1.split()
        list2 = raw_list2.split()

        if len(list1) == len(list2):
            return list1, list2
        else:
            print("Списки разной длины. Попробуйте снова.")


def save_to_mysql(cursor, list1, list2, list_id):
    keys_text = ','.join(list1)
    values_text = ','.join(list2)
    sql = """
    REPLACE INTO list_dictionary (id, keys_text, values_text) VALUES (%s, %s, %s);
    """
    cursor.execute(sql, (list_id, keys_text, values_text))
    print("Данные успешно сохранены в MySQL.")


def update_dictionary(cursor, list_id):
    cursor.execute("SELECT keys_text, values_text FROM list_dictionary WHERE id = %s;", (list_id,))
    record = cursor.fetchone()
    if record:
        keys = record[0].split(',')
        values = record[1].split(',')
        dictionary = dict(zip(keys, values))

        new_key = input("Введите ключ для добавления нового элемента в словарь: ")
        new_value = input("Введите значение для добавления нового элемента в словарь: ")
        dictionary[new_key] = new_value

        save_to_mysql(cursor, list(dictionary.keys()), list(dictionary.values()), list_id)

        print("Обновленный словарь:", dictionary)
        print("Длина словаря:", len(dictionary))
    else:
        print("Запись не найдена.")


def save_to_excel(cursor, filename="list_dictionary.xlsx"):
    cursor.execute("SELECT * FROM list_dictionary ORDER BY id;")
    records = cursor.fetchall()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Список 1", "Список 2", "Обновленный словарь", "Длина словаря"])

    for row in records:
        id, keys_text, values_text = row
        keys = keys_text.split(',')
        values = values_text.split(',')
        dictionary = dict(zip(keys, values))

        ws.append([
            keys_text,
            values_text,
            str(dictionary),
            len(dictionary)
        ])

    wb.save(filename)
    print(f"Данные успешно сохранены в файл {filename}.")

def main():
    connection = connect_to_mysql(config)
    if connection is None:
        return
    cursor = connection.cursor()
    create_table(cursor)

    while True:
        print("\n1. Ввод списков, сохранение и вывод из MySQL.")
        print("2. Преобразование двух списков в словарь, сохранение и вывод из MySQL.")
        print("3. Выполнение всех операций из базового варианта, сохранение результатов и вывод из MySQL.")
        print("4. Сохранение данных из MySQL в Excel и вывод на экран.")
        print("5. Выход.")
        choice = input("Выберите действие: ")

        if choice == '1':
            list1, list2 = input_lists()
            print(list1, list2)
        elif choice == '2':
            print(dict(zip(list1, list2)))
            save_to_mysql(cursor, list1, list2, 1)
        elif choice == '3':
            update_dictionary(cursor, 1)
        elif choice == '4':
            save_to_excel(cursor)
        elif choice == '5':
            print("Завершение работы.")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите корректный пункт меню.")

        connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()

