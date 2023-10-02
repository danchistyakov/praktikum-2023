from sqlalchemy import create_engine, Column, Integer, String, Boolean, Sequence, text
from sqlalchemy.orm import sessionmaker, declarative_base
import openpyxl

Base = declarative_base()


class TupleData(Base):
    __tablename__ = 'task_1_control'
    id = Column(Integer, Sequence('tuple_id_seq'), primary_key=True)
    int_data = Column(Integer)
    str_data = Column(String(50))
    bool_data = Column(Boolean)


class Tuples:
    def __init__(self, session):
        self.session = session

    def create_tuple(self):
        input_string = input("Введите элементы кортежа, разделенные пробелом: ")

        # Преобразуем строку в список
        input_list = input_string.split()

        # Преобразуем список в кортеж
        result_tuple = tuple(input_list)
        print("Сформированный кортеж:", result_tuple)
        self.session.add_all([
            TupleData(int_data=int(result_tuple[0]), str_data=result_tuple[1], bool_data=bool(result_tuple[2])),
            TupleData(int_data=int(result_tuple[3]), str_data=result_tuple[4], bool_data=bool(result_tuple[5])),
            TupleData(int_data=int(result_tuple[6]), str_data=result_tuple[7], bool_data=bool(result_tuple[8])),
            TupleData(int_data=int(result_tuple[9])),
        ])
        self.session.commit()
        print("Кортеж создан и сохранен в MySQL.")

    def get_by_index(self):
        index1 = int(input("Введите первый индекс: "))
        index2 = int(input("Введите второй индекс: "))
        fields_data = self.session.query(TupleData.int_data, TupleData.str_data, TupleData.bool_data).all()
        flat_list = [item for sublist in fields_data for item in sublist]
        print(flat_list[index1:index2 + 1])

    def slice_by_index(self):
        items = self.session.query(TupleData).filter(TupleData.id <= 3).all()
        for item in items:
            print(item.int_data, item.str_data, item.bool_data)

    def print_all(self):
        items = self.session.query(TupleData).all()
        for item in items:
            print(item.int_data, item.str_data, item.bool_data)

    def save_to_excel(self):
        items = self.session.query(TupleData).all()
        wb = openpyxl.Workbook()
        ws = wb.active
        for item in items:
            ws.append([item.int_data, item.str_data, item.bool_data])
            print(item.int_data, item.str_data, item.bool_data)
        wb.save("data.xlsx")
        print("Данные сохранены в Excel.")


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


if __name__ == "__main__":
    main()
