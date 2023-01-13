import random
import time
from bee_algorithm import BeeColony


def create_graph(size, min_max):
    min, max = min_max
    graph = {key: set() for key in range(size)}
    for key in graph:
        r = random.randint(min, max) - len(graph[key])
        for i in range(r):
            elem = random.randint(0, size - 1)
            if elem != key:
                graph[key].add(elem)
        for k in graph[key]:
            graph[k].add(key)
    return graph


def main():
    graph = create_graph(300, (2, 30))
    scouts = 5
    onlookers = 40
    iterations = 10
    bc = BeeColony(graph, scouts, onlookers, iterations)

    start = time.time()
    cliques = bc.abc_algorithm()
    end = time.time()

    print(f"best results of {iterations} iterations:")
    for clique in cliques:
        print(clique)
    print("time:", end - start)


if __name__ == "__main__":
    main()
