""" 
Generic Piece class type to be inherited by all pieces.  

color is stored as (-1, 1) = (White, Black)
"""

from itertools import zip_longest as zipl


"""
Works like the builtin range function without requiring a step to be
entered.
"""


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
    Moves a piece to a given coordinate
    """

    def move(self, end):
        self.pos = end

    """
	Returns whether the destination square is a valid square to move to.
	"""

    def valid_target(self, piece):
        return piece == None or piece.color != self.color

    """
    Gets all the squares a piece is defending.
    """

    def get_defending_squares(self, board):
        defended = []

        for (x, y) in self.vectors:
            defense = (self.pos, (self.pos[0] + x, self.pos[1] + y))

            if board.valid_defense(defense):
                defended.append(defense)

        return defended

    """
	Gets all the available moves for this piece.
	TODO: optimize for moves contained within larger moves.
	TODO: Check for checks.
	"""

    def get_moves(self, board):
        moves = []

        for (x, y) in self.vectors:

            # Applies the vector to our current position
            move = (self.pos, (self.pos[0] + x, self.pos[1] + y))

            # If the vector from start_pos to end_pos results in a valid move.
            if board.valid_move(move):

                # Add the end_pos to the list of moves considered valid.
                moves.append(move)

        return moves

    """
	The vectors each piece generates is dependent on the piece.
	"""

    def get_vectors(self):
        pass


"""
TODO: vector generation may need to be modified for optimisation.
"""
