import random
import time
import sys
import pygame
from board import Board

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Fox and Hounds")
        self.board = Board(board=None,
                           fox_pos=(random.randrange(1, 7, 2), 0),
                           hounds_pos=[(2 * i, 7) for i in range(4)],
                           screen=self.screen)
        self.available_moves = []
        self.active_object = None
        self.available_moves = []
        self.active_object = None
        self.alpha = float("-inf")
        self.beta = float("inf")
        self.depth = 0

    # main menu of the game, where player chooses the game mode: player vs player or player vs ai
    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[1] < 400:
                        self.player_vs_player()
                    else:
                        self.__difficulty_selector()
                    return

            self.screen.fill(BLACK)
            image_p_vp_p = pygame.image.load(f"images/playervsplayer.png")
            self.screen.blit(image_p_vp_p, (275, 150))

            image_p_vp_ai = pygame.image.load(f"images/playervsai.png")
            self.screen.blit(image_p_vp_ai, (275, 500))

            pygame.display.flip()

    # appears if player has chosen player vs ai option. here player selects the difficulty of the game,
    # which depends on how deep the alpha-beta pruning algorithm will search.
    # for easy, medium and hard modes the depth is 3, 5 and 7
    def __difficulty_selector(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos_y = pygame.mouse.get_pos()[1]
                    if pos_y < 233:     # if easy difficulty - depth = 3
                        self.depth = 3
                    elif pos_y < 466:   # if medium difficulty - depth = 5
                        self.depth = 5
                    else:               # if hard difficulty - depth = 7
                        self.depth = 7
                    self.player_vs_ai()
                    return

            self.screen.fill(BLACK)

            image_easy = pygame.image.load(f"images/easy.png")
            self.screen.blit(image_easy, (275, 100))

            image_medium = pygame.image.load(f"images/medium.png")
            self.screen.blit(image_medium, (275, 300))

            image_hard = pygame.image.load(f"images/hard.png")
            self.screen.blit(image_hard, (275, 500))

            pygame.display.flip()

    def player_vs_player(self):
        fox_turn = True
        draw_moves = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    pos = (pos[0] // 100, pos[1] // 100)
                    if self.board[pos[1]][pos[0]]:      # if fox or hound was clicked - show available moves
                        if fox_turn:
                            if pos == self.board.fox.board_index:
                                self.__save_available_moves(
                                    self.board.fox.find_moves(self.board.board))
                                self.active_object = self.board.fox
                                draw_moves = True
                        else:
                            for hound in self.board.hounds:
                                if pos == hound.board_index:
                                    self.active_object = hound
                                    self.__save_available_moves(hound.find_moves(self.board.board))
                                    draw_moves = True
                                    break
                    else:
                        for move in self.available_moves:       # if available move was clicked - move object
                            if pos == move[0]:
                                self.active_object.move((move[1][0] - 50, move[1][1] - 50), self.board)

                                self.available_moves = []
                                draw_moves = False
                                fox_turn = not fox_turn
                                break

            self.__fill_board()

            if draw_moves:
                self.__show_available_moves()

            pygame.display.flip()

    def player_vs_ai(self):
        fox_turn = True
        first_run = True
        draw_moves = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    pos = (pos[0] // 100, pos[1] // 100)
                    if self.board[pos[1]][pos[0]]:      # if hound was clicked - show available moves
                        for hound in self.board.hounds:
                            if pos == hound.board_index:
                                self.active_object = hound
                                self.__save_available_moves(hound.find_moves(self.board.board))
                                draw_moves = True
                                break
                    else:
                        for move in self.available_moves:   # if available move was clicked - move object
                            if pos == move[0]:
                                self.active_object.move((move[1][0] - 50, move[1][1] - 50), self.board)

                                self.available_moves = []
                                draw_moves = False
                                fox_turn = True
                                break

            self.__fill_board()

            if draw_moves:
                self.__show_available_moves()

            pygame.display.flip()

            if fox_turn:
                if first_run:
                    time.sleep(0.5)
                if not self.board.fox.lost(self.board):
                    self.__ai_fox_move()
                fox_turn = False

    # display the game board
    def __fill_board(self):
        self.__draw_board()

        if self.board.fox.won() or self.board.hounds_lost():
            text = pygame.font.Font('freesansbold.ttf', 64).render('FOX WON!', True, GOLD)
            self.screen.blit(text, (235, 340))

        if self.board.fox.lost(self.board):
            text = pygame.font.Font('freesansbold.ttf', 64).render('HOUNDS WON!', True, GOLD)
            self.screen.blit(text, (160, 340))

        if self.board.fox.won() or self.board.hounds_lost() or self.board.fox.lost(self.board):
            pygame.display.flip()
            self.__draw_board()
            time.sleep(2)
            sys.exit()

    # draws the board, fox and hounds on the game screen
    def __draw_board(self):
        self.screen.fill(BLACK)
        for row in range(8):
            for col in range(row % 2, 8, 2):
                pygame.draw.rect(self.screen, WHITE, (row * 100, col * 100, 100, 100))

        self.board.fox.output()
        for hound in self.board.hounds:
            hound.output()

    # draws all possible moves of the chosen element
    def __show_available_moves(self):
        for move in self.available_moves:
            pygame.draw.circle(self.screen, GOLD, move[1], 25)

    def __save_available_moves(self, moves: list[tuple]):
        self.available_moves = []
        for move in moves:
            self.available_moves.append((move, (move[0] * 100 + 50, move[1] * 100 + 50)))

    # creates all possible move of the element and returns list of boards where all of those moves were made
    def __create_all_moves(self, board: Board, object_coords: tuple):
        all_moves = []
        moves = self.__find_possible_moves(board, object_coords)
        for move in moves:
            board_copy = board.copy()
            all_moves.append(self.__create_single_move(board_copy, object_coords, move))
        return all_moves

    @staticmethod
    # makes a single move and returns board with this move
    def __create_single_move(board: Board, at: tuple, to: tuple):
        if board.fox.board_index == at:
            board.fox.move((to[0] * 100, to[1] * 100), board)
        else:
            for hound in board.hounds:
                if hound.board_index == at:
                    hound.move((to[0] * 100, to[1] * 100), board)
        return board, to

    @staticmethod
    # returns coordinates of all possible move for the chosen object
    def __find_possible_moves(board: Board, pos: tuple):
        x, y = pos
        moves = []

        directs = {"bottom-left": (y + 1, x - 1),
                   "bottom-right": (y + 1, x + 1),
                   "top-left": (y - 1, x - 1),
                   "top-right": (y - 1, x + 1)}

        if board[y][x] == "H":
            directs.pop("bottom-left")
            directs.pop("bottom-right")

        for action, (y1, x1) in directs.items():
            if 0 <= y1 < 8 and 0 <= x1 < 8 and board[y1][x1] == 0:
                moves.append((x1, y1))
        return moves

    # calculates the best move using alpha-beta pruning algorithm and makes the move
    def __ai_fox_move(self):
        move = self.__alpha_beta_decision(self.board, self.depth, self.alpha, self.beta, True)[1]
        self.board.fox.move((move[0]*100, move[1]*100), self.board)
        self.alpha = float("-inf")
        self.beta = float("inf")

    # alpha-beta pruning algorithm creates a tree of possible game conditions and is looking for the best moves for
    # MAX or MIN player based on evaluate function. alpha and beta contain values of the best moves for MAX and MIN
    # players, and moves, which are definitely worse than already found are pruned
    def __alpha_beta_decision(self, board: Board, depth, alpha, beta, max_player: bool):
        if depth == 0 or board.fox.won() or board.fox.lost(board):
            return board.evaluate(), None
        if max_player:
            value = float("-inf")
            children = self.__create_all_moves(board, board.fox.board_index)
            move = None
            for child in children:
                eval = self.__alpha_beta_decision(child[0], depth - 1, alpha, beta, False)[0]
                if eval > value:
                    value = eval
                    move = child[1]
                if value > self.beta:
                    break
                self.alpha = max(alpha, value)
            return value, move
        else:
            value = float("inf")
            children = []
            move = None
            for hound in board.hounds:
                children += self.__create_all_moves(board, hound.board_index)
            for child in children:
                eval = self.__alpha_beta_decision(child[0], depth - 1, alpha, beta, False)[0]
                if eval < value:
                    value = eval
                    move = child[1]
                if value < self.alpha:
                    break
                self.beta = min(beta, value)
            return value, move
