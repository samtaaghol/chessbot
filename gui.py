import pygame
from pygame.locals import *
from board import Board
import math

square_width = int(500 / 8)


class Chess_Gui:
    def __init__(self):

        self.screen = pygame.display.set_mode((square_width * 8, square_width * 8))
        self.game = Board()
        self.clock = pygame.time.Clock()

        self.show_threatened_squares = False

        pygame.init()
        self.font = pygame.font.SysFont("monospace", 60)
        self.run()

    def run(self):

        counter = 0

        self.click1 = None
        self.click2 = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    pos = ((x // square_width), (y // square_width))
                    if self.click1 == None:
                        self.click1 = pos
                    else:
                        self.click2 = pos
                        self.game.safe_move((self.click1, self.click2))
                        self.click1, self.click2 = None, None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.show_threatened_squares = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.show_threatened_squares = False

            self.setup_board()

            pygame.display.update()

    @staticmethod
    def quit():

        pygame.display.quit()
        pygame.quit()

    def setup_board(self):

        self.screen.fill((0, 0, 0))
        for x in range(8):
            for y in range(8):
                self.draw_square(x, y)
                if self.game.get((x, y)) != None:
                    self.draw_piece(x, y, self.game.get((x, y)))
        # if self.click1 != None:
        #    self.piece_moves()
        self.draw_moves()
        if self.show_threatened_squares:
            self.draw_threatened()
        pygame.display.update()

    def piece_moves(self):
        for (start, (x, y)) in self.game.get(self.click1).get_moves(self.game):
            pygame.draw.circle(
                self.screen,
                (0, 0, 255),
                (
                    x * square_width + square_width // 2,
                    y * square_width + square_width // 2,
                ),
                square_width // 4,
            )

    def draw_moves(self):
        for ((x1, y1), (x2, y2)) in self.game.moves:
            self.draw_arrow(
                (0, 0, 0),
                (
                    x1 * square_width + square_width / 2,
                    y1 * square_width + square_width / 2,
                ),
                (
                    x2 * square_width + square_width / 2,
                    y2 * square_width + square_width / 2,
                ),
            )

    def draw_threatened(self):
        for (start, (x, y)) in self.game.enemy_moves:
            pygame.draw.circle(
                self.screen,
                (0, 0, 255),
                (
                    x * square_width + square_width // 2,
                    y * square_width + square_width // 2,
                ),
                square_width // 4,
            )

    def draw_piece(self, x, y, piece):

        piece = pygame.image.load(
            "pieces\\images\\" + piece.__class__.__name__ + str(piece.color) + ".png"
        )
        piece = pygame.transform.scale(piece, (square_width, square_width))
        self.screen.blit(piece, (x * square_width, y * square_width))

    def draw_square(self, x, y):

        white = (255, 255, 255)
        green = (152, 251, 152)
        color = green
        if (x + y) % 2 == 0:
            color = white
        pygame.draw.rect(
            self.screen,
            color,
            (x * square_width, y * square_width, square_width, square_width),
        )

    def draw_arrow(self, colour, start, end):
        pygame.draw.line(self.screen, colour, start, end, 2)
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
        pygame.draw.polygon(
            self.screen,
            (255, 0, 0),
            (
                (
                    end[0] + 10 * math.sin(math.radians(rotation)),
                    end[1] + 10 * math.cos(math.radians(rotation)),
                ),
                (
                    end[0] + 10 * math.sin(math.radians(rotation - 120)),
                    end[1] + 10 * math.cos(math.radians(rotation - 120)),
                ),
                (
                    end[0] + 10 * math.sin(math.radians(rotation + 120)),
                    end[1] + 10 * math.cos(math.radians(rotation + 120)),
                ),
            ),
        )


chess = Chess_Gui()
chess.run()
