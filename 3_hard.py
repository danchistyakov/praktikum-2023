from sqlalchemy import create_engine, Column, Integer, String, Sequence, text
from sqlalchemy.orm import sessionmaker, declarative_base
import ast
import openpyxl
import pandas as pd


Base = declarative_base()

class ListToDict(Base):
    __tablename__ = 'task_3'
    id = Column(Integer, Sequence('list_dict_id_seq'), primary_key=True)
    list_one = Column(String(255))
    list_two = Column(String(255))
    dictionary = Column(String(255))

class List:
    def __init__(self, session):
        self.session = session

    def input_and_save_lists(self):
        print("Введите элементы первого списка, разделенные пробелом:")
        list_one = input().split()
        print("Введите элементы второго списка, разделенные пробелом:")
        list_two = input().split()

        if len(list_one) != len(list_two):
            print("Списки разной длины, попробуйте еще раз.")
            return

        new_entry = ListToDict(list_one=str(list_one), list_two=str(list_two))
        self.session.add(new_entry)
        self.session.commit()
        print("Списки сохранены.")

    def lists_to_dict_and_save(self):
        last_entry = self.session.query(ListToDict).order_by(ListToDict.id.desc()).first()
        if not last_entry:
            print("Сначала введите списки.")
            return

        list_one = ast.literal_eval(last_entry.list_one)
        list_two = ast.literal_eval(last_entry.list_two)
        dictionary = dict(zip(list_one, list_two))

        last_entry.dictionary = str(dictionary)
        self.session.commit()
        print("Словарь создан и сохранен.")


    def manage_dict_operations(self):
            # Получение последней записи из базы данных
        last_entry = self.session.query(ListToDict).order_by(ListToDict.id.desc()).first()

        if not last_entry:
            print("Сначала введите списки.")
        else:
                # Ввод новых элементов для словаря
            print("Введите новый ключ для словаря:")
            new_key = input()
            print("Введите новое значение для словаря:")
            new_value = input()

                # Обновление словаря с проверкой существует ли он уже в базе данных
            current_dict = ast.literal_eval(last_entry.dictionary) if last_entry.dictionary else {}
            current_dict[new_key] = new_value  # Добавляем новый элемент в словарь
            last_entry.dictionary = str(current_dict)  # Сохраняем обновленный словарь в строковом формате
            self.session.commit()  # Фиксируем изменения в базе данных
            print("Элемент добавлен в словарь, и словарь обновлен в базе данных.")

                # Обновление всех словарей на основе текущих списков
            all_entries = self.session.query(ListToDict).all()
        for entry in all_entries:
            list_one = ast.literal_eval(entry.list_one) if entry.list_one else []
            list_two = ast.literal_eval(entry.list_two) if entry.list_two else []
            entry.dictionary = str(dict(zip(list_one, list_two)))
        self.session.commit()
        print("Все словари обновлены на основе текущих списков.")

                # Печать длины последнего словаря
        if current_dict:  # Текущий словарь уже загружен выше
            print("Длина словаря:", len(current_dict))

                # Печать ключей и значений последнего словаря
        keys_values_list = list(current_dict.items())
        print("Ключи и значения словаря:", keys_values_list)

    def export_updated_dict_to_excel(self):
        records = self.session.query(ListToDict).all()
        data = {'ID': [], 'List One': [], 'List Two': [], 'Dictionary': []}

        for record in records:
            data['ID'].append(record.id)
            data['List One'].append(record.list_one)
            data['List Two'].append(record.list_two)
            data['Dictionary'].append(record.dictionary)

        df = pd.DataFrame(data)
        df.to_excel('updated_data.xlsx', index=False)
        print("Файл 'updated_data.xlsx' успешно сохранен.")


def main():
    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306"
    engine_no_db = create_engine(DATABASE_URL)
    connection = engine_no_db.connect()
    connection.execute(text("CREATE DATABASE IF NOT EXISTS task_3"))
    connection.close()

    DATABASE_URL_DB = "mysql+pymysql://root:root@localhost:3306/task_3"
    engine_with_db = create_engine(DATABASE_URL_DB)
    Base.metadata.create_all(engine_with_db)
    Session = sessionmaker(bind=engine_with_db)
    session = Session()

    list_manager = List(session)  # Переименовано для соответствия классу List

    while True:
        print("""
        1. Ввод списков, сохранение и вывод из MySQL.
        2. Преобразование два списка в словарь, сохранение и вывод из MySQL.
        3. Добавление элемента в словарь и обновление всех текущих элементов, вывод длины словаря,вывод всех ключей и значений словаря в виде списка.
        4. Сохранение данныx из MySQL в Excel и вывод на экран.
        5. Выход.
        """)
        choice = input("Выберите действие: ")
        if choice == "1":
            list_manager.input_and_save_lists()
        elif choice == "2":
            list_manager.lists_to_dict_and_save()
        elif choice == "3":
            list_manager.manage_dict_operations()
        elif choice == "4":
            list_manager.export_updated_dict_to_excel()
        elif choice == "5":
            break
        else:
            print("Неизвестный выбор!")

    session.close()  # Закрытие сессии после завершения

if __name__ == "__main__":
    main()
