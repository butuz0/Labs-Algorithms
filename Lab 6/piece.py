import pygame


class Piece:
    def __init__(self, screen, coords: tuple, name: str):
        self.name = name
        if screen is not None:
            self.screen = screen
            self.image = pygame.image.load(f"images/{name}.png")
            self.screen_rect = screen.get_rect()
        self.coords = coords
        self.board_index = (self.coords[0]//100, self.coords[1]//100)

    def output(self):
        self.screen.blit(self.image, self.coords)

    def move(self, coords: tuple, board: list):
        x, y = coords
        self.coords = (x, y)
        j0, i0 = self.board_index
        self.board_index = (self.coords[0]//100, self.coords[1]//100)
        j, i = self.board_index
        board[i0][j0], board[i][j] = board[i][j], board[i0][j0]

    # returns coordinates of all possible move for the chosen object
    def find_moves(self, board):
        pass
