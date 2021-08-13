from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King
from pieces.pawn import Pawn
from pieces.rook import Rook
import numpy as np


class Board:
    def __init__(self):

        self.current_color = -1
        self.board = np.full((8, 8), None)
        self.setup_board()
        self.setup_pieces()

        # Stores the piece objects
        self.pieces = self.get_pieces()

        self.enemy_moves = []
        self.moves = self.get_available_moves()

    def get_pieces(self):
        pieces = []
        for row in self.board:
            for square in row:
                if square != None:
                    pieces.append(square)
        return pieces

    def setup_board(self):
        self.board[0] = [
            Rook(-1),
            Knight(-1),
            Bishop(-1),
            Queen(-1),
            King(-1),
            Bishop(-1),
            Knight(-1),
            Rook(-1),
        ]
        self.board[7] = [
            Rook(1),
            Knight(1),
            Bishop(1),
            Queen(1),
            King(1),
            Bishop(1),
            Knight(1),
            Rook(1),
        ]
        self.board[1], self.board[6] = [Pawn(1)] * 8, [Pawn(-1)] * 8

    def setup_pieces(self):
        for x in range(8):
            for y in range(8):
                if self.board[y][x] != None:
                    self.board[y][x].pos = (x, y)

    def get_available_moves(self):
        moves = []
        for piece in self.pieces:
            if piece.color == self.current_color:
                moves += piece.get_moves(self)

        return moves

    def empty(self, position):
        return self.get(position) == None

    def get(self, position):
        return self.board[position[1]][position[0]]

    def set(self, position, value):
        self.board[position[1]][position[0]] = value

    def in_check(self):
        return self.is_safe(self.get_king_pos())

    def get_king_pos(self):
        for piece in self.pieces:
            if isinstance(piece, King) and piece.color == self.current_color:
                return piece.pos

    def is_safe(self, pos):
        return pos in self.enemy_moves

    def moves_into_check(self, move):
        self.unchecked_move(move)
        if self.in_check():
            self.unchecked_move(move[::-1])
            return True
        return False

    def safe_move(self, move):
        if self.valid_move(move):
            self.unchecked_move(move)
            self.enemy_moves = self.get_available_moves()
            self.current_color *= -1
            self.moves = self.get_available_moves()

    def unchecked_move(self, move):
        start, end = move
        self.set(end, self.get(start))
        self.set(start, None)

    """
    Checks if a move is valid in releation to the board. Meaning, there is a piece at the location.
    And everything takes place on the board.
    """

    def valid_move(self, move):
        return (
            self.in_bounds(move[0])
            and self.in_bounds(move[1])
            and self.get(move[0]) != None
        )

    """
    Returns if the given coordinates point to somewhere on the chessboard
    """

    @staticmethod
    def in_bounds(position):
        x, y = position
        return (0 <= x <= 7) and (0 <= y <= 7)
