import random


def print_odds_before_stop():
    stop = 71278
    raw_list = input('Введите список элементов: ')
    str_list = raw_list.split(' ')
    num_list = list(map(int, str_list))
    print(num_list)
    result = []
    for item in num_list:
        if item == stop:
            break
        if item % 2 == 1:
            result.append(item)
    return result


print(print_odds_before_stop())


def remove_number():
    to_remove = 500
    raw_list = input('Введите список элементов: ')
    str_list = raw_list.split(' ')
    num_list = list(map(int, str_list))
    return [number for number in num_list if number != to_remove]


print(remove_number())


def generate_unique_list():
    rn = [x for x in range(1, 76)]
    random.shuffle(rn)
    return print(rn[:20])


print(generate_unique_list())
