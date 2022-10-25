from puzzle import Puzzle
from solution import Solution
import time


def solve(method, board):
    puzzle = Puzzle(board)
    print("your puzzle:")
    puzzle.pprint()
    solution = Solution(puzzle)
    start = time.time()
    if method == "a_star":
        path = solution.a_star()
    elif method == "dls":
        path = solution.dls()
    else:
        print("wrong method!")
        return
    end = time.time()
    if path is not None:
        for node in path:
            node.puzzle.pprint()
        print("finding solution time: ", end - start)
    return path


def test(num, board):
    for i in range(num):
        print("-" * 30 + "\n")
        puzzle = Puzzle(board)
        puzzle.shuffle_board()
        solution = Solution(puzzle)
        puzzle.pprint()
        print("\nA* solution: ")
        start = time.time()
        res1 = solution.a_star()
        print("time: ", time.time() - start)
        print("\nDLS solution: ")
        start = time.time()
        res2 = solution.dls()
        print("time: ", time.time() - start)


board = [[4, 0, 1],
         [7, 2, 5],
         [8, 3, 6]]

res1 = solve("a_star", board)
res2 = solve("dls", board)
