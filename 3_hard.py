from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import openpyxl

Base = declarative_base()

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)

class AdvancedDictionaryManager:
    def __init__(self, session):
        self.session = session

    def task_1(self):
        keys = input("Введите ключи словаря через пробел: ").split()
        values = input("Введите значения словаря через пробел: ").split()

        if len(keys) != len(values):
            print("Списки разной длины. Пожалуйста, введите списки одинаковой длины.")
        else:
            dictionary = dict(zip(keys, values))

            new_key = input("Введите ключ нового элемента: ")
            new_value = input("Введите значение нового элемента: ")
            dictionary[new_key] = new_value

            for key in dictionary:
                dictionary[key] = dictionary[key] + "_updated"

            print(f"Длина словаря: {len(dictionary)}")

            print("Ключи:", list(dictionary.keys()))
            print("Значения:", list(dictionary.values()))

    def load_from_db(self):
        data = self.session.query(Data).all()
        self.dictionary = {item.key: item.value for item in data}
        self.session.close()

    def save_to_excel(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        for key, value in self.dictionary.items():
            ws.append([key, value])
        wb.save("task_3.xlsx")

    def interactive_menu(self):
        while True:
            print("""
            1. Ввод списков, сохранение и вывод из MySQL.
            2. Преобразовать два списка в словарь, сохранение и вывод из MySQL.
            3. Выполнение всех операций из базового варианта, сохранение результатов и вывод из MySQL.
            4. Сохранить данные из MySQL в Excel и вывести на экран.
            5. Выход.
            """)
            choice = input("Выберите действие: ")
            if choice == "1":
                list1, list2 = self.input_lists()
                self.lists_to_dict(list1, list2)
                self.save_to_db()
                self.display()
            elif choice == "2":
                self.load_from_db()
                self.display()
            elif choice == "3":
                self.load_from_db()
                self.add_element_to_dict()
                self.update_dict()
                self.save_to_db()
                self.display()
            elif choice == "4":
                self.load_from_db()
                self.save_to_excel()
                print("Данные сохранены в data.xlsx")
            elif choice == "5":
                break

def main():
    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306"
    engine_no_db = create_engine(DATABASE_URL)
    connection = engine_no_db.connect()
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS task_3"))
    connection.close()

    DATABASE_URL_DB = "mysql+pymysql://root:root@localhost:3306/task_3"
    engine_with_db = create_engine(DATABASE_URL_DB)
    Base.metadata.create_all(engine_with_db)
    Session = sessionmaker(bind=engine_with_db)
    session = Session()

    menu = AdvancedDictionaryManager(session)

    while True:
        print("""
        1 - вычислить расстояние между точками
        2 - создать множество и словарь
        3 - найти минимальное и максимальное значение
        4 - сохранить данные из MySQL в Excel и вывести на экран
        5 - выход
        """)

        choice = input("Выберите действие: ")
        if choice == "1":
            menu.distance_between_points()
        elif choice == "2":
            menu.create_set_and_dict()
        elif choice == "3":
            menu.min_max_values()
        elif choice == "4":
            menu.save_to_excel_and_show()
        elif choice == "5":
            break
        else:
            print("Неизвестный выбор!")

manager = AdvancedDictionaryManager()
manager.interactive_menu()
