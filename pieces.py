""" 
Generic Piece class type to be inherited by all pieces.  

color is stored as (-1, 1) = (White, Black)
"""

from itertools import zip_longest


# This range function excludes start.
def excl_range(start, end, step):
    if step > 0:
        return list(range(start + 1, end, step))
    return list(range(start - 1, end, step))


class Piece:
    def __init__(self, color, position):
        self.color = color
        self.x, self.y = position
        self.vectors = self.get_vectors()
        self.moves = self.get_available_moves()

    """
    Returns the position of the piece
    """

    def get_position(self):
        return (self.x, self.y)

    """
    Generates the path from our piece to the given (a,b) coordinate.
    """

    def path(self, a, b):

        # Gets the x and y path values by using an exclusive range.
        # The step is whether the coordinate is left/right or below/above.
        x_vals = excl_range(self.x, a, self.is_left(a))
        y_vals = excl_range(self.y, b, self.is_above(b))

        # If one of the lists are empty, then the path must be straight
        # hence all the x/y values will be constant.
        const = a if not y_vals else b

        # Zip the two lists together, if one list is empty fill with the constant.
        return zip_longest(x_vals, y_vals, fillvalue=const)

    """
    Checks if all the squares on a given moves path are empty.
    """

    def path_clear(self, board, a, b):
        return all([board.empty(square) for square in self.path(a, b)])

    """
    Returns if the coordinate is right of the piece. (-1 : left, 0 : center, 1 : right)
    """

    def is_right(self, a):
        delta = a - self.x
        if delta == 0:
            return 0
        return delta / abs(delta)

    """
    Returns if the coordinate is above of the piece. (-1 : below, 0 : center, 1 : above)
    """

    def is_above(self, b):
        delta = self.y - b
        if delta == 0:
            return 0
        return delta / abs(delta)

    """
    Checks if a given vector is a valid move for a piece.
    """

    def valid_move(self, board, a, b):
        end_is_not_friend = board.get_piece().color != self.color
        path_is_clear = self.path_clear(board, self.x + a, self.y + b)
        return end_is_not_friend and path_is_clear

    """
    Gets all the available moves for this piece.
    TODO: optimize for moves contained within larger moves.
    TODO: Check for checks.
    """

    def get_available_moves(self, board):
        moves = []
        for (x, y) in self.vectors:
            if self.valid_move(board, x, y):
                moves.append((self.x + x, self.y + y))
        return moves

    """
    The vectors each piece generates is dependent on the piece.
    """

    def get_vectors(self):
        pass


class Pawn(Piece):
    def get_vectors(self):
        return [(0, self.c), (0, 2 * self.c)]

    def get_available_moves(self, board):
        return


class Rook(Piece):
    def get_vectors(self):
        return [(0, self.c), (0, 2 * self.c)]


class Knight(Piece):
    def get_vectors(self):
        return [(0, self.c), (0, 2 * self.c)]


class Bishop(Piece):
    def get_vectors(self):
        return [(0, self.c), (0, 2 * self.c)]


class Queen(Piece):
    def get_vectors(self):
        return [(0, self.c), (0, 2 * self.c)]


class King(Piece):
    def get_vectors(self):
        return [(0, self.c), (0, 2 * self.c)]
