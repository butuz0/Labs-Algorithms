import copy
from random import randint, choice


class Chromosome:
    def __init__(self, chromosome: list, max_weight=None):
        self.chromosome = chromosome
        self.max_weight = max_weight
        self.length = len(self.chromosome)
        self.value, self.weight = self.find_values()

    def find_values(self):
        """Returns a tuple of total value and weight of genes in chromosome"""
        value = 0
        weight = 0
        for gene in self.chromosome:
            if gene:
                value += gene[0]
                weight += gene[1]
        return value, weight

    def mutation(self, mutation_chance: int, items: list):
        """Receives as parameters chance of mutation and list of all items. With a particular chance 'reverses' two
        genes: if gene is 0, it is replaced with a random unique-in-list item; if gene is an item, it is replaced
        with 0 """
        if randint(1, 100) > mutation_chance:
            return
        indexes = [randint(0, self.length-1) for _ in range(2)]
        chromosome_copy = copy.copy(self.chromosome)

        for index in indexes:
            if chromosome_copy[index] == 0:
                # item = choice(items)
                # while item in chromosome_copy:
                #     item = choice(items)
                chromosome_copy[index] = items[index]
            else:
                chromosome_copy[index] = 0

        if Chromosome(chromosome_copy).weight > self.max_weight:
            return

        self.chromosome = chromosome_copy
        self.value, self.weight = self.find_values()

    def local_buff(self, items: list):
        """Receives as a parameter list of all items. Changes random gene in chromosome which equals 0 to a random
        unique-in-list item """
        index = randint(0, self.length-1)
        while self.chromosome[index] != 0:
            index = randint(0, self.length-1)
        # item = choice(items)
        # while item in self.chromosome:
        #     item = choice(items)
        self.chromosome[index] = items[index]
        self.value, self.weight = self.find_values()

    def pprint(self):
        """Prints the chromosome"""
        print(self.chromosome)
