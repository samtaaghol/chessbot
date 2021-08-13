import pygame
from pygame.locals import *
from board import Board

square_width = int(1000 / 8)


class Chess_Gui:
    def __init__(self):

        self.screen = pygame.display.set_mode((1000, 1000))
        self.game = Board()
        self.clock = pygame.time.Clock()
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 60)
        self.run()

    def run(self):

        counter = 0

        click1 = None
        click2 = None

        print(self.game.moves)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    pos = ((x // square_width), (y // square_width))
                    print(pos)
                    if click1 == None:
                        click1 = pos
                    else:
                        click2 = pos
                        self.game.safe_move((click1, click2))
                        click1, click2 = None, None

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
        pygame.display.update()

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


chess = Chess_Gui()
chess.run()
