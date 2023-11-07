
my_tuple = (1, "Hello", True, 2, "FinUniversity", False, 3, "Python", True, 4)

index1 = int(input("Введите первый индекс (от 0 до 9): "))
index2 = int(input("Введите второй индекс (от 0 до 9): "))

element1 = my_tuple[index1]
element2 = my_tuple[index2]
print(f"Элемент с индексом {index1}: {element1}")
print(f"Элемент с индексом {index2}: {element2}")

slice_elements = my_tuple[0:3]
print("Элементы в диапазоне [0:3]:", slice_elements)

print("Все элементы кортежа:", end=" ")
for item in my_tuple:
    print(item, end=" ")
print()

copied_tuple = my_tuple * 2
print("Копия кортежа, умноженная на 2:")
print(copied_tuple)
