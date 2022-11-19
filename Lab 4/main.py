# Ukrainian
# Задача про рюкзак (місткість P=250, 100 предметів, цінність предметів
# від 2 до 30 (випадкова), вага від 1 до 25 (випадкова)), генетичний
# алгоритм (початкова популяція 100 осіб кожна по 1 різному предмету,
# оператор схрещування триточковий 25%, мутація з ймовірністю 5% два
# випадкові гени міняються місцями). Розробити власний оператор локального покращення.

# English
# Backpack problem, (capacity P=250, 100 items, value of items
# from 2 to 30 (random), weight from 1 to 25 (random)), genetic
# algorithm (initial population of 100 people each with 1 different item,
# crossing operator three-point 25%, mutation with a probability of 5% two
# random genes are swapped). Develop your own local improvement operator.

from genetic_algorithm_solution import GeneticSolution
from random import randint


if __name__ == "__main__":
    capacity = 250
    iterations = 1000
    quantity = 100
    items = [(randint(2, 30), randint(1, 25)) for _ in range(quantity)]  # list of items, item = tuple(value, weight)
    items.sort(reverse=True)  # sort items, so that chromosomes in generation were also sorted
    print(items)
    mutation_chance = 5
    solution = GeneticSolution(capacity, iterations, quantity, items, mutation_chance)
    res = solution.solution()
