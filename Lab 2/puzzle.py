import random


class Puzzle:
    def __init__(self, board):
        self.board = board
        self.goal = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]

    def solved(self):
        return self.board == self.goal

    def find_moves(self):
        i = -1
        j = -1
        moves = []
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == 0:
                    i = x
                    j = y
                    break

        directs = {'R': (i, j - 1),
                   'L': (i, j + 1),
                   'U': (i + 1, j),
                   'D': (i - 1, j)}

        for action, (i1, j1) in directs.items():
            if 0 <= i1 < 3 and 0 <= j1 < 3:
                move = self.create_move((i, j), (i1, j1))
                moves.append(move)
        return moves

    def create_move(self, at, to):
        copy = self.copy()
        i, j = at
        i1, j1 = to
        copy.board[i][j], copy.board[i1][j1] = copy.board[i1][j1], copy.board[i][j]
        return copy

    def copy(self):
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def h(self):
        not_placed = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != self.goal[i][j] and self.board[i][j] != 0:
                    not_placed += 1
        return not_placed

    def pprint(self):
        for i in range(3):
            print(self.board[i])
        print()

    def shuffle_board(self):        # used for testing
        for i in range(random.randint(20, 40)):
            self.board = self.rand_find_moves()[random.randint(0, len(self.rand_find_moves())-1)].board

    def rand_find_moves(self):          # used for testing
        i = -1
        j = -1
        moves = []
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == 0:
                    i = x
                    j = y
                    break

        directs = {'R': (i, j - 1),
                   'L': (i, j + 1),
                   'U': (i + 1, j),
                   'D': (i - 1, j)}

        l = list(directs.items())
        random.shuffle(l)
        directs = dict(l)

        for action, (i1, j1) in directs.items():
            if 0 <= i1 < 3 and 0 <= j1 < 3:
                move = self.create_move((i, j), (i1, j1))
                moves.append(move)
        return moves