import random


class BeeColony:
    def __init__(self, graph: dict, scouts_amount: int, onlookers_amount: int, iterations: int):
        self.graph = graph
        self.not_visited = set(self.graph.keys())
        self.not_checked = set(self.graph.keys())
        self.scouts_amount = scouts_amount
        self.scouts = [None for _ in range(self.scouts_amount)]
        self.onlookers_amount = onlookers_amount
        self.iterations = iterations
        self.cliques = []

    # clique problem solution based on artificial bee colony algorithm. returns list of biggest cliques found
    def abc_algorithm(self) -> list:
        max_cliques = []
        for i in range(self.iterations):
            while self.not_checked:
                self.scouts = [None for _ in range(self.scouts_amount)]
                self._send_scouts()
                for scout in self.scouts:
                    vertex = self._choose_by_nectar(self._fitness())
                    self._send_onlookers(vertex)
            max_cliques.append(sorted(self.cliques, key=lambda clique: len(clique), reverse=True)[0])
            self._refresh()
        return max_cliques

    # send scouts on random vertices of graph
    def _send_scouts(self):
        for i, scout in enumerate(self.scouts):
            if self.not_visited:
                vertex = random.choice(list(self.not_visited))
                self.scouts[i] = vertex
            else:
                break

    # send onlookers on chosen vertex and calculate clique for this vertex
    def _send_onlookers(self, vertex: int):
        clique = self._find_clique(vertex)
        if clique not in self.cliques and len(clique) > 2:
            self.cliques.append(clique)

    # share amount of connections of each vertex, return probability list of chosen vertices,
    # the more connections vertex has - the bigger probability to be chosen by onlookers it has
    def _fitness(self) -> list:
        nectar_list = []
        for scout in self.scouts:
            neighbors_amount = len(self.graph[scout])
            nectar_list += [scout for _ in range(neighbors_amount)]
        return nectar_list

    def _choose_by_nectar(self, nectar_list: list) -> int:
        vertex = random.choice(nectar_list)
        i = self.scouts.index(vertex)
        self.scouts.pop(i)
        return vertex

    # send an onlooker to each neighbor of the vertex, check if it is connected with
    # the rest elements of clique, if so - add it to clique
    def _find_clique(self, vertex: int) -> list:
        available_bees = self.onlookers_amount

        if vertex in self.not_checked:
            self.not_checked.remove(vertex)
            self.not_visited.remove(vertex)

        clique = [vertex]
        for neighbor in self.graph[vertex]:
            if available_bees <= 0:
                break

            available_bees -= 1

            if neighbor in self.not_checked:
                self.not_checked.remove(neighbor)

            in_clique = True
            for clique_vertex in clique:
                if neighbor not in self.graph[clique_vertex]:
                    in_clique = False
                    break

            if in_clique:
                clique.append(neighbor)
        return clique

    # return to starting parameters
    def _refresh(self):
        self.not_visited = set(self.graph.keys())
        self.not_checked = set(self.graph.keys())
        self.scouts = [None for _ in range(self.scouts_amount)]
        self.cliques = []
