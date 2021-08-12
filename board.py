from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from itertools import zip_longest
import numpy as np

class Board:
    
    def __init__(self):
        
        self.current_color = -1
        self.board = []
        self.squares_attacked_by_white = []
        self.squares_attacked_by_black = []
        self.setup_pieces()
    
    def setup_pieces(self):
        self.board += [[Rook(-1), Knight(-1), Bishop(-1), Queen(-1), King(-1), Bishop(-1), Knight(-1), Rook(-1)]]
        self.board += [[Pawn(-1)] * 8]]
        self.board += [[[None] * 8]] * 4]
        self.board += [[Pawn(1)] * 8]]
        self.board += [[Rook(-1), Knight(-1), Bishop(-1), King(-1), Queen(-1), Bishop(-1), Knight(-1), Rook(-1)]]
    
    def get_available_moves(self):
        moves = []
        for row in self.board:
            for piece in row:
                if piece != null and piece.color == self.current_color:
                    for move in piece.get_moves(self):
                        moves.append(((piece.x, piece.y), move))
    
    def get(self, x, y):
        return self.board[y][x]
    
    def get_king_pos(self):
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == self.current_color:
                    return king.get_pos()
    
    def leaves_check(self, move):
        
    
    def move(self, move):
        self.board