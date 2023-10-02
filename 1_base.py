import math

def distance_between_points():
    x1, y1 = map(float, input("Введите координаты первой точки (x1, y1): ").strip().split())
    x2, y2 = map(float, input("Введите координаты второй точки (x2, y2): ").strip().split())
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    result = f"Расстояние между точками: {distance:.5f}"

    print(result)

def create_set_and_dict():
    items = [input(f"Введите элемент {i + 1}: ") for i in range(3)]
    sample_dict = {item: len(item) for item in items}
    print(sample_dict)
    item_to_remove = input("Введите элемент для удаления: ")
    sample_dict.pop(item_to_remove, None)

    print("Ключи словаря:", list(sample_dict.keys()))

def min_max_values():
    a, b, c, d = map(int, input("Введите числа a, b, c, d: ").split())
    min_val = min(a, b, c, d)
    max_val = max(a, b, c, d)
    result = f"Минимальное: {min_val}, Максимальное: {max_val}"

    print(result)

def main():
    while True:
        print("""
        Выберите задание:
        1 - Вычисление расстояния между точками
        2 - Работа с множествами и словарями
        3 - Нахождение минимального и максимального значений
        4 - Выход
        """)

        choice = input("Введите номер задания: ")

        if choice == "1":
            distance_between_points()
        elif choice == "2":
            create_set_and_dict()
        elif choice == "3":
            min_max_values()
        elif choice == "4":
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
