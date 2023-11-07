# Импортируем необходимые библиотеки и модули
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Sequence, text
from sqlalchemy.orm import sessionmaker, declarative_base
import openpyxl

# Создаем базовый класс для определения моделей
Base = declarative_base()

# Определяем модель данных для таблицы в базе данных
class TupleData(Base):
    __tablename__ = 'task_1_control'  # Имя таблицы
    id = Column(Integer, Sequence('tuple_id_seq'), primary_key=True)  # Поле для идентификации записей
    int_data = Column(Integer)  # Поле для целых чисел
    str_data = Column(String(50))  # Поле для строк (максимум 50 символов)
    bool_data = Column(Boolean)  # Поле для булевых значений

# Создаем класс для работы с данными
class Tuples:
    def __init__(self, session):
        self.session = session

    # Метод для создания кортежа и сохранения его в базе данных
    def create_tuple(self):
        input_string = input("Введите элементы кортежа, разделенные пробелом: ")

        # Преобразуем строку в список
        input_list = input_string.split()

        # Преобразуем список в кортеж
        result_tuple = tuple(input_list)
        print("Сформированный кортеж:", result_tuple)

        # Создаем объекты модели и добавляем их в сессию
        self.session.add_all([
            TupleData(int_data=int(result_tuple[0]), str_data=result_tuple[1], bool_data=bool(result_tuple[2])),
            TupleData(int_data=int(result_tuple[3]), str_data=result_tuple[4], bool_data=bool(result_tuple[5])),
            TupleData(int_data=int(result_tuple[6]), str_data=result_tuple[7], bool_data=bool(result_tuple[8])),
            TupleData(int_data=int(result_tuple[9])),
        ])
        self.session.commit()  # Сохраняем изменения в базе данных
        print("Кортеж создан и сохранен в MySQL.")

    # Метод для извлечения элементов из базы данных по индексам
    def get_by_index(self):
        index1 = int(input("Введите первый индекс: "))
        index2 = int(input("Введите второй индекс: "))

        # Извлекаем данные из базы данных
        fields_data = self.session.query(TupleData.int_data, TupleData.str_data, TupleData.bool_data).all()
        flat_list = [item for sublist in fields_data for item in sublist]

        # Выводим срез данных в заданном диапазоне
        print(flat_list[index1:index2 + 1])

    # Метод для извлечения среза данных из базы данных по индексам
    def slice_by_index(self):
        index1 = int(input("Введите первый индекс: "))
        index2 = int(input("Введите второй индекс: "))

        # Извлекаем данные из базы данных с использованием фильтрации по диапазону индексов
        items = self.session.query(TupleData).filter(TupleData.id.between(index1 + 1, index2 + 1)).all()

        # Выводим элементы среза
        for item in items:
            print(item.int_data, item.str_data, item.bool_data)

    # Метод для вывода всех элементов из базы данных
    def print_all(self):
        items = self.session.query(TupleData).all()

        # Выводим все элементы
        for item in items:
            print(item.int_data, item.str_data, item.bool_data)

    # Метод для сохранения данных в Excel
    def save_to_excel(self):
        items = self.session.query(TupleData).all()
        wb = openpyxl.Workbook()
        ws = wb.active

        # Записываем данные в Excel
        for item in items:
            ws.append([item.int_data, item.str_data, item.bool_data])
            print(item.int_data, item.str_data, item.bool_data)

        wb.save("data.xlsx")  # Сохраняем файл Excel
        print("Данные сохранены в Excel.")

# Основная функция программы
def main():
    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306"
    engine_no_db = create_engine(DATABASE_URL)
    connection = engine_no_db.connect()
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS task_1_control"))
    connection.close()

    DATABASE_URL_DB = "mysql+pymysql://root:root@localhost:3306/task_1_control"
    engine_with_db = create_engine(DATABASE_URL_DB)
    Base.metadata.create_all(engine_with_db)
    Session = sessionmaker(bind=engine_with_db)
    session = Session()

    tuples = Tuples(session)

    while True:
        print("""
        1. Создание кортежа, сохранение и вывод из MySQL.
        2. Извлечь элементы по индексам, сохранение и вывод из MySQL.
        3. Взятие среза по индексам, сохранение и вывод из MySQL.
        4. Вывод всех элементов кортежа из MySQL.
        5. Сохранить данные из MySQL в Excel и вывести на экран.
        6. Выход.
        """)
        choice = input("Выберите действие: ")
        if choice == "1":
            tuples.create_tuple()
        elif choice == "2":
            tuples.get_by_index()
        elif choice == "3":
            tuples.slice_by_index()
        elif choice == "4":
            tuples.print_all()
        elif choice == "5":
            tuples.save_to_excel()
        elif choice == "6":
            break
        else:
            print("Неизвестный выбор!")

# Запуск основной функции при выполнении скрипта
if __name__ == "__main__":
    main()
