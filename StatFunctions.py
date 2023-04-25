import time
import numpy as np
from math import floor, log2
from Generators import lin_congruent_meth, std_randint, middle_products

significance_level = [0.99, 0.95, 0.90] # уровень значимости

xi_table = {               # таблица статистики хи-квадрат
    5: [0.55, 1.15, 1.61],
    6: [0.87, 1.64, 2.20],
    7: [1.24, 2.18, 2.83],
    8: [1.65, 2.73, 3.49],
    9: [2.09, 3.33, 4.17],
    10: [2.56, 3.94, 4.87],
    11: [3.05, 4.57, 5.58],
    12: [3.57, 5.23, 6.30],
    13: [4.11, 5.89, 7.04],
    15: [5.23, 7.26, 8.5],
    16: [5.81, 7.98, 9.31],
    17: [6.41, 8.67, 10.09],
    18: [7.02, 9.39, 10.87],
    19: [7.63, 10.1, 11.7],
    20: [8.26, 10.9, 12.4],
    21: [8.90, 11.56, 13.2],
    22: [9.54, 12.34, 14.04],
}

def sample_average(sample: list) -> float:
    """
    Вычисление выборочного среднего

    Параметры:
        sample(list): выборка

    Возвращаемое значение:
        Выборочное среднее(float)
    """
    return sum(sample) / len(sample)


def sample_variance(sample: list) -> float:
    """
    Вычисление выборочной дисперсии

    Параметры:
        sample(list): выборка

    Возвращаемое значение:
        Выборочная дисперсия(float)
    """
    m = sample_average(sample)
    summ = 0
    for i in sample:
        summ += (i - m) * (i - m)
    return summ / len(sample)



def xi_square(sample: list) -> tuple:
    """
    Используя критерий хи-квадрат, определяем случайность и равномерность распределения

    Параметры:
        sample(list): выборка

    Возвращаемые значения:
        Значение статистики, а также строковые описания  (tuple)
    """
    a = 0
    theta = 16384
    N = len(sample) # объём выборки
    k = 1 + floor(log2(N)) # количество интервалов, вычисляется по формуле Старджеса
    intervals = np.arange(a, a + theta, (theta - 1) / k) # список интервалов

    prob_intervals = [] # список вероятностей попадания в интервал
    for i in range(len(intervals) - 1):
        left = np.ceil(intervals[i])
        right = np.floor(intervals[i+1])
        if intervals[i+1] == right and right != 16383:
            right -= 1
        prob_intervals.append((right - left + 1) / theta)
    intervals[-1] += 1

    intervals_count = [0] * k # список количества элементов выборки, попадающих в интервал
    for num in sample:
        for i in range(len(intervals) - 1):
            if intervals[i] <= num < intervals[i + 1]:
                intervals_count[i] += 1

    summ = 0
    for j in range(k):
        summ += intervals_count[j] ** 2 / (N * prob_intervals[j])

    statistic = summ - N
    signif_level = xi_table[k - 1]

    if statistic < signif_level[0]: # Если уровень значимости больше 0.99, то выборка равномерна и не случайна
        return (f"Принимается: уровень значимости >= {max(significance_level)}", "Отвергается", statistic)
    elif statistic > signif_level[2]: # Если уровень значимости меньше 0.90, то выборка не равномерна и не случайна
        return ("Отвергается", "Отвергается", statistic)

    conclusion = ""
    for i in range(len(significance_level) - 1): # Если уровень значимости между 0.99 и 0.90, то выборка равномерна и случайна
        if signif_level[i] <= statistic <= signif_level[i+1]:
            conclusion = f": уровень значимости ({significance_level[i+1]}, {significance_level[i]}]"
    return ("Принимается " + conclusion, "Принимается " + conclusion, statistic)


def gen_params(sample: list):
    """
    Вычисляет параметры выборки и, используя критерий хи-квадрат, определяется
    случайность и равномерность распределения

    Параметры:
        sample(list): выборка

    """

    norm_sample = [i / 16383 for i in sample] # нормированная выборка
    mean = sample_average(norm_sample) # выборочное среднее
    dispersion = sample_variance(norm_sample) # выборочное среднее
    standart_deviation = dispersion ** (1 / 2) # отклонение
    variation_coefficient = standart_deviation / mean # коэффициент вариации
    r1, r2, val = xi_square(sample)  # критерий хи-квадрат

    print(
        f"Размер выборки: {len(sample)}",
        f"Среднее: {round(mean, 6)}",
        f"Дисперсия: {round(dispersion, 6)}",
        f"Отклонение: {round(standart_deviation, 6)}",
        f"Коэффициент вариации: {round(variation_coefficient, 6)}",
        f"Значение статистики: {round(val, 6)}",
        f"Равномерность: {r1}",
        f"Случайность: {r2}\n",
        sep="\n"
    )
