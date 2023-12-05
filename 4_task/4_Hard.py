# Импорт необходимых библиотек
import pandas as pd  # Импортируем библиотеку pandas для работы с данными в формате таблицы (DataFrame)
import mysql.connector  # Импортируем библиотеку mysql.connector для работы с базой данных MySQL

# Список для хранения среднемесячного количества осадков
precipitation = []

# Функция для ввода данных с клавиатуры и сохранения в MySQL
def input_data_to_mysql():
    # Ввод данных с клавиатуры
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    for month in months:
        value = float(input(f"Введите среднемесячное количество осадков для месяца {month}: "))  # Запрашиваем у пользователя ввод данных и преобразуем в число
        precipitation.append(value)  # Добавляем введенное значение в список precipitation

    # Подключение к MySQL
    conn = mysql.connector.connect(
        host="localhost",  # Адрес хоста базы данных MySQL
        user="root",  # Имя пользователя для доступа к базе данных
        password="root",  # Пароль для доступа к базе данных
        database="weather_data"  # Имя базы данных, в которую будут сохранены данные
    )
    cursor = conn.cursor()  # Создаем курсор для выполнения SQL-запросов

    # Создание таблицы, если она не существует
    cursor.execute("CREATE TABLE IF NOT EXISTS weather (month VARCHAR(255), precipitation FLOAT)")

    # Вставка данных в MySQL
    for month, value in zip(months, precipitation):
        cursor.execute("INSERT INTO weather (month, precipitation) VALUES (%s, %s)", (month, value))  # Вставляем данные в таблицу

    conn.commit()  # Фиксируем изменения
    conn.close()  # Закрываем соединение с базой данных

# Функция для выполнения операций из базового варианта
def process_data():
    # Списки с месяцами
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    # Вывод таблицы
    print("{:<15} {:<15} {:<15}".format("Номер месяца", "Среднемесячные", "Отклонение"))
    print("{:<15} {:<15} {:<15}".format("", "осадки", "от среднегодового"))

    annual_avg = sum(precipitation) / len(precipitation)  # Рассчитываем среднегодовое количество осадков

    for i in range(len(months)):
        deviation = precipitation[i] - annual_avg  # Рассчитываем отклонение от среднегодового
        print("{:<15} {:<15.1f} {:<15.1f}".format(i + 1, precipitation[i], deviation))

    # Сохранение результатов в MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="weather_data"
    )
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS weather_results (month VARCHAR(255), precipitation FLOAT, deviation FLOAT)")

    for month, value, deviation in zip(months, precipitation, [p - annual_avg for p in precipitation]):
        cursor.execute("INSERT INTO weather_results (month, precipitation, deviation) VALUES (%s, %s, %s)", (month, value, deviation))

    conn.commit()
    conn.close()

# Функция для сохранения данных из MySQL в Excel и вывода на экран
def save_to_excel_and_display():
    # Подключение к MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="weather_data"
    )
    cursor = conn.cursor()

    # Извлечение данных из MySQL
    cursor.execute("SELECT * FROM weather_results")
    data = cursor.fetchall()

    # Создание DataFrame из данных
    df = pd.DataFrame(data, columns=["Месяц", "Среднемесячные осадки", "Отклонение от среднегодового"])

    # Сохранение данных в Excel
    df.to_excel("weather_data.xlsx", index=False)

    # Вывод данных на экран
    print(df)

# Основная программа
while True:
    print("Выберите действие:")
    print("1. Ввести два списка с клавиатуры, сохранить и вывести из MySQL.")
    print("2. Выполнение всех операций из базового варианта, сохранение результатов и вывод из MySQL.")
    print("3. Сохранить данные из MySQL в Excel и вывести на экран.")
    print("4. Выход")
    choice = input("Введите номер действия: ")

    if choice == "1":
        input_data_to_mysql()
    elif choice == "2":
        process_data()
    elif choice == "3":
        save_to_excel_and_display()
    elif choice == "4":
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите действие снова.")
