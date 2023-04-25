import time
import numpy as np
from StatFunctions import *
from Generators import lin_congruent_meth, middle_products, std_randint

def main():
    rand_sizes = [50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, 2000000]

    print("Линейный конгруэнтный метод:")
    for i in rand_sizes:
        gen_params(lin_congruent_meth(i))

    print("Метод серединных произведений:")
    for i in rand_sizes:
        gen_params(middle_products(i))

    lin_congruent_time = []
    middle_products_time = []
    std_time = []

    rand_sizes = [1000, 2500, 5000, 7500, 10000, 25000, 50000, 75000, 100000, 250000, 500000, 750000, 1000000]
    for g in rand_sizes:
        time_start = time.time()
        lin_congruent_meth(g)
        lin_congruent_time.append(round(time.time() - time_start, 6))

        time_start = time.time()
        middle_products(g)
        middle_products_time.append(round(time.time() - time_start, 6))

        time_start = time.time()
        std_randint(g)
        std_time.append(round(time.time() - time_start, 6))

    print("Время генерации:")
    print("\tЛинейный конгруэнтный метод:", lin_congruent_time)
    print("\tМетод серединных произведений:", middle_products_time)
    print("\tСтандартный способ:", std_time)


if __name__ == "__main__":
    main()