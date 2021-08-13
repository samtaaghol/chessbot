""" 
Generic Piece class type to be inherited by all pieces.  

color is stored as (-1, 1) = (White, Black)
"""

from itertools import zip_longest as zipl


"""
Works like the builtin range function without requiring a step to be
entered.
"""


def rnge(a, b):
    return range(a, b) if a < b else range(a, b, -1)


class Piece:
    def __init__(self, color):
        self.color = color
        self.vectors = []
        self.get_vectors()
        self.pos = None

    """
    String representation of a piece is just the name.
    """

    def __str__(self):
        return self.__class__.__name__[:4]

    """
    Print representation of our piece is just a string.
    """

    def __repr__(self):
        return self.__class__.__name__[:4]

    """
	Checks if all the squares on a given moves path are empty.
	"""

    def path_clear(self, board, dst):
        return all(map(board.empty, self.path(dst)))

    """
	Generates the path from our piece to the given (a,b) coordinate.
	"""

    def path(self, dst):

        # Gets the range of the start x/y to the end x/y
        x_vals = rnge(self.pos[0], dst[0])
        y_vals = rnge(self.pos[1], dst[1])

        # horizontal or vertical, one of the arrays will have length 0.
        if not x_vals:
            x_vals = [self.pos[0]] * len(y_vals)

        if not y_vals:
            y_vals = [self.pos[0]] * len(x_vals)

        return list(zip(x_vals, y_vals))

    """
	Returns whether the destination square is a valid square to move to.
	"""

    def valid_target(self, board, dst):
        return board.in_bounds(dst) and (
            board.get(dst) == None or board.get(dst).color != self.color
        )

    """
	Checks if a given vector is a valid move for a piece.
	"""

    def valid_move(self, board, dst):
        return (
            board.in_bounds(dst)
            # If the destination of the piece is not friendly.
            and self.valid_target(board, (dst[0], dst[1]))
            # If the path to the destination has no obstructions
            and self.path_clear(board, (dst[0], dst[1]))
            # If the move does not leave the king in check.
            and not board.moves_into_check((self.pos, (dst[0], dst[1])))
        )

    """
	Gets all the available moves for this piece.
	TODO: optimize for moves contained within larger moves.
	TODO: Check for checks.
	"""

    def get_moves(self, board):
        moves = []
        for (x, y) in self.vectors:

            # Applies the vector to our current position
            new_position = (self.pos[0] + x, self.pos[1] + y)

            # If the vector from start_pos to end_pos results in a valid move.
            if self.valid_move(board, new_position):

                # Add the end_pos to the list of moves considered valid.
                moves.append(new_position)

        # Formats the move into the (start_pos, end_pos) format.
        return map(self.format_move, moves)

    def format_move(self, end):
        return (self.pos, end)

    """
	The vectors each piece generates is dependent on the piece.
	"""

    def get_vectors(self):
        pass


"""
TODO: vector generation may need to be modified for optimisation.
"""
