from sqlalchemy import create_engine, Column, Integer, String, Boolean, Sequence, text
# Импортируем необходимые классы и функции из библиотеки SQLAlchemy для работы с базой данных.

from sqlalchemy.orm import sessionmaker, declarative_base
# Импортируем классы `sessionmaker` и `declarative_base` для создания сессии базы данных и определения моделей.

import openpyxl
# Импортируем модуль `openpyxl`, который будет использоваться для работы с файлами Excel.

Base = declarative_base()
# Создаем объект `Base`, который будет использоваться для определения моделей базы данных.

class TupleData(Base):
    # Определяем класс `TupleData`, который будет соответствовать таблице в базе данных.
    __tablename__ = 'task_1_control'
    # Указываем имя таблицы в базе данных, к которой относится этот класс.

    id = Column(Integer, Sequence('tuple_id_seq'), primary_key=True)
    # Определяем поле `id` как целое число, автоматически генерирующееся с помощью последовательности.
    int_data = Column(Integer)
    # Определяем поле `int_data` как целое число.
    str_data = Column(String(50))
    # Определяем поле `str_data` как строку длиной до 50 символов.
    bool_data = Column(Boolean)
    # Определяем поле `bool_data` как булево значение (True/False).

class Tuples:
    # Определяем класс `Tuples`, который будет использоваться для взаимодействия с кортежами.
    def __init__(self, session):
        # Определяем конструктор класса `Tuples`, который принимает аргумент `session`, представляющий собой сессию базы данных.
        self.session = session

    def create_tuple(self):
        # Определяем метод `create_tuple`, который создает кортеж, сохраняет его в базе данных и выводит на экран.
        my_tuple = (1, "Hello", True, 2, "FinUniversity", False, 3, "Python", True, 4)
        # Создаем кортеж `my_tuple`.

        self.session.add_all([
            TupleData(int_data=my_tuple[0], str_data=my_tuple[1], bool_data=my_tuple[2]),
            TupleData(int_data=my_tuple[3], str_data=my_tuple[4], bool_data=my_tuple[5]),
            TupleData(int_data=my_tuple[6], str_data=my_tuple[7], bool_data=my_tuple[8]),
            TupleData(int_data=my_tuple[9]),
        ])
        # Добавляем объекты `TupleData` в сессию базы данных, представляя каждый элемент кортежа как объект.
        self.session.commit()
        # Сохраняем изменения в базе данных.

        print("Кортеж создан и сохранен в MySQL.")

    def get_by_index(self):
        # Определяем метод `get_by_index`, который извлекает элементы из базы данных по индексам и выводит их на экран.
        index1 = int(input("Введите первый индекс: "))
        index2 = int(input("Введите второй индекс: "))
        # Считываем индексы элементов кортежа с клавиатуры.

        items = self.session.query(TupleData).filter(TupleData.id.in_([index1 + 1, index2 + 1])).all()
        # Извлекаем элементы кортежа из базы данных по указанным индексам.

        for item in items:
            print(item.int_data, item.str_data, item.bool_data)
            # Выводим извлеченные элементы на экран.

    def slice_by_index(self):
        # Определяем метод `slice_by_index`, который извлекает срез элементов кортежа из базы данных и выводит их на экран.
        items = self.session.query(TupleData).filter(TupleData.id <= 3).all()
        # Извлекаем элементы кортежа из базы данных с индексами до 3.

        for item in items:
            print(item.int_data, item.str_data, item.bool_data)
            # Выводим извлеченные элементы на экран.

    def print_all(self):
        # Определяем метод `print_all`, который выводит все элементы кортежа из базы данных на экран.
        items = self.session.query(TupleData).all()
        # Извлекаем все элементы кортежа из базы данных.

        for item in items:
            print(item.int_data, item.str_data, item.bool_data)
            # Выводим извлеченные элементы на экран.

    def save_to_excel(self):
        # Определяем метод `save_to_excel`, который сохраняет данные из базы данных в файл Excel и выводит их на экран.
        items = self.session.query(TupleData).all()
        # Извлекаем все элементы кортежа из базы данных.

        wb = openpyxl.Workbook()
        ws = wb.active
        # Создаем новый файл Excel и активный лист.

        for item in items:
            ws.append([item.int_data, item.str_data, item.bool_data])
            # Добавляем каждый элемент кортежа в Excel-лист как список.

        wb.save("data.xlsx")
        # Сохраняем файл Excel под названием "data.xlsx".

        for item in items:
            print(item.int_data, item.str_data, item.bool_data)
            # Выводим элементы кортежа на экран.

        print("Данные сохранены в Excel.")

def main():
    # Главная функция программы.

    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306"
    # Указываем URL базы данных MySQL.

    engine_no_db = create_engine(DATABASE_URL)
    # Создаем движок базы данных, но пока не подключаемся к ней.

    connection = engine_no_db.connect()
    # Устанавливаем соединение с MySQL.

    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS task_1_control"))
    # Создаем базу данных "task_1_control", если она не существует.

    connection.close()
    # Закрываем соединение с MySQL.

    DATABASE_URL_DB = "mysql+pymysql://root:root@localhost:3306/task_1_control"
    # Указываем URL базы данных MySQL с именем базы данных.

    engine_with_db = create_engine(DATABASE_URL_DB)
    # Создаем движок базы данных с указанием имени базы данных.

    Base.metadata.create_all(engine_with_db)
    # Создаем таблицы базы данных, определенные в моделях SQLAlchemy.

    Session = sessionmaker(bind=engine_with_db)
    # Создаем сессию базы данных для взаимодействия с ней, связывая ее с двигателем `engine_with_db`.

    session = Session()
    # Создаем объект сессии для выполнения операций с базой данных.

    tuples = Tuples(session)
    # Создаем объект класса `Tuples` и передаем ему сессию базы данных.

    while True:
        # Запускаем бесконечный цикл для работы с меню выбора действий.
        print("""
        1. Создание кортежа, сохранение и вывод из MySQL.
        2. Извлечь элементы по индексам, сохранение и вывод из MySQL.
        3. Взятие среза по индексам, сохранение и вывод из MySQL.
        4. Вывод всех элементов кортежа из MySQL.
        5. Сохранить данные из MySQL в Excel и вывести на экран.
        6. Выход.
        """)

        choice = input("Выберите действие: ")
        # Запрашиваем у пользователя выбор действия.

        if choice == "1":
            tuples.create_tuple()
            # Вызываем метод для создания кортежа и сохранения его в базе данных.
        elif choice == "2":
            tuples.get_by_index()
            # Вызываем метод для извлечения элементов по индексам из базы данных.
        elif choice == "3":
            tuples.slice_by_index()
            # Вызываем метод для извлечения среза элементов по индексам из базы данных.
        elif choice == "4":
            tuples.print_all()
            # Вызываем метод для вывода всех элементов кортежа из базы данных.
        elif choice == "5":
            tuples.save_to_excel()
            # Вызываем метод для сохранения данных в Excel и вывода на экран.
        elif choice == "6":
            break
            # Выходим из цикла при выборе опции "выход".
        else:
            print("Неизвестный выбор!")
            # Выводим сообщение об ошибке при некорректном выборе действия.

if __name__ == "__main__":
    main()
    # Запускаем главную функцию программы, если скрипт запущен напрямую.

