""" 
Generic Piece class type to be inherited by all pieces.  

color is stored as (-1, 1) = (White, Black)
"""

from itertools import zip_longest as zipl

sign = lambda a: (a > 0) - (a < 0)


class Piece:
    def __init__(self, color):
        self.color = color
        self.vectors = []
        self.get_vectors()
        self.position = None

    def __str__(self):
        return self.__class__.__name__[:4]

    def __repr__(self):
        return self.__class__.__name__[:4]

    """
	Sets the position of the piece.
	"""

    def set_position(self, x, y):
        self.position = (x, y)

    """
	Returns the position of the piece.
	"""

    def get_pos(self):
        return (self.x, self.y)

    """
	Returns if the given coordinate points to an enemy piece.
	"""

    def is_enemy(self, board, pos):

        piece = board.get(pos[0], pos[1])

        if piece == None:
            return False

        return piece.color != self.color

    """
	Generates the path from our piece to the given (a,b) coordinate.
	"""

    def path(self, a, b):

        # Gets the x and y path values by using an exclusive range.
        # The step is whether the coordinate is left/right or below/above.
        x_vals = range(self.x, a, sign(a - self.x))
        y_vals = range(self.y, b, sign(self.y - b))

        # If one of the lists are empty, then the path must be straight
        # hence all the x/y values will be constant.
        const = a if not y_vals else b

        # Zip the two lists together, if one list is empty fill with the constant.
        # And make sure to remove the first element as thats where this piece is.
        return list(zipl(x_vals, y_vals, fillvalue=const)[1:])

    """
	Checks if all the squares on a given moves path are empty.
	"""

    def path_clear(self, board, a, b):
        return all([board.empty(square) for square in self.path(a, b)])

    """
	Returns whether the destination square is a valid square to move to.
	"""

    def valid_target(self, board, a, b):
        end_is_not_friend = self.is_enemey(board, a, b)
        in_bounds = (-1 < a < 8) and (-1 < b < 8)
        return end_is_not_friend and in_bounds

    """
	Checks if a given vector is a valid move for a piece.
	"""

    def valid_move(self, board, a, b):
        return (
            self.valid_target(board, a, b)
            and self.path_clear(board, a, b)
            and not board.leaves_check((self.get_pos(), (a, b)))
        )

    """
	Gets all the available moves for this piece.
	TODO: optimize for moves contained within larger moves.
	TODO: Check for checks.
	"""

    def get_moves(self, board):
        moves = []
        for (x, y) in self.vectors:
            if self.valid_move(board, self.x + x, self.y + y):
                moves.append((self.x + x, self.y + y))
        return moves

    """
	The vectors each piece generates is dependent on the piece.
	"""

    def get_vectors(self):
        pass


"""
TODO: vector generation may need to be modified for optimisation.
"""
