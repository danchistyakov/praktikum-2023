from sqlalchemy import create_engine, Column, Integer, String, Sequence, text
from sqlalchemy.orm import sessionmaker, declarative_base
import math
import openpyxl

Base = declarative_base()


class Calculation(Base):
    __tablename__ = 'task_1'
    id = Column(Integer, Sequence('calculation_id_seq'), primary_key=True)
    type = Column(String(50))
    data = Column(String(1000))


class Menu:
    def __init__(self, session):
        self.session = session

    def distance_between_points(self):
        x1, y1 = map(float, input("Введите координаты первой точки (x1, y1): ").strip().split())
        x2, y2 = map(float, input("Введите координаты второй точки (x2, y2): ").strip().split())

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        result = f"Расстояние между точками: {distance:.5f}"

        calculation = Calculation(type="distance", data=result)
        self.session.add(calculation)
        self.session.commit()

        print(result)

    def create_set_and_dict(self):
        items = [input(f"Введите элемент {i + 1}: ") for i in range(3)]
        sample_dict = {item: len(item) for item in items}
        print(sample_dict)
        item_to_remove = input("Введите элемент для удаления: ")
        sample_dict.pop(item_to_remove, None)

        calculation = Calculation(type="dict", data=str(list(sample_dict.keys())))
        self.session.add(calculation)
        self.session.commit()

        print("Ключи словаря:", list(sample_dict.keys()))

    def min_max_values(self):
        a, b, c, d = map(int, input("Введите числа a, b, c, d: ").split())
        min_val = min(a, b, c, d)
        max_val = max(a, b, c, d)
        result = f"Минимальное: {min_val}, Максимальное: {max_val}"

        calculation = Calculation(type="minmax", data=result)
        self.session.add(calculation)
        self.session.commit()

        print(result)

    def save_to_excel_and_show(self):
        wb = openpyxl.Workbook()
        ws = wb.active

        calculations = self.session.query(Calculation).all()
        for i, calculation in enumerate(calculations, 1):
            ws.append([calculation.type, calculation.data])

        wb.save("calculations.xlsx")

        for calculation in calculations:
            print(calculation.type, calculation.data)


def main():
    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306"
    engine_no_db = create_engine(DATABASE_URL)
    connection = engine_no_db.connect()
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS task_1"))
    connection.close()

    DATABASE_URL_DB = "mysql+pymysql://root:root@localhost:3306/task_1"
    engine_with_db = create_engine(DATABASE_URL_DB)
    Base.metadata.create_all(engine_with_db)
    Session = sessionmaker(bind=engine_with_db)
    session = Session()

    menu = Menu(session)

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


if __name__ == "__main__":
    main()
