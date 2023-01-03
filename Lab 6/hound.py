from piece import Piece


class Hound(Piece):
    def __init__(self, screen, coords, name="hound"):
        super().__init__(screen, coords, name)

    def find_moves(self, board: list):
        x, y = self.board_index
        moves = []

        directs = {"top-left": (y-1, x-1),
                   "top-right": (y-1, x+1)}

        for action, (y1, x1) in directs.items():
            if 0 <= y1 < 8 and 0 <= x1 < 8 and board[y1][x1] == 0:
                moves.append((x1, y1))
        return moves
