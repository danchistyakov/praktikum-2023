import mysql.connector
import openpyxl

# Конфигурация для подключения к MySQL
config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'task_3',  # Убедитесь, что база данных с таким именем существует
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

        # Добавляем или обновляем элемент в словаре
        new_key = input("Введите ключ для добавления/обновления: ")
        new_value = input("Введите значение для добавления/обновления: ")
        dictionary[new_key] = new_value

        # Сохраняем обновленный словарь обратно в MySQL
        save_to_mysql(cursor, list(dictionary.keys()), list(dictionary.values()), list_id)

        # Вывод обновленного словаря, его длины, ключей и значений
        print("Обновленный словарь:", dictionary)
        print("Длина словаря:", len(dictionary))
    else:
        print("Запись не найдена.")


def save_to_excel(cursor, filename="list_dictionary.xlsx"):
    cursor.execute("SELECT * FROM list_dictionary ORDER BY id;")
    records = cursor.fetchall()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["№", "Словарь", "Длина"])  # Заголовки столбцов

    for row in records:
        id, keys_text, values_text = row
        keys = keys_text.split(',')
        values = values_text.split(',')
        dictionary = dict(zip(keys, values))  # Преобразование в словарь
        ws.append([id, str(dictionary), len(dictionary)])  # Вывод словаря и его длины

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
        print("2. Преобразовать два списка в словарь, сохранение и вывод из MySQL.")
        print("3. Вывести обновленный словарь и его длину в консоль.")
        print("4. Сохранить данные из MySQL в Excel и вывести на экран.")
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
