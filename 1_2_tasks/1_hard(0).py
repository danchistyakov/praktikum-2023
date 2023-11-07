from sqlalchemy import create_engine, Column, Integer, String, Sequence, text
# Импортируем необходимые классы и функции из библиотеки SQLAlchemy для работы с базой данных.

from sqlalchemy.orm import sessionmaker, declarative_base
# Импортируем классы `sessionmaker` и `declarative_base` для создания сессии базы данных и определения моделей.

import math
# Импортируем модуль `math` для выполнения математических операций, таких как вычисление квадратного корня.

import openpyxl
# Импортируем модуль `openpyxl`, который будет использоваться для работы с файлами Excel.

Base = declarative_base()
# Создаем объект `Base`, который будет использоваться для определения моделей базы данных.

class Calculation(Base):
    # Определяем класс `Calculation`, который будет соответствовать таблице в базе данных.
    __tablename__ = 'task_1'
    # Указываем имя таблицы в базе данных, к которой относится этот класс.

    id = Column(Integer, Sequence('calculation_id_seq'), primary_key=True)
    # Определяем поле `id` как целое число, автоматически генерирующееся с помощью последовательности.
    type = Column(String(50))
    # Определяем поле `type` как строку длиной до 50 символов.
    data = Column(String(1000))
    # Определяем поле `data` как строку длиной до 1000 символов.

class Menu:
    # Определяем класс `Menu`, который будет использоваться для взаимодействия с пользователем.
    def __init__(self, session):
        # Определяем конструктор класса `Menu`, который принимает аргумент `session`, представляющий собой сессию базы данных.
        self.session = session

    def distance_between_points(self):
        # Определяем метод `distance_between_points`, который будет вычислять расстояние между точками.
        x1, y1 = map(float, input("Введите координаты первой точки (x1, y1): ").strip().split())
        # Считываем координаты первой точки (x1, y1) с клавиатуры и преобразуем их в числа с плавающей запятой.
        x2, y2 = map(float, input("Введите координаты второй точки (x2, y2): ").strip().split())
        # Считываем координаты второй точки (x2, y2) с клавиатуры и преобразуем их в числа с плавающей запятой.

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # Вычисляем расстояние между двумя точками, используя формулу расстояния в декартовой системе координат.
        result = f"Расстояние между точками: {distance:.5f}"
        # Создаем строку `result`, содержащую результат вычисления расстояния с округлением до 5 знаков после запятой.

        calculation = Calculation(type="distance", data=f"{distance:.5f}")
        # Создаем объект `calculation` класса `Calculation` для записи в базу данных. Указываем тип вычисления и данные (расстояние).

        self.session.add(calculation)
        # Добавляем объект `calculation` в сессию базы данных.
        self.session.commit()
        # Сохраняем изменения в базе данных.

        print(result)
        # Выводим результат расчета на экран.

    def create_set_and_dict(self):
        # Определяем метод `create_set_and_dict`, который создает множество и словарь.
        items = [input(f"Введите элемент {i + 1}: ") for i in range(3)]
        # Создаем список `items`, в котором пользователь вводит три элемента.

        sample_dict = {item: len(item) for item in items}
        # Создаем словарь `sample_dict`, в котором ключами являются элементы, а значениями - их длины.

        item_to_remove = input("Введите элемент для удаления: ")
        # Запрашиваем пользователя на ввод элемента для удаления из словаря.

        sample_dict.pop(item_to_remove, None)
        # Удаляем элемент из словаря, если он существует.

        self.session.add_all([
            Calculation(type="set", data=str(set(sample_dict.keys()))),
            Calculation(type="dict", data=str(sample_dict)),
        ])
        # Добавляем объекты `Calculation` в сессию базы данных для записи данных множества и словаря.
        self.session.commit()
        # Сохраняем изменения в базе данных.

        print("Ключи словаря:", list(sample_dict.keys()))
        # Выводим ключи словаря на экран.

    def min_max_values(self):
        # Определяем метод `min_max_values`, который находит минимальное и максимальное значения.
        a, b, c, d = map(int, input("Введите числа a, b, c, d: ").split())
        # Считываем четыре числа с клавиатуры, разделенные пробелами, и преобразуем их в целые числа.

        min_val = min(a, b, c, d)
        # Находим минимальное значение среди введенных чисел.
        max_val = max(a, b, c, d)
        # Находим максимальное значение среди введенных чисел.

        result = f"Минимальное: {min_val}, Максимальное: {max_val}"
        # Создаем строку `result` с результатами вычислений.

        calculation = Calculation(type="minmax", data=result)
        # Создаем объект `calculation` класса `Calculation` для записи в базу данных. Указываем тип вычисления и данные (результат).

        self.session.add(calculation)
        # Добавляем объект `calculation` в сессию базы данных.
        self.session.commit()
        # Сохраняем изменения в базе данных.

        print(result)
        # Выводим результат на экран.

    def save_to_excel_and_show(self):
        # Определяем метод `save_to_excel_and_show`, который сохраняет данные в Excel и выводит на экран.
        wb = openpyxl.Workbook()
        ws = wb.active
        # Создаем новый файл Excel и активный лист.

        data = self.session.query(Calculation).all()
        # Извлекаем все записи из базы данных в таблице `Calculation`.

        for i, item in enumerate(data, 1):
            ws.append([item.type, item.data])
            # Добавляем каждую запись в Excel-лист как список с типом и данными.

        wb.save("calculations.xlsx")
        # Сохраняем файл Excel под названием "calculations.xlsx".

        for item in data:
            print(item.type, item.data)
            # Выводим тип и данные записей на экран.

def main():
    # Главная функция программы.
    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306"
    # Указываем URL базы данных MySQL.

    engine_no_db = create_engine(DATABASE_URL)
    connection = engine_no_db.connect()
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS task_1"))
    connection.close()
    # Создаем движок базы данных, подключаемся к MySQL и создаем базу данных, если она не существует.

    DATABASE_URL_DB = "mysql+pymysql://root:root@localhost:3306/task_1"
    # Указываем URL базы данных MySQL с именем базы данных.
    engine_with_db = create_engine(DATABASE_URL_DB)

    Base.metadata.create_all(engine_with_db)
    # Создаем таблицы базы данных, определенные в моделях SQLAlchemy.

    Session = sessionmaker(bind=engine_with_db)
    session = Session()
    # Создаем сессию базы данных для взаимодействия с ней.

    menu = Menu(session)

    while True:
        # Запускаем бесконечный цикл для работы с меню выбора действий.
        print("""
        1 - вычислить расстояние между точками
        2 - создать множество и словарь
        3 - найти минимальное и максимальное значение
        4 - сохранить данные из MySQL в Excel и вывести на экран
        5 - выход
        """)

        choice = input("Выберите действие: ")
        # Запрашиваем у пользователя выбор действия.

        if choice == "1":
            menu.distance_between_points()
            # Вызываем метод для вычисления расстояния между точками.
        elif choice == "2":
            menu.create_set_and_dict()
            # Вызываем метод для создания множества и словаря.
        elif choice == "3":
            menu.min_max_values()
            # Вызываем метод для нахождения минимального и максимального значения.
        elif choice == "4":
            menu.save_to_excel_and_show()
            # Вызываем метод для сохранения данных в Excel и вывода на экран.
        elif choice == "5":
            break
            # Выходим из цикла при выборе опции "выход".
        else:
            print("Неизвестный выбор!")
            # Выводим сообщение об ошибке при некорректном выборе действия.

if __name__ == "__main__":
    main()
    # Запускаем главную функцию программы, если скрипт запущен напрямую.
