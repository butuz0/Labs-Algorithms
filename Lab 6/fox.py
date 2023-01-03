from piece import Piece


class Fox(Piece):
    def __init__(self, screen, coords, name="fox"):
        super().__init__(screen, coords, name)

    def find_moves(self, board: list):
        x, y = self.board_index
        moves = []

        directs = {"bottom-left": (y+1, x-1),
                   "bottom-right": (y+1, x+1),
                   "top-left": (y-1, x-1),
                   "top-right": (y-1, x+1)}

        for action, (y1, x1) in directs.items():
            if 0 <= y1 < 8 and 0 <= x1 < 8 and board[y1][x1] == 0:
                moves.append((x1, y1))
        return moves

    # check if fox has reached the opposite side of the board
    def won(self):
        return self.board_index[1] == 7

    # check if fox has any possible moves. if not - fox lost
    def lost(self, board: list):
        if not self.find_moves(board):
            return True
        return False
