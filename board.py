from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King
from pieces.pawn import Pawn
from pieces.rook import Rook
import numpy as np


def rnge(a, b):
    return range(a, b) if a < b else range(a, b, -1)


class Board:
    def __init__(self):

        self.current_color = 1
        self.board = np.full((8, 8), None)
        self.setup_board()
        self.setup_pieces()
        self.king_is_checked = False

        self.checkers = []
        self.enemy_moves = []
        self.moves = self.get_available_moves()

    """
    Gets all of the pieces on the board.
    """

    def get_pieces(self):
        pieces = []
        for row in self.board:
            for square in row:
                if square != None:
                    pieces.append(square)
        return pieces

    """
    Sets up the board by assign the pieces to their correct positions.
    """

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

        self.board[1] = [
            Pawn(-1),
            Pawn(-1),
            Pawn(-1),
            Pawn(-1),
            Pawn(-1),
            Pawn(-1),
            Pawn(-1),
            Pawn(-1),
        ]

        self.board[6] = [
            Pawn(1),
            Pawn(1),
            Pawn(1),
            Pawn(1),
            Pawn(1),
            Pawn(1),
            Pawn(1),
            Pawn(1),
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

    """
    Sets up the pieces by assigning them their positions.
    """

    def setup_pieces(self):
        for x in range(8):
            for y in range(8):
                if self.get((x, y)) != None:
                    self.get((x, y)).pos = (x, y)

    """
    Gets all the available move all the friendly pieces can make.
    """

    def get_available_moves(self):
        moves = []
        for piece in self.get_pieces():
            if piece.color == self.current_color:
                moves += piece.get_moves(self)

        return moves

    """
    Returns whether a given square is empty.
    """

    def empty(self, position):
        return self.get(position) == None

    """
    Gets the piece/None at a given positino.
    """

    def get(self, position):
        return self.board[position[1]][position[0]]

    """
    Sets a given coordinate on the board to a value.
    """

    def set(self, position, value):
        self.board[position[1]][position[0]] = value

    """
    Returns whether the piece at a given position is hostile.
    """

    def is_enemy(self, position):
        if self.get(position) == None:
            return False
        return self.get(position).color != self.current_color

    """
    Returns whether the friendly king is in check.
    """

    def in_check(self):
        return not self.is_safe(self.get_king_pos())

    """
    Returns the position of the friendly king.
    """

    def get_king_pos(self):
        for piece in self.get_pieces():
            if isinstance(piece, King) and piece.color == self.current_color:
                return piece.pos

    """
    Checks if a position on the board is free to move/capture.
    """

    def is_safe(self, pos):
        for enemy_attack in self.enemy_moves:
            if pos == enemy_attack[1]:
                return False
        return True

    """
    Moves a piece making sure it obeys the rules of chess.
    """

    def safe_move(self, move):

        # If the entered move is a valid move.
        if move in self.moves:

            # perform the physical move.
            self.unchecked_move(move)

            # change the current color flag.
            self.current_color *= -1

            # get the squares the enemy is attacking.
            self.enemy_moves = self.get_attacked_squares()

            # check if the new king is in those squares.
            self.king_is_checked = self.in_check()

            # get the new moves for the new team.
            self.moves = self.get_available_moves()

            # gets a list of pieces causing check if there are any.
            self.checkers = self.get_pieces_causing_check()

            self.king_is_checked = False

    """
    Moves a piece without checking if it follows the rules of chess.
    """

    def unchecked_move(self, move):
        start, end = move
        self.set(end, self.get(start))
        self.set(start, None)
        self.get(end).move(end)

    """
    Gets the squares attacked/threatend by enemy pieces.
    """

    def get_attacked_squares(self):
        squares = []
        for piece in self.get_pieces():
            if piece.color != self.current_color:
                squares += piece.get_defending_squares(self)
        return squares

    """
    Returns whether a given piece defends a square. defense = (Piece Location, Square Defended)
    """

    def valid_defense(self, defense):
        # If the start and end of the defense are in bounds.
        if not self.move_in_bounds(defense):
            return False

        # If the piece cant see what its defending.
        if not self.path_clear(defense):
            return False

        else:
            return True

    """
    Checks if a move is valid and follows the rules of chess.
    """

    def valid_move(self, move):

        # If the start and end of the move are not in bounds.
        if not self.move_in_bounds(move):
            return False

        # If the position of the start doesnt contain a piece.
        if self.empty(move[0]) == None:
            return False

        # If the desination and the journey of a move are both invalid.
        if not self.valid_move_journey(move):
            return False

        # If the king is in check and this move doesnt bring him out of check.
        if self.king_is_checked and not self.moves_out_of_check(move):
            return False

        # If this move leaves the king in check.
        if self.moves_into_check(move):
            return False

        else:
            return True

    """
    Returns whether the start and end of the move are both in bounds.
    """

    def move_in_bounds(self, move):
        return self.in_bounds(move[0]) and self.in_bounds(move[1])

    """
    If the destination and the journey of a move are both valid
    """

    def valid_move_journey(self, move):
        p1 = self.get(move[0])
        p2 = self.get(move[1])
        return p1.valid_target(p2) and self.path_clear(move)

    """
	Checks if all the squares on a given moves path are empty.
	"""

    def path_clear(self, move):
        return all(map(self.empty, self.path(move)))

    """
	Generates the path a piece takes on a move.
	"""

    def path(self, move):

        # Gets the range of the start x/y to the end x/y
        x_vals = rnge(move[0][0], move[1][0])
        y_vals = rnge(move[0][1], move[1][1])

        # horizontal or vertical, one of the arrays will have length 0.
        if not x_vals:
            x_vals = [move[0][0]] * len(y_vals)

        if not y_vals:
            y_vals = [move[0][1]] * len(x_vals)

        return list(zip(x_vals, y_vals))[1:]

    """
    Returns whether the given move takes our king out of check.
    """

    def moves_out_of_check(self, move):

        piece = self.get(move[0])

        # If the piece to move is a king.
        if isinstance(piece, King):

            # Make sure the king is not moving into an attacked square.
            return self.is_safe(move[1])

        # Get the pieces causing check.
        enemies = self.get_pieces_causing_check()

        # If 2 or more enemies are causing check the king must move.
        if len(enemies) >= 2:

            # As we already checked if the current piece is a king.
            return False

        # get the position of the enemy piece.
        e_pos = enemies[0]

        # If the attacking piece is a knight, there is no blocking.
        if isinstance(self.get(e_pos), Knight):

            # Return whether the move takes the attacking piece.
            return move[1] == e_pos

        # Get the kings position.
        k_pos = self.get_king_pos()

        # Get the path between the enemy and the king.
        e_k_path = self.path((k_pos, e_pos)) + [e_pos]

        # return whether the move blocks the enemies path to check.
        return move[1] in e_k_path

    """
    Returns an array containing the positions of pieces which cause check.
    """

    def get_pieces_causing_check(self):
        return [s for (s, e) in self.enemy_moves if e == self.get_king_pos()]

    """
    Checks if a move results in check.
    """

    def moves_into_check(self, move):
        # self.unchecked_move(move)
        # if self.in_check():
        #   self.unchecked_move(move[::-1])
        #   return True

        return False

    """
    Returns if the given coordinates point to somewhere on the chessboard
    """

    @staticmethod
    def in_bounds(position):
        x, y = position
        return (0 <= x <= 7) and (0 <= y <= 7)
