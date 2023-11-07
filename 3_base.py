# Функция для ввода списка с проверкой на длину
def input_list(prompt):
    return input(prompt).split()

# Функция для создания словаря из двух списков
def create_dict(list1, list2):
    return dict(zip(list1, list2))

# Функция для добавления элемента в словарь
def add_to_dict(d, key, value):
    d[key] = value

# Функция для обновления элементов в словаре
def update_dict(d):
    return {k: v for k, v in d.items()}

# Ввод и создание списков
first_list = input_list("Введите элементы первого списка через пробел: ")
second_list = input_list("Введите элементы второго списка через пробел: ")

# Проверка длин и работа со словарем
if len(first_list) != len(second_list):
    print("Списки разной длины.")
else:
    my_dict = create_dict(first_list, second_list)
    new_key, new_value = input("Введите новый ключ: "), input("Введите новое значение: ")
    add_to_dict(my_dict, new_key, new_value)
    my_dict = update_dict(my_dict)
    print("Длина словаря:", len(my_dict))
    print("Словарь:", list(my_dict.items()))

# В данной версии используются функции для лучшей структуры кода и возможного переиспользования.
