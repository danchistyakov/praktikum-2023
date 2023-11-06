def input_precipitation_data():
    months = []
    precipitation = []
    for i in range(12):
        month = input(f"Введите среднемесячное количество осадков в месяце {i + 1}: ")
        try:
            precip = float(month)
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число.")
            return None, None
        months.append(i + 1)
        precipitation.append(precip)
    return months, precipitation

def print_precipitation_table(months, precipitation):
    if len(months) != len(precipitation):
        print("Списки должны быть одинаковой длины.")
        return
    # Вычисление среднегодового количества осадков
    annual = sum(precipitation) / len(precipitation)
    # Вывод заголовка таблицы
    print(f"{'Месяц':<10} {'Осадки(мм)':<12} {'Отклонение (мм)':<20}")
    print("="*45)
    # Вывод информации о каждом месяце
    for i in range(len(months)):
        precip = precipitation[i]
        deviation = precip - annual
        print(f"{months[i]:2d}. {months[i]:<10} {precip:<10.1f} {deviation:5.1f}")

# Получаем данные от пользователя
months, precipitation = input_precipitation_data()
if months is not None and precipitation is not None:
    # Вызываем функцию для вывода таблицы
    print_precipitation_table(months, precipitation)

