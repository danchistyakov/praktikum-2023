from sqlalchemy import create_engine, Column, Integer, String, Sequence, text
from sqlalchemy.orm import sessionmaker, declarative_base
import ast
import openpyxl

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

    def add_to_dict_and_update(self):
        # Получение последней записи из базы данных
        last_entry = self.session.query(ListToDict).order_by(ListToDict.id.desc()).first()
        if not last_entry:
            print("Сначала введите списки.")
            return

        # Предложение ввести новые данные для словаря
        print("Введите новый ключ для словаря:")
        new_key = input()
        print("Введите новое значение для словаря:")
        new_value = input()

        # Обновление словаря с проверкой существует ли он уже в базе данных
        if last_entry.dictionary:  # Если словарь существует, загружаем и обновляем его
            current_dict = ast.literal_eval(last_entry.dictionary)
        else:  # Если словаря нет, инициализируем новый
            current_dict = {}

        current_dict[new_key] = new_value  # Добавляем новый элемент в словарь
        last_entry.dictionary = str(current_dict)  # Сохраняем обновленный словарь в строковом формате
        self.session.commit()  # Фиксируем изменения в базе данных
        print("Элемент добавлен в словарь, и словарь обновлен в базе данных.")

    def update_dictionary(self):
        # Select all list pairs and update dictionaries
        all_entries = self.session.query(ListToDict).all()
        for entry in all_entries:
            list_one = ast.literal_eval(entry.list_one)
            list_two = ast.literal_eval(entry.list_two)
            entry.dictionary = str(dict(zip(list_one, list_two)))

        self.session.commit()
        print("Все словари обновлены на основе текущих списков.")

    def get_last_dictionary(self):
        last_entry = self.session.query(ListToDict).order_by(ListToDict.id.desc()).first()
        if not last_entry or not last_entry.dictionary:
            print("Сначала выполните преобразование в словарь.")
            return None
        return ast.literal_eval(last_entry.dictionary)

    def print_dictionary_length(self):
        dictionary = self.get_last_dictionary()
        if dictionary is not None:
            print("Длина словаря:", len(dictionary))

    def print_dictionary_keys_values(self):
        dictionary = self.get_last_dictionary()
        if dictionary is not None:
            keys_values_list = list(dictionary.items())
            print("Ключи и значения словаря:", keys_values_list)

    import openpyxl  # Убедитесь, что openpyxl установлен

    def save_to_excel(self):
        items = self.session.query(ListToDict).all()  # Получаем все записи из таблицы
        wb = openpyxl.Workbook()  # Создаем новую книгу Excel
        ws = wb.active  # Получаем активный лист в книге

        # Добавляем заголовки столбцов в первую строку
        ws.append(['ID', 'List One', 'List Two', 'Dictionary'])

        # Проходимся по всем записям и добавляем данные в лист Excel
        for item in items:
            # Парсим строки обратно в объекты Python перед добавлением
            list_one = ast.literal_eval(item.list_one) if item.list_one else []
            list_two = ast.literal_eval(item.list_two) if item.list_two else []
            dictionary = ast.literal_eval(item.dictionary) if item.dictionary else {}

            # Добавляем данные в строку
            ws.append([item.id, list_one, list_two, dictionary])

        # Сохраняем файл Excel
        wb.save("data.xlsx")
        print("Данные сохранены в Excel.")


# Определение main() без неиспользуемых методов
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
        3. Добавление элемента в словарь и обновление всех текущих элементов.
        4. Вывод длины словаря.
        5. Вывод всех ключей и значений словаря в виде списка.
        6. Сохранение данныч из MySQL в Excel и вывод на экран.
        7. Выход.
        """)
        choice = input("Выберите действие: ")
        if choice == "1":
            list_manager.input_and_save_lists()
        elif choice == "2":
            list_manager.lists_to_dict_and_save()
        elif choice == "3":
            list_manager.add_to_dict_and_update()
        elif choice == "4":
            list_manager.print_dictionary_length()
        elif choice == "5":
            list_manager.print_dictionary_keys_values()
        elif choice == "6":
            list_manager.save_to_excel()
        elif choice == "7":
            break
        else:
            print("Неизвестный выбор!")

    session.close()  # Закрытие сессии после завершения

if __name__ == "__main__":
    main()
