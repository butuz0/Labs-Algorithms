import time
from puzzle import Puzzle
from node import Node
from queue import PriorityQueue


class Solution:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.start = time.time()

    def a_star(self):
        node = Node(self.puzzle)
        queue = PriorityQueue()
        queue.put((node.f(), node))
        while not queue.empty():
            if time.time() > self.start + 30*60:
                print("solution wasn't found")
                return None

            node = queue.get()[1]

            if node.solved():
                print("SOLUTION FOUND")
                print("solution level in tree: ", node.level)
                return node.find_parents()

            for move in node.moves():
                child = Node(move, node)
                queue.put((child.f(), child))

        return None

    def dls(self):
        return self.recursive_dls(Node(self.puzzle))

    def recursive_dls(self, node: Node):
        if time.time() > self.start + 30*60:
            print("solution wasn't found")
            return None

        if node.solved():
            print("SOLUTION FOUND")
            print("solution level in tree: ", node.level)
            return node.find_parents()

        if node.level == 22:
            return None

        for move in node.moves():
            result = self.recursive_dls(Node(move, node))
            if result is not None:
                return result

        return None
