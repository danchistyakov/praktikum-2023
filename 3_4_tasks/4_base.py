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
        month = months[i]
        precip = precipitation[i]
        deviation = precip - annual
        print(f"{i+1:2d}. {month:<10} {precip:<10} {deviation:5.1f}")

# Список месяцев и среднемесячного количества осадков
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
precipitation = [41.3, 38.1, 43.2, 50.4, 85.7, 71.0, 78.4, 47.7, 54.2, 46.6, 41.9, 45.9]

# Вызываем функцию для вывода таблицы
print_precipitation_table(months, precipitation)
