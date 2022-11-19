import random
from chromosome import Chromosome


class Population:
    def __init__(self, quantity: int, items: list):
        self.quantity = quantity
        self.max_value = 0
        self.items = items
        self.population = self.create_population()

    def create_population(self):
        """Creates population sorted from most to least valuable"""
        population = []
        for i in range(self.quantity):
            body = [0 for _ in range(self.quantity)]
            body[i] = self.items[i]
            population.append(body)
        return population

    def choice(self):
        """Returns two lists (parent) for 'crossing': best of the population and a random one"""
        return self.population[0], random.choice(self.population)

    def crossing(self, parents: tuple):
        """Receives as parameter tuple of two lists of the same length, returns their 'child'"""
        l1, l2 = parents
        x = len(self.population)
        return l1[:int(x/4)] + l2[int(x/4):int(x/2)] + l1[int(x/2):int(3*x/4)] + l2[int(3*x/4):]

    def insert(self, chromosome: Chromosome):
        """Receives as parameter a Chromosome object. Inserts new chromosome into the population and deletes the
        worst from it """
        for i, item in enumerate(self.population):
            if Chromosome(item).value < chromosome.value:
                self.population.insert(i, chromosome.chromosome)
                self.delete_worst()
                return

    def delete_worst(self):
        """Deletes last chromosome from the population"""
        self.population.pop(-1)

    def pprint(self):
        """Prints the whole population"""
        for body in self.population:
            print(body)
