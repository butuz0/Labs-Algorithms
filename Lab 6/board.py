import copy
import math
from fox import Fox
from hound import Hound


class Board:
    def __init__(self, board: None or list, fox_pos: tuple, hounds_pos: list[tuple], screen=None):
        self.fox = Fox(screen, (fox_pos[0]*100, fox_pos[1]*100))
        self.hounds = [Hound(screen, (hounds_pos[i][0]*100, hounds_pos[i][1]*100)) for i in range(4)]
        self.board = board if board is not None else self.create_board()

    def create_board(self):
        board = [[0 for _ in range(8)] for _ in range(8)]
        x, y = self.fox.coords
        x = x // 100
        y = y // 100
        board[y][x] = "F"

        for hound in self.hounds:
            x, y = hound.coords
            x = x // 100
            y = y // 100
            board[y][x] = "H"

        return board

    def copy(self):
        board = copy.deepcopy(self.board)
        return Board(board,
                     self.fox.board_index,
                     [hound.board_index for hound in self.hounds])

    def evaluate(self):
        return len(self.fox.find_moves(self.board))**2.4 + \
               self.fox.board_index[1]**2.8 + \
               self.distance_to_hounds()

    # calculate sum of straight-line distances from fox to every hound
    def distance_to_hounds(self):
        distance = 0
        fox_col, fox_row = self.fox.board_index
        for hound in self.hounds:
            hound_col, hound_row = hound.board_index
            distance += math.sqrt((fox_col - hound_col) ** 2 + (fox_row - hound_row) ** 2)
        return distance

    # check if hounds have any possible moves. if not - hounds lost
    def hounds_lost(self):
        for hound in self.hounds:
            if hound.find_moves(self.board):
                return False
        return True

    def pprint(self):
        for row in self.board:
            print(row)
        print()

    def __getitem__(self, index):
        return self.board[index]
