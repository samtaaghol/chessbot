from pieces import Pawn, Rook, Knight, Bishop, Queen, King
import numpy as np

# This function couples one element with a list.
# e.g coupler(1, [1,2,3,4,5]) -> [(1,1), (1,2), (1,3), (1,4), (1,5)]
coupler = lambda pos, moves: map(lambda move: (pos, move), moves)


class Board:
    def __init__(self):

        self.current_color = -1
        self.board = np.full((8, 8), None)
        self.white_moves = []
        self.black_moves = []
        self.setup_board()
        self.setup_pieces()

        # Stores the piece objects
        self.pieces = [[p for p in row if p != None] for row in self.board]

    def setup_board(self):
        self.board[0] = [
            Rook(1),
            Knight(1),
            Bishop(1),
            Queen(1),
            King(1),
            Bishop(1),
            Knight(1),
            Rook(1),
        ]
        self.board[7] = [
            Rook(-1),
            Knight(-1),
            Bishop(-1),
            Queen(-1),
            King(-1),
            Bishop(-1),
            Knight(-1),
            Rook(-1),
        ]
        self.board[1], self.board[6] = [Pawn(1)] * 8, [Pawn(-1)] * 8

    def setup_pieces(self):
        for x in range(8):
            for y in range(8):
                if self.board[y][x] != None:
                    self.board[y][x].set_position(x, y)

    def get_available_moves(self):
        for piece in self.pieces:
            if piece.color == -1:
                self.white_moves += coupler(piece.get_pos(), piece.get_moves())
            if piece.color == 1:
                self.black_moves += coupler(piece.get_pos(), piece.get_moves())

    def empty(self, x, y):
        return self.get(x, y) == None

    def get(self, x, y):
        return self.board[y][x]

    def get_king_pos(self):
        for piece in self.pieces:
            if isinstance(piece, King) and piece.color == self.current_color:
                return piece.get_pos()

    def in_check(self):
        for piece in self.pieces:
            if piece.color != self.current_color:
                if self.get_king_pos() in piece.get_moves():
                    return True
        return False

    def moves_into_check(self, move):
        self.move(move)
        if self.in_check():
            self.move(move[::-1])
            return True
        return False

    def move(self, move):
        if move in (self.white_moves if self.current_color == -1 else self.black_moves):
            start, end = move
            self.board[end[1]][end[0]] = self.board[start[1]][start[0]]
            self.board[start[1]][start[0]] = None
