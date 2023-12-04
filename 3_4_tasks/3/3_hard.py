import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '3306',
    'raise_on_warnings': True
}


def input_values(cursor, connection):
    list1 = input("Введите элементы первого списка через пробел: ").split()
    list2 = input("Введите элементы второго списка через пробел: ").split()
    sql = """
        INSERT INTO task_5_table (id, list1, list2) VALUES (%s, %s, %s) AS new_values (id, list1, list2)
        ON DUPLICATE KEY UPDATE list1 = new_values.list1, list2 = new_values.list2;
        """
    values = (1, list1, list2)
    cursor.execute(sql, values)
    connection.commit()


def convert(cursor, connection):
    # Ввод списков с клавиатуры и проверка их длины
    list1 = input("Введите элементы первого списка через пробел: ").split()
    list2 = input("Введите элементы второго списка через пробел: ").split()

    if len(list1) == len(list2):
        # Преобразование списков в словарь
        dictionary = dict(zip(list1, list2))

        # Добавление элемента в словарь
        key_to_add = input("Введите ключ для добавления в словарь: ")
        value_to_add = input("Введите значение для этого ключа: ")
        dictionary[key_to_add] = value_to_add

        # Обновление всех текущих элементов
        for key in list(dictionary.keys()):  # Используйте list чтобы избежать RuntimeError
            new_value = input(f"Введите новое значение для {key}: ")
            dictionary[key] = new_value

        # Вывод длины словаря
        print("Длина словаря:", len(dictionary))

        # Вывод всех ключей и значений словаря в виде списка
        keys_values_list = [(key, value) for key, value in dictionary.items()]
        print("Ключи и значения словаря:", keys_values_list)

    else:
        print("Списки разной длины. Убедитесь, что длины списков одинаковы.")


def main():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_3")
    except:
        print("")
    cursor.execute("USE task_3")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS task_3_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        list1 VARCHAR(255)
        list2 VARCHAR(255)
        dictionary VARCHAR(255)
    );
    """
    try:
        cursor.execute(create_table_query)
    except:
        print("")

    while True:
        print("""
        1. Ввод списков, сохранение и вывод из MySQL.
        2. Преобразовать два списка в словарь, сохранение и вывод из MySQL.
        3. Выполнение всех операций из базового варианта, сохранение результатов и вывод из MySQL.
        4. Сохранить данные из MySQL в Excel и вывести на экран.
        5. Выход
        """)
        choice = input("Выберите действие: ")
        if choice == "1":
            input_values(cursor, connection)
        elif choice == "2":
            convert(cursor, connection)
        elif choice == "3":
        elif choice == "4":
            break
        else:
            print("Неизвестный выбор!")


if __name__ == "__main__":
    main()
