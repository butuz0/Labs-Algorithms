from population import Population
from chromosome import Chromosome


class GeneticSolution:
    def __init__(self, max_capacity: int, iterations: int, quantity: int, items: list, mutation_chance: int):
        self.max_capacity = max_capacity
        self.iterations = iterations
        self.mutation_chance = mutation_chance
        self.items = items
        self.population = Population(quantity, self.items)

    def solution(self):
        """Finds solution of backpack problem using genetic algorithm. Returns the best solution."""
        for i in range(self.iterations):
            parents = self.population.choice()
            child = Chromosome(self.population.crossing(parents), self.max_capacity)
            if child.weight > self.max_capacity:
                continue
            child.mutation(self.mutation_chance, self.items)
            child.local_buff(self.items)
            if child.weight > self.max_capacity:
                continue
            self.population.insert(child)

        # for chromosome in self.population.population:
        #     print("backpack: ", Chromosome(chromosome).find_values())

        print(f"best solution is: \n{self.population.population[0]}\nsummary value, weight of solution: "
              f"\n{Chromosome(self.population.population[0]).find_values()}")
        return self.population.population[0]
