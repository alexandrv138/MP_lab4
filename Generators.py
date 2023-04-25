from random import randint
import time

def lin_congruent_meth(size):
    """
    Линейный конгруэнтный метод [0, 16383]

    Входные значения:
    size(int) : количество генерируемых чисел

    Возвращаемые значения:
    Cписок псевдослучайных чисел (list)

    """
    res = []
    M = (1 << 61) - 1
    k = 1 << 61

    b = int(time.perf_counter_ns() // 100)
    if b == M:
        b -= 1
    r0 = 15

    for i in range(size):
        r0 = (k * r0 + b) % M
        res.append(r0 % 16384)
    return res

def middle_products(size):
    """
    Метод серединных произведений [0, 16383]

    :param size: количество генерируемых чисел
    :type size: int

    :return: список псевдослучайных чисел
    :rtype: list
    """
    r0 = int(time.time()) % 128 + 1
    r1 = int(time.time()) % 128 + 1
    b = 11
    res = []

    for i in range(size):
        r = (r0 * r1 * b) & 16383
        res.append(r)
        r0 = r1
        r1 = r
        r0 += 12
        r1 += 16
        b += 2
    return res


def std_randint(size):
    """
        Встроенный генератор псевдослучайных последовательностей [0, 16383]

        Входные значения:
        size(int) : количество генерируемых чисел

        Возвращаемые значения:
        Cписок псевдослучайных чисел (list)
    """
    res = []
    for i in range(size):
        res.append(randint(0, 16384))
    return res
