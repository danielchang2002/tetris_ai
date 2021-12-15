from board import Board
from greedy import Greedy_AI

from genetic import Genetic_AI
from mcts import MCTS_AI
from piece import Piece
import pygame

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = (0, 255, 0)


class Game:
    def __init__(self, mode, agent=None):
        self.board = Board()
        self.curr_piece = Piece()
        self.y = 20
        self.x = 5
        self.screenWidth = 400
        self.screenHeight = 800
        self.top = 0
        self.pieces_dropped = 0
        self.rows_cleared = 0
        if mode == "greedy":
            self.ai = Greedy_AI()
        elif mode == "genetic":
            if agent == None:
                self.ai = Genetic_AI()
            else:
                self.ai = agent
        elif mode == "mcts":
            self.ai = MCTS_AI()
        else:
            self.ai = None

    def run_no_visual(self):
        if self.ai == None:
            return -1
        while True:
            x, piece = self.ai.get_best_move(self.board, self.curr_piece)
            self.curr_piece = piece
            y = self.board.drop_height(self.curr_piece, x)
            self.drop(y, x=x)
            if self.board.top_filled():
                break
        print(self.pieces_dropped, self.rows_cleared)
        return self.pieces_dropped, self.rows_cleared

    def run(self):
        pygame.init()
        self.screenSize = self.screenWidth, self.screenHeight
        self.pieceHeight = (self.screenHeight - self.top) / self.board.height
        self.pieceWidth = self.screenWidth / self.board.width
        self.screen = pygame.display.set_mode(self.screenSize)
        running = True
        if self.ai != None:
            MOVEEVENT, t = pygame.USEREVENT + 1, 100
        else:
            MOVEEVENT, t = pygame.USEREVENT + 1, 500
        pygame.time.set_timer(MOVEEVENT, t)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.ai != None:
                    if event.type == MOVEEVENT:
                        # if event.type == pygame.KEYDOWN:
                        x, piece = self.ai.get_best_move(self.board, self.curr_piece)
                        self.curr_piece = piece
                        y = self.board.drop_height(self.curr_piece, x)
                        self.drop(y, x=x)
                        if self.board.top_filled():
                            running = False
                            break
                    continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        y = self.board.drop_height(self.curr_piece, self.x)
                        self.drop(y)
                        if self.board.top_filled():
                            running = False
                            break
                    if event.key == pygame.K_a:
                        if self.x - 1 >= 0:
                            occupied = False
                            for b in self.curr_piece.body:
                                if self.y + b[1] >= self.board.width:
                                    continue
                                if self.board.board[self.y + b[1]][self.x + b[0] - 1]:
                                    occupied = True
                                    break
                            if not occupied:
                                self.x -= 1
                    if event.key == pygame.K_d:
                        if self.x + 1 <= self.board.width - len(self.curr_piece.skirt):
                            occupied = False
                            for b in self.curr_piece.body:
                                if self.y + b[1] >= self.board.width:
                                    continue
                                if self.board.board[self.y + b[1]][self.x + b[0] + 1]:
                                    occupied = True
                                    break
                            if not occupied:
                                self.x += 1
                    if event.key == pygame.K_w:
                        self.curr_piece = self.curr_piece.get_next_rotation()
                if event.type == MOVEEVENT:
                    if self.board.drop_height(self.curr_piece, self.x) == self.y:
                        self.drop(self.y)
                        if self.board.top_filled():
                            running = False
                        break
                    self.y -= 1
            self.screen.fill(BLACK)
            self.draw()
            pygame.display.flip()
        pygame.quit()
        # print("Game information:")
        print("Pieces dropped:", self.pieces_dropped)
        print("Rows cleared:", self.rows_cleared)
        return self.pieces_dropped, self.rows_cleared

    def drop(self, y, x=None):
        if x == None:
            x = self.x
        self.board.place(x, y, self.curr_piece)
        self.x = 5
        self.y = 20
        self.curr_piece = Piece()
        self.pieces_dropped += 1
        self.rows_cleared += self.board.clear_rows()

    def draw(self):
        self.draw_pieces()
        self.draw_hover()
        self.draw_grid()

    def draw_grid(self):
        for row in range(0, self.board.height):
            start = (0, row * self.pieceHeight + self.top)
            end = (self.screenWidth, row * self.pieceHeight + self.top)
            pygame.draw.line(self.screen, WHITE, start, end, width=2)
        for col in range(1, self.board.height):
            start = (col * self.pieceWidth, self.top)
            end = (col * self.pieceWidth, self.screenHeight)
            pygame.draw.line(self.screen, WHITE, start, end, width=2)
        # border
        tl = (0, 0)
        bl = (0, self.screenHeight - 2)
        br = (self.screenWidth - 2, self.screenHeight - 2)
        tr = (self.screenWidth - 2, 0)
        pygame.draw.line(self.screen, WHITE, tl, tr, width=2)
        pygame.draw.line(self.screen, WHITE, tr, br, width=2)
        pygame.draw.line(self.screen, WHITE, br, bl, width=2)
        pygame.draw.line(self.screen, WHITE, tl, bl, width=2)

    def draw_pieces(self):
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.board[row][col]:
                    tl = (
                        col * self.pieceWidth,
                        (self.board.height - row - 1) * self.pieceHeight,
                    )
                    pygame.draw.rect(
                        self.screen,
                        self.board.colors[row][col],
                        pygame.Rect(tl, (self.pieceWidth, self.pieceHeight)),
                    )

    def draw_hover(self):
        for b in self.curr_piece.body:
            tl = (
                (self.x + b[0]) * self.pieceWidth,
                (self.board.height - (self.y + b[1]) - 1) * self.pieceHeight,
            )
            pygame.draw.rect(
                self.screen,
                self.curr_piece.color,
                pygame.Rect(tl, (self.pieceWidth, self.pieceHeight)),
            )
