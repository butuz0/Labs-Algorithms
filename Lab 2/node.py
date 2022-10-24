from puzzle import Puzzle


class Node:
    def __init__(self, puzzle: Puzzle, parent=None):
        self.puzzle = puzzle
        self.parent = parent
        if self.parent is not None:
            self.level = parent.level + 1
        else:
            self.level = 0

    def f(self):
        return self.level + self.h()

    def h(self):
        return self.puzzle.h()

    def find_parents(self):
        node = self
        p = []
        while node:
            p.append(node)
            node = node.parent
        return reversed(p)

    def solved(self):
        return self.puzzle.solved()

    def __lt__(self, other):
        return self.f() < other.f()

    def __gt__(self, other):
        return self.f() > other.f()

    def moves(self):
        return self.puzzle.find_moves()
